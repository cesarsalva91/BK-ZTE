import json

RUTA_JSON = "equipos.json"

def cargar_equipos():
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def guardar_equipos(equipos):
    with open(RUTA_JSON, "w", encoding="utf-8") as f:
        json.dump(equipos, f, indent=4)

def agregar_equipo(marca, ip, usuario, contrasena):
    equipos = cargar_equipos()
    equipos.append({
        "marca": marca,
        "ip": ip,
        "usuario": usuario,
        "contrasena": contrasena
    })
    guardar_equipos(equipos)
