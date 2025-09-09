from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count, F, ExpressionWrapper, DurationField, DateTimeField
from django.db.models.functions import TruncDate, TruncHour, TruncMonth
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from .models import Dono, Pet, Consulta, Medicacao, Prescricao, Agenda
from .forms import DonoForm, PetForm, ConsultaForm, MedicacaoForm, PrescricaoForm, AgendaForm, ProfileForm, UserForm
from django.core.paginator import Paginator
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.conf import settings
from itertools import chain
from operator import attrgetter
from datetime import datetime, timedelta
import random
import json

# Importa o módulo de dicas de pets
from . import pet_tips

# Páginas principais
@login_required
def index(request):
    """Página inicial do sistema"""
    total_pets = Pet.objects.count()
    total_donos = Dono.objects.count()
    total_consultas = Consulta.objects.count()
    total_agendamentos = Agenda.objects.count()
    proximas_consultas = Consulta.objects.filter(
        data_hora__gte=timezone.now(),
        status__in=['AGENDADA', 'CONFIRMADA']
    ).order_by('data_hora')[:5]
    
    proximos_agendamentos = Agenda.objects.filter(
        data_hora__gte=timezone.now(),
        concluido=False
    ).order_by('data_hora')[:5]
    
    pets = Pet.objects.all().order_by('-id')[:3]
    donos = Dono.objects.all().order_by('-id')[:3]
    
    # Obtém uma dica de cuidado com pets
    pet_tip = pet_tips.get_random_pet_tip()
    
    context = {
        'total_pets': total_pets,
        'total_donos': total_donos,
        'total_consultas': total_consultas,
        'total_agendamentos': total_agendamentos,
        'proximas_consultas': proximas_consultas,
        'proximos_agendamentos': proximos_agendamentos,
        'pets': pets,
        'donos': donos,
        'pet_tip': pet_tip,
    }
    return render(request, 'core/index.html', context)

@login_required
@login_required
def dashboard(request):
    """Dashboard com estatísticas e informações gerais"""
    hoje = timezone.now().date()
    
    # Consultas do dia
    consultas_hoje = Consulta.objects.filter(
        data_hora__date=hoje
    ).order_by('data_hora')
    
    # Agendamentos do dia
    agendamentos_hoje = Agenda.objects.filter(
        data_hora__date=hoje,
        concluido=False
    ).order_by('data_hora')
    
    # Pets recentemente cadastrados
    pets_recentes = Pet.objects.all().order_by('-data_cadastro')[:5]
    
    context = {
        'consultas_hoje': consultas_hoje,
        'agendamentos_hoje': agendamentos_hoje,
        'pets_recentes': pets_recentes,
        'hoje': hoje,
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def dashboard_estatisticas(request):
    """Dashboard com gráficos e estatísticas"""
    # Dados para o gráfico de consultas por data
    ultimos_30_dias = timezone.now() - timedelta(days=30)
    consultas_por_data = (
        Consulta.objects
        .filter(data_hora__gte=ultimos_30_dias)
        .annotate(data=TruncDate('data_hora'))
        .values('data')
        .annotate(total=Count('id'))
        .order_by('data')
    )
    
    # Dados para o gráfico de consultas por veterinário
    consultas_por_veterinario = (
        Consulta.objects
        .values('veterinario')
        .annotate(total=Count('id'))
        .order_by('-total')
    )
    
    # Dados para o gráfico de horários de pico
    horarios_consulta = (
        Consulta.objects
        .annotate(hora=TruncHour('data_hora'))
        .values('hora')
        .annotate(total=Count('id'))
        .order_by('hora')
    )
    
    # Dados para o gráfico de tratamentos mais comuns
    tratamentos_mais_comuns = (
        Consulta.objects
        .exclude(tratamento__isnull=True)
        .exclude(tratamento__exact='')
        .values('tratamento')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]  # Top 10 tratamentos mais comuns
    )
    
    # Preparar dados para o template
    dados_graficos = {
        'consultas_por_data': list(consultas_por_data),
        'consultas_por_veterinario': list(consultas_por_veterinario),
        'horarios_consulta': list(horarios_consulta),
        'tratamentos_mais_comuns': list(tratamentos_mais_comuns),
    }
    
    # Se for uma requisição AJAX, retorna JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse(dados_graficos)
    
    # Se for uma requisição normal, renderiza o template
    return render(request, 'core/dashboard_estatisticas.html', {
        'dados_graficos': json.dumps(dados_graficos),
    })

