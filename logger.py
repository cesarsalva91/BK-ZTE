from datetime import datetime

LOG_FILE = "logs.txt"

def registrar_log(ip, mensaje, nivel="INFO"):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{fecha_hora}] [{nivel}] [{ip}] {mensaje}\n")