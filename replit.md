# Overview

This is a Flask-based portfolio web application called "Portfólio Digital" designed for showcasing projects, achievements, and personal information. The application features a complete content management system with user authentication, project management, contact forms, and social sharing capabilities. It's built as a personal portfolio website with admin functionality for managing content.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Backend Architecture
- **Framework**: Flask web framework with application factory pattern
- **Database**: SQLAlchemy ORM with SQLite default (configurable to PostgreSQL via DATABASE_URL)
- **Authentication**: Flask-Login for session management with bcrypt password hashing
- **Forms**: Flask-WTF for form handling and CSRF protection
- **File Uploads**: Werkzeug for secure file handling with PIL for image processing
- **Middleware**: ProxyFix for handling proxy headers in production environments

## Frontend Architecture
- **Templates**: Jinja2 templating engine with Bootstrap 5 for responsive design
- **Styling**: Custom CSS with CSS variables for theming (dark blue color scheme)
- **JavaScript**: Vanilla JavaScript for theme switching, animations, and UI interactions
- **Icons**: Font Awesome 6.5.0 for iconography
- **Fonts**: Google Fonts (Inter family) for typography

## Data Models
- **User**: Authentication and profile management with admin privileges
- **Project**: Portfolio projects with categories, tags, media uploads, and publishing status
- **Category**: Project organization with color coding
- **Tag**: Project tagging system
- **Comment**: User feedback system for projects
- **Like**: Social engagement features
- **Achievement**: Professional accomplishments showcase
- **ContactMessage**: Contact form submissions

## Authentication & Authorization
- Role-based access control with admin and regular user roles
- Session-based authentication using Flask-Login
- Password hashing with Werkzeug security utilities
- CSRF protection on all forms

## File Management
- Secure file upload handling with extension validation
- Automatic image resizing and optimization using PIL
- Unique filename generation to prevent conflicts
- Support for both images and videos

## Features Architecture
- **Portfolio Showcase**: Public project gallery with filtering and search
- **Admin Panel**: Complete CRUD operations for content management
- **Contact System**: Form-based contact with message storage
- **Social Integration**: LinkedIn sharing capabilities
- **Responsive Design**: Mobile-first approach with Bootstrap grid system
- **Theme System**: Dark/light mode with CSS custom properties

# External Dependencies

## Core Framework Dependencies
- **Flask**: Web application framework
- **Flask-SQLAlchemy**: Database ORM integration
- **Flask-Login**: User session management
- **Flask-WTF**: Form handling and validation
- **WTForms**: Form field definitions and validation
- **Werkzeug**: WSGI utilities and security functions

## Frontend Dependencies
- **Bootstrap 5.3.2**: CSS framework for responsive design
- **Font Awesome 6.5.0**: Icon library
- **Google Fonts**: Web typography (Inter font family)

## Database
- **SQLite**: Default development database
- **PostgreSQL**: Production database option (configurable via DATABASE_URL)

## Image Processing
- **Pillow (PIL)**: Image manipulation and optimization

## Development Tools
- **Python Logging**: Application logging and debugging
- **Environment Variables**: Configuration management for sensitive data

## Third-party Integrations
- **LinkedIn API**: Social sharing functionality for projects
- **File Upload Services**: Support for image and video uploads with validation