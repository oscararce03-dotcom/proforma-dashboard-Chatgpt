# PROFORMA Dashboard V5 — GitHub + Render

V5 agrega una capa de control de calidad para que el dashboard pueda comprobar la estructura del XLSM y reproducir totales críticos desde los registros.

## QA
- `/api/admin/qa`
- Pantalla **Control Excel vs BI**
- Hojas requeridas
- Totales independientes en Comp Aportes, Oportunidad de Crecimiento y 80/20
- Conteo de registros
- `qa_v5.py` para validar antes del deploy

## Deploy
1. Subir el contenido de este ZIP a un repositorio GitHub.
2. En Render usar el `render.yaml` incluido.
3. Backend: configurar `JWT_SECRET`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` y `FRONTEND_URL`.
4. Frontend: configurar `VITE_API_URL` con la URL pública del backend.

## Fuente
Se incluye el XLSM real dentro de `data/`. El archivo se lee con `keep_vba=True` y no se modifica.
