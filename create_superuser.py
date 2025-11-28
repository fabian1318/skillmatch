import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skillmatch.settings")
django.setup()

from django.contrib.auth import get_user_model

def create_admin():
    User = get_user_model()
    
    # Leer credenciales desde Variables de Entorno (Render)
    email = os.getenv('DJANGO_SUPERUSER_EMAIL')
    password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

    if email and password:
        if not User.objects.filter(email=email).exists():
            print(f"Creando superusuario {email}...")
            User.objects.create_superuser(
                username=email,  # Usamos el email como username también
                email=email,
                password=password,
                first_name="Admin",
                last_name="Render"
            )
            print("¡Superusuario creado exitosamente!")
        else:
            print("El superusuario ya existe. Omitiendo creación.")
    else:
        print("No se encontraron variables de entorno para crear superusuario.")

if __name__ == "__main__":
    create_admin()