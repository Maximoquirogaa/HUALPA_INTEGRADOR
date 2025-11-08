# utilidades_csv.py
import os
import csv

def buscar_archivos_csv(raiz):
    """
    Recorre recursivamente la carpeta `raiz` y devuelve una lista con las
    rutas de todos los archivos que terminen en .csv
    """
    archivos = []
    for ruta_dir, dirs, files in os.walk(raiz):
        for nombre in files:
            if nombre.lower().endswith(".csv"):
                archivos.append(os.path.join(ruta_dir, nombre))
    return archivos


def leer_csv(ruta):
    """
    Lee un CSV y devuelve:
    - lista de diccionarios (filas)
    - lista de nombres de columnas (fieldnames)
    """
    try:
        with open(ruta, newline='', encoding='utf-8') as f:
            lector = csv.DictReader(f)
            filas = list(lector)
            campos = lector.fieldnames
        return filas, campos
    except FileNotFoundError:
        return [], []
    except Exception as e:
        print(f"Error al leer {ruta}: {e}")
        return [], []


def escribir_csv(ruta, filas, nombres_campos):
    """
    Escribe la lista de diccionarios `filas` en el archivo `ruta`
    usando `nombres_campos` como encabezado.
    """
    try:
        with open(ruta, 'w', newline='', encoding='utf-8') as f:
            escritor = csv.DictWriter(f, fieldnames=nombres_campos)
            escritor.writeheader()
            for fila in filas:
                escritor.writerow(fila)
        return True
    except Exception as e:
        print(f"Error al escribir {ruta}: {e}")
        return False