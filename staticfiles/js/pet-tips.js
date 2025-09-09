document.addEventListener('DOMContentLoaded', function() {
    const petTipElement = document.getElementById('pet-tip');
    const UPDATE_INTERVAL = 5000; // 5 segundos em milissegundos
    let tipInterval;
    
    // Função para buscar a próxima dica
    function fetchNextTip() {
        // Mostra o indicador de carregamento
        petTipElement.innerHTML = '<i class="fas fa-spinner fa-spin" aria-hidden="true"></i> Carregando dica...';
        
        // Adiciona um timestamp para evitar cache do navegador
        const timestamp = new Date().getTime();
        
        // Faz uma requisição para obter uma nova dica
        fetch(`/api/pet-tip/?t=${timestamp}`, {
            method: 'GET',
            headers: {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Atualiza o texto da dica
            if (data && data.tip && data.tip.trim() !== '') {
                petTipElement.textContent = data.tip;
                console.log('Nova dica carregada com sucesso');
            } else {
                throw new Error('Dica vazia ou formato inválido');
            }
        })
        .catch(error => {
            console.error('Erro ao carregar dica:', error);
            // Usa uma dica padrão em caso de erro
            const defaultTips = [
                "A escovação diária dos dentes do seu pet pode prevenir doenças periodontais graves.",
                "A vacinação anual é essencial para prevenir doenças como raiva e cinomose.",
                "Mantenha sempre água limpa e fresca disponível para o seu pet.",
                "A obesidade em pets pode reduzir significativamente a expectativa de vida.",
                "Consulte regularmente um médico veterinário para check-ups preventivos."
            ];
            const randomIndex = Math.floor(Math.random() * defaultTips.length);
            petTipElement.textContent = defaultTips[randomIndex];
        });
    }
    
    // Inicia a troca automática de dicas
    function startTipRotation() {
        // Busca a primeira dica imediatamente
        fetchNextTip();
        
        // Configura o intervalo para trocar as dicas
        tipInterval = setInterval(fetchNextTip, UPDATE_INTERVAL);
    }
    
    // Inicia o carrossel de dicas
    startTipRotation();
    
    // Limpa o intervalo quando a página for descarregada
    window.addEventListener('beforeunload', function() {
        if (tipInterval) {
            clearInterval(tipInterval);
        }
    });
});
