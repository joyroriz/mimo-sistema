/**
 * 🍞 MIMO Toast Notifications System
 * Sistema completo de notificações visuais para o Sistema MIMO
 */

class MIMOToast {
    constructor() {
        this.container = null;
        this.toasts = new Map();
        this.init();
    }

    /**
     * Inicializa o sistema de toast
     */
    init() {
        // Criar container se não existir
        if (!document.querySelector('.toast-container')) {
            this.container = document.createElement('div');
            this.container.className = 'toast-container';
            document.body.appendChild(this.container);
        } else {
            this.container = document.querySelector('.toast-container');
        }
    }

    /**
     * Mostra um toast de sucesso
     */
    success(title, message, options = {}) {
        return this.show('success', title, message, {
            icon: 'bi-check-circle-fill',
            duration: 4000,
            ...options
        });
    }

    /**
     * Mostra um toast de erro
     */
    error(title, message, options = {}) {
        return this.show('error', title, message, {
            icon: 'bi-x-circle-fill',
            duration: 6000,
            ...options
        });
    }

    /**
     * Mostra um toast de aviso
     */
    warning(title, message, options = {}) {
        return this.show('warning', title, message, {
            icon: 'bi-exclamation-triangle-fill',
            duration: 5000,
            ...options
        });
    }

    /**
     * Mostra um toast informativo
     */
    info(title, message, options = {}) {
        return this.show('info', title, message, {
            icon: 'bi-info-circle-fill',
            duration: 4000,
            ...options
        });
    }

    /**
     * Mostra um toast de loading
     */
    loading(title, message, options = {}) {
        return this.show('loading', title, message, {
            icon: 'bi-arrow-clockwise',
            duration: 0, // Não remove automaticamente
            closable: false,
            ...options
        });
    }

    /**
     * Mostra um toast com countdown
     */
    countdown(title, message, seconds, onComplete, options = {}) {
        const toastId = this.show('warning', title, message, {
            icon: 'bi-clock-fill',
            duration: 0,
            countdown: true,
            countdownSeconds: seconds,
            onComplete: onComplete,
            ...options
        });

        this.startCountdown(toastId, seconds, onComplete);
        return toastId;
    }

    /**
     * Mostra um toast com botão de ação
     */
    action(title, message, actionText, actionCallback, options = {}) {
        return this.show('info', title, message, {
            icon: 'bi-hand-index-fill',
            duration: 0,
            action: {
                text: actionText,
                callback: actionCallback
            },
            ...options
        });
    }

    /**
     * Método principal para mostrar toast
     */
    show(type, title, message, options = {}) {
        const toastId = 'toast_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        
        const defaultOptions = {
            icon: 'bi-info-circle-fill',
            duration: 4000,
            closable: true,
            countdown: false,
            countdownSeconds: 0,
            action: null,
            onComplete: null
        };

        const config = { ...defaultOptions, ...options };

        // Criar elemento do toast
        const toast = this.createToastElement(toastId, type, title, message, config);
        
        // Adicionar ao container
        this.container.appendChild(toast);
        this.toasts.set(toastId, { element: toast, config: config });

        // Mostrar com animação
        setTimeout(() => {
            toast.classList.add('show');
        }, 100);

        // Auto-remover se tiver duração
        if (config.duration > 0) {
            setTimeout(() => {
                this.hide(toastId);
            }, config.duration);

            // Animar barra de progresso
            const progressBar = toast.querySelector('::before');
            if (progressBar) {
                toast.style.setProperty('--progress-duration', config.duration + 'ms');
            }
        }

        return toastId;
    }

