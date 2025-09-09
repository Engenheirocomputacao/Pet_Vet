from django import forms
from django.contrib.auth.models import User
from .models import Dono, Pet, Consulta, Medicacao, Prescricao, Agenda, Profile

class DonoForm(forms.ModelForm):
    class Meta:
        model = Dono
        fields = ['nome', 'cpf', 'telefone', 'email', 'endereco']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome completo'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'endereco': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Endereço completo', 'rows': 3}),
        }

class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['nome', 'dono', 'especie', 'raca', 'sexo', 'data_nascimento', 'peso', 'foto', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do pet'}),
            'dono': forms.Select(attrs={'class': 'form-select'}),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Raça'}),
            'sexo': forms.Select(attrs={'class': 'form-select'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Peso em kg'}),
            'foto': forms.FileInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 3}),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['pet', 'veterinario', 'data_hora', 'motivo', 'diagnostico', 'tratamento', 'status', 'observacoes']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
            'data_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'motivo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Motivo da consulta'}),
            'diagnostico': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Diagnóstico', 'rows': 3}),
            'tratamento': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tratamento', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 3}),
        }

class MedicacaoForm(forms.ModelForm):
    class Meta:
        model = Medicacao
        fields = ['nome', 'descricao', 'instrucoes']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome da medicação'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 3}),
            'instrucoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Instruções de uso', 'rows': 3}),
        }

class PrescricaoForm(forms.ModelForm):
    class Meta:
        model = Prescricao
        fields = ['consulta', 'medicacao', 'dosagem', 'frequencia', 'duracao', 'data_inicio', 'data_fim', 'observacoes']
        widgets = {
            'consulta': forms.Select(attrs={'class': 'form-select'}),
            'medicacao': forms.Select(attrs={'class': 'form-select'}),
            'dosagem': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dosagem (ex: 10mg, 1 comprimido)'}),
            'frequencia': forms.Select(attrs={'class': 'form-select'}),
            'duracao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duração em dias'}),
            'data_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'data_fim': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Observações', 'rows': 3}),
        }

class AgendaForm(forms.ModelForm):
    class Meta:
        model = Agenda
        fields = ['pet', 'veterinario', 'tipo', 'titulo', 'descricao', 'data_hora', 'notificar']
        widgets = {
            'pet': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Título do agendamento'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descrição', 'rows': 3}),
            'data_hora': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'notificar': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'telefone']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
