# Deployment Guide: Render + Namecheap

This guide will help you deploy your Nano Banana TA Tool to Render and connect it to your Namecheap domain.

## Prerequisites

- ✅ Domain purchased on Namecheap
- ✅ Render account (sign up at https://render.com)
- ✅ GitHub account (for connecting your repo)
- ✅ Google API key for Gemini

## Step 1: Prepare Your Code

### 1.1 Update CORS Settings (Production)

The backend currently allows all origins (`*`). For production, you should update this to your domain.

**File: `backend/main.py`** (around line 71-77)

```python
# Update CORS to allow your domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
        "https://nano-banana-ta-frontend.onrender.com"  # Render frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 1.2 Update Frontend API URL

**File: `frontend/src/components/UploadChart.tsx`**

Find the API call (around line 50-60) and update:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'https://nano-banana-ta-backend.onrender.com';
```

## Step 2: Deploy Backend to Render

### 2.1 Create Backend Service

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:
   - **Name**: `nano-banana-ta-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory**: Leave empty (or `backend` if you want to set it)

### 2.2 Set Environment Variables

In Render dashboard, go to your backend service → **Environment** tab:

- `GOOGLE_API_KEY` = Your Google Gemini API key
- `GEMINI_MODEL` = `nano-banana-pro-preview` (or your preferred model)
- `PYTHON_VERSION` = `3.11.0`

### 2.3 Add Persistent Disk (for cache)

1. Go to your backend service → **Disks** tab
2. Click **"Add Disk"**
3. Configure:
   - **Name**: `cache-disk`
   - **Mount Path**: `/opt/render/project/src/backend/cache`
   - **Size**: 1 GB

### 2.4 Deploy

Click **"Save Changes"** and Render will start deploying. Wait for deployment to complete.

**Note your backend URL**: `https://nano-banana-ta-backend.onrender.com`

## Step 3: Deploy Frontend to Render

### 3.1 Create Frontend Service

1. Click **"New +"** → **"Static Site"** (or **"Web Service"** if using preview)
2. Connect your GitHub repository
3. Configure:
   - **Name**: `nano-banana-ta-frontend`
   - **Environment**: `Node`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`
   - **Root Directory**: Leave empty

### 3.2 Set Environment Variables

- `VITE_API_URL` = `https://nano-banana-ta-backend.onrender.com` (your backend URL from Step 2)

### 3.3 Deploy

Click **"Save Changes"** and wait for deployment.

**Note your frontend URL**: `https://nano-banana-ta-frontend.onrender.com`

## Step 4: Connect Domain to Render (Namecheap)

### 4.1 Get Render DNS Records

1. Go to your **frontend service** on Render
2. Click **"Settings"** → Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter your domain: `yourdomain.com` and `www.yourdomain.com`
5. Render will show you DNS records you need to add

You'll see something like:
- **Type**: `CNAME`
- **Name**: `@` (or blank)
- **Value**: `nano-banana-ta-frontend.onrender.com`
- **Type**: `CNAME`
- **Name**: `www`
- **Value**: `nano-banana-ta-frontend.onrender.com`

### 4.2 Configure DNS on Namecheap

1. Log into Namecheap
2. Go to **Domain List** → Click **"Manage"** next to your domain
3. Go to **"Advanced DNS"** tab
4. Add DNS records:

   **For root domain (@):**
   - **Type**: `CNAME Record`
   - **Host**: `@`
   - **Value**: `nano-banana-ta-frontend.onrender.com`
   - **TTL**: Automatic (or 3600)

   **For www subdomain:**
   - **Type**: `CNAME Record`
   - **Host**: `www`
   - **Value**: `nano-banana-ta-frontend.onrender.com`
   - **TTL**: Automatic (or 3600)

   **Alternative (if CNAME doesn't work for root):**
   - **Type**: `A Record`
   - **Host**: `@`
   - **Value**: Render's IP address (check Render docs for current IP)
   - **TTL**: Automatic

5. **Remove** any existing A records for `@` if you're using CNAME
6. Click **"Save All Changes"**

### 4.3 Wait for DNS Propagation

- DNS changes can take 5 minutes to 48 hours (usually 15-30 minutes)
- Check propagation: https://www.whatsmydns.net
- Once propagated, Render will automatically provision SSL certificate

## Step 5: Update CORS with Your Domain

Once your domain is connected:

1. Go to backend service → **Environment** tab
2. Update CORS origins to include your domain:
   ```
   https://yourdomain.com,https://www.yourdomain.com,https://nano-banana-ta-frontend.onrender.com
   ```
3. Or update `backend/main.py` directly and redeploy

## Step 6: Test Your Deployment

1. Visit `https://yourdomain.com` (or `https://www.yourdomain.com`)
2. Upload a test chart
3. Verify analysis works
4. Check browser console for any errors

## Troubleshooting

### Backend not responding
- Check Render logs: Service → **Logs** tab
- Verify `GOOGLE_API_KEY` is set correctly
- Check health endpoint: `https://nano-banana-ta-backend.onrender.com/health`

### Frontend can't connect to backend
- Verify `VITE_API_URL` environment variable is set
- Check browser console for CORS errors
- Ensure backend CORS includes your frontend URL

### DNS not working
- Wait 30+ minutes for propagation
- Verify DNS records match Render's requirements exactly
- Check Namecheap DNS settings (some domains need nameservers changed)

### SSL Certificate issues
- Render auto-provisions SSL, but it can take 1-2 hours after DNS propagates
- Check Render dashboard → Custom Domain section for SSL status

## Cost Estimate (Render Free Tier)

- **Backend**: Free tier includes 750 hours/month (enough for 24/7)
- **Frontend**: Static sites are free
- **Disk**: 1GB free disk included
- **Total**: **$0/month** (as long as you stay within free tier limits)

## Production Checklist

- [ ] Backend deployed and healthy
- [ ] Frontend deployed and accessible
- [ ] Domain connected and SSL active
- [ ] Environment variables set correctly
- [ ] CORS configured for your domain
- [ ] Cache disk mounted
- [ ] Test upload and analysis works
- [ ] Monitor Render logs for errors

## Need Help?

- Render Docs: https://render.com/docs
- Namecheap DNS Guide: https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/
- Render Support: support@render.com

