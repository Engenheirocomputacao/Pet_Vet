from django.shortcuts import render
from django.db.models import Count, Avg, Sum, Q, F
from django.db.models.functions import TruncMonth, TruncYear, ExtractYear
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Dono, Pet, Consulta, Agenda, Prescricao, Medicacao

def dashboard_home(request):
    """Dashboard principal com visão geral"""
    context = get_dashboard_data()
    return render(request, 'dashboard/dashboard_home.html', context)

@csrf_exempt
def dashboard_api(request):
    """API para dados do dashboard (AJAX)"""
    try:
        data_type = request.GET.get('type', 'overview')
        
        if data_type == 'overview':
            data = get_overview_data()
        elif data_type == 'consultas_periodo':
            days = int(request.GET.get('days', 7))
            data = get_consultas_periodo_data(days)
        elif data_type == 'especies_racas':
            data = get_especies_racas_data()
        elif data_type == 'veterinarios_performance':
            data = get_veterinarios_performance_data()
        elif data_type == 'procedimentos_tipos':
            data = get_procedimentos_tipos_data()
        elif data_type == 'clientes_fidelizacao':
            data = get_clientes_fidelizacao_data()
        elif data_type == 'saude_animal':
            data = get_saude_animal_data()
        # Novos endpoints financeiros
        elif data_type == 'procedimentos_financeiro':
            data = get_procedimentos_financeiro_data()
        elif data_type == 'veterinarios_financeiro':
            data = get_veterinarios_financeiro_data()
        elif data_type == 'clientes_valor':
            data = get_clientes_valor_data()
        elif data_type == 'tendencias_financeiro':
            data = get_tendencias_financeiro_data()
        else:
            data = {'error': 'Tipo de dados não reconhecido'}
        
        return JsonResponse(data)
    except Exception as e:
        # Retornar erro em formato JSON
        return JsonResponse({
            'error': f'Erro interno da API: {str(e)}',
            'type': data_type if 'data_type' in locals() else 'unknown'
        }, status=500)

def dashboard_financeiro(request):
    """Dashboard financeiro da clínica"""
    return render(request, 'dashboard/dashboard_financeiro.html')

def dashboard_saude(request):
    """Dashboard de saúde animal"""
    return render(request, 'dashboard/dashboard_saude.html')

def dashboard_debug(request):
    """Dashboard de debug para testar APIs"""
    context = get_dashboard_data()
    return render(request, 'dashboard/dashboard_debug.html', context)

def dashboard_simple(request):
    """Dashboard simples para teste"""
    context = get_dashboard_data()
    return render(request, 'dashboard/dashboard_simple.html', context)

def get_dashboard_data():
    """Dados principais para o dashboard"""
    hoje = timezone.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    inicio_ano = hoje.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Métricas gerais
    total_donos = Dono.objects.count()
    total_pets = Pet.objects.count()
    total_consultas = Consulta.objects.count()
    consultas_mes = Consulta.objects.filter(data_hora__gte=inicio_mes).count()
    consultas_ano = Consulta.objects.filter(data_hora__gte=inicio_ano).count()
    
    # Consultas por status
    consultas_agendadas = Consulta.objects.filter(status='AGENDADA').count()
    consultas_realizadas = Consulta.objects.filter(status='REALIZADA').count()
    consultas_canceladas = Consulta.objects.filter(status='CANCELADA').count()
    
    # Distribuição por espécie
    especies_count = Pet.objects.values('especie').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Veterinários mais ativos
    veterinarios_count = Consulta.objects.values('veterinario').annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    # Agendamentos pendentes
    agendamentos_pendentes = Agenda.objects.filter(
        status='PENDENTE',
        data_hora__gte=hoje
    ).count()
    
    # Pets por dono
    pets_por_dono = Dono.objects.annotate(
        total_pets=Count('pets')
    ).order_by('-total_pets')[:5]
    
    context = {
        'total_donos': total_donos,
        'total_pets': total_pets,
        'total_consultas': total_consultas,
        'consultas_mes': consultas_mes,
        'consultas_ano': consultas_ano,
        'consultas_agendadas': consultas_agendadas,
        'consultas_realizadas': consultas_realizadas,
        'consultas_canceladas': consultas_canceladas,
        'especies_count': especies_count,
        'veterinarios_count': veterinarios_count,
        'agendamentos_pendentes': agendamentos_pendentes,
        'pets_por_dono': pets_por_dono,
    }
    
    return context

