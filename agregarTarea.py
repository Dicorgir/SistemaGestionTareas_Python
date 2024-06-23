import tkinter as tk
from tkinter import ttk, font
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import menu_principal

def ventana_agregarTarea():
    def mostrar_fecha_seleccionada():
        fecha_seleccionada = cal.get_date()
        etiqueta_fecha.config(text=f"{fecha_seleccionada}")

    def on_select(event):
        selected_value = combo.get()
        print(f"Seleccionar Prioridad: {selected_value}")

    def on_select_estado(event):
        selected_value = comboEstado.get()
        print(f"Seleccionar Estado: {selected_value}")

    def btn_volver():
        ventana_agregar.destroy()
        menu_principal.ventana_menuPrincipal()

    def on_entry_click(entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_entry_leave(entry, default_text):
        if entry.get() == "":
            entry.insert(0, default_text)
            entry.config(fg="grey")

    def insertar_tarea():
        # Obtener los valores de los widgets
        nombre_tarea = textField_nombreTarea.get()
        fecha_vencimiento = etiqueta_fecha.cget("text")
        prioridad = combo.get()
        estado = comboEstado.get()
        
        # Convertir la fecha a formato correcto (de tkcalendar a MySQL)
        fecha_vencimiento_final = datetime.strptime(fecha_vencimiento, "%d/%m/%y").strftime("%Y-%m-%d")

        # Conectar a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            port="3307",
            password="",
            database="gestion_tareas"
        )

        # Crear un cursor para ejecutar consultas
        cursor = conexion.cursor()

        # Ejecutar la consulta de inserción
        consulta = "INSERT INTO Tareas (nombre, fecha_vencimiento, prioridad, estado) VALUES (%s, %s, %s, %s)"
        valores = (nombre_tarea, fecha_vencimiento_final, prioridad, estado)
        cursor.execute(consulta, valores)

        # Confirmar la inserción y cerrar la conexión
        conexion.commit()
        conexion.close()

        print("Tarea agregada con éxito")

    ventana_agregar = tk.Toplevel()
    ventana_agregar.title("Agregar Tarea")

    fuente_titulo = font.Font(family="Lemon", size=17)
    fuente_boton = font.Font(family="Oswald", size=14)

    imagen_fondo = Image.open("imagenes/fondoAgregarTareas.png")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    canvas = tk.Canvas(ventana_agregar, width=744, height=500)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

    color_fondo_label = "#072c2c"
    label_titulo = tk.Label(ventana_agregar, text="AGREGAR TAREAS", font=fuente_titulo, background=color_fondo_label, foreground="white")
    label_titulo.place(x=30, y=30)

    nombrePorDefecto = "Nombre de la tarea"
    textField_nombreTarea = tk.Entry(ventana_agregar, fg="grey")
    textField_nombreTarea.insert(0, nombrePorDefecto)
    textField_nombreTarea.bind("<FocusIn>", lambda event, entry=textField_nombreTarea, nombrePorDefecto=nombrePorDefecto: on_entry_click(entry, nombrePorDefecto))
    textField_nombreTarea.bind("<FocusOut>", lambda event, entry=textField_nombreTarea, nombrePorDefecto=nombrePorDefecto: on_entry_leave(entry, nombrePorDefecto))
    textField_nombreTarea.place(x=50, y=110, width=210, height=30)

    cal = Calendar(ventana_agregar, selectmode='day', year=2024, month=1, day=1)
    cal.place(x=300, y=90)

    boton_obtener_fecha = tk.Button(ventana_agregar, text="Obtener Fecha Venc.", foreground="white", background="#158c81", font=fuente_boton, command=mostrar_fecha_seleccionada)
    boton_obtener_fecha.place(x=570, y=90, width=150, height=40)

    etiqueta_fecha = tk.Label(ventana_agregar, text="", background="#cff8f0", font=fuente_boton)
    etiqueta_fecha.place(x=580, y=140, width=130, height=40)

    btn_cancelar = tk.Button(ventana_agregar, text="CANCELAR", font=fuente_boton, foreground="white", background="#158c81", command=btn_volver)
    btn_cancelar.place(x=240, y=300, width=110, height=40)

    btn_insertarTarea = tk.Button(ventana_agregar, text="AGREGAR TAREA", font=fuente_boton, foreground="white", background="#158c81", command=insertar_tarea)
    btn_insertarTarea.place(x=380, y=300, width=135, height=40)

    opciones_prioridad = ["Alta Prioridad", "Prioridad Media", "Baja Prioridad"]
    combo = ttk.Combobox(ventana_agregar, values=opciones_prioridad, background="#158c81", font=fuente_boton, state="readonly")
    combo.set("Seleccionar Prioridad: ")

    opciones_estado = ["Sin Completar", "Pendiente", "Completado"]
    comboEstado = ttk.Combobox(ventana_agregar, values=opciones_estado, background="#158c81", font=fuente_boton, state="readonly")
    comboEstado.set("Seleccionar Estado: ")

    combo.bind("<<ComboboxSelected>>", on_select)
    combo.place(x=50, y=160, width=210, height=40)

    comboEstado.bind("<<ComboboxSelected>>", on_select_estado)
    comboEstado.place(x=50, y=230, width=210, height=40)

    ventana_agregar.geometry("735x370")
    ventana_agregar.resizable(False, False)

    ventana_agregar.mainloop()
