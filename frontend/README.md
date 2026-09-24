# Frontend — Viajes Aventura

React + Vite. Documentación completa del proyecto (negocio, reglas de negocio, arquitectura, cómo correrlo) en el [`README.md`](../README.md) de la raíz del repositorio.

## Desarrollo

```
npm install
npm run dev
```

Vite corre en `:5173` y su proxy (`vite.config.js`) reenvía `/api/*` al backend en `:8000`.

## Build

```
npm run build
```

Compila a `../backend/static/`, que FastAPI sirve como archivos estáticos para la entrega (ver README raíz, §6).
