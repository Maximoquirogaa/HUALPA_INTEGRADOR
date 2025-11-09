
from config import MODALIDADES

def imprimir_menu():
    #Muestra el menú principal al usuario
    print("""\n--- Gestor de Carreras Universitarias ---
1) Listar todas las carreras
2) Añadir carrera
3) Editar carrera
4) Eliminar carrera
5) Ver estadísticas
6) Exportar consolidado
7) Salir
""")

def mostrar_mensaje(mensaje):
    #Muestra un mensaje simple (de éxito o error)
    print(mensaje)

def mostrar_carreras(carreras):
    #Recibe una lista de carreras y las imprime formateadass
    if not carreras:
        print("No se encontraron carreras.")
        return
    
    print("\n--- Listado de Carreras ---")
    for r in carreras:
        print(f'{r.get("id")} | {r.get("nombre_carrera", "").title()} | {r.get("duracion_anios")} años | '
              f'{r.get("cupos_anuales")} cupos | {r.get("modalidad")} | {r.get("_archivo_origen")}')

def mostrar_archivos_csv(archivos):
    #Muestra una lista numerada de archivos CS
    if not archivos:
        print("No hay archivos CSV en la estructura de carpetas.")
        return
    
    print("Elija un archivo CSV donde operar:")
    for i, ruta in enumerate(archivos, 1):
        print(f"{i}) {ruta}")

def mostrar_estadisticas(stats):
    #Recibe un diccionario de estadísticas y lo imprime
    if stats["total_carreras"] == 0:
        print("No hay datos para calcular estadísticas.")
        return
        
    print("\n--- Estadísticas ---")
    print(f"Total de carreras: {stats['total_carreras']}")
    print(f"Cupos totales: {stats['total_cupos']}")
    print(f"Duración media (años): {stats['duracion_media']:.2f}")

def mostrar_registro(registro):
    #Muestra un único registro (diccionario)
    print("Registro encontrado:")
    print(registro)

def pedir_campo(campo, valor_actual=None):
    #Función pedir un campo (para añadir o editar).
    if campo == "modalidad":
        prompt = f"{campo} (Opciones: {MODALIDADES})"
    else:
        prompt = f"{campo}"
    
    if valor_actual is not None:
        prompt += f" [{valor_actual}]"
    
    valor = input(f"{prompt}: ").strip()
    
    if campo == "modalidad" and valor:
        return valor.title()
    
    return valor
