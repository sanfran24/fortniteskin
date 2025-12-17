import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { copyFileSync } from 'fs'
import { join } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // Copy .htaccess to dist folder after build
    {
      name: 'copy-htaccess',
      closeBundle() {
        try {
          copyFileSync(
            join(__dirname, '.htaccess'),
            join(__dirname, 'dist', '.htaccess')
          )
          console.log('✅ Copied .htaccess to dist folder')
        } catch (err) {
          console.warn('⚠️  Could not copy .htaccess (file may not exist)')
        }
      },
    },
  ],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})

