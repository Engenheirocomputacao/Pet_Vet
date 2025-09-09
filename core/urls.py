from django.urls import path
from . import views
from . import dashboard_views

app_name = 'core'

urlpatterns = [
    # Captcha
    path('generate-captcha/', views.generate_captcha, name='generate_captcha'),
    # Páginas principais
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/estatisticas/', views.dashboard_estatisticas, name='dashboard_estatisticas'),
    
    # Dashboard Veterinário
    path('dashboard-veterinario/', dashboard_views.dashboard_home, name='dashboard_veterinario'),
    path('dashboard-financeiro/', dashboard_views.dashboard_financeiro, name='dashboard_financeiro'),
    path('dashboard-saude/', dashboard_views.dashboard_saude, name='dashboard_saude'),
    path('dashboard-debug/', dashboard_views.dashboard_debug, name='dashboard_debug'),
    path('dashboard-simple/', dashboard_views.dashboard_simple, name='dashboard_simple'),
    path('dashboard-api/', dashboard_views.dashboard_api, name='dashboard_api'),
    
    # Donos
    path('donos/', views.dono_list, name='dono_list'),
    path('donos/novo/', views.dono_create, name='dono_create'),
    path('donos/<int:pk>/', views.dono_detail, name='dono_detail'),
    path('donos/<int:pk>/editar/', views.dono_update, name='dono_update'),
    path('donos/<int:pk>/excluir/', views.dono_delete, name='dono_delete'),
    
    # Pets
    path('pets/', views.pet_list, name='pet_list'),
    path('pets/novo/', views.pet_create, name='pet_create'),
    path('pets/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('pets/<int:pk>/historico/', views.pet_historico, name='pet_historico'),
    path('pets/<int:pk>/editar/', views.pet_update, name='pet_update'),
    path('pets/<int:pk>/excluir/', views.pet_delete, name='pet_delete'),
    
    # Consultas
    path('consultas/', views.consulta_list, name='consulta_list'),
    path('consultas/nova/', views.consulta_create, name='consulta_create'),
    path('consultas/<int:pk>/', views.consulta_detail, name='consulta_detail'),
    path('consultas/<int:pk>/editar/', views.consulta_update, name='consulta_update'),
    path('consultas/<int:pk>/excluir/', views.consulta_delete, name='consulta_delete'),
    path('consultas/<int:pk>/confirmar/', views.consulta_confirmar, name='consulta_confirmar'),
    path('consultas/<int:pk>/realizar/', views.consulta_realizar, name='consulta_realizar'),
    path('consultas/<int:pk>/cancelar/', views.consulta_cancelar, name='consulta_cancelar'),
    
    # Medicações
    path('medicacoes/', views.medicacao_list, name='medicacao_list'),
    path('medicacoes/nova/', views.medicacao_create, name='medicacao_create'),
    path('medicacoes/<int:pk>/', views.medicacao_detail, name='medicacao_detail'),
    path('medicacoes/<int:pk>/editar/', views.medicacao_update, name='medicacao_update'),
    path('medicacoes/<int:pk>/excluir/', views.medicacao_delete, name='medicacao_delete'),
    
    # Prescrições
    path('prescricoes/', views.prescricao_list, name='prescricao_list'),
    path('prescricoes/nova/', views.prescricao_create, name='prescricao_create'),
    path('prescricoes/<int:pk>/', views.prescricao_detail, name='prescricao_detail'),
    path('prescricoes/<int:pk>/editar/', views.prescricao_update, name='prescricao_update'),
    path('prescricoes/<int:pk>/excluir/', views.prescricao_delete, name='prescricao_delete'),
    
    # Agenda
    path('agenda/', views.agenda_list, name='agenda_list'),
    path('agenda/create/', views.agenda_create, name='agenda_create'),
    path('agenda/<int:pk>/', views.agenda_detail, name='agenda_detail'),
    path('agenda/<int:pk>/update/', views.agenda_update, name='agenda_update'),
    path('agenda/<int:pk>/delete/', views.agenda_delete, name='agenda_delete'),
    path('agenda/<int:pk>/confirmar/', views.agenda_confirmar, name='agenda_confirmar'),
    path('agenda/calendario/', views.agenda_calendario, name='agenda_calendario'),
    path('agenda/<int:pk>/concluir/', views.agenda_concluir, name='agenda_concluir'),
    path('consulta/<int:pk>/', views.consulta_detalhe, name='consulta_detalhe'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('sobre/', views.about, name='about'),
    path('termos/', views.terms, name='terms'),
    path('acessibilidade/', views.accessibility, name='accessibility'),
    path('contato/', views.contact, name='contact'),
]
