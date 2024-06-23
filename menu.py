from interfaz import programa_con_interfaz

def main():
    while True:
        print("\n--- Menú ---")
        print("1. Abrir interfaz gráfica.")
        print("2. Salir.")
        
        opcion = input("Selecciona una opción: ")
     
        if opcion == "1":
            programa_con_interfaz()
            break 
        elif opcion == "2":
            print("Saliendo del programa")
            break
        else:
            print("Opción no válida. Inténtelo de nuevo.")

if __name__ == "__main__":
    main()