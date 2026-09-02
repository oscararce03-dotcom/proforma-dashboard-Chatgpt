import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "Graficos Aportes Proforma.xlsm"
JWT_SECRET = os.getenv("JWT_SECRET", "development-only-change-me")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
