import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  },
  build: {
    outDir: '../static/dist',
    assetsDir: 'assets',
    emptyOutDir: true,
  },
  server: {
    port: 8080,
    proxy: {
      '/api': 'http://127.0.0.1:8001',
      '/rest': 'http://127.0.0.1:8001',
      '/user': 'http://127.0.0.1:8001',
      '/admin': 'http://127.0.0.1:8001',
    }
  }
})