    /**
     * Cria o elemento HTML do toast
     */
    createToastElement(id, type, title, message, config) {
        const toast = document.createElement('div');
        toast.className = `mimo-toast ${type}`;
        toast.setAttribute('data-toast-id', id);

        // Aplicar duração da barra de progresso
        if (config.duration > 0) {
            toast.style.setProperty('--progress-duration', config.duration + 'ms');
        }

        let html = `
            <div class="toast-icon">
                <i class="${config.icon}"></i>
            </div>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
        `;

        // Adicionar countdown se necessário
        if (config.countdown) {
            html = html.replace('</div>', `
                <div class="countdown-timer">${config.countdownSeconds}s</div>
            </div>`);
            toast.classList.add('countdown');
        }

        // Adicionar botão de ação se necessário
        if (config.action) {
            html += `<button class="toast-action" onclick="window.mimoToast.handleAction('${id}')">${config.action.text}</button>`;
        }

        // Adicionar botão de fechar se permitido
        if (config.closable) {
            html += `<button class="toast-close" onclick="window.mimoToast.hide('${id}')">
                <i class="bi bi-x"></i>
            </button>`;
        }

        toast.innerHTML = html;
        return toast;
    }

    /**
     * Inicia countdown no toast
     */
    startCountdown(toastId, seconds, onComplete) {
        const toast = this.toasts.get(toastId);
        if (!toast) return;

        const timerElement = toast.element.querySelector('.countdown-timer');
        let remaining = seconds;

        const interval = setInterval(() => {
            remaining--;
            if (timerElement) {
                timerElement.textContent = remaining + 's';
            }

            if (remaining <= 0) {
                clearInterval(interval);
                this.hide(toastId);
                if (onComplete && typeof onComplete === 'function') {
                    onComplete();
                }
            }
        }, 1000);

        // Salvar interval para poder cancelar
        toast.interval = interval;
    }

    /**
     * Manipula ação do botão
     */
    handleAction(toastId) {
        const toast = this.toasts.get(toastId);
        if (toast && toast.config.action && toast.config.action.callback) {
            toast.config.action.callback();
            this.hide(toastId);
        }
    }

    /**
     * Esconde um toast específico
     */
    hide(toastId) {
        const toast = this.toasts.get(toastId);
        if (!toast) return;

        // Limpar interval se existir
        if (toast.interval) {
            clearInterval(toast.interval);
        }

        // Animar saída
        toast.element.classList.add('hide');
        toast.element.classList.remove('show');

        // Remover após animação
        setTimeout(() => {
            if (toast.element.parentNode) {
                toast.element.parentNode.removeChild(toast.element);
            }
            this.toasts.delete(toastId);
        }, 400);
    }

    /**
     * Atualiza um toast existente
     */
    update(toastId, title, message) {
        const toast = this.toasts.get(toastId);
        if (!toast) return;

        const titleElement = toast.element.querySelector('.toast-title');
        const messageElement = toast.element.querySelector('.toast-message');

        if (titleElement) titleElement.textContent = title;
        if (messageElement) messageElement.textContent = message;
    }

    /**
     * Remove todos os toasts
     */
    clear() {
        this.toasts.forEach((toast, id) => {
            this.hide(id);
        });
    }

    /**
     * Verifica se um toast existe
     */
    exists(toastId) {
        return this.toasts.has(toastId);
    }
}

// Inicializar sistema global
window.mimoToast = new MIMOToast();

// Funções de conveniência globais
window.showToast = {
    success: (title, message, options) => window.mimoToast.success(title, message, options),
    error: (title, message, options) => window.mimoToast.error(title, message, options),
    warning: (title, message, options) => window.mimoToast.warning(title, message, options),
    info: (title, message, options) => window.mimoToast.info(title, message, options),
    loading: (title, message, options) => window.mimoToast.loading(title, message, options),
    countdown: (title, message, seconds, onComplete, options) => window.mimoToast.countdown(title, message, seconds, onComplete, options),
    action: (title, message, actionText, actionCallback, options) => window.mimoToast.action(title, message, actionText, actionCallback, options)
};

// Auto-inicializar quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    if (!window.mimoToast) {
        window.mimoToast = new MIMOToast();
    }
});
