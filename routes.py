import os
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_, desc
from app import db
from models import User, Project, Category, Tag, Comment, Like, Achievement, ContactMessage, project_tags
from forms import (LoginForm, RegisterForm, ProjectForm, AchievementForm, CategoryForm, 
                  CommentForm, ContactForm, ProfileForm)
from utils import save_uploaded_file, delete_file, format_date, format_datetime, truncate_text, generate_linkedin_share_url

# Create blueprints
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
admin_bp = Blueprint('admin', __name__)

# Template filters
@main_bp.app_template_filter('format_date')
def format_date_filter(date):
    return format_date(date)

@main_bp.app_template_filter('format_datetime')
def format_datetime_filter(datetime_obj):
    return format_datetime(datetime_obj)

@main_bp.app_template_filter('truncate')
def truncate_filter(text, length=150):
    return truncate_text(text, length)

# Static file serving for uploads
@main_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded files"""
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# Main routes
@main_bp.route('/')
def index():
    """Homepage with featured projects and latest achievements"""
    # Get featured projects
    featured_projects = Project.query.filter_by(is_published=True, is_featured=True).limit(6).all()
    
    # Get latest projects if no featured ones
    if not featured_projects:
        featured_projects = Project.query.filter_by(is_published=True).order_by(desc(Project.created_at)).limit(6).all()
    
    # Get latest achievements
    latest_achievements = Achievement.query.filter_by(is_published=True).order_by(desc(Achievement.created_at)).limit(3).all()
    
    # Get real statistics from database
    total_projects = Project.query.filter_by(is_published=True).count()
    total_achievements = Achievement.query.filter_by(is_published=True).count()
    total_likes = Like.query.count()
    
    return render_template('index.html', 
                         featured_projects=featured_projects,
                         latest_achievements=latest_achievements,
                         stats={'projects': total_projects, 'achievements': total_achievements, 'likes': total_likes})

@main_bp.route('/projects')
def projects():
    """Projects listing with pagination and filtering"""
    page = request.args.get('page', 1, type=int)
    category_id = request.args.get('category', type=int)
    tag = request.args.get('tag')
    search = request.args.get('search', '')
    
    # Base query
    query = Project.query.filter_by(is_published=True)
    
    # Apply filters
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if tag:
        query = query.join(project_tags).join(Tag).filter(Tag.name == tag)
    
    if search:
        query = query.filter(or_(
            Project.title.contains(search),
            Project.description.contains(search)
        ))
    
    # Order by creation date
    query = query.order_by(desc(Project.created_at))
    
    # Paginate
    projects_pagination = query.paginate(
        page=page, per_page=9, error_out=False
    )
    
    # Get categories and tags for filters
    categories = Category.query.all()
    tags = Tag.query.all()
    
    return render_template('projects.html',
                         projects=projects_pagination.items,
                         pagination=projects_pagination,
                         categories=categories,
                         tags=tags,
                         current_category=category_id,
                         current_tag=tag,
                         search_query=search)

@main_bp.route('/project/<int:id>')
def project_detail(id):
    """Project detail page with comments and likes"""
    project = Project.query.get_or_404(id)
    
    if not project.is_published:
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Projeto não encontrado.', 'error')
            return redirect(url_for('main.projects'))
    
    # Get comments
    comments = Comment.query.filter_by(project_id=id).order_by(desc(Comment.created_at)).all()
    
    # Check if current user liked this project
    user_liked = False
    if current_user.is_authenticated:
        user_liked = Like.query.filter_by(user_id=current_user.id, project_id=id).first() is not None
    
    # Comment form
    comment_form = CommentForm()
    
    # LinkedIn share URL
    linkedin_url = generate_linkedin_share_url(
        project.title,
        project.description,
        request.url
    )
    
    # Related projects
    related_projects = Project.query.filter(
        Project.category_id == project.category_id,
        Project.id != project.id,
        Project.is_published == True
    ).limit(3).all()
    
    return render_template('project_detail.html',
                         project=project,
                         comments=comments,
                         comment_form=comment_form,
                         user_liked=user_liked,
                         linkedin_url=linkedin_url,
                         related_projects=related_projects)

@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with form"""
    form = ContactForm()
    
    if form.validate_on_submit():
        # Save message to database
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            subject=form.subject.data,
            message=form.message.data
        )
        
        db.session.add(message)
        db.session.commit()
        
        # Send email notification (requires email configuration)
        try:
            from utils import send_contact_email
            send_contact_email(
                name=form.name.data,
                email=form.email.data,
                subject=form.subject.data,
                message=form.message.data
            )
            flash('Mensagem enviada com sucesso! Retornaremos em breve.', 'success')
        except Exception as e:
            # Even if email fails, message is saved in database
            current_app.logger.warning(f'Email não pôde ser enviado: {e}')
            flash('Mensagem salva! Para receber por email, configure as credenciais SMTP.', 'info')
        
        return redirect(url_for('main.contact'))
    
    return render_template('contact.html', form=form)

