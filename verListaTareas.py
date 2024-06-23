import tkinter as tk
from tkinter import ttk, font
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import menu_principal

def ventana_listaTareas():
    def btn_volver():
        ventana_lista.destroy()
        menu_principal.ventana_menuPrincipal()

    def cargar_lista_tareas():
        # Realiza la conexión a la base de datos y ejecuta la consulta para obtener la lista de tareas
        conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
        cursor = conexion.cursor()

        # Consulta SQL para obtener la lista de tareas con detalles
        consulta = "SELECT nombre, fecha_vencimiento, prioridad FROM Tareas"
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

    ventana_lista = tk.Toplevel()
    ventana_lista.title("Ver Lista de Tareas")
    
    fuente_titulo = font.Font(family="Lemon", size=17)
    fuente_boton = font.Font(family="Oswald", size=14)
    
    imagen_fondo = Image.open("imagenes/fondoVerLista.png")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    
    canvas = tk.Canvas(ventana_lista, width=744, height=500)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)
    
    color_fondo_label = "#12225c"
    label_titulo = tk.Label(ventana_lista, text="VER LISTA", font=fuente_titulo, background=color_fondo_label, foreground="white")
    label_titulo.place(x=30, y=20)

    btn_cancelar = tk.Button(ventana_lista, text="CANCELAR", font=fuente_boton, foreground="white", background="#158c81", command=btn_volver)
    btn_cancelar.place(x=200, y=305, width=110, height=40)

    # Crear un Treeview para mostrar la lista de tareas
    tree = ttk.Treeview(ventana_lista, columns=("Nombre", "Fecha de Vencimiento", "Prioridad"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
    tree.heading("Prioridad", text="Prioridad")
    tree.place(x=30, y=70, width=590, height=220)

    # Botón para cargar la lista de tareas
    btn_cargar_tareas = tk.Button(ventana_lista, text="CARGAR LISTA DE TAREAS", font=fuente_boton, foreground="white", background="#158c81", command=cargar_lista_tareas)
    btn_cargar_tareas.place(x=350, y=305, width=190, height=40)

    ventana_lista.geometry("650x370")
    ventana_lista.resizable(False, False)

    ventana_lista.mainloop()

