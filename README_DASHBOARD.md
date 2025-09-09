# 🏥 Dashboard Veterinário PetVet

## 📋 Visão Geral

O Dashboard Veterinário PetVet é uma solução completa de análise de dados para clínicas veterinárias, oferecendo três dashboards especializados:

1. **Dashboard Principal** - Visão geral da clínica
2. **Dashboard Financeiro** - Análise financeira e de procedimentos
3. **Dashboard de Saúde** - Análise médica e epidemiológica

## 🚀 Funcionalidades Principais

### 📊 Dashboard Principal (`/core/dashboard-veterinario/`)

- **Métricas Gerais**: Total de donos, pets, consultas, agendamentos
- **Gráficos Interativos**: 
  - Consultas dos últimos 7 dias
  - Distribuição por espécie
  - Crescimento mensal
  - Performance dos veterinários
- **Tabelas de Dados**:
  - Top veterinários
  - Top clientes
  - Status das consultas
  - Distribuição por idade

### 💰 Dashboard Financeiro (`/core/dashboard-financeiro/`)

- **Métricas Financeiras**: Faturamento mensal, semanal, anual
- **Análise por Abas**:
  - **Procedimentos**: Faturamento por tipo, volume, top procedimentos
  - **Veterinários**: Performance financeira, eficiência
  - **Clientes**: Distribuição por valor, frequência de visitas
  - **Tendências**: Evolução temporal, sazonalidade

### 🏥 Dashboard de Saúde (`/core/dashboard-saude/`)

- **Alertas de Saúde**: Vacinações pendentes, consultas de retorno
- **Métricas Médicas**: Vacinações, exames, consultas, cirurgias
- **Análise por Abas**:
  - **Espécies**: Distribuição, raças, estatísticas
  - **Procedimentos**: Tipos, evolução, complicações
  - **Veterinários**: Performance, especialidades, ranking
  - **Epidemiologia**: Doenças por estação, prevalência

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2
- **Frontend**: HTML5, CSS3, JavaScript
- **Gráficos**: Chart.js
- **Banco de Dados**: SQLite (desenvolvimento)
- **Design**: CSS Grid, Flexbox, Gradientes modernos

## 📁 Estrutura do Projeto

```
core/
├── dashboard_views.py          # Views dos dashboards
├── models.py                   # Modelos de dados
├── urls.py                     # URLs dos dashboards
└── ...

templates/
└── dashboard/
    ├── dashboard_home.html     # Dashboard principal
    ├── dashboard_financeiro.html # Dashboard financeiro
    └── dashboard_saude.html    # Dashboard de saúde
```

## 🚀 Como Usar

### 1. Acesso aos Dashboards

Após fazer login no sistema, você encontrará os links no menu de navegação:

- **Dashboard** → Dashboard principal
- **Financeiro** → Dashboard financeiro  
- **Saúde** → Dashboard de saúde

### 2. Navegação

- **Dashboard Principal**: Visão geral com todas as métricas principais
- **Dashboard Financeiro**: Use as abas para navegar entre diferentes análises
- **Dashboard de Saúde**: Explore as abas para análises médicas específicas

### 3. Interatividade

- **Gráficos**: Todos os gráficos são interativos e responsivos
- **Tabelas**: Dados organizados com hover effects
- **Atualização**: Botão "Atualizar Dados" em cada dashboard

## 📊 Tipos de Gráficos Disponíveis

- **Gráficos de Linha**: Para evolução temporal
- **Gráficos de Barras**: Para comparações
- **Gráficos de Pizza/Doughnut**: Para distribuições
- **Gráficos de Radar**: Para comparação de múltiplas métricas
- **Gráficos de Área**: Para tendências com preenchimento

## 🔧 Personalização

### Adicionar Novas Métricas

1. Edite `core/dashboard_views.py`
2. Adicione a lógica de cálculo
3. Atualize o template correspondente

### Modificar Gráficos

1. Edite o arquivo HTML do dashboard
2. Modifique as funções JavaScript de criação de gráficos
3. Ajuste cores, tipos e opções do Chart.js

### Adicionar Novas Abas

1. Crie o conteúdo HTML da nova aba
2. Adicione o botão de navegação
3. Implemente a lógica JavaScript para mostrar/ocultar

## 📱 Responsividade

Todos os dashboards são totalmente responsivos e funcionam em:

- **Desktop**: Layout completo com todas as funcionalidades
- **Tablet**: Adaptação automática para telas médias
- **Mobile**: Layout otimizado para dispositivos móveis

## 🎨 Design System

### Cores Principais
- **Primária**: #667eea (Azul)
- **Secundária**: #764ba2 (Roxo)
- **Sucesso**: #27ae60 (Verde)
- **Aviso**: #f39c12 (Laranja)
- **Perigo**: #e74c3c (Vermelho)

### Componentes
- **Cards**: Fundo branco translúcido com sombras
- **Gráficos**: Cores consistentes e legibilidade
- **Tabelas**: Hover effects e espaçamento adequado
- **Botões**: Gradientes e transições suaves

## 📈 Dados em Tempo Real

Os dashboards utilizam:

- **Dados Estáticos**: Para demonstração e desenvolvimento
- **API Endpoints**: Para dados dinâmicos (`/core/dashboard-api/`)
- **AJAX**: Para atualizações assíncronas

## 🔒 Segurança

- **Autenticação**: Acesso restrito a usuários logados
- **Validação**: Dados validados no backend
- **Sanitização**: Proteção contra XSS e injeção

## 🚀 Próximos Passos

### Funcionalidades Planejadas

1. **Exportação de Relatórios**: PDF, Excel, CSV
2. **Notificações em Tempo Real**: WebSockets
3. **Filtros Avançados**: Por período, veterinário, espécie
4. **Comparativos**: Análise ano vs ano
5. **Alertas Automáticos**: Baseados em regras de negócio

### Melhorias Técnicas

1. **Cache**: Redis para melhor performance
2. **Background Tasks**: Celery para processamento assíncrono
3. **APIs REST**: Endpoints para integração externa
4. **Testes**: Cobertura completa de testes

## 📞 Suporte

Para dúvidas ou sugestões sobre os dashboards:

- **Documentação**: Este README
- **Código**: Arquivos fonte comentados
- **Issues**: Sistema de tickets do projeto

## 🎯 Objetivos do Dashboard

### Para a Clínica
- **Monitoramento**: Acompanhamento de métricas em tempo real
- **Decisões**: Base de dados para tomada de decisões
- **Eficiência**: Identificação de gargalos e oportunidades

### Para Veterinários
- **Performance**: Acompanhamento individual
- **Especialidades**: Foco em áreas de expertise
- **Desenvolvimento**: Identificação de pontos de melhoria

### Para Gestão
- **Financeiro**: Controle de receitas e custos
- **Operacional**: Planejamento de recursos
- **Estratégico**: Análise de tendências e mercado

---

**Desenvolvido com ❤️ para a clínica veterinária PetVet**

*Sistema de Dashboard Completo e Profissional*