# Views para Donos
@login_required
def dono_list(request):
    """Lista todos os donos cadastrados"""
    query = request.GET.get('q', '')
    if query:
        donos = Dono.objects.filter(
            Q(nome__icontains=query) | 
            Q(cpf__icontains=query) | 
            Q(email__icontains=query)
        ).order_by('nome')
    else:
        donos = Dono.objects.all().order_by('nome')
    
    # Paginação: 10 donos por página
    paginator = Paginator(donos, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'donos': page_obj,
        'query': query,
    }
    return render(request, 'core/dono/list.html', context)

@login_required
def dono_create(request):
    """Cadastra um novo dono"""
    if request.method == 'POST':
        form = DonoForm(request.POST)
        if form.is_valid():
            dono = form.save()
            messages.success(request, f'Dono {dono.nome} cadastrado com sucesso!')
            return redirect('core:dono_detail', pk=dono.pk)
    else:
        form = DonoForm()
    
    context = {
        'form': form,
        'title': 'Novo Dono',
    }
    return render(request, 'core/dono/form.html', context)

@login_required
def dono_detail(request, pk):
    """Exibe detalhes de um dono"""
    dono = get_object_or_404(Dono, pk=pk)
    pets = Pet.objects.filter(dono=dono).order_by('nome')
    
    context = {
        'dono': dono,
        'pets': pets,
    }
    return render(request, 'core/dono/detail.html', context)

@login_required
def dono_update(request, pk):
    """Atualiza dados de um dono"""
    dono = get_object_or_404(Dono, pk=pk)
    
    if request.method == 'POST':
        form = DonoForm(request.POST, instance=dono)
        if form.is_valid():
            dono = form.save()
            messages.success(request, f'Dados de {dono.nome} atualizados com sucesso!')
            return redirect('core:dono_detail', pk=dono.pk)
    else:
        form = DonoForm(instance=dono)
    
    context = {
        'form': form,
        'dono': dono,
        'title': f'Editar {dono.nome}',
    }
    return render(request, 'core/dono/form.html', context)

@login_required
def dono_delete(request, pk):
    """Remove um dono"""
    dono = get_object_or_404(Dono, pk=pk)
    
    if request.method == 'POST':
        nome = dono.nome
        dono.delete()
        messages.success(request, f'Dono {nome} removido com sucesso!')
        return redirect('core:dono_list')
    
    context = {
        'dono': dono,
    }
    return render(request, 'core/dono/delete.html', context)

# Views para Pets
@login_required
def pet_list(request):
    """Lista todos os pets"""
    search_query = request.GET.get('search', '')
    if search_query:
        pets = Pet.objects.filter(
            Q(nome__icontains=search_query) |
            Q(dono__nome__icontains=search_query) |
            Q(especie__icontains=search_query) |
            Q(raca__icontains=search_query)
        ).order_by('nome')
    else:
        pets = Pet.objects.all().order_by('nome')
    
    # Paginação
    paginator = Paginator(pets, 6)  # 6 pets por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'pets': page_obj,
        'search_query': search_query,
        'total_pets': pets.count(),
    }
    return render(request, 'core/pet/list.html', context)

@login_required
def pet_create(request):
    """Cadastra um novo pet"""
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f'Pet {pet.nome} cadastrado com sucesso!')
            return redirect('core:pet_detail', pk=pet.pk)
    else:
        form = PetForm()
    
    context = {
        'form': form,
        'title': 'Novo Pet',
    }
    return render(request, 'core/pet/form.html', context)

@login_required
def pet_detail(request, pk):
    """Exibe detalhes de um pet"""
    pet = get_object_or_404(Pet, pk=pk)
    consultas = Consulta.objects.filter(pet=pet).order_by('-data_hora')[:5]  # Mostra apenas as 5 mais recentes
    agendamentos = Agenda.objects.filter(pet=pet).order_by('-data_hora')[:5]  # Mostra apenas os 5 mais recentes
    
    context = {
        'pet': pet,
        'consultas': consultas,
        'agendamentos': agendamentos,
    }
    return render(request, 'core/pet/detail.html', context)

