import { useState, useCallback } from 'react'
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
    ? 'https://fortnite-skin-generator.onrender.com' 
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

  const handleFile = (file: File) => {
    console.log('File selected:', file.name, file.type, file.size)
    
    // Validate file type
    const validMimeTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
    const validExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    
    const isValidType = file.type && validMimeTypes.includes(file.type.toLowerCase())
    const isValidExtension = validExtensions.includes(fileExtension)
    
    if (!isValidType && !isValidExtension) {
      onError(`Please upload an image file (PNG, JPG, JPEG, GIF, or WEBP)`)
      return
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024
    if (file.size > maxSize) {
      onError(`File too large (${(file.size / 1024 / 1024).toFixed(2)}MB). Maximum size is 10MB`)
      return
    }

    // Create preview
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

    console.log('Sending request to:', `${API_URL}/generate`, 'with style:', selectedStyle)

    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        body: formData,
      })

      console.log('Response status:', response.status)

      if (!response.ok) {
        let errorMessage = `Server error: ${response.status}`
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
        } catch {
          // Use default error message
        }
        throw new Error(errorMessage)
      }

      const result: GenerationResult = await response.json()
      console.log('Generation complete:', result)
      
      if (!result.success) {
        throw new Error('Generation failed')
      }
      
      onGenerationComplete(result)
    } catch (err) {
      console.error('Upload error:', err)
      if (err instanceof TypeError && err.message.includes('fetch')) {
        onError(`Cannot connect to server at ${API_URL}. Is the backend running?`)
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
      {/* Upload Zone */}
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''} ${preview ? 'has-preview' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Preview" className="preview-image" />
            <button onClick={clearPreview} className="clear-btn">✕</button>
            <p className="preview-text">Ready to transform!</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">🎯</div>
            <h2>DROP YOUR IMAGE HERE</h2>
            <p>Upload any image to transform into a Fortnite skin</p>
            <p className="upload-hint">Person, character, meme, pet... anything works!</p>
            
            <input
              type="file"
              id="file-input"
              accept="image/*"
              onChange={handleFileInput}
              className="file-input"
            />
            <label htmlFor="file-input" className="btn-primary upload-btn">
              📁 CHOOSE FILE
            </label>
          </>
        )}
      </div>

      {/* Style Selector */}
      <div className="style-section">
        <h3>SELECT SKIN RARITY</h3>
        <div className="style-grid">
          {styles.map((style) => (
            <button
              key={style.id}
              className={`style-card ${selectedStyle === style.id ? 'selected' : ''}`}
              onClick={() => setSelectedStyle(style.id)}
              style={{ 
                '--rarity-color': style.color,
                borderColor: selectedStyle === style.id ? style.color : 'transparent'
              } as React.CSSProperties}
            >
              <span className="style-icon">{style.icon}</span>
              <span className="style-name">{style.name}</span>
              <span className="style-desc">{style.description}</span>
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
          {showAdvanced ? '▼' : '▶'} Advanced Options
        </button>
        
        {showAdvanced && (
          <div className="advanced-content">
            <label htmlFor="custom-prompt">Custom Instructions:</label>
            <textarea
              id="custom-prompt"
              value={customPrompt}
              onChange={(e) => setCustomPrompt(e.target.value)}
              placeholder="Add specific details... e.g., 'Make it look like a robot version' or 'Add fire effects'"
              rows={3}
            />
          </div>
        )}
      </div>

      {/* Generate Button */}
      {selectedFile && (
        <div className="generate-section">
          <button onClick={handleGenerate} className="btn-generate">
            <span className="btn-icon">⚡</span>
            <span className="btn-text">GENERATE FORTNITE SKIN</span>
          </button>
        </div>
      )}

      {/* Info Section */}
      <div className="info-section">
        <div className="info-card">
          <span className="info-icon">🖼️</span>
          <h4>Any Image</h4>
          <p>Upload selfies, characters, memes, pets, or anything!</p>
        </div>
        <div className="info-card">
          <span className="info-icon">🤖</span>
          <h4>AI Powered</h4>
          <p>Nano Banana AI transforms your image into Fortnite style</p>
        </div>
        <div className="info-card">
          <span className="info-icon">🎨</span>
          <h4>Multiple Styles</h4>
          <p>Choose from Legendary, Epic, Meme, Anime, and more!</p>
        </div>
      </div>
    </div>
  )
}

