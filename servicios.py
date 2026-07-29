from logger_config import logger

class ServicioExternoAPI:
    @staticmethod
    def validar_identidad_api(cliente_id):
        """Simula la consulta a una API externa de validación de identidad."""
        if str(cliente_id).strip() != "":
            logger.info(f"API Externa: Identidad validada con éxito para ID {cliente_id}")
            return True
        return False

    @staticmethod
    def enviar_email_bienvenida(email, nombre):
        """Simula el envío de un correo electrónico de bienvenida mediante un servicio externo."""
        logger.info(f"API Externa Email: Mensaje enviado exitosamente a {email} ({nombre})")
        print(f"--> [API EMAIL] Correo de bienvenida enviado a {email}")
        return True