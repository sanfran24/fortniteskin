# Quick Render Setup Guide

## Option 1: Using render.yaml (Recommended)

If you have `render.yaml` in your repo root, Render will auto-detect it.

1. Push your code to GitHub
2. Go to Render Dashboard → **New** → **Blueprint**
3. Connect your GitHub repo
4. Render will detect `render.yaml` and create services automatically
5. Add environment variables in Render dashboard

## Option 2: Manual Setup

### Backend Setup

1. **New Web Service**
   - Connect GitHub repo
   - Name: `nano-banana-ta-backend`
   - Environment: `Python 3`
   - Build: `pip install -r backend/requirements.txt`
   - Start: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Root Directory: `backend` (optional)

2. **Environment Variables**
   ```
   GOOGLE_API_KEY=your_key_here
   GEMINI_MODEL=nano-banana-pro-preview
   PYTHON_VERSION=3.11.0
   ```

3. **Add Disk** (for cache persistence)
   - Name: `cache-disk`
   - Mount: `/opt/render/project/src/backend/cache`
   - Size: 1GB

### Frontend Setup

1. **New Static Site** (or Web Service)
   - Connect GitHub repo
   - Name: `nano-banana-ta-frontend`
   - Build: `cd frontend && npm install && npm run build`
   - Publish: `frontend/dist`

2. **Environment Variables**
   ```
   VITE_API_URL=https://nano-banana-ta-backend.onrender.com
   ```

## Domain Setup (Namecheap)

1. In Render frontend service → **Settings** → **Custom Domain**
2. Add: `yourdomain.com` and `www.yourdomain.com`
3. Render shows DNS records to add

4. In Namecheap → **Domain List** → **Manage** → **Advanced DNS**:
   - Add CNAME: `@` → `nano-banana-ta-frontend.onrender.com`
   - Add CNAME: `www` → `nano-banana-ta-frontend.onrender.com`
   - Save

5. Wait 15-30 minutes for DNS + SSL provisioning

## Update CORS After Domain Setup

In `backend/main.py`, update CORS origins:

```python
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com",
    "https://nano-banana-ta-frontend.onrender.com"
]
```

Redeploy backend after updating.

