import { useState, useCallback } from 'react'
import { AnalysisResult } from '../App'
import './UploadChart.css'

interface UploadChartProps {
  onAnalysisStart: () => void
  onAnalysisComplete: (result: AnalysisResult) => void
  onError: (error: string) => void
}

// @ts-ignore - Vite env types
// In production, this will use VITE_API_URL from .env.production
// Defaults to Render backend URL for production, localhost for development
const API_URL = import.meta.env.VITE_API_URL || (
  import.meta.env.PROD 
    ? 'https://nano-banana-ta-backend.onrender.com' 
    : 'http://localhost:8000'
)

export default function UploadChart({
  onAnalysisStart,
  onAnalysisComplete,
  onError,
}: UploadChartProps) {
  const [isDragging, setIsDragging] = useState(false)
  const [preview, setPreview] = useState<string | null>(null)
  const [timeframe, setTimeframe] = useState<string>('auto')

  const handleFile = async (file: File) => {
    console.log('File selected:', file.name, file.type, file.size)
    
    // Validate file type - check MIME type or extension
    const validMimeTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
    const validExtensions = ['.png', '.jpg', '.jpeg', '.gif', '.webp']
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase()
    
    const isValidType = file.type && validMimeTypes.includes(file.type.toLowerCase())
    const isValidExtension = validExtensions.includes(fileExtension)
    
    if (!isValidType && !isValidExtension) {
      onError(`Please upload an image file (PNG, JPG, JPEG, GIF, or WEBP). Received: ${file.type || 'unknown type'}`)
      return
    }

    // Validate file size (max 10MB)
    const maxSize = 10 * 1024 * 1024 // 10MB
    if (file.size > maxSize) {
      onError(`File too large (${(file.size / 1024 / 1024).toFixed(2)}MB). Maximum size is 10MB`)
      return
    }

    if (file.size === 0) {
      onError('File is empty')
      return
    }

    // Create preview
    const reader = new FileReader()
    reader.onload = (e) => {
      setPreview(e.target?.result as string)
    }
    reader.readAsDataURL(file)

    // Upload and analyze
    onAnalysisStart()

    const formData = new FormData()
    formData.append('file', file)
    formData.append('timeframe', timeframe)

    console.log('Sending request to:', `${API_URL}/analyze`, 'with timeframe:', timeframe)
    console.log('File details:', { name: file.name, type: file.type, size: file.size })

    try {
      const response = await fetch(`${API_URL}/analyze`, {
        method: 'POST',
        body: formData,
        // Don't set Content-Type header - browser will set it with boundary for multipart/form-data
      })

      console.log('Response status:', response.status, response.statusText)
      console.log('Response headers:', Object.fromEntries(response.headers.entries()))

      if (!response.ok) {
        let errorMessage = `Server error: ${response.status} ${response.statusText}`
        const contentType = response.headers.get('content-type')
        
        try {
          if (contentType && contentType.includes('application/json')) {
            const errorData = await response.json()
            errorMessage = errorData.detail || errorData.message || errorMessage
            console.error('Error response JSON:', errorData)
          } else {
            const text = await response.text()
            console.error('Error response text:', text)
            errorMessage = text || errorMessage
          }
        } catch (parseError) {
          console.error('Failed to parse error response:', parseError)
        }
        throw new Error(errorMessage)
      }

      const contentType = response.headers.get('content-type')
      if (!contentType || !contentType.includes('application/json')) {
        const text = await response.text()
        console.error('Unexpected response type:', contentType, text.substring(0, 200))
        throw new Error('Server returned non-JSON response')
      }

      const result: AnalysisResult = await response.json()
      console.log('Analysis complete:', result)
      
      if (!result.success) {
        throw new Error('Analysis failed - server returned success: false')
      }
      
      onAnalysisComplete(result)
    } catch (err) {
      console.error('Upload error:', err)
      if (err instanceof TypeError) {
        if (err.message.includes('fetch') || err.message.includes('Failed to fetch')) {
          onError('Failed to connect to server. Make sure the backend is running on http://localhost:8000')
        } else {
          onError(`Network error: ${err.message}`)
        }
      } else if (err instanceof Error) {
        onError(err.message)
      } else {
        onError('Failed to analyze chart. Please try again.')
      }
    }
  }

  const handleDrop = useCallback(
    (e: React.DragEvent<HTMLDivElement>) => {
      e.preventDefault()
      setIsDragging(false)

      const file = e.dataTransfer.files[0]
      if (file) {
        handleFile(file)
      }
    },
    []
  )

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
    if (file) {
      handleFile(file)
    }
  }

  return (
    <div className="upload-container">
      <div
        className={`upload-zone ${isDragging ? 'dragging' : ''}`}
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
      >
        {preview ? (
          <div className="preview-container">
            <img src={preview} alt="Chart preview" className="preview-image" />
            <p className="preview-text">Chart ready for analysis</p>
          </div>
        ) : (
          <>
            <div className="upload-icon">📊</div>
            <h2>UPLOAD TRADING CHART</h2>
            <p>Drag and drop your chart screenshot here, or click to browse</p>
            
            <div className="timeframe-selector">
              <label htmlFor="timeframe-select" className="timeframe-label">
                Chart Timeframe:
              </label>
              <select
                id="timeframe-select"
                value={timeframe}
                onChange={(e) => setTimeframe(e.target.value)}
                className="timeframe-select"
              >
                <option value="auto">Auto-detect (Recommended)</option>
                <option value="1m">1 Minute</option>
                <option value="5m">5 Minutes</option>
                <option value="15m">15 Minutes</option>
                <option value="30m">30 Minutes</option>
                <option value="1h">1 Hour</option>
                <option value="4h">4 Hours</option>
                <option value="1d">Daily</option>
                <option value="1w">Weekly</option>
                <option value="1M">Monthly</option>
              </select>
            </div>
            
            <input
              type="file"
              id="file-input"
              accept="image/*"
              onChange={handleFileInput}
              className="file-input"
            />
            <label htmlFor="file-input" className="btn-primary">
              CHOOSE FILE
            </label>
          </>
        )}
      </div>

      <div className="upload-info">
        <h3>SUPPORTED FORMATS</h3>
        <ul>
          <li>PNG, JPG, JPEG images</li>
          <li>Clear, high-resolution charts work best</li>
          <li>Any timeframe (1m to weekly)</li>
          <li>Any asset type (stocks, crypto, forex, etc.)</li>
        </ul>
      </div>
    </div>
  )
}

