# Advanced Features Implementation Plan

## Overview
Add asset type selection (BTC, SOL, ETH, Alts, Memecoin) and trade direction (Short/Long) options to enhance chart analysis.

---

## Feature 1: Asset Type Selection

### Purpose
Allow users to specify the asset type so the AI can provide more context-aware analysis (e.g., memecoins have different volatility patterns than BTC).

### UI Changes

#### Frontend: `UploadChart.tsx`
**Location**: Above or below the timeframe selector

**New Component**:
```typescript
// Asset type selector
<select value={assetType} onChange={(e) => setAssetType(e.target.value)}>
  <option value="auto">Auto-detect</option>
  <option value="btc">Bitcoin (BTC)</option>
  <option value="sol">Solana (SOL)</option>
  <option value="eth">Ethereum (ETH)</option>
  <option value="alts">Altcoins</option>
  <option value="memecoin">Memecoin</option>
</select>
```

**Styling**:
- Match existing cow skin theme
- Bold font, white outline
- Same styling as timeframe selector
- Place between timeframe selector and upload zone

**State Management**:
- Add `assetType` state (default: "auto")
- Pass to backend in FormData

---

## Feature 2: Trade Direction Selection (Optional)

### Purpose
Allow users to specify if they're looking for long or short opportunities, helping the AI focus analysis accordingly.

### UI Changes

#### Frontend: `UploadChart.tsx`
**Location**: Next to asset type selector (horizontal layout)

**New Component**:
```typescript
// Trade direction selector (optional)
<div className="trade-direction-selector">
  <label>Trade Direction (Optional):</label>
  <div className="direction-buttons">
    <button 
      className={tradeDirection === 'long' ? 'active' : ''}
      onClick={() => setTradeDirection('long')}
    >
      📈 LONG
    </button>
    <button 
      className={tradeDirection === 'short' ? 'active' : ''}
      onClick={() => setTradeDirection('short')}
    >
      📉 SHORT
    </button>
    <button 
      className={tradeDirection === null ? 'active' : ''}
      onClick={() => setTradeDirection(null)}
    >
      🔄 BOTH
    </button>
  </div>
</div>
```

**Styling**:
- Button group with 3 options: LONG, SHORT, BOTH
- Active state: Highlighted with cow skin theme colors
- Bold text, white outlines
- Optional indicator (can be left as "BOTH")

**State Management**:
- Add `tradeDirection` state (default: `null` = "both")
- Only send to backend if not null
- If null, AI analyzes both directions

---

## Backend Changes

### API Endpoint: `backend/main.py`

#### New Form Parameters
```python
@app.post("/analyze")
async def analyze_chart(
    file: UploadFile = File(...),
    timeframe: str = Form(default="auto"),
    asset_type: str = Form(default="auto"),      # NEW
    trade_direction: Optional[str] = Form(default=None)  # NEW
):
```

#### Pass to Prompt Generator
```python
prompt = get_ta_prompt(
    timeframe=timeframe if timeframe != "auto" else None,
    asset_type=asset_type if asset_type != "auto" else None,  # NEW
    trade_direction=trade_direction  # NEW
)
```

---

## Prompt Engineering Changes

### File: `backend/utils/prompts.py`

#### Function Signature Update
```python
def get_ta_prompt(
    timeframe: Optional[str] = None,
    asset_type: Optional[str] = None,      # NEW
    trade_direction: Optional[str] = None  # NEW
) -> str:
```

#### Asset Type Context
Add context based on asset type:

