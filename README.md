# 🎮 Fortnite Skin Generator

Transform any image into a Fortnite-style character skin using Google's Nano Banana AI (Gemini Image Generation).

![Fortnite Skin Generator](https://img.shields.io/badge/Powered%20by-Nano%20Banana%20AI-blueviolet)
![Python](https://img.shields.io/badge/Backend-FastAPI-green)
![React](https://img.shields.io/badge/Frontend-React%20+%20TypeScript-blue)

## ✨ Features

- **🖼️ Any Image Input**: Upload selfies, characters, memes, pets - anything works!
- **🎨 Multiple Styles**: Choose from 12+ skin rarities and styles:
  - ⭐ Legendary - Ultra-premium with glowing effects
  - 💜 Epic - High-quality distinctive design
  - 💙 Rare - Cool and stylish
  - 💚 Uncommon - Clean and simple
  - 😂 Meme Lord - Hilarious viral-worthy skins
  - 🌸 Anime - Manga/anime styled characters
  - 🤖 Cyberpunk - Neon futuristic warriors
  - 🍌 Peely Style - Banana-inspired fun
  - And more!
- **🤖 AI Powered**: Uses Google's Nano Banana (Gemini 2.0 Flash) for intelligent image transformation
- **📜 Detailed Descriptions**: Get full skin concepts with back bling, pickaxe, and emote ideas
- **🛒 Item Shop Preview**: See your skin as it would appear in the Fortnite Item Shop

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Google API Key with Gemini access

### Backend Setup

```bash
cd "fortnite skin"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GOOGLE_API_KEY=your-api-key-here" > .env

# Run the server
python main.py
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

### Access the App

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Required
GOOGLE_API_KEY=your-google-api-key

# Optional
IMAGE_MODEL=gemini-2.0-flash-exp
VISION_MODEL=gemini-2.0-flash-exp
ALLOWED_ORIGINS=*
CACHE_DIR=cache
```

### API Models

The app uses Google's Nano Banana models:

- **gemini-2.0-flash-exp**: For image generation and vision tasks
- Fallback to description-only mode if image generation is unavailable

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info and status |
| `/health` | GET | Health check |
| `/styles` | GET | Get available skin styles |
| `/generate` | POST | Generate Fortnite skin from image |

### Generate Skin Request

```bash
curl -X POST "http://localhost:8000/generate" \
  -F "file=@your-image.jpg" \
  -F "style=legendary" \
  -F "custom_prompt=Add fire effects"
```

### Response

```json
{
  "success": true,
  "style": "legendary",
  "original_image": "data:image/png;base64,...",
  "generated_images": ["data:image/png;base64,..."],
  "description": "Introducing **FLAME WARRIOR**...",
  "skin_details": {
    "name": "Flame Warrior",
    "rarity": "Legendary",
    "set": "Inferno Series"
  }
}
```

## 🏗️ Project Structure

```
fortnite skin/
├── main.py              # FastAPI backend
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── utils/
│   └── prompts.py       # AI prompts for skin generation
├── frontend/
│   ├── src/
│   │   ├── App.tsx      # Main React app
│   │   ├── App.css      # Global styles
│   │   └── components/
│   │       ├── UploadImage.tsx   # Image upload component
│   │       ├── SkinResult.tsx    # Result display component
│   │       └── *.css             # Component styles
│   ├── package.json
│   └── vite.config.ts
└── cache/               # Cached generations
```

## 🎨 Customization

### Adding New Styles

Edit `utils/prompts.py` to add new skin styles:

```python
style_prompts = {
    "your_style": """**YOUR STYLE SKIN**
    
    Create a [your description]...
    """,
}
```

Then add it to `get_skin_styles()` function.

### Styling the Frontend

The app uses CSS variables for theming. Edit `App.css`:

```css
:root {
  --fortnite-blue: #00d4ff;
  --fortnite-purple: #9d4edd;
  --legendary: #f5a623;
  /* ... */
}
```

## 🚢 Deployment

### Deploy to Render

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set environment variables:
   - `GOOGLE_API_KEY`: Your API key
4. Deploy!

### Docker

```bash
docker build -t fortnite-skin-generator .
docker run -p 8000:8000 -e GOOGLE_API_KEY=your-key fortnite-skin-generator
```

## ⚠️ Disclaimer

This project is NOT affiliated with, endorsed by, or connected to Epic Games or Fortnite. This is a fan-made AI art project for entertainment purposes only. All Fortnite-related trademarks and copyrights are property of Epic Games.

## 📄 License

MIT License - feel free to use and modify!

## 🙏 Credits

- **AI**: Google Gemini / Nano Banana
- **Framework**: FastAPI + React + TypeScript
- **Styling**: Custom CSS with Fortnite-inspired design

---

Made with ⚡ by AI enthusiasts
