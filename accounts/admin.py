from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Habilidad,Insignia

# Configuración para ver el CustomUser en el admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'carrera', 'rol', 'is_active')
    list_filter = ('rol', 'is_active', 'carrera')
    ordering = ('email',)
    
    # Agregamos nuestros campos personalizados al fieldset de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información Académica', {'fields': ('carrera', 'rol', 'estado_cuenta')}),
        ('Perfil', {'fields': ('biografia', 'habilidades_ofrecidas', 'habilidades_buscadas')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información Académica', {'fields': ('carrera', 'rol', 'email')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Habilidad)
admin.site.register(Insignia)