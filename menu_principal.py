import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import agregarTarea 
import verListaTareas
import marcarTareaCompletada
import filtrarTarea
import imprimirLista
import recordatorio
import asociarUsuarios

class CircleButton:
    def __init__(self, canvas, x, y, *, anchor="nw", command, **kwargs):
        self.id = canvas.create_image(x, y, anchor=anchor, **kwargs)
        self.canvas = canvas
        self.command = command
        self.image = kwargs.get("image")
        canvas.tag_bind(self.id, "<Button-1>", self.call)

    def call(self, event):
        return self.command()
    

def ventana_menuPrincipal():
    
    def abrir_ventana_Agregar():
        menu_ventana.destroy()
        agregarTarea.ventana_agregarTarea()
    
    def abrir_ventana_asociarUsuarios():
        menu_ventana.destroy()
        asociarUsuarios.ventana_AsoUsuarios()
    
    def abrir_ventana_listaTareas():
        menu_ventana.destroy()
        verListaTareas.ventana_listaTareas()
    
    def abrir_marcarTareaCompletada():
        menu_ventana.destroy()
        marcarTareaCompletada.ventana_marcarCompletada()
    
    def abrir_filtrarTareas():
        menu_ventana.destroy()
        filtrarTarea.ventana_filtrarTareas()
    
    def abrir_recordatorio():
        recordatorio.alerta_recordatorio()
    
    def abrir_imprimirLista():
        menu_ventana.destroy()
        imprimirLista.ventana_imprimirLista()
        
    
    # Crear la ventana del menú
    menu_ventana = tk.Toplevel()
    menu_ventana.title("Menú Principal")

    imagen_fondo = Image.open("imagenes/fondoMenu.png")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    canvas = tk.Canvas(menu_ventana, width=758, height=500)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

    fuente_titulo = font.Font(family="Lemon", size=14)
    custom_font_button = font.Font(family="Oswald", size=11)

    color_fondo_label = "#1c1e4a"
    titulo_label = tk.Label(menu_ventana, text="MENÚ PRINCIPAL", font=fuente_titulo, background=color_fondo_label, foreground="white")
    titulo_label.place(x=300, y=40)
    
    #Agregar las fotos y el botón del menú
    icono_agregarTarea = Image.open("imagenes/agregarTarea.png")
    icono_agregarTarea = icono_agregarTarea.resize((75, 75))
    icono_agregarTarea = ImageTk.PhotoImage(icono_agregarTarea)
    CircleButton(canvas, 120, 140, command=None, anchor="center", image=icono_agregarTarea)

    boton_AgregarTarea = tk.Button(menu_ventana, text="AGREGAR TAREA", background="#158c81", foreground="white", font=custom_font_button, command=abrir_ventana_Agregar)
    boton_AgregarTarea.place(x=60, y=190, width=120, height=40)

    icono_asociarUsuarios = Image.open("imagenes/asociarUsuarios.png")
    icono_asociarUsuarios = icono_asociarUsuarios.resize((70, 70))
    icono_asociarUsuarios = ImageTk.PhotoImage(icono_asociarUsuarios)
    CircleButton(canvas, 275, 140, command=None, anchor="center", image=icono_asociarUsuarios)

    boton_AsociarUsuarios = tk.Button(menu_ventana, text="ASOCIAR TAREAS", background="#158c81", foreground="white", font=custom_font_button, command=abrir_ventana_asociarUsuarios)
    boton_AsociarUsuarios.place(x=220, y=190, width=120, height=40)

    icono_VerListaTareas = Image.open("imagenes/listaTareas.png")
    icono_VerListaTareas = icono_VerListaTareas.resize((75, 75))
    icono_VerListaTareas = ImageTk.PhotoImage(icono_VerListaTareas)
    CircleButton(canvas, 445, 140, command=None, anchor="center", image=icono_VerListaTareas)

    boton_VerLista = tk.Button(menu_ventana, text="VER LISTA TAREAS", background="#158c81", foreground="white", font=custom_font_button, command=abrir_ventana_listaTareas)
    boton_VerLista.place(x=380, y=190, width=130, height=40)

    icono_MarcarCompletado = Image.open("imagenes/TareasCompletadas.png")
    icono_MarcarCompletado = icono_MarcarCompletado.resize((80, 80))
    icono_MarcarCompletado = ImageTk.PhotoImage(icono_MarcarCompletado)
    CircleButton(canvas, 635, 140, command=None, anchor="center", image=icono_MarcarCompletado)

    boton_MarcarCompletado = tk.Button(menu_ventana, text="MARCAR COMO COMPLETADO", background="#158c81", foreground="white", font=custom_font_button, command=abrir_marcarTareaCompletada)
    boton_MarcarCompletado.place(x=560, y=190, width=170, height=40)

    icono_FiltrarTareas = Image.open("imagenes/filtrarTareas.png")
    icono_FiltrarTareas = icono_FiltrarTareas.resize((70, 70))
    icono_FiltrarTareas = ImageTk.PhotoImage(icono_FiltrarTareas)
    CircleButton(canvas, 210, 340, command=None, anchor="center", image=icono_FiltrarTareas)

    boton_FiltrarTareas = tk.Button(menu_ventana, text="FILTRAR TAREAS", background="#158c81", foreground="white", font=custom_font_button, command=abrir_filtrarTareas)
    boton_FiltrarTareas.place(x=150, y=390, width=120, height=40)

    icono_RecordarTareas = Image.open("imagenes/recordatorioTareas.png")
    icono_RecordarTareas = icono_RecordarTareas.resize((85, 85))
    icono_RecordarTareas = ImageTk.PhotoImage(icono_RecordarTareas)
    CircleButton(canvas, 390, 340, command=None, anchor="center", image=icono_RecordarTareas)

    boton_RecordarTareas = tk.Button(menu_ventana, text="RECORDATORIO TAREAS", background="#158c81", foreground="white", font=custom_font_button, command=abrir_recordatorio)
    boton_RecordarTareas.place(x=310, y=390, width=160, height=40)

    icono_ImprimirTareas = Image.open("imagenes/imprimirtareas.png")
    icono_ImprimirTareas = icono_ImprimirTareas.resize((90, 90))
    icono_ImprimirTareas = ImageTk.PhotoImage(icono_ImprimirTareas)
    CircleButton(canvas, 573, 340, command=None, anchor="center", image=icono_ImprimirTareas)

    boton_ImprimirTareas = tk.Button(menu_ventana, text="IMPRIMIR TAREAS", background="#158c81", foreground="white", font=custom_font_button, command=abrir_imprimirLista)
    boton_ImprimirTareas.place(x=510, y=390, width=120, height=40)
    
    menu_ventana.geometry("758x500")
    menu_ventana.resizable(False, False)

    # Mostrar la ventana del menú
    menu_ventana.mainloop()

