# Solution Tech — Gestor Inteligente de Clientes

Sistema de gestión de clientes desarrollado en Python aplicando Programación Orientada a Objetos (POO), persistencia de datos relacional y no relacional, integración con APIs y una interfaz gráfica de usuario (GUI) con Tkinter.

---

## Aspectos Técnicos y Arquitectura

El proyecto sigue una arquitectura por capas para garantizar el desacoplamiento y facilitar el mantenimiento:

1. **Capa de Modelo (`cliente.py`)**: Define la jerarquía de clases utilizando POO. Aplica herencia y polimorfismo mediante una clase base `Cliente` y subclases especificas (`ClienteRegular`, `ClientePremium`, `ClienteCorporativo`).
2. **Capa de Persistencia (`base_datos.py`)**: Encargada de gestionar la base de datos SQLite (`app_data.db`), sincronizar datos en JSON y exportar reportes en CSV.
3. **Capa de Servicios (`servicios.py`)**: Simula servicios externos de verificación de identidad mediante API REST e integración de correo electrónico.
4. **Capa de Interfaz Gráfica (`gui.py`)**: Desarrollada con Tkinter y `ttk`, proporcionando un formulario intuitivo, tabla dinámica de visualización de datos y manejo de eventos.
5. **Manejo de Excepciones y Logs (`excepciones.py`, `logger_config.py`)**: Excepciones personalizadas para el control de errores de dominio y registro centralizado de eventos del sistema.

---

## Diagrama de Clases UML

```mermaid
classDiagram
    %% --- cliente.py ---
    class Cliente {
        <<Abstract>>
        +str id
        +str nombre
        +str email
        +str telefono
        +str direccion
        +obtener_tipo()* str
    }

    class ClienteRegular {
        +obtener_tipo() str
    }

    class ClientePremium {
        +obtener_tipo() str
    }

    class ClienteCorporativo {
        +str empresa
        +str rtu
        +obtener_tipo() str
    }

    Cliente <|-- ClienteRegular
    Cliente <|-- ClientePremium
    Cliente <|-- ClienteCorporativo

    %% --- base_datos.py ---
    class GestorBaseDatos {
        -str db_path
        -str json_path
        -str csv_path
        -_inicializar_bd()
        +guardar_cliente(cliente: Cliente)
        +eliminar_cliente(cliente_id: str)
        +obtener_todos() list~Cliente~
        +exportar_csv()
        -_sincronizar_json()
    }

    %% --- servicios.py ---
    class ServicioExternoAPI {
        +validar_identidad_api(c_id: str)$ bool
        +enviar_email_bienvenida(email: str, nombre: str)$ bool
    }

    %% --- excepciones.py ---
    class ClienteError {
        <<Exception>>
    }

    class BaseDatosError {
        <<Exception>>
    }

    %% --- gui.py ---
    class AppSolutionTech {
        +GestorBaseDatos db
        +Entry ent_id
        +Entry ent_nombre
        +Entry ent_email
        +Entry ent_telefono
        +Entry ent_direccion
        +Combobox combo_tipo
        +Treeview tabla
        +crear_componentes()
        +guardar_cliente()
        +eliminar_cliente()
        +exportar_csv()
        +cargar_tabla()
        +seleccionar_registro(event)
        +limpiar_campos()
    }

    %% --- main.py ---
    class MainScript {
        <<Script>>
        +mostrar_encabezado()
        +mostrar_despedida()
    }

    %% --- Relaciones del Sistema ---
    MainScript ..> AppSolutionTech : instancia
    AppSolutionTech --> GestorBaseDatos : usa
    AppSolutionTech ..> ServicioExternoAPI : consulta
    AppSolutionTech ..> Cliente : gestiona
    GestorBaseDatos ..> Cliente : persiste
    GestorBaseDatos ..> BaseDatosError : lanza
    AppSolutionTech ..> ClienteError : maneja
    AppSolutionTech ..> BaseDatosError : maneja
```
## Capturas de Pantalla y Demostración

### Interfaz Gráfica (GUI)
![Pantalla Principal](docs/interfaz.png)

### Ejecución por Consola
![Salida de Terminal](docs/terminal.png)

### Organización de archivos del proyecto
![Salida de Terminal](docs/organizacion_archivos_proyecto.png)

---

## Fragmentos de Código Destacados

### Polimorfismo en la Jerarquía de Clientes (`cliente.py`)
```python
class ClienteRegular(Cliente):
    def obtener_tipo(self) -> str:
        return "Regular"

class ClientePremium(Cliente):
    def obtener_tipo(self) -> str:
        return "Premium (Descuento 10%)"
```
## Repo Git
https://github.com/catacode-tech/gestor_clientes

