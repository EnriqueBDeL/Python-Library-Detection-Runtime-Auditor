import time
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from Estructura.utils import obtener_ruta_recurso
from Estructura.texts import TEXTOS

def mostrar_pantalla_carga(idioma="es"):
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="#0B0F19")

    ruta_ico = obtener_ruta_recurso("app_icon.ico")
    if ruta_ico.exists():
        try:
            splash.iconbitmap(default=str(ruta_ico))
        except Exception:
            try:
                splash.iconbitmap(str(ruta_ico))
            except Exception:
                pass

    ancho_splash = 720
    alto_splash = 430
    x_pantalla = (splash.winfo_screenwidth() // 2) - (ancho_splash // 2)
    y_pantalla = (splash.winfo_screenheight() // 2) - (alto_splash // 2)
    splash.geometry(f"{ancho_splash}x{alto_splash}+{x_pantalla}+{y_pantalla}")

    ruta_img = obtener_ruta_recurso("splash_bg.png")
    foto_splash = None
    if ruta_img.exists():
        try:
            pil_img = Image.open(ruta_img).resize((720, 393), Image.Resampling.LANCZOS)
            foto_splash = ImageTk.PhotoImage(pil_img)
        except Exception:
            foto_splash = None

    if foto_splash:
        lbl_img = tk.Label(splash, image=foto_splash, bg="#0B0F19", bd=0)
        lbl_img.image = foto_splash
        lbl_img.pack(fill=tk.BOTH, expand=True)
    else:
        lbl_fallback = tk.Label(
            splash, 
            text="PYTHON LIBRARY DETECTION\nAUDITOR & SCANNER", 
            font=("Segoe UI", 18, "bold"), 
            fg="#38BDF8", 
            bg="#0B0F19"
        )
        lbl_fallback.pack(pady=60)

    marco_inferior = tk.Frame(splash, bg="#0B0F19", height=45)
    marco_inferior.pack(fill=tk.X, side=tk.BOTTOM, padx=15, pady=(0, 10))

    lbl_estado = tk.Label(
        marco_inferior, 
        text=TEXTOS[idioma]["splash_iniciando"], 
        font=("Segoe UI", 9), 
        fg="#94A3B8", 
        bg="#0B0F19", 
        anchor="w"
    )
    lbl_estado.pack(fill=tk.X, pady=(0, 4))

    progreso = ttk.Progressbar(marco_inferior, orient="horizontal", mode="determinate")
    progreso.pack(fill=tk.X)

    etapas = [
        (25, TEXTOS[idioma]["splash_iniciando"]),
        (60, TEXTOS[idioma]["splash_inspeccionando"]),
        (85, TEXTOS[idioma]["splash_optimizando"]),
        (100, TEXTOS[idioma]["splash_listo"])
    ]

    for val, texto in etapas:
        progreso["value"] = val
        lbl_estado.config(text=texto)
        splash.update()
        time.sleep(0.25)

    time.sleep(0.1)
    splash.destroy()
