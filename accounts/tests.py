from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserTests(TestCase):
    
    def test_crear_usuario_inacap_exitoso(self):
        """Prueba que un correo @inacap.cl se crea correctamente."""
        user = CustomUser.objects.create(email='alumno@inacap.cl', password='password123')
        self.assertEqual(user.email, 'alumno@inacap.cl')
        # Verificar que se copió el email al username
        self.assertEqual(user.username, 'alumno@inacap.cl')

    def test_crear_usuario_externo_fallido(self):
        """Prueba que un correo @gmail.com falla la validación."""
        user = CustomUser(email='hacker@gmail.com', password='password123')
        
        # Intentar validar manualmente (como lo hace el ModelForm)
        with self.assertRaises(ValidationError):
            user.full_clean() # Esto dispara los validadores del modelo