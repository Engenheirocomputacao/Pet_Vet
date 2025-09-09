// Controle de tamanho de fonte
document.addEventListener('DOMContentLoaded', function() {
    const increaseFont = document.getElementById('increaseFont');
    const decreaseFont = document.getElementById('decreaseFont');
    const normalFont = document.getElementById('normalFont');
    const highContrast = document.getElementById('highContrast');

    // Aumentar fonte
    increaseFont.addEventListener('click', function() {
        document.body.classList.remove('font-size-small', 'font-size-medium');
        document.body.classList.add('font-size-large');
        localStorage.setItem('fontSize', 'large');
    });

    // Diminuir fonte
    decreaseFont.addEventListener('click', function() {
        document.body.classList.remove('font-size-large', 'font-size-medium');
        document.body.classList.add('font-size-small');
        localStorage.setItem('fontSize', 'small');
    });

    // Fonte normal
    normalFont.addEventListener('click', function() {
        document.body.classList.remove('font-size-small', 'font-size-large');
        document.body.classList.add('font-size-medium');
        localStorage.setItem('fontSize', 'medium');
    });

    // Alto contraste
    highContrast.addEventListener('click', function() {
        document.body.classList.toggle('high-contrast');
        this.classList.toggle('active');
        localStorage.setItem('highContrast', document.body.classList.contains('high-contrast'));
    });

    // Carregar preferências salvas
    const fontSize = localStorage.getItem('fontSize');
    if (fontSize) {
        document.body.classList.add('font-size-' + fontSize);
    }

    if (localStorage.getItem('highContrast') === 'true') {
        document.body.classList.add('high-contrast');
        highContrast.classList.add('active');
    }
}); 