import sys
import os
from pathlib import Path
from Estructura.config import ROOT_DIR, MEDIA_DIR, APP_AUTHOR

def obtener_ruta_recurso(nombre_archivo):
    if hasattr(sys, "_MEIPASS"):
        base_meipass = Path(sys._MEIPASS)
        p_media = base_meipass / "Media" / nombre_archivo
        if p_media.exists():
            return p_media
        return base_meipass / nombre_archivo

    p_media = MEDIA_DIR / nombre_archivo
    if p_media.exists():
        return p_media

    p_root = ROOT_DIR / nombre_archivo
    if p_root.exists():
        return p_root

    return p_media

def formatear_tamano(peso_bytes):
    if peso_bytes == 0:
        return "0 B"
    elif peso_bytes < 1024:
        return f"{peso_bytes} B"
    elif peso_bytes < 1024 * 1024:
        return f"{peso_bytes / 1024:.2f} KB"
    elif peso_bytes < 1024 * 1024 * 1024:
        return f"{peso_bytes / (1024 * 1024):.2f} MB"
    else:
        return f"{peso_bytes / (1024 * 1024 * 1024):.2f} GB"
