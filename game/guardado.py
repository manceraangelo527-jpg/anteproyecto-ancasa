import json
import os

RUTA_GUARDADO = "savegame.json"


def existe_guardado():
    return os.path.exists(RUTA_GUARDADO)


def guardar_partida(estado, escena_actual_id, es_autosave=False):
    datos = {
        "escena_actual_id": escena_actual_id,
        "estado": estado,
        "autosave": es_autosave,
    }
    with open(RUTA_GUARDADO, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)
    return True


def cargar_partida():
    if not existe_guardado():
        return None
    with open(RUTA_GUARDADO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)