def get_overview_data():
    """Dados para visão geral"""
    hoje = timezone.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Crescimento mensal
    meses = []
    consultas_mensais = []
    
    for i in range(6):
        data = inicio_mes - timedelta(days=30*i)
        mes = data.strftime('%b/%Y')
        consultas = Consulta.objects.filter(
            data_hora__year=data.year,
            data_hora__month=data.month
        ).count()
        
        meses.append(mes)
        consultas_mensais.append(consultas)
    
    return {
        'meses': meses[::-1],
        'consultas_mensais': consultas_mensais[::-1]
    }

def get_consultas_periodo_data(days=7):
    """Dados de consultas por período
    
    Args:
        days (int): Número de dias para o período (7, 15, 30, 90, 180, 365)
    """
    hoje = timezone.now()
    
    # Definir o formato da data baseado no período
    if days <= 30:  # Até 30 dias: mostrar por dia
        date_format = '%d/%m'
        step = 1
    elif days <= 90:  # Até 3 meses: mostrar por semana
        date_format = '%d/%m'
        step = 7
    elif days <= 180:  # Até 6 meses: mostrar por 2 semanas
        date_format = '%b'
        step = 14
    else:  # Mais de 6 meses: mostrar por mês
        date_format = '%b/%y'
        step = 30
    
    consultas_periodo = []
    datas_periodo = []
    
    # Ajustar para o início do dia
    hoje = hoje.replace(hour=0, minute=0, second=0, microsecond=0)
    
    for i in range(0, days + 1, step):
        data_fim = hoje - timedelta(days=i)
        data_inicio = data_fim - timedelta(days=step-1) if i + step <= days else hoje - timedelta(days=days)
        
        consultas = Consulta.objects.filter(
            data_hora__date__range=(data_inicio.date(), data_fim.date())
        ).count()
        
        # Se for o último período (mais antigo), ajustar o rótulo
        if i + step > days:
            label = f"{data_inicio.strftime(date_format)} - {data_fim.strftime(date_format)}"
        else:
            label = data_fim.strftime(date_format)
        
        consultas_periodo.append(consultas)
        datas_periodo.append(label)
    
    # Inverter as listas para mostrar do mais antigo para o mais recente
    return {
        'consultas_periodo': consultas_periodo[::-1],
        'datas_periodo': datas_periodo[::-1],
        'total_dias': days
    }

def get_especies_racas_data():
    """Dados de distribuição por espécie e raça"""
    especies = Pet.objects.values('especie').annotate(
        total=Count('id')
    ).order_by('-total')
    
    racas = Pet.objects.values('raca').annotate(
        total=Count('id')
    ).filter(raca__isnull=False).exclude(raca='').order_by('-total')[:10]
    
    return {
        'especies': list(especies),
        'racas': list(racas)
    }

def get_veterinarios_performance_data():
    """Dados de performance dos veterinários"""
    veterinarios = Consulta.objects.values('veterinario').annotate(
        total_consultas=Count('id'),
        consultas_realizadas=Count('id', filter=Q(status='REALIZADA')),
        consultas_agendadas=Count('id', filter=Q(status='AGENDADA'))
    ).order_by('-total_consultas')
    
    # Calcular taxa de realização
    for vet in veterinarios:
        if vet['total_consultas'] > 0:
            vet['taxa_realizacao'] = round(
                (vet['consultas_realizadas'] / vet['total_consultas']) * 100, 1
            )
        else:
            vet['taxa_realizacao'] = 0
    
    return {
        'veterinarios': list(veterinarios)
    }

