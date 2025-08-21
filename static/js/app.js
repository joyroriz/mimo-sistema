// JavaScript customizado para o Sistema MIMO

// Configurações globais
const MIMO = {
    // URLs da API
    api: {
        clientes: '/api/clientes',
        produtos: '/api/produtos',
        vendas: '/api/vendas',
        entregas: '/api/entregas'
    },
    
    // Configurações
    config: {
        animationDuration: 300,
        alertTimeout: 5000,
        dateFormat: 'DD/MM/YYYY',
        currencyFormat: 'pt-BR'
    }
};

// Utilitários
const Utils = {
    // Formatar moeda
    formatCurrency: function(value) {
        return new Intl.NumberFormat('pt-BR', {
            style: 'currency',
            currency: 'BRL'
        }).format(value);
    },
    
    // Formatar data
    formatDate: function(date) {
        return moment(date).format(MIMO.config.dateFormat);
    },
    
    // Validar CPF/CNPJ
    validateDocument: function(doc) {
        doc = doc.replace(/[^\d]/g, '');
        if (doc.length === 11) {
            return this.validateCPF(doc);
        } else if (doc.length === 14) {
            return this.validateCNPJ(doc);
        }
        return false;
    },
    
    // Validar CPF
    validateCPF: function(cpf) {
        if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) return false;
        
        let sum = 0;
        for (let i = 0; i < 9; i++) {
            sum += parseInt(cpf.charAt(i)) * (10 - i);
        }
        let remainder = 11 - (sum % 11);
        if (remainder === 10 || remainder === 11) remainder = 0;
        if (remainder !== parseInt(cpf.charAt(9))) return false;
        
        sum = 0;
        for (let i = 0; i < 10; i++) {
            sum += parseInt(cpf.charAt(i)) * (11 - i);
        }
        remainder = 11 - (sum % 11);
        if (remainder === 10 || remainder === 11) remainder = 0;
        return remainder === parseInt(cpf.charAt(10));
    },
    
    // Validar email
    validateEmail: function(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    },
    
    // Mostrar loading
    showLoading: function(element) {
        const spinner = '<div class="spinner-custom mx-auto"></div>';
        $(element).html(spinner);
    },
    
    // Esconder loading
    hideLoading: function(element) {
        $(element).find('.spinner-custom').remove();
    }
};

// Notificações
const Notifications = {
    show: function(message, type = 'info', timeout = MIMO.config.alertTimeout) {
        const alertClass = type === 'error' ? 'danger' : type;
        const icon = this.getIcon(type);
        
        const alert = `
            <div class="alert alert-${alertClass} alert-dismissible fade show" role="alert">
                <i class="bi bi-${icon} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        $('.container').first().prepend(alert);
        
        if (timeout > 0) {
            setTimeout(() => {
                $('.alert').first().fadeOut();
            }, timeout);
        }
    },
    
    getIcon: function(type) {
        const icons = {
            success: 'check-circle',
            error: 'exclamation-triangle',
            warning: 'exclamation-circle',
            info: 'info-circle'
        };
        return icons[type] || 'info-circle';
    },
    
    success: function(message) {
        this.show(message, 'success');
    },
    
    error: function(message) {
        this.show(message, 'error');
    },
    
    warning: function(message) {
        this.show(message, 'warning');
    },
    
    info: function(message) {
        this.show(message, 'info');
    }
};

// Formulários
const Forms = {
    // Validar formulário
    validate: function(formId) {
        const form = document.getElementById(formId);
        if (!form) return false;
        
        let isValid = true;
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                this.showFieldError(input, 'Este campo é obrigatório');
                isValid = false;
            } else {
                this.clearFieldError(input);
            }
            
            // Validações específicas
            if (input.type === 'email' && input.value && !Utils.validateEmail(input.value)) {
                this.showFieldError(input, 'Email inválido');
                isValid = false;
            }
        });
        
        return isValid;
    },
    
    // Mostrar erro no campo
    showFieldError: function(input, message) {
        this.clearFieldError(input);
        input.classList.add('is-invalid');
        
        const feedback = document.createElement('div');
        feedback.className = 'invalid-feedback';
        feedback.textContent = message;
        input.parentNode.appendChild(feedback);
    },
    
    // Limpar erro do campo
    clearFieldError: function(input) {
        input.classList.remove('is-invalid');
        const feedback = input.parentNode.querySelector('.invalid-feedback');
        if (feedback) {
            feedback.remove();
        }
    },
    
    // Submeter formulário via AJAX
    submit: function(formId, url, callback) {
        if (!this.validate(formId)) {
            return false;
        }
        
        const form = document.getElementById(formId);
        const formData = new FormData(form);
        
        $.ajax({
            url: url,
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    Notifications.success(response.message);
                    if (callback) callback(response);
                } else {
                    Notifications.error(response.message);
                }
            },
            error: function() {
                Notifications.error('Erro ao processar solicitação');
            }
        });
    }
};

// Tabelas
const Tables = {
    // Inicializar DataTable
    init: function(tableId, options = {}) {
        const defaultOptions = {
            language: {
                url: '//cdn.datatables.net/plug-ins/1.13.4/i18n/pt-BR.json'
            },
            responsive: true,
            pageLength: 25,
            order: [[0, 'desc']]
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        return $(`#${tableId}`).DataTable(finalOptions);
    },
    
    // Recarregar tabela
    reload: function(tableId) {
        $(`#${tableId}`).DataTable().ajax.reload();
    }
};

