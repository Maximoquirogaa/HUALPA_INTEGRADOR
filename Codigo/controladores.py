import gestor_carreras as gestor
import utilidades_csv as csv_util
import prints
from config import RUTA_BASE

def controlador_listar_carreras():
    """Obtiene las carreras y se las pasa a la vista."""
    carreras = gestor.obtener_todas_las_carreras()
    prints.mostrar_carreras(carreras)

def _controlador_seleccionar_csv():
    """
    Lógica para seleccionar un CSV.
    Devuelve la ruta seleccionada o None.
    """
    archivos = csv_util.buscar_archivos_csv(RUTA_BASE)
    prints.mostrar_archivos_csv(archivos)
    if not archivos:
        return None
    
    elec = input("Número (Enter para cancelar): ").strip()
    if not elec:
        return None
    try:
        idx = int(elec) - 1
        if 0 <= idx < len(archivos):
            return archivos[idx]
        else:
            prints.mostrar_mensaje("Selección inválida.")
            return None
    except Exception:
        prints.mostrar_mensaje("Selección inválida.")
        return None

def controlador_agregar_carrera():
    """Pide los datos para agregar una carrera."""
    ruta = _controlador_seleccionar_csv()
    if not ruta:
        return
    
    _, campos = csv_util.leer_csv(ruta)
    if not campos:
        prints.mostrar_mensaje("No se pudieron leer las columnas del archivo.")
        return

    prints.mostrar_mensaje(f"Añadiendo carrera en {ruta}. Ingrese los datos:")
    nuevo = {}
    for campo in campos:
        valor = prints.pedir_campo(campo)
        nuevo[campo] = valor

    ok, msg = gestor.agregar_carrera(ruta, nuevo)
    prints.mostrar_mensaje(msg)

def controlador_editar_carrera():
    """Pide el ID y los nuevos datos para editar."""
    id_ = input("ID de la carrera a editar: ").strip()
    ruta, _, campos, registro = gestor.buscar_carrera_por_id(id_)
    
    if not registro:
        prints.mostrar_mensaje("Carrera no encontrada.")
        return

    prints.mostrar_registro(registro)
    prints.mostrar_mensaje("Ingrese nuevos valores (deje vacío para no cambiar):")

    datos_actualizados = {}
    for campo in campos:
        if campo == "id":
            continue  # No permitir editar el id
        
        nuevo_valor = prints.pedir_campo(campo, registro.get(campo))
        
        if nuevo_valor:
            datos_actualizados[campo] = nuevo_valor

    if not datos_actualizados:
        prints.mostrar_mensaje("No se ingresaron cambios.")
        return

    ok, msg = gestor.editar_carrera(id_, datos_actualizados)
    prints.mostrar_mensaje(msg)


def controlador_eliminar_carrera():
    """Pide el ID y la confirmación para eliminar."""
    id_ = input("ID de la carrera a eliminar: ").strip()
    
    _, _, _, registro = gestor.buscar_carrera_por_id(id_)
    if not registro:
        prints.mostrar_mensaje("Carrera no encontrada.")
        return

    confirma = input(f"Confirmar eliminar '{registro.get('nombre_carrera')}' (ID: {id_}) [s/N]: ").strip().lower()
    
    if confirma != "s":
        prints.mostrar_mensaje("Eliminación cancelada.")
        return

    ok, msg = gestor.eliminar_carrera(id_)
    prints.mostrar_mensaje(msg)

def controlador_estadisticas():
    """Obtiene las estadísticas y se las pasa a la vista."""
    stats = gestor.calcular_estadisticas()
    prints.mostrar_estadisticas(stats)

def controlador_exportar_consolidado():
    """Pide el nombre de archivo y llama al gestor."""
    destino = input("Nombre de archivo de salida (ej: consolidado.csv): ").strip()
    if not destino:
        prints.mostrar_mensaje("Cancelado.")
        return
    
    if not destino.lower().endswith(".csv"):
        destino += ".csv"
        
    ok, msg = gestor.exportar_consolidado(destino)
    prints.mostrar_mensaje(msg)
