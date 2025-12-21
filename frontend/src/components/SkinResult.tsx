import { useState } from 'react'
import { GenerationResult } from '../App'
import './SkinResult.css'

interface SkinResultProps {
  result: GenerationResult
  onReset: () => void
}

export default function SkinResult({ result, onReset }: SkinResultProps) {
  const [activeTab, setActiveTab] = useState<'generated' | 'original'>('generated')
  const [expandedDescription, setExpandedDescription] = useState(false)

  const getRarityColor = (style: string) => {
    const colors: Record<string, string> = {
      legendary: '#ff9800',
      epic: '#e040fb',
      rare: '#29b6f6',
      uncommon: '#66bb6a',
      common: '#bdbdbd',
      meme: '#ff9800',
      anime: '#f48fb1',
      cyberpunk: '#00e5ff',
      peely: '#ffeb3b',
    }
    return colors[style.toLowerCase()] || '#e040fb'
  }

  const getPrice = (style: string) => {
    const prices: Record<string, string> = {
      legendary: '2,000',
      epic: '1,500',
      rare: '1,200',
      uncommon: '800',
      common: '500',
    }
    return prices[style.toLowerCase()] || '1,500'
  }

  const hasGeneratedImages = result.generated_images && result.generated_images.length > 0

  return (
    <div className="skin-result-container">
      {/* Left Panel - Details */}
      <div className="details-panel">
        {/* Header */}
        <div className="result-header">
          <span 
            className="rarity-badge" 
            style={{ backgroundColor: getRarityColor(result.style) }}
          >
            {result.style.toUpperCase()}
          </span>
          <h2>{result.skin_details?.name || 'CUSTOM SKIN'}</h2>
        </div>

        {/* Stats */}
        <div className="stats-grid">
          <div className="stat-card" style={{ '--stat-color': getRarityColor(result.style) } as React.CSSProperties}>
            <span className="stat-label">Rarity</span>
            <span className="stat-value">{result.style}</span>
          </div>
          {result.skin_details?.set && (
            <div className="stat-card" style={{ '--stat-color': '#29b6f6' } as React.CSSProperties}>
              <span className="stat-label">Set</span>
              <span className="stat-value">{result.skin_details.set}</span>
            </div>
          )}
          <div className="stat-card" style={{ '--stat-color': '#66bb6a' } as React.CSSProperties}>
            <span className="stat-label">Back Bling</span>
            <span className="stat-value">{result.skin_details?.back_bling || 'Included'}</span>
          </div>
          <div className="stat-card" style={{ '--stat-color': '#e040fb' } as React.CSSProperties}>
            <span className="stat-label">Pickaxe</span>
            <span className="stat-value">{result.skin_details?.pickaxe || 'Matching'}</span>
          </div>
        </div>

        {/* Description */}
        {result.description && (
          <div className="description-card">
            <h3>📜 Skin Concept</h3>
            <div className={`description-content ${expandedDescription ? 'expanded' : ''}`}>
              <p>{result.description}</p>
            </div>
            {result.description.length > 400 && (
              <button 
                className="expand-btn"
                onClick={() => setExpandedDescription(!expandedDescription)}
              >
                {expandedDescription ? '▲ Less' : '▼ More'}
              </button>
            )}
          </div>
        )}

        {/* Actions */}
        <div className="action-buttons">
          {hasGeneratedImages && (
            <a 
              href={result.generated_images[0]} 
              download={`fortnite-skin-${result.style}.png`}
              className="btn-download"
            >
              ⬇️ Download Skin
            </a>
          )}
          <button 
            className="btn-share"
            onClick={() => {
              navigator.clipboard.writeText('Check out my AI-generated Fortnite skin! Made with Fortnite Skin Generator')
              alert('Copied to clipboard!')
            }}
          >
            📋 Share
          </button>
          <button onClick={onReset} className="btn-new">
            🔄 Create New Skin
          </button>
        </div>
      </div>

      {/* Right Panel - Preview */}
      <div className="preview-panel">
        <div className="character-display">
          {/* Tabs */}
          <div className="image-tabs">
            {hasGeneratedImages && (
              <button 
                className={`tab-btn ${activeTab === 'generated' ? 'active' : ''}`}
                onClick={() => setActiveTab('generated')}
              >
                ✨ Generated
              </button>
            )}
            <button 
              className={`tab-btn ${activeTab === 'original' ? 'active' : ''}`}
              onClick={() => setActiveTab('original')}
            >
              📷 Original
            </button>
          </div>

          {/* Image */}
          <div className="image-display">
            {activeTab === 'generated' && hasGeneratedImages ? (
              <div className="generated-images">
                {result.generated_images.map((img, idx) => (
                  <img 
                    key={idx}
                    src={img} 
                    alt={`Generated Skin ${idx + 1}`}
                    className="result-image generated"
                  />
                ))}
              </div>
            ) : activeTab === 'generated' && !hasGeneratedImages ? (
              <div className="no-image-placeholder">
                <span className="placeholder-icon">🎨</span>
                <p>Image generation in description mode</p>
                <p className="placeholder-sub">Check the skin concept on the left!</p>
              </div>
            ) : (
              <img 
                src={result.original_image} 
                alt="Original"
                className="result-image original"
              />
            )}
          </div>

          {/* Shop Price */}
          <div className="shop-preview">
            <h4>Item Shop Price</h4>
            <div className="shop-price">
              <span className="vbucks-icon">💎</span>
              <span>{getPrice(result.style)}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
