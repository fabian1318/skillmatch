from .models import Insignia

def verificar_logros(usuario):
    """
    Verifica si el usuario cumple requisitos para nuevas insignias
    y se las asigna automáticamente.
    """
    # Estadísticas actuales
    # Nota: Ajusta los nombres de relación si cambiaste los related_name en models.py
    # Asumimos: related_name='solicitudes_enviadas' / 'solicitudes_recibidas'
    
    total_intercambios = 0
    if hasattr(usuario, 'solicitudes_enviadas'):
        total_intercambios += usuario.solicitudes_enviadas.filter(estado='Completado').count()
    if hasattr(usuario, 'solicitudes_recibidas'):
        total_intercambios += usuario.solicitudes_recibidas.filter(estado='Completado').count()

    promedio = usuario.reputacion

    # --- REGLA 1: Primeros Pasos (1 intercambio) ---
    if total_intercambios >= 1:
        otorgar_insignia(usuario, "Iniciador", "bi-rocket-takeoff", "Completar tu primer intercambio.")

    # --- REGLA 2: Veterano (5 intercambios) ---
    if total_intercambios >= 5:
        otorgar_insignia(usuario, "Veterano", "bi-shield-check", "Completar 5 intercambios.")

    # --- REGLA 3: Mentor Estrella (Reputación alta) ---
    if promedio >= 4.5 and total_intercambios >= 3:
        otorgar_insignia(usuario, "Mentor Estrella", "bi-star-fill", "Mantener un promedio sobre 4.5 en 3+ sesiones.")

def otorgar_insignia(usuario, nombre, icono_defecto, requisito_defecto):
    """
    Busca la insignia por nombre (o la crea si no existe) y se la da al usuario.
    """
    # Get or Create para asegurar que la insignia exista en la BD
    insignia, created = Insignia.objects.get_or_create(
        nombre=nombre,
        defaults={
            'descripcion': f"Otorgada por: {requisito_defecto}",
            'icono': icono_defecto,
            'requisito': requisito_defecto
        }
    )
    
    # Si el usuario no la tiene, se la agregamos
    if insignia not in usuario.insignias.all():
        usuario.insignias.add(insignia)
        return True # Retorna True si se ganó una nueva
    
    return False