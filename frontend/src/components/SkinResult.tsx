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
      legendary: '#f5a623',
      epic: '#9b59b6',
      rare: '#3498db',
      uncommon: '#2ecc71',
      common: '#b4b4b4',
      collab: '#e74c3c',
      meme: '#f39c12',
      anime: '#ff6b9d',
      cyberpunk: '#00ffff',
      fantasy: '#8e44ad',
      horror: '#1a1a2e',
      peely: '#ffeb3b',
      slurp: '#00bcd4',
    }
    return colors[style.toLowerCase()] || '#9b59b6'
  }

  const hasGeneratedImages = result.generated_images && result.generated_images.length > 0

  return (
    <div className="skin-result-container">
      {/* Header */}
      <div className="result-header">
        <div className="rarity-badge" style={{ backgroundColor: getRarityColor(result.style) }}>
          {result.style.toUpperCase()}
        </div>
        <h2>
          {result.skin_details?.name || 'YOUR FORTNITE SKIN'}
        </h2>
        <button onClick={onReset} className="btn-secondary">
          🔄 CREATE ANOTHER
        </button>
      </div>

      {/* Main Content */}
      <div className="result-content">
        {/* Image Display */}
        <div className="image-section">
          {/* Tab Buttons */}
          <div className="image-tabs">
            {hasGeneratedImages && (
              <button 
                className={`tab-btn ${activeTab === 'generated' ? 'active' : ''}`}
                onClick={() => setActiveTab('generated')}
              >
                ✨ Generated Skin
              </button>
            )}
            <button 
              className={`tab-btn ${activeTab === 'original' ? 'active' : ''}`}
              onClick={() => setActiveTab('original')}
            >
              📷 Original
            </button>
          </div>

          {/* Image Display */}
          <div className="image-display">
            {activeTab === 'generated' && hasGeneratedImages ? (
              <div className="generated-images">
                {result.generated_images.map((img, idx) => (
                  <img 
                    key={idx}
                    src={img} 
                    alt={`Generated Fortnite Skin ${idx + 1}`}
                    className="result-image generated"
                  />
                ))}
              </div>
            ) : activeTab === 'generated' && !hasGeneratedImages ? (
              <div className="no-image-placeholder">
                <span className="placeholder-icon">🎨</span>
                <p>Image generation not available in this mode</p>
                <p className="placeholder-sub">Check out the detailed description below!</p>
              </div>
            ) : (
              <img 
                src={result.original_image} 
                alt="Original image"
                className="result-image original"
              />
            )}
          </div>

          {/* Download Button */}
          {hasGeneratedImages && activeTab === 'generated' && (
            <div className="download-section">
              <a 
                href={result.generated_images[0]} 
                download={`fortnite-skin-${result.style}.png`}
                className="btn-download"
              >
                ⬇️ DOWNLOAD SKIN
              </a>
            </div>
          )}
        </div>

        {/* Skin Details */}
        <div className="details-section">
          {/* Quick Stats */}
          <div className="stats-grid">
            <div className="stat-card">
              <span className="stat-label">RARITY</span>
              <span className="stat-value" style={{ color: getRarityColor(result.style) }}>
                {result.style.toUpperCase()}
              </span>
            </div>
            {result.skin_details?.set && (
              <div className="stat-card">
                <span className="stat-label">SET</span>
                <span className="stat-value">{result.skin_details.set}</span>
              </div>
            )}
            {result.skin_details?.back_bling && (
              <div className="stat-card">
                <span className="stat-label">BACK BLING</span>
                <span className="stat-value">{result.skin_details.back_bling}</span>
              </div>
            )}
            {result.skin_details?.pickaxe && (
              <div className="stat-card">
                <span className="stat-label">PICKAXE</span>
                <span className="stat-value">{result.skin_details.pickaxe}</span>
              </div>
            )}
          </div>

          {/* Description */}
          {result.description && (
            <div className="description-card">
              <h3>📜 SKIN CONCEPT</h3>
              <div className={`description-content ${expandedDescription ? 'expanded' : ''}`}>
                <p>{result.description}</p>
              </div>
              {result.description.length > 500 && (
                <button 
                  className="expand-btn"
                  onClick={() => setExpandedDescription(!expandedDescription)}
                >
                  {expandedDescription ? '▲ Show Less' : '▼ Read More'}
                </button>
              )}
            </div>
          )}

          {/* Item Shop Preview */}
          <div className="item-shop-preview">
            <h3>🛒 ITEM SHOP PREVIEW</h3>
            <div className="shop-card" style={{ borderColor: getRarityColor(result.style) }}>
              <div className="shop-image">
                {hasGeneratedImages ? (
                  <img src={result.generated_images[0]} alt="Shop preview" />
                ) : (
                  <img src={result.original_image} alt="Shop preview" />
                )}
                <div className="shop-rarity-bar" style={{ backgroundColor: getRarityColor(result.style) }}></div>
              </div>
              <div className="shop-info">
                <span className="shop-name">{result.skin_details?.name || 'Custom Skin'}</span>
                <span className="shop-price">
                  <span className="vbucks-icon">💎</span>
                  {result.style === 'legendary' ? '2,000' : 
                   result.style === 'epic' ? '1,500' : 
                   result.style === 'rare' ? '1,200' : 
                   result.style === 'uncommon' ? '800' : '1,500'}
                </span>
              </div>
            </div>
          </div>

          {/* Share Section */}
          <div className="share-section">
            <h3>📤 SHARE YOUR SKIN</h3>
            <div className="share-buttons">
              <button className="share-btn twitter" onClick={() => {
                const text = `Check out this AI-generated Fortnite skin concept! 🎮✨ Made with Fortnite Skin Generator`
                window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}`, '_blank')
              }}>
                🐦 Twitter
              </button>
              <button className="share-btn copy" onClick={() => {
                navigator.clipboard.writeText('Made with Fortnite Skin Generator - AI powered by Nano Banana!')
                alert('Link copied to clipboard!')
              }}>
                📋 Copy Link
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

