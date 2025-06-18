import paramiko
import time
from datetime import datetime
from logger import registrar_log

def esperar_y_leer(shell, espera=2):
    time.sleep(espera)
    if shell.recv_ready():
        return shell.recv(65535).decode('utf-8', errors='ignore')
    return ""

def verificar_ping_desde_equipo(shell, ip_destino):
    shell.send(f"ping {ip_destino}\n")
    time.sleep(3)
    return esperar_y_leer(shell, 1)

def hacer_backup_zte(nombre, ip, usuario, contrasena):
    fecha = datetime.now().strftime("%d-%m-%y")
    id_sanitizado = nombre.replace(" ", "_")
    nombre_archivo = f"{id_sanitizado}_{fecha}.dat"
    comandos = [
        "config tffs",
        "cd cfg",
        f"tftp 10.243.0.220 upload startrun.dat /zte/{nombre_archivo}"
    ]

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=ip,
            port=22,
            username=usuario,
            password=contrasena,
            look_for_keys=False,
            allow_agent=False
        )
        registrar_log(ip, f"Conexión SSH exitosa ({nombre})")

        shell = ssh.invoke_shell()
        esperar_y_leer(shell)

        # Autenticación enable
        shell.send("enable\n")
        output = esperar_y_leer(shell, 1)

        if "Password" in output or "password" in output:
            shell.send(contrasena + "\n")
            output = esperar_y_leer(shell, 2)
            if "#" not in output:
                registrar_log(ip, f"Fallo autenticación modo enable ({nombre})", nivel="ERROR")
                shell.close()
                ssh.close()
                return
            registrar_log(ip, f"Autenticado en modo enable ({nombre})")
        else:
            registrar_log(ip, f"No se solicitó contraseña de enable ({nombre})", nivel="WARNING")

        # Verificación de conectividad hacia el servidor TFTP
        print(f"[*] Verificando conectividad desde {nombre} hacia 10.243.0.220...")
        ping_output = verificar_ping_desde_equipo(shell, "10.243.0.220")
        if not any(p in ping_output for p in ["Reply from", "bytes from", "!"]):
            print(f"[X] {nombre} no puede alcanzar al servidor TFTP (10.243.0.220). Backup omitido.")
            registrar_log(ip, f"{nombre} no puede alcanzar el servidor TFTP 10.243.0.220 tras enable", nivel="ERROR")
            shell.close()
            ssh.close()
            return
        else:
            print(f"[OK] {nombre} tiene conectividad con el servidor TFTP.")
            registrar_log(ip, f"{nombre} tiene conectividad hacia el servidor TFTP 10.243.0.220")

        # Ejecutar comandos
        for cmd in comandos:
            shell.send(cmd + "\n")
            espera = 5 if "tftp" in cmd else 2
            output = esperar_y_leer(shell, espera)

            primer_renglon = output.strip().split('\n')[0] if output else "Sin respuesta"
            registrar_log(ip, f"{nombre}: Comando: {cmd} | Salida: {primer_renglon}")

            if "tftp" in cmd:
                print(f"[DEBUG] Salida completa del comando TFTP en {nombre}:\n{output.strip()}")

                errores_detectados = ["error", "timeout", "parameter too much", "command not found"]
                if any(err in output.lower() for err in errores_detectados):
                    print(f"[X] Error al guardar el backup de {nombre} ({ip})")
                    registrar_log(ip, f"{nombre}: Falla en transferencia TFTP", nivel="ERROR")
                elif ".dat" in output or "completed" in output.lower():
                    print(f"[OK] Backup guardado correctamente: {nombre_archivo} ({ip})")
                    registrar_log(ip, f"Backup guardado como {nombre_archivo}")
                else:
                    print(f"[!] Resultado incierto para {nombre} ({ip}) → {output.strip()[:80]}")
                    registrar_log(ip, f"{nombre}: Respuesta TFTP incierta", nivel="WARNING")

        shell.close()
        ssh.close()

    except Exception as e:
        registrar_log(ip, f"{nombre}: Error durante el backup: {e}", nivel="ERROR")
        print(f"[X] Error inesperado en {nombre} ({ip}): {e}")