```python
asset_context = ""
if asset_type:
    asset_context_map = {
        "btc": """
**BITCOIN (BTC) ANALYSIS:**
- Focus on major support/resistance levels (BTC has strong institutional levels)
- Consider macro trends and market dominance
- Higher liquidity = tighter spreads, better fills
- Major psychological levels: 10K, 20K, 30K, 50K, 100K
- Volatility typically lower than alts, but can spike during major events
""",
        "sol": """
**SOLANA (SOL) ANALYSIS:**
- Higher volatility than BTC/ETH
- Strong correlation with DeFi and NFT trends
- Key levels: 50, 100, 150, 200
- Watch for ecosystem news (airdrops, new protocols)
- Faster price movements, tighter stop-losses recommended
""",
        "eth": """
**ETHEREUM (ETH) ANALYSIS:**
- Second-largest market cap, high liquidity
- Influenced by DeFi, staking, and upgrade narratives
- Key levels: 1000, 2000, 3000, 4000
- Gas fee trends can affect price
- More stable than alts, less than BTC
""",
        "alts": """
**ALTCOIN ANALYSIS:**
- Higher volatility and risk
- Strong correlation with BTC trends
- Look for breakout patterns and momentum
- Wider stop-losses recommended (3-5%)
- Consider market cap and liquidity
- Watch for news and partnerships
""",
        "memecoin": """
**MEMECOIN ANALYSIS:**
- EXTREME volatility - high risk, high reward
- Very sensitive to social media and hype
- Can move 50-100%+ in hours
- Use wider stops (5-10%) or consider smaller position sizes
- Strong momentum plays, quick entries/exits
- High risk of sudden reversals
- Consider taking profits quickly
"""
    }
    asset_context = asset_context_map.get(asset_type.lower(), "")
```

#### Trade Direction Context
Add bias based on trade direction:

```python
direction_context = ""
if trade_direction:
    if trade_direction.lower() == "long":
        direction_context = """
**TRADE DIRECTION: LONG (BULLISH BIAS)**
- Focus on BUY/ENTRY opportunities
- Identify support levels for entries
- Look for bullish patterns (cup & handle, ascending triangles, etc.)
- Set stop-losses below key support
- Target resistance levels for take-profits
- Emphasize bullish setups and upward momentum
"""
    elif trade_direction.lower() == "short":
        direction_context = """
**TRADE DIRECTION: SHORT (BEARISH BIAS)**
- Focus on SELL/SHORT opportunities
- Identify resistance levels for entries
- Look for bearish patterns (head & shoulders, descending triangles, etc.)
- Set stop-losses above key resistance
- Target support levels for take-profits
- Emphasize bearish setups and downward momentum
"""
```

#### Integrate into Prompt
Add both contexts to the main prompt:
```python
prompt_text = f"""You are an elite technical analyst...
{timeframe_context}
{asset_context}
{direction_context}
...
```

---

## UI/UX Enhancements

### Visual Improvements

1. **Layout**:
   ```
   [Timeframe Selector]
   [Asset Type Selector]  [Trade Direction Buttons]
   [Upload Zone]
   ```

2. **Styling**:
   - Match existing cow skin theme
   - Bold fonts, white outlines
   - Active states for selected options
   - Hover effects on buttons

3. **Responsive Design**:
   - Stack vertically on mobile
   - Horizontal layout on desktop

### User Flow

1. User selects timeframe (existing)
2. User selects asset type (new)
3. User optionally selects trade direction (new)
4. User uploads chart
5. Analysis includes asset-specific and direction-specific insights

---

## Analysis Result Enhancements

### Display Changes: `AnnotatedChart.tsx`

#### Show Selected Options
Display the selected asset type and trade direction in the results:

```typescript
<div className="analysis-metadata">
  <span>Asset: {analysis.asset_type || 'Auto-detected'}</span>
  <span>Direction: {analysis.trade_direction || 'Both'}</span>
  <span>Timeframe: {analysis.timeframe}</span>
</div>
```

#### Enhanced Summary Card
- Highlight if analysis matches selected direction
- Show asset-specific risk warnings (especially for memecoins)
- Display direction-specific confidence levels

---

## Backend Response Updates

### Analysis JSON Structure
Add new fields to response:

