/**
 * EduPlatform - UX Enhancements
 * Mejoras de experiencia de usuario: animaciones, efectos y micro-interacciones
 */

// ====================================
// RIPPLE EFFECT
// ====================================
function createRipple(event) {
    const button = event.currentTarget;
    if (!button.classList.contains('ripple-effect')) return;

    const circle = document.createElement('span');
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    const rect = button.getBoundingClientRect();
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - rect.left - radius}px`;
    circle.style.top = `${event.clientY - rect.top - radius}px`;
    circle.classList.add('ripple');

    const existingRipple = button.querySelector('.ripple');
    if (existingRipple) existingRipple.remove();

    button.appendChild(circle);

    setTimeout(() => circle.remove(), 600);
}

// ====================================
// SCROLL REVEAL ANIMATIONS
// ====================================
function initScrollReveal() {
    const revealElements = document.querySelectorAll('.scroll-reveal');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    revealElements.forEach(el => observer.observe(el));
}

// ====================================
// STAGGER ANIMATIONS
// ====================================
function initStaggerAnimations() {
    document.querySelectorAll('[data-stagger]').forEach(container => {
        const children = container.children;
        Array.from(children).forEach((child, index) => {
            child.style.animationDelay = `${index * 0.1}s`;
        });
    });
}

// ====================================
// SMOOTH COUNTER ANIMATION
// ====================================
function animateCounter(element, target, duration = 2000) {
    const start = 0;
    const startTime = performance.now();

    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);

        // Easing function (ease-out-expo)
        const easing = 1 - Math.pow(2, -10 * progress);
        const current = Math.floor(easing * target);

        element.textContent = current.toLocaleString();

        if (progress < 1) {
            requestAnimationFrame(update);
        } else {
            element.textContent = target.toLocaleString();
        }
    }

    requestAnimationFrame(update);
}

function initCounters() {
    const counters = document.querySelectorAll('[data-counter]');

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.dataset.counter);
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => observer.observe(counter));
}

// ====================================
// PROGRESS BAR ANIMATION
// ====================================
function animateProgressBars() {
    document.querySelectorAll('.progress-bar-fill[data-progress]').forEach(bar => {
        const target = bar.dataset.progress;
        bar.style.width = '0%';

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        bar.style.width = target + '%';
                    }, 200);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(bar);
    });
}

// ====================================
// SMOOTH SCROLLING
// ====================================
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const href = this.getAttribute('href');
            if (href === '#') return;

            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// ====================================
// HEADER SCROLL EFFECT
// ====================================
function initHeaderScroll() {
    const header = document.querySelector('.header-premium, header');
    if (!header) return;

    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        header.classList.toggle('scrolled', currentScroll > 50);

        if (currentScroll > lastScroll && currentScroll > 100) {
            header.style.transform = 'translateY(-100%)';
        } else {
            header.style.transform = 'translateY(0)';
        }

        lastScroll = currentScroll;
    }, { passive: true });
}

// ====================================
// CARD HOVER TILT EFFECT
// ====================================
function initTiltEffect() {
    document.querySelectorAll('.card-tilt').forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = (centerX - x) / 10;

            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)';
        });
    });
}

// ====================================
// TYPING EFFECT
// ====================================
function typeEffect(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';

    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }

    type();
}

function initTypingEffects() {
    document.querySelectorAll('[data-typing]').forEach(el => {
        const text = el.dataset.typing;
        const speed = parseInt(el.dataset.typingSpeed) || 50;

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    typeEffect(entry.target, text, speed);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        observer.observe(el);
    });
}

// ====================================
// NOTIFICATION TOAST
// ====================================
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };

    toast.innerHTML = `
        <i class="fas ${icons[type]}"></i>
        <span>${message}</span>
    `;

    // Create container if not exists
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.style.cssText = 'position: fixed; bottom: 20px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px;';
        document.body.appendChild(container);
    }

    // Style toast
    toast.style.cssText = `
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 14px 20px;
        border-radius: 12px;
        color: white;
        font-weight: 500;
        font-size: 14px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        animation: slideInRight 0.3s ease, fadeOut 0.3s ease ${duration - 300}ms forwards;
        ${type === 'success' ? 'background: linear-gradient(135deg, #22c55e, #16a34a);' : ''}
        ${type === 'error' ? 'background: linear-gradient(135deg, #ef4444, #dc2626);' : ''}
        ${type === 'warning' ? 'background: linear-gradient(135deg, #f59e0b, #d97706);' : ''}
        ${type === 'info' ? 'background: linear-gradient(135deg, #0ea5e9, #0284c7);' : ''}
    `;

    container.appendChild(toast);

    setTimeout(() => toast.remove(), duration);
}

// Add toast animations
const toastStyles = document.createElement('style');
toastStyles.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes fadeOut {
        from { opacity: 1; transform: translateX(0); }
        to { opacity: 0; transform: translateX(20px); }
    }
`;
document.head.appendChild(toastStyles);

// ====================================
// LOADING SKELETON
// ====================================
function showSkeleton(containerId, count = 3) {
    const container = document.getElementById(containerId);
    if (!container) return;

    container.innerHTML = '';

    for (let i = 0; i < count; i++) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-card';
        skeleton.innerHTML = `
            <div class="skeleton-premium skeleton-avatar" style="width: 60px; height: 60px; border-radius: 12px; margin-bottom: 16px;"></div>
            <div class="skeleton-premium skeleton-text" style="width: 80%; height: 20px; margin-bottom: 8px;"></div>
            <div class="skeleton-premium skeleton-text" style="width: 60%; height: 16px;"></div>
        `;
        skeleton.style.cssText = 'padding: 20px; background: white; border-radius: 16px; margin-bottom: 16px;';
        container.appendChild(skeleton);
    }
}

