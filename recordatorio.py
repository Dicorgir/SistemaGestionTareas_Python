import datetime
import mysql.connector
from tkinter import messagebox


def alerta_recordatorio():
    # Establecer conexión a la base de datos
    db_connection = mysql.connector.connect(
        host="localhost",
        user="root",
        port=3307,
        password="",
        database="gestion_tareas"
    )
    cursor = db_connection.cursor()

    # Obtener la fecha actual
    fecha_actual = datetime.date.today()

    # Consultar tareas pendientes para hoy
    query = "SELECT nombre FROM tareas WHERE fecha_vencimiento = %s AND estado = 'Pendiente'"
    cursor.execute(query, (fecha_actual,))
    tareas_pendientes = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    cursor.close()
    db_connection.close()

    # Mostrar alerta si hay tareas pendientes
    if tareas_pendientes:
        mensaje = "Tareas pendientes para hoy:\n"
        for tarea in tareas_pendientes:
            mensaje += "- {}\n".format(tarea[0])

        messagebox.showwarning("Alerta", mensaje)
    else:
        messagebox.showinfo("Alerta", "No hay tareas pendientes para hoy.")
