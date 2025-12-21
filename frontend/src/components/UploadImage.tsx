import { useState, useCallback, useRef } from 'react'
import { GenerationResult, SkinStyle } from '../App'
import './UploadImage.css'

interface UploadImageProps {
  styles: SkinStyle[]
  onGenerationStart: () => void
  onGenerationComplete: (result: GenerationResult) => void
  onError: (error: string) => void
}

const API_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.PROD 
    ? 'https://fortniteskin-backend.onrender.com' 
    : 'http://localhost:8000'
)

export default function UploadImage({
  styles,
  onGenerationStart,
  onGenerationComplete,
  onError,
}: UploadImageProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [selectedStyle, setSelectedStyle] = useState<string>('legendary')
  const [customPrompt, setCustomPrompt] = useState<string>('')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const fileInputRef = useRef<HTMLInputElement>(null)

  const handleFile = (file: File) => {
    const validMimeTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
    const validExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    
    const isValidType = file.type && validMimeTypes.includes(file.type.toLowerCase())
    const isValidExtension = validExtensions.includes(fileExtension)
    
    if (!isValidType && !isValidExtension) {
      onError(`Please upload an image file (PNG, JPG, GIF, WEBP)`)
      return
    }

    const maxSize = 10 * 1024 * 1024
    if (file.size > maxSize) {
      onError(`File too large. Maximum size is 10MB`)
      return
    }

    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target?.result as string)
    }
    reader.readAsDataURL(file)
    setSelectedFile(file)
  }

  const handleGenerate = async () => {
    if (!selectedFile) {
      onError('Please select an image first')
      return
    }

    onGenerationStart()

    const formData = new FormData()
    formData.append('file', selectedFile)
    formData.append('style', selectedStyle)
    if (customPrompt) {
      formData.append('custom_prompt', customPrompt)
    }

    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        body: formData,
      })

      if (!response.ok) {
        let errorMessage = `Server error: ${response.status}`
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
        } catch {
          // Use default
        }
        throw new Error(errorMessage)
      }

      const result: GenerationResult = await response.json()
      if (!result.success) {
        throw new Error('Generation failed')
      }
      
      onGenerationComplete(result)
    } catch (err) {
      if (err instanceof TypeError && err.message.includes('fetch')) {
        onError(`Cannot connect to server. Is the backend running?`)
      } else if (err instanceof Error) {
        onError(err.message)
      } else {
        onError('Failed to generate skin. Please try again.')
      }
    }
  }

  const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }, [])

  const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) handleFile(file)
  }

  const clearPreview = () => {
    setPreview(null)
    setSelectedFile(null)
  }


  return (
    <div className="upload-container">
      {/* Left Panel - Locker Style */}
      <div className="left-panel">
        <div className="panel-header">
          <h2>🎮 Skin Generator</h2>
        </div>

        {/* Style Selection */}
        <div className="style-section">
          <h3>SELECT RARITY</h3>
          <div className="style-grid">
            {styles.map((style) => (
              <button
                key={style.id}
                className={`style-card ${selectedStyle === style.id ? 'selected' : ''}`}
                onClick={() => setSelectedStyle(style.id)}
                style={{ '--rarity-color': style.color } as React.CSSProperties}
              >
                <span className="style-icon">{style.icon}</span>
                <span className="style-name">{style.name}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Advanced Options */}
        <div className="advanced-section">
          <button 
            className="advanced-toggle"
            onClick={() => setShowAdvanced(!showAdvanced)}
          >
            {showAdvanced ? '▼' : '▶'} OPTIONS
          </button>
          
          {showAdvanced && (
            <div className="advanced-content">
              <label>Custom Instructions:</label>
              <textarea
                value={customPrompt}
                onChange={(e) => setCustomPrompt(e.target.value)}
                placeholder="Add fire effects, make it robot style..."
                rows={2}
              />
            </div>
          )}
        </div>
      </div>

      {/* Right Panel - Character Preview */}
      <div className="right-panel">
        <div className="character-preview">
          <div
            className={`upload-zone ${isDragging ? 'dragging' : ''} ${preview ? 'has-preview' : ''}`}
            onDrop={handleDrop}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onClick={() => {
              if (!preview && fileInputRef.current) {
                fileInputRef.current.click();
              }
            }}
            style={{ cursor: preview ? 'default' : 'pointer' }}
          >
            {preview ? (
              <div className="preview-container">
                <img src={preview} alt="Preview" className="preview-image" />
                <button onClick={clearPreview} className="clear-btn">✕</button>
                <p className="preview-text">✓ Ready to generate</p>
              </div>
            ) : (
              <>
                <div className="upload-icon">🎯</div>
                <h2>Drop Image Here</h2>
                <p>Upload any image to transform</p>
                <p className="upload-hint">Selfies, characters, memes, pets...</p>
                
                <label className="upload-label" onClick={(e) => e.stopPropagation()}>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={handleFileInput}
                    ref={fileInputRef}
                  />
                  <span className="btn-primary upload-btn">📁 CHOOSE FILE</span>
                </label>
              </>
            )}
          </div>
        </div>

        {/* Generate Button */}
        {selectedFile && (
          <div className="generate-section">
            <button onClick={handleGenerate} className="btn-generate">
              <span className="btn-icon">⚡</span>
              <span>GENERATE SKIN</span>
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
