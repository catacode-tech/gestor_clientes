import sys
import os

# Agrega la carpeta del proyecto a las rutas de Python para evitar errores de módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import ttk, messagebox
from cliente import ClienteRegular, ClientePremium, ClienteCorporativo
from base_datos import GestorBaseDatos
from servicios import ServicioExternoAPI
from excepciones import ClienteError, BaseDatosError
from logger_config import logger

class AppSolutionTech(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Solution Tech - Gestor Inteligente de Clientes")
        self.geometry("750x550")
        
        self.db = GestorBaseDatos()
        self.crear_componentes()
        self.cargar_tabla()

    def crear_componentes(self):
        # Título
        lbl_titulo = tk.Label(self, text="Gestor Inteligente de Clientes", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Formulario (Corregido con padx y pady)
        frame_form = tk.LabelFrame(self, text=" Datos del Cliente ", padx=10, pady=10)
        frame_form.pack(fill="x", padx=15, pady=5)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.ent_id = tk.Entry(frame_form)
        self.ent_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Nombre:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.ent_nombre = tk.Entry(frame_form)
        self.ent_nombre.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(frame_form, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.ent_email = tk.Entry(frame_form)
        self.ent_email.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Teléfono:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.ent_telefono = tk.Entry(frame_form)
        self.ent_telefono.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(frame_form, text="Dirección:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.ent_direccion = tk.Entry(frame_form)
        self.ent_direccion.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(frame_form, text="Tipo:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.combo_tipo = ttk.Combobox(frame_form, values=["Regular", "Premium", "Corporativo"], state="readonly")
        self.combo_tipo.set("Regular")
        self.combo_tipo.grid(row=2, column=3, padx=5, pady=2)

        # Botones de Acción
        frame_btn = tk.Frame(self)
        frame_btn.pack(fill="x", padx=15, pady=10)

        tk.Button(frame_btn, text="Guardar / Actualizar", bg="#4CAF50", fg="black", command=self.guardar_cliente).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Eliminar Cliente", bg="#f44336", fg="black", command=self.eliminar_cliente).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Exportar a CSV", bg="#2196F3", fg="black", command=self.exportar_csv).pack(side="left", padx=5)
        tk.Button(frame_btn, text="Limpiar Formulario", command=self.limpiar_campos).pack(side="left", padx=5)

        # Tabla (Treeview)
        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = ("ID", "Nombre", "Email", "Teléfono", "Dirección", "Tipo")
        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=110)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_registro)

    def guardar_cliente(self):
        c_id = self.ent_id.get().strip()
        nombre = self.ent_nombre.get().strip()
        email = self.ent_email.get().strip()
        telefono = self.ent_telefono.get().strip()
        direccion = self.ent_direccion.get().strip()
        tipo = self.combo_tipo.get()

        if not all([c_id, nombre, email, telefono, direccion]):
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return

        try:
            if not ServicioExternoAPI.validar_identidad_api(c_id):
                messagebox.showerror("Error", "Validación de identidad fallida.")
                return

            if tipo == "Premium":
                nuevo_cliente = ClientePremium(c_id, nombre, email, telefono, direccion)
            elif tipo == "Corporativo":
                nuevo_cliente = ClienteCorporativo(c_id, nombre, email, telefono, direccion, "TechCorp", "RTU-123")
            else:
                nuevo_cliente = ClienteRegular(c_id, nombre, email, telefono, direccion)

            self.db.guardar_cliente(nuevo_cliente)
            ServicioExternoAPI.enviar_email_bienvenida(email, nombre)

            messagebox.showinfo("Éxito", f"Cliente {nombre} guardado correctamente.")
            self.cargar_tabla()
            self.limpiar_campos()

        except ClienteError as e:
            messagebox.showerror("Error de Validación", str(e))
        except BaseDatosError as e:
            messagebox.showerror("Error de BD", str(e))

    def eliminar_cliente(self):
        c_id = self.ent_id.get().strip()
        if not c_id:
            messagebox.showwarning("Advertencia", "Seleccione o ingrese un ID para eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar al cliente con ID {c_id}?"):
            try:
                self.db.eliminar_cliente(c_id)
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
                self.cargar_tabla()
                self.limpiar_campos()
            except BaseDatosError as e:
                messagebox.showerror("Error", str(e))

    def exportar_csv(self):
        try:
            self.db.exportar_csv()
            messagebox.showinfo("Éxito", "Datos exportados a clientes.csv exitosamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

    def cargar_tabla(self):
        for item in self.tabla.get_children():
            self.tabla.delete(item)
        try:
            clientes = self.db.obtener_todos()
            for c in clientes:
                self.tabla.insert("", "end", values=(c.id, c.nombre, c.email, c.telefono, c.direccion, c.obtener_tipo()))
        except BaseDatosError as e:
            logger.error(f"Error al cargar tabla: {e}")

    def seleccionar_registro(self, event):
        item = self.tabla.focus()
        if item:
            valores = self.tabla.item(item, "values")
            self.limpiar_campos()
            self.ent_id.insert(0, valores[0])
            self.ent_nombre.insert(0, valores[1])
            self.ent_email.insert(0, valores[2])
            self.ent_telefono.insert(0, valores[3])
            self.ent_direccion.insert(0, valores[4])
            self.combo_tipo.set(valores[5])

    def limpiar_campos(self):
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_telefono.delete(0, tk.END)
        self.ent_direccion.delete(0, tk.END)
        self.combo_tipo.set("Regular")