```json
{
  "analysis": {
    "asset_type": "btc",           // NEW: Detected or selected
    "trade_direction": "long",     // NEW: If user specified
    "asset_specific_notes": "...", // NEW: Asset-specific insights
    "direction_bias": "bullish",   // NEW: Based on direction selection
    ...
  }
}
```

---

## Caching Considerations

### Cache Key Update
Update cache key to include new parameters:

```python
def get_cache_path(image_hash: str, timeframe: str, asset_type: str, trade_direction: Optional[str]) -> Path:
    """Get cache file path including all parameters"""
    params = f"{timeframe}_{asset_type}"
    if trade_direction:
        params += f"_{trade_direction}"
    return CACHE_DIR / f"{image_hash}_{params}.json"
```

**Note**: Same chart with different asset_type/direction = different cache entries (different analysis)

---

## Implementation Order

### Phase 1: Asset Type Selection
1. ✅ Add UI component to `UploadChart.tsx`
2. ✅ Add state management
3. ✅ Update backend API to accept `asset_type`
4. ✅ Update prompt generator with asset context
5. ✅ Test with different asset types

### Phase 2: Trade Direction Selection
1. ✅ Add UI component (optional buttons)
2. ✅ Add state management
3. ✅ Update backend API to accept `trade_direction`
4. ✅ Update prompt generator with direction context
5. ✅ Test long/short/both scenarios

### Phase 3: Enhanced Display
1. ✅ Show selected options in results
2. ✅ Highlight direction-specific insights
3. ✅ Add asset-specific warnings/notes
4. ✅ Update styling

### Phase 4: Caching & Optimization
1. ✅ Update cache key generation
2. ✅ Test cache behavior with new parameters
3. ✅ Optimize prompt length if needed

---

## Testing Checklist

- [ ] Asset type selection works in UI
- [ ] Trade direction buttons work (long/short/both)
- [ ] Backend receives new parameters correctly
- [ ] Prompt includes asset-specific context
- [ ] Prompt includes direction-specific context
- [ ] Analysis reflects selected asset type
- [ ] Analysis reflects selected trade direction
- [ ] Cache works correctly with new parameters
- [ ] UI displays selected options in results
- [ ] Styling matches cow skin theme
- [ ] Mobile responsive design works

---

## Edge Cases to Handle

1. **Auto-detect asset**: If user selects "auto", AI should detect from chart
2. **No direction selected**: Default to analyzing both long and short
3. **Mismatched direction**: If chart shows bearish but user selected long, AI should note this
4. **Cache conflicts**: Same image, different parameters = different cache entries
5. **Invalid combinations**: Handle gracefully (e.g., memecoin + very tight stops)

---

## Future Enhancements (Not in Scope)

- Save user preferences
- Recent asset types dropdown
- Custom asset type input
- Multiple timeframe analysis
- Comparison mode (BTC vs ETH)
- Historical performance tracking

---

## Files to Modify

### Frontend
- `frontend/src/components/UploadChart.tsx` - Add selectors
- `frontend/src/components/UploadChart.css` - Style new components
- `frontend/src/components/AnnotatedChart.tsx` - Display new data
- `frontend/src/components/AnnotatedChart.css` - Style new displays

### Backend
- `backend/main.py` - Add form parameters
- `backend/utils/prompts.py` - Add asset/direction context
- `backend/main.py` - Update cache key generation

---

## Estimated Impact

- **User Experience**: ⬆️ Significantly improved (more control, better analysis)
- **Analysis Quality**: ⬆️ Better (context-aware, direction-focused)
- **Code Complexity**: ⬆️ Moderate increase
- **Performance**: ➡️ Minimal impact (prompt slightly longer)
- **Cache Size**: ⬆️ Slight increase (more cache entries per image)

---

## Ready for Implementation?

This plan provides:
- ✅ Clear UI/UX design
- ✅ Backend API changes
- ✅ Prompt engineering details
- ✅ Caching strategy
- ✅ Testing checklist
- ✅ Implementation phases

**Next Step**: Review plan, then proceed with Phase 1 implementation.

