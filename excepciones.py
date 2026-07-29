class ClienteError(Exception):
    """Excepción base para errores relacionados con los clientes."""
    pass

class EmailInvalidoError(ClienteError):
    """Se lanza cuando el formato del email no es válido."""
    pass

class TelefonoInvalidoError(ClienteError):
    """Se lanza cuando el formato del teléfono no es válido."""
    pass

class BaseDatosError(Exception):
    """Se lanza cuando ocurre un error en las operaciones con la base de datos."""
    pass