function hideSkeleton(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.querySelectorAll('.skeleton-card').forEach(el => el.remove());
    }
}

// ====================================
// CONFETTI EFFECT
// ====================================
function showConfetti() {
    const colors = ['#ff6b6b', '#4ecdc4', '#ffe66d', '#a29bfe', '#fd79a8', '#0ea5e9'];
    const container = document.createElement('div');
    container.id = 'confetti-container';
    container.style.cssText = 'position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999; overflow: hidden;';
    document.body.appendChild(container);

    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: absolute;
            width: ${Math.random() * 10 + 5}px;
            height: ${Math.random() * 10 + 5}px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            left: ${Math.random() * 100}%;
            top: -20px;
            border-radius: ${Math.random() > 0.5 ? '50%' : '0'};
            animation: confetti-fall ${Math.random() * 3 + 2}s linear forwards;
        `;
        container.appendChild(confetti);
    }

    // Add confetti animation
    if (!document.getElementById('confetti-style')) {
        const style = document.createElement('style');
        style.id = 'confetti-style';
        style.textContent = `
            @keyframes confetti-fall {
                to {
                    transform: translateY(100vh) rotate(720deg);
                    opacity: 0;
                }
            }
        `;
        document.head.appendChild(style);
    }

    setTimeout(() => container.remove(), 5000);
}

// ====================================
// DARK MODE TOGGLE
// ====================================
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    const isDark = document.body.classList.contains('dark-mode');
    localStorage.setItem('darkMode', isDark);

    showToast(isDark ? 'Modo oscuro activado' : 'Modo claro activado', 'info', 2000);
}

function initDarkMode() {
    const savedMode = localStorage.getItem('darkMode');
    if (savedMode === 'true') {
        document.body.classList.add('dark-mode');
    }
}

// ====================================
// KEYBOARD SHORTCUTS
// ====================================
function initKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl/Cmd + K for search
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('[data-search], #search-input, input[type="search"]');
            if (searchInput) searchInput.focus();
        }

        // Escape to close modals
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal:not(.hidden)').forEach(modal => {
                modal.classList.add('hidden');
            });
        }
    });
}

// ====================================
// LAZY LOADING IMAGES
// ====================================
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.add('loaded');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    } else {
        images.forEach(img => {
            img.src = img.dataset.src;
        });
    }
}

// ====================================
// TOOLTIP
// ====================================
function initTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(el => {
        el.classList.add('tooltip-modern');
    });
}

// ====================================
// FOCUS TRAP FOR MODALS
// ====================================
function trapFocus(element) {
    const focusableElements = element.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    const firstFocusable = focusableElements[0];
    const lastFocusable = focusableElements[focusableElements.length - 1];

    element.addEventListener('keydown', (e) => {
        if (e.key === 'Tab') {
            if (e.shiftKey) {
                if (document.activeElement === firstFocusable) {
                    lastFocusable.focus();
                    e.preventDefault();
                }
            } else {
                if (document.activeElement === lastFocusable) {
                    firstFocusable.focus();
                    e.preventDefault();
                }
            }
        }
    });
}

// ====================================
// FORM VALIDATION FEEDBACK
// ====================================
function initFormValidation() {
    document.querySelectorAll('form[data-validate]').forEach(form => {
        form.addEventListener('submit', (e) => {
            let isValid = true;

            form.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    input.classList.add('input-error');
                    input.style.borderColor = '#ef4444';

                    // Shake animation
                    input.classList.add('animate-shake');
                    setTimeout(() => input.classList.remove('animate-shake'), 500);
                } else {
                    input.classList.remove('input-error');
                    input.style.borderColor = '';
                }
            });

            if (!isValid) {
                e.preventDefault();
                showToast('Por favor completa todos los campos requeridos', 'error');
            }
        });

        // Clear error on input
        form.querySelectorAll('input, textarea, select').forEach(input => {
            input.addEventListener('input', () => {
                input.classList.remove('input-error');
                input.style.borderColor = '';
            });
        });
    });
}

// ====================================
// COPY TO CLIPBOARD
// ====================================
async function copyToClipboard(text, successMessage = 'Copiado al portapapeles') {
    try {
        await navigator.clipboard.writeText(text);
        showToast(successMessage, 'success', 2000);
    } catch (err) {
        showToast('Error al copiar', 'error');
    }
}

// ====================================
// INITIALIZE ALL
// ====================================
function initUXEnhancements() {
    // Add ripple effect to buttons
    document.querySelectorAll('.btn, .button, button').forEach(btn => {
        if (!btn.classList.contains('no-ripple')) {
            btn.classList.add('ripple-effect');
            btn.addEventListener('click', createRipple);
        }
    });

    // Initialize all features
    initScrollReveal();
    initStaggerAnimations();
    initCounters();
    animateProgressBars();
    initSmoothScroll();
    initTiltEffect();
    initTypingEffects();
    initDarkMode();
    initKeyboardShortcuts();
    initLazyLoading();
    initTooltips();
    initFormValidation();

    console.log('✨ EduPlatform UX Enhancements loaded');
}

// Auto-initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initUXEnhancements);
} else {
    initUXEnhancements();
}

// Export for global use
window.EduPlatformUX = {
    showToast,
    showConfetti,
    toggleDarkMode,
    copyToClipboard,
    showSkeleton,
    hideSkeleton,
    typeEffect,
    animateCounter
};
