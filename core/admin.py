from django.contrib import admin
from .models import Dono, Pet, Consulta, Medicacao, Prescricao, Agenda

@admin.register(Dono)
class DonoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cpf', 'telefone', 'email', 'data_cadastro')
    search_fields = ('nome', 'cpf', 'email')
    list_filter = ('data_cadastro',)

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dono', 'especie', 'raca', 'sexo', 'data_nascimento', 'peso')
    list_filter = ('especie', 'sexo')
    search_fields = ('nome', 'dono__nome', 'raca')
    autocomplete_fields = ('dono',)

@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('pet', 'veterinario', 'data_hora', 'motivo', 'status')
    list_filter = ('status', 'veterinario', 'data_hora')
    search_fields = ('pet__nome', 'veterinario', 'motivo', 'diagnostico')
    autocomplete_fields = ('pet',)

@admin.register(Medicacao)
class MedicacaoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)

@admin.register(Prescricao)
class PrescricaoAdmin(admin.ModelAdmin):
    list_display = ('medicacao', 'consulta', 'dosagem', 'frequencia', 'data_inicio', 'data_fim')
    list_filter = ('frequencia', 'data_inicio')
    search_fields = ('medicacao__nome', 'consulta__pet__nome')
    autocomplete_fields = ('consulta', 'medicacao')

@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'pet', 'veterinario', 'tipo', 'data_hora', 'concluido')
    list_filter = ('tipo', 'veterinario', 'concluido', 'data_hora')
    search_fields = ('titulo', 'pet__nome', 'veterinario', 'descricao')
    autocomplete_fields = ('pet',)
