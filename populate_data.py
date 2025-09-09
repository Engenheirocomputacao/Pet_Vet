#!/usr/bin/env python
import os
import sys
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar ambiente Django
sys.path.append('/home/ubuntu/pet_vet')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_vet_project.settings')
django.setup()

# Importar modelos após configuração do Django
from core.models import Dono, Pet, Consulta, Medicacao, Prescricao, Agenda

def criar_donos():
    """Cria 5 donos de exemplo"""
    donos = [
        {
            'nome': 'Carlos Silva',
            'cpf': '123.456.789-00',
            'telefone': '(11) 98765-4321',
            'email': 'carlos.silva@email.com',
            'endereco': 'Rua das Flores, 123, São Paulo - SP'
        },
        {
            'nome': 'Maria Oliveira',
            'cpf': '987.654.321-00',
            'telefone': '(21) 91234-5678',
            'email': 'maria.oliveira@email.com',
            'endereco': 'Avenida Central, 456, Rio de Janeiro - RJ'
        },
        {
            'nome': 'João Santos',
            'cpf': '456.789.123-00',
            'telefone': '(31) 99876-5432',
            'email': 'joao.santos@email.com',
            'endereco': 'Rua dos Ipês, 789, Belo Horizonte - MG'
        },
        {
            'nome': 'Ana Pereira',
            'cpf': '789.123.456-00',
            'telefone': '(41) 98765-1234',
            'email': 'ana.pereira@email.com',
            'endereco': 'Avenida das Araucárias, 321, Curitiba - PR'
        },
        {
            'nome': 'Roberto Costa',
            'cpf': '321.654.987-00',
            'telefone': '(51) 97654-3210',
            'email': 'roberto.costa@email.com',
            'endereco': 'Rua da Praia, 654, Porto Alegre - RS'
        }
    ]
    
    dono_objects = []
    for dono_data in donos:
        dono, created = Dono.objects.get_or_create(
            cpf=dono_data['cpf'],
            defaults=dono_data
        )
        dono_objects.append(dono)
        if created:
            print(f"Dono criado: {dono.nome}")
        else:
            print(f"Dono já existente: {dono.nome}")
    
    return dono_objects

def criar_pets(donos):
    """Cria 5 pets de exemplo, um para cada dono"""
    pets = [
        {
            'nome': 'Rex',
            'dono': donos[0],
            'especie': 'CACHORRO',
            'raca': 'Labrador',
            'sexo': 'M',
            'data_nascimento': timezone.now().date() - timedelta(days=365*3),  # 3 anos
            'peso': 25.5,
            'observacoes': 'Muito dócil e brincalhão. Gosta de correr no parque.'
        },
        {
            'nome': 'Mia',
            'dono': donos[1],
            'especie': 'GATO',
            'raca': 'Siamês',
            'sexo': 'F',
            'data_nascimento': timezone.now().date() - timedelta(days=365*2),  # 2 anos
            'peso': 4.2,
            'observacoes': 'Gata independente e curiosa. Prefere ficar em locais altos.'
        },
        {
            'nome': 'Pingo',
            'dono': donos[2],
            'especie': 'CACHORRO',
            'raca': 'Poodle',
            'sexo': 'M',
            'data_nascimento': timezone.now().date() - timedelta(days=365*5),  # 5 anos
            'peso': 8.7,
            'observacoes': 'Cão tranquilo e obediente. Tem alergia a alguns alimentos.'
        },
        {
            'nome': 'Luna',
            'dono': donos[3],
            'especie': 'GATO',
            'raca': 'Persa',
            'sexo': 'F',
            'data_nascimento': timezone.now().date() - timedelta(days=365*1),  # 1 ano
            'peso': 3.8,
            'observacoes': 'Gata calma e carinhosa. Gosta de brincar com bolinhas.'
        },
        {
            'nome': 'Thor',
            'dono': donos[4],
            'especie': 'CACHORRO',
            'raca': 'Pastor Alemão',
            'sexo': 'M',
            'data_nascimento': timezone.now().date() - timedelta(days=365*4),  # 4 anos
            'peso': 32.1,
            'observacoes': 'Cão protetor e leal. Excelente guardião da casa.'
        }
    ]
    
    pet_objects = []
    for pet_data in pets:
        pet, created = Pet.objects.get_or_create(
            nome=pet_data['nome'],
            dono=pet_data['dono'],
            defaults=pet_data
        )
        pet_objects.append(pet)
        if created:
            print(f"Pet criado: {pet.nome} ({pet.dono.nome})")
        else:
            print(f"Pet já existente: {pet.nome} ({pet.dono.nome})")
    
    return pet_objects

