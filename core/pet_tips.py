import random
from django.core.cache import cache

# Lista abrangente de dicas de cuidados com pets
DEFAULT_PET_TIPS = [
    # Saúde Bucal
    "Escove os dentes do seu pet diariamente com pasta específica para animais. A saúde bucal previne doenças graves e mau hálito.",
    "Ofereça brinquedos de morder apropriados para ajudar na limpeza dos dentes e aliviar o desconforto da troca dentária em filhotes.",
    "Consulte um veterinário especializado em odontologia para limpezas dentárias anuais e verificação de problemas bucais.",
    
    # Alimentação
    "Mantenha uma rotina de alimentação com horários fixos e porções adequadas ao tamanho, idade e nível de atividade do seu pet.",
    "Evite dar alimentos humanos, especialmente chocolate, cebola, alho, uva, passas e adoçantes como xilitol, que são tóxicos.",
    "A transição entre rações deve ser feita gradualmente ao longo de 7-10 dias para evitar problemas digestivos.",
    
    # Hidratação
    "Mantenha sempre água fresca e limpa disponível. Troque a água pelo menos duas vezes ao dia para incentivar a hidratação.",
    "Em dias quentes, adicione cubos de gelo ou use fontes de água para estimular o consumo de líquidos, especialmente para gatos.",
    
    # Exercícios
    "Cães precisam de pelo menos 30 minutos a 2 horas de exercícios diários, dependendo da raça e idade.",
    "Enriqueça o ambiente do seu gato com arranhadores, prateleiras e brinquedos que estimulem o comportamento de caça.",
    
    # Higiene
    "Banhos devem ser dados a cada 4-6 semanas para a maioria dos cães, usando produtos específicos para pets para não ressecar a pele.",
    "Escove seu pet regularmente para remover pelos mortos, especialmente em raças de pelo longo ou durante a troca de pelagem.",
    
    # Saúde Preventiva
    "Mantenha em dia a vacinação e o controle de parasitas (pulgas, carrapatos e vermes) conforme orientação do veterinário.",
    "Castrar seu pet pode prevenir diversos problemas de saúde e contribuir para o controle populacional de animais.",
    
    # Comportamento
    "O adestramento com reforço positivo fortalece o vínculo e melhora a comunicação entre você e seu pet.",
    "Gatos precisam de arranhadores para marcar território e manter as unhas saudáveis - coloque em áreas estratégicas da casa.",
    
    # Segurança
    "Nunca deixe seu pet sozinho no carro, mesmo com os vidros abertos. A temperatura pode subir rapidamente e causar hipertermia.",
    "Use coleira com identificação e considere a microchipagem para aumentar as chances de reencontro em caso de fuga ou perda.",
    
    # Idosos
    "Pets idosos precisam de check-ups veterinários mais frequentes, pelo menos a cada 6 meses.",
    "Adapte a alimentação e os exercícios conforme a idade e condições de saúde do seu pet sênior.",
    
    # Bem-estar emocional
    "Pets também podem sofrer de ansiedade e estresse. Mantenha uma rotina estável e ofereça um ambiente seguro e tranquilo.",
    "Brincadeiras e carinho são essenciais para o bem-estar emocional do seu pet e fortalecem seu vínculo com ele.",
    
    # Viagens e Transporte
    "Use caixas de transporte seguras e acostume seu pet desde cedo para evitar estresse durante viagens.",
    "Em viagens longas, faça paradas regulares para seu cachorro se exercitar e fazer suas necessidades.",
    
    # Primeiros Socorros
    "Tenha um kit de primeiros socorros para pets em casa e saiba os telefones de emergência de clínicas 24h da sua região.",
    "Aprenda a verificar os sinais vitais do seu pet: frequência cardíaca, respiração e temperatura corporal.",
    
    # Enriquecimento Ambiental
    "Gatos adoram locais altos para observação. Considere prateleiras ou árvores de gato perto de janelas.",
    "Esconda petiscos ou ração em brinquedos interativos para estimular o instinto de caça e forrageamento.",
    
    # Mudanças Comportamentais
    "Mudanças súbitas no comportamento podem indicar problemas de saúde. Consulte um veterinário se notar algo incomum.",
    "Arranhar móveis ou fazer xixi fora do lugar podem ser sinais de estresse ou problemas de saúde que precisam de atenção.",
    
    # Cuidados Específicos por Espécie
    "Coelhos precisam de feno de qualidade ilimitado para manter o sistema digestivo saudável e desgastar os dentes.",
    "Pássaros precisam de brinquedos e poleiros de diferentes espessuras para exercitar os pés e evitar problemas articulares.",
    
    # Verificação Geral de Saúde
    "Faça um check-up mensal em casa: verifique olhos, ouvidos, boca, pele, patas e peso do seu pet.",
    "Observe o apetite, consumo de água, nível de energia e hábitos de eliminação do seu pet diariamente para identificar mudanças.",
    
    # Dicas para Filhotes
    "Socialize seu filhote com pessoas, animais e ambientes diferentes entre 3 e 14 semanas de vida para um desenvolvimento equilibrado.",
    "Estabeleça uma rotina de alimentação, brincadeiras e descanso para ajudar no treinamento e adaptação do filhote.",
    
    # Cuidados com o Calor
    "Nunca tose seu cão no verão. A pelagem ajuda a regular a temperatura e protege contra queimaduras solares.",
    "Ofereça locais frescos e sombreados, e evite passeios nos horários mais quentes do dia.",
    
    # Cuidados com o Frio
    "Pets também sentem frio! Forneça cobertores e casinhas isoladas para animais que ficam em áreas externas.",
    "Seque bem seu pet após banhos ou chuva, principalmente as patas e entre os dedos, para evitar fungos e resfriados.",
    
    # Cuidados com Idosos
    "Pets idosos podem desenvolver artrite. Considere rampas ou degraus para ajudá-los a subir em móveis e camas ortopédicas.",
    "Alguns pets idosos podem desenvolver demência. Mantenha a rotina estável e evite mudanças bruscas no ambiente.",
    
    # Cuidados com Gatos
    "Gatos precisam de pelo menos uma caixa de areia por gato, mais uma extra, em locais tranquilos e de fácil acesso.",
    "Arranhadores verticais e horizontais atendem a diferentes necessidades de alongamento e marcação de território dos gatos.",
    
    # Cuidados com Cães
    "Passeios diários são essenciais para a saúde física e mental do seu cão, além de serem oportunidades importantes de socialização.",
    "Ensine comandos básicos como 'senta', 'fica' e 'aqui' para a segurança e melhor convivência com seu cão.",
    
    # Dicas Finais
    "Nunca medique seu pet sem orientação veterinária. Medicamentos humanos podem ser altamente tóxicos para animais.",
    "Considere um seguro saúde para pets para ajudar nos custos com consultas, exames e emergências veterinárias."
]

def get_random_pet_tip():
    """Obtém uma dica aleatória sobre cuidados com pets."""
    # Verifica se há uma dica em cache
    cached_tip = cache.get('current_pet_tip')
    if cached_tip:
        return cached_tip
    
    # Seleciona uma dica aleatória
    tip = random.choice(DEFAULT_PET_TIPS)
    
    # Armazena a dica em cache por 5 segundos
    cache.set('current_pet_tip', tip, 5)
    return tip
