
import csv
from config import RUTA_BASE
import utilidades_csv as csv_util
import validaciones

def obtener_todas_las_carreras():
    """
    Recorre todos los CSV y devuelve una lista de diccionarios,
    cada uno representando una carrera.
    """
    archivos = csv_util.buscar_archivos_csv(RUTA_BASE)
    todas = []
    for ruta in archivos:
        filas, _ = csv_util.leer_csv(ruta)
        for f in filas:
            f["_archivo_origen"] = ruta  # Añadir de dónde vino
            todas.append(f)
    return todas

def buscar_carrera_por_id(id_buscar):
    """
    Busca una carrera por su ID en todos los CSV.
    Si la encuentra devuelve: (ruta_archivo, filas_del_archivo, campos, registro_encontrado)
    Si no la encuentra devuelve: (None, None, None, None)
    """
    archivos = csv_util.buscar_archivos_csv(RUTA_BASE)
    for ruta in archivos:
        filas, campos = csv_util.leer_csv(ruta)
        for fila in filas:
            if fila.get("id") == id_buscar:
                return ruta, filas, campos, fila
    return None, None, None, None

def agregar_carrera(ruta_csv, nuevo_registro):
    """
    Añade un nuevo registro a un CSV específico.
    Devuelve (True, "Mensaje éxito") o (False, "Mensaje error").
    """
    ok, msg = validaciones.validar_registro(nuevo_registro)
    if not ok:
        return False, f"Error de validación: {msg}"

    filas, campos = csv_util.leer_csv(ruta_csv)
    
    # Validar que los campos coincidan
    if set(campos) != set(nuevo_registro.keys()):
         return False, f"Los campos del registro no coinciden con las columnas del CSV."

    filas.append(nuevo_registro)
    
    if csv_util.escribir_csv(ruta_csv, filas, campos):
        return True, "Carrera añadida correctamente."
    else:
        return False, "Error al escribir en el archivo."

def editar_carrera(id_carrera, datos_actualizados):
    """
    Actualiza los datos de una carrera por su ID.
    Devuelve (True, "Mensaje éxito") o (False, "Mensaje error").
    """
    ruta, filas, campos, registro = buscar_carrera_por_id(id_carrera)
    if not ruta:
        return False, "ID de carrera no encontrado."

    # Actualizar el registro original (que es una referencia al objeto en 'filas')
    registro.update(datos_actualizados)
    
    ok, msg = validaciones.validar_registro(registro)
    if not ok:
        return False, f"Error de validación: {msg}"

    if csv_util.escribir_csv(ruta, filas, campos):
        return True, "Carrera actualizada."
    else:
        return False, "Error al guardar la actualización."


def eliminar_carrera(id_carrera):
    """
    Elimina una carrera por su ID.
    Devuelve (True, "Mensaje éxito") o (False, "Mensaje error").
    """
    ruta, filas, campos, registro = buscar_carrera_por_id(id_carrera)
    if not ruta:
        return False, "ID de carrera no encontrado."

    filas_nuevas = [f for f in filas if f.get("id") != id_carrera]
    
    if csv_util.escribir_csv(ruta, filas_nuevas, campos):
        return True, "Carrera eliminada."
    else:
        return False, "Error al guardar tras eliminar."


def calcular_estadisticas():
    """
    Calcula estadísticas sobre todas las carreras.
    Devuelve un diccionario con los resultados.
    """
    carreras = obtener_todas_las_carreras()
    total_carreras = 0
    total_cupos = 0
    total_duracion = 0
    
    for f in carreras:
        try:
            total_carreras += 1
            total_cupos += int(f.get("cupos_anuales", 0))
            total_duracion += int(f.get("duracion_anios", 0))
        except (ValueError, TypeError):
            pass # Ignorar filas con datos mal formateados

    if total_carreras == 0:
        return {"total_carreras": 0, "total_cupos": 0, "duracion_media": 0.0}

    duracion_media = round(total_duracion / total_carreras, 2)
    
    return {
        "total_carreras": total_carreras,
        "total_cupos": total_cupos,
        "duracion_media": duracion_media
    }

def exportar_consolidado(archivo_destino):
    """
    Exporta todas las carreras a un único CSV.
    Devuelve (True, "Mensaje éxito") o (False, "Mensaje error").
    """
    carreras = obtener_todas_las_carreras()
    if not carreras:
        return False, "No hay carreras para exportar."

    # Obtener todos los campos posibles, incluyendo _archivo_origen
    campos_unicos = set()
    for c in carreras:
        campos_unicos.update(c.keys())
    
    # Asegurar un orden consistente
    campos_ordenados = sorted(list(campos_unicos), key=lambda x: (x != 'id', x != 'nombre_carrera', x))

    try:
        with open(archivo_destino, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=campos_ordenados)
            escritor.writeheader()
            for fila in carreras:
                escritor.writerow(fila)
        return True, f"Exportado correctamente a {archivo_destino}"
    except Exception as e:
        return False, f"Error al exportar: {e}"