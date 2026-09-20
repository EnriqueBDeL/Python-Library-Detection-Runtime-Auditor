import sys
import os
import site
import subprocess
import glob
import importlib
import importlib.metadata

class AuditorEntornoPython:
    def __init__(self):
        self.modulos_estandar = []
        self.paquetes_externos = []
        self.distribuciones_map = {}
        self.peso_total_bytes = 0
        self.rutas_busqueda = self.descubrir_rutas_site_packages()

    def descubrir_rutas_site_packages(self):
        rutas = []

        def agregar_ruta(p):
            if p and os.path.isdir(p):
                abs_p = os.path.abspath(p)
                if abs_p not in rutas:
                    rutas.append(abs_p)

        if not getattr(sys, "frozen", False):
            try:
                for p in site.getsitepackages():
                    agregar_ruta(p)
            except Exception:
                pass
            try:
                agregar_ruta(site.getusersitepackages())
            except Exception:
                pass
            for p in sys.path:
                if "site-packages" in p.lower() or "dist-packages" in p.lower():
                    agregar_ruta(p)

        if getattr(sys, "frozen", False) or not rutas:
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            for cmd in [["py", "-3", "-c"], ["python", "-c"]]:
                try:
                    code = "import site, sys; print('|'.join([p for p in site.getsitepackages() + [site.getusersitepackages()] + sys.path if p]))"
                    out = subprocess.check_output(cmd + [code], creationflags=flags, text=True, timeout=3).strip()
                    for item in out.split("|"):
                        if item and os.path.isdir(item) and ("site-packages" in item.lower() or "dist-packages" in item.lower()):
                            agregar_ruta(item)
                    if rutas:
                        break
                except Exception:
                    pass

            local_appdata = os.environ.get("LOCALAPPDATA", "")
            if local_appdata:
                for sp in glob.glob(os.path.join(local_appdata, "Programs", "Python", "Python3*", "Lib", "site-packages")):
                    agregar_ruta(sp)

            appdata = os.environ.get("APPDATA", "")
            if appdata:
                for sp in glob.glob(os.path.join(appdata, "Python", "Python3*", "site-packages")):
                    agregar_ruta(sp)

            for sp in glob.glob("C:/Python3*/Lib/site-packages") + glob.glob("C:/Program Files/Python3*/Lib/site-packages"):
                agregar_ruta(sp)

        return rutas

    def invalidar_cache(self):
        importlib.invalidate_caches()
        self.rutas_busqueda = self.descubrir_rutas_site_packages()

    def escanear_estandar(self):
        modulos = sorted(list(sys.stdlib_module_names))
        self.modulos_estandar = [(m, "Built-in / Core") for m in modulos]
        return self.modulos_estandar

    def escanear_externas(self):
        paquetes = []
        peso_acumulado = 0
        self.distribuciones_map = {}
        nombres_vistos = set()

        try:
            if self.rutas_busqueda:
                iter_dists = importlib.metadata.distributions(path=self.rutas_busqueda)
            else:
                iter_dists = importlib.metadata.distributions()
        except Exception:
            iter_dists = importlib.metadata.distributions()

        for pkg in iter_dists:
            try:
                nombre = pkg.metadata["Name"] if "Name" in pkg.metadata else "Desconocido"
                nombre_clave = nombre.lower()
                if nombre_clave in nombres_vistos:
                    continue
                nombres_vistos.add(nombre_clave)
                self.distribuciones_map[nombre_clave] = pkg

                version = pkg.version if pkg.version else "?"
                tamano_pkg = 0

                if pkg.files:
                    for archivo in pkg.files:
                        try:
                            ruta = pkg.locate_file(archivo)
                            tamano_pkg += os.path.getsize(ruta)
                        except (OSError, TypeError):
                            pass

                peso_acumulado += tamano_pkg
                resumen = pkg.metadata.get("Summary", "") or "Paquete Python"
                paquetes.append((nombre, version, tamano_pkg, resumen))
            except Exception:
                continue

        paquetes.sort(key=lambda x: x[0].lower())
        self.paquetes_externos = paquetes
        self.peso_total_bytes = peso_acumulado
        return self.paquetes_externos, self.peso_total_bytes

    def obtener_distribucion(self, nombre):
        if not nombre:
            return None
        nombre_clave = nombre.strip().lower()
        if nombre_clave in self.distribuciones_map:
            return self.distribuciones_map[nombre_clave]
        try:
            if self.rutas_busqueda:
                dists = list(importlib.metadata.distributions(path=self.rutas_busqueda))
                for d in dists:
                    if d.metadata.get("Name", "").strip().lower() == nombre_clave:
                        return d
            return importlib.metadata.distribution(nombre)
        except Exception:
            return None

    def ejecutar_auditoria_completa(self):
        self.invalidar_cache()
        self.escanear_estandar()
        self.escanear_externas()
        return {
            "estandar": self.modulos_estandar,
            "externas": self.paquetes_externos,
            "peso_total": self.peso_total_bytes
        }

    def filtrar(self, termino_busqueda=""):
        termino = termino_busqueda.strip().lower()

        if not termino:
            return self.modulos_estandar, self.paquetes_externos

        std_filtrados = [(nom, tipo) for nom, tipo in self.modulos_estandar if termino in nom.lower()]
        ext_filtrados = [
            (nom, ver, peso, res) 
            for nom, ver, peso, res in self.paquetes_externos 
            if termino in nom.lower() or termino in res.lower()
        ]
        return std_filtrados, ext_filtrados
