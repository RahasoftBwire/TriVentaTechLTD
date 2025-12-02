// Bwire Global Tech - Contact Form Handler
// Sends emails to bilfordderek917@gmail.com via SMTP

class ContactFormHandler {
    constructor(formId) {
        this.form = document.getElementById(formId);
        if (this.form) {
            this.init();
        }
    }

    init() {
        this.form.addEventListener('submit', (e) => this.handleSubmit(e));
    }

    async handleSubmit(e) {
        e.preventDefault();

        const formData = new FormData(this.form);
        const data = {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone') || '',
            subject: formData.get('subject') || 'Contact Form Submission',
            message: formData.get('message'),
            formType: this.form.dataset.formType || 'contact'
        };

        // Validation
        if (!data.name || !data.email || !data.message) {
            this.showMessage('Please fill in all required fields.', 'error');
            return;
        }

        if (!this.validateEmail(data.email)) {
            this.showMessage('Please enter a valid email address.', 'error');
            return;
        }

        // Show loading state
        const submitBtn = this.form.querySelector('button[type="submit"]');
        const originalText = submitBtn.textContent;
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';

        try {
            // Try to send via PHP backend
            const response = await fetch('send-email.php', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (result.success) {
                this.showMessage(result.message, 'success');
                this.form.reset();
            } else {
                throw new Error(result.message);
            }

        } catch (error) {
            // Fallback to mailto if PHP fails
            this.sendViaMailto(data);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
        }
    }

    sendViaMailto(data) {
        const subject = encodeURIComponent(`Bwire Global Tech - ${data.subject}`);
        const body = encodeURIComponent(
            `Name: ${data.name}\n` +
            `Email: ${data.email}\n` +
            ${data.phone ? `Phone: ${data.phone}\n` : ''} +
            `\nMessage:\n${data.message}`
        );
        
        window.location.href = `mailto:bilfordderek917@gmail.com?subject=${subject}&body=${body}`;
        
        this.showMessage(
            'Opening your email client... Please send the email to complete your message.',
            'info'
        );
    }

    validateEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    showMessage(message, type) {
        // Remove existing messages
        const existingMsg = this.form.querySelector('.form-message');
        if (existingMsg) {
            existingMsg.remove();
        }

        // Create message element
        const messageDiv = document.createElement('div');
        messageDiv.className = `form-message form-message-${type}`;
        messageDiv.textContent = message;
        
        // Style the message
        messageDiv.style.padding = '15px';
        messageDiv.style.marginTop = '15px';
        messageDiv.style.borderRadius = '8px';
        messageDiv.style.fontWeight = '500';
        messageDiv.style.animation = 'slideIn 0.3s ease';
        
        if (type === 'success') {
            messageDiv.style.background = '#d4edda';
            messageDiv.style.color = '#155724';
            messageDiv.style.border = '1px solid #c3e6cb';
        } else if (type === 'error') {
            messageDiv.style.background = '#f8d7da';
            messageDiv.style.color = '#721c24';
            messageDiv.style.border = '1px solid #f5c6cb';
        } else {
            messageDiv.style.background = '#d1ecf1';
            messageDiv.style.color = '#0c5460';
            messageDiv.style.border = '1px solid #bee5eb';
        }

        this.form.appendChild(messageDiv);

        // Auto remove after 5 seconds
        setTimeout(() => {
            messageDiv.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => messageDiv.remove(), 300);
        }, 5000);
    }
}

// Add animation styles
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideOut {
        from {
            opacity: 1;
            transform: translateY(0);
        }
        to {
            opacity: 0;
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(style);

// Initialize all contact forms on page load
document.addEventListener('DOMContentLoaded', () => {
    // Find all forms with class 'contact-form'
    const contactForms = document.querySelectorAll('.contact-form, form[action*="contact"]');
    contactForms.forEach(form => {
        if (form.id) {
            new ContactFormHandler(form.id);
        }
    });
});
