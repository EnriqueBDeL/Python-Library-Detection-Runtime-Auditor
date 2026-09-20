import sys
from pathlib import Path

APP_NAME = "Python Library Detection"
APP_SUBTITLE = "Auditor & Inspector de Entorno de Ejecución"
APP_VERSION = "1.0.0"
APP_AUTHOR = "EnriqueBDL"
APP_ID_WINDOWS = "enriquebdl.python.library.detector.v2"

ROOT_DIR = Path(__file__).resolve().parent.parent
ESTRUCTURA_DIR = ROOT_DIR / "Estructura"
MEDIA_DIR = ROOT_DIR / "Media"
OTROS_DIR = ROOT_DIR / "Otros"

PALETA = {
    "BG_DARK": "#0B0F19",
    "BG_PANEL": "#111827",
    "BG_CARD": "#1E293B",
    "BORDER_CARD": "#334155",
    "TEXT_WHITE": "#F8FAFC",
    "TEXT_MUTED": "#94A3B8",
    "TEXT_SUB": "#64748B",
    "ACCENT_CYAN": "#38BDF8",
    "ACCENT_BLUE": "#0284C7",
    "ACCENT_GREEN": "#10B981",
    "ACCENT_ORANGE": "#F59E0B",
    "ROW_EVEN": "#111827",
    "ROW_ODD": "#162032",
    "ROW_SELECT": "#0369A1"
}
