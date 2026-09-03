import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "Graficos Aportes Proforma.xlsm"

# Valores de prueba iniciales. En Render se recomienda reemplazarlos mediante
# variables de entorno (ADMIN_USERNAME, ADMIN_PASSWORD y JWT_SECRET).
JWT_SECRET = os.getenv("JWT_SECRET", "proforma-dashboard-v56-change-this-secret")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "gerencia")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "Proforma2026")
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://oscararce03-dotcom.github.io/proforma-dashboard-Chatgpt/").rstrip("/")
