import sys
sys.dont_write_bytecode = True

if sys.platform == "win32":
    import ctypes
    from Estructura.config import APP_ID_WINDOWS
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID_WINDOWS)
    except Exception:
        pass

import tkinter as tk
from Estructura.splash import mostrar_pantalla_carga
from Estructura.app import AppAuditorLibrerias

def main():
    mostrar_pantalla_carga(idioma="es")

    root = tk.Tk()
    app = AppAuditorLibrerias(root)
    root.mainloop()

if __name__ == "__main__":
    main()