def get_procedimentos_tipos_data():
    """Dados de tipos de procedimentos"""
    tipos_agenda = Agenda.objects.values('tipo').annotate(
        total=Count('id')
    ).order_by('-total')
    
    # Status dos agendamentos
    status_agenda = Agenda.objects.values('status').annotate(
        total=Count('id')
    ).order_by('-total')
    
    return {
        'tipos': list(tipos_agenda),
        'status': list(status_agenda)
    }

def get_procedimentos_financeiro_data():
    """Retorna dados financeiros por tipo de procedimento (proxy por preço fixo)."""
    print("\n=== INÍCIO get_procedimentos_financeiro_data() ===")
    
    # Preços médios por tipo (R$)
    precos = {
        'CONSULTA': 80,
        'VACINA': 100,
        'EXAME': 150,
        'MEDICACAO': 60,
        'OUTRO': 120,
    }
    tipos_legenda = {
        'CONSULTA': 'Consulta',
        'VACINA': 'Vacinação',
        'EXAME': 'Exame',
        'MEDICACAO': 'Medicação',
        'OUTRO': 'Outro',
    }
    
    print("Buscando todos os agendamentos, independentemente da data...")
    
    # Consulta para obter a contagem de agendamentos por tipo (sem filtrar por data)
    agg = (Agenda.objects
           .values('tipo')
           .annotate(qtd=Count('id'))
           .order_by('-qtd'))
    
    print(f"Total de registros encontrados: {agg.count()}")
    
    labels = []
    faturamentos = []
    quantidades = []
    tabela = []
    
    # Se não houver dados, retornar dados vazios para evitar erros
    if not agg.exists():
        print("Nenhum agendamento encontrado no mês atual.")
        # Adicionar valores zerados para todos os tipos
        for tipo, legenda in tipos_legenda.items():
            labels.append(legenda)
            quantidades.append(0)
            faturamentos.append(0)
            tabela.append({
                'procedimento': legenda,
                'quantidade': 0,
                'faturamento': 0,
                'ticket_medio': 0,
            })
    else:
        # Processar os dados encontrados
        for item in agg:
            tipo = item['tipo']
            qtd = item['qtd'] or 0
            preco = precos.get(tipo, 0)
            faturamento = qtd * preco
            
            print(f"Tipo: {tipo}, Quantidade: {qtd}, Preço: {preco}, Faturamento: {faturamento}")
            
            labels.append(tipos_legenda.get(tipo, tipo))
            quantidades.append(qtd)
            faturamentos.append(faturamento)
            ticket = round((faturamento / qtd), 2) if qtd > 0 else 0
            
            tabela.append({
                'procedimento': tipos_legenda.get(tipo, tipo),
                'quantidade': qtd,
                'faturamento': faturamento,
                'ticket_medio': ticket,
            })
    
    print(f"Labels: {labels}")
    print(f"Faturamentos: {faturamentos}")
    print(f"Quantidades: {quantidades}")
    print("=== FIM get_procedimentos_financeiro_data() ===\n")
    
    return {
        'labels': labels,
        'faturamentos': faturamentos,
        'quantidades': quantidades,
        'tabela': tabela,
    }

