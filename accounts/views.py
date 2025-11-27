from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileUpdateForm
from .tokens import account_activation_token
from .models import CustomUser, Habilidad

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            # CORRECCIÓN: Copiar email a username para evitar error de integridad
            #user.username = user.email 
            
            # HU-29: Cuenta inactiva hasta validar correo
            user.is_active = False 
            user.estado_cuenta = 'PendienteActivacion'
            user.save()

            # Preparar correo de activación
            current_site = get_current_site(request)
            mail_subject = 'Activa tu cuenta SkillMatch'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            try:
                email.send()
                messages.success(request, 'Por favor confirma tu correo electrónico para completar el registro.')
            except Exception as e:
                messages.error(request, f'Error al enviar correo: {e}')
                
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        # Activar usuario
        user.is_active = True
        user.estado_cuenta = 'Activo'
        user.save()
        
        # MEJORA UX: Iniciar sesión automáticamente
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        messages.success(request, '¡Cuenta activada correctamente! Bienvenido a SkillMatch.')
        return redirect('home') # Redirige directo al Dashboard
    else:
        messages.error(request, 'El enlace de activación es inválido o ha expirado. Intenta registrarte nuevamente o contacta soporte.')
        return redirect('login')

@login_required
def profile(request):
    """Vista para ver mi propio perfil (HU-23 parcial)"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
@login_required
def edit_profile(request):
    """Vista para editar perfil y habilidades (HU-2, HU-6, HU-8)"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            # Guardar datos básicos y relaciones M2M (habilidades seleccionadas)
            form.save()
            
            # NOTA: Se eliminó la creación dinámica de habilidades.
            # Ahora solo se seleccionan del pool existente.

            messages.success(request, '¡Tu perfil ha sido actualizado correctamente!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def catalogo_insignias(request):
    """Ver catálogo de insignias (HU-4)."""
    # Importación diferida para evitar ciclos si fuera necesario, o asegurar que el modelo existe
    from .models import Insignia 
    
    filtro = request.GET.get('filtro', 'todas')
    todas_insignias = Insignia.objects.all()
    mis_insignias = request.user.insignias.all()
    
    if filtro == 'obtenidas':
        insignias_mostrar = mis_insignias
    elif filtro == 'faltantes':
        insignias_mostrar = todas_insignias.difference(mis_insignias)
    else:
        insignias_mostrar = todas_insignias

    context = {
        'insignias': insignias_mostrar,
        'mis_ids': list(mis_insignias.values_list('id', flat=True)),
        'filtro_actual': filtro
    }
    return render(request, 'accounts/badges_catalog.html', context)