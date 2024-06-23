import tkinter as tk
from tkinter import ttk, font
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import menu_principal

def ventana_filtrarTareas():
    def on_select(event):
        selected_value = combo.get()
        print(f"Seleccionar Prioridad: {selected_value}")
    def btn_volver():
        ventana_filtrar.destroy()
        menu_principal.ventana_menuPrincipal()
    def cargar_lista_tareas():
        # Realiza la conexión a la base de datos
        conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
        cursor = conexion.cursor()

        # Obtener la prioridad seleccionada
        selected_priority = combo.get()

        # Consulta SQL para obtener la lista de tareas filtrada por prioridad
        consulta = "SELECT nombre, fecha_vencimiento, estado FROM Tareas WHERE prioridad = %s"
        cursor.execute(consulta, (selected_priority,))

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
            
    ventana_filtrar = tk.Toplevel()
    ventana_filtrar.title("Filtrar Tarea")
    
    fuente_titulo = font.Font(family="Lemon", size=17)
    fuente_boton = font.Font(family="Oswald", size=14)
    
    imagen_fondo = Image.open("imagenes/fondoFiltrarTareas.png")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    
    canvas = tk.Canvas(ventana_filtrar, width=744, height=500)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)
    
    color_fondo_label = "#12225c"
    label_titulo = tk.Label(ventana_filtrar, text="FILTRAR TAREAS", font=fuente_titulo, background=color_fondo_label, foreground="white")
    label_titulo.place(x=30, y=20)
    
    # Crear un Treeview para mostrar la lista de tareas
    tree = ttk.Treeview(ventana_filtrar, columns=("Nombre", "Fecha de Vencimiento", "Estado"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
    tree.heading("Estado", text="Estado")
    tree.place(x=50, y=140, width=590, height=220)
    
    # Botón para cargar la lista de tareas
    btn_cancelar = tk.Button(ventana_filtrar, text="CANCELAR", font=fuente_boton, foreground="white", background="#158c81", command=btn_volver)
    btn_cancelar.place(x=300, y=380, width=120, height=40)

    btn_Buscar = tk.Button(ventana_filtrar, text="BUSCAR", font=fuente_boton, foreground="white", background="#165955", command=cargar_lista_tareas)
    btn_Buscar.place(x=520, y=80, width=120, height=40)
    
    opciones_prioridad = ["Alta Prioridad", "Prioridad Media", "Baja Prioridad"]
    combo = ttk.Combobox(ventana_filtrar, values=opciones_prioridad, background="#158c81", font=fuente_boton, state="readonly")
    combo.set("Seleccionar Prioridad: ")
    
    combo.bind("<<ComboboxSelected>>", on_select)
    combo.place(x=270, y=80, width=210, height=40)
    
    ventana_filtrar.geometry("700x470")
    ventana_filtrar.resizable(False, False)
    
    ventana_filtrar.mainloop()
