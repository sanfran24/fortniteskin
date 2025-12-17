"""
Image annotation utilities for drawing TA elements on charts.
"""
from PIL import Image, ImageDraw, ImageFont
import math
from typing import Dict, List, Optional, Tuple
import logging
import traceback

logger = logging.getLogger(__name__)


def estimate_price_y_position(price: float, min_price: float, max_price: float, 
                              image_height: int, chart_top: int = 50, 
                              chart_bottom: int = 50) -> int:
    """
    Estimate Y pixel position for a price level on the chart.
    Uses linear interpolation with improved accuracy.
    """
    chart_height = image_height - chart_top - chart_bottom
    price_range = max_price - min_price
    
    if price_range == 0 or price_range < 0:
        logger.warning(f"⚠️ Invalid price range: {min_price} - {max_price}, using center")
        return image_height // 2
    
    # Clamp price to valid range to avoid out-of-bounds
    clamped_price = max(min_price, min(price, max_price))
    if clamped_price != price:
        logger.warning(f"⚠️ Price {price} clamped to range [{min_price}, {max_price}] -> {clamped_price}")
    
    # Normalize price to 0-1 range (inverted because Y=0 is top)
    # Higher prices = lower Y position (top of chart)
    # Lower prices = higher Y position (bottom of chart)
    normalized = (max_price - clamped_price) / price_range
    
    # Ensure normalized is between 0 and 1
    normalized = max(0.0, min(1.0, normalized))
    
    # Convert to pixel position
    y_pos = chart_top + int(normalized * chart_height)
    
    # Clamp to chart bounds
    final_y = max(chart_top, min(y_pos, image_height - chart_bottom))
    
    logger.debug(f"📍 Price {price} -> Y={final_y} (normalized={normalized:.3f}, chart_height={chart_height}, range={min_price}-{max_price})")
    
    return final_y


def parse_price(price_str: str) -> Optional[float]:
    """Parse price string to float, handling common formats including K/M notation."""
    if not price_str:
        return None
    
    try:
        # Remove common characters and convert to string
        cleaned = str(price_str).replace('$', '').replace(',', '').replace(' ', '').strip().upper()
        
        # Handle various notation formats
        multiplier = 1
        
        # Check for "MILLION" or "MILL" text
        if 'MILLION' in cleaned or 'MILL' in cleaned:
            cleaned = cleaned.replace('MILLION', '').replace('MILL', '')
            multiplier = 1000000
        # Check for "THOUSAND" or "K" notation
        elif cleaned.endswith('K') or 'THOUSAND' in cleaned:
            if cleaned.endswith('K'):
                cleaned = cleaned[:-1]
            else:
                cleaned = cleaned.replace('THOUSAND', '')
            multiplier = 1000
        # Check for "M" notation (million)
        elif cleaned.endswith('M'):
            multiplier = 1000000
            cleaned = cleaned[:-1]
        # Check for "B" notation (billion)
        elif cleaned.endswith('B'):
            multiplier = 1000000000
            cleaned = cleaned[:-1]
        
        # Handle decimal numbers (e.g., "1.5M" = 1.5 * 1000000 = 1500000)
        price_value = float(cleaned)
        result = price_value * multiplier
        
        logger.debug(f"Parsed price '{price_str}' -> {price_value} * {multiplier} = {result}")
        return result
    except (ValueError, AttributeError) as e:
        logger.warning(f"Failed to parse price '{price_str}': {e}")
        return None


