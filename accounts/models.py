from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_dominio_inacap(value):
    dominio = value.split('@')[1]
    dominios_permitidos = ['inacap.cl', 'inacapmail.cl']
    if dominio not in dominios_permitidos:
        raise ValidationError(
            _('El correo debe ser institucional (@inacap.cl o @inacapmail.cl).'),
            params={'value': value},
        )

# --- NUEVO MODELO: HABILIDAD ---
class Habilidad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name='Nombre de la Habilidad')
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción')
    
    # Contador de popularidad (opcional, útil para ordenar)
    veces_solicitada = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'
        ordering = ['nombre']

class Insignia(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField()
    icono = models.CharField(max_length=50, default='bi-award') # Para usar iconos Bootstrap (bi-star, etc.)
    requisito = models.CharField(max_length=255, help_text="Ej. Completar 5 intercambios")
    
    def __str__(self):
        return self.nombre

class CustomUser(AbstractUser):
    ROL_CHOICES = [
        ('Estudiante', 'Estudiante'),
        ('Administrador', 'Administrador'),
    ]
    
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('PendienteActivacion', 'Pendiente de Activación'),
        ('Bloqueado', 'Bloqueado'),
    ]
    
    email = models.EmailField(
        _('correo institucional'), 
        unique=True,
        validators=[validar_dominio_inacap],
        error_messages={
            'unique': _("Ya existe un usuario registrado con este correo."),
        }
    )
    
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='Estudiante')
    estado_cuenta = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PendienteActivacion')
    carrera = models.CharField(max_length=50, blank=True, null=True)
    
    # Campos de Biografía (HU-2)
    biografia = models.TextField(blank=True, null=True, verbose_name='Sobre mí')

    # NUEVA RELACIÓN (HU-7)
    insignias = models.ManyToManyField(Insignia, blank=True, related_name='ganadores')
    
    # Campo de Reputación (Promedio de estrellas) - HU-3
    reputacion = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    # --- NUEVAS RELACIONES (HU-6) ---
    # related_name permite buscar a la inversa: Habilidad.usuarios_que_ofrecen.all()
    habilidades_ofrecidas = models.ManyToManyField(
        Habilidad, 
        related_name='usuarios_ofrecen', 
        blank=True,
        verbose_name='Habilidades que ofrezco'
    )
    
    habilidades_buscadas = models.ManyToManyField(
        Habilidad, 
        related_name='usuarios_buscan', 
        blank=True,
        verbose_name='Habilidades que busco'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        # Lógica de seguridad:
        # Si no se especificó un username, usamos el email automáticamente.
        # Esto garantiza que nunca haya errores de unicidad por username vacío.
        if not self.username and self.email:
            self.username = self.email
            
        super().save(*args, **kwargs)
        
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'