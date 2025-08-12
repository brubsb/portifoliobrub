/**
 * Main JavaScript file for Portfolio Digital
 * Handles theme switching, animations, interactions, and UI enhancements
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initThemeToggle();
    initBackToTop();
    initNavigation();
    initAnimations();
    initForms();
    initModals();
    initTooltips();
    initLoadingScreen();
    
    console.log('Portfolio Digital loaded successfully! 🚀');
});

/**
 * Theme Toggle Functionality
 */
function initThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const html = document.documentElement;
    
    if (!themeToggle || !themeIcon) return;
    
    // Get saved theme or default to dark
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        // Add transition class
        html.style.transition = 'all 0.3s ease';
        
        // Update theme
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
        
        // Remove transition after animation
        setTimeout(() => {
            html.style.transition = '';
        }, 300);
        
        // Add animation to toggle button
        this.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            this.style.transform = '';
        }, 300);
    });
    
    function updateThemeIcon(theme) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
        themeToggle.title = theme === 'dark' ? 'Modo claro' : 'Modo escuro';
    }
}

/**
 * Back to Top Button
 */
function initBackToTop() {
    const backToTopBtn = document.getElementById('back-to-top');
    
    if (!backToTopBtn) return;
    
    // Show/hide button based on scroll position
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    // Smooth scroll to top
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        
        // Add animation
        this.style.transform = 'scale(0.9)';
        setTimeout(() => {
            this.style.transform = '';
        }, 150);
    });
}

/**
 * Navigation Enhancements
 */
function initNavigation() {
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    
    if (!navbar) return;
    
    // Add scrolled class to navbar
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Active link highlighting
    const currentPage = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPage) {
            link.classList.add('active');
        }
        
        // Add hover animation
        link.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    // Mobile menu auto-close
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth < 992) {
                    navbarCollapse.classList.remove('show');
                }
            });
        });
    }
}

/**
 * Animation System
 */
function initAnimations() {
    // Intersection Observer for scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Special animations for specific elements
                if (entry.target.classList.contains('counter')) {
                    animateCounter(entry.target);
                }
                
                if (entry.target.classList.contains('skill-progress')) {
                    animateSkillBar(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observe elements with data-aos attribute
    document.querySelectorAll('[data-aos]').forEach(el => {
        observer.observe(el);
    });
    
    // Counter animation
    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count')) || 0;
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;
        
        const counter = setInterval(() => {
            current += step;
            if (current >= target) {
                element.textContent = target;
                clearInterval(counter);
            } else {
                element.textContent = Math.floor(current);
            }
        }, 16);
    }
    
    // Skill bar animation
    function animateSkillBar(element) {
        const width = element.style.width;
        element.style.width = '0%';
        
        setTimeout(() => {
            element.style.width = width;
        }, 200);
    }
    
    // Parallax effect for hero section
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            
            const heroBackground = heroSection.querySelector('.hero-background');
            if (heroBackground) {
                heroBackground.style.transform = `translateY(${rate}px)`;
            }
        });
    }
    
    // Floating animation for hero elements
    initFloatingAnimation();
}

/**
 * Floating Animation for Hero Elements
 */
function initFloatingAnimation() {
    const floatingElements = document.querySelectorAll('.float-element, .float-icon');
    
    floatingElements.forEach((element, index) => {
        const duration = 3000 + (index * 500);
        const amplitude = 15 + (index * 5);
        const delay = index * 200;
        
        setTimeout(() => {
            setInterval(() => {
                const time = Date.now() / duration;
                const y = Math.sin(time) * amplitude;
                const x = Math.cos(time * 0.5) * (amplitude * 0.3);
                
                element.style.transform = `translate(${x}px, ${y}px)`;
            }, 16);
        }, delay);
    });
}

/**
 * Form Enhancements
 */
