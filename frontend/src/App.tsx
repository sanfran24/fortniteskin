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

  useEffect(() => {
    const fetchStyles = async () => {
      try {
        const API_URL = import.meta.env.VITE_API_URL || (
          import.meta.env.PROD 
            ? 'https://fortniteskin-backend.onrender.com' 
            : 'http://localhost:8000'
        )
        const response = await fetch(`${API_URL}/styles`)
        if (response.ok) {
          const data = await response.json()
          setStyles(data.styles)
        }
      } catch {
        setStyles([
          { id: 'legendary', name: 'Legendary', description: 'Ultra-premium skin', color: '#ff9800', icon: '⭐' },
          { id: 'epic', name: 'Epic', description: 'High-quality skin', color: '#e040fb', icon: '💜' },
          { id: 'rare', name: 'Rare', description: 'Cool distinctive skin', color: '#29b6f6', icon: '💙' },
          { id: 'uncommon', name: 'Uncommon', description: 'Clean simple skin', color: '#66bb6a', icon: '💚' },
          { id: 'meme', name: 'Meme Lord', description: 'Hilarious viral skin', color: '#ff9800', icon: '😂' },
          { id: 'anime', name: 'Anime', description: 'Anime-styled character', color: '#f48fb1', icon: '🌸' },
          { id: 'cyberpunk', name: 'Cyberpunk', description: 'Neon cyber warrior', color: '#00e5ff', icon: '🤖' },
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
        </div>
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
            </div>
            <div className="loading-text">
              <span className="loading-main">GENERATING SKIN...</span>
              <span className="loading-sub">AI is crafting your custom outfit</span>
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
              🔄 TRY AGAIN
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
        <p>Powered by Nano Banana AI • Not affiliated with Epic Games</p>
      </footer>
    </div>
  )
}

export default App
