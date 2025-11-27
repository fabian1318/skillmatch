🎓 SkillMatch - Plataforma de Intercambio de Habilidades

SkillMatch es una plataforma web diseñada para la comunidad estudiantil de INACAP Sede Maipú. Permite a los alumnos encontrar mentores, ofrecer sus conocimientos y gestionar ciclos de aprendizaje colaborativo (Trueque de Habilidades).

🚀 Características Principales

Autenticación Segura: Registro exclusivo con correo institucional (@inacap.cl) y activación por token.

Perfiles Académicos: Gestión de habilidades ("Qué ofrezco" vs "Qué busco") y biografía.

Motor de Búsqueda: Filtros por habilidad y carrera.

Ciclo de Intercambio Completo: Solicitud → Aceptación → En Progreso → Finalizado.

Gamificación: Sistema de reputación (estrellas) e insignias automáticas por logros.

Seguridad: Sistema de reportes de conducta y buzón de sugerencias.

🛠️ Tecnologías Utilizadas

Backend: Python 3.11+, Django 5.0

Base de Datos: PostgreSQL 15+

Frontend: HTML5, Bootstrap 5.3 (Diseño responsivo tipo Dashboard)

Email: SMTP (Gmail/Outlook) para notificaciones transaccionales.

⚙️ Instalación y Despliegue Local

Sigue estos pasos para levantar el proyecto en tu máquina:

1. Clonar y preparar entorno

# Clonar repositorio (Si aplica)
git clone <url-del-repo>
cd skillmatch

# Crear entorno virtual
python -m venv venv

# Activar entorno
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt


2. Configuración de Variables de Entorno

Crea un archivo .env en la raíz (junto a manage.py) con el siguiente contenido:

DEBUG=True
SECRET_KEY=tu_clave_secreta_segura
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de Datos
DB_NAME=skillmatch_db
DB_USER=skillmatch_user
DB_PASSWORD=password123
DB_HOST=localhost
DB_PORT=5432

# Correo (Ejemplo Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_contraseña_de_aplicacion


3. Base de Datos y Migraciones

Asegúrate de tener PostgreSQL corriendo y la base de datos creada. Si es la primera vez, asegúrate de que tu usuario tenga permisos CREATEDB si planeas correr tests.

python manage.py makemigrations
python manage.py migrate


4. Crear Superusuario (Admin)

Para acceder al panel de control (/admin):

python manage.py createsuperuser
# Usa un correo institucional ficticio si es necesario (ej: admin@inacap.cl)


5. Cargar Datos Iniciales (Insignias)

Para que el sistema de gamificación funcione desde el inicio, puedes ejecutar este script en la shell de Django:

python manage.py shell


# Dentro de la shell interactiva:
from accounts.models import Insignia
Insignia.objects.get_or_create(nombre="Iniciador", defaults={'icono':'bi-rocket-takeoff', 'requisito':'Completar tu primer intercambio.', 'descripcion': 'Otorgada por completar tu primer intercambio.'})
Insignia.objects.get_or_create(nombre="Veterano", defaults={'icono':'bi-shield-check', 'requisito':'Completar 5 intercambios.', 'descripcion': 'Usuario experimentado con trayectoria.'})
Insignia.objects.get_or_create(nombre="Mentor Estrella", defaults={'icono':'bi-star-fill', 'requisito':'Promedio de 4.5 estrellas en 3+ sesiones.', 'descripcion': 'Reconocimiento a la excelencia en enseñanza.'})
exit()


6. Ejecutar Servidor

python manage.py runserver


Visita http://127.0.0.1:8000/ en tu navegador.

🧪 Pruebas Automatizadas

El proyecto incluye pruebas unitarias para validar la lógica crítica (como el registro de correos institucionales).

Para ejecutar los tests:

python manage.py test accounts


Nota: Si recibes un error de permisos en la base de datos, asegúrate de dar permisos de creación de DB a tu usuario en Postgres: ALTER USER skillmatch_user CREATEDB;

👥 Autores y Créditos

Proyecto desarrollado para la asignatura Proyecto Integrado - INACAP Sede Maipú.

Equipo de Desarrollo:

Nicolas Caerols

Fabian Esquivel

Daniela Macaya

Sebastián Rodríguez

Docente: Manuel Rojas
Fecha: Noviembre 2025