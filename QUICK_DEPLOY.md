# 🚀 Quick Deploy Guide: Render + Namecheap

## What You Need
- ✅ Domain from Namecheap
- ✅ Render account (free tier works!)
- ✅ GitHub repo with your code
- ✅ Google Gemini API key

## Step-by-Step

### 1️⃣ Push Code to GitHub
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

### 2️⃣ Deploy Backend on Render

1. Go to https://dashboard.render.com
2. **New +** → **Web Service**
3. Connect GitHub → Select your repo
4. Settings:
   - **Name**: `nano-banana-ta-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m uvicorn main:app --host 0.0.0.0 --port $PORT`

5. **Environment Variables**:
   ```
   GOOGLE_API_KEY = your_api_key_here
   GEMINI_MODEL = nano-banana-pro-preview
   ALLOWED_ORIGINS = https://yourdomain.com,https://www.yourdomain.com
   ```

6. **Add Disk** (for cache):
   - Name: `cache-disk`
   - Mount: `/opt/render/project/src/cache`
   - Size: 1GB

7. Click **Create Web Service**

**Save your backend URL**: `https://nano-banana-ta-backend.onrender.com`

### 3️⃣ Deploy Frontend on Render

1. **New +** → **Static Site**
2. Connect same GitHub repo
3. Settings:
   - **Name**: `nano-banana-ta-frontend`
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Publish Directory**: `frontend/dist`

4. **Environment Variables**:
   ```
   VITE_API_URL = https://nano-banana-ta-backend.onrender.com
   ```

5. Click **Create Static Site**

**Save your frontend URL**: `https://nano-banana-ta-frontend.onrender.com`

### 4️⃣ Connect Domain (Namecheap)

#### In Render:
1. Frontend service → **Settings** → **Custom Domain**
2. Add: `yourdomain.com` and `www.yourdomain.com`
3. Copy the DNS records shown

#### In Namecheap:
1. Login → **Domain List** → Click **Manage**
2. **Advanced DNS** tab
3. Add these records:

   **Record 1:**
   - Type: `CNAME Record`
   - Host: `@`
   - Value: `nano-banana-ta-frontend.onrender.com`
   - TTL: Automatic

   **Record 2:**
   - Type: `CNAME Record`
   - Host: `www`
   - Value: `nano-banana-ta-frontend.onrender.com`
   - TTL: Automatic

4. **Save All Changes**

5. Wait 15-30 minutes for DNS + SSL

### 5️⃣ Update CORS (After Domain Works)

1. Backend service → **Environment**
2. Update `ALLOWED_ORIGINS`:
   ```
   https://yourdomain.com,https://www.yourdomain.com,https://nano-banana-ta-frontend.onrender.com
   ```
3. Redeploy backend

### 6️⃣ Test!

Visit `https://yourdomain.com` and upload a chart! 🎉

## Troubleshooting

**Backend not working?**
- Check logs in Render dashboard
- Verify `GOOGLE_API_KEY` is set
- Test: `https://nano-banana-ta-backend.onrender.com/health`

**Frontend can't connect?**
- Check browser console (F12)
- Verify `VITE_API_URL` matches backend URL
- Check CORS settings

**Domain not working?**
- Wait 30+ minutes
- Check DNS: https://www.whatsmydns.net
- Verify records match Render exactly

## Cost
- **Free tier**: $0/month (750 hours backend, unlimited static sites)
- **Paid**: Only if you exceed free limits

## Need Help?
- Full guide: See `DEPLOYMENT.md`
- Render docs: https://render.com/docs
- Namecheap DNS: https://www.namecheap.com/support/knowledgebase/article.aspx/319/2237/

