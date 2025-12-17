# Fix Python Version in Render Dashboard

Render is ignoring `runtime.txt`. You need to set Python version manually in the dashboard.

## Steps to Fix:

1. **Go to Render Dashboard** → Your backend service
2. **Click "Settings"** tab
3. **Scroll to "Python Version"** section
4. **Set Python Version**: `3.11.9` (or `3.11`)
5. **Click "Save Changes"**
6. **Manual Deploy**: Click "Manual Deploy" → "Deploy latest commit"

## Alternative: Set via Environment Variable

1. Go to **Environment** tab
2. Add/Update: `PYTHON_VERSION` = `3.11.9`
3. Save and redeploy

This will force Render to use Python 3.11.9 instead of 3.13.4.

