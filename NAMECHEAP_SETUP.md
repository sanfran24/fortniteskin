# Namecheap Stellar Hosting Setup Guide

This guide will help you deploy the frontend to Namecheap Stellar hosting and connect it to your Render backend.

## Prerequisites

- ✅ Namecheap domain with Stellar hosting
- ✅ Backend deployed on Render
- ✅ Backend URL: `https://nano-banana-ta-backend.onrender.com` (or your custom URL)

## Step 1: Build the Frontend

### Option A: Using the Build Script (Easiest)

**Windows:**
```powershell
.\build-and-zip.ps1
```

**Mac/Linux:**
```bash
chmod +x build-and-zip.sh
./build-and-zip.sh
```

### Option B: Manual Build

1. **Set backend URL** (if not using default):
   ```powershell
   # Windows PowerShell
   $env:VITE_API_URL="https://nano-banana-ta-backend.onrender.com"
   ```

2. **Build:**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

3. **Zip the dist folder:**
   ```powershell
   # Windows
   Compress-Archive -Path frontend\dist\* -DestinationPath frontend-build.zip
   
   # Mac/Linux
   cd frontend/dist
   zip -r ../../frontend-build.zip .
   ```

## Step 2: Upload to Namecheap

1. **Log into Namecheap cPanel**
   - Go to https://www.namecheap.com
   - Login → **Manage** → **cPanel**

2. **Open File Manager**
   - Find **File Manager** in cPanel
   - Navigate to `public_html` folder

3. **Backup existing files** (if any)
   - Select all files → **Compress** → Download backup

4. **Upload frontend-build.zip**
   - Click **Upload** in File Manager
   - Select `frontend-build.zip`
   - Wait for upload to complete

5. **Extract the zip**
   - Right-click `frontend-build.zip` → **Extract**
   - Extract to `public_html`
   - **Important**: Make sure files are extracted directly into `public_html`, not into a subfolder

6. **Verify file structure**
   Your `public_html` should contain:
   ```
   public_html/
     ├── index.html
     ├── assets/
     │   ├── index-[hash].js
     │   ├── index-[hash].css
     │   └── ...
     └── [other static files]
   ```

7. **Upload .htaccess** (optional but recommended)
   - Copy `frontend/.htaccess` to `public_html/.htaccess`
   - This enables proper routing and caching

## Step 3: Configure Backend CORS

After your domain is live, update Render backend:

1. **Get your domain URL**
   - Your site should be at: `https://yourdomain.com` or `https://www.yourdomain.com`

2. **Update Render backend environment**
   - Go to Render dashboard → Your backend service → **Environment**
   - Add/Update: `ALLOWED_ORIGINS`
   - Value: `https://yourdomain.com,https://www.yourdomain.com`
   - Click **Save Changes**
   - Backend will auto-redeploy

3. **Verify CORS**
   - Visit your site: `https://yourdomain.com`
   - Open browser console (F12)
   - Upload a test chart
   - Check for CORS errors (should be none)

## Step 4: Test Your Deployment

1. **Visit your site**: `https://yourdomain.com`
2. **Test upload**: Upload a chart image
3. **Check console**: Open browser DevTools (F12) → Console tab
4. **Verify API calls**: Network tab should show requests to Render backend

## Troubleshooting

### Frontend shows blank page
- ✅ Check that `index.html` is in `public_html` root (not in a subfolder)
- ✅ Verify all files from `dist` were uploaded
- ✅ Check browser console for errors
- ✅ Verify `.htaccess` is uploaded (if using)

### Can't connect to backend
- ✅ Check browser console for CORS errors
- ✅ Verify `VITE_API_URL` was set during build (check built files)
- ✅ Check backend is running: `https://nano-banana-ta-backend.onrender.com/health`
- ✅ Verify CORS settings on backend include your domain

### 404 errors on page refresh
- ✅ Upload `.htaccess` file to `public_html`
- ✅ Verify rewrite rules are enabled in cPanel

### Assets not loading
- ✅ Check file permissions (should be 644 for files, 755 for folders)
- ✅ Verify all files from `dist` folder were uploaded
- ✅ Check browser console for 404 errors on specific files

### Build script fails
- ✅ Make sure you're in project root directory
- ✅ Verify Node.js and npm are installed: `node --version` and `npm --version`
- ✅ Try manual build steps instead

## File Structure Checklist

After upload, verify:
- [ ] `public_html/index.html` exists
- [ ] `public_html/assets/` folder exists with JS/CSS files
- [ ] `public_html/.htaccess` exists (optional)
- [ ] No nested folders (files should be directly in `public_html`)

## Updating Your Site

When you make changes:

1. **Rebuild frontend**:
   ```powershell
   .\build-and-zip.ps1
   ```

2. **Upload new zip** to Namecheap
3. **Extract** (overwrite existing files)
4. **Clear browser cache** or do hard refresh (Ctrl+F5)

## Security Notes

- ✅ Backend API key is NOT exposed (stays on Render)
- ✅ Frontend only contains public code
- ✅ CORS protects backend from unauthorized domains
- ✅ `.htaccess` adds security headers

## Need Help?

- Namecheap Support: https://www.namecheap.com/support/
- Render Docs: https://render.com/docs
- Check browser console (F12) for specific errors

