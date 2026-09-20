TEXTOS = {
    "es": {
        "titulo_app": "Python Library Detection — Auditor & Inspector",
        "subtitulo_app": "Monitor dinámico de módulos nativos y paquetes externos • By EnriqueBDL",
        "btn_recargar": "🔄 Recargar Entorno",
        "tooltip_recargar": "Re-escanear librerías e invalidar caché (F5)",
        "btn_abrir_librerias": "📂 Abrir Carpeta de Librerías",
        "lbl_buscar": "Filtrar librerías:",
        "placeholder_buscar": "Escribe para filtrar en tiempo real...",
        "btn_limpiar": "✖",
        "tab_librerias": "📦 Gestor de Librerías",
        "tab_info": "📖 Documentación y Arquitectura",
        "kpi_std_titulo": "Librerías Estándar",
        "kpi_std_sub": "Nativas del Intérprete CPython",
        "kpi_ext_titulo": "Librerías Externas",
        "kpi_ext_sub": "Instaladas vía Pip / Conda",
        "kpi_peso_titulo": "Espacio en Disco",
        "kpi_peso_sub": "Ocupado en site-packages",
        "col_std_num": "#",
        "col_std_nombre": "Módulo Estándar",
        "col_std_tipo": "Tipo de Módulo",
        "col_ext_num": "#",
        "col_ext_nombre": "Paquete Externo",
        "col_ext_version": "Versión",
        "col_ext_peso": "Tamaño en Disco",
        "col_ext_resumen": "Descripción / Ubicación",
        "menu_copiar_nombre": "📋 Copiar Nombre",
        "menu_copiar_todo": "📑 Copiar Datos del Paquete",
        "menu_abrir_carpeta": "📂 Abrir Carpeta en Explorador",
        "menu_pypi": "🌐 Ver en PyPI",
        "status_python": "Intérprete: Python {}",
        "status_version": "v{}",
        "status_actualizado": "Última sincronización: {}",
        "status_creditos": "Desarrollado por: EnriqueBDL",
        "msg_error_carpeta": "No se pudo abrir la carpeta: {}",
        "msg_no_site_packages": "No se encontró el directorio site-packages.",
        "msg_no_ubicacion": "No se pudo resolver la carpeta física de {}",
        "splash_iniciando": "Iniciando subsistemas y motor de detección...",
        "splash_inspeccionando": "Auditoría de módulos nativos y dependencias pip...",
        "splash_optimizando": "Generando índices de búsqueda y caché de memoria...",
        "splash_listo": "¡Entorno verificado correctamente!",
        "lang_label": "Idioma:",
        "doc_texto": """╔══════════════════════════════════════════════════════════════════════════════╗
║        MANUAL TÉCNICO Y ARQUITECTURA DEL SISTEMA — AUDITOR PYTHON PRO        ║
║                       Desarrollado por: EnriqueBDL                           ║
╚══════════════════════════════════════════════════════════════════════════════╝

1. ARQUITECTURA GENERAL Y POLÍTICA DE PRIVACIDAD STRICTA
─────────────────────────────────────────────────────────────────────────────
* 100% OFFLINE & PRIVADO: Esta aplicación NO realiza peticiones de red externas, no incluye telemetría y no envía datos fuera de su máquina. Todo el análisis se ejecuta localmente mediante llamadas nativas al intérprete y al sistema de archivos del sistema operativo.

┌─────────────────────────────────────────────────────────────────────────┐
│                    FLUJO DE AUDITORÍA LOCAL EN CALIENTE                 │
├──────────────────────────────────┬──────────────────────────────────────┤
│      LIBRERÍAS ESTÁNDAR          │         LIBRERÍAS EXTERNAS           │
│  sys.stdlib_module_names         │  importlib.metadata.distributions()  │
│  (Módulos C & Python nativos)    │  (site-packages / dist-info)         │
└────────────────┬─────────────────┴──────────────────┬───────────────────┘
                 │                                    │
                 ▼                                    ▼
       [ Filtro en Memoria ]               [ Cálculo de Peso Físico ]
                 │                         os.path.getsize(locate_file)
                 └────────────────┬───────────────────┘
                                  ▼
                   [ Tablas Treeview + KPIs en UI ]

2. MOTOR DE RECARGA EN CALIENTE (HOT-RELOAD & CACHE INVALIDATION)
─────────────────────────────────────────────────────────────────────────────
* PROBLEMA: Python mantiene en caché interna los metadatos de importación de los paquetes. Si instalas un paquete con 'pip install' en una terminal con la app abierta, Python no lo detectará.
* SOLUCIÓN: El botón '🔄 Recargar Entorno' (o tecla F5) invoca 'importlib.invalidate_caches()', limpiando los índices del Import Finder y re-escaneando el directorio 'site-packages' en tiempo real.

3. AUDITORÍA FORENSE DE TAMAÑO EN DISCO
─────────────────────────────────────────────────────────────────────────────
* Para cada paquete registrado, se obtiene su manifiesto de archivos mediante 'dist.files' (archivo RECORD en dist-info).
* Se resuelve la ubicación física con 'dist.locate_file(archivo)'.
* 'os.path.getsize()' evalúa el tamaño de archivos fuente (.py), extensiones compiladas en C (.pyd / .dll), activos estáticos y metadatos.
* Se formatea la métrica acumulada a unidades legibles (Bytes, KB, MB, GB).

4. ESTRUCTURA MODULAR DEL PROYECTO
─────────────────────────────────────────────────────────────────────────────
• main.py               : Punto de entrada principal y bootstrap de la app.
• Estructura/           : Código fuente modularizado (app.py, scanner.py, utils.py, texts.py, config.py, splash.py).
• Media/                : Recursos gráficos (app_logo.png, splash_bg.png, app_icon.ico).
• Otros/                : Herramientas de soporte y scripts de compilación.
"""
    },
    "en": {
        "titulo_app": "Python Library Detection — Runtime Auditor",
        "subtitulo_app": "Dynamic monitor for built-in modules and third-party packages • By EnriqueBDL",
        "btn_recargar": "🔄 Reload Environment",
        "tooltip_recargar": "Rescan libraries and invalidate cache (F5)",
        "btn_abrir_librerias": "📂 Open Libraries Folder",
        "lbl_buscar": "Filter libraries:",
        "placeholder_buscar": "Type to filter in real time...",
        "btn_limpiar": "✖",
        "tab_librerias": "📦 Library Manager",
        "tab_info": "📖 Documentation & Architecture",
        "kpi_std_titulo": "Standard Libraries",
        "kpi_std_sub": "CPython Native Built-in Modules",
        "kpi_ext_titulo": "External Packages",
        "kpi_ext_sub": "Installed via Pip / Conda",
        "kpi_peso_titulo": "Disk Storage",
        "kpi_peso_sub": "Occupied in site-packages",
        "col_std_num": "#",
        "col_std_nombre": "Standard Module",
        "col_std_tipo": "Module Type",
        "col_ext_num": "#",
        "col_ext_nombre": "External Package",
        "col_ext_version": "Version",
        "col_ext_peso": "Disk Size",
        "col_ext_resumen": "Summary / Location",
        "menu_copiar_nombre": "📋 Copy Name",
        "menu_copiar_todo": "📑 Copy Package Details",
        "menu_abrir_carpeta": "📂 Open Folder in Explorer",
        "menu_pypi": "🌐 View on PyPI",
        "status_python": "Interpreter: Python {}",
        "status_version": "v{}",
        "status_actualizado": "Last synced: {}",
        "status_creditos": "Developed by: EnriqueBDL",
        "msg_error_carpeta": "Could not open folder: {}",
        "msg_no_site_packages": "Could not find site-packages directory.",
        "msg_no_ubicacion": "Could not resolve physical folder for {}",
        "splash_iniciando": "Starting subsystems and detection engine...",
        "splash_inspeccionando": "Auditing native modules and pip dependencies...",
        "splash_optimizando": "Building live search indexes and memory cache...",
        "splash_listo": "Environment verified successfully!",
        "lang_label": "Language:",
        "doc_texto": """╔══════════════════════════════════════════════════════════════════════════════╗
║       TECHNICAL MANUAL & SYSTEM ARCHITECTURE — PYTHON AUDITOR PRO            ║
║                       Developed by: EnriqueBDL                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

1. GENERAL ARCHITECTURE & STRICT LOCAL PRIVACY POLICY
─────────────────────────────────────────────────────────────────────────────
* 100% OFFLINE & PRIVATE: This application performs ZERO network requests, includes zero telemetry, and never transmits data outside your machine. All auditing is executed locally via direct interpreter and filesystem calls.

┌─────────────────────────────────────────────────────────────────────────┐
│                        LOCAL AUDIT PIPELINE                             │
├──────────────────────────────────┬──────────────────────────────────────┤
│       STANDARD MODULES           │         EXTERNAL PACKAGES            │
│  sys.stdlib_module_names         │  importlib.metadata.distributions()  │
│  (Native C & Python modules)     │  (site-packages / dist-info)         │
└────────────────┬─────────────────┴──────────────────┬───────────────────┘
                 │                                    │
                 ▼                                    ▼
        [ In-Memory Filter ]                 [ Physical Size Audit ]
                 │                         os.path.getsize(locate_file)
                 └────────────────┬───────────────────┘
                                  ▼
                    [ Treeviews & Metric Cards ]

2. HOT-RELOAD & CACHE INVALIDATION ENGINE
─────────────────────────────────────────────────────────────────────────────
* PROBLEM: Python caches module import metadata in memory. Installing a package via 'pip install' during app runtime is ignored by default.
* SOLUTION: The '🔄 Reload Environment' action triggers 'importlib.invalidate_caches()', flushing obsolete finders and rebuilding live site-packages catalog.

3. DEEP DISK FOOTPRINT EVALUATION
─────────────────────────────────────────────────────────────────────────────
* Parses 'dist.files' manifest (RECORD in dist-info metadata).
* Resolves absolute filesystem paths with 'dist.locate_file(file)'.
* Evaluates total byte size across scripts, compiled extensions (.pyd/.dll), and static data.

4. MODULAR DIRECTORY LAYOUT
─────────────────────────────────────────────────────────────────────────────
• main.py               : Main entry point and bootstrap script.
• Estructura/           : Modular source code (app.py, scanner.py, utils.py, texts.py, config.py, splash.py).
• Media/                : Visual assets (app_logo.png, splash_bg.png, app_icon.ico).
• Otros/                : Support tools and compilation scripts.
"""
    }
}
