# PROFORMA Dashboard V5.3 FREE

## Corrección del build de Render

El log de V5.2 mostró que Render estaba ejecutando Python 3.14 (`/opt/render/project/src/.venv/bin/python3.14`). Eso provocó que `pydantic-core==2.33.1` intentara compilarse desde Rust y fallara por las restricciones del entorno de build.

V5.3 fija Python 3.11.11 de dos formas:
- `backend/.python-version`
- `PYTHON_VERSION=3.11.11` en `render.yaml`

## Render
- Root Directory: `backend`
- Runtime: Python 3
- Build Command: `pip install -r requirements.txt`
- Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Plan: Free
- Health Check: `/api/health`

## Importante
Después de subir esta versión a GitHub, en Render debe aparecer al inicio del build algo equivalente a:
`==> Using Python version 3.11.11`

Si vuelve a aparecer Python 3.14, no hay que continuar con el build: revisar la variable `PYTHON_VERSION` del servicio y hacer un nuevo deploy.
