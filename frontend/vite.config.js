import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // En desarrollo, las llamadas a /api van al backend FastAPI (uvicorn en :8000)
      '/api': 'http://localhost:8000',
    },
  },
  build: {
    // FastAPI sirve este build como archivos estaticos para la entrega/demo
    outDir: '../backend/static',
    emptyOutDir: true,
  },
})
