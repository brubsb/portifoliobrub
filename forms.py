from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, SelectField, URLField, DateField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, URL

class LoginForm(FlaskForm):
    """Login form for user authentication"""
    email = StringField('Email', validators=[DataRequired(), Email()], 
                       render_kw={"placeholder": "seu@email.com", "class": "form-control"})
    password = PasswordField('Senha', validators=[DataRequired()],
                           render_kw={"placeholder": "Sua senha", "class": "form-control"})
    remember_me = BooleanField('Lembrar de mim', render_kw={"class": "form-check-input"})

class RegisterForm(FlaskForm):
    """Registration form for new users"""
    name = StringField('Nome Completo', validators=[DataRequired(), Length(min=2, max=100)],
                      render_kw={"placeholder": "Seu nome completo", "class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                       render_kw={"placeholder": "seu@email.com", "class": "form-control"})
    password = PasswordField('Senha', validators=[DataRequired(), Length(min=6)],
                           render_kw={"placeholder": "Mínimo 6 caracteres", "class": "form-control"})
    password2 = PasswordField('Confirmar Senha', 
                            validators=[DataRequired(), EqualTo('password', message='As senhas devem ser iguais')],
                            render_kw={"placeholder": "Confirme sua senha", "class": "form-control"})
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)],
                       render_kw={"placeholder": "Conte um pouco sobre você (opcional)", "class": "form-control", "rows": "3"})

class ProjectForm(FlaskForm):
    """Form for creating and editing projects"""
    title = StringField('Título', validators=[DataRequired(), Length(max=200)],
                       render_kw={"class": "form-control"})
    description = TextAreaField('Descrição', validators=[DataRequired()],
                               render_kw={"class": "form-control", "rows": "4"})
    content = TextAreaField('Conteúdo Detalhado', validators=[Optional()],
                           render_kw={"class": "form-control", "rows": "8"})
    category_id = SelectField('Categoria', coerce=int, validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    image = FileField('Imagem', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg', 'webp'], 'Apenas imagens!')],
                     render_kw={"class": "form-control"})
    video = FileField('Vídeo', validators=[FileAllowed(['mp4', 'avi', 'mov', 'webm'], 'Apenas vídeos!')],
                     render_kw={"class": "form-control"})
    project_url = URLField('URL do Projeto', validators=[Optional(), URL()],
                          render_kw={"class": "form-control", "placeholder": "https://projeto.com"})
    github_url = URLField('URL do GitHub', validators=[Optional(), URL()],
                         render_kw={"class": "form-control", "placeholder": "https://github.com/usuario/projeto"})
    tags = StringField('Tags', validators=[Optional()],
                      render_kw={"class": "form-control", "placeholder": "React, Python, API (separadas por vírgula)"})
    is_published = BooleanField('Publicar', render_kw={"class": "form-check-input"})
    is_featured = BooleanField('Destacar', render_kw={"class": "form-check-input"})

class AchievementForm(FlaskForm):
    """Form for creating and editing achievements"""
    title = StringField('Título', validators=[DataRequired(), Length(max=200)],
                       render_kw={"class": "form-control"})
    description = TextAreaField('Descrição', validators=[DataRequired()],
                               render_kw={"class": "form-control", "rows": "4"})
    issuer = StringField('Emissor/Instituição', validators=[Optional(), Length(max=100)],
                        render_kw={"class": "form-control"})
    date_achieved = DateField('Data', validators=[Optional()],
                             render_kw={"class": "form-control"})
    image = FileField('Imagem/Certificado', validators=[FileAllowed(['jpg', 'png', 'pdf', 'gif', 'jpeg'], 'Apenas imagens ou PDF!')],
                     render_kw={"class": "form-control"})
    certificate_url = URLField('URL do Certificado', validators=[Optional(), URL()],
                              render_kw={"class": "form-control", "placeholder": "https://certificado.com"})
    is_published = BooleanField('Publicar', render_kw={"class": "form-check-input"})

class CategoryForm(FlaskForm):
    """Form for creating and editing categories"""
    name = StringField('Nome', validators=[DataRequired(), Length(max=50)],
                      render_kw={"class": "form-control"})
    description = StringField('Descrição', validators=[Optional(), Length(max=200)],
                             render_kw={"class": "form-control"})
    color = StringField('Cor', validators=[Optional()],
                       render_kw={"class": "form-control", "type": "color", "value": "#1e40af"})

class CommentForm(FlaskForm):
    """Form for posting comments"""
    content = TextAreaField('Comentário', validators=[DataRequired(), Length(min=1, max=1000)],
                           render_kw={"class": "form-control", "rows": "3", "placeholder": "Deixe seu comentário..."})

class ContactForm(FlaskForm):
    """Contact form for visitor inquiries"""
    name = StringField('Nome', validators=[DataRequired(), Length(max=100)],
                      render_kw={"class": "form-control", "placeholder": "Seu nome"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                       render_kw={"class": "form-control", "placeholder": "seu@email.com"})
    subject = StringField('Assunto', validators=[DataRequired(), Length(max=200)],
                         render_kw={"class": "form-control", "placeholder": "Assunto da mensagem"})
    message = TextAreaField('Mensagem', validators=[DataRequired(), Length(min=10, max=2000)],
                           render_kw={"class": "form-control", "rows": "5", "placeholder": "Sua mensagem..."})

class ProfileForm(FlaskForm):
    """Form for editing user profile"""
    name = StringField('Nome', validators=[DataRequired(), Length(min=2, max=100)],
                      render_kw={"class": "form-control"})
    bio = TextAreaField('Bio', validators=[Optional(), Length(max=500)],
                       render_kw={"class": "form-control", "rows": "4", "placeholder": "Conte um pouco sobre você"})
    profile_image = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'], 'Apenas imagens!')],
                             render_kw={"class": "form-control"})
