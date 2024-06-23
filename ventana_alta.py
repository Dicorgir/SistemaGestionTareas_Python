import tkinter as tk
from tkinter import ttk, font, filedialog, messagebox
from PIL import Image, ImageTk
import mysql.connector
import re 
import interfaz 

def on_entry_click(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, tk.END)
        entry.config(fg="black")

def on_entry_leave(entry, default_text):
    if entry.get() == "":
        entry.insert(0, default_text)
        entry.config(fg="grey")
def on_entry_click_contra(entry, default_text):
    if entry.get() == default_text:
        entry.delete(0, "end")
        entry.config(show="*", fg="black")

def on_entry_leave_contra(entry, default_text):
    if entry.get() == "":
        entry.insert(0, "Contraseña")
        entry.config(show="", fg="grey")

def seleccionar_archivo(entry, image_label):
    archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")])
    if archivo:
        # Mostrar la imagen seleccionada al lado del botón
        image = Image.open(archivo)
        image = image.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label.config(image=photo)
        image_label.image = photo  # Se debe mantener una referencia a la imagen para que no sea eliminada por el recolector de basura

def insertar_datos(nombre, apellidos, nombre_usuario, contrasenia):
    try:
        conexion = mysql.connector.connect(
        host="localhost",
        port=3307,
        user="root",
        database="gestion_tareas"
        )

        cursor = conexion.cursor()

        # Insertar datos en la tabla usuario
        query = "INSERT INTO usuarios (nombre, apellidos, nombre_usuario, contrasenia) VALUES (%s, %s, %s, %s)"
        datos = (nombre, apellidos, nombre_usuario, contrasenia)
        cursor.execute(query, datos)

        # Confirmar la transacción
        conexion.commit()

        # Cerrar la conexión
        cursor.close()
        conexion.close()

        print("Datos insertados correctamente.")
    except mysql.connector.Error as error:
        print(f"Error al insertar datos: {error}")
    


def crear_linea_discontinua(canvas, x, y, longitud, espaciado, orientacion):
    if orientacion == "horizontal":
        for i in range(0, longitud, espaciado):
            canvas.create_line(x + i, y, x + i + espaciado, y, dash=(5, 5), width=2, fill="white")
    elif orientacion == "vertical":
        for i in range(0, longitud, espaciado):
            canvas.create_line(x, y + i, x, y + i + espaciado, dash=(5, 5), width=2, fill="white")

