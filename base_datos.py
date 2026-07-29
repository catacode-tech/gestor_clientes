import sqlite3
import json
import csv
import os
from cliente import ClienteRegular, ClientePremium, ClienteCorporativo
from excepciones import BaseDatosError
from logger_config import logger

class GestorBaseDatos:
    def __init__(self, db_path="app_data.db", json_path="clientes.json", csv_path="clientes.csv"):
        self.db_path = db_path
        self.json_path = json_path
        self.csv_path = csv_path
        self._inicializar_bd()

    def _inicializar_bd(self):
        """Crea la tabla en SQLite si no existe."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS clientes (
                        id TEXT PRIMARY KEY,
                        nombre TEXT NOT NULL,
                        email TEXT NOT NULL,
                        telefono TEXT NOT NULL,
                        direccion TEXT NOT NULL,
                        tipo TEXT NOT NULL
                    )
                """)
                conn.commit()
            logger.info("Base de datos SQLite inicializada correctamente.")
        except sqlite3.Error as e:
            logger.error(f"Error al inicializar la base de datos: {e}")
            raise BaseDatosError(f"No se pudo inicializar la base de datos: {e}")

    def guardar_cliente(self, cliente):
        """Guarda o actualiza un cliente en SQLite y sincroniza el archivo JSON."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO clientes (id, nombre, email, telefono, direccion, tipo)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    cliente.id,
                    cliente.nombre,
                    cliente.email,
                    cliente.telefono,
                    cliente.direccion,
                    cliente.obtener_tipo()
                ))
                conn.commit()
            logger.info(f"Cliente con ID {cliente.id} guardado correctamente.")
            self._sincronizar_json()
        except sqlite3.Error as e:
            logger.error(f"Error al guardar cliente en SQLite: {e}")
            raise BaseDatosError(f"Error al guardar cliente en la base de datos: {e}")

    def eliminar_cliente(self, cliente_id):
        """Elimina un cliente por su ID en SQLite y actualiza el JSON."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
                if cursor.rowcount == 0:
                    raise BaseDatosError(f"No se encontró un cliente con el ID: {cliente_id}")
                conn.commit()
            logger.info(f"Cliente con ID {cliente_id} eliminado de SQLite.")
            self._sincronizar_json()
        except sqlite3.Error as e:
            logger.error(f"Error al eliminar cliente {cliente_id}: {e}")
            raise BaseDatosError(f"Error al eliminar cliente de la base de datos: {e}")

    def obtener_todos(self):
        """Recupera todos los registros de SQLite y retorna objetos del modelo Cliente."""
        clientes = []
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, nombre, email, telefono, direccion, tipo FROM clientes")
                filas = cursor.fetchall()

                for fila in filas:
                    c_id, nombre, email, telefono, direccion, tipo = fila
                    
                    # Reconstrucción del objeto según su tipo
                    if "Premium" in tipo:
                        cliente = ClientePremium(c_id, nombre, email, telefono, direccion)
                    elif "Corporativo" in tipo:
                        cliente = ClienteCorporativo(c_id, nombre, email, telefono, direccion, "TechCorp", "RTU-123")
                    else:
                        cliente = ClienteRegular(c_id, nombre, email, telefono, direccion)
                    
                    clientes.append(cliente)
            return clientes
        except sqlite3.Error as e:
            logger.error(f"Error al recuperar clientes de SQLite: {e}")
            raise BaseDatosError(f"Error al leer datos desde SQLite: {e}")

    def _sincronizar_json(self):
        """Respalda el contenido actual de SQLite en un archivo JSON."""
        try:
            clientes = self.obtener_todos()
            data = [
                {
                    "id": c.id,
                    "nombre": c.nombre,
                    "email": c.email,
                    "telefono": c.telefono,
                    "direccion": c.direccion,
                    "tipo": c.obtener_tipo()
                }
                for c in clientes
            ]
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            logger.info("Respaldo JSON sincronizado exitosamente.")
        except Exception as e:
            logger.error(f"Error al sincronizar el archivo JSON: {e}")

    def exportar_csv(self):
        """Exporta la lista de clientes a un archivo de formato CSV."""
        try:
            clientes = self.obtener_todos()
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["ID", "Nombre", "Email", "Teléfono", "Dirección", "Tipo"])
                for c in clientes:
                    writer.writerow([c.id, c.nombre, c.email, c.telefono, c.direccion, c.obtener_tipo()])
            logger.info(f"Reporte exportado exitosamente a {self.csv_path}.")
        except Exception as e:
            logger.error(f"Error al exportar CSV: {e}")
            raise BaseDatosError(f"Error al generar el archivo CSV: {e}")