from django.db import migrations

def create_profiles_for_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('core', 'Profile')
    
    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)

class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_profile'),
    ]

    operations = [
        migrations.RunPython(create_profiles_for_existing_users),
    ] 