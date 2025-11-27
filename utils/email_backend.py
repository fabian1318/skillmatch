import ssl
from django.core.mail.backends.smtp import EmailBackend as SmtpEmailBackend

class CustomEmailBackend(SmtpEmailBackend):
    """
    Backend de correo personalizado para evitar errores de SSL en desarrollo local (Windows).
    Ignora la verificación del certificado (ssl.CERT_NONE).
    """
    def open(self):
        if self.connection:
            return False
        try:
            # CORRECCIÓN: Construimos connection_params manualmente como lo hace Django internamente
            connection_params = {}
            if getattr(self, 'timeout', None) is not None:
                connection_params['timeout'] = self.timeout
            if getattr(self, 'local_hostname', None) is not None:
                connection_params['local_hostname'] = self.local_hostname
            if getattr(self, 'source_address', None) is not None:
                connection_params['source_address'] = self.source_address

            # Creamos la conexión usando los parámetros construidos
            self.connection = self.connection_class(self.host, self.port, **connection_params)
            
            # Si usamos TLS (Gmail usa puerto 587 + TLS), creamos un contexto permisivo
            if self.use_tls:
                # Crear un contexto que no verifique el hostname ni el certificado
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # Iniciar TLS con nuestro contexto "relajado"
                self.connection.starttls(context=context)
            
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            
            return True
        except OSError:
            if not self.fail_silently:
                raise