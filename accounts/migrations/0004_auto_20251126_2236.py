# BUSCA EL ARCHIVO GENERADO EN accounts/migrations/ Y REEMPLAZA SU CONTENIDO
# El nombre del archivo será algo como 0002_auto_2023...py o 0003_...

from django.db import migrations

def cargar_datos_iniciales(apps, schema_editor):
    # Obtenemos los modelos históricos (así evitamos errores si el modelo cambia en el futuro)
    Habilidad = apps.get_model('accounts', 'Habilidad')
    Insignia = apps.get_model('accounts', 'Insignia')

    # 1. LISTA DE HABILIDADES
    pool_habilidades = [
        # Ciencias Básicas
        "Matemática I", "Matemática II", "Álgebra", "Cálculo", "Estadística", "Física Mecánica",
        # Idiomas
        "Inglés Básico", "Inglés Intermedio", "Inglés Avanzado", "Inglés Técnico",
        # Informática
        "Python", "JavaScript", "Java", "C++", "C#", "SQL / Bases de Datos", 
        "Desarrollo Web (HTML/CSS)", "React", "Django", "Soporte de Hardware", "Redes CCNA",
        # Administración
        "Contabilidad", "Finanzas", "Marketing Digital", "Recursos Humanos", "Excel Avanzado",
        # Otros
        "Repostería", "Cocina Chilena", "Mecánica Automotriz", "Electricidad Domiciliaria",
        "Liderazgo", "Oratoria"
    ]

    for nombre in pool_habilidades:
        Habilidad.objects.get_or_create(nombre=nombre)

    # 2. LISTA DE INSIGNIAS (Gamificación)
    Insignia.objects.get_or_create(
        nombre="Iniciador",
        defaults={
            'descripcion': 'Otorgada por completar tu primer intercambio.',
            'icono': 'bi-rocket-takeoff',
            'requisito': 'Completar 1 intercambio'
        }
    )
    Insignia.objects.get_or_create(
        nombre="Veterano",
        defaults={
            'descripcion': 'Usuario experimentado con trayectoria.',
            'icono': 'bi-shield-check',
            'requisito': 'Completar 5 intercambios'
        }
    )
    Insignia.objects.get_or_create(
        nombre="Mentor Estrella",
        defaults={
            'descripcion': 'Reconocimiento a la excelencia en enseñanza.',
            'icono': 'bi-star-fill',
            'requisito': 'Promedio de 4.5 estrellas en 3+ sesiones'
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        # CORRECCIÓN: Apuntamos a la migración 0003 que creó la tabla Insignia
        # El nombre exacto viene de tu mensaje de error
        ('accounts', '0003_insignia_customuser_reputacion_customuser_insignias'), 
    ]

    operations = [
        migrations.RunPython(cargar_datos_iniciales),
    ]