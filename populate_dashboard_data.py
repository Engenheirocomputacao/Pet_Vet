#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_vet_project.settings')
django.setup()

# Importar modelos após configuração do Django
from core.models import Dono, Pet, Consulta, Agenda, Medicacao, Prescricao

def criar_consultas_recentes():
    """Cria consultas dos últimos 7 dias para o dashboard"""
    hoje = timezone.now()
    pets = Pet.objects.all()
    
    if not pets.exists():
        print("Nenhum pet encontrado. Crie pets primeiro.")
        return
    
    # Criar consultas para os últimos 7 dias
    for i in range(7):
        data = hoje - timedelta(days=i)
        
        # Criar 2-4 consultas por dia
        for j in range(2 + (i % 3)):  # Varia entre 2 e 4 consultas
            pet = pets[j % pets.count()]
            
            # Status variado
            if i == 0:  # Hoje
                status = 'AGENDADA'
            elif i == 1:  # Ontem
                status = 'REALIZADA'
            else:
                status = 'REALIZADA' if j % 2 == 0 else 'AGENDADA'
            
            # Veterinários variados
            veterinarios = [
                'MV Paulo Alelúia',
                'MV Cleber Azevedo Souza',
                'MV Ana Carolinna Piazza',
                'MV Camila Banborra'
            ]
            
            consulta, created = Consulta.objects.get_or_create(
                pet=pet,
                data_hora=data.replace(hour=9 + j, minute=0, second=0, microsecond=0),
                defaults={
                    'veterinario': veterinarios[j % len(veterinarios)],
                    'motivo': f'Consulta de rotina - dia {data.strftime("%d/%m")}',
                    'diagnostico': 'Animal saudável' if status == 'REALIZADA' else '',
                    'tratamento': 'Acompanhamento' if status == 'REALIZADA' else '',
                    'status': status,
                    'observacoes': f'Consulta criada para teste do dashboard - {data.strftime("%d/%m/%Y")}'
                }
            )
            
            if created:
                print(f"Consulta criada: {consulta}")
            else:
                print(f"Consulta já existente: {consulta}")

def criar_agendamentos_recentes():
    """Cria agendamentos recentes para o dashboard"""
    hoje = timezone.now()
    pets = Pet.objects.all()
    
    if not pets.exists():
        print("Nenhum pet encontrado.")
        return
    
    tipos = ['CONSULTA', 'VACINA', 'EXAME', 'MEDICACAO']
    status_list = ['PENDENTE', 'CONFIRMADO', 'CANCELADO']
    
    # Criar agendamentos para os próximos 7 dias
    for i in range(7):
        data = hoje + timedelta(days=i)
        
        for j in range(1 + (i % 2)):  # 1-2 agendamentos por dia
            pet = pets[j % pets.count()]
            tipo = tipos[j % len(tipos)]
            status = status_list[j % len(status_list)]
            
            agenda, created = Agenda.objects.get_or_create(
                pet=pet,
                data_hora=data.replace(hour=10 + j, minute=0, second=0, microsecond=0),
                defaults={
                    'veterinario': 'MV Paulo Alelúia',
                    'tipo': tipo,
                    'titulo': f'{tipo} - {pet.nome}',
                    'descricao': f'Agendamento de {tipo.lower()} para {pet.nome}',
                    'status': status,
                    'concluido': status == 'CONFIRMADO',
                    'notificar': True
                }
            )
            
            if created:
                print(f"Agendamento criado: {agenda}")
            else:
                print(f"Agendamento já existente: {agenda}")

def criar_consultas_mensais():
    """Cria consultas para os últimos 6 meses para mostrar crescimento"""
    hoje = timezone.now()
    pets = Pet.objects.all()
    
    if not pets.exists():
        print("Nenhum pet encontrado.")
        return
    
    # Criar consultas para os últimos 6 meses
    for mes in range(6):
        data = hoje.replace(day=1) - timedelta(days=30*mes)
        
        # Criar 10-20 consultas por mês
        for j in range(10 + (mes % 10)):
            pet = pets[j % pets.count()]
            
            # Data aleatória no mês
            dia = 1 + (j % 28)
            hora = 8 + (j % 8)
            
            data_consulta = data.replace(day=dia, hour=hora, minute=0, second=0, microsecond=0)
            
            # Só criar se a data for no passado
            if data_consulta < hoje:
                veterinarios = [
                    'MV Paulo Alelúia',
                    'MV Cleber Azevedo Souza',
                    'MV Ana Carolinna Piazza',
                    'MV Camila Banborra'
                ]
                
                consulta, created = Consulta.objects.get_or_create(
                    pet=pet,
                    data_hora=data_consulta,
                    defaults={
                        'veterinario': veterinarios[j % len(veterinarios)],
                        'motivo': f'Consulta mensal - {data_consulta.strftime("%m/%Y")}',
                        'diagnostico': 'Animal saudável',
                        'tratamento': 'Acompanhamento',
                        'status': 'REALIZADA',
                        'observacoes': f'Consulta histórica para dashboard - {data_consulta.strftime("%d/%m/%Y")}'
                    }
                )
                
                if created:
                    print(f"Consulta mensal criada: {consulta}")

def verificar_dados():
    """Verifica os dados existentes no banco"""
    print("\n=== VERIFICAÇÃO DE DADOS ===")
    print(f"Total de Donos: {Dono.objects.count()}")
    print(f"Total de Pets: {Pet.objects.count()}")
    print(f"Total de Consultas: {Consulta.objects.count()}")
    print(f"Total de Agendamentos: {Agenda.objects.count()}")
    
    # Verificar consultas por status
    print(f"\nConsultas por Status:")
    for status in ['AGENDADA', 'REALIZADA', 'CANCELADA']:
        count = Consulta.objects.filter(status=status).count()
        print(f"  {status}: {count}")
    
    # Verificar consultas dos últimos 7 dias
    hoje = timezone.now()
    inicio_semana = hoje - timedelta(days=7)
    consultas_semana = Consulta.objects.filter(data_hora__gte=inicio_semana).count()
    print(f"\nConsultas dos últimos 7 dias: {consultas_semana}")
    
    # Verificar espécies
    print(f"\nDistribuição por Espécie:")
    from django.db.models import Count
    especies = Pet.objects.values('especie').annotate(total=Count('id')).order_by('-total')
    for especie in especies:
        print(f"  {especie['especie']}: {especie['total']}")
    
    # Verificar veterinários
    print(f"\nConsultas por Veterinário:")
    veterinarios = Consulta.objects.values('veterinario').annotate(total=Count('id')).order_by('-total')
    for vet in veterinarios:
        print(f"  {vet['veterinario']}: {vet['total']}")

def main():
    """Função principal"""
    print("🚀 Populando dados para o Dashboard PetVet...")
    
    # Verificar dados existentes
    verificar_dados()
    
    print("\n📊 Criando dados adicionais...")
    
    # Criar consultas dos últimos 7 dias
    criar_consultas_recentes()
    
    # Criar agendamentos recentes
    criar_agendamentos_recentes()
    
    # Criar consultas mensais para histórico
    criar_consultas_mensais()
    
    print("\n✅ Dados populados com sucesso!")
    
    # Verificar dados finais
    verificar_dados()

if __name__ == '__main__':
    main()
