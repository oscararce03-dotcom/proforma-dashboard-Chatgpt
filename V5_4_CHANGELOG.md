# V5.4 — Corrección GitHub Pages / TypeScript

Corrige los errores de Build frontend reportados por GitHub Actions:
- `import.meta.env` ahora tiene tipado Vite mediante `src/vite-env.d.ts`.
- TypeScript cambia a ES2021 para soportar `String.replaceAll`.
- Se agregan tipos explícitos en callbacks que estaban bajo `strict` (`implicit any`).
- Workflow GitHub Pages actualizado a Node 24.
- Se elimina el caché npm que estaba fallando por ausencia de `package-lock.json`.
- El entorno `github-pages` queda asociado al job de deploy, no al job de build.

## Build esperado
`npm install` → `npm run build` → upload artifact → deploy GitHub Pages.
