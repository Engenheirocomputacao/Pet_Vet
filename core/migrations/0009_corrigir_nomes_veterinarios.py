from django.db import migrations

def update_veterinario_names(apps, schema_editor):
    # Atualiza os nomes nas consultas
    Consulta = apps.get_model('core', 'Consulta')
    Consulta.objects.filter(veterinario='MV Paulo Alelúlia').update(veterinario='MV Paulo Alelúia')
    Consulta.objects.filter(veterinario='MV Cleber Azevedon Souza').update(veterinario='MV Cleber Azevedo Souza')
    Consulta.objects.filter(veterinario='MV Ana Aarolina Piazza').update(veterinario='MV Ana Carolinna Piazza')
    
    # Atualiza os nomes na agenda
    Agenda = apps.get_model('core', 'Agenda')
    Agenda.objects.filter(veterinario='MV Paulo Alelúlia').update(veterinario='MV Paulo Alelúia')
    Agenda.objects.filter(veterinario='MV Cleber Azevedon Souza').update(veterinario='MV Cleber Azevedo Souza')
    Agenda.objects.filter(veterinario='MV Ana Aarolina Piazza').update(veterinario='MV Ana Carolinna Piazza')

def reverse_update(apps, schema_editor):
    # Função para reverter as alterações, se necessário
    Consulta = apps.get_model('core', 'Consulta')
    Consulta.objects.filter(veterinario='MV Paulo Alelúia').update(veterinario='MV Paulo Alelúlia')
    Consulta.objects.filter(veterinario='MV Cleber Azevedo Souza').update(veterinario='MV Cleber Azevedon Souza')
    Consulta.objects.filter(veterinario='MV Ana Carolinna Piazza').update(veterinario='MV Ana Aarolina Piazza')
    
    Agenda = apps.get_model('core', 'Agenda')
    Agenda.objects.filter(veterinario='MV Paulo Alelúia').update(veterinario='MV Paulo Alelúlia')
    Agenda.objects.filter(veterinario='MV Cleber Azevedo Souza').update(veterinario='MV Cleber Azevedon Souza')
    Agenda.objects.filter(veterinario='MV Ana Carolinna Piazza').update(veterinario='MV Ana Aarolina Piazza')

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_corrigir_nomes_veterinarios'),
    ]

    operations = [
        migrations.RunPython(update_veterinario_names, reverse_code=reverse_update),
    ]
