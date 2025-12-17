# Quick Start Guide

Get your Nano Banana TA Tool running in 5 minutes!

## Step 1: Get Your API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key (you'll need it in Step 3)

## Step 2: Install Dependencies

### Option A: Automated Setup (Recommended)

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option B: Manual Setup

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm install
```

## Step 3: Configure API Key

1. Create `backend/.env` file:
   ```bash
   cd backend
   cp .env.example .env  # Or create manually
   ```

2. Edit `backend/.env` and add your API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-1.5-pro
   ```

## Step 4: Run the Application

**Terminal 1 - Start Backend:**
```bash
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Start Frontend:**
```bash
cd frontend
npm run dev
```

You should see:
```
  VITE v5.x.x  ready in xxx ms
  ➜  Local:   http://localhost:5173/
```

## Step 5: Test It Out!

1. Open `http://localhost:5173` in your browser
2. Upload a trading chart screenshot
3. Wait 5-15 seconds for analysis
4. Review the results!

## Troubleshooting

**"GOOGLE_API_KEY not found"**
- Make sure `.env` file is in `backend/` directory (not root)
- Check that the file is named exactly `.env` (not `.env.txt`)
- Verify the API key is on a single line with no quotes

**Backend won't start**
- Make sure you activated the virtual environment
- Check Python version: `python --version` (need 3.9+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**Frontend won't start**
- Check Node.js version: `node --version` (need 18+)
- Delete `node_modules` and reinstall: `rm -rf node_modules && npm install`

**CORS errors**
- Make sure backend is running on port 8000
- Check browser console for specific error messages

## Next Steps

- Customize the TA prompt in `backend/utils/prompts.py`
- Modify UI styling in `frontend/src/`
- Deploy to production (see README.md)

Happy trading! 📈

