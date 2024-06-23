import tkinter as tk
from tkinter import ttk, font
from PIL import Image, ImageTk
import mysql.connector
import menu_principal

def ventana_marcarCompletada():
    def on_select(event):
        selected_value = combo.get()
        print(f"Seleccionar Prioridad: {selected_value}")
    
    def btn_volver():
        ventana_marcarTareaCompletada.destroy()
        menu_principal.ventana_menuPrincipal()
        
    def cargar_lista_tareas():
        # Realiza la conexión a la base de datos y ejecuta la consulta para obtener la lista de tareas
        conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
        cursor = conexion.cursor()

        # Consulta SQL para obtener la lista de tareas con detalles
        consulta = "SELECT nombre, estado FROM tareas"
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
    
    def marcar_como_completada():
        # Obtiene la tarea seleccionada en el Treeview
        selected_item = tree.selection()
        if selected_item:
            # Obtiene la fila seleccionada en el Treeview
            item_values = tree.item(selected_item, "values")
            tarea_nombre = item_values[0]  # Nombre de la tarea
            tarea_estado = item_values[1]  # Estado de la tarea

            if tarea_estado != "Completado":
                # Realiza la conexión a la base de datos y actualiza el estado de la tarea
                conexion = mysql.connector.connect(host="localhost", user="root", password="", port=3307, database="gestion_tareas")
                cursor = conexion.cursor()

                # Actualiza el estado de la tarea a "Completado"
                update_query = "UPDATE tareas SET estado = 'Completado' WHERE nombre = %s"
                cursor.execute(update_query, (tarea_nombre,))

                # Realiza el commit para aplicar los cambios en la base de datos
                conexion.commit()

                # Cierra la conexión a la base de datos
                cursor.close()
                conexion.close()

                # Vuelve a cargar la lista de tareas después de la actualización
                cargar_lista_tareas()
            else:
                print("La tarea ya está marcada como completada.")
                
    ventana_marcarTareaCompletada = tk.Toplevel()
    ventana_marcarTareaCompletada.title("Marcar Tareas como Completas")
    
    fuente_titulo = font.Font(family="Lemon", size=17)
    fuente_boton = font.Font(family="Oswald", size=14)

    
    imagen_fondo = Image.open("imagenes/fondoMarcarCompletado.png")
    imagen_fondo = ImageTk.PhotoImage(imagen_fondo)
    
    canvas = tk.Canvas(ventana_marcarTareaCompletada, width=744, height=500)
    canvas.grid(row=0, column=0)
    canvas.create_image(0, 0, anchor=tk.NW, image=imagen_fondo)
        
    color_fondo_label = "#12225c"
    label_titulo = tk.Label(ventana_marcarTareaCompletada, text="MARCAR TAREA COMO COMPLETADA", font=fuente_titulo, background=color_fondo_label, foreground="white")
    label_titulo.place(x=30, y=20)   
        
    btn_cancelar = tk.Button(ventana_marcarTareaCompletada, text="CANCELAR", font=fuente_boton, foreground="white", background="#158c81", command=btn_volver)
    btn_cancelar.place(x=390, y=260, width=110, height=40)    
        
    # Crear un Treeview para mostrar la lista de tareas
    tree = ttk.Treeview(ventana_marcarTareaCompletada, columns=("Nombre", "Estado"), show="headings")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Estado", text="Estado")

    # Establecer tamaños fijos para las columnas
    tree.column("Nombre", width=100)
    tree.column("Estado", width=100)
    tree.place(x=30, y=70, width=270, height=220)
    
    opcion_completado = ["Completado"]
    combo = ttk.Combobox(ventana_marcarTareaCompletada, values=opcion_completado, background="#158c81", font=fuente_boton, state="reandonly") 
    combo.set("Marcar como COMPLETADO: ")
    
    combo.bind("<<ComboboxSelected>>", on_select)
    combo.place(x=330, y=140, width=225, height=40)
        
    # Botón para cargar la lista de tareas
    btn_cargar_tareas = tk.Button(ventana_marcarTareaCompletada, text="CARGAR LISTA DE TAREAS", font=fuente_boton, foreground="white", background="#158c81", command=cargar_lista_tareas)
    btn_cargar_tareas.place(x=75, y=305, width=190, height=40)
    
    btn_completar_tarea = tk.Button(ventana_marcarTareaCompletada, text="COMPLETAR TAREA", font=fuente_boton, foreground="white", background="#165955", command=marcar_como_completada)
    btn_completar_tarea.place(x=350, y=200, width=190, height=40)
   
    ventana_marcarTareaCompletada.geometry("600x370")
    ventana_marcarTareaCompletada.resizable(False, False)

    ventana_marcarTareaCompletada.mainloop()
