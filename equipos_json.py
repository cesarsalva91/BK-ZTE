import json
import os
from dispositivos import cargar_equipos_desde_excel

RUTA_JSON = "equipos.json"

def crear_json_desde_excel():
    """Convierte el Excel en un JSON inicial con todos los equipos."""
    equipos = cargar_equipos_desde_excel()
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(equipos, f, indent=4, ensure_ascii=False)

def cargar_equipos_desde_json():
    """Carga equipos pendientes desde el JSON."""
    if not os.path.exists(RUTA_JSON):
        crear_json_desde_excel()
    with open(RUTA_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_equipos_json(equipos):
    """Sobrescribe el JSON con los equipos pendientes."""
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(equipos, f, indent=4, ensure_ascii=False)

def eliminar_equipo_de_json(nombre):
    """Elimina un equipo por nombre del JSON (sin importar mayúsculas/minúsculas)."""
    equipos = cargar_equipos_desde_json()
    equipos = [e for e in equipos if e["nombre"].lower() != nombre.lower()]
    guardar_equipos_json(equipos)
