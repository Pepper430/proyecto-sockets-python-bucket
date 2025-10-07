import pandas as pd  # Se usa para leer y manipular datos de tablas, como las de Excel o CSV. La llamamos 'pd' por convención.
import json          # Sirve para crear y leer archivos en formato JSON.
import datetime      # Nos permite trabajar con fechas y horas, como obtener la hora actual.
import os            # Nos da herramientas para interactuar con el sistema operativo, como revisar la extensión de un archivo.

# --- SECCIÓN DE CONFIGURACIÓN ---
# Aquí definimos las variables principales que el script usa.
# Si queremos procesar otro archivo, solo tendríamos que cambiar el nombre aquí.

# Nombre del archivo que vamos a leer. Puede ser un .xlsx o un .csv.
archivo_entrada = 'datos_prueba.csv'
# Nombre del archivo que vamos a crear con el resultado.
archivo_salida = 'salida.json'

# --- LÓGICA PRINCIPAL DEL SCRIPT ---
# Imprimimos un mensaje en la consola para saber que el script ha comenzado.
print(f"Iniciando la conversión de '{archivo_entrada}'...")

# Usamos un bloque 'try...except' para manejar posibles errores de forma controlada.
# Si algo falla dentro del 'try', el programa no se cierra bruscamente, sino que ejecuta el 'except' correspondiente.
try:
    # Usamos la librería 'os' para separar el nombre del archivo de su extensión (ej: '.csv').
    nombre, extension = os.path.splitext(archivo_entrada)

    # Revisamos qué extensión tiene el archivo para saber cómo leerlo.
    if extension == '.xlsx':
        # Si la extensión es '.xlsx', usamos la función de pandas para leer archivos de Excel.
        df = pd.read_excel(archivo_entrada)
    elif extension == '.csv':
        # Si la extensión es '.csv', usamos la función para leer archivos CSV.
        # Añadimos 'encoding="latin-1"' porque Excel en Windows a menudo guarda los CSV con una codificación especial
        # que puede dar problemas con las tildes y caracteres como la 'ñ'.
        df = pd.read_csv(archivo_entrada, encoding='latin-1')
    else:
        # Si el archivo no es ni .xlsx ni .csv, detenemos el programa y mostramos un error.
        raise ValueError("Formato de archivo no soportado. Use .xlsx o .csv")

    # Verificamos si existe una columna llamada 'Fecha_Compra' en los datos.
    if 'Fecha_Compra' in df.columns:
        # Si existe, la convertimos a un formato de texto estándar ('Año-Mes-Día').
        # Esto es necesario porque el formato de fecha de pandas no es compatible con JSON directamente.
        df['Fecha_Compra'] = pd.to_datetime(df['Fecha_Compra']).dt.strftime('%Y-%m-%d')

    # Convertimos toda la tabla de datos (DataFrame) a una lista de diccionarios de Python.
    # El formato 'records' crea un diccionario por cada fila de la tabla.
    datos_extraidos = df.to_dict(orient='records')

    # Creamos un diccionario para la metadata, que es información sobre el proceso de conversión.
    metadata = {
        'fuente_original': archivo_entrada,  # Guardamos el nombre del archivo original.
        'fecha_conversion': datetime.datetime.now().isoformat(),  # Guardamos la fecha y hora exactas de la conversión.
        'registros_procesados': len(datos_extraidos)  # Contamos cuántas filas (registros) se procesaron.
    }

    # Creamos el diccionario final que contendrá toda la estructura del JSON.
    json_final = {
        'metadata': metadata,  # La sección de metadata.
        'datos': datos_extraidos  # La sección con los datos de la tabla.
    }

    # Abrimos (o creamos si no existe) el archivo de salida en modo escritura ('w').
    # 'encoding="utf-8"' asegura que se guarden bien los caracteres especiales como las tildes.
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        # Usamos la librería 'json' para volcar ('dump') nuestro diccionario final en el archivo.
        # 'indent=4' hace que el archivo JSON se vea ordenado y legible para los humanos.
        # 'ensure_ascii=False' también ayuda a que los caracteres en español se guarden correctamente.
        json.dump(json_final, f, indent=4, ensure_ascii=False)

    # Si todo ha ido bien, imprimimos un mensaje de éxito.
    print(f"¡Éxito! El archivo '{archivo_salida}' ha sido creado correctamente.")

# --- SECCIÓN DE MANEJO DE ERRORES ---
# Si ocurre un error en el bloque 'try', el programa saltará a una de estas secciones.

except FileNotFoundError:
    # Este error ocurre si el 'archivo_entrada' no se encuentra en la misma carpeta que el script.
    print(f"Error: No se encontró el archivo '{archivo_entrada}'. Asegúrate de que esté en la misma carpeta.")
except ValueError as ve:
    # Este error lo lanzamos nosotros mismos si el formato del archivo no es .xlsx o .csv.
    print(f"Error de formato: {ve}")
except Exception as e:
    # Este es un 'atrapa-todo' para cualquier otro error inesperado que pueda ocurrir durante la ejecución.
    print(f"Ocurrió un error inesperado: {e}")