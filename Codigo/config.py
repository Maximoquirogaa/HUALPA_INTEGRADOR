#Aca almacenamos la s variables globales
import os

# Carpeta base donde están las carpetas por país/provincia/facultad.
RUTA_BASE = os.path.join(os.path.dirname(__file__), "Argentina")

# Modalidades permitidas para una carrera
MODALIDADES = {"Presencial", "Virtual", "Mixta"}