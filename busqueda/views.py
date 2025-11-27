from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.models import CustomUser, Habilidad

@login_required
def buscar(request):
    """
    HU-20: Buscar usuarios por habilidad.
    HU-19: Filtrar por carrera.
    """
    query = request.GET.get('q', '') # Término de búsqueda (ej. 'Excel')
    carrera_filter = request.GET.get('carrera', '') # Filtro de carrera

    # Obtener todos los usuarios activos (menos yo mismo y los admins)
    usuarios = CustomUser.objects.filter(
        is_active=True, 
        is_superuser=False
    ).exclude(id=request.user.id)

    # Aplicar filtro de búsqueda por habilidad (HU-20)
    if query:
        # Buscamos usuarios que tengan una habilidad ofrecida que contenga el texto 'query'
        usuarios = usuarios.filter(
            habilidades_ofrecidas__nombre__icontains=query
        ).distinct()

    # Aplicar filtro por carrera (HU-19)
    if carrera_filter:
        usuarios = usuarios.filter(carrera=carrera_filter)

    # Obtener lista de carreras para el select del filtro (solo las que existen en la BD)
    carreras_disponibles = CustomUser.objects.exclude(carrera__isnull=True).exclude(carrera='').values_list('carrera', flat=True).distinct()

    context = {
        'usuarios': usuarios,
        'query': query,
        'carrera_filter': carrera_filter,
        'carreras_disponibles': carreras_disponibles,
    }
    return render(request, 'busqueda/buscar.html', context)

@login_required
def perfil_publico(request, user_id):
    """
    HU-23: Ver perfil detallado de otro estudiante.
    """
    perfil_usuario = get_object_or_404(CustomUser, id=user_id)
    
    # Evitar ver mi propio perfil público (redirigir a mi perfil privado)
    if perfil_usuario == request.user:
        return redirect('profile')

    context = {
        'perfil': perfil_usuario,
    }
    return render(request, 'busqueda/perfil_publico.html', context)