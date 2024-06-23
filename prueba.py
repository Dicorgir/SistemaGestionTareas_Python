import tkinter as tk

def mostrar_seleccion():
    seleccion = ""
    for opcion, valor in opciones.items():
        seleccion += f"{opcion}: {'Seleccionado' if valor.get() else 'No seleccionado'}\n"
    etiqueta_resultado.config(text=seleccion)

root = tk.Tk()
root.title("Ejemplo de Checkbutton")

opciones = {
    "Opción 1": tk.BooleanVar(),
    "Opción 2": tk.BooleanVar(),
    "Opción 3": tk.BooleanVar()
}

for opcion, valor in opciones.items():
    checkbutton = tk.Checkbutton(root, text=opcion, variable=valor, command=mostrar_seleccion)
    checkbutton.pack(anchor="w")

etiqueta_resultado = tk.Label(root, text="")
etiqueta_resultado.pack()

root.mainloop()
