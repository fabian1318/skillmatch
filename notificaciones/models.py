from django.db import models
from django.conf import settings

class Notificacion(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notificaciones'
    )
    mensaje = models.CharField(max_length=255)
    leido = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # Opcional: Link para ir directo al evento (ej: /intercambios/mis-intercambios/)
    url_destino = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Notificación para {self.usuario}: {self.mensaje}"