import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime


class GestorTienda:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tienda")

        # Crear la conexión con la base de datos
        self.conexion = sqlite3.connect("tienda.db")
        self.cursor = self.conexion.cursor()

        # Crear la tabla de productos si no existe
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS productos (id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "nombre TEXT, precio REAL, cantidad INTEGER, fecha TEXT)"
        )
        self.conexion.commit()

        # Variables para los campos de entrada
        self.id_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.precio_var = tk.DoubleVar()
        self.cantidad_var = tk.IntVar()
        self.busqueda_var = tk.StringVar()

        tk.Label(root, text="Nombre del producto:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.nombre_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(root, text="Precio:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.precio_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(root, text="Cantidad:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.cantidad_var).grid(row=3, column=1, padx=5, pady=5)

        # Botones
        tk.Button(root, text="Agregar", command=self.agregar_producto).grid(row=4, column=0, padx=5, pady=5)
        tk.Button(root, text="Mostrar", command=self.mostrar_productos).grid(row=4, column=1, padx=5, pady=5)

        # Campo de búsqueda
        tk.Label(root, text="Buscar por nombre:").grid(row=5, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.busqueda_var).grid(row=5, column=1, padx=5, pady=5)
        tk.Button(root, text="Buscar", command=self.buscar_productos).grid(row=5, column=2, padx=5, pady=5)

        # Tabla
        self.tabla = ttk.Treeview(root, columns=("id", "nombre", "precio", "cantidad", "fecha"), show="headings")
        self.tabla.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("cantidad", text="Cantidad")
        self.tabla.heading("fecha", text="Fecha")

        self.tabla.bind("<ButtonRelease-1>", self.seleccionar_producto)

    def agregar_producto(self):
        nombre = self.nombre_var.get()
        precio = self.precio_var.get()
        cantidad = self.cantidad_var.get()
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if nombre and precio and cantidad:
            self.cursor.execute(
                "INSERT INTO productos (nombre, precio, cantidad, fecha) VALUES (?, ?, ?, ?)",
                (nombre, precio, cantidad, fecha),
            )
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            self.nombre_var.set("")
            self.precio_var.set(0.0)
            self.cantidad_var.set(0)
            self.mostrar_productos()
        else:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")

    def mostrar_productos(self):
        self.tabla.delete(*self.tabla.get_children())
        self.cursor.execute("SELECT * FROM productos")
        productos = self.cursor.fetchall()

        for producto in productos:
            self.tabla.insert("", "end", values=producto)

    def seleccionar_producto(self, event):
        fila_seleccionada = self.tabla.selection()
        if fila_seleccionada:
            producto = self.tabla.item(fila_seleccionada)["values"]
            self.id_var.set(producto[0])
            self.nombre_var.set(producto[1])
            self.precio_var.set(producto[2])
            self.cantidad_var.set(producto[3])

    def actualizar_producto(self):
        id_producto = self.id_var.get()
        nombre = self.nombre_var.get()
        precio = self.precio_var.get()
        cantidad = self.cantidad_var.get()

        if id_producto:
            if nombre and precio and cantidad:
                self.cursor.execute(
                    "UPDATE productos SET nombre=?, precio=?, cantidad=? WHERE id=?",
                    (nombre, precio, cantidad, id_producto),
                )
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Producto actualizado correctamente.")
                self.id_var.set("")
                self.nombre_var.set("")
                self.precio_var.set(0.0)
                self.cantidad_var.set(0)
                self.mostrar_productos()
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto para editar.")

    def eliminar_producto(self):
        id_producto = self.id_var.get()

        if id_producto:
            confirmacion = messagebox.askyesno(
                "Confirmar", "¿Está seguro de que desea eliminar este producto?"
            )
            if confirmacion:
                self.cursor.execute("DELETE FROM productos WHERE id=?", (id_producto,))
                self.conexion.commit()
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
                self.id_var.set("")
                self.nombre_var.set("")
                self.precio_var.set(0.0)
                self.cantidad_var.set(0)
                self.mostrar_productos()
        else:
            messagebox.showerror("Error", "Por favor, seleccione un producto para eliminar.")

    def buscar_productos(self):
        nombre_busqueda = self.busqueda_var.get()
        if nombre_busqueda:
            self.tabla.delete(*self.tabla.get_children())
            self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre_busqueda + '%',))
            productos = self.cursor.fetchall()

            for producto in productos:
                self.tabla.insert("", "end", values=producto)
        else:
            messagebox.showerror("Error", "Por favor, ingrese un nombre de producto para buscar.")


if __name__ == "__main__":
    root = tk.Tk()
    gestor_tienda = GestorTienda(root)
    tk.Button(root, text="Actualizar", command=gestor_tienda.actualizar_producto).grid(row=7, column=0, padx=5, pady=5)
    tk.Button(root, text="Eliminar", command=gestor_tienda.eliminar_producto).grid(row=7, column=1, padx=5, pady=5)
    root.mainloop()
