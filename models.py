from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    """User model for authentication and profile management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile_image = db.Column(db.String(200))
    bio = db.Column(db.Text)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='user', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'

class Category(db.Model):
    """Category model for organizing projects"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200))
    color = db.Column(db.String(7), default='#1e40af')  # Default dark blue
    
    # Relationships
    projects = db.relationship('Project', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(db.Model):
    """Tag model for project tagging"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# Association table for many-to-many relationship between projects and tags
project_tags = db.Table('project_tags',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Project(db.Model):
    """Project model for portfolio items"""
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    video_url = db.Column(db.String(300))
    project_url = db.Column(db.String(300))
    github_url = db.Column(db.String(300))
    is_published = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # Relationships
    tags = db.relationship('Tag', secondary=project_tags, lazy='subquery',
                          backref=db.backref('projects', lazy=True))
    comments = db.relationship('Comment', backref='project', lazy=True, cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='project', lazy=True, cascade='all, delete-orphan')
    
    @property
    def likes_count(self):
        return len(self.likes)
    
    @property
    def comments_count(self):
        return len(self.comments)
    
    def __repr__(self):
        return f'<Project {self.title}>'

class Achievement(db.Model):
    """Achievement model for accomplishments and certifications"""
    __tablename__ = 'achievements'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(300))
    certificate_url = db.Column(db.String(300))
    issuer = db.Column(db.String(100))
    date_achieved = db.Column(db.Date)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Achievement {self.title}>'

class Comment(db.Model):
    """Comment model for project feedback"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment by {self.user.name}>'

class Like(db.Model):
    """Like model for project likes"""
    __tablename__ = 'likes'
    
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    
    # Unique constraint to prevent duplicate likes
    __table_args__ = (db.UniqueConstraint('user_id', 'project_id', name='unique_user_project_like'),)
    
    def __repr__(self):
        return f'<Like by {self.user.name} on {self.project.title}>'

class ContactMessage(db.Model):
    """Contact message model for visitor inquiries"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage from {self.email}>'
