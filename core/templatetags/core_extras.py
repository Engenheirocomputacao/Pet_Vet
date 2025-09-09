from django import template
from django.apps import apps

register = template.Library()

@register.filter
def class_name(obj):
    return obj.__class__.__name__

@register.filter
def model_name(obj):
    """
    Retorna o nome do modelo em minúsculas para uso em templates
    Exemplo: {{ object|model_name }}
    """
    if hasattr(obj, '_meta'):
        return obj._meta.model_name
    return ''