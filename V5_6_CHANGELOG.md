# PROFORMA Dashboard V5.6 — corrección Render

- Corregido el error de Render que estaba ejecutando Python 3.14 y compilando pydantic-core con Rust.
- Python 3.11.11 queda fijado en raíz y backend mediante `.python-version` y `runtime.txt`.
- Dependencias compatibles y estables para Python 3.11.
- Se eliminó la carga del XLSM durante el arranque del proceso; ahora el Excel se carga de forma diferida al primer endpoint que lo necesita, reduciendo riesgo de segmentation fault en Render Free.
- `reload` reinicia correctamente el procesador diferido.
- Se conserva la autenticación V5.6 y los perfiles Gerencia General / Gerencia Comercial.

## Credenciales de prueba
- Gerencia General: `gerencia` / `Proforma2026`
- Gerencia Comercial: `comercial` / `Proforma2026`

En producción, usar `JWT_SECRET`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` y `FRONTEND_URL` como variables de entorno en Render.
