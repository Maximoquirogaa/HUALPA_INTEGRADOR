
import os
import sys
import prints
import controladores
from config import RUTA_BASE

def main():
    
    #Punto de entrada principal.
    #Verifica RUTA_BASE y ejecuta el bucle de menú.
    
    if not os.path.exists(RUTA_BASE):
        prints.mostrar_mensaje(f"Error: No se encontró la carpeta base: {RUTA_BASE}")
        prints.mostrar_mensaje("Asegúrese de que la carpeta 'Argentina' exista.")
        sys.exit(1)
        
    while True:
        prints.imprimir_menu()
        opcion = input("Opción: ").strip()
        
        match opcion:
            case "1":
                controladores.controlador_listar_carreras()
            case "2":
                controladores.controlador_agregar_carrera()
            case "3":
                controladores.controlador_editar_carrera()
            case "4":
                controladores.controlador_eliminar_carrera()
            case "5":
                controladores.controlador_estadisticas()
            case "6":
                controladores.controlador_exportar_consolidado()
            case "7":
                prints.mostrar_mensaje("Terminando programa... ¡Adiós!")
                break
            case _:
                prints.mostrar_mensaje("Opción inválida. Intente de nuevo.")

if __name__ == "__main__":
    main()