function initForms() {
    // Form validation feedback
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            // Real-time validation
            input.addEventListener('input', function() {
                validateField(this);
            });
            
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            // Clear validation on focus
            input.addEventListener('focus', function() {
                this.classList.remove('is-valid', 'is-invalid');
            });
        });
        
        // Form submission handling
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processando...';
                
                // Re-enable after timeout (fallback)
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
        });
    });
    
    function validateField(field) {
        const value = field.value.trim();
        const type = field.type;
        const required = field.hasAttribute('required');
        
        let isValid = true;
        let message = '';
        
        if (required && !value) {
            isValid = false;
            message = 'Este campo é obrigatório';
        } else if (type === 'email' && value && !isValidEmail(value)) {
            isValid = false;
            message = 'Email inválido';
        } else if (type === 'password' && value && value.length < 6) {
            isValid = false;
            message = 'Senha deve ter pelo menos 6 caracteres';
        }
        
        if (isValid && value) {
            field.classList.remove('is-invalid');
            field.classList.add('is-valid');
        } else if (!isValid) {
            field.classList.remove('is-valid');
            field.classList.add('is-invalid');
            showFieldError(field, message);
        }
    }
    
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }
    
    function showFieldError(field, message) {
        // Remove existing error
        const existingError = field.parentNode.querySelector('.field-error');
        if (existingError) {
            existingError.remove();
        }
        
        // Add new error
        if (message) {
            const errorDiv = document.createElement('div');
            errorDiv.className = 'field-error small text-danger mt-1';
            errorDiv.textContent = message;
            field.parentNode.appendChild(errorDiv);
        }
    }
    
    // Character counter for textareas
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(textarea => {
        const maxLength = parseInt(textarea.getAttribute('maxlength'));
        const counter = document.createElement('div');
        counter.className = 'character-counter small text-muted text-end mt-1';
        textarea.parentNode.appendChild(counter);
        
        function updateCounter() {
            const currentLength = textarea.value.length;
            const remaining = maxLength - currentLength;
            counter.innerHTML = `
                <span class="${remaining < 50 ? 'text-warning' : 'text-muted'}">
                    ${currentLength}/${maxLength} caracteres
                </span>
            `;
        }
        
        textarea.addEventListener('input', updateCounter);
        updateCounter();
    });
}

/**
 * Modal Enhancements
 */
function initModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        modal.addEventListener('shown.bs.modal', function() {
            const firstInput = this.querySelector('input, textarea');
            if (firstInput) {
                firstInput.focus();
            }
            
            // Add modal animation
            this.querySelector('.modal-dialog').style.transform = 'scale(1)';
        });
        
        modal.addEventListener('hide.bs.modal', function() {
            // Reset forms in modal
            const form = this.querySelector('form');
            if (form) {
                form.reset();
                form.querySelectorAll('.is-valid, .is-invalid').forEach(el => {
                    el.classList.remove('is-valid', 'is-invalid');
                });
                form.querySelectorAll('.field-error').forEach(el => {
                    el.remove();
                });
            }
        });
    });
}

/**
 * Tooltip Initialization
 */