def get_price_range(analysis: Dict) -> Tuple[float, float]:
    """Estimate price range from analysis data with improved accuracy.
    
    Priority:
    1. Use chart_min_price/chart_max_price if provided (most accurate)
    2. Use min/max of all prices in analysis
    3. Fallback to defaults
    """
    prices = []
    price_strings = []  # Keep original strings for debugging
    
    # FIRST PRIORITY: Use chart's visible price range if provided (most accurate)
    chart_min = analysis.get('chart_min_price')
    chart_max = analysis.get('chart_max_price')
    
    if chart_min and chart_max:
        parsed_min = parse_price(str(chart_min))
        parsed_max = parse_price(str(chart_max))
        if parsed_min is not None and parsed_max is not None and parsed_min < parsed_max:
            logger.info(f"✅ Using chart's visible price range: {parsed_min:,.2f} - {parsed_max:,.2f}")
            return parsed_min, parsed_max
        else:
            logger.warning(f"⚠️ Invalid chart price range: {chart_min} - {chart_max}, falling back to analysis prices")
    
    # SECOND PRIORITY: Collect all price values from analysis
    def add_price(price_str, source=""):
        if price_str:
            parsed = parse_price(str(price_str))
            if parsed is not None:
                prices.append(parsed)
                price_strings.append(f"{price_str} ({source}) -> {parsed}")
    
    if analysis.get('current_price'):
        add_price(analysis['current_price'], 'current_price')
    
    if analysis.get('entry') and analysis['entry'].get('price'):
        add_price(analysis['entry']['price'], 'entry')
    
    if analysis.get('stop_loss') and analysis['stop_loss'].get('price'):
        add_price(analysis['stop_loss']['price'], 'stop_loss')
    
    if analysis.get('take_profits'):
        for tp in analysis['take_profits']:
            if tp.get('price'):
                add_price(tp['price'], 'take_profit')
    
    if analysis.get('support_levels'):
        for level in analysis['support_levels']:
            if level.get('price'):
                add_price(level['price'], 'support')
    
    if analysis.get('resistance_levels'):
        for level in analysis['resistance_levels']:
            if level.get('price'):
                add_price(level['price'], 'resistance')
    
    logger.info(f"📊 Collected {len(prices)} prices: {price_strings[:10]}")
    
    if len(prices) < 2:
        # Default range if we can't determine
        if prices:
            base = prices[0]
            # Use wider range for single price
            range_pct = 0.2  # 20% above and below
            logger.warning(f"⚠️ Only one price found ({base}), using range: {base * (1 - range_pct)} - {base * (1 + range_pct)}")
            return base * (1 - range_pct), base * (1 + range_pct)
        logger.warning("⚠️ No prices found, using default range 0-100")
        return 0, 100
    
    min_price = min(prices)
    max_price = max(prices)
    
    # Add padding - use percentage-based padding for better accuracy
    price_range = max_price - min_price
    
    # For large price ranges (like millions), use smaller percentage padding
    # For small ranges, use larger percentage padding
    if price_range > 1000000:  # Millions range
        padding_pct = 0.05  # 5% padding
    elif price_range > 1000:  # Thousands range
        padding_pct = 0.1  # 10% padding
    else:  # Small numbers
        padding_pct = 0.15  # 15% padding
    
    padding = price_range * padding_pct
    
    result_min = min_price - padding
    result_max = max_price + padding
    
    logger.info(f"💰 Price range: {min_price} - {max_price} (range: {price_range})")
    logger.info(f"📏 With {padding_pct*100}% padding: {result_min} - {result_max}")
    
    return result_min, result_max


