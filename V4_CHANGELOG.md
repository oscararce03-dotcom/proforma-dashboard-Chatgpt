# PROFORMA Dashboard V4

## Objetivo
Validar antes de producción que el dashboard esté respaldado por el XLSM real y que no se estén inventando datos.

## Cambios
- Pantalla **Validación Excel**.
- Endpoint `/api/admin/validation`.
- Validación de hojas requeridas.
- Conteo de registros por hoja.
- Reporte `backend/app/validation_report.json`.
- Script `validate_v4.py`.
- Mejoras de robustez para lectura del XLSM.
- Se mantiene el archivo XLSM real dentro de `data/`.
- UI preparada para mostrar el estado de calidad de los datos.

## Criterio
Un error en una hoja requerida deja el estado global en `ERROR`.
