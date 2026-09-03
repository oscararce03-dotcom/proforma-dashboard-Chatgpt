# PROFORMA Dashboard V5.6

## Correcciones principales

- Corregida la autenticación inicial para usar por defecto:
  - Gerencia General: `gerencia` / `Proforma2026`
  - Gerencia Comercial: `comercial` / `Proforma2026`
- Mantiene variables de entorno de Render para reemplazar estas credenciales de prueba.
- Corregida la configuración CORS para la URL de GitHub Pages publicada.
- Agregado endpoint `/api/me` para reconocer el perfil autenticado.
- Menú diferenciado por perfil: Gerencia General y Gerencia Comercial.
- Implementada la pantalla `Validación Excel`, que faltaba en el renderizado.
- Implementada la pantalla `Control Excel vs BI` en el menú correspondiente.
- Backend actualizado a versión 5.6.0.
- Eliminada la duplicidad del endpoint `/api/health`.
- Se mantiene Python 3.11.11 para Render y el workflow de GitHub Pages con Node 24.

## Importante

Para producción, definir en Render `JWT_SECRET`, `ADMIN_USERNAME`, `ADMIN_PASSWORD` y `FRONTEND_URL`.
