/**
 * Bwire Global Tech - Mobile Navigation System
 * Universal mobile menu handler for all pages
 */

document.addEventListener('DOMContentLoaded', function() {
    initMobileNavigation();
});

function initMobileNavigation() {
    const mainNav = document.querySelector('.main-nav');
    if (!mainNav) return;
    
    // Create mobile menu toggle button if it doesn't exist
    let mobileToggle = document.querySelector('.mobile-menu-toggle');
    if (!mobileToggle) {
        mobileToggle = createMobileToggleButton();
        // Insert before the nav element
        mainNav.parentNode.insertBefore(mobileToggle, mainNav);
    }
    
    // Create overlay
    let overlay = document.querySelector('.mobile-nav-overlay');
    if (!overlay) {
        overlay = document.createElement('div');
        overlay.className = 'mobile-nav-overlay';
        document.body.appendChild(overlay);
    }
    
    // Get the navigation menu (either ul or nav-dropdown-container)
    const navMenu = mainNav.querySelector('ul') || mainNav.querySelector('.nav-dropdown-container');
    
    if (!navMenu) return;
    
    // Toggle menu function
    function toggleMenu() {
        const isActive = navMenu.classList.contains('active');
        
        if (isActive) {
            // Close menu
            navMenu.classList.remove('active');
            mobileToggle.classList.remove('active');
            overlay.classList.remove('active');
            document.body.classList.remove('mobile-menu-open');
        } else {
            // Open menu
            navMenu.classList.add('active');
            mobileToggle.classList.add('active');
            overlay.classList.add('active');
            document.body.classList.add('mobile-menu-open');
        }
    }
    
    // Event listeners
    mobileToggle.addEventListener('click', toggleMenu);
    overlay.addEventListener('click', toggleMenu);
    
    // Close menu when clicking on a link
    const navLinks = navMenu.querySelectorAll('a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Small delay to allow navigation
            setTimeout(() => {
                if (navMenu.classList.contains('active')) {
                    toggleMenu();
                }
            }, 100);
        });
    });
    
    // Close menu on escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navMenu.classList.contains('active')) {
            toggleMenu();
        }
    });
    
    // Handle window resize
    let resizeTimer;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function() {
            // If screen is wider than 768px, close mobile menu
            if (window.innerWidth > 768 && navMenu.classList.contains('active')) {
                toggleMenu();
            }
        }, 250);
    });
}

function createMobileToggleButton() {
    const button = document.createElement('button');
    button.className = 'mobile-menu-toggle';
    button.setAttribute('aria-label', 'Toggle mobile menu');
    button.setAttribute('aria-expanded', 'false');
    
    button.innerHTML = `
        <div class="hamburger-icon">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;
    
    return button;
}

// Update aria-expanded attribute when menu state changes
document.addEventListener('click', function(e) {
    if (e.target.closest('.mobile-menu-toggle')) {
        const button = e.target.closest('.mobile-menu-toggle');
        const isExpanded = button.getAttribute('aria-expanded') === 'true';
        button.setAttribute('aria-expanded', !isExpanded);
    }
});
