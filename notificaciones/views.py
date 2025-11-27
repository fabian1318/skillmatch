from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notificacion

@login_required
def marcar_como_leida(request, notificacion_id):
    """
    Marca una notificación como leída y redirige a su destino.
    """
    notificacion = get_object_or_404(Notificacion, id=notificacion_id, usuario=request.user)
    
    # Marcar como leída
    if not notificacion.leido:
        notificacion.leido = True
        notificacion.save()
    
    # Redirigir al destino (si existe) o a la lista de notificaciones
    if notificacion.url_destino:
        return redirect(notificacion.url_destino)
    else:
        return redirect('listar_notificaciones')

@login_required
def listar_notificaciones(request):
    """
    HU-28: Ver historial completo de notificaciones.
    """
    # Obtener todas las notificaciones del usuario (leídas y no leídas)
    notificaciones = request.user.notificaciones.all()
    
    # Opción: Marcar todas como leídas al entrar aquí
    # request.user.notificaciones.filter(leido=False).update(leido=True)

    return render(request, 'notificaciones/lista.html', {'notificaciones': notificaciones})