@login_required
def pet_historico(request, pk):
    """Exibe o histórico completo de consultas e agendamentos do pet"""
    pet = get_object_or_404(Pet, pk=pk)
    
    # Obtém todas as consultas e agendamentos ordenados por data (mais recente primeiro)
    consultas = Consulta.objects.filter(pet=pet).order_by('-data_hora')
    agendamentos = Agenda.objects.filter(pet=pet).order_by('-data_hora')
    
    # Combina as consultas e agendamentos em uma única lista ordenada por data
    historico = sorted(
        list(consultas) + list(agendamentos),
        key=lambda x: x.data_hora,
        reverse=True
    )
    
    context = {
        'pet': pet,
        'historico': historico,
    }
    return render(request, 'core/pet/historico.html', context)

@login_required
def pet_update(request, pk):
    """Atualiza dados de um pet"""
    pet = get_object_or_404(Pet, pk=pk)
    
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            pet = form.save()
            messages.success(request, f'Dados de {pet.nome} atualizados com sucesso!')
            return redirect('core:pet_detail', pk=pet.pk)
    else:
        form = PetForm(instance=pet)
    
    context = {
        'form': form,
        'pet': pet,
        'title': f'Editar {pet.nome}',
    }
    return render(request, 'core/pet/form.html', context)

@login_required
def pet_delete(request, pk):
    """Remove um pet"""
    pet = get_object_or_404(Pet, pk=pk)
    
    if request.method == 'POST':
        nome = pet.nome
        pet.delete()
        messages.success(request, f'Pet {nome} removido com sucesso!')
        return redirect('core:pet_list')
    
    context = {
        'pet': pet,
    }
    return render(request, 'core/pet/delete.html', context)

# Views para Consultas
@login_required
def consulta_list(request):
    """Lista todas as consultas e agendamentos confirmados"""
    status = request.GET.get('status', '')
    query = request.GET.get('q', '')
    
    # Busca consultas
    consultas = Consulta.objects.all()
    if status:
        consultas = consultas.filter(status=status)
    if query:
        consultas = consultas.filter(
            Q(pet__nome__icontains=query) | 
            Q(motivo__icontains=query) | 
            Q(diagnostico__icontains=query)
        )
    consultas = consultas.order_by('-data_hora')
    
    # Busca agendamentos confirmados
    agendamentos = Agenda.objects.filter(status='CONFIRMADO')
    if query:
        agendamentos = agendamentos.filter(
            Q(pet__nome__icontains=query) |
            Q(titulo__icontains=query) |
            Q(descricao__icontains=query)
        )
    agendamentos = agendamentos.order_by('-data_hora')
    
    # Combina os resultados
    from itertools import chain
    from operator import attrgetter
    resultados = sorted(
        chain(consultas, agendamentos),
        key=attrgetter('data_hora'),
        reverse=True
    )
    
    # Paginação
    paginator = Paginator(resultados, 6)  # 6 itens por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'status': status,
        'query': query,
    }
    return render(request, 'core/consulta/list.html', context)

@login_required
def consulta_create(request):
    """Cadastra uma nova consulta"""
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            consulta = form.save()
            messages.success(request, f'Consulta para {consulta.pet.nome} agendada com sucesso!')
            return redirect('core:consulta_detail', pk=consulta.pk)
    else:
        # Obtém o pet_id da query string para pré-preenchimento
        pet_id = request.GET.get('pet')
        initial = {}
        if pet_id and pet_id.isdigit():
            initial['pet'] = pet_id
        form = ConsultaForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Nova Consulta',
    }
    return render(request, 'core/consulta/form.html', context)

@login_required
def consulta_detail(request, pk):
    """Exibe detalhes de uma consulta"""
    consulta = get_object_or_404(Consulta, pk=pk)
    prescricoes = Prescricao.objects.filter(consulta=consulta)
    
    context = {
        'consulta': consulta,
        'prescricoes': prescricoes,
    }
    return render(request, 'core/consulta/detail.html', context)

