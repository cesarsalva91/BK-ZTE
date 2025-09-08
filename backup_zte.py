import paramiko
import time
import re
from datetime import datetime
from logger import registrar_log

def esperar_y_leer(shell, espera=2, cmd=None):
    time.sleep(espera)
    if shell.recv_ready():
        raw_output = shell.recv(65535).decode('utf-8', errors='ignore')

        # 🔹 Eliminar caracteres de control (backspace, tabs, etc.)
        limpio = re.sub(r'[\x00-\x1F\x7F]', '', raw_output)

        # 🔹 Si se pasa el comando, eliminarlo de la salida
        if cmd:
            limpio = limpio.replace(cmd, '')

        # 🔹 Normalizar espacios múltiples
        limpio = re.sub(r'\s+', ' ', limpio)

        return limpio.strip()
    return ""

def verificar_ping_desde_equipo(shell, ip_destino):
    shell.send(f"ping {ip_destino}\n")
    time.sleep(3)
    return esperar_y_leer(shell, 1, cmd=f"ping {ip_destino}")

def hacer_backup_zte(nombre, ip, usuario, contrasena):
    fecha = datetime.now().strftime("%d-%m-%y_%H:%M:%S")
    id_sanitizado = nombre.replace(" ", "_")
    nombre_archivo = f"{id_sanitizado}_{fecha}.dat"
    comandos = [
        "config tffs",
        "cd cfg",
        f"tftp 10.243.0.220 upload startrun.dat {nombre_archivo}"
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
        output = esperar_y_leer(shell, 1, cmd="enable")

        if "Password" in output or "password" in output:
            shell.send(contrasena + "\n")
            output = esperar_y_leer(shell, 2)
            if "#" not in output:
                registrar_log(ip, f"Fallo autenticación modo enable ({nombre})", nivel="ERROR")
                shell.close()
                ssh.close()
                return False
            registrar_log(ip, f"Autenticado en modo enable ({nombre})")
        else:
            registrar_log(ip, f"No se solicitó contraseña de enable ({nombre})", nivel="WARNING")

        # Obtener nombre real del equipo
        shell.send("show running-config\n")
        output_sys = esperar_y_leer(shell, 2, cmd="show running-config")

        nombre_equipo = "NO_DETECTADO"
        for line in output_sys.splitlines():
            if "hostname" in line.strip().lower():
                partes = line.strip().split()
                idx = [i for i, p in enumerate(partes) if p.lower() == "hostname"]
                if idx:
                    nombre_equipo = partes[idx[0] + 1].strip()
                    break


        print(f"[INFO] Nombre real detectado: {nombre_equipo}")
        registrar_log(ip, f"Nombre real detectado desde el equipo: {nombre_equipo}")

        # Verificación de conectividad
        print(f"[*] Verificando conectividad desde {nombre_equipo} hacia 10.243.0.220...")
        ping_output = verificar_ping_desde_equipo(shell, "10.243.0.220")
        if not any(p in ping_output for p in ["Reply from", "bytes from", "!"]):
            log = (f"[X] {nombre_equipo} no puede alcanzar al servidor TFTP (10.243.0.220). Backup omitido."
                   "\n***************************************************************\n")
            print(log)
            registrar_log(ip, log, nivel="ERROR")
            shell.close()
            ssh.close()
            return False
        else:
            print(f"[OK] {nombre_equipo} tiene conectividad con el servidor TFTP.")
            registrar_log(ip, f"{nombre_equipo} tiene conectividad hacia el servidor TFTP 10.243.0.220")

        # Ejecutar comandos
        for cmd in comandos:
            shell.send(cmd + "\n")
            espera = 5 if "tftp" in cmd else 2
            output = esperar_y_leer(shell, espera, cmd)

            primer_renglon = output.split('\n')[0] if output else "Sin respuesta"
            log_cmd = f"{nombre_equipo}: Comando: {cmd} | Salida: {primer_renglon}"
            registrar_log(ip, log_cmd)

            if "tftp" in cmd:
                print(f"[DEBUG] Salida completa del comando TFTP en {nombre_equipo}")

                errores_detectados = ["error", "timeout", "parameter too much", "command not found"]
                if any(err in output.lower() for err in errores_detectados):
                    log = (f"[X] Error al guardar el backup de {nombre_equipo} ({ip})"
                           "\n***************************************************************\n")
                    print(log)
                    registrar_log(ip, log, nivel="ERROR")
                    shell.close()
                    ssh.close()
                    return False

                elif "bytes uploaded" in output.lower():
                    log = (f"[OK] Backup guardado correctamente: {nombre_archivo} ({ip})"
                           "\n***************************************************************\n")
                    print(log)
                    registrar_log(ip, log)
                    shell.close()
                    ssh.close()
                    return True

                else:
                    log = (f"[!] Resultado incierto para {nombre_equipo} ({ip}) -> {output[:80]}"
                           "\n***************************************************************\n")
                    print(log)
                    registrar_log(ip, log, nivel="WARNING")
                    shell.close()
                    ssh.close()
                    return False

    except Exception as e:
        log = (f"[X] Error inesperado en {nombre} ({ip}): {e}"
               "\n***************************************************************\n")
        print(log)
        registrar_log(ip, log, nivel="ERROR")
        return False

