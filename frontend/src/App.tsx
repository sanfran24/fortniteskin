import { useState } from 'react'
import UploadChart from './components/UploadChart'
import AnnotatedChart from './components/AnnotatedChart'
import './App.css'

export interface AnalysisResult {
  success: boolean
  analysis: {
    bias?: string
    confidence?: number
    timeframe?: string
    asset?: string
    current_price?: string
    support_levels?: Array<{ price: string; strength: string; reason: string }>
    resistance_levels?: Array<{ price: string; strength: string; reason: string }>
    patterns?: Array<{ name: string; type: string; reliability: string }>
    trend?: {
      direction: string
      strength: string
      since: string
    }
    entry?: {
      price: string
      reasoning: string
    }
    stop_loss?: {
      price: string
      risk_percent: string
      reasoning: string
    }
    take_profits?: Array<{
      price: string
      risk_reward: string
      reasoning: string
    }>
    risk_reward_ratio?: string
    position_sizing?: string
    risks?: string[]
    reasoning?: string
    raw_text?: string
    parsed?: boolean
  }
  raw_response?: string
  original_image?: string
  annotated_image?: string | null
}

function App() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleAnalysisComplete = (result: AnalysisResult) => {
    setAnalysisResult(result)
    setLoading(false)
    setError(null)
  }

  const handleAnalysisStart = () => {
    setLoading(true)
    setError(null)
    setAnalysisResult(null)
  }

  const handleError = (errorMessage: string) => {
    setError(errorMessage)
    setLoading(false)
  }

  const handleReset = () => {
    setAnalysisResult(null)
    setError(null)
    setLoading(false)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>NANO BANANA TA TOOL</h1>
        <p>AI-Powered Technical Analysis for Trading Charts</p>
      </header>

      <main className="app-main">
        {!analysisResult && !loading && (
          <UploadChart
            onAnalysisStart={handleAnalysisStart}
            onAnalysisComplete={handleAnalysisComplete}
            onError={handleError}
          />
        )}

        {loading && (
          <div className="loading-container">
            <div className="spinner"></div>
            <p style={{ color: '#000000', fontSize: '1.5rem', fontWeight: '900', letterSpacing: '2px', textTransform: 'uppercase', textShadow: 'var(--text-outline)', WebkitTextStroke: '2px rgba(255, 255, 255, 1)' }}>ANALYZING CHART...</p>
          </div>
        )}

        {error && (
          <div className="error-container">
            <h2>Error</h2>
            <p>{error}</p>
            <button onClick={handleReset} className="btn-primary">
              Try Again
            </button>
          </div>
        )}

        {analysisResult && (
          <AnnotatedChart
            result={analysisResult}
            onReset={handleReset}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>POWERED BY GOOGLE GEMINI VISION • BUILT WITH CURSOR & CLAUDE OPUS</p>
      </footer>
    </div>
  )
}

export default App