def criar_medicacoes():
    """Cria medicações de exemplo"""
    medicacoes = [
        {
            'nome': 'Antibiótico Canino',
            'descricao': 'Antibiótico de amplo espectro para cães',
            'instrucoes': 'Administrar com alimento. Evitar exposição ao sol durante o tratamento.'
        },
        {
            'nome': 'Vermífugo Felino',
            'descricao': 'Vermífugo para gatos de todas as idades',
            'instrucoes': 'Administrar em jejum. Repetir após 15 dias.'
        },
        {
            'nome': 'Anti-inflamatório Pet',
            'descricao': 'Anti-inflamatório para cães e gatos',
            'instrucoes': 'Administrar após as refeições. Não usar por mais de 7 dias consecutivos.'
        },
        {
            'nome': 'Vitamina Pet',
            'descricao': 'Suplemento vitamínico para cães e gatos',
            'instrucoes': 'Pode ser misturado à ração diária.'
        },
        {
            'nome': 'Shampoo Medicinal',
            'descricao': 'Shampoo para tratamento de problemas de pele',
            'instrucoes': 'Aplicar no pelo molhado, massagear e deixar agir por 5 minutos antes de enxaguar.'
        }
    ]
    
    medicacao_objects = []
    for med_data in medicacoes:
        medicacao, created = Medicacao.objects.get_or_create(
            nome=med_data['nome'],
            defaults=med_data
        )
        medicacao_objects.append(medicacao)
        if created:
            print(f"Medicação criada: {medicacao.nome}")
        else:
            print(f"Medicação já existente: {medicacao.nome}")
    
    return medicacao_objects

def criar_consultas(pets):
    """Cria consultas de exemplo para os pets"""
    hoje = timezone.now()
    
    consultas = [
        {
            'pet': pets[0],
            'data_hora': hoje - timedelta(days=30),
            'motivo': 'Checkup anual',
            'diagnostico': 'Animal saudável',
            'tratamento': 'Manter alimentação balanceada e exercícios regulares',
            'status': 'REALIZADA',
            'observacoes': 'Próximo checkup em 1 ano'
        },
        {
            'pet': pets[1],
            'data_hora': hoje - timedelta(days=15),
            'motivo': 'Vômitos frequentes',
            'diagnostico': 'Gastrite leve',
            'tratamento': 'Medicação para gastrite e dieta especial',
            'status': 'REALIZADA',
            'observacoes': 'Retorno em 15 dias para avaliação'
        },
        {
            'pet': pets[2],
            'data_hora': hoje + timedelta(days=5),
            'motivo': 'Vacinação anual',
            'status': 'AGENDADA',
            'observacoes': 'Trazer carteira de vacinação'
        },
        {
            'pet': pets[3],
            'data_hora': hoje + timedelta(days=2),
            'motivo': 'Avaliação de rotina',
            'status': 'CONFIRMADA',
            'observacoes': 'Primeira consulta no veterinário'
        },
        {
            'pet': pets[4],
            'data_hora': hoje + timedelta(days=10),
            'motivo': 'Problema na pata traseira',
            'status': 'AGENDADA',
            'observacoes': 'Animal apresenta dificuldade para andar'
        }
    ]
    
    consulta_objects = []
    for consulta_data in consultas:
        consulta, created = Consulta.objects.get_or_create(
            pet=consulta_data['pet'],
            data_hora=consulta_data['data_hora'],
            defaults=consulta_data
        )
        consulta_objects.append(consulta)
        if created:
            print(f"Consulta criada: {consulta.pet.nome} em {consulta.data_hora.strftime('%d/%m/%Y')}")
        else:
            print(f"Consulta já existente: {consulta.pet.nome} em {consulta.data_hora.strftime('%d/%m/%Y')}")
    
    return consulta_objects

