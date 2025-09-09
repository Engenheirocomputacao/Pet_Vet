from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.conf import settings
from .pet_tips import get_random_pet_tip, DEFAULT_PET_TIPS
import json
import random

@csrf_exempt
@require_http_methods(["GET"])
@cache_page(30)  # Cache de 30 segundos
@require_GET
def pet_tip_api(request):
    """
    API endpoint que retorna uma dica aleatória de cuidados com pets.
    """
    try:
        # Tenta obter uma dica usando a função principal
        tip = get_random_pet_tip()
        
        # Garante que a dica não está vazia
        if not tip or not tip.strip():
            tip = random.choice(DEFAULT_PET_TIPS)
            
        # Adiciona headers para evitar cache do navegador
        response = JsonResponse({'tip': tip})
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
        
    except Exception as e:
        # Log do erro para debug
        print(f"Erro na API de dicas: {str(e)}")
        
        # Retorna uma dica padrão em caso de erro
        default_tips = [
            "A escovação diária dos dentes do seu pet pode prevenir doenças periodontais graves.",
            "A vacinação anual é essencial para prevenir doenças como raiva e cinomose.",
            "Mantenha sempre água limpa e fresca disponível para o seu pet.",
            "A obesidade em pets pode reduzir significativamente a expectativa de vida.",
            "Consulte regularmente um médico veterinário para check-ups preventivos."
        ]
        
        response = JsonResponse({
            'tip': random.choice(default_tips),
            'error': str(e)
        }, status=500)
        
        # Headers para evitar cache em caso de erro
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        
        return response