@login_required
def consulta_update(request, pk):
    """Atualiza dados de uma consulta"""
    consulta = get_object_or_404(Consulta, pk=pk)
    
    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save()
            messages.success(request, f'Consulta de {consulta.pet.nome} atualizada com sucesso!')
            return redirect('core:consulta_detail', pk=consulta.pk)
    else:
        form = ConsultaForm(instance=consulta)
    
    context = {
        'form': form,
        'consulta': consulta,
        'title': f'Editar Consulta de {consulta.pet.nome}',
    }
    return render(request, 'core/consulta/form.html', context)

@login_required
def consulta_delete(request, pk):
    """Remove uma consulta"""
    consulta = get_object_or_404(Consulta, pk=pk)
    
    if request.method == 'POST':
        pet_nome = consulta.pet.nome
        consulta.delete()
        messages.success(request, f'Consulta de {pet_nome} removida com sucesso!')
        return redirect('core:consulta_list')
    
    context = {
        'consulta': consulta,
    }
    return render(request, 'core/consulta/delete.html', context)

@login_required
def consulta_confirmar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.status = 'CONFIRMADA'
        consulta.save()
        messages.success(request, 'Consulta confirmada com sucesso!')
        return redirect('core:consulta_detail', pk=consulta.pk)
    return redirect('core:consulta_detail', pk=consulta.pk)

@login_required
def consulta_realizar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.status = 'REALIZADA'
        consulta.save()
        messages.success(request, 'Consulta marcada como realizada!')
        return redirect('core:consulta_detail', pk=consulta.pk)
    return redirect('core:consulta_detail', pk=consulta.pk)

@login_required
def consulta_cancelar(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    if request.method == 'POST':
        consulta.status = 'CANCELADA'
        consulta.save()
        messages.success(request, 'Consulta cancelada com sucesso!')
        return redirect('core:consulta_detail', pk=consulta.pk)
    return redirect('core:consulta_detail', pk=consulta.pk)

# Views para Medicações
@login_required
def medicacao_list(request):
    """Lista todas as medicações"""
    query = request.GET.get('q', '')
    if query:
        medicacoes = Medicacao.objects.filter(
            Q(nome__icontains=query) | 
            Q(descricao__icontains=query)
        ).order_by('nome')
    else:
        medicacoes = Medicacao.objects.all().order_by('nome')
    
    # Paginação
    paginator = Paginator(medicacoes, 6)  # 6 medicações por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'core/medicacao/list.html', context)

@login_required
def medicacao_create(request):
    """Cadastra uma nova medicação"""
    if request.method == 'POST':
        form = MedicacaoForm(request.POST)
        if form.is_valid():
            medicacao = form.save()
            messages.success(request, f'Medicação {medicacao.nome} cadastrada com sucesso!')
            return redirect('core:medicacao_detail', pk=medicacao.pk)
    else:
        form = MedicacaoForm()
    
    context = {
        'form': form,
        'title': 'Nova Medicação',
    }
    return render(request, 'core/medicacao/form.html', context)

@login_required
def medicacao_detail(request, pk):
    """Exibe detalhes de uma medicação"""
    medicacao = get_object_or_404(Medicacao, pk=pk)
    prescricoes = Prescricao.objects.filter(medicacao=medicacao).order_by('-data_inicio')
    
    context = {
        'medicacao': medicacao,
        'prescricoes': prescricoes,
    }
    return render(request, 'core/medicacao/detail.html', context)

@login_required
def medicacao_update(request, pk):
    """Atualiza dados de uma medicação"""
    medicacao = get_object_or_404(Medicacao, pk=pk)
    
    if request.method == 'POST':
        form = MedicacaoForm(request.POST, instance=medicacao)
        if form.is_valid():
            medicacao = form.save()
            messages.success(request, f'Medicação {medicacao.nome} atualizada com sucesso!')
            return redirect('core:medicacao_detail', pk=medicacao.pk)
    else:
        form = MedicacaoForm(instance=medicacao)
    
    context = {
        'form': form,
        'medicacao': medicacao,
        'title': f'Editar {medicacao.nome}',
    }
    return render(request, 'core/medicacao/form.html', context)

@login_required
def medicacao_delete(request, pk):
    """Remove uma medicação"""
    medicacao = get_object_or_404(Medicacao, pk=pk)
    
    if request.method == 'POST':
        nome = medicacao.nome
        medicacao.delete()
        messages.success(request, f'Medicação {nome} removida com sucesso!')
        return redirect('core:medicacao_list')
    
    context = {
        'medicacao': medicacao,
    }
    return render(request, 'core/medicacao/delete.html', context)

# Views para Agenda
@login_required
def agenda_list(request):
    """Lista todos os agendamentos"""
    tipo = request.GET.get('tipo', '')
    concluido = request.GET.get('concluido', '')
    query = request.GET.get('q', '')
    
    agendamentos = Agenda.objects.all()
    
    if tipo:
        agendamentos = agendamentos.filter(tipo=tipo)
    
    if concluido:
        concluido_bool = concluido == 'sim'
        agendamentos = agendamentos.filter(concluido=concluido_bool)
    
    if query:
        agendamentos = agendamentos.filter(
            Q(titulo__icontains=query) | 
            Q(pet__nome__icontains=query) | 
            Q(descricao__icontains=query)
        )
    
    agendamentos = agendamentos.order_by('-data_hora')
    
    # Paginação
    paginator = Paginator(agendamentos, 6)  # 6 agendamentos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'tipo': tipo,
        'concluido': concluido,
        'query': query,
    }
    return render(request, 'core/agenda/list.html', context)

