
from config import MODALIDADES

def validar_registro(registro):
    #Validacion de
    # duracion_anios y cupos_anuales sean enteros > 0
    # modalidad esté en MODALIDADES
    # id y nombre_carrera no estén vacíos
    Devuelve (True, "") si OK, o (False, "mensaje") si hay error.
    try:
        dur = int(registro.get("duracion_anios", ""))
        cup = int(registro.get("cupos_anuales", ""))
        if dur <= 0 or cup <= 0:
            return False, "duracion_anios y cupos_anuales deben ser > 0"
    except Exception:
        return False, "duracion_anios y cupos_anuales deben ser enteros"

    if registro.get("modalidad") not in MODALIDADES:
        return False, f"modalidad debe ser una de {MODALIDADES}"

    if not registro.get("id") or not registro.get("nombre_carrera"):
        return False, "id y nombre_carrera no pueden estar vacíos"

    return True, ""
