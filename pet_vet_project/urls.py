from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from core.api_views import pet_tip_api
from core.views import login_with_captcha

def redirect_to_login(request):
    return redirect('login')

def redirect_to_contact(request):
    return redirect('core:contact')

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('contato/', redirect_to_contact, name='contact_redirect'),
    path('api/pet-tip/', pet_tip_api, name='pet_tip_api'),
    
    # URLs de autenticação
    path('login/', login_with_captcha, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]

# Adiciona URLs para servir arquivos estáticos e de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
