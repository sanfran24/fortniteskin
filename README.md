# 🍌 Nano Banana TA Tool

AI-powered technical analysis tool for trading charts using Google's Gemini Vision model (Nano Banana Pro when available).

## Features

- 📊 **Chart Analysis**: Upload trading chart screenshots for AI-powered technical analysis
- 🎯 **Trade Setup**: Get entry, stop-loss, and take-profit recommendations
- 📈 **Pattern Recognition**: Automatically detect chart patterns and trends
- 🎨 **Visual Annotations**: View annotated charts with key levels marked
- ⚡ **Fast & Accurate**: Powered by Google's latest Gemini vision models

## Tech Stack

- **Frontend**: React + TypeScript + Vite
- **Backend**: FastAPI (Python)
- **AI Model**: Google Gemini Vision API
- **Styling**: Modern CSS with dark theme

## Prerequisites

- Python 3.9+
- Node.js 18+
- Google API Key ([Get one here](https://makersuite.google.com/app/apikey))

## Setup

### 1. Clone and Install Dependencies

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` in the backend directory:

```bash
cp .env.example backend/.env
```

Edit `backend/.env` and add your Google API key:

```
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL=nano-banana-pro-preview
```

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python main.py
# Or: uvicorn main:app --reload
```

The backend will run on `http://localhost:8000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The frontend will run on `http://localhost:5173`

### 4. Use the Tool

1. Open `http://localhost:5173` in your browser
2. Upload a trading chart screenshot (PNG, JPG)
3. Wait for AI analysis (usually 5-15 seconds)
4. Review the analysis results:
   - Trade setup (entry, SL, TP)
   - Support/resistance levels
   - Detected patterns
   - Trend analysis
   - Risk assessment

## Project Structure

```
chart-ta-tool/
├── backend/
│   ├── main.py              # FastAPI server
│   ├── utils/
│   │   └── prompts.py       # TA prompt templates
│   ├── requirements.txt
│   └── .env                 # API keys (not in git)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── UploadChart.tsx
│   │   │   └── AnnotatedChart.tsx
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## API Endpoints

### `POST /analyze`

Upload a chart image for analysis.

**Request:**
- `file`: Image file (multipart/form-data)

**Response:**
```json
{
  "success": true,
  "analysis": {
    "bias": "bullish",
    "confidence": 8,
    "entry": { "price": "45.20", "reasoning": "..." },
    "stop_loss": { "price": "44.50", "risk_percent": "1.5%" },
    "take_profits": [...],
    "support_levels": [...],
    "resistance_levels": [...],
    "patterns": [...],
    "trend": {...},
    "reasoning": "..."
  },
  "original_image": "data:image/png;base64,...",
  "annotated_image": null
}
```

## Customization

### Modify the TA Prompt

Edit `backend/utils/prompts.py` to customize the analysis style, add indicators, or change the output format.

### Change Model

Update `GEMINI_MODEL` in `.env`:
- `nano-banana-pro-preview` - Optimized for vision tasks like chart analysis (default)
- `gemini-2.5-pro` - Best quality alternative
- `gemini-2.0-flash` - Faster, lower cost

### Frontend Styling

Modify CSS files in `frontend/src/` to customize the UI theme and layout.

## Deployment

### Backend (FastAPI)

**Render:**
```bash
# Add render.yaml or use Render dashboard
```

**Fly.io:**
```bash
fly launch
```

**Heroku:**
```bash
# Add Procfile: web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vite)

**Vercel:**
```bash
npm install -g vercel
vercel
```

**Netlify:**
```bash
npm run build
# Deploy dist/ folder
```

## Tips for Best Results

1. **Chart Quality**: Use clear, high-resolution screenshots
2. **Timeframe**: Works with any timeframe (1m to weekly)
3. **Multiple Charts**: Upload different timeframes for comprehensive analysis
4. **API Costs**: Gemini 1.5 Pro costs ~$0.001-0.01 per analysis. Consider caching common analyses.

## Troubleshooting

**"GOOGLE_API_KEY not found"**
- Ensure `.env` file exists in `backend/` directory
- Check that the API key is correctly set

**CORS errors**
- Update `allow_origins` in `backend/main.py` to include your frontend URL

**Image upload fails**
- Check file size (max ~10MB recommended)
- Ensure image format is PNG/JPG/JPEG

## Future Enhancements

- [ ] Image annotation overlay (when Gemini supports image editing)
- [ ] Multi-chart comparison
- [ ] Analysis history/saved charts
- [ ] Custom prompt templates per user
- [ ] Real-time chart analysis from trading platforms
- [ ] Export analysis as PDF/PNG

## License

MIT

## Credits

Built with Cursor & Claude Opus, powered by Google Gemini Vision.