def get_veterinarios_financeiro_data():
    """Faturamento por veterinário (proxy: consultas REALIZADAS x preço médio)."""
    print("\n=== INÍCIO get_veterinarios_financeiro_data() ===")
    
    preco_consulta = 150  # Aumentando o valor para um valor mais realista
    
    # Consulta para obter a contagem de consultas realizadas por veterinário
    agg = (Consulta.objects
           .filter(status='REALIZADA')
           .values('veterinario')
           .annotate(qtd=Count('id'))
           .order_by('-qtd'))
    
    print(f"Total de veterinários com consultas realizadas: {agg.count()}")
    
    # Se não houver dados, retornar dados vazios para evitar erros
    if not agg.exists():
        print("Nenhuma consulta realizada encontrada.")
        return {
            'labels': [],
            'faturamentos': [],
        }
    
    # Processar os dados encontrados
    labels = []
    faturamentos = []
    
    for item in agg:
        vet = item['veterinario']
        qtd = item['qtd'] or 0
        faturamento = qtd * preco_consulta
        
        print(f"Veterinário: {vet}, Consultas: {qtd}, Faturamento: {faturamento}")
        
        labels.append(vet)
        faturamentos.append(faturamento)
    
    print(f"Labels: {labels}")
    print(f"Faturamentos: {faturamentos}")
    print("=== FIM get_veterinarios_financeiro_data() ===\n")
    
    return {
        'labels': labels,
        'faturamentos': faturamentos,
    }

def get_clientes_valor_data():
    """Distribuição de clientes por valor (proxy por frequência de consultas)."""
    print("\n=== INÍCIO get_clientes_valor_data() ===")
    
    # Obter todos os donos
    donos = Dono.objects.all()
    print(f"Total de donos: {donos.count()}")
    
    alto = medio = baixo = 0
    
    for i, d in enumerate(donos, 1):
        # Contar o total de consultas de todos os pets do dono
        total_consultas = d.pets.aggregate(total=Count('consultas'))['total'] or 0
        
        # Classificar o cliente com base no total de consultas
        if total_consultas >= 5:
            categoria = 'Alto Valor'
            alto += 1
        elif total_consultas >= 2:
            categoria = 'Médio Valor'
            medio += 1
        else:
            categoria = 'Baixo Valor'
            baixo += 1
        
        print(f"Dono {i}: {d.nome}, Consultas: {total_consultas}, Categoria: {categoria}")
    
    print(f"\nResumo:")
    print(f"- Alto Valor: {alto} clientes")
    print(f"- Médio Valor: {medio} clientes")
    print(f"- Baixo Valor: {baixo} clientes")
    print("=== FIM get_clientes_valor_data() ===\n")
    
    return {
        'labels': ['Alto Valor', 'Médio Valor', 'Baixo Valor'],
        'values': [alto, medio, baixo],
    }

def get_tendencias_financeiro_data():
    """Tendência mensal de faturamento (proxy: consultas REALIZADAS x preço médio por mês do ano atual)."""
    print("\n=== INÍCIO get_tendencias_financeiro_data() ===")
    
    preco_consulta = 150  # Aumentando o valor para um valor mais realista
    hoje = timezone.now()
    ano = hoje.year
    
    print(f"Ano de referência: {ano}")
    
    # Nomes dos meses em português
    meses_nomes = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
    
    # Inicializar lista de valores com zeros
    valores = [0] * 12
    
    # Obter contagem de consultas por mês
    from django.db.models.functions import ExtractMonth
    
    # Consulta para obter o número de consultas realizadas por mês no ano atual
    consultas_por_mes = (Consulta.objects
                         .filter(status='REALIZADA', data_hora__year=ano)
                         .annotate(mes=ExtractMonth('data_hora'))
                         .values('mes')
                         .annotate(total=Count('id'))
                         .order_by('mes'))
    
    print(f"Consultas por mês: {list(consultas_por_mes)}")
    
    # Preencher os valores com base nos dados reais
    for item in consultas_por_mes:
        mes = item['mes'] - 1  # Ajustar para índice baseado em 0
        if 0 <= mes < 12:  # Garantir que o mês esteja no intervalo válido
            valores[mes] = item['total'] * preco_consulta
    
    print(f"Valores de faturamento por mês: {valores}")
    print("=== FIM get_tendencias_financeiro_data() ===\n")
    
    return {
        'labels': meses_nomes,
        'valores': valores,
    }

