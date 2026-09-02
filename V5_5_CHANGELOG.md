# V5.5 — Corrección final TypeScript / GitHub Pages

Corrige el error de Build frontend V5.4:
- El arreglo de KPIs de Oportunidad ahora se tipa explícitamente como `[string, string][]`, evitando TS2345 al hacer destructuring en `map`.
- Se conserva `vite-env.d.ts` para `import.meta.env.VITE_API_URL`.
- Se conserva ES2021 para `replaceAll`.
- Se conserva GitHub Actions con Node 24 y `npm install`.

Error corregido:
`TS2345: Argument of type '([k, t]: [string, string]) => JSX.Element' is not assignable ... string[][]`
