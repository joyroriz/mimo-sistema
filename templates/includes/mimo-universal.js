/**
 * MIMO Sistema - JavaScript Universal
 * Funções compartilhadas para todas as páginas
 */

// Implementação completa do sistema de Toast
const showToast = {
    success: function(title, message) { this.show('success', title, message); },
    error: function(title, message) { this.show('error', title, message); },
    warning: function(title, message) { this.show('warning', title, message); },
    info: function(title, message) { this.show('info', title, message); },
    loading: function(title, message) { return this.show('loading', title, message); },
    countdown: function(title, message, seconds, callback, options) {
        return this.show('countdown', title, message, { seconds, callback, options });
    },
    show: function(type, title, message, extra = {}) {
        let container = document.getElementById('toast-container');
        if (!container) {
            container = document.createElement('div');
            container.id = 'toast-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 350px;
            `;
            document.body.appendChild(container);
        }

        const toast = document.createElement('div');
        const toastId = 'toast-' + Date.now();
        toast.id = toastId;
        
        const colors = {
            success: { bg: '#d4edda', border: '#c3e6cb', text: '#155724' },
            error: { bg: '#f8d7da', border: '#f5c6cb', text: '#721c24' },
            warning: { bg: '#fff3cd', border: '#ffeaa7', text: '#856404' },
            info: { bg: '#d1ecf1', border: '#bee5eb', text: '#0c5460' },
            loading: { bg: '#e2e3e5', border: '#d6d8db', text: '#383d41' },
            countdown: { bg: '#fff3cd', border: '#ffeaa7', text: '#856404' }
        };

        const color = colors[type] || colors.info;
        
        toast.style.cssText = `
            background: ${color.bg};
            border: 1px solid ${color.border};
            color: ${color.text};
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            animation: slideIn 0.3s ease-out;
            position: relative;
        `;

        let content = `
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <strong>${title}</strong>
                    <div style="margin-top: 5px;">${message}</div>
                </div>
                <button onclick="this.parentElement.parentElement.remove()" 
                        style="background: none; border: none; font-size: 18px; cursor: pointer; color: ${color.text};">×</button>
            </div>
        `;

        if (type === 'countdown' && extra.seconds) {
            let remainingSeconds = extra.seconds;
            content += `<div id="${toastId}-countdown" style="margin-top: 10px; font-weight: bold;">Tempo restante: ${remainingSeconds}s</div>`;
            
            if (extra.options && extra.options.action) {
                content += `<button onclick="${extra.options.action.callback}" 
                                   style="margin-top: 10px; padding: 5px 10px; background: ${color.text}; color: ${color.bg}; border: none; border-radius: 4px; cursor: pointer;">
                                ${extra.options.action.text}
                               </button>`;
            }

            const countdownInterval = setInterval(() => {
                remainingSeconds--;
                const countdownEl = document.getElementById(`${toastId}-countdown`);
                if (countdownEl) {
                    countdownEl.textContent = `Tempo restante: ${remainingSeconds}s`;
                }
                
                if (remainingSeconds <= 0) {
                    clearInterval(countdownInterval);
                    if (extra.callback) extra.callback();
                    toast.remove();
                }
            }, 1000);
        }

        toast.innerHTML = content;
        container.appendChild(toast);

        if (type !== 'loading' && type !== 'countdown') {
            setTimeout(() => {
                if (toast.parentElement) {
                    toast.style.animation = 'slideOut 0.3s ease-in';
                    setTimeout(() => toast.remove(), 300);
                }
            }, 5000);
        }

        return toastId;
    }
};

// Adicionar CSS de animação
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOut {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Funções utilitárias
const MimoUtils = {
    // Formatar moeda
    formatCurrency: function(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    },

    // Formatar data
    formatDate: function(dateString) {
        return new Date(dateString).toLocaleDateString('pt-BR');
    },

    // Formatar data e hora
    formatDateTime: function(dateString) {
        return new Date(dateString).toLocaleString('pt-BR');
    },

    // Validar email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },

    // Validar telefone
    validatePhone: function(phone) {
        const re = /^\(\d{2}\)\s\d{4,5}-\d{4}$/;
        return re.test(phone);
    },

    // Confirmar ação
    confirm: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // Loading state
    setLoading: function(element, loading = true) {
        if (loading) {
            element.disabled = true;
            element.innerHTML = '<i class="bi bi-hourglass-split"></i> Carregando...';
        } else {
            element.disabled = false;
            element.innerHTML = element.getAttribute('data-original-text') || 'Salvar';
        }
    }
};

// Funções de API
const MimoAPI = {
    // Fazer requisição GET
    get: async function(url) {
        try {
            const response = await fetch(url);
            return await response.json();
        } catch (error) {
            showToast.error('Erro', 'Erro ao carregar dados');
            throw error;
        }
    },

    // Fazer requisição POST
    post: async function(url, data) {
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            showToast.error('Erro', 'Erro ao enviar dados');
            throw error;
        }
    },

    // Fazer requisição PUT
    put: async function(url, data) {
        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            showToast.error('Erro', 'Erro ao atualizar dados');
            throw error;
        }
    },

    // Fazer requisição DELETE
    delete: async function(url) {
        try {
            const response = await fetch(url, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            showToast.error('Erro', 'Erro ao excluir dados');
            throw error;
        }
    }
};

// Inicialização global
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar loading aos botões de formulário
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            submitBtn.setAttribute('data-original-text', submitBtn.innerHTML);
        }
    });

    // Adicionar confirmação para botões de exclusão
    const deleteButtons = document.querySelectorAll('[data-action="delete"]');
    deleteButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const message = this.getAttribute('data-confirm') || 'Tem certeza que deseja excluir?';
            MimoUtils.confirm(message, () => {
                // Executar ação de exclusão
                const url = this.getAttribute('data-url');
                if (url) {
                    MimoAPI.delete(url).then(result => {
                        if (result.success) {
                            showToast.success('Sucesso', result.message);
                            setTimeout(() => location.reload(), 1500);
                        }
                    });
                }
            });
        });
    });
});

// Exportar para uso global
window.showToast = showToast;
window.MimoUtils = MimoUtils;
window.MimoAPI = MimoAPI;
