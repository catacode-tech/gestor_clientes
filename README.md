# Solution Tech — Gestor Inteligente de Clientes

Sistema de gestión de clientes desarrollado en Python 3 bajo un esquema modular por capas. La solución aplica los principios avanzados de Programación Orientada a Objetos (POO), persistencia de datos relacional, servicios externos y una interfaz gráfica de usuario (GUI) con Tkinter.

---

## Aspectos Técnicos y Arquitectura

El proyecto sigue una arquitectura por capas para garantizar el desacoplamiento y facilitar el mantenimiento:

<u>1. Capa de Modelo (`cliente.py`)</u>: Define la jerarquía de clases utilizando POO. Aplica herencia y polimorfismo mediante una clase base `Cliente` y subclases especificas (`ClienteRegular`, `ClientePremium`, `ClienteCorporativo`).
<u>2. Capa de Persistencia (`base_datos.py`)</u>: Encargada de gestionar la base de datos SQLite (`app_data.db`), sincronizar datos en JSON y exportar reportes en CSV.
<u>3. Capa de Servicios (`servicios.py`)</u>: Simula servicios externos de verificación de identidad mediante API REST e integración de correo electrónico.
<u>4. Capa de Interfaz Gráfica (`gui.py`)</u>: Desarrollada con Tkinter y `ttk`, proporcionando un formulario intuitivo, tabla dinámica de visualización de datos y manejo de eventos.
<u>5. Manejo de Excepciones y Logs (`excepciones.py`, `logger_config.py`)</u>: Excepciones personalizadas para el control de errores de dominio y registro centralizado de eventos del sistema.

---

## Diagrama de Clases UML

```mermaid
classDiagram
    direction TB

    %% Capa de Modelo
    namespace Capa_Modelo {
        class Cliente {
            -id
            -nombre
            -_email
            -_telefono
            -direccion
            +email : property
            +telefono : property
            +obtener_tipo() str
            +calcular_descuento(monto) float
            +__str__() str
            +__eq__(otro) bool
        }

        class ClienteRegular {
            +obtener_tipo() str
            +calcular_descuento(monto) float
        }

        class ClientePremium {
            +nivel_fidelidad : int
            +obtener_tipo() str
            +calcular_descuento(monto) float
        }

        class ClienteCorporativo {
            +empresa : str
            +rtu : str
            +obtener_tipo() str
            +calcular_descuento(monto) float
        }
    }

    %% Capa de Persistencia
    namespace Capa_Persistencia {
        class BaseDatos {
            -db_path : str
            +conectar()
            +guardar_cliente(cliente)
            +obtener_clientes() list
            +exportar_json(ruta)
            +exportar_csv(ruta)
        }
    }

    %% Capa de Servicios
    namespace Capa_Servicios {
        class ServicioExterno {
            +verificar_identidad(rtu) bool
            +enviar_correo_bienvenida(email)
        }
    }

    %% Capa de Presentación
    namespace Capa_Presentacion {
        class InterfazGUI {
            -master
            -treeview
            +crear_widgets()
            +agregar_cliente_gui()
            +actualizar_tabla()
        }

        class Main {
            +main()
        }
    }

    %% Soporte Transversal
    namespace Soporte_Transversal {
        class EmailInvalidoError {
        }
        class TelefonoInvalidoError {
        }
        class LoggerConfig {
            +logger
        }
    }

    %% Relaciones de Herencia (Modelo)
    Cliente <|-- ClienteRegular
    Cliente <|-- ClientePremium
    Cliente <|-- ClienteCorporativo

    %% Relaciones entre capas
    Main ..> InterfazGUI : inicia
    InterfazGUI --> BaseDatos : utiliza
    InterfazGUI --> ServicioExterno : consulta
    InterfazGUI ..> Cliente : administra
    BaseDatos ..> Cliente : persiste
    
    %% Uso de excepciones y logs
    Cliente ..> EmailInvalidoError : lanza
    Cliente ..> TelefonoInvalidoError : lanza
    Cliente ..> LoggerConfig : registra
```
## Capturas de Pantalla y Demostración

### Interfaz Gráfica (GUI)
![Pantalla Principal](docs/interfaz.png)

### Ejecución por Consola
![Salida de Terminal](docs/terminal.png)

### Organización de archivos del proyecto
![Salida de Terminal](docs/organizacion_archivos_proyecto.png)

---
```
## Repo Git
https://github.com/catacode-tech/gestor_clientes

