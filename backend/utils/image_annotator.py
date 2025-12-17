"""
Image annotation utilities for drawing TA elements on charts.
"""
from PIL import Image, ImageDraw, ImageFont
import math
from typing import Dict, List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


def estimate_price_y_position(price: float, min_price: float, max_price: float, 
                              image_height: int, chart_top: int = 50, 
                              chart_bottom: int = 50) -> int:
    """
    Estimate Y pixel position for a price level on the chart.
    """
    chart_height = image_height - chart_top - chart_bottom
    price_range = max_price - min_price
    
    if price_range == 0:
        return image_height // 2
    
    # Normalize price to 0-1 range (inverted because Y=0 is top)
    normalized = (max_price - price) / price_range
    
    # Convert to pixel position
    y_pos = chart_top + int(normalized * chart_height)
    
    return max(chart_top, min(y_pos, image_height - chart_bottom))


def parse_price(price_str: str) -> Optional[float]:
    """Parse price string to float, handling common formats including K notation."""
    if not price_str:
        return None
    
    try:
        # Remove common characters and convert to string
        cleaned = str(price_str).replace('$', '').replace(',', '').replace(' ', '').strip().upper()
        
        # Handle K notation (e.g., 300K = 300000)
        multiplier = 1
        if cleaned.endswith('K'):
            multiplier = 1000
            cleaned = cleaned[:-1]
        elif cleaned.endswith('M'):
            multiplier = 1000000
            cleaned = cleaned[:-1]
        
        return float(cleaned) * multiplier
    except (ValueError, AttributeError):
        return None


def get_price_range(analysis: Dict) -> Tuple[float, float]:
    """Estimate price range from analysis data."""
    prices = []
    
    # Collect all price values
    if analysis.get('current_price'):
        prices.append(parse_price(str(analysis['current_price'])))
    
    if analysis.get('entry') and analysis['entry'].get('price'):
        prices.append(parse_price(str(analysis['entry']['price'])))
    
    if analysis.get('stop_loss') and analysis['stop_loss'].get('price'):
        prices.append(parse_price(str(analysis['stop_loss']['price'])))
    
    if analysis.get('take_profits'):
        for tp in analysis['take_profits']:
            if tp.get('price'):
                prices.append(parse_price(str(tp['price'])))
    
    if analysis.get('support_levels'):
        for level in analysis['support_levels']:
            if level.get('price'):
                prices.append(parse_price(str(level['price'])))
    
    if analysis.get('resistance_levels'):
        for level in analysis['resistance_levels']:
            if level.get('price'):
                prices.append(parse_price(str(level['price'])))
    
    # Filter out None values
    prices = [p for p in prices if p is not None]
    
    if len(prices) < 2:
        # Default range if we can't determine
        if prices:
            base = prices[0]
            return base * 0.9, base * 1.1
        return 0, 100
    
    min_price = min(prices)
    max_price = max(prices)
    
    # Add padding
    price_range = max_price - min_price
    padding = max(price_range * 0.1, (max_price - min_price) * 0.05)  # At least 5% padding
    
    return min_price - padding, max_price + padding


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
        logger.info(f"Price range determined: {min_price} - {max_price}")
    except Exception as e:
        logger.warning(f"Could not determine price range: {e}, using defaults")
        min_price, max_price = 0, 100
    
    # Estimate chart area (use most of the image)
    chart_left = int(width * 0.05)  # 5% margin
    chart_right = int(width * 0.98)  # 2% margin
    chart_top = int(height * 0.05)  # 5% margin
    chart_bottom = int(height * 0.95)  # 5% margin
    
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