function initTooltips() {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * Loading Screen
 */
function initLoadingScreen() {
    const loadingScreen = document.getElementById('loading-screen');
    
    if (!loadingScreen) return;
    
    // Hide loading screen after page load
    window.addEventListener('load', function() {
        setTimeout(() => {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }, 800);
    });
    
    // Fallback: hide after maximum time
    setTimeout(() => {
        if (loadingScreen.style.display !== 'none') {
            loadingScreen.style.opacity = '0';
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }
    }, 3000);
}

/**
 * AJAX Like System
 */
function initLikeSystem() {
    const likeButtons = document.querySelectorAll('.like-btn');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', function() {
            const projectId = this.getAttribute('data-project-id');
            if (!projectId) return;
            
            // Optimistic UI update
            const wasLiked = this.classList.contains('active');
            this.classList.toggle('active');
            
            const countSpan = this.querySelector('.likes-count');
            let currentCount = parseInt(countSpan.textContent) || 0;
            countSpan.textContent = wasLiked ? currentCount - 1 : currentCount + 1;
            
            // Send request
            fetch(`/api/like/${projectId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                credentials: 'same-origin'
            })
            .then(response => response.json())
            .then(data => {
                if (data.liked !== undefined) {
                    this.classList.toggle('active', data.liked);
                    countSpan.textContent = data.likes_count;
                    
                    // Add animation
                    this.style.transform = 'scale(1.2)';
                    setTimeout(() => {
                        this.style.transform = '';
                    }, 200);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                // Revert optimistic update
                this.classList.toggle('active');
                countSpan.textContent = currentCount;
                
                showNotification('Erro ao curtir projeto', 'error');
            });
        });
    });
}

/**
 * Comment System
 */
function initCommentSystem() {
    const commentForm = document.getElementById('commentForm');
    
    if (!commentForm) return;
    
    commentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;
        
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Enviando...';
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Add new comment to the list
                const commentsList = document.getElementById('commentsList');
                const newCommentHtml = createCommentHTML(data.comment);
                commentsList.insertAdjacentHTML('afterbegin', newCommentHtml);
                
                // Clear form
                this.reset();
                
                // Update comment count
                updateCommentCount(1);
                
                showNotification('Comentário adicionado com sucesso!', 'success');
            } else {
                showNotification('Erro ao adicionar comentário', 'error');
                console.error('Comment errors:', data.errors);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification('Erro de conexão', 'error');
        })
        .finally(() => {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalText;
        });
    });
    
    function createCommentHTML(comment) {
        const avatarHTML = comment.user_image 
            ? `<img src="/uploads/${comment.user_image}" class="rounded-circle me-3" width="50" height="50" alt="${comment.user_name}">`
            : `<div class="avatar-placeholder me-3"><i class="fas fa-user-circle fa-2x text-muted"></i></div>`;
        
        return `
            <div class="comment-item mb-4 new-comment">
                <div class="d-flex">
                    ${avatarHTML}
                    <div class="flex-grow-1">
                        <div class="comment-content bg-dark-light p-3 rounded">
                            <div class="d-flex justify-content-between align-items-center mb-2">
                                <h6 class="fw-bold mb-0">${comment.user_name}</h6>
                                <small class="text-muted">${comment.created_at}</small>
                            </div>
                            <p class="mb-0">${comment.content}</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    function updateCommentCount(increment) {
        const countElements = document.querySelectorAll('.comments-count, .comment-count');
        countElements.forEach(element => {
            const current = parseInt(element.textContent) || 0;
            element.textContent = current + increment;
        });
    }
}

/**
 * Search Functionality
 */
function initSearch() {
    const searchForm = document.getElementById('searchForm');
    const searchInput = document.querySelector('input[name="search"]');
    
    if (!searchForm || !searchInput) return;
    
    // Auto-complete functionality (if needed)
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        if (query.length > 2) {
            searchTimeout = setTimeout(() => {
                // Implement autocomplete if needed
                console.log('Searching for:', query);
            }, 300);
        }
    });
    
    // Highlight search terms in results
    const searchQuery = new URLSearchParams(window.location.search).get('search');
    if (searchQuery) {
        highlightSearchTerms(searchQuery);
    }
    
    function highlightSearchTerms(query) {
        const regex = new RegExp(`(${query})`, 'gi');
        const elements = document.querySelectorAll('.project-card .card-title, .project-card .card-text');
        
        elements.forEach(element => {
            if (element.textContent.toLowerCase().includes(query.toLowerCase())) {
                element.innerHTML = element.innerHTML.replace(regex, '<mark>$1</mark>');
            }
        });
    }
}

/**
 * Image Lazy Loading
 */
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                    
                    img.addEventListener('load', function() {
                        this.style.opacity = '1';
                    });
                }
            });
        });
        
        images.forEach(img => {
            imageObserver.observe(img);
        });
    } else {
        // Fallback for older browsers
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

/**
 * Notification System
 */
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show`;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        z-index: 1060;
        max-width: 400px;
        animation: slideInRight 0.5s ease;
    `;
    
    const icons = {
        success: 'check-circle',
        error: 'exclamation-triangle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    
    notification.innerHTML = `
        <i class="fas fa-${icons[type] || icons.info} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 150);
    }, duration);
}

/**
 * Utility Functions
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Link copiado!', 'success', 2000);
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            showNotification('Link copiado!', 'success', 2000);
        } catch (err) {
            showNotification('Erro ao copiar link', 'error', 2000);
        }
        document.body.removeChild(textArea);
    }
}

// Initialize additional features after DOM load
document.addEventListener('DOMContentLoaded', function() {
    initLikeSystem();
    initCommentSystem();
    initSearch();
    initLazyLoading();
});

// Performance optimization
window.addEventListener('load', function() {
    // Remove loading classes
    document.body.classList.add('loaded');
    
    // Initialize non-critical features
    setTimeout(() => {
        // Add any heavy initialization here
        console.log('All features loaded');
    }, 1000);
});

// Error handling
window.addEventListener('error', function(e) {
    console.error('JavaScript error:', e.error);
});

window.addEventListener('unhandledrejection', function(e) {
    console.error('Unhandled promise rejection:', e.reason);
});
