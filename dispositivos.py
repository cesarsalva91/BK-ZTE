import pandas as pd

ARCHIVO_EQUIPOS_XLSX = "equipos.xlsx"

def cargar_equipos_desde_excel():
    try:
        # Cargar archivo Excel
        dataframe = pd.read_excel(ARCHIVO_EQUIPOS_XLSX)

        # Definir columnas obligatorias (tal como están en el Excel)
        columnas_requeridas = {"NOMBRE", "MARCA", "IP", "USUARIO", "CONTRASEÑA", "ID"}
        columnas_en_archivo = set(dataframe.columns)

        # Validar existencia de todas las columnas
        if not columnas_requeridas.issubset(columnas_en_archivo):
            columnas_faltantes = columnas_requeridas - columnas_en_archivo
            raise ValueError(f"[X] Faltan columnas requeridas en el archivo Excel: {columnas_faltantes}")

        # Convertir cada fila en un diccionario compatible con el sistema
        equipos = []
        for _, fila in dataframe.iterrows():
            equipo = {
                "nombre": fila["NOMBRE"],
                "marca": fila["MARCA"],
                "ip": fila["IP"],
                "usuario": fila["USUARIO"],
                "contrasena": fila["CONTRASEÑA"],
                "id": fila["ID"]
            }
            equipos.append(equipo)

        return equipos

    except FileNotFoundError:
        print(f"[X] No se encontró el archivo: {ARCHIVO_EQUIPOS_XLSX}")
        return []
    except Exception as error:
        print(f"[X] Error al procesar el archivo Excel: {error}")
        return []
