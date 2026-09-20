import sys
import os
import datetime
import webbrowser
import subprocess
import site
from pathlib import Path

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

from Estructura.config import PALETA, ROOT_DIR, APP_AUTHOR, APP_NAME, APP_VERSION
from Estructura.texts import TEXTOS
from Estructura.utils import obtener_ruta_recurso, formatear_tamano
from Estructura.scanner import AuditorEntornoPython

class AppAuditorLibrerias:
    def __init__(self, root):
        self.root = root
        self.idioma = "es"
        self.auditor = AuditorEntornoPython()

        self.root.title(TEXTOS[self.idioma]["titulo_app"])
        self.root.geometry("1180x750")
        self.root.minsize(980, 620)
        self.root.configure(bg=PALETA["BG_DARK"])

        self.configurar_iconos()
        self.configurar_estilos()

        self.crear_cabecera()
        self.crear_panel_kpi()
        self.crear_barra_herramientas()
        self.crear_pestanas()
        self.crear_barra_estado()

        self.crear_menu_contextual()
        self.configurar_atajos()

        self.recargar_entorno(notificar=False)

    def configurar_iconos(self):
        ruta_ico = obtener_ruta_recurso("app_icon.ico")
        ruta_logo = obtener_ruta_recurso("app_logo.png")

        icono_establecido = False
        if ruta_ico.exists():
            try:
                self.root.iconbitmap(default=str(ruta_ico))
                icono_establecido = True
            except Exception:
                try:
                    self.root.iconbitmap(str(ruta_ico))
                    icono_establecido = True
                except Exception:
                    pass

        if not icono_establecido and ruta_logo.exists():
            try:
                pil_logo = Image.open(ruta_logo).resize((64, 64), Image.Resampling.LANCZOS)
                self.foto_icono_tk = ImageTk.PhotoImage(pil_logo)
                self.root.iconphoto(True, self.foto_icono_tk)
            except Exception:
                pass

    def configurar_estilos(self):
        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "TNotebook", 
            background=PALETA["BG_DARK"], 
            borderwidth=0
        )
        self.style.configure(
            "TNotebook.Tab", 
            background=PALETA["BG_CARD"], 
            foreground="#CBD5E1", 
            padding=[18, 8], 
            font=("Segoe UI", 10, "bold"),
            borderwidth=0
        )
        self.style.map(
            "TNotebook.Tab", 
            background=[("selected", PALETA["ACCENT_BLUE"]), ("active", "#334155")],
            foreground=[("selected", "#FFFFFF"), ("active", "#FFFFFF")]
        )

        self.style.configure(
            "Custom.Treeview",
            background=PALETA["ROW_EVEN"],
            foreground=PALETA["TEXT_WHITE"],
            fieldbackground=PALETA["ROW_EVEN"],
            rowheight=28,
            font=("Segoe UI", 9),
            borderwidth=0
        )
        self.style.configure(
            "Custom.Treeview.Heading",
            background=PALETA["BG_CARD"],
            foreground=PALETA["ACCENT_CYAN"],
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padding=[6, 6]
        )
        self.style.map(
            "Custom.Treeview.Heading",
            background=[("active", "#334155")],
            foreground=[("active", "#FFFFFF")]
        )
        self.style.map(
            "Custom.Treeview",
            background=[("selected", PALETA["ROW_SELECT"])],
            foreground=[("selected", "#FFFFFF")]
        )

    def crear_cabecera(self):
        self.marco_cabecera = tk.Frame(self.root, bg=PALETA["BG_PANEL"], padx=16, pady=12, highlightthickness=1, highlightbackground=PALETA["BG_CARD"])
        self.marco_cabecera.pack(fill=tk.X)

        marco_logo_info = tk.Frame(self.marco_cabecera, bg=PALETA["BG_PANEL"])
        marco_logo_info.pack(side=tk.LEFT)

        ruta_logo = obtener_ruta_recurso("app_logo.png")
        if ruta_logo.exists():
            try:
                pil_logo = Image.open(ruta_logo).resize((54, 54), Image.Resampling.LANCZOS)
                self.foto_logo_header = ImageTk.PhotoImage(pil_logo)
                lbl_logo = tk.Label(marco_logo_info, image=self.foto_logo_header, bg=PALETA["BG_PANEL"], bd=0)
                lbl_logo.pack(side=tk.LEFT, padx=(0, 14))
            except Exception:
                pass

        marco_textos_header = tk.Frame(marco_logo_info, bg=PALETA["BG_PANEL"])
        marco_textos_header.pack(side=tk.LEFT)

        self.lbl_app_titulo = tk.Label(
            marco_textos_header, 
            text=TEXTOS[self.idioma]["titulo_app"], 
            font=("Segoe UI", 13, "bold"), 
            fg=PALETA["TEXT_WHITE"], 
            bg=PALETA["BG_PANEL"]
        )
        self.lbl_app_titulo.pack(anchor="w")

        self.lbl_app_sub = tk.Label(
            marco_textos_header, 
            text=TEXTOS[self.idioma]["subtitulo_app"], 
            font=("Segoe UI", 9), 
            fg=PALETA["TEXT_MUTED"], 
            bg=PALETA["BG_PANEL"]
        )
        self.lbl_app_sub.pack(anchor="w")

        marco_lang = tk.Frame(self.marco_cabecera, bg=PALETA["BG_PANEL"])
        marco_lang.pack(side=tk.RIGHT, padx=4)

        self.lbl_lang_txt = tk.Label(
            marco_lang, 
            text=TEXTOS[self.idioma]["lang_label"], 
            font=("Segoe UI", 9, "bold"), 
            fg=PALETA["TEXT_MUTED"], 
            bg=PALETA["BG_PANEL"]
        )
        self.lbl_lang_txt.pack(side=tk.LEFT, padx=(0, 6))

        self.btn_lang_es = tk.Button(
            marco_lang, 
            text="ES", 
            font=("Segoe UI", 9, "bold"), 
            bg=PALETA["ACCENT_BLUE"] if self.idioma == "es" else PALETA["BG_CARD"], 
            fg="#FFFFFF", 
            activebackground="#0369A1",
            activeforeground="#FFFFFF",
            relief=tk.FLAT, 
            padx=10, 
            pady=3,
            cursor="hand2",
            command=lambda: self.cambiar_idioma("es")
        )
        self.btn_lang_es.pack(side=tk.LEFT, padx=2)

        self.btn_lang_en = tk.Button(
            marco_lang, 
            text="EN", 
            font=("Segoe UI", 9, "bold"), 
            bg=PALETA["ACCENT_BLUE"] if self.idioma == "en" else PALETA["BG_CARD"], 
            fg="#FFFFFF", 
            activebackground="#0369A1",
            activeforeground="#FFFFFF",
            relief=tk.FLAT, 
            padx=10, 
            pady=3,
            cursor="hand2",
            command=lambda: self.cambiar_idioma("en")
        )
        self.btn_lang_en.pack(side=tk.LEFT, padx=2)

    def crear_panel_kpi(self):
        self.marco_kpi = tk.Frame(self.root, bg=PALETA["BG_DARK"], padx=16, pady=10)
        self.marco_kpi.pack(fill=tk.X)

        self.card_std = tk.Frame(self.marco_kpi, bg=PALETA["BG_CARD"], padx=14, pady=10, highlightthickness=1, highlightbackground=PALETA["BORDER_CARD"])
        self.card_std.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))

        self.lbl_kpi_std_tit = tk.Label(self.card_std, text=TEXTOS[self.idioma]["kpi_std_titulo"], font=("Segoe UI", 9), fg=PALETA["TEXT_MUTED"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_std_tit.pack(anchor="w")
        self.lbl_kpi_std_val = tk.Label(self.card_std, text="0", font=("Segoe UI", 17, "bold"), fg=PALETA["ACCENT_CYAN"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_std_val.pack(anchor="w")
        self.lbl_kpi_std_sub = tk.Label(self.card_std, text=TEXTOS[self.idioma]["kpi_std_sub"], font=("Segoe UI", 8), fg=PALETA["TEXT_SUB"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_std_sub.pack(anchor="w")

        self.card_ext = tk.Frame(self.marco_kpi, bg=PALETA["BG_CARD"], padx=14, pady=10, highlightthickness=1, highlightbackground=PALETA["BORDER_CARD"])
        self.card_ext.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=4)

        self.lbl_kpi_ext_tit = tk.Label(self.card_ext, text=TEXTOS[self.idioma]["kpi_ext_titulo"], font=("Segoe UI", 9), fg=PALETA["TEXT_MUTED"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_ext_tit.pack(anchor="w")
        self.lbl_kpi_ext_val = tk.Label(self.card_ext, text="0", font=("Segoe UI", 17, "bold"), fg=PALETA["ACCENT_GREEN"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_ext_val.pack(anchor="w")
        self.lbl_kpi_ext_sub = tk.Label(self.card_ext, text=TEXTOS[self.idioma]["kpi_ext_sub"], font=("Segoe UI", 8), fg=PALETA["TEXT_SUB"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_ext_sub.pack(anchor="w")

        self.card_peso = tk.Frame(self.marco_kpi, bg=PALETA["BG_CARD"], padx=14, pady=10, highlightthickness=1, highlightbackground=PALETA["BORDER_CARD"])
        self.card_peso.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(8, 0))

        self.lbl_kpi_peso_tit = tk.Label(self.card_peso, text=TEXTOS[self.idioma]["kpi_peso_titulo"], font=("Segoe UI", 9), fg=PALETA["TEXT_MUTED"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_peso_tit.pack(anchor="w")
        self.lbl_kpi_peso_val = tk.Label(self.card_peso, text="0 MB", font=("Segoe UI", 17, "bold"), fg=PALETA["ACCENT_ORANGE"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_peso_val.pack(anchor="w")
        self.lbl_kpi_peso_sub = tk.Label(self.card_peso, text=TEXTOS[self.idioma]["kpi_peso_sub"], font=("Segoe UI", 8), fg=PALETA["TEXT_SUB"], bg=PALETA["BG_CARD"])
        self.lbl_kpi_peso_sub.pack(anchor="w")

    def crear_barra_herramientas(self):
        self.marco_toolbar = tk.Frame(self.root, bg=PALETA["BG_DARK"], padx=16, pady=4)
        self.marco_toolbar.pack(fill=tk.X)

        self.btn_recargar = tk.Button(
            self.marco_toolbar,
            text=TEXTOS[self.idioma]["btn_recargar"],
            font=("Segoe UI", 10, "bold"),
            bg=PALETA["ACCENT_GREEN"],
            fg="#FFFFFF",
            activebackground="#059669",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=16,
            pady=6,
            cursor="hand2",
            command=self.recargar_entorno
        )
        self.btn_recargar.pack(side=tk.LEFT)

        self.btn_abrir_libs = tk.Button(
            self.marco_toolbar,
            text=TEXTOS[self.idioma]["btn_abrir_librerias"],
            font=("Segoe UI", 10, "bold"),
            bg=PALETA["ACCENT_BLUE"],
            fg="#FFFFFF",
            activebackground="#0369A1",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            padx=14,
            pady=6,
            cursor="hand2",
            command=self.abrir_carpeta_librerias
        )
        self.btn_abrir_libs.pack(side=tk.LEFT, padx=(10, 0))

        marco_search = tk.Frame(self.marco_toolbar, bg=PALETA["BG_CARD"], padx=6, pady=3, highlightthickness=1, highlightbackground=PALETA["BORDER_CARD"])
        marco_search.pack(side=tk.RIGHT)

        self.lbl_buscar = tk.Label(
            marco_search,
            text="🔍 " + TEXTOS[self.idioma]["lbl_buscar"],
            font=("Segoe UI", 9, "bold"),
            fg=PALETA["TEXT_MUTED"],
            bg=PALETA["BG_CARD"]
        )
        self.lbl_buscar.pack(side=tk.LEFT, padx=(4, 6))

        self.var_busqueda = tk.StringVar()
        self.var_busqueda.trace_add("write", lambda *args: self.filtrar_datos())

        self.entrada_busqueda = tk.Entry(
            marco_search,
            textvariable=self.var_busqueda,
            font=("Segoe UI", 10),
            bg=PALETA["BG_DARK"],
            fg=PALETA["TEXT_WHITE"],
            insertbackground=PALETA["ACCENT_CYAN"],
            relief=tk.FLAT,
            width=28
        )
        self.entrada_busqueda.pack(side=tk.LEFT, padx=4, ipady=3)

        btn_clear = tk.Button(
            marco_search,
            text="✖",
            font=("Segoe UI", 9, "bold"),
            bg=PALETA["BG_CARD"],
            fg=PALETA["TEXT_MUTED"],
            activebackground="#334155",
            activeforeground="#FFFFFF",
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            command=self.limpiar_busqueda
        )
        btn_clear.pack(side=tk.LEFT, padx=(2, 4))

    def crear_pestanas(self):
        self.cuaderno = ttk.Notebook(self.root, style="TNotebook")
        self.cuaderno.pack(fill=tk.BOTH, expand=True, padx=16, pady=(8, 4))

        self.tab_libs = tk.Frame(self.cuaderno, bg=PALETA["BG_DARK"])
        self.cuaderno.add(self.tab_libs, text=TEXTOS[self.idioma]["tab_librerias"])

        paned = tk.PanedWindow(self.tab_libs, orient=tk.HORIZONTAL, bg=PALETA["BG_DARK"], bd=0, sashwidth=6)
        paned.pack(fill=tk.BOTH, expand=True, pady=4)

        frame_std = tk.Frame(paned, bg=PALETA["BG_PANEL"], highlightthickness=1, highlightbackground=PALETA["BG_CARD"])
        paned.add(frame_std, stretch="always")

        header_std = tk.Frame(frame_std, bg=PALETA["BG_CARD"], padx=10, pady=6)
        header_std.pack(fill=tk.X)
        self.lbl_head_std = tk.Label(header_std, text="🐍 " + TEXTOS[self.idioma]["kpi_std_titulo"], font=("Segoe UI", 10, "bold"), fg=PALETA["ACCENT_CYAN"], bg=PALETA["BG_CARD"])
        self.lbl_head_std.pack(side=tk.LEFT)

        scroll_std_y = tk.Scrollbar(frame_std)
        scroll_std_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_std = ttk.Treeview(
            frame_std, 
            columns=("num", "nombre", "tipo"), 
            show="headings", 
            style="Custom.Treeview",
            yscrollcommand=scroll_std_y.set
        )
        self.tree_std.pack(fill=tk.BOTH, expand=True)
        scroll_std_y.config(command=self.tree_std.yview)

        self.tree_std.heading("num", text=TEXTOS[self.idioma]["col_std_num"])
        self.tree_std.heading("nombre", text=TEXTOS[self.idioma]["col_std_nombre"])
        self.tree_std.heading("tipo", text=TEXTOS[self.idioma]["col_std_tipo"])

        self.tree_std.column("num", width=45, minwidth=35, anchor="center")
        self.tree_std.column("nombre", width=180, minwidth=120)
        self.tree_std.column("tipo", width=120, minwidth=80)

        frame_ext = tk.Frame(paned, bg=PALETA["BG_PANEL"], highlightthickness=1, highlightbackground=PALETA["BG_CARD"])
        paned.add(frame_ext, stretch="always")

        header_ext = tk.Frame(frame_ext, bg=PALETA["BG_CARD"], padx=10, pady=6)
        header_ext.pack(fill=tk.X)
        self.lbl_head_ext = tk.Label(header_ext, text="📦 " + TEXTOS[self.idioma]["kpi_ext_titulo"], font=("Segoe UI", 10, "bold"), fg=PALETA["ACCENT_GREEN"], bg=PALETA["BG_CARD"])
        self.lbl_head_ext.pack(side=tk.LEFT)

        scroll_ext_y = tk.Scrollbar(frame_ext)
        scroll_ext_y.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_ext = ttk.Treeview(
            frame_ext, 
            columns=("num", "nombre", "version", "peso", "resumen"), 
            show="headings", 
            style="Custom.Treeview",
            yscrollcommand=scroll_ext_y.set
        )
        self.tree_ext.pack(fill=tk.BOTH, expand=True)
        scroll_ext_y.config(command=self.tree_ext.yview)

        self.tree_ext.heading("num", text=TEXTOS[self.idioma]["col_ext_num"])
        self.tree_ext.heading("nombre", text=TEXTOS[self.idioma]["col_ext_nombre"])
        self.tree_ext.heading("version", text=TEXTOS[self.idioma]["col_ext_version"])
        self.tree_ext.heading("peso", text=TEXTOS[self.idioma]["col_ext_peso"])
        self.tree_ext.heading("resumen", text=TEXTOS[self.idioma]["col_ext_resumen"])

        self.tree_ext.column("num", width=45, minwidth=35, anchor="center")
        self.tree_ext.column("nombre", width=160, minwidth=100)
        self.tree_ext.column("version", width=90, minwidth=70, anchor="center")
        self.tree_ext.column("peso", width=110, minwidth=90, anchor="e")
        self.tree_ext.column("resumen", width=220, minwidth=120)

        self.tree_std.tag_configure("even", background=PALETA["ROW_EVEN"])
        self.tree_std.tag_configure("odd", background=PALETA["ROW_ODD"])
        self.tree_ext.tag_configure("even", background=PALETA["ROW_EVEN"])
        self.tree_ext.tag_configure("odd", background=PALETA["ROW_ODD"])

        self.tab_doc = tk.Frame(self.cuaderno, bg=PALETA["BG_PANEL"], highlightthickness=1, highlightbackground=PALETA["BG_CARD"])
        self.cuaderno.add(self.tab_doc, text=TEXTOS[self.idioma]["tab_info"])

        marco_visor_doc = tk.Frame(self.tab_doc, bg=PALETA["BG_PANEL"])
        marco_visor_doc.pack(fill=tk.BOTH, expand=True)

        scroll_doc = tk.Scrollbar(marco_visor_doc)
        scroll_doc.pack(side=tk.RIGHT, fill=tk.Y)

        self.caja_doc = tk.Text(
            marco_visor_doc,
            font=("Consolas", 10),
            bg="#0F172A",
            fg="#E2E8F0",
            insertbackground=PALETA["ACCENT_CYAN"],
            padx=20,
            pady=18,
            relief=tk.FLAT,
            yscrollcommand=scroll_doc.set
        )
        self.caja_doc.pack(fill=tk.BOTH, expand=True)
        scroll_doc.config(command=self.caja_doc.yview)

        self.caja_doc.insert(tk.END, TEXTOS[self.idioma]["doc_texto"])
        self.caja_doc.config(state=tk.DISABLED)

    def abrir_carpeta_librerias(self):
        candidatos = [p for p in site.getsitepackages() if os.path.isdir(p) and "site-packages" in p]
        if not candidatos:
            user_site = site.getusersitepackages()
            if os.path.isdir(user_site):
                candidatos = [user_site]
            else:
                candidatos = [p for p in site.getsitepackages() if os.path.isdir(p)]

        if candidatos:
            ruta = candidatos[0]
            try:
                if sys.platform == "win32":
                    os.startfile(str(ruta))
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", str(ruta)])
                else:
                    subprocess.Popen(["xdg-open", str(ruta)])
            except Exception as e:
                messagebox.showerror("Error", TEXTOS[self.idioma]["msg_error_carpeta"].format(e))
        else:
            messagebox.showinfo("Python", TEXTOS[self.idioma]["msg_no_site_packages"])

    def crear_barra_estado(self):
        self.marco_status = tk.Frame(self.root, bg=PALETA["BG_PANEL"], padx=16, pady=6, highlightthickness=1, highlightbackground=PALETA["BG_CARD"])
        self.marco_status.pack(fill=tk.X, side=tk.BOTTOM)

        version_python = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.lbl_status_py = tk.Label(
            self.marco_status,
            text=TEXTOS[self.idioma]["status_python"].format(version_python),
            font=("Segoe UI", 9),
            fg=PALETA["TEXT_MUTED"],
            bg=PALETA["BG_PANEL"]
        )
        self.lbl_status_py.pack(side=tk.LEFT)

        self.lbl_status_sync = tk.Label(
            self.marco_status,
            text="",
            font=("Segoe UI", 9, "bold"),
            fg=PALETA["ACCENT_GREEN"],
            bg=PALETA["BG_PANEL"]
        )
        self.lbl_status_sync.pack(side=tk.RIGHT)

        self.lbl_status_creditos = tk.Label(
            self.marco_status,
            text=TEXTOS[self.idioma]["status_creditos"],
            font=("Segoe UI", 9, "bold"),
            fg=PALETA["ACCENT_CYAN"],
            bg=PALETA["BG_PANEL"]
        )
        self.lbl_status_creditos.pack(side=tk.RIGHT, padx=25)

        self.lbl_status_ver = tk.Label(
            self.marco_status,
            text=TEXTOS[self.idioma]["status_version"].format(APP_VERSION),
            font=("Segoe UI", 9, "bold"),
            fg=PALETA["TEXT_WHITE"],
            bg=PALETA["BG_PANEL"]
        )
        self.lbl_status_ver.pack(side=tk.LEFT, expand=True)

    def crear_menu_contextual(self):
        self.menu_contextual = tk.Menu(self.root, tearoff=0, bg=PALETA["BG_CARD"], fg=PALETA["TEXT_WHITE"], activebackground=PALETA["ACCENT_BLUE"], activeforeground="#FFFFFF")
        self.menu_contextual.add_command(label=TEXTOS[self.idioma]["menu_copiar_nombre"], command=self.copiar_nombre_seleccionado)
        self.menu_contextual.add_command(label=TEXTOS[self.idioma]["menu_copiar_todo"], command=self.copiar_datos_seleccionados)
        self.menu_contextual.add_separator()
        self.menu_contextual.add_command(label=TEXTOS[self.idioma]["menu_abrir_carpeta"], command=self.abrir_ubicacion_paquete)
        self.menu_contextual.add_command(label=TEXTOS[self.idioma]["menu_pypi"], command=self.abrir_en_pypi)

        self.tree_ext.bind("<Button-3>", self.mostrar_menu_contextual)
        self.tree_std.bind("<Button-3>", self.mostrar_menu_contextual_std)

    def mostrar_menu_contextual(self, event):
        item = self.tree_ext.identify_row(event.y)
        if item:
            self.tree_ext.selection_set(item)
            self.menu_contextual.post(event.x_root, event.y_root)

    def mostrar_menu_contextual_std(self, event):
        item = self.tree_std.identify_row(event.y)
        if item:
            self.tree_std.selection_set(item)
            menu_std = tk.Menu(self.root, tearoff=0, bg=PALETA["BG_CARD"], fg=PALETA["TEXT_WHITE"], activebackground=PALETA["ACCENT_BLUE"], activeforeground="#FFFFFF")
            menu_std.add_command(label=TEXTOS[self.idioma]["menu_copiar_nombre"], command=self.copiar_nombre_std_seleccionado)
            menu_std.post(event.x_root, event.y_root)

    def copiar_nombre_seleccionado(self):
        sel = self.tree_ext.selection()
        if sel:
            valores = self.tree_ext.item(sel[0])["values"]
            self.root.clipboard_clear()
            self.root.clipboard_append(str(valores[1]))

    def copiar_nombre_std_seleccionado(self):
        sel = self.tree_std.selection()
        if sel:
            valores = self.tree_std.item(sel[0])["values"]
            self.root.clipboard_clear()
            self.root.clipboard_append(str(valores[1]))

    def copiar_datos_seleccionados(self):
        sel = self.tree_ext.selection()
        if sel:
            valores = self.tree_ext.item(sel[0])["values"]
            linea = f"{valores[1]}=={valores[2]} ({valores[3]})"
            self.root.clipboard_clear()
            self.root.clipboard_append(linea)

    def abrir_en_pypi(self):
        sel = self.tree_ext.selection()
        if sel:
            valores = self.tree_ext.item(sel[0])["values"]
            nombre = valores[1]
            webbrowser.open(f"https://pypi.org/project/{nombre}/")

    def abrir_ubicacion_paquete(self):
        sel = self.tree_ext.selection()
        if not sel:
            return
        valores = self.tree_ext.item(sel[0])["values"]
        nombre = str(valores[1])
        
        try:
            dist = self.auditor.obtener_distribucion(nombre)
            if dist and dist.files:
                for f in dist.files:
                    try:
                        p = Path(dist.locate_file(f))
                        if p.exists():
                            directorio = p.parent
                            if sys.platform == "win32":
                                os.startfile(str(directorio))
                            elif sys.platform == "darwin":
                                subprocess.Popen(["open", str(directorio)])
                            else:
                                subprocess.Popen(["xdg-open", str(directorio)])
                            return
                    except Exception:
                        pass
        except Exception:
            pass
        messagebox.showinfo("Python", TEXTOS[self.idioma]["msg_no_ubicacion"].format(nombre))

    def configurar_atajos(self):
        self.root.bind("<F5>", lambda e: self.recargar_entorno())
        self.root.bind("<Control-r>", lambda e: self.recargar_entorno())
        self.root.bind("<Control-f>", lambda e: self.foco_buscador())

    def recargar_entorno(self, notificar=True):
        resultados = self.auditor.ejecutar_auditoria_completa()

        self.lbl_kpi_std_val.config(text=str(len(resultados["estandar"])))
        self.lbl_kpi_ext_val.config(text=str(len(resultados["externas"])))
        self.lbl_kpi_peso_val.config(text=formatear_tamano(resultados["peso_total"]))

        self.filtrar_datos()

        ahora = datetime.datetime.now().strftime("%H:%M:%S")
        self.lbl_status_sync.config(text=f"✔ {TEXTOS[self.idioma]['status_actualizado'].format(ahora)}")

    def filtrar_datos(self):
        termino = self.var_busqueda.get().strip()
        std_filtrados, ext_filtrados = self.auditor.filtrar(termino)

        self.tree_std.delete(*self.tree_std.get_children())
        self.tree_ext.delete(*self.tree_ext.get_children())

        idx_std = 1
        for nom, tipo in std_filtrados:
            tag = "even" if idx_std % 2 == 0 else "odd"
            self.tree_std.insert("", tk.END, values=(idx_std, nom, tipo), tags=(tag,))
            idx_std += 1

        idx_ext = 1
        for nom, ver, peso, res in ext_filtrados:
            tag = "even" if idx_ext % 2 == 0 else "odd"
            peso_fmt = formatear_tamano(peso)
            self.tree_ext.insert("", tk.END, values=(idx_ext, nom, ver, peso_fmt, res), tags=(tag,))
            idx_ext += 1

    def limpiar_busqueda(self):
        self.var_busqueda.set("")
        self.entrada_busqueda.focus()

    def foco_buscador(self):
        self.entrada_busqueda.focus()
        self.entrada_busqueda.select_range(0, tk.END)

    def cambiar_idioma(self, nuevo_idioma):
        self.idioma = nuevo_idioma
        t = TEXTOS[self.idioma]

        self.root.title(t["titulo_app"])
        self.lbl_app_titulo.config(text=t["titulo_app"])
        self.lbl_app_sub.config(text=t["subtitulo_app"])
        self.lbl_lang_txt.config(text=t["lang_label"])

        self.btn_lang_es.config(bg=PALETA["ACCENT_BLUE"] if self.idioma == "es" else PALETA["BG_CARD"])
        self.btn_lang_en.config(bg=PALETA["ACCENT_BLUE"] if self.idioma == "en" else PALETA["BG_CARD"])

        self.lbl_kpi_std_tit.config(text=t["kpi_std_titulo"])
        self.lbl_kpi_std_sub.config(text=t["kpi_std_sub"])
        self.lbl_kpi_ext_tit.config(text=t["kpi_ext_titulo"])
        self.lbl_kpi_ext_sub.config(text=t["kpi_ext_sub"])
        self.lbl_kpi_peso_tit.config(text=t["kpi_peso_titulo"])
        self.lbl_kpi_peso_sub.config(text=t["kpi_peso_sub"])

        self.btn_recargar.config(text=t["btn_recargar"])
        self.btn_abrir_libs.config(text=t["btn_abrir_librerias"])
        self.lbl_buscar.config(text="🔍 " + t["lbl_buscar"])

        self.cuaderno.tab(0, text=t["tab_librerias"])
        self.cuaderno.tab(1, text=t["tab_info"])

        self.lbl_head_std.config(text="🐍 " + t["kpi_std_titulo"])
        self.lbl_head_ext.config(text="📦 " + t["kpi_ext_titulo"])

        self.tree_std.heading("num", text=t["col_std_num"])
        self.tree_std.heading("nombre", text=t["col_std_nombre"])
        self.tree_std.heading("tipo", text=t["col_std_tipo"])

        self.tree_ext.heading("num", text=t["col_ext_num"])
        self.tree_ext.heading("nombre", text=t["col_ext_nombre"])
        self.tree_ext.heading("version", text=t["col_ext_version"])
        self.tree_ext.heading("peso", text=t["col_ext_peso"])
        self.tree_ext.heading("resumen", text=t["col_ext_resumen"])

        self.caja_doc.config(state=tk.NORMAL)
        self.caja_doc.delete(1.0, tk.END)
        self.caja_doc.insert(tk.END, t["doc_texto"])
        self.caja_doc.config(state=tk.DISABLED)

        version_python = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.lbl_status_py.config(text=t["status_python"].format(version_python))
        self.lbl_status_ver.config(text=t["status_version"].format(APP_VERSION))
        self.lbl_status_creditos.config(text=t["status_creditos"])

        ahora = datetime.datetime.now().strftime("%H:%M:%S")
        self.lbl_status_sync.config(text=f"✔ {t['status_actualizado'].format(ahora)}")

        self.filtrar_datos()
