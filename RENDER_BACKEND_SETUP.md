# Render Backend Setup - Step by Step

## Manual Setup (Recommended)

### Step 1: Create Web Service
1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Click **"Connect account"** → Connect your GitHub account
4. Select repository: **`sanfran24/billybob`**

### Step 2: Configure Service Settings

**Basic Settings:**
- **Name**: `nano-banana-ta-backend`
- **Region**: Choose closest to you (e.g., `Oregon (US West)`)
- **Branch**: `main`
- **Root Directory**: `backend` ⚠️ **IMPORTANT**

**Build & Deploy:**
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

**Advanced Settings (Optional):**
- **Auto-Deploy**: `Yes` (deploys on every push to main)

### Step 3: Add Environment Variables

Click **"Environment"** tab, then add these variables:

1. **GOOGLE_API_KEY**
   - Key: `GOOGLE_API_KEY`
   - Value: `your_google_api_key_here` (paste your actual key)
   - Click **"Save Changes"**

2. **GEMINI_MODEL** (Optional)
   - Key: `GEMINI_MODEL`
   - Value: `nano-banana-pro-preview`
   - Click **"Save Changes"**

3. **ALLOWED_ORIGINS** (Set after domain is live)
   - Key: `ALLOWED_ORIGINS`
   - Value: `https://yourdomain.com,https://www.yourdomain.com`
   - Click **"Save Changes"**

### Step 4: Deploy

1. Click **"Create Web Service"** at the bottom
2. Render will start building
3. Watch the logs - first build takes 2-3 minutes
4. Once deployed, you'll see: **"Your service is live at https://nano-banana-ta-backend.onrender.com"**

### Step 5: Verify Deployment

1. Visit: `https://nano-banana-ta-backend.onrender.com/health`
2. Should see: `{"status":"healthy","model":"nano-banana-pro-preview","api_configured":true}`

---

## Troubleshooting

### Build Command Not Showing
- Make sure **Root Directory** is set to `backend`
- Make sure **Environment** is set to `Python 3`
- The build/start commands should appear automatically

### Build Fails
- Check logs in Render dashboard
- Verify `requirements.txt` exists in `backend/` folder
- Make sure Python version is compatible (3.9+)

### Start Command Not Working
- Verify: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
- Make sure `main.py` exists in `backend/` folder
- Check logs for specific errors

### API Key Not Working
- Verify `GOOGLE_API_KEY` is set in Environment tab
- Check logs for API errors
- Test API key locally first: `python backend/test_api.py`

---

## Quick Reference

**Service Name**: `nano-banana-ta-backend`  
**Root Directory**: `backend`  
**Build Command**: `pip install -r requirements.txt`  
**Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`  
**Environment**: `Python 3`

**Required Env Vars:**
- `GOOGLE_API_KEY` (required)
- `GEMINI_MODEL` (optional, defaults to nano-banana-pro-preview)
- `ALLOWED_ORIGINS` (set after domain is live)

