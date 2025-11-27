from .models import Notificacion

def notificaciones_globales(request):
    """
    Inyecta las notificaciones no leídas en todas las plantillas.
    Disponible como la variable {{ notificaciones_no_leidas }}
    """
    if request.user.is_authenticated:
        notificaciones = Notificacion.objects.filter(
            usuario=request.user, 
            leido=False
        ).order_by('-fecha_creacion')[:5] # Mostramos las 5 más recientes
        
        conteo = Notificacion.objects.filter(usuario=request.user, leido=False).count()
        
        return {
            'notificaciones_no_leidas': notificaciones,
            'conteo_notificaciones': conteo
        }
    return {}