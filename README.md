# 🛠️ ZTE Backup

Sistema automatizado para realizar respaldos de configuración en switches **ZTE** vía **SSH** y transferencia mediante **TFTP**, utilizando Python y `paramiko`. Diseñado para facilitar tareas de mantenimiento, prevenir pérdidas de configuración y asegurar la trazabilidad mediante archivos de log estructurados.

---

## 📌 Descripción general

Este sistema se conecta a cada equipo listado en un archivo **Excel (.xlsx)**, se autentica por SSH, accede al modo `enable`, verifica conectividad con el servidor TFTP y ejecuta una copia del archivo `startrun.dat` hacia un servidor remoto. Toda la actividad (mensajes de consola y errores) se registra automáticamente en el archivo `logs.txt`.

---

## 📊 Formato del archivo `equipos.xlsx`

El archivo Excel debe estar ubicado en el mismo directorio que los scripts de Python y debe llamarse `equipos.xlsx`. Este contiene los datos de conexión de cada equipo.

### 📋 Estructura esperada:

El archivo debe contener las siguientes columnas con nombres exactos (sin errores tipográficos ni espacios adicionales):

| NOMBRE           | MARCA | IP           | USUARIO | CONTRASEÑA | ID       |
|------------------|-------|--------------|---------|------------|----------|

### 🧩 Descripción de las columnas:

- **NOMBRE**: Nombre descriptivo del equipo (alias o ubicación).
- **MARCA**: Marca del switch (actualmente soportado: "ZTE").
- **IP**: Dirección IP del dispositivo.
- **USUARIO**: Usuario habilitado para iniciar sesión SSH.
- **CONTRASEÑA**: Contraseña del usuario SSH.
- **ID**: Identificador único del equipo (utilizado para nombrar los archivos de backup).

> ⚠️ Todas las columnas son obligatorias. Si alguna está ausente o vacía, el sistema mostrará un error.

### ✅ Recomendaciones:

- Evitar celdas vacías.
- No modificar los nombres de las columnas.
- Guardar el archivo en formato **Excel (.xlsx)**.

---

## ⚙️ Requisitos del sistema

- Python 3.8 o superior
- Acceso de red a los switches y al servidor TFTP
- Librerías necesarias:

```bash
pip install paramiko openpyxl
```

---

## 🚀 Funcionamiento del sistema

1. Lee los datos desde el archivo `equipos.xlsx`.
2. Se conecta por SSH a cada dispositivo.
3. Autentica y accede al modo `enable`.
4. Extrae el `hostname` desde la configuración (`running-config`).
5. Verifica la conectividad con el servidor TFTP.
6. Realiza el respaldo mediante TFTP y guarda el archivo en `/zte/{equipo}_{fecha}.dat`.
7. Registra todas las operaciones y estados en consola y en el archivo `logs.txt`.

---

## 🔐 Seguridad

- Las credenciales de los dispositivos son manejadas en memoria y no se almacenan en disco.
- Se recomienda proteger el archivo `equipos.xlsx` mediante permisos adecuados y limitar el acceso físico y lógico al entorno de ejecución.

---

## ✅ Estado actual del desarrollo

- ✔️ Autenticación SSH
- ✔️ Acceso a modo enable
- ✔️ Extracción de hostname real
- ✔️ Transferencia TFTP y generación de backups
- ✔️ Registro completo en logs
- ✔️ Lectura dinámica desde archivo Excel

---

## 👤 Autor

**Cesar Salva**  
📧 cesarsalva91@gmail.com  
📍 Argentina  
🔗 LinkedIn - (https://www.linkedin.com/in/cesarsalva)

