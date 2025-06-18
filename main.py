from dispositivos import cargar_equipos_desde_excel
from backup_zte import hacer_backup_zte

equipos = cargar_equipos_desde_excel()

for equipo in equipos:
    if equipo["marca"].upper() == "ZTE":
        hacer_backup_zte(
            nombre=equipo["nombre"],
            ip=equipo["ip"],
            usuario=equipo["usuario"],
            contrasena=equipo["contrasena"]
        )
