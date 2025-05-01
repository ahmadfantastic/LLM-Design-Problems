import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    host: true, // or '0.0.0.0'
    proxy: {
      '/api': 'http://localhost:5000' // forward REST calls to Flask
    }
  }
})