import tkinter as tk

# Crea una instancia de la ventana
ventana = tk.Tk()
ventana.title("Gestor De Negocios")
ventana.geometry("400x300")

# mostrar_texto
def mostrar_texto():
    texto = producto.get()
    datos.config(text=texto) 
    

# Nombre del producto

NombreDelProducto = tk.Label(ventana, text="Ingresa el nombre del producto: ")
NombreDelProducto.pack()
producto = tk.Entry(ventana)
producto.pack()

# creando label de texto
datos = tk.Label(ventana, text="Texto mostrado")
datos.pack()

# Botón para obtener los datos
boton = tk.Button(ventana, text="Obtener datos", command=mostrar_texto)
boton.pack()


# Ejecuta el bucle principal de la ventana
ventana.mainloop()
