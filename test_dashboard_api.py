#!/usr/bin/env python
import os
import sys
import django
import json

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pet_vet_project.settings')
django.setup()

# Importar views do dashboard
from core.dashboard_views import (
    get_overview_data,
    get_consultas_periodo_data,
    get_especies_racas_data,
    get_veterinarios_performance_data,
    get_clientes_fidelizacao_data,
    get_saude_animal_data
)

def test_dashboard_apis():
    """Testa todas as APIs do dashboard"""
    print("🧪 TESTANDO APIS DO DASHBOARD")
    print("=" * 50)
    
    # Teste 1: Dados de visão geral
    print("\n1️⃣ Testando get_overview_data()...")
    try:
        data = get_overview_data()
        print(f"✅ Sucesso: {len(data['meses'])} meses, {len(data['consultas_mensais'])} consultas")
        print(f"   Meses: {data['meses']}")
        print(f"   Consultas: {data['consultas_mensais']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 2: Consultas por período
    print("\n2️⃣ Testando get_consultas_periodo_data()...")
    try:
        data = get_consultas_periodo_data()
        print(f"✅ Sucesso: {len(data['consultas_semana'])} dias, {len(data['datas_semana'])} datas")
        print(f"   Consultas: {data['consultas_semana']}")
        print(f"   Datas: {data['datas_semana']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 3: Espécies e raças
    print("\n3️⃣ Testando get_especies_racas_data()...")
    try:
        data = get_especies_racas_data()
        print(f"✅ Sucesso: {len(data['especies'])} espécies, {len(data['racas'])} raças")
        print(f"   Espécies: {data['especies']}")
        print(f"   Raças: {data['racas']}")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 4: Performance dos veterinários
    print("\n4️⃣ Testando get_veterinarios_performance_data()...")
    try:
        data = get_veterinarios_performance_data()
        print(f"✅ Sucesso: {len(data['veterinarios'])} veterinários")
        for vet in data['veterinarios']:
            print(f"   {vet['veterinario']}: {vet['total_consultas']} consultas, {vet['taxa_realizacao']}% taxa")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 5: Fidelização de clientes
    print("\n5️⃣ Testando get_clientes_fidelizacao_data()...")
    try:
        data = get_clientes_fidelizacao_data()
        print(f"✅ Sucesso: {len(data['donos_multiplos_pets'])} donos múltiplos pets")
        print(f"   {len(data['donos_consultas'])} donos com consultas")
        print(f"   Taxa de retorno: {data['taxa_retorno']}%")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    # Teste 6: Saúde animal
    print("\n6️⃣ Testando get_saude_animal_data()...")
    try:
        data = get_saude_animal_data()
        print(f"✅ Sucesso: {len(data['pets_idade'])} faixas de idade")
        print(f"   {len(data['pets_peso'])} espécies com peso")
        print(f"   {len(data['motivos_consultas'])} motivos de consulta")
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TESTE CONCLUÍDO!")

def test_dashboard_data():
    """Testa os dados principais do dashboard"""
    print("\n📊 TESTANDO DADOS PRINCIPAIS DO DASHBOARD")
    print("=" * 50)
    
    from core.dashboard_views import get_dashboard_data
    
    try:
        data = get_dashboard_data()
        print("✅ Dados principais obtidos com sucesso!")
        print(f"   Total Donos: {data['total_donos']}")
        print(f"   Total Pets: {data['total_pets']}")
        print(f"   Total Consultas: {data['total_consultas']}")
        print(f"   Consultas Mês: {data['consultas_mes']}")
        print(f"   Consultas Ano: {data['consultas_ano']}")
        print(f"   Consultas Agendadas: {data['consultas_agendadas']}")
        print(f"   Consultas Realizadas: {data['consultas_realizadas']}")
        print(f"   Agendamentos Pendentes: {data['agendamentos_pendentes']}")
        
        print(f"\n   Espécies: {len(data['especies_count'])}")
        for especie in data['especies_count']:
            print(f"     {especie['especie']}: {especie['total']}")
        
        print(f"\n   Veterinários: {len(data['veterinarios_count'])}")
        for vet in data['veterinarios_count']:
            print(f"     {vet['veterinario']}: {vet['total']}")
            
    except Exception as e:
        print(f"❌ Erro nos dados principais: {e}")

if __name__ == '__main__':
    test_dashboard_apis()
    test_dashboard_data()
