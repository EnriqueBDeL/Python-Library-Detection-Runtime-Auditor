# AGENT.md — Directrices, Reglas de Diseño y Arquitectura para Agentes de IA

Este documento establece las reglas obligatorias, principios arquitectónicos y estándares de diseño que cualquier agente de inteligencia artificial o desarrollador debe seguir al modificar, ampliar o mantener el proyecto **Python Library Detection & Runtime Auditor**.

---

## 📌 Metadatos del Proyecto

- **Nombre del Proyecto**: Python Library Detection & Runtime Auditor
- **Versión**: v1.0.0
- **Autor y Desarrollador Principal**: **EnriqueBDL**
- **Entorno de Desarrollo**: Python 3.10+, Tkinter / ttk, Pillow
- **Plataformas**: Windows (Principal), Linux / macOS (Compatible)
- **Herramientas de IA y Desarrollo**: Google Antigravity, Visual Studio Code, Gemini Pro

---

## 🛡️ Regla 1: Privacidad Absoluta y Filosofía 100% Offline

> [!CAUTION]
> **POLÍTICA DE PRIVACIDAD ESTRICTA (ZERO NETWORK / ZERO TELEMETRY)**
> La aplicación está diseñada como una herramienta de auditoría forense local. **Queda estrictamente prohibido introducir llamadas de red automáticas, telemetría, rastreo de uso o envío de datos de librerías a servidores remotos**.

1. **Inspección Exclusivamente Local**: Todo el análisis de librerías estándar y externas debe realizarse a través de las APIs nativas del intérprete (`sys.stdlib_module_names`, `importlib.metadata`) y del sistema de archivos local (`os.path`).
2. **Navegación Web Únicamente Bajo Acción Explícita del Usuario**: La única interacción con internet permitida es la apertura voluntaria del navegador web del sistema mediante `webbrowser.open()` cuando el usuario hace clic derecho y selecciona expresamente _"Ver en PyPI"_.

---

## 📁 Regla 2: Estructura de Archivos y Organización del Directorio

Cualquier nuevo módulo, activo o script debe ubicarse estrictamente en la carpeta correspondiente:

| Directorio        | Propósito y Contenido                                                                                                              |
| :---------------- | :--------------------------------------------------------------------------------------------------------------------------------- |
| **`Media/`**      | Recursos gráficos, imágenes, fondos (`splash_bg.png`), logotipos (`app_logo.png`) e iconos (`app_icon.ico`).                       |
| **`Estructura/`** | Código fuente modularizado de la aplicación (`config.py`, `texts.py`, `scanner.py`, `utils.py`, `splash.py`, `app.py`).            |
| **`Otros/`**      | Herramientas auxiliares, generadores de accesos directos (`create_shortcut.py`), scripts de compilación (`compilar_exe.bat`), etc. |
| **`Raíz (./)`**   | Exclusivamente el archivo de inicio limpio `main.py`, la documentación `README.md` y este archivo `AGENT.md`.                      |

---

## 🎨 Regla 3: Estándares de Diseño Visual y Experiencia de Usuario (UI/UX)

La aplicación debe mantener una estética visual impecable, moderna y de alto contraste:

1. **Paleta de Colores _Cyber Slate Dark_**:
   - Fondo Principal: `#0B0F19`
   - Paneles y Cabeceras: `#111827`
   - Tarjetas y Contenedores: `#1E293B` (Borde: `#334155`)
   - Textos: Blanco `#F8FAFC`, Atenuado `#94A3B8`, Secundario `#64748B`
   - Acentos: Cian `#38BDF8`, Azul `#0284C7`, Verde Esmeralda `#10B981`, Ámbar `#F59E0B`
2. **Tablas con Filas Alternas (_Zebra Striping_)**:
   - Filas pares: `#111827` | Filas impares: `#162032` | Selección: `#0369A1`
3. **Identidad de Marca e Iconos de Windows**:
   - Siempre debe configurarse `ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID` en Windows para evitar que la barra de tareas muestre el icono genérico de Python o la pluma de Tkinter.
   - La ventana debe cargar simultáneamente `iconbitmap("Media/app_icon.ico")` y `iconphoto(True, PhotoImage)`.
4. **Tarjetas Métricas (KPIs)**:
   - Toda información estadística clave debe presentarse en tarjetas destacadas en la parte superior.

---

## ⚡ Regla 4: Motor de Recarga Dinámica en Caliente (Hot-Reload)

1. **Invalidación Forzada de Caché**: Cada vez que se invoque la recarga o sincronización del entorno, es **obligatorio** ejecutar `importlib.invalidate_caches()`.
2. **Cálculo Preciso de Espacio**: El tamaño de los paquetes debe calcularse sumando el tamaño real en bytes de los archivos declarados en el manifiesto `dist.files` mediante `os.path.getsize(dist.locate_file(f))` con manejo seguro de excepciones (`OSError`).
3. **Filtrado Eficiente en Memoria**: El buscador en tiempo real debe filtrar los datos ya almacenados en memoria RAM sin re-escanear el disco innecesariamente.

---

## 🌐 Regla 5: Soporte Multi-Idioma (Bilingüe ES / EN)

1. **Cero Textos Hardcodeados en la UI**: Ninguna cadena de texto visible al usuario debe escribirse directamente en los componentes visuales de `app.py`.
2. **Centralización en `Estructura/texts.py`**: Todos los títulos, etiquetas, encabezados de columnas, mensajes de diálogo, menús contextuales y manuales deben definirse tanto en `es` como en `en`.
3. **Actualización Dinámica**: El cambio de idioma mediante `cambiar_idioma()` debe actualizar instantáneamente todos los widgets, encabezados de Treeview y el texto de la pestaña de Documentación sin necesidad de reiniciar la app.

---

## 📦 Regla 6: Compatibilidad con Empaquetado PyInstaller (.EXE)

1. **Resolución Universal de Rutas**: Nunca usar rutas relativas directas como `"./imagen.png"`. Se debe utilizar la función `obtener_ruta_recurso("nombre_archivo")` de `Estructura/utils.py`, la cual comprueba primero el directorio temporal `sys._MEIPASS` de PyInstaller y luego las carpetas `Media/` y raíz.
2. **Comando Estándar de Compilación**:
   ```powershell
   pyinstaller --noconsole --onefile --icon="Media/app_icon.ico" --add-data "Media;Media" --name="DLP" main.py
   ```

---

## ✍️ Regla 7: Firma de Autoría y Créditos

En todas las interfaces principales, cabeceras de módulos y documentación se debe preservar la firma del autor:

- **Desarrollado por EnriqueBDL**
