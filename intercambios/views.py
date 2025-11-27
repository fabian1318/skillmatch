from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse # <-- Necesario para generar links de notificaciones
from accounts.models import CustomUser, Habilidad
from accounts.gamification import verificar_logros
from .models import Intercambio, Resena, Reporte
from .forms import ResenaForm, ReporteForm
from django.db.models import Avg
# --- NUEVO IMPORT PARA NOTIFICACIONES ---
from notificaciones.models import Notificacion

@login_required
def iniciar_solicitud(request, receptor_id, habilidad_id):
    """HU-21: Iniciar solicitud de intercambio 1x1."""
    receptor = get_object_or_404(CustomUser, id=receptor_id)
    habilidad_solicitada = get_object_or_404(Habilidad, id=habilidad_id)

    if request.method == 'POST':
        habilidad_ofrecida_id = request.POST.get('habilidad_ofrecida')
        
        if habilidad_ofrecida_id:
            habilidad_ofrecida = get_object_or_404(Habilidad, id=habilidad_ofrecida_id)
            
            # Crear el intercambio
            intercambio = Intercambio.objects.create(
                solicitante=request.user,
                receptor=receptor,
                habilidad_solicitada=habilidad_solicitada,
                habilidad_ofrecida=habilidad_ofrecida,
                estado='Pendiente'
            )
            
            # ### NUEVO: Crear Notificación para el Receptor ###
            Notificacion.objects.create(
                usuario=receptor,
                mensaje=f"¡Hola! {request.user.first_name} quiere aprender {habilidad_solicitada.nombre} contigo.",
                url_destino=reverse('listar_intercambios') # Lleva a "Mis Intercambios"
            )
            # #################################################
            
            messages.success(request, f'¡Solicitud enviada a {receptor.first_name}!')
            return redirect('buscar')
        else:
            messages.error(request, 'Debes seleccionar una habilidad para ofrecer.')

    mis_habilidades = request.user.habilidades_ofrecidas.all()
    
    context = {
        'receptor': receptor,
        'habilidad_solicitada': habilidad_solicitada,
        'mis_habilidades': mis_habilidades
    }
    return render(request, 'intercambios/crear_solicitud.html', context)

@login_required
def listar_intercambios(request):
    """HU-15: Historial de intercambios."""
    solicitudes_recibidas = Intercambio.objects.filter(receptor=request.user).order_by('-fecha_creacion')
    solicitudes_enviadas = Intercambio.objects.filter(solicitante=request.user).order_by('-fecha_creacion')

    context = {
        'solicitudes_recibidas': solicitudes_recibidas,
        'solicitudes_enviadas': solicitudes_enviadas
    }
    return render(request, 'intercambios/lista_intercambios.html', context)

@login_required
def responder_solicitud(request, intercambio_id, accion):
    """Maneja la aceptación o rechazo."""
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)

    if request.user != intercambio.receptor:
        messages.error(request, "No tienes permiso para responder esta solicitud.")
        return redirect('listar_intercambios')

    if accion == 'aceptar':
        intercambio.estado = 'Aceptado'
        intercambio.save()
        
        # ### NUEVO: Notificar al Solicitante que fue aceptado ###
        Notificacion.objects.create(
            usuario=intercambio.solicitante,
            mensaje=f"¡Genial! {request.user.first_name} aceptó tu solicitud de intercambio.",
            url_destino=reverse('listar_intercambios')
        )
        # #######################################################

        messages.success(request, f"¡Has aceptado el intercambio con {intercambio.solicitante.first_name}!")
        
    elif accion == 'rechazar':
        intercambio.estado = 'Rechazado'
        intercambio.save()
        
        # ### NUEVO: Notificar rechazo ###
        Notificacion.objects.create(
            usuario=intercambio.solicitante,
            mensaje=f"{request.user.first_name} no puede aceptar tu solicitud por ahora.",
            url_destino=reverse('listar_intercambios')
        )
        # ###############################

        messages.warning(request, "Has rechazado la solicitud.")
    
    return redirect('listar_intercambios')

