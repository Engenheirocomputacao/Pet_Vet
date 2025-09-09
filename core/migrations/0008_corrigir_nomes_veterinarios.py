from django.db import migrations

def update_veterinario_names(apps, schema_editor):
    Agenda = apps.get_model('core', 'Agenda')
    
    # Atualiza os nomes dos veterinários existentes
    Agenda.objects.filter(veterinario='MV Paulo Alelúlia').update(veterinario='MV Paulo Alelúia')
    Agenda.objects.filter(veterinario='MV Cleber Azevedon Souza').update(veterinario='MV Cleber Azevedo Souza')
    Agenda.objects.filter(veterinario='MV Ana Aarolina Piazza').update(veterinario='MV Ana Carolinna Piazza')
    Agenda.objects.filter(veterinario='MV Camila Banborra').update(veterinario='MV Camila Banborra')

def reverse_update(apps, schema_editor):
    # Função para reverter as alterações, se necessário
    Agenda = apps.get_model('core', 'Agenda')
    
    Agenda.objects.filter(veterinario='MV Paulo Alelúia').update(veterinario='MV Paulo Alelúlia')
    Agenda.objects.filter(veterinario='MV Cleber Azevedo Souza').update(veterinario='MV Cleber Azevedon Souza')
    Agenda.objects.filter(veterinario='MV Ana Carolinna Piazza').update(veterinario='MV Ana Aarolina Piazza')
    # O nome 'MV Camila Banborra' não precisa de atualização reversa pois está correto

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_agenda_veterinario'),
    ]

    operations = [
        migrations.RunPython(update_veterinario_names, reverse_code=reverse_update),
    ]
