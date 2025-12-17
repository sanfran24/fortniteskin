# Building Frontend for Namecheap Stellar Hosting

## Step 1: Build the Frontend

Run this command in your project root:

```bash
cd frontend
npm install
npm run build
```

This creates a `frontend/dist` folder with all the production files.

## Step 2: Configure Backend URL

Before building, set the backend URL:

**Option A: Set environment variable (recommended)**
```bash
# Windows PowerShell
$env:VITE_API_URL="https://nano-banana-ta-backend.onrender.com"
cd frontend
npm run build

# Or create a .env.production file in frontend/
```

**Option B: Edit the code directly**

Edit `frontend/src/components/UploadChart.tsx` line 12:
```typescript
const API_URL = 'https://nano-banana-ta-backend.onrender.com';
```

Then build:
```bash
cd frontend
npm run build
```

## Step 3: Zip the Build Files

After building, zip the contents of `frontend/dist` folder:

**Windows:**
```powershell
Compress-Archive -Path frontend\dist\* -DestinationPath frontend-build.zip
```

**Mac/Linux:**
```bash
cd frontend/dist
zip -r ../../frontend-build.zip .
```

## Step 4: Upload to Namecheap

1. Log into Namecheap cPanel
2. Go to **File Manager**
3. Navigate to `public_html` (or your domain's root folder)
4. Delete any existing files (or backup first)
5. Upload `frontend-build.zip`
6. Extract the zip file in `public_html`
7. Make sure `index.html` is in the root of `public_html`

## Step 5: Update Backend CORS

After your domain is live, update Render backend environment variable:

1. Go to Render dashboard → Backend service → Environment
2. Add/Update: `ALLOWED_ORIGINS`
3. Value: `https://yourdomain.com,https://www.yourdomain.com`
4. Redeploy backend

## File Structure After Upload

Your `public_html` should look like:
```
public_html/
  ├── index.html
  ├── assets/
  │   ├── index-[hash].js
  │   ├── index-[hash].css
  │   └── ...
  └── [other static files]
```

## Troubleshooting

**Frontend can't connect to backend?**
- Check browser console (F12) for errors
- Verify backend URL is correct in the built files
- Check CORS settings on backend

**404 errors?**
- Make sure `index.html` is in the root of `public_html`
- Check if Namecheap needs a `.htaccess` file (see below)

**Assets not loading?**
- Verify all files from `dist` folder were uploaded
- Check file permissions (should be 644 for files, 755 for folders)