// Modais
const Modals = {
    // Abrir modal
    open: function(modalId, data = {}) {
        const modal = new bootstrap.Modal(document.getElementById(modalId));
        
        // Preencher dados se fornecidos
        if (Object.keys(data).length > 0) {
            this.populateModal(modalId, data);
        }
        
        modal.show();
        return modal;
    },
    
    // Fechar modal
    close: function(modalId) {
        const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
        if (modal) {
            modal.hide();
        }
    },
    
    // Preencher modal com dados
    populateModal: function(modalId, data) {
        const modal = document.getElementById(modalId);
        
        Object.keys(data).forEach(key => {
            const element = modal.querySelector(`[name="${key}"], #${key}`);
            if (element) {
                if (element.type === 'checkbox') {
                    element.checked = data[key];
                } else {
                    element.value = data[key];
                }
            }
        });
    }
};

// Calendário
const Calendar = {
    // Renderizar calendário
    render: function(containerId, events = []) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const today = moment();
        const startOfMonth = today.clone().startOf('month');
        const endOfMonth = today.clone().endOf('month');
        const startDate = startOfMonth.clone().startOf('week');
        const endDate = endOfMonth.clone().endOf('week');
        
        let html = '<div class="calendar-grid">';
        
        // Cabeçalho dos dias da semana
        html += '<div class="row text-center fw-bold mb-2">';
        const weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        weekdays.forEach(day => {
            html += `<div class="col">${day}</div>`;
        });
        html += '</div>';
        
        // Dias do mês
        const current = startDate.clone();
        while (current.isSameOrBefore(endDate)) {
            if (current.day() === 0) {
                html += '<div class="row">';
            }
            
            const isToday = current.isSame(today, 'day');
            const isCurrentMonth = current.isSame(today, 'month');
            const dayEvents = events.filter(event => 
                moment(event.date).isSame(current, 'day')
            );
            
            html += `
                <div class="col calendar-day ${isToday ? 'today' : ''} ${!isCurrentMonth ? 'text-muted' : ''}">
                    <div class="fw-bold mb-1">${current.date()}</div>
                    ${dayEvents.map(event => 
                        `<div class="calendar-event" title="${event.title}">${event.title}</div>`
                    ).join('')}
                </div>
            `;
            
            if (current.day() === 6) {
                html += '</div>';
            }
            
            current.add(1, 'day');
        }
        
        html += '</div>';
        container.innerHTML = html;
    }
};

// Inicialização quando o documento estiver pronto
$(document).ready(function() {
    // Configurar moment.js
    moment.locale('pt-br');
    
    // Máscaras para inputs
    $('input[data-mask="phone"]').mask('(00) 00000-0000');
    $('input[data-mask="cpf"]').mask('000.000.000-00');
    $('input[data-mask="cnpj"]').mask('00.000.000/0000-00');
    $('input[data-mask="currency"]').mask('#.##0,00', {reverse: true});
    
    // Auto-save para formulários
    $('form[data-autosave]').on('input', function() {
        const formData = $(this).serialize();
        localStorage.setItem(`form_${this.id}`, formData);
    });
    
    // Restaurar dados salvos
    $('form[data-autosave]').each(function() {
        const savedData = localStorage.getItem(`form_${this.id}`);
        if (savedData) {
            const params = new URLSearchParams(savedData);
            params.forEach((value, key) => {
                const input = this.querySelector(`[name="${key}"]`);
                if (input && !input.value) {
                    input.value = value;
                }
            });
        }
    });
    
    // Confirmação para exclusões
    $('.btn-delete').click(function(e) {
        if (!confirm('Tem certeza que deseja excluir este item?')) {
            e.preventDefault();
        }
    });
    
    // Tooltips
    $('[data-bs-toggle="tooltip"]').tooltip();
    
    // Popovers
    $('[data-bs-toggle="popover"]').popover();
});

// Exportar para uso global
window.MIMO = MIMO;
window.Utils = Utils;
window.Notifications = Notifications;
window.Forms = Forms;
window.Tables = Tables;
window.Modals = Modals;
window.Calendar = Calendar;
