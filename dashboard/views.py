from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# --- IMPORTS NUEVOS PARA EL CORREO ---
from django.core.mail import send_mail
from django.conf import settings
# -------------------------------------
from accounts.models import CustomUser
from .forms import SugerenciaForm

def home(request):
    """
    HU-9: Dashboard de estadísticas personales.
    """
    if request.user.is_authenticated:
        user = request.user
        total_ofrecidas = user.habilidades_ofrecidas.count()
        total_buscadas = user.habilidades_buscadas.count()
        
        # Estadísticas simuladas o calculadas
        intercambios_completados = 0 
        if hasattr(user, 'solicitudes_enviadas'):
             intercambios_completados += user.solicitudes_enviadas.filter(estado='Completado').count()
        if hasattr(user, 'solicitudes_recibidas'):
             intercambios_completados += user.solicitudes_recibidas.filter(estado='Completado').count()

        nivel_reputacion = f"{user.reputacion} ★" if user.reputacion > 0 else "Novato"

        context = {
            'total_ofrecidas': total_ofrecidas,
            'total_buscadas': total_buscadas,
            'intercambios_completados': intercambios_completados,
            'nivel_reputacion': nivel_reputacion,
        }
        return render(request, 'dashboard/dashboard_user.html', context)
    else:
        return render(request, 'dashboard/home_guest.html')

@login_required
def enviar_sugerencia(request):
    """
    HU-27: Enviar Feedback o Sugerencias.
    Guarda en BD y envía notificación por correo al Admin.
    """
    if request.method == 'POST':
        form = SugerenciaForm(request.POST)
        if form.is_valid():
            # 1. Guardar el registro en la Base de Datos
            sugerencia = form.save(commit=False)
            sugerencia.usuario = request.user
            sugerencia.save()
            
            # 2. Enviar Correo Electrónico (Lógica agregada)
            asunto = f"Nueva {sugerencia.tipo} de {request.user.first_name} en SkillMatch"
            mensaje_email = f"""
            Has recibido un nuevo mensaje en el buzón de sugerencias:
            
            ----------------------------------------------------
            Usuario: {request.user.first_name} {request.user.last_name}
            Correo:  {request.user.email}
            Tipo:    {sugerencia.tipo}
            ----------------------------------------------------
            
            Mensaje:
            {sugerencia.mensaje}
            """
            
            try:
                send_mail(
                    asunto,
                    mensaje_email,
                    settings.DEFAULT_FROM_EMAIL,   # Remitente (tu gmail)
                    [settings.DEFAULT_FROM_EMAIL], # Destinatario (te llega a ti mismo)
                    fail_silently=False,
                )
            except Exception as e:
                # Si falla el correo (ej. firewall), no mostramos error al usuario,
                # pero lo imprimimos en consola para que tú lo sepas.
                print(f"Error enviando correo de sugerencia: {e}")

            messages.success(request, "¡Gracias por tu feedback! Lo hemos recibido correctamente.")
            return redirect('home')
    else:
        form = SugerenciaForm()
    
    return render(request, 'dashboard/sugerencia.html', {'form': form})