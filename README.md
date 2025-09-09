# PetVet - Sistema Veterinário

Sistema completo para gerenciamento de clínicas veterinárias, com foco na saúde e bem-estar dos pets.

## Funcionalidades

- **Cadastro de Donos**: Gerenciamento completo de informações dos tutores dos pets
- **Cadastro de Pets**: Registro detalhado dos animais, incluindo upload de fotos
- **Consultas**: Agendamento e registro de consultas, diagnósticos e tratamentos
- **Medicações**: Cadastro de medicamentos e controle de prescrições
- **Agenda**: Sistema de agendamento para consultas, medicações, vacinas e exames
- **Dashboard**: Visão geral das atividades e estatísticas da clínica

## Recursos de Acessibilidade

O sistema foi desenvolvido com foco em acessibilidade, incluindo:

- **Alto Contraste**: Modo de alto contraste para pessoas com baixa visão
- **VLibras**: Integração com o VLibras para tradução em Língua Brasileira de Sinais
- **Tamanho de Texto Ajustável**: Controles para aumentar o tamanho do texto
- **Navegação por Teclado**: Suporte completo para navegação sem mouse
- **Redução de Movimento**: Opção para desativar animações
- **Skip to Content**: Link para pular diretamente para o conteúdo principal
- **Suporte a Leitores de Tela**: Marcações ARIA e textos alternativos

## Tecnologias Utilizadas

- **Backend**: Python 3.11 com Django 5.2
- **Banco de Dados**: SQLite (padrão para desenvolvimento, configurável para produção)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Acessibilidade**: ARIA, VLibras, CSS personalizado
- **Calendário**: FullCalendar para visualização de agendamentos

## Instalação e Execução (Desenvolvimento)

1.  **Clone o repositório:**
    ```bash
    git clone <url_do_repositorio>
    cd pet_vet
    ```
2.  **Crie e ative um ambiente virtual Python:** (Recomendado)
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # venv\Scripts\activate  # Windows
    ```
    **Importante:** Não inclua o diretório `venv` no controle de versão (adicione-o ao `.gitignore`) nem em pacotes de distribuição.
3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Execute as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```
    **Nota:** O arquivo `db.sqlite3` é criado automaticamente. Não o inclua no controle de versão se estiver usando SQLite em desenvolvimento e pretender usar outro banco em produção.
5.  **(Opcional) Crie um superusuário:** Para acessar a área administrativa (`/admin/`).
    ```bash
    python manage.py createsuperuser
    ```
6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
7.  Acesse o sistema em `http://127.0.0.1:8000` ou `http://localhost:8000`.

## Configuração para Produção

Para implantar o PetVet em um ambiente de produção, siga estas recomendações:

1.  **Variáveis de Ambiente:** **Nunca** use as configurações padrão de `SECRET_KEY` e `DEBUG = True` em produção. Configure-as através de variáveis de ambiente ou um sistema de gerenciamento de segredos.
    *   `DJANGO_SECRET_KEY`: Defina uma chave secreta longa e aleatória.
    *   `DJANGO_DEBUG`: Defina como `False`.
    *   `DJANGO_ALLOWED_HOSTS`: Liste os domínios permitidos para o seu site (ex: `meusite.com,www.meusite.com`).
    *   Considere também configurar as credenciais do banco de dados (`DATABASES` em `settings.py`) e de email (`EMAIL_*`) via variáveis de ambiente.
2.  **Banco de Dados:** Use um banco de dados robusto como PostgreSQL ou MySQL em produção. Configure a seção `DATABASES` em `settings.py` de acordo (preferencialmente usando variáveis de ambiente).
3.  **Servidor WSGI/ASGI:** Não use o servidor de desenvolvimento (`runserver`) em produção. Use um servidor WSGI como Gunicorn ou uWSGI.
    *   Instale o Gunicorn: `pip install gunicorn` (adicione ao `requirements.txt` se for usar)
    *   Execute com Gunicorn (exemplo básico):
        ```bash
        gunicorn pet_vet_project.wsgi:application --bind 0.0.0.0:8000
        ```
        (Ajuste a porta e considere usar mais workers e outras configurações avançadas).
4.  **Arquivos Estáticos:** Colete todos os arquivos estáticos em um único diretório usando:
    ```bash
    python manage.py collectstatic
    ```
    Configure seu servidor web (Nginx, Apache) para servir os arquivos do diretório `STATIC_ROOT` (definido em `settings.py`, geralmente `staticfiles/`).
5.  **Arquivos de Mídia:** Configure seu servidor web para servir os arquivos do diretório `MEDIA_ROOT` (definido em `settings.py`, geralmente `media/`). Garanta que o processo do servidor WSGI tenha permissão de escrita neste diretório.
6.  **HTTPS:** Configure seu servidor web para usar HTTPS para proteger a comunicação. Ajuste as configurações de segurança do Django em `settings.py` (`SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`, `SECURE_SSL_REDIRECT`) para `True`.

## Design Moderno e Responsivo

O sistema conta com um design moderno, utilizando cores atuais e animações suaves para uma experiência agradável. A interface é totalmente responsiva, adaptando-se a diferentes tamanhos de tela, desde smartphones até desktops.

## Estrutura do Projeto

- **core/**: Aplicativo principal com modelos, views e templates.
- **pet_vet_project/**: Configurações do projeto Django (`settings.py`, `urls.py`, etc.).
- **static/**: Arquivos estáticos globais do projeto (CSS, JS, imagens) usados durante o desenvolvimento.
- **media/**: Diretório onde os arquivos de mídia enviados pelos usuários (fotos dos pets) são armazenados.
- **templates/**: Templates HTML globais do projeto.
- **requirements.txt**: Lista de dependências Python do projeto.
- **manage.py**: Utilitário de linha de comando do Django.
- **README.md**: Este arquivo.

## Personalização

O sistema pode ser facilmente personalizado para atender às necessidades específicas de cada clínica veterinária, incluindo:

- Adição de novos campos nos modelos
- Personalização de cores e estilos
- Integração com outros sistemas
- Configuração para diferentes bancos de dados

## Licença

Este projeto é distribuído sob a licença MIT.

