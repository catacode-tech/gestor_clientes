import unittest
from unittest.mock import MagicMock, patch
import tkinter as tk
from gui import AppSolutionTech
from cliente import ClienteRegular

class TestAppSolutionTech(unittest.TestCase):
    @patch("gui.GestorBaseDatos")
    def setUp(self, MockGestorBD):
        # Evitar crear archivos de BD reales durante las pruebas de la GUI
        self.mock_db = MockGestorBD.return_value
        self.mock_db.obtener_todos.return_value = [
            ClienteRegular("1", "Test User", "test@mail.com", "12345", "Direccion Test")
        ]
        
        self.app = AppSolutionTech()
        # Ocultar la ventana de Tkinter durante la ejecución de los tests
        self.app.withdraw()

    def tearDown(self):
        self.app.destroy()

    def test_inicializacion_componentes(self):
        self.assertEqual(self.app.title(), "Solution Tech - Gestor Inteligente de Clientes")
        self.assertIsNotNone(self.app.ent_id)
        self.assertIsNotNone(self.app.ent_nombre)
        self.assertIsNotNone(self.app.tabla)

    def test_limpiar_campos(self):
        self.app.ent_id.insert(0, "999")
        self.app.ent_nombre.insert(0, "Nombre Pruebas")
        
        self.app.limpiar_campos()
        
        self.assertEqual(self.app.ent_id.get(), "")
        self.assertEqual(self.app.ent_nombre.get(), "")
        self.assertEqual(self.app.combo_tipo.get(), "Regular")

    def test_cargar_tabla(self):
        self.app.cargar_tabla()
        items = self.app.tabla.get_children()
        self.assertEqual(len(items), 1)

if __name__ == "__main__":
    unittest.main()