@login_required
def iniciar_intercambio(request, intercambio_id):
    """HU-10: Marcar solicitud como En Progreso."""
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    
    if request.user not in [intercambio.solicitante, intercambio.receptor]:
        messages.error(request, "No tienes permiso para gestionar este intercambio.")
        return redirect('listar_intercambios')

    if intercambio.estado == 'Aceptado':
        intercambio.estado = 'EnProgreso'
        intercambio.save()
        
        # Notificar a la contraparte
        otro_usuario = intercambio.receptor if request.user == intercambio.solicitante else intercambio.solicitante
        Notificacion.objects.create(
            usuario=otro_usuario,
            mensaje=f"El intercambio de {intercambio.habilidad_solicitada.nombre} ha comenzado.",
            url_destino=reverse('listar_intercambios')
        )

        messages.success(request, "¡El intercambio ha comenzado!")
    
    return redirect('listar_intercambios')

@login_required
def finalizar_intercambio(request, intercambio_id):
    """HU-13: Marcar intercambio como Completado."""
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    
    if request.user not in [intercambio.solicitante, intercambio.receptor]:
        messages.error(request, "No tienes permiso.")
        return redirect('listar_intercambios')

    if intercambio.estado == 'EnProgreso':
        intercambio.estado = 'Completado'
        intercambio.save()
        
        # Verificar logros (Gamificación)
        verificar_logros(intercambio.solicitante)
        verificar_logros(intercambio.receptor)
        
        # Notificar finalización
        otro_usuario = intercambio.receptor if request.user == intercambio.solicitante else intercambio.solicitante
        Notificacion.objects.create(
            usuario=otro_usuario,
            mensaje=f"El intercambio ha sido marcado como completado. ¡No olvides calificar!",
            url_destino=reverse('listar_intercambios')
        )

        messages.success(request, "¡Felicidades! Intercambio completado exitosamente.")
    
    return redirect('listar_intercambios')

@login_required
def calificar_intercambio(request, intercambio_id):
    """HU-11: Calificar con estrellas y comentarios."""
    intercambio = get_object_or_404(Intercambio, id=intercambio_id)
    
    if intercambio.estado != 'Completado':
        messages.error(request, "Solo puedes calificar intercambios completados.")
        return redirect('listar_intercambios')
        
    if request.user == intercambio.solicitante:
        usuario_a_calificar = intercambio.receptor
    else:
        usuario_a_calificar = intercambio.solicitante

    try:
        resena_existente = Resena.objects.get(intercambio=intercambio, autor=request.user)
    except Resena.DoesNotExist:
        resena_existente = None

    if request.method == 'POST':
        form = ResenaForm(request.POST, instance=resena_existente)
        if form.is_valid():
            resena = form.save(commit=False)
            resena.intercambio = intercambio
            resena.autor = request.user
            resena.calificado = usuario_a_calificar
            resena.save()
            
            # Actualizar promedio
            nuevo_promedio = Resena.objects.filter(calificado=usuario_a_calificar).aggregate(Avg('estrellas'))['estrellas__avg']
            if nuevo_promedio:
                usuario_a_calificar.reputacion = round(nuevo_promedio, 2)
                usuario_a_calificar.save()

            verificar_logros(usuario_a_calificar)
            
            # Notificar calificación recibida
            Notificacion.objects.create(
                usuario=usuario_a_calificar,
                mensaje=f"{request.user.first_name} te ha calificado con {resena.estrellas} estrellas.",
                url_destino=reverse('profile')
            )

            messages.success(request, f"¡Reseña guardada para {usuario_a_calificar.first_name}!")
            return redirect('listar_intercambios')
    else:
        form = ResenaForm(instance=resena_existente)

    return render(request, 'intercambios/calificar.html', {
        'form': form, 
        'intercambio': intercambio, 
        'otro_usuario': usuario_a_calificar
    })

@login_required
def reportar_usuario(request, usuario_id):
    """HU-22: Reportar conducta inapropiada."""
    usuario_a_reportar = get_object_or_404(CustomUser, id=usuario_id)
    
    if request.method == 'POST':
        form = ReporteForm(request.POST)
        if form.is_valid():
            reporte = form.save(commit=False)
            reporte.denunciante = request.user
            reporte.denunciado = usuario_a_reportar
            reporte.save()
            
            messages.warning(request, "Tu reporte ha sido enviado a administración para su revisión.")
            return redirect('buscar')
    else:
        form = ReporteForm()
    
    return render(request, 'intercambios/reportar.html', {
        'form': form, 
        'usuario': usuario_a_reportar
    })