@login_required
def agenda_create(request):
    """Cadastra um novo agendamento"""
    if request.method == 'POST':
        form = AgendaForm(request.POST)
        if form.is_valid():
            agenda = form.save()
            messages.success(request, f'Agendamento "{agenda.titulo}" para {agenda.pet.nome} criado com sucesso!')
            return redirect('core:agenda_detail', pk=agenda.pk)
    else:
        # Obtém o pet_id da query string para pré-preenchimento
        pet_id = request.GET.get('pet')
        initial = {}
        if pet_id and pet_id.isdigit():
            initial['pet'] = pet_id
        form = AgendaForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Novo Agendamento',
    }
    return render(request, 'core/agenda/form.html', context)

@login_required
def agenda_detail(request, pk):
    """Exibe detalhes de um agendamento"""
    agenda = get_object_or_404(Agenda, pk=pk)
    
    context = {
        'agenda': agenda,
    }
    return render(request, 'core/agenda/detail.html', context)

@login_required
def agenda_update(request, pk):
    """Atualiza dados de um agendamento"""
    agenda = get_object_or_404(Agenda, pk=pk)
    
    if request.method == 'POST':
        form = AgendaForm(request.POST, instance=agenda)
        if form.is_valid():
            agenda = form.save()
            messages.success(request, f'Agendamento "{agenda.titulo}" atualizado com sucesso!')
            return redirect('core:agenda_detail', pk=agenda.pk)
    else:
        form = AgendaForm(instance=agenda)
    
    context = {
        'form': form,
        'agenda': agenda,
        'title': f'Editar Agendamento',
    }
    return render(request, 'core/agenda/form.html', context)

@login_required
def agenda_delete(request, pk):
    """Remove um agendamento"""
    agenda = get_object_or_404(Agenda, pk=pk)
    
    if request.method == 'POST':
        titulo = agenda.titulo
        pet_nome = agenda.pet.nome
        agenda.delete()
        messages.success(request, f'Agendamento "{titulo}" para {pet_nome} removido com sucesso!')
        return redirect('core:agenda_list')
    
    context = {
        'agenda': agenda,
    }
    return render(request, 'core/agenda/delete.html', context)

@login_required
def agenda_calendario(request):
    """Exibe calendário com todos os agendamentos"""
    agendamentos = Agenda.objects.all().order_by('data_hora')
    consultas = Consulta.objects.all().order_by('data_hora')
    
    context = {
        'agendamentos': agendamentos,
        'consultas': consultas,
    }
    return render(request, 'core/agenda/calendario.html', context)

@login_required
def agenda_detalhe(request, pk):
    agendamento = get_object_or_404(Agenda, pk=pk)
    return render(request, 'core/agenda/detalhe.html', {
        'agendamento': agendamento
    })

@login_required
def consulta_detalhe(request, pk):
    consulta = get_object_or_404(Consulta, pk=pk)
    return render(request, 'core/consulta/detalhe.html', {
        'consulta': consulta
    })

