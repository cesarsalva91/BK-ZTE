from dispositivos import cargar_equipos
from backup_zte import hacer_backup_zte

equipos = cargar_equipos()

for equipo in equipos:
    if equipo["marca"].upper() == "ZTE":
        hacer_backup_zte(
            nombre=equipo["nombre"],
            ip=equipo["ip"],
            usuario=equipo["usuario"],
            contrasena=equipo["contrasena"]
        )