def ventana_alta():
    def validar_nombre(nombre):
        patron = re.compile(r'^[A-Z][a-z]*$')
        return bool(patron.match(nombre))
    
    def validar_apellidos(apellidos):
        # Expresión regular para verificar si hay dos palabras con la primera letra en mayúscula y un espacio entre ellas
        patron = re.compile(r'^[A-Z][a-z]+ [A-Z][a-z]+$')
        return bool(patron.match(apellidos))
    
    def validar_contrasenia(contrasenia):
        # Expresión regular para verificar que haya al menos una letra mayúscula, un número y un mínimo de 5 caracteres
        patron = re.compile(r'^(?=.*[A-Z])(?=.*\d).{5,}$')
        return bool(patron.match(contrasenia))

        
    def btn_aceptar_click():
        # Obtener datos de los campos
        nombre = textField_nombre.get()
        apellidos = textField_apellido.get()
        nombre_usuario = textField_usuario.get()
        contrasenia = textField_contra.get()

        # Validar los apellidos antes de insertar datos en la base de datos
        if not validar_apellidos(apellidos):
            messagebox.showerror("Error", "Los apellidos deben tener dos palabras con la primera letra en mayúscula y un espacio entre ellas.")
            return
        
        # Validar el nombre antes de insertar datos en la base de datos
        if not validar_nombre(nombre):
            messagebox.showerror("Error", "El nombre debe comenzar con una letra mayúscula seguida de letras minúsculas.")
            return
        
        # Validar la contraseña antes de insertar datos en la base de datos
        if not validar_contrasenia(contrasenia):
            messagebox.showerror("Error", "La contraseña debe contener al menos una letra mayúscula, un número y tener un mínimo de 5 caracteres.")
            return

        # Insertar datos en la base de datos
        insertar_datos(nombre, apellidos, nombre_usuario, contrasenia)
        ventana_de_alta.destroy()
        interfaz.programa_con_interfaz()
        
        
    ventana_de_alta = tk.Tk()
    ventana_de_alta.title("Dar de alta")

    fuente_titulo = font.Font(family="Lemon", size=14)
    fuente_boton_seleccion = font.Font(family="Oswald", size=11)

    imagen_fondo = Image.open("imagenes/fondoAlta.jpg")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    canvas = tk.Canvas(ventana_de_alta, width=600, height=420)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

    color_fondo_label = "#1c1e4a"
    titulo_label = tk.Label(ventana_de_alta, text="ALTA DE USUARIO", font=fuente_titulo, background=color_fondo_label, foreground="white")
    titulo_label.place(x=30, y=40)

    default_text_nombre = "Pon tu nombre"
    textField_nombre = tk.Entry(ventana_de_alta, fg="grey", background="#cff8ef")
    textField_nombre.insert(0, default_text_nombre)
    textField_nombre.bind("<FocusIn>", lambda event, entry=textField_nombre, default_text=default_text_nombre: on_entry_click(entry, default_text))
    textField_nombre.bind("<FocusOut>", lambda event, entry=textField_nombre, default_text=default_text_nombre: on_entry_leave(entry, default_text))
    textField_nombre.place(x=50, y=90, width=210, height=30)

    default_text_apellido = "Pon tus apellidos"
    textField_apellido = tk.Entry(ventana_de_alta, fg="grey", background="#cff8ef")
    textField_apellido.insert(0, default_text_apellido)
    textField_apellido.bind("<FocusIn>", lambda event, entry=textField_apellido, default_text=default_text_apellido: on_entry_click(entry, default_text))
    textField_apellido.bind("<FocusOut>", lambda event, entry=textField_apellido, default_text=default_text_apellido: on_entry_leave(entry, default_text))
    textField_apellido.place(x=50, y=140, width=210, height=30)
    
    default_text_usuario = "Pon tu nombre de usuario"
    textField_usuario = tk.Entry(ventana_de_alta, fg="grey", background="#cff8ef")
    textField_usuario.insert(0, default_text_usuario)
    textField_usuario.bind("<FocusIn>", lambda event, entry=textField_usuario, default_text=default_text_usuario: on_entry_click(entry, default_text))
    textField_usuario.bind("<FocusOut>", lambda event, entry=textField_usuario, default_text=default_text_usuario: on_entry_leave(entry, default_text))
    textField_usuario.place(x=320, y=90, width=210, height=30)
    
    default_text_contra = "Pon la contraseña que desees"
    textField_contra = tk.Entry(ventana_de_alta, fg="grey", background="#cff8ef", show="")
    textField_contra.insert(0, default_text_contra)
    textField_contra.bind("<FocusIn>", lambda event, entry=textField_contra, default_text=default_text_contra: on_entry_click_contra(entry, default_text))
    textField_contra.bind("<FocusOut>", lambda event, entry=textField_contra, default_text=default_text_contra: on_entry_leave_contra(entry, default_text))
    textField_contra.place(x=320, y=140, width=210, height=30)
    
    # Crear una línea discontinua horizontal
    crear_linea_discontinua(canvas, x=45, y=210, longitud=500, espaciado=5, orientacion="horizontal")
    crear_linea_discontinua(canvas, x=45, y=360, longitud=500, espaciado=5, orientacion="horizontal")
    
    # Crear una etiqueta para mostrar la imagen seleccionada
    image_label = tk.Label(ventana_de_alta, background="#cff8ef")
    image_label.place(x=370, y=240, width=100, height=100)

    # Botón para seleccionar un archivo
    btn_seleccionar_archivo = tk.Button(ventana_de_alta, text="Seleccionar Archivo", command=lambda: seleccionar_archivo(textField_usuario, image_label), font=fuente_boton_seleccion, foreground="white", background="#158c81")
    btn_seleccionar_archivo.place(x=70, y=270, width=180, height=30)

    btn_Aceptar_datos = tk.Button(ventana_de_alta, text="ACEPTAR", command=btn_aceptar_click, font=fuente_boton_seleccion, foreground="white", background="#158c81")
    btn_Aceptar_datos.place(x=240, y=380, width=120, height=30)

    ventana_de_alta.geometry("600x420")
    ventana_de_alta.resizable(False, False)

    ventana_de_alta.mainloop()
