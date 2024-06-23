import tkinter as tk
from tkinter import ttk, font
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import datetime
import mysql.connector
import menu_principal

def tarea_existe(nombre_tarea):
    conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
    cursor = conexion.cursor()

    try:
        # Verificar si la tarea existe
        cursor.execute("SELECT id FROM Tareas WHERE nombre = %s", (nombre_tarea,))
        resultado = cursor.fetchone()

        return resultado is not None

    except mysql.connector.Error as err:
        print(f"Error al verificar la existencia de la tarea: {err}")

    finally:
        cursor.close()
        conexion.close()

    return False

def ventana_AsoUsuarios():
    def on_select(event):
        selected_value = combo.get()
        print(f"Seleccionar Usuario 1: {selected_value}")

    def on_select_2(event):
        selected_value = combo2.get()
        print(f"Seleccionar Usuario 2: {selected_value}")

    def asociar_usuarios():
        # Obtener la tarea seleccionada
        selected_task = tree.selection()
        if not selected_task:
            print("Seleccione una tarea antes de asociar usuarios.")
            return

        # Obtener el nombre de la tarea directamente de la fila seleccionada
        nombre_tarea = tree.item(selected_task, 'values')[0]

        # Obtener los usuarios seleccionados
        usuario_1 = combo.get()
        usuario_2 = combo2.get()

        # Realizar la asociación en la base de datos
        conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
        cursor = conexion.cursor()

        try:
            # Obtener el id de la tarea
            cursor.execute("SELECT id FROM Tareas WHERE nombre = %s", (nombre_tarea,))
            tarea_id = cursor.fetchone()

            if tarea_id:
                # Insertar asociación en la tabla Asignaciones_Multiples
                if usuario_2:  # Asociar dos usuarios
                    insert_query = "INSERT INTO Asignaciones_Multiples (tarea_id, nombre_usuario) VALUES (%s, %s), (%s, %s)"
                    cursor.execute(insert_query, (tarea_id[0], usuario_1, tarea_id[0], usuario_2))
                else:  # Asociar un solo usuario
                    insert_query = "INSERT INTO Asignaciones_Multiples (tarea_id, nombre_usuario) VALUES (%s, %s)"
                    cursor.execute(insert_query, (tarea_id[0], usuario_1))

                # Confirmar la transacción y cerrar la conexión
                conexion.commit()
                print("Usuarios asociados correctamente a la tarea.")
            else:
                print(f"La tarea con nombre '{nombre_tarea}' no existe. No se pueden asociar usuarios.")

        except mysql.connector.Error as err:
            print(f"Error al asociar usuarios a la tarea: {err}")
            conexion.rollback()

        finally:
            cursor.close()
            conexion.close()


    def btn_volver():
        ventana_asociar.destroy()
        menu_principal.ventana_menuPrincipal()

    def cargar_lista_tareas():
        # Realiza la conexión a la base de datos y ejecuta la consulta para obtener la lista de tareas
        conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
        cursor = conexion.cursor()

        # Consulta SQL para obtener la lista de tareas con detalles, filtrando por estado "completo" o "pendiente"
        consulta = "SELECT nombre, fecha_vencimiento, estado FROM Tareas"
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

    def cargar_usuarios():
        # Realiza la conexión a la base de datos y ejecuta la consulta para obtener la lista de usuarios
        conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
        cursor = conexion.cursor()

        # Consulta SQL para obtener la lista de usuarios
        consulta = "SELECT nombre_usuario FROM Usuarios"
        cursor.execute(consulta)

        # Obtiene todos los resultados de la consulta
        usuarios = [usuario[0] for usuario in cursor.fetchall()]

        # Cierra la conexión a la base de datos
        cursor.close()
        conexion.close()

        # Configura los valores del primer Combobox con la lista de usuarios
        combo["values"] = usuarios

        # Configura los valores del segundo Combobox con la lista de usuarios
        combo2["values"] = usuarios

    ventana_asociar = tk.Toplevel()
    ventana_asociar.title("Asociar Usuarios")

    fuente_titulo = font.Font(family="Lemon", size=17)
    fuente_boton = font.Font(family="Oswald", size=14)

    imagen_fondo = Image.open("imagenes/fondoAsociarUsuarios.png")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)

    canvas = tk.Canvas(ventana_asociar, width=744, height=500)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)

    color_fondo_label = "#072c2c"
    label_titulo = tk.Label(ventana_asociar, text="ASOCIAR USUARIOS", font=fuente_titulo, background=color_fondo_label, foreground="white")
    label_titulo.place(x=30, y=30)

    # Crear un Treeview para mostrar la lista de tareas
    tree = ttk.Treeview(ventana_asociar, columns=("Nombre", "Fecha de Vencimiento", "Estado"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Fecha de Vencimiento", text="Fecha de Vencimiento")
    tree.heading("Estado", text="Estado")

    # Establecer tamaños fijos para las columnas
    tree.column("Nombre", width=50)
    tree.column("Fecha de Vencimiento", width=50)
    tree.column("Estado", width=50)
    tree.place(x=30, y=70, width=440, height=220)

    combo = ttk.Combobox(ventana_asociar, background="#158c81", font=fuente_boton, state="readonly")
    combo.set("Seleccionar Usuario 1: ")
    combo.bind("<<ComboboxSelected>>", on_select)
    combo.place(x=510, y=90, width=190, height=40)

    combo2 = ttk.Combobox(ventana_asociar, background="#158c81", font=fuente_boton, state="readonly")
    combo2.set("Seleccionar Usuario 2: ")
    combo2.bind("<<ComboboxSelected>>", on_select_2)
    combo2.place(x=510, y=160, width=190, height=40)

    # Botón para cargar la lista de tareas
    btn_cargar_tareas = tk.Button(ventana_asociar, text="MOSTRAR LISTA DE TAREAS", font=fuente_boton, foreground="white", background="#158c81", command=cargar_lista_tareas)
    btn_cargar_tareas.place(x=70, y=305, width=210, height=40)

    btn_sociarUsuario = tk.Button(ventana_asociar, text="ASOCIAR USUARIO/OS", font=fuente_boton, foreground="white", background="#158c81", command=asociar_usuarios)
    btn_sociarUsuario.place(x=500, y=230, width=210, height=40)

    btn_cancelar = tk.Button(ventana_asociar, text="CANCELAR", font=fuente_boton, foreground="white", background="#072c2c", command=btn_volver)
    btn_cancelar.place(x=300, y=305, width=110, height=40)

    cargar_usuarios()

    ventana_asociar.geometry("735x360")
    ventana_asociar.resizable(False, False)

    ventana_asociar.mainloop()
