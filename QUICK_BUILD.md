# Quick Build Guide for Namecheap

## One-Command Build & Zip

**Windows:**
```powershell
.\build-and-zip.ps1
```

**Mac/Linux:**
```bash
chmod +x build-and-zip.sh && ./build-and-zip.sh
```

This will:
1. ✅ Build the frontend with production settings
2. ✅ Create `frontend-build.zip` ready for upload
3. ✅ Show you next steps

## Upload to Namecheap

1. **cPanel → File Manager → public_html**
2. **Upload** `frontend-build.zip`
3. **Extract** it (files should go directly into `public_html`)
4. **Verify** `index.html` is in `public_html` root

## Update Backend CORS

After your domain is live:

1. **Render Dashboard → Backend → Environment**
2. **Add**: `ALLOWED_ORIGINS` = `https://yourdomain.com,https://www.yourdomain.com`
3. **Save** (auto-redeploys)

## Test

Visit `https://yourdomain.com` and upload a chart!

---

**Full guide**: See `NAMECHEAP_SETUP.md` for detailed instructions.