@login_required
def agenda_concluir(request, pk):
    """Marca um agendamento como concluído e redireciona para a tela de consulta"""
    agenda = get_object_or_404(Agenda, pk=pk)
    
    if request.method == 'POST':
        agenda.concluido = True
        agenda.save()
        messages.success(request, f'Agendamento "{agenda.titulo}" marcado como concluído!')
        
        # Cria uma nova consulta a partir do agendamento
        consulta = Consulta(
            pet=agenda.pet,
            data_hora=agenda.data_hora,
            motivo=f'Consulta gerada a partir do agendamento: {agenda.titulo}',
            status='REALIZADA',
            observacoes=agenda.descricao if agenda.descricao else 'Nenhuma observação fornecida.'
        )
        consulta.save()
        
        # Redireciona para a tela de detalhes da consulta criada
        return redirect('core:consulta_detail', pk=consulta.pk)
    
    return redirect('core:agenda_detail', pk=agenda.pk)

@login_required
def agenda_confirmar(request, pk):
    """Confirma um agendamento"""
    agenda = get_object_or_404(Agenda, pk=pk)
    
    if request.method == 'POST':
        agenda.status = 'CONFIRMADO'
        agenda.save()
        messages.success(request, f'Agendamento "{agenda.titulo}" confirmado com sucesso!')
        return redirect('core:agenda_detail', pk=agenda.pk)
    
    return redirect('core:agenda_detail', pk=agenda.pk)

# Views para Prescrições
@login_required
def prescricao_list(request):
    prescricoes = Prescricao.objects.all().order_by('-data_prescricao')
    context = {
        'prescricoes': prescricoes,
    }
    return render(request, 'core/prescricao/list.html', context)

@login_required
def prescricao_create(request):
    """Cadastra uma nova prescrição"""
    if request.method == 'POST':
        form = PrescricaoForm(request.POST)
        if form.is_valid():
            prescricao = form.save()
            messages.success(request, 'Prescrição criada com sucesso!')
            return redirect('core:prescricao_detail', pk=prescricao.pk)
    else:
        # Obtém os valores iniciais da query string
        medicacao_id = request.GET.get('medicacao')
        pet_id = request.GET.get('pet')
        
        # Verifica se os IDs são válidos
        initial = {}
        if medicacao_id and medicacao_id.isdigit():
            initial['medicacao'] = medicacao_id
        if pet_id and pet_id.isdigit():
            initial['pet'] = pet_id
            
        form = PrescricaoForm(initial=initial)
    
    context = {
        'form': form,
        'title': 'Nova Prescrição',
    }
    return render(request, 'core/prescricao/form.html', context)

@login_required
def prescricao_detail(request, pk):
    prescricao = get_object_or_404(Prescricao, pk=pk)
    context = {
        'prescricao': prescricao,
    }
    return render(request, 'core/prescricao/detail.html', context)

@login_required
def prescricao_update(request, pk):
    prescricao = get_object_or_404(Prescricao, pk=pk)
    if request.method == 'POST':
        form = PrescricaoForm(request.POST, instance=prescricao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Prescrição atualizada com sucesso!')
            return redirect('core:prescricao_detail', pk=prescricao.pk)
    else:
        form = PrescricaoForm(instance=prescricao)
    
    context = {
        'form': form,
        'prescricao': prescricao,
    }
    return render(request, 'core/prescricao/form.html', context)

@login_required
def prescricao_delete(request, pk):
    prescricao = get_object_or_404(Prescricao, pk=pk)
    if request.method == 'POST':
        prescricao.delete()
        messages.success(request, 'Prescrição excluída com sucesso!')
        return redirect('core:prescricao_list')
    
    context = {
        'prescricao': prescricao,
    }
    return render(request, 'core/prescricao/delete.html', context)

class IndexView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pets'] = Pet.objects.count()
        context['total_donos'] = Dono.objects.count()
        context['total_consultas'] = Consulta.objects.count()
        context['total_agendamentos'] = Agenda.objects.count()
        context['proximas_consultas'] = Consulta.objects.filter(
            data_hora__gte=timezone.now()
        ).order_by('data_hora')[:5]
        context['proximos_agendamentos'] = Agenda.objects.filter(
            data_hora__gte=timezone.now()
        ).order_by('data_hora')[:5]
        context['pets'] = Pet.objects.all().order_by('-id')[:3]
        context['donos'] = Dono.objects.all().order_by('-id')[:3]
        return context

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('core:profile_edit')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'core/profile/edit.html', context)