def criar_prescricoes(consultas, medicacoes):
    """Cria prescrições de medicamentos para as consultas realizadas"""
    hoje = timezone.now().date()
    
    # Apenas para consultas já realizadas
    consultas_realizadas = [c for c in consultas if c.status == 'REALIZADA']
    
    if not consultas_realizadas:
        print("Não há consultas realizadas para criar prescrições")
        return []
    
    prescricoes = [
        {
            'consulta': consultas_realizadas[0],
            'medicacao': medicacoes[3],  # Vitamina Pet
            'dosagem': '1 comprimido',
            'frequencia': '1X',
            'duracao': 30,
            'data_inicio': hoje - timedelta(days=30),
            'data_fim': hoje,
            'observacoes': 'Administrar junto com a ração'
        }
    ]
    
    if len(consultas_realizadas) > 1:
        prescricoes.append({
            'consulta': consultas_realizadas[1],
            'medicacao': medicacoes[2],  # Anti-inflamatório
            'dosagem': '1/2 comprimido',
            'frequencia': '2X',
            'duracao': 7,
            'data_inicio': hoje - timedelta(days=15),
            'data_fim': hoje - timedelta(days=8),
            'observacoes': 'Administrar após as refeições'
        })
    
    prescricao_objects = []
    for prescricao_data in prescricoes:
        prescricao, created = Prescricao.objects.get_or_create(
            consulta=prescricao_data['consulta'],
            medicacao=prescricao_data['medicacao'],
            defaults=prescricao_data
        )
        prescricao_objects.append(prescricao)
        if created:
            print(f"Prescrição criada: {prescricao.medicacao.nome} para {prescricao.consulta.pet.nome}")
        else:
            print(f"Prescrição já existente: {prescricao.medicacao.nome} para {prescricao.consulta.pet.nome}")
    
    return prescricao_objects

def criar_agendamentos(pets):
    """Cria agendamentos na agenda para os pets"""
    hoje = timezone.now()
    
    agendamentos = [
        {
            'pet': pets[0],
            'tipo': 'VACINA',
            'titulo': 'Vacina Antirrábica',
            'descricao': 'Vacinação anual obrigatória',
            'data_hora': hoje + timedelta(days=20),
            'notificar': True
        },
        {
            'pet': pets[1],
            'tipo': 'MEDICACAO',
            'titulo': 'Aplicação de Vermífugo',
            'descricao': 'Segunda dose do vermífugo',
            'data_hora': hoje + timedelta(days=15),
            'notificar': True
        },
        {
            'pet': pets[2],
            'tipo': 'EXAME',
            'titulo': 'Exame de Sangue',
            'descricao': 'Hemograma completo para avaliação geral',
            'data_hora': hoje + timedelta(days=7),
            'notificar': True
        },
        {
            'pet': pets[3],
            'tipo': 'VACINA',
            'titulo': 'Vacina V4',
            'descricao': 'Proteção contra doenças comuns em felinos',
            'data_hora': hoje + timedelta(days=25),
            'notificar': True
        },
        {
            'pet': pets[4],
            'tipo': 'OUTRO',
            'titulo': 'Tosa e Banho',
            'descricao': 'Serviço de estética completo',
            'data_hora': hoje + timedelta(days=3),
            'notificar': True
        }
    ]
    
    agenda_objects = []
    for agenda_data in agendamentos:
        agenda, created = Agenda.objects.get_or_create(
            pet=agenda_data['pet'],
            data_hora=agenda_data['data_hora'],
            titulo=agenda_data['titulo'],
            defaults=agenda_data
        )
        agenda_objects.append(agenda)
        if created:
            print(f"Agendamento criado: {agenda.titulo} para {agenda.pet.nome} em {agenda.data_hora.strftime('%d/%m/%Y')}")
        else:
            print(f"Agendamento já existente: {agenda.titulo} para {agenda.pet.nome} em {agenda.data_hora.strftime('%d/%m/%Y')}")
    
    return agenda_objects

def main():
    """Função principal para popular o banco de dados"""
    print("Iniciando população do banco de dados...")
    
    # Criar donos
    donos = criar_donos()
    
    # Criar pets
    pets = criar_pets(donos)
    
    # Criar medicações
    medicacoes = criar_medicacoes()
    
    # Criar consultas
    consultas = criar_consultas(pets)
    
    # Criar prescrições
    prescricoes = criar_prescricoes(consultas, medicacoes)
    
    # Criar agendamentos
    agendamentos = criar_agendamentos(pets)
    
    print("\nPopulação do banco de dados concluída com sucesso!")
    print(f"Foram criados:")
    print(f"- {len(donos)} donos")
    print(f"- {len(pets)} pets")
    print(f"- {len(medicacoes)} medicações")
    print(f"- {len(consultas)} consultas")
    print(f"- {len(prescricoes)} prescrições")
    print(f"- {len(agendamentos)} agendamentos")

if __name__ == "__main__":
    main()
