import tkinter as tk
from tkinter import ttk, font
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import menu_principal

def ventana_imprimirLista():
    def btn_volver():
        ventana_imprimir.destroy()
        menu_principal.ventana_menuPrincipal()
    
    def cargar_lista_tareas():
        # Realiza la conexión a la base de datos y ejecuta la consulta para obtener la lista de tareas
        conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
        cursor = conexion.cursor()

        # Consulta SQL para obtener la lista de tareas con detalles, filtrando por estado "completo" o "pendiente"
        consulta = "SELECT nombre, fecha_vencimiento, prioridad, estado FROM Tareas WHERE estado IN ('completado', 'pendiente')"
        cursor.execute(consulta)

        # Obtiene todos los resultados de la consulta
        resultados = cursor.fetchall()

        # Cierra la conexión a la base de datos
        cursor.close()
        conexion.close()

        # Limpia las filas existentes en el Treeview
        for fila in tree.get_children():
            tree.delete(fila)

        # Inserta los resultados en el Treeview
        for resultado in resultados:
            tree.insert("", "end", values=resultado)

    ventana_imprimir = tk.Toplevel()
    ventana_imprimir.title("Imprimir Lista de Tareas")
    
    fuente_titulo = font.Font(family="Lemon", size=17)
    fuente_boton = font.Font(family="Oswald", size=14)
    
    imagen_fondo = Image.open("imagenes/fondoImprimirLista.png")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    
    canvas = tk.Canvas(ventana_imprimir, width=744, height=500)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)
    
    color_fondo_label = "#12225c"
    label_titulo = tk.Label(ventana_imprimir, text="IMPRIMIR LISTA", font=fuente_titulo, background=color_fondo_label, foreground="white")
    label_titulo.place(x=240, y=20)
    
    # Crear un Treeview para mostrar la lista de tareas
    tree = ttk.Treeview(ventana_imprimir, columns=("Nombre", "Fecha de Vencimiento", "Prioridad", "Estado"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
    tree.heading("Prioridad", text="Prioridad")
    tree.heading("Estado", text="Estado")
    
    # Establecer tamaños fijos para las columnas
    tree.column("Nombre", width=70)
    tree.column("Fecha de Vencimiento", width=70)
    tree.column("Prioridad", width=70)
    tree.column("Estado", width=70)
    tree.place(x=30, y=70, width=590, height=220)
    
    # Botón para cargar la lista de tareas
    btn_cargar_tareas = tk.Button(ventana_imprimir, text="MOSTRAR LISTA DE TAREAS", font=fuente_boton, foreground="white", background="#158c81", command=cargar_lista_tareas)
    btn_cargar_tareas.place(x=315, y=305, width=210, height=40)

    btn_cancelar = tk.Button(ventana_imprimir, text="CANCELAR", font=fuente_boton, foreground="white", background="#158c81", command=btn_volver)
    btn_cancelar.place(x=180, y=305, width=110, height=40)
    
    ventana_imprimir.geometry("650x370")
    ventana_imprimir.resizable(False, False)

    ventana_imprimir.mainloop()
