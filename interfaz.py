import tkinter as tk
import mysql.connector
from ventana_alta import ventana_alta
import menu_principal
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from PIL import Image, ImageTk

class CircleButton:
    def __init__(self, canvas, x, y, *, anchor="nw", command, **kwargs):
        self.id = canvas.create_image(x, y, anchor=anchor, **kwargs)
        self.canvas = canvas
        self.command = command
        self.image = kwargs.get("image")
        canvas.tag_bind(self.id, "<Button-1>", self.call)

    def call(self, event):
        return self.command()
    
def programa_con_interfaz():
    def cerrar_ventana():
        ventana.destroy()
        
    def on_entry_click(event):
        if entrar_usuario.get() == "Usuario":
            entrar_usuario.delete(0, "end")
            entrar_usuario.config(fg="black")

    def on_entry_leave(event):
        if entrar_usuario.get() == "":
            entrar_usuario.insert(0, "Usuario")
            entrar_usuario.config(fg="grey")

    def on_entry_click_contra(event):
        if entrar_contra.get() == "Contraseña":
            entrar_contra.delete(0, "end")
            entrar_contra.config(show="*", fg="black")

    def on_entry_leave_contra(event):
        if entrar_contra.get() == "":
            entrar_contra.insert(0, "Contraseña")
            entrar_contra.config(show="", fg="grey")

    
    def validar_credenciales(usuario, contrasenia):
        try:
            # Establecer la conexión a la base de datos
            conexion = mysql.connector.connect(
                host="localhost",
                port=3307,
                user="root",
                database="gestion_tareas"
            )

            # Crear un cursor para ejecutar consultas
            cursor = conexion.cursor()

            # Ejecutar una consulta para obtener el usuario y la contraseña
            consulta = "SELECT nombre_usuario, contrasenia FROM usuarios WHERE nombre_usuario=%s"
            cursor.execute(consulta, (usuario,))

            # Obtener los resultados de la consulta
            resultado = cursor.fetchone()

            # Cerrar la conexión
            cursor.close()
            conexion.close()

            # Verificar si las credenciales son válidas
            if resultado and resultado[1] == contrasenia:
                return True
            else:
                return False

        except mysql.connector.Error as error:
            print(f"Error de base de datos: {error}")
            return False
        
    def ventana_menu():
        usuario = entrar_usuario.get()
        contrasenia = entrar_contra.get()
        if validar_credenciales(usuario, contrasenia):
            messagebox.showinfo("Inicio de sesión", "Inicio de sesión exitoso.")
            ventana.iconify()
            menu_principal.ventana_menuPrincipal()
            ventana.deiconify()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas. Inténtelo de nuevo.")
            # Limpiar los campos de texto
            entrar_usuario.delete(0, tk.END)
            entrar_contra.delete(0, tk.END)
            
    def abrir_ventana_alta():
        cerrar_ventana()
        ventana_alta()
        
    ventana = tk.Tk()
    ventana.title("Inicio de Sesión")
    
    # Fuentes de la ventana
    custom_font = font.Font(family="Lemon", size=14)
    custom_font_button = font.Font(family="Oswald", size=11)
    
    # Cargar la imagen de fondo
    imagen_fondo = Image.open("imagenes/fondoLogin.jpg") 
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    # Crear el Canvas y mostrar la imagen de fondo
    canvas = tk.Canvas(ventana, width=400, height=450)
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

    # Crear el label del título
    color_fondo_label = "#158c81"
    titulo_label = tk.Label(ventana, text="SISTEMA DE GESTIÓN DE TAREAS", font=custom_font, background=color_fondo_label, foreground="white")
    # Configurar el fondo del label como transparente
    titulo_label.place(x=30, y=30)
    
    # Crear el cuadro de entrada para el usuario con marcador de posición
    entrar_usuario = tk.Entry(ventana, fg="grey")
    entrar_usuario.insert(0, "Usuario")
    entrar_usuario.bind("<FocusIn>", on_entry_click)
    entrar_usuario.bind("<FocusOut>", on_entry_leave)
    entrar_usuario.place(x=156, y=190, width=150, height=30)

    # Crear la etiqueta y el cuadro de contraseña
    entrar_contra = tk.Entry(ventana, show="", fg="grey")
    entrar_contra.insert(0, "Contraseña")
    entrar_contra.bind("<FocusIn>", on_entry_click_contra)
    entrar_contra.bind("<FocusOut>", on_entry_leave_contra)
    entrar_contra.place(x=156, y=230, width=150, height=30)

    # Agregar la imagen principal del login
    icono_perfil = Image.open("imagenes/icono.png")
    icono_perfil = icono_perfil.resize((75, 75))
    icono_perfil = ImageTk.PhotoImage(icono_perfil)
    CircleButton(canvas, 210, 130, command=None, anchor='center', image=icono_perfil)
    
    # Agregar la imagen al lado del cuadro de entrada de usuario
    icono_usuario = Image.open("imagenes/iconoUsuario.png")
    # Ajustar el tamaño de la imagen
    icono_usuario = icono_usuario.resize((35, 35))
    icono_usuario = ImageTk.PhotoImage(icono_usuario)
    CircleButton(canvas, 130, 205, command=lambda: entrar_usuario.focus_set(), anchor='center',image=icono_usuario)

    # Agregar la imagen de contraseña al lado de su cuadro de entrada correspondiente
    icono_contrasenia = Image.open("imagenes/candado.png")
    icono_contrasenia = icono_contrasenia.resize((35, 35))
    icono_contrasenia = ImageTk.PhotoImage(icono_contrasenia)
    CircleButton(canvas, 132, 245, command=lambda: entrar_contra.focus_set(), anchor='center', image=icono_contrasenia)


    boton_entrar = tk.Button(ventana, text="INICIAR SESIÓN", background="#158c81", foreground="white", font=custom_font_button, command=ventana_menu)
    boton_entrar.place(x=215, y=300, width=120, height=40)
    
    boton_alta = tk.Button(ventana, text="DAR DE ALTA", background="#158c81", foreground="white" , font=custom_font_button, command=abrir_ventana_alta)
    boton_alta.place(x=80, y=300, width=120, height=40)

    ventana.geometry("400x410")
    ventana.resizable(False, False)

    ventana.mainloop()
