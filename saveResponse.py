import json
from datetime import datetime
import os

def saveResponse(response):
    # Obtener la ruta del directorio del script actual
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Crear el directorio de backup si no existe
    backup_dir = os.path.join(current_dir, "backup")
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    # Obtener la fecha y hora actual en formato adecuado para el nombre del archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Crear el nombre del archivo con la fecha y hora
    filename = os.path.join(backup_dir, f"{timestamp}.json")

    # Guardar la respuesta en un archivo JSON
    with open(filename, 'w') as file:
        json.dump(response, file)

    return f"Respuesta guardada en el archivo {filename}"


def retrieveLastResponse():
    # Verificar si existe el directorio de backup
    if not os.path.exists("backup"):
        return None

    # Obtener la lista de archivos en el directorio de backup
    files = os.listdir("backup")
    
    # Filtrar solo archivos .json y ordenarlos por fecha de modificación (el más reciente primero)
    files = [file for file in files if file.endswith('.json')]
    files.sort(key=lambda x: os.path.getmtime(os.path.join("backup", x)), reverse=True)

    # Verificar si hay archivos en la lista
    if not files:
        return None

    # Abrir el archivo más reciente y cargar la respuesta
    with open(f"backup/{files[0]}", 'r') as file:
        response_list = json.load(file)

    # Devolver todos los mensajes menos el primero
    if response_list and isinstance(response_list, list) and len(response_list) > 1:
        return response_list[1:]  # Excluye el primer elemento
    else:
        return None

# Ejemplo de uso de la función
#last_response = retrieveLastResponse()
#last_response


# Ejemplo de uso de la función
#response = {"mensaje": "Hola, esto es una prueba", "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
#saveResponse(response)
