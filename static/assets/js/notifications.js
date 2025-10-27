/**
 * ========================================
 * NOTIFICATION SYSTEM JAVASCRIPT
 * ========================================
 * Advanced notification system with queue management
 * Author: GreenGardens Team
 * Version: 1.0.0
 */

class NotificationSystem {
    constructor() {
        this.container = null;
        this.queue = [];
        this.isProcessingQueue = false;
        this.defaultSettings = {
            autoDismiss: 5000,
            position: 'top-right',
            maxNotifications: 5
        };
        this.init();
    }

    init() {
        // Create container if it doesn't exist
        this.container = document.getElementById('notification-container');
        if (!this.container) {
            this.container = document.createElement('div');
            this.container.id = 'notification-container';
            this.container.className = 'notification-container';
            document.body.appendChild(this.container);
        }

        // Auto dismiss existing notifications on page load
        this.setupAutoDissmiss();
    }

    /**
     * Setup auto dismiss for existing notifications
     */
    setupAutoDissmiss() {
        const notifications = document.querySelectorAll('.notification[data-auto-dismiss]');
        notifications.forEach((notification) => {
            const delay = parseInt(notification.getAttribute('data-auto-dismiss'));
            if (delay > 0) {
                setTimeout(() => {
                    this.dismissNotification(notification);
                }, delay);
            }
        });
    }

    /**
     * Dismiss a single notification
     * @param {Element} element - Notification element or button
     */
    dismissNotification(element) {
        const notification = element.closest ? element.closest('.notification') : element;
        if (notification && notification.parentNode) {
            notification.classList.add('hiding');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 300);
        }
    }

    /**
     * Show a notification
     * @param {string} message - Notification message
     * @param {string} type - Notification type (success, error, warning, info)
     * @param {Object} options - Additional options
     */
    show(message, type = 'info', options = {}) {
        const settings = { ...this.defaultSettings, ...options };
        
        // Limit number of notifications
        const existingNotifications = this.container.children;
        if (existingNotifications.length >= settings.maxNotifications) {
            this.dismissNotification(existingNotifications[0]);
        }

        const icons = {
            'success': 'fas fa-check-circle',
            'error': 'fas fa-times-circle',
            'warning': 'fas fa-exclamation-triangle',
            'info': 'fas fa-info-circle'
        };

        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-icon">
                <i class="${icons[type] || 'fas fa-bell'}"></i>
            </div>
            <div class="notification-content">
                ${message}
            </div>
            <button class="notification-close" onclick="notificationSystem.dismissNotification(this)">
                <i class="fas fa-times"></i>
            </button>
        `;

        this.container.appendChild(notification);

        // Auto dismiss
        if (settings.autoDismiss > 0) {
            setTimeout(() => {
                this.dismissNotification(notification);
            }, settings.autoDismiss);
        }

        return notification;
    }

    /**
     * Show success notification
     */
    success(message, options = {}) {
        return this.show(message, 'success', { autoDismiss: 5000, ...options });
    }

    /**
     * Show error notification
     */
    error(message, options = {}) {
        return this.show(message, 'error', { autoDismiss: 7000, ...options });
    }

    /**
     * Show warning notification
     */
    warning(message, options = {}) {
        return this.show(message, 'warning', { autoDismiss: 6000, ...options });
    }

    /**
     * Show info notification
     */
    info(message, options = {}) {
        return this.show(message, 'info', { autoDismiss: 5000, ...options });
    }

    /**
     * Add notification to queue
     */
    addToQueue(message, type = 'info', options = {}) {
        this.queue.push({ message, type, options });
        this.processQueue();
    }

    /**
     * Process notification queue
     */
    processQueue() {
        if (this.isProcessingQueue || this.queue.length === 0) return;

        this.isProcessingQueue = true;
        const { message, type, options } = this.queue.shift();

        this.show(message, type, options);

        setTimeout(() => {
            this.isProcessingQueue = false;
            this.processQueue();
        }, 500);
    }

    /**
     * Clear all notifications
     */
    clearAll() {
        const notifications = this.container.querySelectorAll('.notification');
        notifications.forEach(notification => {
            this.dismissNotification(notification);
        });
    }

    /**
     * Update default settings
     */
    updateSettings(newSettings) {
        this.defaultSettings = { ...this.defaultSettings, ...newSettings };
    }
}

// Initialize notification system
const notificationSystem = new NotificationSystem();

// Legacy function support for backward compatibility
function dismissNotification(button) {
    notificationSystem.dismissNotification(button);
}

function showNotification(message, type = 'info', autoDismiss = 5000) {
    return notificationSystem.show(message, type, { autoDismiss });
}

function showSuccessNotification(message, autoDismiss = 5000) {
    return notificationSystem.success(message, { autoDismiss });
}

function showErrorNotification(message, autoDismiss = 7000) {
    return notificationSystem.error(message, { autoDismiss });
}

function showWarningNotification(message, autoDismiss = 6000) {
    return notificationSystem.warning(message, { autoDismiss });
}

function showInfoNotification(message, autoDismiss = 5000) {
    return notificationSystem.info(message, { autoDismiss });
}

function addToNotificationQueue(message, type = 'info', autoDismiss = 5000) {
    notificationSystem.addToQueue(message, type, { autoDismiss });
}

// Auto-initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Setup auto dismiss for server-side notifications
    notificationSystem.setupAutoDissmiss();
    
    // Add global error handler for AJAX requests
    window.addEventListener('unhandledrejection', function(event) {
        if (event.reason && event.reason.message) {
            notificationSystem.error(`Error: ${event.reason.message}`);
        }
    });
    
    // Service navigation enhancement
    const serviceLinks = document.querySelectorAll('.service-one__item');
    serviceLinks.forEach(function(serviceItem) {
        serviceItem.addEventListener('click', function(e) {
            // Only trigger if not clicking on a link directly
            if (!e.target.closest('a')) {
                const link = serviceItem.querySelector('a[href*="service_details"]');
                if (link) {
                    window.location.href = link.href;
                }
            }
        });
        
        // Add hover effect
        serviceItem.addEventListener('mouseenter', function() {
            serviceItem.style.transform = 'translateY(-5px)';
        });
        
        serviceItem.addEventListener('mouseleave', function() {
            serviceItem.style.transform = 'translateY(0)';
        });
    });
});

// Export for module use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NotificationSystem;
}

// Global shorthand
window.notify = notificationSystem;