import { useState } from 'react'
import { AnalysisResult } from '../App'
import './AnnotatedChart.css'

interface AnnotatedChartProps {
  result: AnalysisResult
  onReset: () => void
}

export default function AnnotatedChart({ result, onReset }: AnnotatedChartProps) {
  const { analysis, original_image } = result
  const [activeModal, setActiveModal] = useState<string | null>(null)

  const openModal = (moduleId: string) => {
    setActiveModal(moduleId)
  }

  const closeModal = () => {
    setActiveModal(null)
  }

  const getBiasColor = (bias?: string) => {
    if (!bias) return '#666'
    const lower = bias.toLowerCase()
    if (lower.includes('bullish')) return '#10b981'
    if (lower.includes('bearish')) return '#ef4444'
    return '#6b7280'
  }

  const getConfidenceColor = (confidence?: number) => {
    if (!confidence) return '#666'
    if (confidence >= 7) return '#10b981'
    if (confidence >= 4) return '#f59e0b'
    return '#ef4444'
  }

  return (
    <div className="annotated-chart-container">
      <div className="chart-header">
        <h2>ANALYSIS RESULTS</h2>
        {result.metadata && (
          <div className="analysis-metadata">
            {result.metadata.asset_type && result.metadata.asset_type !== 'auto' && (
              <span className="metadata-badge">
                Asset: {result.metadata.asset_type.toUpperCase()}
              </span>
            )}
            {result.metadata.trade_direction && (
              <span className="metadata-badge">
                Direction: {result.metadata.trade_direction.toUpperCase()}
              </span>
            )}
            {result.metadata.timeframe && result.metadata.timeframe !== 'auto' && (
              <span className="metadata-badge">
                Timeframe: {result.metadata.timeframe.toUpperCase()}
              </span>
            )}
          </div>
        )}
        <button onClick={onReset} className="btn-secondary">
          ANALYZE ANOTHER CHART
        </button>
      </div>

      <div className="chart-content">
        {/* Chart Display */}
        <div className="chart-display-section">
          <div className="chart-wrapper">
            {result.annotated_image ? (
              <div>
                <h3 style={{ marginBottom: '1rem', color: '#000000', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: '900', fontSize: '1.8rem', textShadow: 'var(--text-outline)', WebkitTextStroke: '2px rgba(255, 255, 255, 1)' }}>ANNOTATED CHART</h3>
                <img
                  src={result.annotated_image}
                  alt="Annotated trading chart"
                  className="chart-image annotated"
                />
                {original_image && (
                  <details style={{ marginTop: '1rem' }}>
                    <summary style={{ cursor: 'pointer', color: '#000000', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '1px', fontWeight: '900', fontSize: '1.1rem', textShadow: 'var(--text-outline)', WebkitTextStroke: '1.5px rgba(255, 255, 255, 1)' }}>
                      VIEW ORIGINAL CHART
                    </summary>
                    <img
                      src={original_image}
                      alt="Original trading chart"
                      className="chart-image"
                      style={{ marginTop: '0.5rem' }}
                    />
                  </details>
                )}
              </div>
            ) : (
              original_image && (
                <div>
                  <h3 style={{ marginBottom: '1rem', color: '#000000', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: '900', fontSize: '1.8rem', textShadow: 'var(--text-outline)', WebkitTextStroke: '2px rgba(255, 255, 255, 1)' }}>CHART</h3>
                  <img
                    src={original_image}
                    alt="Trading chart"
                    className="chart-image"
                  />
                  {result.annotated_image === null && (
                    <p style={{ marginTop: '0.5rem', color: '#000000', fontSize: '1.2rem', textTransform: 'uppercase', letterSpacing: '1px', fontWeight: '900', textShadow: 'var(--text-outline)', WebkitTextStroke: '1.5px rgba(255, 255, 255, 1)' }}>
                      ⚠️ VISUAL ANNOTATIONS COULD NOT BE GENERATED. ANALYSIS DATA IS SHOWN BELOW.
                    </p>
                  )}
                </div>
              )
            )}
          </div>
        </div>

        {/* Analysis Panel */}
        <div className="analysis-panel">
          {/* Summary Card */}
          <div 
            className="analysis-card summary"
            onClick={() => openModal('summary')}
            style={{ cursor: 'pointer' }}
          >
            <h3 className="module-header">
              <span className="module-title">
                SUMMARY
              </span>
              <button onClick={(e) => { e.stopPropagation(); openModal('summary'); }} className="popup-btn" title="Open in full screen">
                🔍
              </button>
            </h3>
            <div className="module-content">
            <div className="summary-grid">
              <div className="summary-item">
                <span className="label">Bias:</span>
                <span
                  className="value bias"
                  style={{ color: getBiasColor(analysis.bias) }}
                >
                  {analysis.bias?.toUpperCase() || 'N/A'}
                </span>
              </div>
              <div className="summary-item">
                <span className="label">Confidence:</span>
                <span
                  className="value"
                  style={{ color: getConfidenceColor(analysis.confidence) }}
                >
                  {analysis.confidence ? `${analysis.confidence}/10` : 'N/A'}
                </span>
              </div>
              <div className="summary-item">
                <span className="label">Timeframe:</span>
                <span className="value">{analysis.timeframe || 'N/A'}</span>
              </div>
              <div className="summary-item">
                <span className="label">Asset:</span>
                <span className="value">{analysis.asset || 'Unknown'}</span>
              </div>
              {analysis.current_price && (
                <div className="summary-item">
                  <span className="label">Current Price:</span>
                  <span className="value">{analysis.current_price}</span>
                </div>
              )}
            </div>
            </div>
          </div>

          {/* Entry/Exit Points */}
          {(analysis.entry || analysis.stop_loss || analysis.take_profits) && (
            <div 
              className="analysis-card"
              onClick={() => openModal('trade-setup')}
              style={{ cursor: 'pointer' }}
            >
              <h3 className="module-header">
                <span className="module-title">
                  TRADE SETUP
                </span>
                <button onClick={(e) => { e.stopPropagation(); openModal('trade-setup'); }} className="popup-btn" title="Open in full screen">
                  🔍
                </button>
              </h3>
              <div className="module-content">
              <>
              {analysis.entry && (
                <div className="trade-item entry">
                  <span className="trade-label">Entry:</span>
                  <span className="trade-value">{analysis.entry.price}</span>
                  <p className="trade-reasoning">{analysis.entry.reasoning}</p>
                </div>
              )}
              {analysis.stop_loss && (
                <div className="trade-item stop-loss">
                  <span className="trade-label">Stop Loss:</span>
                  <span className="trade-value">{analysis.stop_loss.price}</span>
                  <span className="risk-badge">
                    {analysis.stop_loss.risk_percent} risk
                  </span>
                  <p className="trade-reasoning">{analysis.stop_loss.reasoning}</p>
                </div>
              )}
              {analysis.take_profits && analysis.take_profits.length > 0 && (
                <div className="trade-item take-profit">
                  <span className="trade-label">Take Profits:</span>
                  <div className="tp-list">
                    {analysis.take_profits.map((tp, idx) => (
                      <div key={idx} className="tp-item">
                        <span className="tp-price">TP{idx + 1}: {tp.price}</span>
                        <span className="tp-rr">R:R {tp.risk_reward}</span>
                        <p className="tp-reasoning">{tp.reasoning}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
              {analysis.risk_reward_ratio && (
                <div className="risk-reward">
                  <span className="label">Overall Risk:Reward:</span>
                  <span className="value">{analysis.risk_reward_ratio}</span>
                </div>
              )}
              </>
              </div>
            </div>
          )}

          {/* Support/Resistance */}
          {(analysis.support_levels?.length || analysis.resistance_levels?.length) && (
            <div 
              className="analysis-card"
              onClick={() => openModal('key-levels')}
              style={{ cursor: 'pointer' }}
            >
              <h3 className="module-header">
                <span className="module-title">
                  KEY LEVELS
                </span>
                <button onClick={(e) => { e.stopPropagation(); openModal('key-levels'); }} className="popup-btn" title="Open in full screen">
                  🔍
                </button>
              </h3>
              <div className="module-content">
              <>
              {analysis.support_levels && analysis.support_levels.length > 0 && (
                <div className="levels-section">
                  <h4>SUPPORT LEVELS</h4>
                  <ul className="levels-list">
                    {analysis.support_levels.map((level, idx) => (
                      <li key={idx} className={`level-item support ${level.strength}`}>
                        <span className="level-price">{level.price}</span>
                        <span className="level-strength">{level.strength}</span>
                        <p className="level-reason">{level.reason}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              {analysis.resistance_levels && analysis.resistance_levels.length > 0 && (
                <div className="levels-section">
                  <h4>RESISTANCE LEVELS</h4>
                  <ul className="levels-list">
                    {analysis.resistance_levels.map((level, idx) => (
                      <li key={idx} className={`level-item resistance ${level.strength}`}>
                        <span className="level-price">{level.price}</span>
                        <span className="level-strength">{level.strength}</span>
                        <p className="level-reason">{level.reason}</p>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              </>
              </div>
            </div>
          )}

          {/* Patterns */}
          {analysis.patterns && analysis.patterns.length > 0 && (
            <div 
              className="analysis-card"
              onClick={() => openModal('patterns')}
              style={{ cursor: 'pointer' }}
            >
              <h3 className="module-header">
                <span className="module-title">
                  DETECTED PATTERNS
                </span>
                <button onClick={(e) => { e.stopPropagation(); openModal('patterns'); }} className="popup-btn" title="Open in full screen">
                  🔍
                </button>
              </h3>
              <div className="module-content">
              <ul className="patterns-list">
                {analysis.patterns.map((pattern, idx) => (
                  <li key={idx} className="pattern-item">
                    <span className="pattern-name">{pattern.name}</span>
                    <span className={`pattern-type ${pattern.type}`}>
                      {pattern.type}
                    </span>
                    <span className={`pattern-reliability ${pattern.reliability}`}>
                      {pattern.reliability} reliability
                    </span>
                  </li>
                ))}
              </ul>
              </div>
            </div>
          )}

          {/* Trend */}
          {analysis.trend && (
            <div 
              className="analysis-card"
              onClick={() => openModal('trend')}
              style={{ cursor: 'pointer' }}
            >
              <h3 className="module-header">
                <span className="module-title">
                  TREND ANALYSIS
                </span>
                <button onClick={(e) => { e.stopPropagation(); openModal('trend'); }} className="popup-btn" title="Open in full screen">
                  🔍
                </button>
              </h3>
              <div className="module-content">
              <div className="trend-info">
                <div className="trend-item">
                  <span className="label">Direction:</span>
                  <span className={`value trend-${analysis.trend.direction}`}>
                    {analysis.trend.direction.toUpperCase()}
                  </span>
                </div>
                <div className="trend-item">
                  <span className="label">Strength:</span>
                  <span className="value">{analysis.trend.strength}</span>
                </div>
                {analysis.trend.since && (
                  <div className="trend-item">
                    <span className="label">Since:</span>
                    <span className="value">{analysis.trend.since}</span>
                  </div>
                )}
              </div>
              </div>
            </div>
          )}

          {/* Risks */}
          {analysis.risks && analysis.risks.length > 0 && (
            <div 
              className="analysis-card risks"
              onClick={() => openModal('risks')}
              style={{ cursor: 'pointer' }}
            >
              <h3 className="module-header">
                <span className="module-title">
                  RISKS & CONSIDERATIONS
                </span>
                <button onClick={(e) => { e.stopPropagation(); openModal('risks'); }} className="popup-btn" title="Open in full screen">
                  🔍
                </button>
              </h3>
              <div className="module-content">
              <ul className="risks-list">
                {analysis.risks.map((risk, idx) => (
                  <li key={idx}>{risk}</li>
                ))}
              </ul>
              </div>
            </div>
          )}

          {/* Reasoning */}
          {analysis.reasoning && (
            <div 
              className="analysis-card reasoning"
              onClick={() => openModal('reasoning')}
              style={{ cursor: 'pointer' }}
            >
              <h3 className="module-header">
                <span className="module-title">
                  DETAILED ANALYSIS
                </span>
                <button onClick={(e) => { e.stopPropagation(); openModal('reasoning'); }} className="popup-btn" title="Open in full screen">
                  🔍
                </button>
              </h3>
              <div className="module-content">
              <p className="reasoning-text">{analysis.reasoning}</p>
              </div>
            </div>
          )}

          {/* Position Sizing */}
          {analysis.position_sizing && (
            <div 
              className="analysis-card"
              onClick={() => openModal('position-sizing')}
              style={{ cursor: 'pointer' }}
            >
              <h3 className="module-header">
                <span className="module-title">
                  POSITION SIZING
                </span>
                <button onClick={(e) => { e.stopPropagation(); openModal('position-sizing'); }} className="popup-btn" title="Open in full screen">
                  🔍
                </button>
              </h3>
              <div className="module-content">
              <p>{analysis.position_sizing}</p>
              </div>
            </div>
          )}

          {/* Raw Response (if JSON parsing failed) - Show at bottom, collapsed */}
          {analysis.parsed === false && result.raw_response && (
            <details className="analysis-card raw-response">
              <summary style={{ cursor: 'pointer', color: 'var(--text-secondary)' }}>
                <h3 style={{ display: 'inline' }}>RAW ANALYSIS RESPONSE</h3>
              </summary>
              <pre className="raw-text">{result.raw_response}</pre>
            </details>
          )}
        </div>
      </div>

      {/* Modal Overlay */}
      {activeModal && (
        <div className="modal-overlay" onClick={closeModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <button className="modal-close" onClick={closeModal}>✕</button>
            {activeModal === 'summary' && (
              <div className="modal-module">
                <h2>SUMMARY</h2>
                <div className="summary-grid modal-grid">
                  <div className="summary-item">
                    <span className="label">Bias:</span>
                    <span className="value bias" style={{ color: getBiasColor(analysis.bias) }}>
                      {analysis.bias?.toUpperCase() || 'N/A'}
                    </span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Confidence:</span>
                    <span className="value" style={{ color: getConfidenceColor(analysis.confidence) }}>
                      {analysis.confidence ? `${analysis.confidence}/10` : 'N/A'}
                    </span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Timeframe:</span>
                    <span className="value">{analysis.timeframe || 'N/A'}</span>
                  </div>
                  <div className="summary-item">
                    <span className="label">Asset:</span>
                    <span className="value">{analysis.asset || 'Unknown'}</span>
                  </div>
                  {analysis.current_price && (
                    <div className="summary-item">
                      <span className="label">Current Price:</span>
                      <span className="value">{analysis.current_price}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
            {activeModal === 'trade-setup' && (
              <div className="modal-module">
                <h2>TRADE SETUP</h2>
                {analysis.entry && (
                  <div className="trade-item entry">
                    <span className="trade-label">Entry:</span>
                    <span className="trade-value">{analysis.entry.price}</span>
                    <p className="trade-reasoning">{analysis.entry.reasoning}</p>
                  </div>
                )}
                {analysis.stop_loss && (
                  <div className="trade-item stop-loss">
                    <span className="trade-label">Stop Loss:</span>
                    <span className="trade-value">{analysis.stop_loss.price}</span>
                    <span className="risk-badge">{analysis.stop_loss.risk_percent} risk</span>
                    <p className="trade-reasoning">{analysis.stop_loss.reasoning}</p>
                  </div>
                )}
                {analysis.take_profits && analysis.take_profits.length > 0 && (
                  <div className="trade-item take-profit">
                    <span className="trade-label">Take Profits:</span>
                    <div className="tp-list">
                      {analysis.take_profits.map((tp, idx) => (
                        <div key={idx} className="tp-item">
                          <span className="tp-price">TP{idx + 1}: {tp.price}</span>
                          <span className="tp-rr">R:R {tp.risk_reward}</span>
                          <p className="tp-reasoning">{tp.reasoning}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {analysis.risk_reward_ratio && (
                  <div className="risk-reward">
                    <span className="label">Overall Risk:Reward:</span>
                    <span className="value">{analysis.risk_reward_ratio}</span>
                  </div>
                )}
              </div>
            )}
            {activeModal === 'key-levels' && (
              <div className="modal-module">
                <h2>KEY LEVELS</h2>
                {analysis.support_levels && analysis.support_levels.length > 0 && (
                  <div className="levels-section">
                    <h4>SUPPORT LEVELS</h4>
                    <ul className="levels-list">
                      {analysis.support_levels.map((level, idx) => (
                        <li key={idx} className={`level-item support ${level.strength}`}>
                          <span className="level-price">{level.price}</span>
                          <span className="level-strength">{level.strength}</span>
                          <p className="level-reason">{level.reason}</p>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
                {analysis.resistance_levels && analysis.resistance_levels.length > 0 && (
                  <div className="levels-section">
                    <h4>RESISTANCE LEVELS</h4>
                    <ul className="levels-list">
                      {analysis.resistance_levels.map((level, idx) => (
                        <li key={idx} className={`level-item resistance ${level.strength}`}>
                          <span className="level-price">{level.price}</span>
                          <span className="level-strength">{level.strength}</span>
                          <p className="level-reason">{level.reason}</p>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
            {activeModal === 'patterns' && (
              <div className="modal-module">
                <h2>DETECTED PATTERNS</h2>
                <ul className="patterns-list">
                  {analysis.patterns?.map((pattern, idx) => (
                    <li key={idx} className="pattern-item">
                      <span className="pattern-name">{pattern.name}</span>
                      <span className={`pattern-type ${pattern.type}`}>{pattern.type}</span>
                      <span className={`pattern-reliability ${pattern.reliability}`}>
                        {pattern.reliability} reliability
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
            {activeModal === 'trend' && (
              <div className="modal-module">
                <h2>TREND ANALYSIS</h2>
                <div className="trend-info">
                  <div className="trend-item">
                    <span className="label">Direction:</span>
                    <span className={`value trend-${analysis.trend?.direction}`}>
                      {analysis.trend?.direction.toUpperCase()}
                    </span>
                  </div>
                  <div className="trend-item">
                    <span className="label">Strength:</span>
                    <span className="value">{analysis.trend?.strength}</span>
                  </div>
                  {analysis.trend?.since && (
                    <div className="trend-item">
                      <span className="label">Since:</span>
                      <span className="value">{analysis.trend.since}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
            {activeModal === 'risks' && (
              <div className="modal-module">
                <h2>RISKS & CONSIDERATIONS</h2>
                <ul className="risks-list">
                  {analysis.risks?.map((risk, idx) => (
                    <li key={idx}>{risk}</li>
                  ))}
                </ul>
              </div>
            )}
            {activeModal === 'reasoning' && (
              <div className="modal-module">
                <h2>DETAILED ANALYSIS</h2>
                <p className="reasoning-text">{analysis.reasoning}</p>
              </div>
            )}
            {activeModal === 'position-sizing' && (
              <div className="modal-module">
                <h2>POSITION SIZING</h2>
                <p>{analysis.position_sizing}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

