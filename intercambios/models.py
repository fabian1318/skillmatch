from django.db import models
from django.conf import settings
from accounts.models import Habilidad

class Intercambio(models.Model):
    # Estados definidos en el Diccionario de Datos
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('Aceptado', 'Aceptado'),
        ('EnProgreso', 'En Progreso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
        ('Rechazado', 'Rechazado'),
    ]

    solicitante = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='solicitudes_enviadas'
    )
    receptor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='solicitudes_recibidas'
    )
    
    # La habilidad que el solicitante QUIERE aprender (del receptor)
    habilidad_solicitada = models.ForeignKey(
        Habilidad, 
        on_delete=models.CASCADE, 
        related_name='intercambios_como_solicitada'
    )
    
    # La habilidad que el solicitante OFRECE a cambio (suya)
    habilidad_ofrecida = models.ForeignKey(
        Habilidad, 
        on_delete=models.CASCADE, 
        related_name='intercambios_como_ofrecida'
    )

    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    
    # Fechas de auditoría
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.solicitante} solicita {self.habilidad_solicitada} a {self.receptor}"

    class Meta:
        ordering = ['-fecha_creacion']

class Resena(models.Model):
    # CAMBIO: De OneToOneField a ForeignKey
    intercambio = models.ForeignKey(Intercambio, on_delete=models.CASCADE, related_name='resenas')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resenas_hechas')
    calificado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='resenas_recibidas')
    estrellas = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        # RESTRICCIÓN: Un autor solo puede hacer una reseña por intercambio
        unique_together = ('intercambio', 'autor')

    def __str__(self):
        return f"Reseña de {self.autor} a {self.calificado} ({self.estrellas}★)"

class Reporte(models.Model):
    MOTIVOS = [
        ('Conducta', 'Conducta inapropiada'),
        ('Ausencia', 'No se presentó'),
        ('Spam', 'Spam o publicidad'),
        ('Otro', 'Otro'),
    ]
    
    denunciante = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reportes_enviados')
    denunciado = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reportes_recibidos', null=True, blank=True)
    intercambio = models.ForeignKey(Intercambio, on_delete=models.SET_NULL, null=True, blank=True)
    motivo = models.CharField(max_length=20, choices=MOTIVOS)
    descripcion = models.TextField()
    resuelto = models.BooleanField(default=False)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reporte {self.id} - {self.motivo}"