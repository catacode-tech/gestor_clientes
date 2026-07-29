from gui import AppSolutionTech
from logger_config import logger

def mostrar_encabezado():
    """Muestra un mensaje de bienvenida estructurado en la consola."""
    ancho = 60
    print("=" * ancho)
    print("SOLUTION TECH - GESTOR INTELIGENTE DE CLIENTES".center(ancho))
    print("=" * ancho)
    print("  -> Estado: Cargando modulos y base de datos...")
    print("  -> Interfaz: Abriendo ventana principal...")
    print("-" * ancho + "\n")

def mostrar_despedida():
    """Muestra un mensaje de cierre estructurado en la consola."""
    ancho = 60
    print("\n" + "-" * ancho)
    print("  [OK] Cierre de sesion registrado en los logs.")
    print("=" * ancho)
    print("EJECUCION FINALIZADA CON EXITO".center(ancho))
    print("Gracias por usar Solution Tech".center(ancho))
    print("=" * ancho + "\n")

if __name__ == "__main__":
    mostrar_encabezado()
    logger.info("Iniciando la Aplicacion Solution Tech Gestor de Clientes")
    
    # Iniciar interfaz grafica
    app = AppSolutionTech()
    app.mainloop()
    
    logger.info("Aplicacion finalizada correctamente.")
    mostrar_despedida()