/* Arquivo JavaScript principal para o aplicativo veterinário */

// Espera o DOM carregar completamente
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa tooltips do Bootstrap
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Inicializa popovers do Bootstrap
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Animação para elementos ao entrar na viewport
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 50) {
                element.classList.add('animated');
            }
        });
    };

    // Executa a animação ao carregar e ao rolar a página
    animateOnScroll();
    window.addEventListener('scroll', animateOnScroll);

    // Validação de formulários
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    });

    // Máscaras para campos de formulário
    const cpfInputs = document.querySelectorAll('.cpf-mask');
    cpfInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            
            if (value.length > 9) {
                value = value.replace(/^(\d{3})(\d{3})(\d{3})(\d{2}).*/, '$1.$2.$3-$4');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{3})(\d{3})(\d{0,3}).*/, '$1.$2.$3');
            } else if (value.length > 3) {
                value = value.replace(/^(\d{3})(\d{0,3}).*/, '$1.$2');
            }
            
            e.target.value = value;
        });
    });

    const phoneInputs = document.querySelectorAll('.phone-mask');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, '');
            if (value.length > 11) value = value.slice(0, 11);
            
            if (value.length > 10) {
                value = value.replace(/^(\d{2})(\d{5})(\d{4}).*/, '($1) $2-$3');
            } else if (value.length > 6) {
                value = value.replace(/^(\d{2})(\d{4})(\d{0,4}).*/, '($1) $2-$3');
            } else if (value.length > 2) {
                value = value.replace(/^(\d{2})(\d{0,5}).*/, '($1) $2');
            }
            
            e.target.value = value;
        });
    });

    // Preview de imagem ao selecionar arquivo
    const photoInput = document.querySelector('#id_foto');
    const photoPreview = document.querySelector('.photo-preview');
    
    if (photoInput && photoPreview) {
        photoInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    photoPreview.style.backgroundImage = `url(${e.target.result})`;
                    photoPreview.classList.remove('no-image');
                    photoPreview.innerHTML = '';
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Animação para cards na dashboard
    const dashboardCards = document.querySelectorAll('.dashboard-stat-card');
    dashboardCards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Efeito de hover para botões de ação
    const actionButtons = document.querySelectorAll('.btn-action');
    actionButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.classList.add('pulse');
        });
        button.addEventListener('mouseleave', function() {
            this.classList.remove('pulse');
        });
    });

    // Notificações toast
    const toastElements = document.querySelectorAll('.toast');
    toastElements.forEach(toastEl => {
        const toast = new bootstrap.Toast(toastEl, {
            autohide: true,
            delay: 5000
        });
        toast.show();
    });

    // Confirmação para exclusão
    const deleteButtons = document.querySelectorAll('.btn-delete-confirm');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item? Esta ação não pode ser desfeita.')) {
                e.preventDefault();
            }
        });
    });

    // Filtros dinâmicos
    const filterSelects = document.querySelectorAll('.dynamic-filter');
    filterSelects.forEach(select => {
        select.addEventListener('change', function() {
            const form = this.closest('form');
            if (form) {
                form.submit();
            }
        });
    });

    // Animação para o logo
    const logo = document.querySelector('.navbar-brand');
    if (logo) {
        logo.addEventListener('mouseenter', function() {
            this.classList.add('pulse');
        });
        logo.addEventListener('mouseleave', function() {
            this.classList.remove('pulse');
        });
    }

    // Efeito de parallax para o header da página inicial
    const header = document.querySelector('.hero-header');
    if (header) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.scrollY;
            header.style.backgroundPositionY = `${scrollPosition * 0.5}px`;
        });
    }
});

// Função para alternar o tema claro/escuro
function toggleTheme() {
    const body = document.body;
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark-theme');
        localStorage.setItem('theme', 'dark');
    }
}

// Verifica o tema salvo no localStorage
function checkTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
    }
}

// Executa a verificação do tema ao carregar a página
window.addEventListener('DOMContentLoaded', checkTheme);