def draw_arrow(draw: ImageDraw.Draw, x: int, y: int, direction: str = 'up', 
               color: Tuple[int, int, int] = (0, 255, 0), size: int = 20):
    """Draw an arrow pointing up or down."""
    if direction == 'up':
        # Up arrow (for entry)
        points = [
            (x, y - size),  # Top point
            (x - size//2, y - size//2),  # Left
            (x - size//4, y - size//2),  # Left inner
            (x - size//4, y + size//2),  # Left bottom
            (x + size//4, y + size//2),  # Right bottom
            (x + size//4, y - size//2),  # Right inner
            (x + size//2, y - size//2),  # Right
        ]
    else:
        # Down arrow (for stop loss)
        points = [
            (x, y + size),  # Bottom point
            (x - size//2, y + size//2),  # Left
            (x - size//4, y + size//2),  # Left inner
            (x - size//4, y - size//2),  # Left top
            (x + size//4, y - size//2),  # Right top
            (x + size//4, y + size//2),  # Right inner
            (x + size//2, y + size//2),  # Right
        ]
    
    draw.polygon(points, fill=color, outline=color)


def annotate_chart(image: Image.Image, analysis: Dict) -> Image.Image:
    """
    Annotate a chart image with TA analysis.
    """
    # Handle case where analysis is just raw text (parsing failed)
    if not isinstance(analysis, dict):
        logger.warning("Analysis is not a dict, returning original image")
        return image.copy()
    
    # Force annotation - even if parsed=False, try to use what we have
    has_data = any([
        analysis.get('entry'),
        analysis.get('stop_loss'),
        analysis.get('take_profits'),
        analysis.get('support_levels'),
        analysis.get('resistance_levels'),
        analysis.get('current_price')
    ])
    
    logger.info(f"🔍 Checking for annotation data - Has entry: {bool(analysis.get('entry'))}, Has SL: {bool(analysis.get('stop_loss'))}, Has TPs: {bool(analysis.get('take_profits'))}, Has supports: {bool(analysis.get('support_levels'))}, Has resistances: {bool(analysis.get('resistance_levels'))}")
    
    # If parsed=False but we have raw_text, try to extract prices
    if not has_data and analysis.get('parsed') == False and analysis.get('raw_text'):
        import re
        logger.info("📝 Attempting to extract prices from raw text...")
        # More comprehensive price pattern
        price_pattern = r'(?:price|entry|stop|loss|tp|take.profit|support|resistance)[\s:]*\$?(\d+\.?\d*)'
        prices = re.findall(price_pattern, analysis.get('raw_text', ''), re.IGNORECASE)
        if not prices:
            # Fallback: find any numbers that look like prices
            price_pattern = r'\b(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)\b'
            prices = re.findall(price_pattern, analysis.get('raw_text', ''))
        
        logger.info(f"📊 Extracted {len(prices)} prices from raw text: {prices[:5]}")
        
        if prices:
            # Create structure for annotation
            analysis = {
                'entry': {'price': prices[0] if len(prices) > 0 else None},
                'stop_loss': {'price': prices[1] if len(prices) > 1 else None},
                'take_profits': [{'price': p} for p in prices[2:4]] if len(prices) > 2 else [],
                'parsed': True
            }
            has_data = True
    
    # ALWAYS try to annotate if we have ANY price data - even just support/resistance
    if not has_data:
        logger.warning("⚠️ No price data found for annotation, returning original image")
        return image.copy()
    
    logger.info("✅ Proceeding with annotation - data found!")
    
    # Create a copy to draw on (ensure RGB mode)
    if image.mode != 'RGB':
        annotated = image.convert('RGB').copy()
    else:
        annotated = image.copy()
    draw = ImageDraw.Draw(annotated)
    
    width, height = image.size
    
    # Try to get price range
    try:
        min_price, max_price = get_price_range(analysis)
        logger.info(f"✅ Price range determined: {min_price:,.2f} - {max_price:,.2f}")
        
        # Validate price range
        if min_price >= max_price:
            logger.error(f"❌ Invalid price range: {min_price} >= {max_price}")
            # Try to fix by using a percentage range around the prices
            all_prices = []
            for key in ['current_price', 'entry', 'stop_loss']:
                if analysis.get(key) and isinstance(analysis[key], dict) and analysis[key].get('price'):
                    p = parse_price(str(analysis[key]['price']))
                    if p: all_prices.append(p)
            if analysis.get('take_profits'):
                for tp in analysis['take_profits']:
                    p = parse_price(str(tp.get('price', '')))
                    if p: all_prices.append(p)
            if all_prices:
                avg_price = sum(all_prices) / len(all_prices)
                min_price = avg_price * 0.8
                max_price = avg_price * 1.2
                logger.warning(f"⚠️ Fixed range using average: {min_price:,.2f} - {max_price:,.2f}")
            else:
                min_price, max_price = 0, 100
    except Exception as e:
        logger.error(f"❌ Could not determine price range: {e}\n{traceback.format_exc()}")
        min_price, max_price = 0, 100
    
    # Estimate chart area (use most of the image, but be more conservative)
    # Charts typically have price axis on left/right, so leave more margin
    chart_left = int(width * 0.08)  # 8% margin for price axis
    chart_right = int(width * 0.95)  # 5% margin
    chart_top = int(height * 0.08)  # 8% margin for top labels
    chart_bottom = int(height * 0.92)  # 8% margin for bottom
    
    logger.info(f"Annotating chart: {width}x{height}, chart area: {chart_left}-{chart_right}, {chart_top}-{chart_bottom}")
    logger.info(f"Has entry: {bool(analysis.get('entry'))}, Has SL: {bool(analysis.get('stop_loss'))}, Has TPs: {bool(analysis.get('take_profits'))}")
    
    # Get font
    try:
        font_large = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
        font_medium = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
        font_small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
    except:
        try:
            font_large = ImageFont.truetype("arial.ttf", 16)
            font_medium = ImageFont.truetype("arial.ttf", 14)
            font_small = ImageFont.truetype("arial.ttf", 12)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # Entry point (green arrow) - draw on right side
    if analysis.get('entry') and analysis['entry'].get('price'):
        entry_price = parse_price(str(analysis['entry']['price']))
        if entry_price:
            entry_y = estimate_price_y_position(entry_price, min_price, max_price, 
                                               height, chart_top, height - chart_bottom)
            entry_x = int(width * 0.75)  # Right side of chart
            
            logger.info(f"Drawing entry at price {entry_price}, Y position: {entry_y}")
            
            # Draw green arrow pointing up
            draw_arrow(draw, entry_x, entry_y, direction='up', 
                      color=(0, 255, 0), size=35)
            
            # Label with background
            entry_label = f"ENTRY\n{analysis['entry']['price']}"
            try:
                bbox = draw.textbbox((entry_x + 25, entry_y - 50), entry_label, font=font_large)
            except AttributeError:
                bbox = draw.textsize(entry_label, font=font_large)
                bbox = (entry_x + 25, entry_y - 50, entry_x + 25 + bbox[0], entry_y - 50 + bbox[1])
            # Draw background
            draw.rectangle([(bbox[0] - 8, bbox[1] - 6), (bbox[2] + 8, bbox[3] + 6)], 
                          fill=(0, 0, 0), outline=(0, 255, 0), width=3)
            draw.text((entry_x + 25, entry_y - 50), entry_label, 
                     fill=(0, 255, 0), font=font_large)
    
    # Stop Loss (red line) - make it very visible
    if analysis.get('stop_loss') and analysis['stop_loss'].get('price'):
        sl_price = parse_price(str(analysis['stop_loss']['price']))
        if sl_price:
            sl_y = estimate_price_y_position(sl_price, min_price, max_price, 
                                            height, chart_top, height - chart_bottom)
            
            logger.info(f"Drawing stop loss at price {sl_price}, Y position: {sl_y}")
            
            # Draw red horizontal line (thick)
            draw.line([(chart_left, sl_y), (chart_right, sl_y)], 
                     fill=(255, 0, 0), width=5)
            
            # Dashed line effect
            dash_length = 15
            gap_length = 10
            x = chart_left
            while x < chart_right:
                end_x = min(x + dash_length, chart_right)
                draw.line([(x, sl_y), (end_x, sl_y)], fill=(255, 0, 0), width=5)
                x += dash_length + gap_length
            
            # Label on left side
            label_text = f"STOP LOSS: {analysis['stop_loss']['price']}"
            try:
                bbox = draw.textbbox((chart_left + 15, sl_y - 20), label_text, font=font_medium)
            except AttributeError:
                bbox = draw.textsize(label_text, font=font_medium)
                bbox = (chart_left + 15, sl_y - 20, chart_left + 15 + bbox[0], sl_y - 20 + bbox[1])
            # Draw background with border
            draw.rectangle([(bbox[0] - 8, bbox[1] - 6), (bbox[2] + 8, bbox[3] + 6)], 
                          fill=(0, 0, 0), outline=(255, 0, 0), width=4)
            draw.text((chart_left + 15, sl_y - 20), label_text, 
                     fill=(255, 0, 0), font=font_medium)
    
    # Take Profit levels (blue lines) - make very visible
    if analysis.get('take_profits'):
        for idx, tp in enumerate(analysis['take_profits']):
            if tp.get('price'):
                tp_price = parse_price(str(tp['price']))
                if tp_price:
                    tp_y = estimate_price_y_position(tp_price, min_price, max_price, 
                                                    height, chart_top, height - chart_bottom)
                    
                    logger.info(f"Drawing TP{idx+1} at price {tp_price}, Y position: {tp_y}")
                    
                    # Draw blue horizontal line (thick)
                    draw.line([(chart_left, tp_y), (chart_right, tp_y)], 
                             fill=(0, 150, 255), width=4)
                    
                    # Dashed line effect
                    dash_length = 12
                    gap_length = 8
                    x = chart_left
                    while x < chart_right:
                        end_x = min(x + dash_length, chart_right)
                        draw.line([(x, tp_y), (end_x, tp_y)], fill=(0, 150, 255), width=4)
                        x += dash_length + gap_length
                    
                    # Label on right side
                    label_x = chart_right - 120
                    label_text = f"TP{idx + 1}: {tp['price']}"
                    try:
                        bbox = draw.textbbox((label_x + 8, tp_y - 15), label_text, font=font_medium)
                    except AttributeError:
                        bbox = draw.textsize(label_text, font=font_medium)
                        bbox = (label_x + 8, tp_y - 15, label_x + 8 + bbox[0], tp_y - 15 + bbox[1])
                    # Draw background
                    draw.rectangle([(bbox[0] - 6, bbox[1] - 4), (bbox[2] + 6, bbox[3] + 4)], 
                                  fill=(0, 0, 0), outline=(0, 150, 255), width=3)
                    draw.text((label_x + 8, tp_y - 15), label_text, 
                             fill=(0, 200, 255), font=font_medium)
    
    # Support levels (yellow dashed lines) - ALWAYS draw these
    if analysis.get('support_levels'):
        logger.info(f"📈 Drawing {len(analysis['support_levels'])} support levels")
        for idx, level in enumerate(analysis['support_levels'][:5]):  # Show up to 5
            if level.get('price'):
                support_price = parse_price(str(level['price']))
                if support_price:
                    support_y = estimate_price_y_position(support_price, min_price, max_price, 
                                                         height, chart_top, height - chart_bottom)
                    
                    logger.info(f"  → Support {idx+1}: {level['price']} ({support_price}) at Y={support_y}")
                    
                    # Draw yellow dashed line (thicker, more visible)
                    dash_length = 12
                    gap_length = 6
                    x = chart_left
                    while x < chart_right:
                        end_x = min(x + dash_length, chart_right)
                        draw.line([(x, support_y), (end_x, support_y)], 
                                 fill=(255, 255, 0), width=4)
                        x += dash_length + gap_length
                    
                    # Always add label with background
                    label_text = f"Support: {level['price']}"
                    try:
                        bbox = draw.textbbox((chart_left + 10, support_y - 18), label_text, font=font_small)
                    except AttributeError:
                        bbox = draw.textsize(label_text, font=font_small)
                        bbox = (chart_left + 10, support_y - 18, chart_left + 10 + bbox[0], support_y - 18 + bbox[1])
                    # Draw background
                    draw.rectangle([(bbox[0] - 4, bbox[1] - 3), (bbox[2] + 4, bbox[3] + 3)], 
                                  fill=(0, 0, 0), outline=(255, 255, 0), width=2)
                    draw.text((chart_left + 10, support_y - 18), label_text, 
                             fill=(255, 255, 0), font=font_small)
    
    # Resistance levels (orange dashed lines) - ALWAYS draw these
    if analysis.get('resistance_levels'):
        logger.info(f"📉 Drawing {len(analysis['resistance_levels'])} resistance levels")
        for idx, level in enumerate(analysis['resistance_levels'][:5]):  # Show up to 5
            if level.get('price'):
                resistance_price = parse_price(str(level['price']))
                if resistance_price:
                    resistance_y = estimate_price_y_position(resistance_price, min_price, max_price, 
                                                            height, chart_top, height - chart_bottom)
                    
                    logger.info(f"  → Resistance {idx+1}: {level['price']} ({resistance_price}) at Y={resistance_y}")
                    
                    # Draw orange dashed line (thicker, more visible)
                    dash_length = 12
                    gap_length = 6
                    x = chart_left
                    while x < chart_right:
                        end_x = min(x + dash_length, chart_right)
                        draw.line([(x, resistance_y), (end_x, resistance_y)], 
                                 fill=(255, 165, 0), width=4)
                        x += dash_length + gap_length
                    
                    # Always add label with background
                    label_text = f"Resistance: {level['price']}"
                    try:
                        bbox = draw.textbbox((chart_left + 10, resistance_y - 18), label_text, font=font_small)
                    except AttributeError:
                        bbox = draw.textsize(label_text, font=font_small)
                        bbox = (chart_left + 10, resistance_y - 18, chart_left + 10 + bbox[0], resistance_y - 18 + bbox[1])
                    # Draw background
                    draw.rectangle([(bbox[0] - 4, bbox[1] - 3), (bbox[2] + 4, bbox[3] + 3)], 
                                  fill=(0, 0, 0), outline=(255, 165, 0), width=2)
                    draw.text((chart_left + 10, resistance_y - 18), label_text, 
                             fill=(255, 165, 0), font=font_small)
    
    logger.info("✅ Annotation complete! Returning annotated image.")
    return annotated
