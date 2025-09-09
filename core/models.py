from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Dono(models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    endereco = models.TextField()
    data_cadastro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Dono'
        verbose_name_plural = 'Donos'
        ordering = ['nome']

class Pet(models.Model):
    ESPECIES = (
        ('CACHORRO', 'Cachorro'),
        ('GATO', 'Gato'),
        ('AVE', 'Ave'),
        ('ROEDOR', 'Roedor'),
        ('REPTIL', 'Réptil'),
        ('OUTRO', 'Outro'),
    )
    
    SEXO = (
        ('M', 'Macho'),
        ('F', 'Fêmea'),
    )
    
    nome = models.CharField(max_length=100)
    dono = models.ForeignKey(Dono, on_delete=models.CASCADE, related_name='pets')
    especie = models.CharField(max_length=20, choices=ESPECIES)
    raca = models.CharField(max_length=50, blank=True)
    sexo = models.CharField(max_length=1, choices=SEXO)
    data_nascimento = models.DateField(null=True, blank=True)
    peso = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    foto = models.ImageField(upload_to='pets_fotos/', null=True, blank=True)
    observacoes = models.TextField(blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.nome} ({self.dono.nome})"
    
    def idade(self):
        if self.data_nascimento:
            hoje = timezone.now().date()
            return hoje.year - self.data_nascimento.year - ((hoje.month, hoje.day) < (self.data_nascimento.month, self.data_nascimento.day))
        return None
    
    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['nome']

class Consulta(models.Model):
    STATUS = (
        ('AGENDADA', 'Agendada'),
        ('CONFIRMADA', 'Confirmada'),
        ('REALIZADA', 'Realizada'),
        ('CANCELADA', 'Cancelada'),
    )

    VETERINARIOS = (
        ('MV Paulo Alelúia', 'MV Paulo Alelúia'),
        ('MV Cleber Azevedo Souza', 'MV Cleber Azevedo Souza'),
        ('MV Ana Carolinna Piazza', 'MV Ana Carolinna Piazza'),
        ('MV Camila Banborra', 'MV Camila Banborra'),
    )

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='consultas')
    veterinario = models.CharField(max_length=100, choices=VETERINARIOS, default='MV Paulo Alelúia')
    data_hora = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    diagnostico = models.TextField(blank=True)
    tratamento = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='AGENDADA')
    observacoes = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consulta de {self.pet.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'
        ordering = ['-data_hora']

class Medicacao(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    instrucoes = models.TextField(blank=True)
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = 'Medicação'
        verbose_name_plural = 'Medicações'
        ordering = ['nome']

class Prescricao(models.Model):
    FREQUENCIA = (
        ('1X', '1 vez ao dia'),
        ('2X', '2 vezes ao dia'),
        ('3X', '3 vezes ao dia'),
        ('4X', '4 vezes ao dia'),
        ('SEMANA', 'Semanal'),
        ('QUINZENA', 'Quinzenal'),
        ('MES', 'Mensal'),
        ('OUTRO', 'Outro'),
    )
    
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='prescricoes')
    medicacao = models.ForeignKey(Medicacao, on_delete=models.CASCADE)
    dosagem = models.CharField(max_length=50)
    frequencia = models.CharField(max_length=20, choices=FREQUENCIA)
    duracao = models.IntegerField(help_text="Duração em dias")
    data_inicio = models.DateField()
    data_fim = models.DateField()
    observacoes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.medicacao.nome} - {self.dosagem} ({self.frequencia})"
    
    class Meta:
        verbose_name = 'Prescrição'
        verbose_name_plural = 'Prescrições'
        ordering = ['data_inicio']

class Agenda(models.Model):
    TIPO = (
        ('CONSULTA', 'Consulta'),
        ('MEDICACAO', 'Medicação'),
        ('VACINA', 'Vacina'),
        ('EXAME', 'Exame'),
        ('OUTRO', 'Outro'),
    )

    STATUS = (
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    )

    VETERINARIOS = (
        ('MV Paulo Alelúia', 'MV Paulo Alelúia'),
        ('MV Cleber Azevedo Souza', 'MV Cleber Azevedo Souza'),
        ('MV Ana Carolinna Piazza', 'MV Ana Carolinna Piazza'),
        ('MV Camila Banborra', 'MV Camila Banborra'),
    )

    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='agendamentos')
    veterinario = models.CharField(max_length=100, choices=VETERINARIOS, default='MV Paulo Alelúia')
    tipo = models.CharField(max_length=20, choices=TIPO)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data_hora = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS, default='PENDENTE')
    concluido = models.BooleanField(default=False)
    notificar = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.pet.nome} em {self.data_hora.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        verbose_name = 'Agenda'
        verbose_name_plural = 'Agendas'
        ordering = ['data_hora']

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    telefone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Se o usuário já existe, tenta obter o perfil ou criar um novo
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Remove o signal de save pois já estamos tratando no create_user_profile
    pass
