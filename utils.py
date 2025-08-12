import os
import uuid
from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename

def allowed_file(filename, extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

def save_uploaded_file(file, folder='uploads', max_size=(1200, 1200)):
    """
    Save uploaded file with unique filename and resize if it's an image
    
    Args:
        file: Uploaded file object
        folder: Destination folder
        max_size: Maximum image dimensions (width, height)
    
    Returns:
        Filename of saved file or None if failed
    """
    if not file or file.filename == '':
        return None
    
    # Generate unique filename
    filename = secure_filename(file.filename)
    name, ext = os.path.splitext(filename)
    unique_filename = f"{uuid.uuid4().hex}{ext}"
    
    # Create upload directory if it doesn't exist
    upload_dir = os.path.join(current_app.root_path, folder)
    os.makedirs(upload_dir, exist_ok=True)
    
    file_path = os.path.join(upload_dir, unique_filename)
    
    try:
        # Save the file
        file.save(file_path)
        
        # If it's an image, resize it
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        if ext.lower() in image_extensions:
            with Image.open(file_path) as img:
                # Convert RGBA to RGB if necessary
                if img.mode == 'RGBA' and ext.lower() in {'.jpg', '.jpeg'}:
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                # Resize if larger than max_size
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(file_path, optimize=True, quality=85)
        
        return unique_filename
    
    except Exception as e:
        # Remove file if processing failed
        if os.path.exists(file_path):
            os.remove(file_path)
        current_app.logger.error(f"Error saving file: {e}")
        return None

def delete_file(filename, folder='uploads'):
    """Delete uploaded file"""
    if not filename:
        return False
    
    file_path = os.path.join(current_app.root_path, folder, filename)
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {e}")
    
    return False

def format_date(date_obj):
    """Format date for display"""
    if not date_obj:
        return ""
    
    return date_obj.strftime("%d/%m/%Y")

def format_datetime(datetime_obj):
    """Format datetime for display"""
    if not datetime_obj:
        return ""
    
    return datetime_obj.strftime("%d/%m/%Y às %H:%M")

def truncate_text(text, max_length=150):
    """Truncate text to specified length with ellipsis"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length].rsplit(' ', 1)[0] + '...'

def generate_linkedin_share_url(title, description, url):
    """Generate LinkedIn share URL"""
    base_url = "https://www.linkedin.com/sharing/share-offsite/"
    params = f"?url={url}&title={title}&summary={description}"
    return base_url + params
