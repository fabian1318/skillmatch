from django.contrib import admin
from .models import Sugerencia

@admin.register(Sugerencia)
class SugerenciaAdmin(admin.ModelAdmin):
    list_display = ('tipo', 'usuario', 'fecha', 'leido')
    list_filter = ('tipo', 'leido', 'fecha')
    search_fields = ('mensaje', 'usuario__email')
    list_editable = ('leido',) # Para marcar como leído rápido desde la lista