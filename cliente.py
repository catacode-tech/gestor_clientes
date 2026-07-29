import re
from excepciones import EmailInvalidoError, TelefonoInvalidoError
from logger_config import logger

class Cliente:
    """Clase Base que representa a un cliente general de Solution Tech."""

    def __init__(self, cliente_id, nombre, email, telefono, direccion):
        self.id = cliente_id
        self.nombre = nombre
        self.email = email        # Utiliza el setter con validación
        self.telefono = telefono  # Utiliza el setter con validación
        self.direccion = direccion

    # Encapsulación y Validaciones
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(patron, valor):
            logger.error(f"Intento de registro con email inválido: {valor}")
            raise EmailInvalidoError(f"El email '{valor}' no tiene un formato válido.")
        self._email = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        # Valida números telefónicos de al menos 8 dígitos
        patron = r'^\+?\d{8,15}$'
        if not re.match(patron, valor):
            logger.error(f"Intento de registro con teléfono inválido: {valor}")
            raise TelefonoInvalidoError(f"El teléfono '{valor}' no es válido (debe contener entre 8 y 15 dígitos).")
        self._telefono = valor

    def obtener_tipo(self):
        return "Regular"

    def calcular_descuento(self, monto):
        """Método que será sobrescrito en las subclases (Polimorfismo)."""
        return monto

    # Métodos Especiales
    def __str__(self):
        return f"[{self.obtener_tipo()}] ID: {self.id} | Nombre: {self.nombre} | Email: {self.email}"

    def __eq__(self, otro):
        if isinstance(otro, Cliente):
            return self.id == otro.id and self.email == otro.email
        return False


# Subclases: Herencia y Polimorfismo

class ClienteRegular(Cliente):
    def obtener_tipo(self):
        return "Regular"

    def calcular_descuento(self, monto):
        return monto  # Sin descuento


class ClientePremium(Cliente):
    def __init__(self, cliente_id, nombre, email, telefono, direccion, nivel_fidelidad=1):
        super().__init__(cliente_id, nombre, email, telefono, direccion)
        self.nivel_fidelidad = nivel_fidelidad

    def obtener_tipo(self):
        return "Premium"

    def calcular_descuento(self, monto):
        # Descuento del 15%
        return monto * 0.85


class ClienteCorporativo(Cliente):
    def __init__(self, cliente_id, nombre, email, telefono, direccion, empresa, rtu):
        super().__init__(cliente_id, nombre, email, telefono, direccion)
        self.empresa = empresa
        self.rtu = rtu

    def obtener_tipo(self):
        return "Corporativo"

    def calcular_descuento(self, monto):
        # Descuento del 25% para empresas
        return monto * 0.75