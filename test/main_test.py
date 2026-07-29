import unittest
from unittest.mock import patch
import main

class TestMainProgram(unittest.TestCase):
    @patch("builtins.print")
    def test_mostrar_encabezado(self, mock_print):
        main.mostrar_encabezado()
        mock_print.assert_called()

    @patch("builtins.print")
    def test_mostrar_despedida(self, mock_print):
        main.mostrar_despedida()
        mock_print.assert_called()

    @patch("main.AppSolutionTech")
    @patch("main.mostrar_encabezado")
    @patch("main.mostrar_despedida")
    def test_ejecucion_main(self, mock_despedida, mock_encabezado, MockApp):
        mock_app_instance = MockApp.return_value
        
        # Simulación de la ejecución principal
        main.mostrar_encabezado()
        app = main.AppSolutionTech()
        app.mainloop()
        main.mostrar_despedida()

        mock_encabezado.assert_called_once()
        mock_app_instance.mainloop.assert_called_once()
        mock_despedida.assert_called_once()

if __name__ == "__main__":
    unittest.main()