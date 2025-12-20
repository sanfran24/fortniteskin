import { useState, useEffect } from 'react'
import UploadImage from './components/UploadImage'
import SkinResult from './components/SkinResult'
import './App.css'

export interface SkinStyle {
  id: string
  name: string
  description: string
  color: string
  icon: string
}

export interface GenerationResult {
  success: boolean
  style: string
  original_image: string
  generated_images: string[]
  description: string
  skin_details: {
    name?: string
    rarity?: string
    set?: string
    features?: string[]
    colors?: string[]
    back_bling?: string
    pickaxe?: string
    emote?: string
  }
}

function App() {
  const [result, setResult] = useState<GenerationResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [styles, setStyles] = useState<SkinStyle[]>([])

  // Fetch available styles on mount
  useEffect(() => {
    const fetchStyles = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || (
          import.meta.env.PROD 
            ? 'https://fortnite-skin-generator.onrender.com' 
            : 'http://localhost:8000'
        )
        const response = await fetch(`${API_URL}/styles`)
        if (response.ok) {
          const data = await response.json()
          setStyles(data.styles)
        }
      } catch (err) {
        console.log('Could not fetch styles, using defaults')
        // Default styles if API is not available
        setStyles([
          { id: 'legendary', name: 'Legendary', description: 'Ultra-premium skin', color: '#f5a623', icon: '⭐' },
          { id: 'epic', name: 'Epic', description: 'High-quality skin', color: '#9b59b6', icon: '💜' },
          { id: 'rare', name: 'Rare', description: 'Cool distinctive skin', color: '#3498db', icon: '💙' },
          { id: 'uncommon', name: 'Uncommon', description: 'Clean simple skin', color: '#2ecc71', icon: '💚' },
          { id: 'meme', name: 'Meme Lord', description: 'Hilarious viral skin', color: '#f39c12', icon: '😂' },
          { id: 'anime', name: 'Anime', description: 'Anime-styled character', color: '#ff6b9d', icon: '🌸' },
          { id: 'cyberpunk', name: 'Cyberpunk', description: 'Neon cyber warrior', color: '#00ffff', icon: '🤖' },
          { id: 'peely', name: 'Peely Style', description: 'Banana-inspired fun', color: '#ffeb3b', icon: '🍌' },
        ])
      }
    }
    fetchStyles()
  }, [])

  const handleGenerationComplete = (generationResult: GenerationResult) => {
    setResult(generationResult)
    setLoading(false)
    setError(null)
  }

  const handleGenerationStart = () => {
    setLoading(true)
    setError(null)
    setResult(null)
  }

  const handleError = (errorMessage: string) => {
    setError(errorMessage)
    setLoading(false)
  }

  const handleReset = () => {
    setResult(null)
    setError(null)
    setLoading(false)
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <div className="logo-section">
            <span className="logo-icon">🎮</span>
            <h1>FORTNITE SKIN GENERATOR</h1>
          </div>
          <p className="tagline">Transform any image into a Fortnite character skin using AI</p>
        </div>
        <div className="header-glow"></div>
      </header>

      <main className="app-main">
        {!result && !loading && (
          <UploadImage
            styles={styles}
            onGenerationStart={handleGenerationStart}
            onGenerationComplete={handleGenerationComplete}
            onError={handleError}
          />
        )}

        {loading && (
          <div className="loading-container">
            <div className="loading-battle-bus">
              <div className="bus-icon">🚌</div>
              <div className="loading-trail"></div>
            </div>
            <div className="loading-text">
              <span className="loading-main">GENERATING YOUR SKIN...</span>
              <span className="loading-sub">Nano Banana AI is working its magic</span>
            </div>
            <div className="loading-bar">
              <div className="loading-progress"></div>
            </div>
          </div>
        )}

        {error && (
          <div className="error-container">
            <div className="error-icon">💀</div>
            <h2>ELIMINATED!</h2>
            <p>{error}</p>
            <button onClick={handleReset} className="btn-primary">
              🔄 DROP AGAIN
            </button>
          </div>
        )}

        {result && (
          <SkinResult
            result={result}
            onReset={handleReset}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>⚡ POWERED BY GOOGLE NANO BANANA AI • NOT AFFILIATED WITH EPIC GAMES ⚡</p>
      </footer>
    </div>
  )
}

export default App
