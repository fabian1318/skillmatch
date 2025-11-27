from django.db import models
from django.conf import settings

class Sugerencia(models.Model):
    TIPOS = [
        ('Sugerencia', 'Sugerencia'),
        ('Error', 'Reporte de Error'),
        ('Felicitacion', 'Felicitación'),
        ('Otro', 'Otro'),
    ]
    
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sugerencias'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS, default='Sugerencia')
    mensaje = models.TextField(verbose_name="Tu mensaje")
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False, verbose_name="Leído por Admin")

    def __str__(self):
        return f"{self.tipo} de {self.usuario.first_name} ({self.fecha.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Sugerencia / Feedback"
        verbose_name_plural = "Buzón de Sugerencias"
        ordering = ['-fecha']