def get_clientes_fidelizacao_data():
    """Dados de fidelização de clientes"""
    try:
        # Donos com múltiplos pets
        donos_multiplos_pets = Dono.objects.annotate(
            total_pets=Count('pets')
        ).filter(total_pets__gt=1).order_by('-total_pets')[:10]
        
        # Donos com mais consultas - usar subquery para calcular corretamente
        from django.db.models import Subquery, OuterRef
        
        # Primeiro, vamos pegar os donos com mais consultas
        donos_consultas_raw = Dono.objects.annotate(
            total_consultas=Count('pets__consultas')
        ).filter(total_consultas__gt=0).order_by('-total_consultas')[:10]
        
        # Agora vamos criar uma lista com os dados corretos
        donos_consultas = []
        for dono in donos_consultas_raw:
            total_pets = dono.pets.count()
            total_consultas = dono.pets.aggregate(
                total=Count('consultas')
            )['total'] or 0
            
            donos_consultas.append({
                'id': dono.id,
                'nome': dono.nome,
                'total_consultas': total_consultas,
                'total_pets': total_pets
            })
        
        # Ordenar por total de consultas
        donos_consultas.sort(key=lambda x: x['total_consultas'], reverse=True)
        
        # Taxa de retorno (clientes com + de 1 consulta)
        total_donos_consultas = Dono.objects.filter(pets__consultas__isnull=False).distinct().count()
        donos_retorno = Dono.objects.annotate(
            total_consultas=Count('pets__consultas')
        ).filter(total_consultas__gt=1).distinct().count()
        
        taxa_retorno = 0
        if total_donos_consultas > 0:
            taxa_retorno = round((donos_retorno / total_donos_consultas) * 100, 1)
        
        return {
            'donos_multiplos_pets': [
                {
                    'id': dono.id,
                    'nome': dono.nome,
                    'total_pets': dono.total_pets
                } for dono in donos_multiplos_pets
            ],
            'donos_consultas': donos_consultas,  # Já está no formato correto
            'taxa_retorno': taxa_retorno,
            'total_donos_consultas': total_donos_consultas,
            'donos_retorno': donos_retorno
        }
    except Exception as e:
        # Retornar erro em formato JSON
        return {
            'error': f'Erro ao processar dados de clientes: {str(e)}',
            'donos_multiplos_pets': [],
            'donos_consultas': [],
            'taxa_retorno': 0,
            'total_donos_consultas': 0,
            'donos_retorno': 0
        }

def get_saude_animal_data():
    """Dados de saúde animal"""
    # Distribuição por idade
    pets_idade = []
    for i in range(5):
        idade_min = i * 2
        idade_max = (i + 1) * 2
        if i == 4:  # Último grupo: 8+ anos
            count = Pet.objects.filter(
                data_nascimento__lte=timezone.now().date() - timedelta(days=365*idade_min)
            ).count()
        else:
            count = Pet.objects.filter(
                data_nascimento__lte=timezone.now().date() - timedelta(days=365*idade_min),
                data_nascimento__gt=timezone.now().date() - timedelta(days=365*idade_max)
            ).count()
        
        pets_idade.append({
            'faixa': f'{idade_min}-{idade_max if i < 4 else "+"} anos',
            'total': count
        })
    
    # Distribuição por peso (para cães e gatos)
    pets_peso = []
    especies_peso = ['CACHORRO', 'GATO']
    
    for especie in especies_peso:
        pets = Pet.objects.filter(especie=especie, peso__isnull=False)
        if pets.exists():
            peso_medio = pets.aggregate(Avg('peso'))['peso__avg']
            pets_peso.append({
                'especie': especie,
                'peso_medio': round(peso_medio, 1)
            })
    
    # Consultas por motivo
    motivos_consultas = Consulta.objects.values('motivo').annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    return {
        'pets_idade': pets_idade,
        'pets_peso': pets_peso,
        'motivos_consultas': list(motivos_consultas)
    }