def about(request):
    """Página Sobre o sistema"""
    return render(request, 'core/about.html')

def terms(request):
    """Página de Termos de Uso"""
    return render(request, 'core/terms.html')

def accessibility(request):
    """Página de Acessibilidade"""
    return render(request, 'core/accessibility.html')

def contact(request):
    """Página de Contato"""
    if request.method == 'POST':
        # Aqui você pode adicionar a lógica para processar o formulário
        # Por exemplo, enviar um email, salvar no banco de dados, etc.
        messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
        return redirect('core:contact')
    return render(request, 'core/contact.html')

def login_with_captcha(request):
    """
    View personalizada para login com validação de captcha
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        captcha_answer = request.POST.get('captcha_answer')
        captcha_id = request.POST.get('captcha_id')
        
        # Validar captcha
        if not validate_captcha(request, captcha_id, captcha_answer):
            messages.error(request, 'Resposta do captcha incorreta. Tente novamente.')
            return render(request, 'registration/login.html', {
                'username': username,
                'captcha_error': True
            })
        
        # Autenticar usuário
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url and next_url.strip():
                return redirect(next_url)
            else:
                return redirect('core:index')
        else:
            messages.error(request, 'Usuário ou senha incorretos.')
            return render(request, 'registration/login.html', {
                'username': username,
                'captcha_error': True
            })
    
    return render(request, 'registration/login.html')

def validate_captcha(request, captcha_id, user_answer):
    """
    Valida a resposta do captcha de imagem
    """
    if not captcha_id or not user_answer:
        return False
    
    # Recuperar a resposta correta da sessão
    correct_answer = request.session.get(f'captcha_{captcha_id}')
    if not correct_answer:
        return False
    
    # Limpar o captcha da sessão após validação
    if f'captcha_{captcha_id}' in request.session:
        del request.session[f'captcha_{captcha_id}']
    
    # Normalizar respostas (remover espaços, converter para maiúsculas)
    user_answer_clean = user_answer.strip().upper()
    correct_answer_clean = correct_answer.strip().upper()
    
    # Comparar respostas
    return user_answer_clean == correct_answer_clean

def generate_captcha(request):
    """
    Gera um novo captcha de imagem com caracteres distorcidos
    """
    from PIL import Image, ImageDraw, ImageFont
    import string
    import io
    import base64
    
    # Gerar texto aleatório (6 caracteres)
    characters = string.ascii_uppercase + string.digits
    captcha_text = ''.join(random.choice(characters) for _ in range(6))
    
    # Gerar ID único para o captcha
    captcha_id = f"captcha_{random.randint(1000, 9999)}"
    
    # Criar imagem do captcha
    width, height = 200, 80
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Adicionar ruído (pontos)
    for _ in range(1000):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill='black')
    
    # Adicionar linhas distorcidas
    for _ in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line([(x1, y1), (x2, y2)], fill='black', width=2)
    
    # Adicionar texto distorcido
    try:
        # Tentar usar uma fonte do sistema
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    except:
        # Fallback para fonte padrão
        font = ImageFont.load_default()
    
    # Calcular posição do texto
    bbox = draw.textbbox((0, 0), captcha_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Desenhar texto com distorção
    for i, char in enumerate(captcha_text):
        char_x = x + i * (text_width // len(captcha_text))
        char_y = y + random.randint(-5, 5)
        draw.text((char_x, char_y), char, fill='black', font=font)
    
    # Converter para base64
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    
    # Armazenar resposta na sessão
    request.session[f'captcha_{captcha_id}'] = captcha_text
    
    return JsonResponse({
        'captcha_id': captcha_id,
        'image': f"data:image/png;base64,{img_str}",
        'text': captcha_text  # Em produção, não enviar o texto
    })
    return JsonResponse({
        'captcha_id': captcha_id,
        'image': f"data:image/png;base64,{img_str}",
        'text': captcha_text  # Em produção, não enviar o texto
    })
