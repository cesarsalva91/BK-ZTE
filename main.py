from backup_zte import hacer_backup_zte
from equipos_json import (
    crear_json_desde_excel,
    cargar_equipos_desde_json,
    eliminar_equipo_de_json
)

MAX_INTENTOS = 3

def ejecutar_backups():
    for intento in range(1, MAX_INTENTOS + 1):
        print(f"\n===== EJECUCION #{intento} =====")
        equipos = cargar_equipos_desde_json()
        
        if not equipos:
            print(" Todos los backups se completaron con éxito.")
            return

        for equipo in equipos[:]:  # [:] para trabajar sobre una copia
            if equipo["marca"].upper() == "ZTE":
                exito = hacer_backup_zte(
                    nombre=equipo["nombre"],
                    ip=equipo["ip"],
                    usuario=equipo["usuario"],
                    contrasena=equipo["contrasena"]
                )
                if exito is True:
                    eliminar_equipo_de_json(equipo["nombre"])

    # Si después de los intentos aún quedan equipos
    equipos_restantes = cargar_equipos_desde_json()
    if equipos_restantes:
        print("\n Los siguientes equipos no pudieron realizar backup:")
        for eq in equipos_restantes:
            print(f" - {eq['nombre']} ({eq['ip']})")

if __name__ == "__main__":
    crear_json_desde_excel()  # JSON inicial solo si no existe
    ejecutar_backups()
