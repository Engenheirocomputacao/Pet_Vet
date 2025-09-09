"""
Configurações do projeto Django para o sistema veterinário
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configurações de Segurança Essenciais ---

# SECURITY WARNING: keep the secret key used in production secret!
# É altamente recomendado carregar esta chave de uma variável de ambiente ou gerenciador de segredos em produção.
# Exemplo: SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'sua-chave-padrao-desenvolvimento')
SECRET_KEY = 'django-insecure-pet-vet-project-secret-key-123456789'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: Seja mais específico com ALLOWED_HOSTS em produção.
# Evite usar '*' em produção. Liste apenas os domínios que seu site servirá.
# Exemplo: ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# --- Definição das Aplicações ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # Aplicativo principal
]

# --- Middlewares ---
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- Configuração de Cache ---
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'petvet-cache',
    }
}

# Tempo de vida do cache em segundos (30 segundos)
CACHE_TTL = 30

# --- Configuração de URLs ---
ROOT_URLCONF = 'pet_vet_project.urls'

# --- Configuração de Templates ---
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Diretório onde os templates globais do projeto são procurados.
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- Configuração WSGI ---
WSGI_APPLICATION = 'pet_vet_project.wsgi.application'

# --- Banco de Dados ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases
# Considere usar variáveis de ambiente para configurar o banco de dados em produção.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- Validação de Senhas ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalização ---
# https://docs.djangoproject.com/en/5.2/topics/i18n/
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- Arquivos Estáticos (CSS, JavaScript, Imagens) ---
# https://docs.djangoproject.com/en/5.2/howto/static-files/
STATIC_URL = '/static/'
# Diretório onde o Django procura arquivos estáticos não vinculados a um app específico durante o desenvolvimento.
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
# Diretório onde o comando `collectstatic` reunirá todos os arquivos estáticos para implantação em produção.
# Certifique-se de que seu servidor web de produção (ex: Nginx) esteja configurado para servir arquivos deste diretório.
STATIC_ROOT = BASE_DIR / 'staticfiles'

# --- Arquivos de Mídia (Uploads de Usuários) ---
# https://docs.djangoproject.com/en/5.2/topics/files/
MEDIA_URL = '/media/'
# Diretório onde os arquivos enviados pelos usuários serão armazenados.
MEDIA_ROOT = BASE_DIR / 'media'
# Certifique-se de que seu servidor web de produção esteja configurado para servir arquivos de MEDIA_ROOT via MEDIA_URL.
# Garanta também que o diretório MEDIA_ROOT tenha permissões de escrita apropriadas para o processo do servidor web.

# --- Tipo de Chave Primária Padrão ---
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- Mensagens do Django Framework ---
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert-secondary',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

# --- Configurações de Autenticação ---
LOGIN_URL = 'login' # Nome da URL para a página de login
LOGIN_REDIRECT_URL = 'core:index' # Nome da URL para redirecionar após login bem-sucedido
LOGOUT_REDIRECT_URL = 'login' # Nome da URL para redirecionar após logout

# --- Configurações de Email (Ex: para recuperação de senha) ---
# Para desenvolvimento, usar o console backend é útil para ver emails no terminal.
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# Para produção, configure um backend SMTP real:
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.example.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
# EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASS')

# --- Configurações de Segurança para Desenvolvimento ---
if DEBUG:
    # Forçar HTTP em desenvolvimento
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SECURE_REFERRER_POLICY = None
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None
    SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = None
    SECURE_CROSS_ORIGIN_RESOURCE_POLICY = None
    
    # Configurações adicionais para desenvolvimento
    SECURE_PROXY_SSL_HEADER = None
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SECURE_REFERRER_POLICY = None
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None
    SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = None
    SECURE_CROSS_ORIGIN_RESOURCE_POLICY = None

    # Configurações específicas para forçar HTTP
    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = None
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    SECURE_REFERRER_POLICY = None
    SECURE_CROSS_ORIGIN_OPENER_POLICY = None
    SECURE_CROSS_ORIGIN_EMBEDDER_POLICY = None
    SECURE_CROSS_ORIGIN_RESOURCE_POLICY = None
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

