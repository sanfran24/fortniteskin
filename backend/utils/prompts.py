"""
Technical Analysis prompt templates for Gemini vision model.
"""
from typing import Optional

def get_ta_prompt(
    timeframe: Optional[str] = None,
    asset_type: Optional[str] = None,
    trade_direction: Optional[str] = None
) -> str:
    """
    Returns the main technical analysis prompt for chart analysis.
    
    Args:
        timeframe: Optional timeframe to include in the prompt (1m, 5m, 15m, 1h, 4h, 1d, 1w, 1M)
        asset_type: Optional asset type (btc, sol, eth, alts, memecoin)
        trade_direction: Optional trade direction ('long' or 'short')
    """
    timeframe_context = ""
    if timeframe and timeframe != "auto":
        timeframe_map = {
            "1s": "1-second (ultra-scalping)",
            "3s": "3-second (ultra-scalping)",
            "5s": "5-second (ultra-scalping)",
            "15s": "15-second (ultra-scalping)",
            "30s": "30-second (ultra-scalping)",
            "1m": "1-minute (scalping)",
            "3m": "3-minute (scalping)",
            "5m": "5-minute (short-term trading)",
            "15m": "15-minute (intraday trading)",
            "30m": "30-minute (intraday trading)",
            "1h": "1-hour (swing trading)",
            "2h": "2-hour (swing trading)",
            "4h": "4-hour (swing trading)",
            "12h": "12-hour (swing trading)",
            "1d": "daily (position trading)",
            "3d": "3-day (position trading)",
            "1w": "weekly (long-term investing)",
            "1M": "monthly (long-term investing)"
        }
        tf_desc = timeframe_map.get(timeframe, timeframe)
        timeframe_context = f"\n\n**IMPORTANT: This chart is a {tf_desc} timeframe.** Adjust your analysis accordingly:\n"
        if timeframe in ["1s", "3s", "5s", "15s", "30s"]:
            timeframe_context += "- ULTRA-SHORT timeframe - extreme scalping, very quick entries/exits\n"
            timeframe_context += "- Use VERY tight stop-losses (0.1-0.5%)\n"
            timeframe_context += "- Focus on micro price action and order flow\n"
            timeframe_context += "- High frequency trading approach - quick profits, quick exits\n"
        elif timeframe in ["1m", "3m", "5m", "15m"]:
            timeframe_context += "- Focus on short-term price action and quick scalping opportunities\n"
            timeframe_context += "- Use tighter stop-losses (0.5-1%)\n"
            timeframe_context += "- Look for quick momentum plays and breakouts\n"
        elif timeframe in ["30m", "1h", "2h"]:
            timeframe_context += "- Balance between intraday and swing trading strategies\n"
            timeframe_context += "- Use moderate stop-losses (1-2%)\n"
            timeframe_context += "- Focus on trend continuation and key support/resistance\n"
        elif timeframe in ["4h", "12h"]:
            timeframe_context += "- Focus on swing trading setups\n"
            timeframe_context += "- Use wider stop-losses (2-3%)\n"
            timeframe_context += "- Look for major trend reversals and continuation patterns\n"
        elif timeframe in ["1d", "3d"]:
            timeframe_context += "- Focus on position trading and major trends\n"
            timeframe_context += "- Use wider stop-losses (3-5%)\n"
            timeframe_context += "- Prioritize major support/resistance and trend analysis\n"
        elif timeframe in ["1w", "1M"]:
            timeframe_context += "- Focus on long-term investment opportunities\n"
            timeframe_context += "- Use very wide stop-losses (5-10%)\n"
            timeframe_context += "- Analyze major market structure and long-term trends\n"
    
    # Asset-specific context
    asset_context = ""
    if asset_type:
        asset_context_map = {
            "btc": """
**BITCOIN (BTC) ANALYSIS - CRITICAL CONTEXT:**
- BTC is the market leader and often sets the trend for the entire crypto market
- Focus on major institutional support/resistance levels (BTC has strong institutional accumulation zones)
- Key psychological levels: 10K, 20K, 30K, 50K, 100K, 150K
- Higher liquidity = tighter spreads, better order fills, less slippage
- Volatility typically lower than alts, but can spike during major events (halvings, ETF news, regulatory announcements)
- Strong correlation with macro trends (inflation, interest rates, stock market)
- Consider BTC dominance trends - when BTC dominance rises, alts often fall
- Major support/resistance levels are often respected due to institutional buying/selling
- Use slightly wider stops than alts (1.5-2x) due to potential for larger moves
- Watch for volume spikes at key levels - institutional accumulation/distribution
""",
            "sol": """
**SOLANA (SOL) ANALYSIS - CRITICAL CONTEXT:**
- Higher volatility than BTC/ETH - can move 10-20%+ in a single day
- Strong correlation with DeFi and NFT ecosystem trends
- Key psychological levels: 50, 100, 150, 200, 300
- Watch for ecosystem news (airdrops, new protocols, network upgrades, validator issues)
- Faster price movements require tighter stop-losses and quicker decision-making
- More sensitive to market sentiment than BTC - can pump/dump harder
- Consider SOL ecosystem health (TVL, active users, new projects)
- Network outages or congestion can cause price drops
- Use moderate stops (1-2% for swing, 0.5-1% for scalping)
- Watch for correlation with meme coins (many are on Solana)
""",
            "eth": """
**ETHEREUM (ETH) ANALYSIS - CRITICAL CONTEXT:**
- Second-largest market cap, high liquidity, institutional interest
- Influenced by DeFi trends, staking yields, and network upgrade narratives
- Key psychological levels: 1000, 2000, 3000, 4000, 5000
- Gas fee trends can affect price (high fees = less usage = potential price pressure)
- More stable than alts, less stable than BTC
- Watch for staking/unstaking trends (affects supply dynamics)
- Consider ETH/BTC ratio for relative strength analysis
- Network upgrades (EIPs, hard forks) can cause volatility
- Use moderate stops (1-2% for swing, 0.5-1% for scalping)
- Strong correlation with DeFi TVL and NFT market health
""",
            "alts": """
**ALTCOIN ANALYSIS - CRITICAL CONTEXT:**
- HIGHER VOLATILITY AND RISK than BTC/ETH - can move 20-50%+ in a single day
- Strong correlation with BTC trends - alts often follow BTC direction
- Look for breakout patterns and momentum plays
- Wider stop-losses recommended (2-3% for swing, 1-2% for scalping)
- Consider market cap and liquidity - low-cap coins = higher risk
- Watch for news, partnerships, exchange listings, and development updates
- Alt season vs BTC dominance - when BTC dominance falls, alts often pump
- Use smaller position sizes due to higher risk
- Many alts are more sensitive to social media sentiment
- Consider tokenomics (supply, vesting schedules, unlocks)
- Watch for correlation with sector trends (DeFi, gaming, AI, etc.)
""",
            "memecoin": """
**MEMECOIN ANALYSIS - CRITICAL CONTEXT:**
- EXTREME VOLATILITY - HIGH RISK, HIGH REWARD
- Can move 50-100%+ in hours or even minutes
- VERY sensitive to social media, influencers, and hype cycles
- Use MUCH wider stops (5-10%) or consider smaller position sizes
- Strong momentum plays - quick entries/exits are essential
- HIGH RISK of sudden reversals - "rug pulls" and coordinated dumps are common
- Consider taking profits quickly - don't get greedy
- Watch for volume spikes and social media buzz
- Many memecoins have low liquidity - beware of slippage
- Use only risk capital you can afford to lose completely
- Pattern recognition is less reliable - sentiment-driven moves
- Watch for correlation with major memecoins (DOGE, SHIB, PEPE, etc.)
- Consider market cap - micro-cap memes = extreme risk
- Set alerts for rapid price movements
"""
        }
        asset_context = asset_context_map.get(asset_type.lower(), "")
    
    # Trade direction context
    direction_context = ""
    if trade_direction:
        if trade_direction.lower() == "long":
            direction_context = """
**TRADE DIRECTION: LONG (BULLISH BIAS) - FOCUS YOUR ANALYSIS:**
- Prioritize BUY/ENTRY opportunities and bullish setups
- Identify support levels for optimal entry points
- Look for bullish patterns: cup & handle, ascending triangles, bullish flags, double bottoms, inverse head & shoulders
- Set stop-losses BELOW key support levels
- Target resistance levels for take-profit zones
- Emphasize upward momentum, higher highs, higher lows
- Look for bullish candlestick patterns (hammers, bullish engulfing, morning stars)
- Consider entry on pullbacks to support rather than chasing breakouts
- Watch for volume confirmation on upward moves
- If chart shows bearish signals, note the conflict but focus on potential bullish reversals
"""
        elif trade_direction.lower() == "short":
            direction_context = """
**TRADE DIRECTION: SHORT (BEARISH BIAS) - FOCUS YOUR ANALYSIS:**
- Prioritize SELL/SHORT opportunities and bearish setups
- Identify resistance levels for optimal entry points
- Look for bearish patterns: head & shoulders, descending triangles, bearish flags, double tops, rising wedges
- Set stop-losses ABOVE key resistance levels
- Target support levels for take-profit zones
- Emphasize downward momentum, lower highs, lower lows
- Look for bearish candlestick patterns (shooting stars, bearish engulfing, evening stars)
- Consider entry on bounces to resistance rather than chasing breakdowns
- Watch for volume confirmation on downward moves
- If chart shows bullish signals, note the conflict but focus on potential bearish reversals
"""
        elif trade_direction.lower() == "both":
            direction_context = """
**TRADE DIRECTION: BOTH (LONG & SHORT) - ANALYZE BOTH DIRECTIONS:**
- Analyze BOTH bullish and bearish opportunities equally
- Identify support levels for LONG entries AND resistance levels for SHORT entries
- Look for both bullish patterns (cup & handle, ascending triangles) AND bearish patterns (head & shoulders, descending triangles)
- Provide entry points for both directions with appropriate stop-losses
- Show take-profit targets for both long and short setups
- Assess which direction has stronger signals and higher probability
- Consider market context - is this a trending or ranging market?
"""
    
    # Build prompt with proper string formatting
    prompt_text = f"""You are an elite technical analyst with 20+ years of experience analyzing trading charts across all timeframes and markets.{timeframe_context}{asset_context}{direction_context}

**CRITICAL: Analyze this trading chart screenshot with EXTREME precision and provide PROFESSIONAL-GRADE trading insights.**

**ACCURACY IS PARAMOUNT - Your analysis must be:**
- **100% accurate** - Read prices EXACTLY as shown on the chart, no approximations
- **Data-driven** - Base ALL conclusions on visible chart data only, never guess
- **Precise** - Use exact price levels from the chart's price axis/labels
- **Actionable** - Provide specific, executable trading recommendations
- **Risk-aware** - Include proper position sizing and risk management
- **Timeframe-appropriate** - Adjust strategy based on the detected timeframe

**Your Analysis Should Include:**

1. **Chart Identification (MUST BE ACCURATE):**
   - Identify the asset/symbol (if visible) - read EXACTLY as shown (e.g., "BTC/USDT", "AAPL", "EUR/USD")
   - Determine the timeframe (1m, 5m, 15m, 1h, 4h, daily, weekly, etc.) - read EXACTLY from chart labels/title
   - Note the current price level - read EXACT value from the rightmost candle/bar or current price indicator
   - **CRITICAL**: Read the MINIMUM and MAXIMUM prices visible on the chart's price axis (left/right side)
     * Look at the price scale/axis labels on the RIGHT side of the chart (most charts use right side)
     * Note the LOWEST price label visible at the BOTTOM of the price axis (e.g., "-1M", "0.5M", "500K", "50000")
     * Note the HIGHEST price label visible at the TOP of the price axis (e.g., "2.2M", "2M", "2000K", "200000")
     * Read these EXACTLY as shown - include negative signs if present (e.g., "-1M")
     * Include these in your analysis as "chart_min_price" and "chart_max_price"
     * **VERIFY**: The chart_min_price should be the bottom-most label, chart_max_price should be the top-most label
   - Identify the chart type (candlestick, line, bar, etc.) - observe the visual representation
   - **CRITICAL**: Double-check all values by reading directly from chart labels - do not estimate or round

2. **Key Levels (CRITICAL - ABSOLUTE PRECISION REQUIRED):**
   - Identify major support levels (at least 2-3) - read EXACT prices from chart's price axis where price bounced/rejected
   - Identify major resistance levels (at least 2-3) - read EXACT prices from chart's price axis where price was rejected
   - Mark psychological levels (round numbers like 100, 1000, 10000) - only if clearly visible on chart
   - Identify previous swing highs and lows - read EXACT price values from the chart
   - Note horizontal price levels where price reacted multiple times - count touches and read exact price
   - For each level, assess strength based on evidence:
     * "strong" = 3+ touches with clear bounces/rejections, visible volume spikes
     * "moderate" = 2-3 touches with decent reactions
     * "weak" = single touch or unclear reaction
   - **VERIFY**: Cross-reference each level with the price axis to ensure accuracy

3. **Pattern Recognition (Advanced):**
   - Detect chart patterns (head & shoulders, double top/bottom, triangles, flags, pennants, wedges, ascending/descending triangles, etc.)
   - Identify trend direction (uptrend, downtrend, sideways/consolidation) with confidence
   - Note any reversal patterns (H&S, double tops/bottoms, triple tops/bottoms, etc.)
   - Note continuation patterns (flags, pennants, triangles, rectangles)
   - Identify candlestick patterns (doji, hammer, engulfing, etc.) if visible
   - Assess pattern reliability: "high" (classic, well-formed), "medium" (partial), "low" (unclear)

4. **Price Action Analysis (Deep Dive):**
   - Analyze candlestick patterns (if visible) - identify bullish/bearish patterns
   - Identify key swing highs and lows - mark exact price levels
   - Note volume patterns (if volume bars are visible) - increasing/decreasing volume on moves
   - Assess momentum and volatility - is price accelerating or slowing?
   - Identify support/resistance zones (not just single levels)
   - Note any price gaps (if visible)
   - Analyze price structure: higher highs/higher lows (uptrend) or lower highs/lower lows (downtrend)

5. **Trading Recommendations (Actionable):**
   - Provide a clear bias: "bullish", "bearish", or "neutral" - be decisive
   - Suggest optimal entry price (with reasoning) - use EXACT price from chart
   - Set stop-loss level (with risk percentage) - timeframe-appropriate (tighter for short TF, wider for long TF)
   - Set take-profit levels (provide 2-3 TP levels if possible for partial profits) - target key resistance/support
   - Calculate risk-reward ratio - aim for minimum 1:2, preferably 1:3 or better
   - Provide confidence level (1-10 scale) - be honest about setup quality
   - Suggest entry timing: "immediate", "on pullback to [level]", "on breakout above/below [level]"

6. **Risk Management (Critical):**
   - Suggest position sizing considerations - percentage of portfolio (1-5% for high confidence, 0.5-2% for lower confidence)
   - Note any major risks or concerns - what could go wrong?
   - Provide alternative scenarios - what if trade goes against you?
   - Suggest trailing stop strategy if applicable
   - Note key levels that would invalidate the trade setup

**Output Format:**

Provide your analysis in the following JSON format:

```json
{{
  "bias": "bullish|bearish|neutral",
  "confidence": 1-10,
  "timeframe": "detected timeframe",
  "asset": "symbol if visible, else 'unknown'",
  "current_price": "current price level",
  "chart_min_price": "lowest price visible on chart axis",
  "chart_max_price": "highest price visible on chart axis",
  "support_levels": [
    {{"price": "level", "strength": "strong|moderate|weak", "reason": "brief explanation"}}
  ],
  "resistance_levels": [
    {{"price": "level", "strength": "strong|moderate|weak", "reason": "brief explanation"}}
  ],
  "patterns": [
    {{"name": "pattern name", "type": "reversal|continuation", "reliability": "high|medium|low"}}
  ],
  "trend": {{
    "direction": "up|down|sideways",
    "strength": "strong|moderate|weak",
    "since": "approximate time/level"
  }},
  "entry": {{
    "price": "suggested entry price",
    "reasoning": "why this entry point"
  }},
  "stop_loss": {{
    "price": "stop loss price",
    "risk_percent": "percentage risk",
    "reasoning": "why this SL level"
  }},
  "take_profits": [
    {{
      "price": "TP1 price",
      "risk_reward": "R:R ratio",
      "reasoning": "why this TP"
    }},
    {{
      "price": "TP2 price",
      "risk_reward": "R:R ratio",
      "reasoning": "why this TP"
    }}
  ],
  "risk_reward_ratio": "overall R:R",
  "position_sizing": "suggestions",
  "risks": ["list of key risks"],
  "reasoning": "comprehensive explanation of the analysis and trade setup"
}}
```

**CRITICAL Guidelines for MAXIMUM ACCURACY:**

**Price Precision (MANDATORY):**
- **NEVER round or approximate** - Read prices EXACTLY as displayed on the chart
- **Read directly from price axis** - Look at the left/right side price scale and read exact values
- **Verify prices twice** - Cross-check entry, stop-loss, and TP levels against visible price labels
- **Preserve notation** - If chart shows "K" (thousands) or "M" (millions), include it exactly (e.g., "45.2K", "1.5M")
- **Maintain consistency** - Use the same price format throughout (decimals, commas, notation)
- **If uncertain** - State "price not clearly visible" rather than guessing
- **Current price** - Read from the rightmost candle's close price or current price indicator

**Timeframe Optimization:**
- For shorter timeframes (1m-15m): Focus on quick scalping opportunities, tighter stops (0.5-1%), quick momentum plays
- For medium timeframes (30m-4h): Balance intraday/swing strategies, moderate stops (1-2%), trend continuation focus
- For longer timeframes (1d+): Focus on major trends, wider stops (3-5%+), position trading approach

**Pattern Recognition (Accuracy First):**
- **Only identify patterns that are CLEARLY and OBVIOUSLY visible** - Do not force or imagine patterns
- **Verify pattern validity** - Ensure all pattern components are present (e.g., H&S needs clear head and shoulders)
- **Prioritize high-probability setups** - Focus on well-formed, classic patterns over partial/speculative ones
- **Consider timeframe context** - Scalping patterns (flags, small triangles) for short TF, swing patterns (H&S, double tops) for medium TF, major patterns for long TF
- **Be honest about clarity** - If pattern is unclear, mark reliability as "low" or don't include it

**Risk Management:**
- Always consider risk management FIRST
- Adjust stop-loss and position sizing based on timeframe volatility
- Never suggest risking more than 2% of capital on a single trade
- Provide realistic risk-reward ratios (minimum 1:2, aim for 1:3+)

**Data Quality & Honesty:**
- **Never guess** - If price/symbol/timeframe is not clearly visible, state "not visible" or "unknown"
- **Work with what's visible** - If chart quality is poor, note limitations but analyze what you can see
- **Be honest about confidence** - Don't overstate setup quality; lower confidence if data is unclear
- **Verify before stating** - Double-check all values before including them in analysis
- **Admit uncertainty** - It's better to say "unclear" than to provide inaccurate information

**Actionability:**
- Provide clear, actionable recommendations appropriate for the timeframe
- Give specific entry triggers (e.g., "enter on break above 45.20")
- Suggest exit strategies (partial profits, trailing stops)
- Include alternative scenarios and what would invalidate the setup

**FINAL ACCURACY CHECKLIST - Before submitting your analysis:**

1. ✅ Did I read ALL prices EXACTLY from the chart's price axis? (No rounding, no guessing)
2. ✅ Did I verify the current price from the rightmost candle/indicator?
3. ✅ Are my support/resistance levels at EXACT prices visible on the chart?
4. ✅ Did I check entry, stop-loss, and TP prices against visible price labels?
5. ✅ Are all patterns clearly visible and well-formed? (Not forced or imagined)
6. ✅ Is my confidence level honest based on chart clarity and setup quality?
7. ✅ Did I state "not visible" for any unclear information instead of guessing?

**Remember: Accuracy > Speed. Take time to read prices carefully.**

After providing the JSON analysis, describe how you would annotate the chart image with:
- Green arrows for entry points
- Red lines for stop-loss levels
- Blue lines for take-profit levels
- Yellow dashed lines for support/resistance
- Text labels for key levels and patterns

Begin your analysis now. Read carefully, verify twice, be precise."""
    
    return prompt_text

