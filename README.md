# PROFORMA Dashboard V5

Dashboard BI basado en `Graficos Aportes Proforma.xlsm`, preparado para GitHub y Render.

## Estructura
- `backend/` API FastAPI + lectura XLSM
- `frontend/` React + Vite
- `data/` archivo XLSM fuente
- `render.yaml` configuración de despliegue
- `qa_v5.py` control previo al despliegue

## Local
Backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000`
Frontend: `cd frontend && npm install && npm run dev`

## Render
El `render.yaml` crea dos servicios: API y frontend estático. Configura las variables de entorno indicadas en el archivo.

## V5.7 — Visual BI
La versión V5.7 reconstruye los principales gráficos del Excel como gráficos web interactivos y responsivos. Incluye KPIs, comparativos 2025/2026, avance de objetivo, Pareto 80/20, oportunidad de crecimiento, rankings comerciales y tablas con búsqueda/paginación.
