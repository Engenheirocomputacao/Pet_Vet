// Sistema de Captcha de Imagem para Login
class CaptchaManager {
    constructor() {
        this.captchaUrl = '/core/generate-captcha/';
        this.isLoading = false;
        this.init();
    }

    init() {
        this.loadCaptcha();
        this.setupEventListeners();
    }

    async loadCaptcha() {
        if (this.isLoading) return;
        
        this.setLoadingState(true);
        
        try {
            const response = await fetch(this.captchaUrl);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Atualizar elementos do DOM
            document.getElementById('captcha_id').value = data.captcha_id;
            
            // Atualizar imagem do captcha
            const imageElement = document.getElementById('captcha-image');
            imageElement.src = data.image;
            imageElement.alt = 'Captcha - Digite os caracteres mostrados';
            
            // Limpar campo de entrada
            document.getElementById('captcha_answer').value = '';
            
            // Limpar mensagens de erro
            this.clearMessages();
            
            // Mostrar sucesso temporário
            this.showSuccess('Novo código carregado!');
            
            // Focar no campo de entrada
            document.getElementById('captcha_answer').focus();
            
        } catch (error) {
            console.error('Erro ao carregar captcha:', error);
            document.getElementById('captcha-image').src = '';
            this.showError('Erro ao carregar código. Tente novamente.');
        } finally {
            this.setLoadingState(false);
        }
    }

    setLoadingState(loading) {
        this.isLoading = loading;
        const container = document.querySelector('.captcha-container');
        const refreshButton = document.querySelector('.captcha-refresh');
        
        if (loading) {
            container.classList.add('captcha-loading');
            refreshButton.disabled = true;
            document.getElementById('captcha-image').style.opacity = '0.5';
        } else {
            container.classList.remove('captcha-loading');
            refreshButton.disabled = false;
            document.getElementById('captcha-image').style.opacity = '1';
        }
    }

    refreshCaptcha() {
        this.loadCaptcha();
    }

    setupEventListeners() {
        // Botão de atualizar captcha
        const refreshButton = document.querySelector('.captcha-refresh');
        if (refreshButton) {
            refreshButton.addEventListener('click', () => this.refreshCaptcha());
        }

        // Validação do formulário
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', (e) => this.validateForm(e));
        }

        // Focar no campo de resposta quando pressionar Enter
        const captchaInput = document.getElementById('captcha_answer');
        if (captchaInput) {
            captchaInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    e.preventDefault();
                    document.querySelector('.btn-login').click();
                }
            });
            
            // Validar entrada em tempo real
            captchaInput.addEventListener('input', (e) => {
                this.validateInput(e.target.value);
            });
        }
    }

    validateInput(value) {
        const input = document.getElementById('captcha_answer');
        
        // Converter para maiúsculas e permitir apenas letras e números
        const cleanValue = value.replace(/[^a-zA-Z0-9]/g, '').toUpperCase();
        if (value !== cleanValue) {
            input.value = cleanValue;
        }
        
        // Limitar a 6 caracteres
        if (cleanValue.length > 6) {
            input.value = cleanValue.substring(0, 6);
        }
        
        // Limpar mensagens de erro se o usuário começar a digitar
        if (value && this.hasError()) {
            this.clearMessages();
        }
    }

    validateForm(e) {
        const captchaAnswer = document.getElementById('captcha_answer').value;
        const captchaId = document.getElementById('captcha_id').value;
        
        if (!captchaAnswer || !captchaId) {
            e.preventDefault();
            this.showError('Por favor, digite o código do captcha antes de continuar.');
            document.getElementById('captcha_answer').focus();
            return false;
        }

        // Validar se tem pelo menos 6 caracteres
        if (captchaAnswer.length < 6) {
            e.preventDefault();
            this.showError('Por favor, digite todos os 6 caracteres.');
            document.getElementById('captcha_answer').focus();
            return false;
        }
        
        // Validar se contém apenas letras e números
        if (!/^[A-Z0-9]{6}$/.test(captchaAnswer)) {
            e.preventDefault();
            this.showError('Por favor, digite apenas letras e números.');
            document.getElementById('captcha_answer').focus();
            return false;
        }
    }

    showError(message) {
        this.clearMessages();
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'captcha-error';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
        
        const captchaContainer = document.querySelector('.captcha-container');
        captchaContainer.appendChild(errorDiv);
    }

    showSuccess(message) {
        this.clearMessages();
        
        const successDiv = document.createElement('div');
        successDiv.className = 'captcha-success';
        successDiv.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
        
        const captchaContainer = document.querySelector('.captcha-container');
        captchaContainer.appendChild(successDiv);
        
        // Remover mensagem de sucesso após 2 segundos
        setTimeout(() => {
            if (successDiv.parentNode) {
                successDiv.remove();
            }
        }, 2000);
    }

    clearMessages() {
        const errorElement = document.querySelector('.captcha-error');
        const successElement = document.querySelector('.captcha-success');
        
        if (errorElement) {
            errorElement.remove();
        }
        if (successElement) {
            successElement.remove();
        }
    }

    hasError() {
        return document.querySelector('.captcha-error') !== null;
    }
}

// Inicializar o gerenciador de captcha quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    new CaptchaManager();
}); 