@main_bp.route('/profile')
@login_required
def profile():
    """User profile page"""
    form = ProfileForm(obj=current_user)
    return render_template('profile.html', form=form)

@main_bp.route('/profile/edit', methods=['POST'])
@login_required
def edit_profile():
    """Edit user profile"""
    form = ProfileForm()
    
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.bio = form.bio.data
        
        # Handle profile image upload
        if form.profile_image.data:
            # Delete old image
            if current_user.profile_image:
                delete_file(current_user.profile_image)
            
            # Save new image
            filename = save_uploaded_file(form.profile_image.data, max_size=(300, 300))
            if filename:
                current_user.profile_image = filename
        
        db.session.commit()
        flash('Perfil atualizado com sucesso!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
    
    return redirect(url_for('main.profile'))

# AJAX routes for interactions
@main_bp.route('/api/like/<int:project_id>', methods=['POST'])
@login_required
def toggle_like(project_id):
    """Toggle like for a project"""
    project = Project.query.get_or_404(project_id)
    
    existing_like = Like.query.filter_by(user_id=current_user.id, project_id=project_id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        liked = False
    else:
        new_like = Like(user_id=current_user.id, project_id=project_id)
        db.session.add(new_like)
        liked = True
    
    db.session.commit()
    
    return jsonify({
        'liked': liked,
        'likes_count': project.likes_count
    })

@main_bp.route('/api/comment/<int:project_id>', methods=['POST'])
@login_required
def add_comment(project_id):
    """Add comment to a project"""
    project = Project.query.get_or_404(project_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            project_id=project_id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'user_name': comment.user.name,
                'user_image': comment.user.profile_image,
                'created_at': format_datetime(comment.created_at)
            }
        })
    
    return jsonify({'success': False, 'errors': form.errors}), 400

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            flash(f'Bem-vindo(a), {user.name}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('main.index'))
        
        flash('Email ou senha incorretos.', 'error')
    
    return render_template('login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegisterForm()
    
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Este email já está cadastrado.', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(
            name=form.name.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            bio=form.bio.data
        )
        
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        flash('Cadastro realizado com sucesso! Bem-vindo(a)!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('main.index'))

# Admin routes
def admin_required(f):
    """Decorator to require admin privileges"""
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Acesso negado. Apenas administradores podem acessar esta página.', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics"""
    # Get statistics
    total_projects = Project.query.count()
    published_projects = Project.query.filter_by(is_published=True).count()
    total_achievements = Achievement.query.count()
    total_users = User.query.count()
    total_comments = Comment.query.count()
    total_likes = Like.query.count()
    unread_messages = ContactMessage.query.filter_by(is_read=False).count()
    
    # Recent activity
    recent_projects = Project.query.order_by(desc(Project.created_at)).limit(5).all()
    recent_comments = Comment.query.order_by(desc(Comment.created_at)).limit(5).all()
    recent_messages = ContactMessage.query.order_by(desc(ContactMessage.created_at)).limit(5).all()
    
    # Most liked projects
    popular_projects = Project.query.join(Like).group_by(Project.id).order_by(desc(db.func.count(Like.id))).limit(5).all()
    
    stats = {
        'total_projects': total_projects,
        'published_projects': published_projects,
        'total_achievements': total_achievements,
        'total_users': total_users,
        'total_comments': total_comments,
        'total_likes': total_likes,
        'unread_messages': unread_messages
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_projects=recent_projects,
                         recent_comments=recent_comments,
                         recent_messages=recent_messages,
                         popular_projects=popular_projects)

@admin_bp.route('/projects')
@login_required
@admin_required
def projects_list():
    """Admin projects list"""
    page = request.args.get('page', 1, type=int)
    
    projects = Project.query.order_by(desc(Project.created_at)).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/projects_list.html', projects=projects)

@admin_bp.route('/projects/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_project():
    """Create new project"""
    form = ProjectForm()
    
    # Populate category choices
    categories = Category.query.all()
    form.category_id.choices = [(0, 'Selecione uma categoria')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            description=form.description.data,
            content=form.content.data,
            category_id=form.category_id.data if form.category_id.data != 0 else None,
            project_url=form.project_url.data,
            github_url=form.github_url.data,
            is_published=form.is_published.data,
            is_featured=form.is_featured.data
        )
        
        # Handle file uploads
        if form.image.data:
            filename = save_uploaded_file(form.image.data)
            if filename:
                project.image_url = filename
        
        if form.video.data:
            filename = save_uploaded_file(form.video.data)
            if filename:
                project.video_url = filename
        
        # Handle tags
        if form.tags.data:
            tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                project.tags.append(tag)
        
        db.session.add(project)
        db.session.commit()
        
        flash('Projeto criado com sucesso!', 'success')
        return redirect(url_for('admin.projects_list'))
    
    return render_template('admin/project_form.html', form=form, title='Novo Projeto')

@admin_bp.route('/projects/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_project(id):
    """Edit existing project"""
    project = Project.query.get_or_404(id)
    form = ProjectForm(obj=project)
    
    # Populate category choices
    categories = Category.query.all()
    form.category_id.choices = [(0, 'Selecione uma categoria')] + [(c.id, c.name) for c in categories]
    
    # Set current tags
    form.tags.data = ', '.join([tag.name for tag in project.tags])
    
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.content = form.content.data
        project.category_id = form.category_id.data if form.category_id.data != 0 else None
        project.project_url = form.project_url.data
        project.github_url = form.github_url.data
        project.is_published = form.is_published.data
        project.is_featured = form.is_featured.data
        project.updated_at = datetime.utcnow()
        
        # Handle file uploads
        if form.image.data:
            if project.image_url:
                delete_file(project.image_url)
            filename = save_uploaded_file(form.image.data)
            if filename:
                project.image_url = filename
        
        if form.video.data:
            if project.video_url:
                delete_file(project.video_url)
            filename = save_uploaded_file(form.video.data)
            if filename:
                project.video_url = filename
        
        # Handle tags
        project.tags.clear()
        if form.tags.data:
            tag_names = [tag.strip() for tag in form.tags.data.split(',') if tag.strip()]
            for tag_name in tag_names:
                tag = Tag.query.filter_by(name=tag_name).first()
                if not tag:
                    tag = Tag(name=tag_name)
                    db.session.add(tag)
                project.tags.append(tag)
        
        db.session.commit()
        
        flash('Projeto atualizado com sucesso!', 'success')
        return redirect(url_for('admin.projects_list'))
    
    return render_template('admin/project_form.html', form=form, project=project, title='Editar Projeto')

@admin_bp.route('/projects/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_project(id):
    """Delete project"""
    project = Project.query.get_or_404(id)
    
    # Delete associated files
    if project.image_url:
        delete_file(project.image_url)
    if project.video_url:
        delete_file(project.video_url)
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Projeto excluído com sucesso!', 'success')
    return redirect(url_for('admin.projects_list'))

# Error handlers
@main_bp.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@main_bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('404.html'), 500
