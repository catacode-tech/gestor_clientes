import unittest
import os
from cliente import ClienteRegular
from base_datos import GestorBaseDatos
from excepciones import BaseDatosError

class TestGestorBaseDatos(unittest.TestCase):
    def setUp(self):
        self.db_test = "test_app_data.db"
        self.json_test = "test_clientes.json"
        self.csv_test = "test_clientes.csv"
        self.gestor = GestorBaseDatos(db_path=self.db_test, json_path=self.json_test, csv_path=self.csv_test)

    def tearDown(self):
        for archivo in [self.db_test, self.json_test, self.csv_test]:
            if os.path.exists(archivo):
                os.remove(archivo)

    def test_guardar_y_obtener_cliente(self):
        cliente = ClienteRegular("101", "Laura Gomez", "laura@test.com", "12345678", "Av. Principal 123")
        self.gestor.guardar_cliente(cliente)
        
        clientes = self.gestor.obtener_todos()
        self.assertEqual(len(clientes), 1)
        self.assertEqual(clientes[0].id, "101")
        self.assertEqual(clientes[0].nombre, "Laura Gomez")

    def test_eliminar_cliente_existente(self):
        cliente = ClienteRegular("102", "Carlos Perez", "carlos@test.com", "87654321", "Calle 45")
        self.gestor.guardar_cliente(cliente)
        self.gestor.eliminar_cliente("102")
        
        clientes = self.gestor.obtener_todos()
        self.assertEqual(len(clientes), 0)

    def test_eliminar_cliente_inexistente_lanza_excepcion(self):
        with self.assertRaises(BaseDatosError):
            self.gestor.eliminar_cliente("9999")

    def test_exportar_csv(self):
        cliente = ClienteRegular("103", "Ana Silva", "ana@test.com", "11223344", "Pasaje Central")
        self.gestor.guardar_cliente(cliente)
        self.gestor.exportar_csv()
        
        self.assertTrue(os.path.exists(self.csv_test))

if __name__ == "__main__":
    unittest.main()