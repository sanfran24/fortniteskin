"""
Fortnite Skin Generator prompts for Nano Banana (Gemini Image Generation).
"""
from typing import Optional

def get_skin_styles() -> list:
    """Returns all available Fortnite skin styles - 5 distinct options"""
    return [
        {
            "id": "legendary",
            "name": "Legendary",
            "description": "Premium glowing armor with gold/chrome effects",
            "color": "#f5a623",
            "icon": "⭐"
        },
        {
            "id": "anime",
            "name": "Anime",
            "description": "Cel-shaded anime/manga character style",
            "color": "#ff6b9d",
            "icon": "🌸"
        },
        {
            "id": "meme",
            "name": "Meme Lord",
            "description": "Funny, goofy, viral-worthy character",
            "color": "#f39c12",
            "icon": "😂"
        },
        {
            "id": "cyberpunk",
            "name": "Cyberpunk",
            "description": "Neon-lit futuristic cyber warrior",
            "color": "#00ffff",
            "icon": "🤖"
        },
        {
            "id": "horror",
            "name": "Horror",
            "description": "Creepy, spooky Fortnitemares style",
            "color": "#8b0000",
            "icon": "👻"
        }
    ]


def get_fortnite_skin_prompt(style: str = "legendary", custom_prompt: str = "") -> str:
    """
    Returns the prompt for generating a Fortnite skin based on style.
    Each style has a VERY DISTINCT visual direction.
    """
    
    style_prompts = {
        "legendary": """CREATE A LEGENDARY FORTNITE SKIN:

VISUAL STYLE - LEGENDARY TIER:
- GOLD and CHROME metallic armor pieces
- GLOWING energy effects (blue/orange/purple glow)
- Elaborate detailed costume with multiple layers
- Premium materials: crystals, gems, glowing runes
- Particle effects around the character (sparks, energy wisps)
- Imposing, powerful superhero-like presence
- Think: Iron Man meets fantasy warrior

COLOR PALETTE: Gold, silver, chrome, with glowing blue/purple/orange accents

REFERENCE SKINS: Omega, Ragnarok, Ice King, Midas
This should look like a 2000 V-Bucks skin!""",

        "anime": """**ANIME SERIES SKIN**

Create an ANIME-STYLED character:
- Cel-shaded manga aesthetic
- Dramatic poses and expressions
- Anime hair and features
- Vibrant anime color palette
- Dynamic action lines
- Possible transformation style
- Matching anime-style accessories

Think: Naruto series, Dragon Ball, My Hero Academia tier.
A skin straight from your favorite anime!""",

        "meme": """CREATE A MEME LORD FORTNITE SKIN:

VISUAL STYLE - FUNNY/GOOFY:
- RIDICULOUS and HILARIOUS character design
- Exaggerated silly facial expression (derpy, goofy, funny)
- Absurd costume or body shape
- Could be food-themed, animal-themed, or just weird
- Maximum meme potential
- The kind of skin streamers would use to troll
- Instant classic funny vibes

COLOR PALETTE: Bright, silly colors - yellows, pinks, whatever's funny

REFERENCE SKINS: Peely (banana), Fishstick, Guff, Lil Whip
Make people LAUGH when they see this skin!""",

        "cyberpunk": """CREATE A CYBERPUNK FORTNITE SKIN:

VISUAL STYLE - NEON CYBER FUTURE:
- GLOWING NEON lights (hot pink, cyan, electric blue)
- Dark black base with bright neon accents
- Futuristic tech armor/clothing
- LED strips and circuit patterns on outfit
- Cyber implants, robotic parts, or augmentations  
- Holographic elements floating nearby
- Visor or mask with digital display
- Blade Runner / Tron aesthetic

COLOR PALETTE: Black base + HOT PINK + CYAN + ELECTRIC BLUE neon

REFERENCE: Cyberpunk 2077, Tron, neon dystopia
Make it GLOW with neon energy!""",

        "horror": """CREATE A HORROR FORTNITE SKIN:

VISUAL STYLE - CREEPY/SCARY:
- TERRIFYING and UNSETTLING design
- Horror movie monster vibes
- Creepy mask or disturbing face
- Dark, shadowy color palette
- Could be: zombie, demon, ghost, slasher villain
- Glowing evil eyes (red/green)
- Tattered, damaged, or corrupted clothing
- Nightmare fuel but still cool

COLOR PALETTE: Dark blacks, grays, with red/green accents

REFERENCE SKINS: Skull Trooper, Chaos Agent, Cube Queen
Perfect for Fortnitemares - genuinely CREEPY!"""
    }

    # Get style-specific prompt (default to legendary)
    style_key = style.lower()
    if style_key not in style_prompts:
        style_key = "legendary"
    
    style_prompt = style_prompts[style_key]
    
    # Build the full prompt with clear structure
    full_prompt = f"""You are creating a Fortnite character skin. Generate a FULL BODY character image.

{style_prompt}

CRITICAL REQUIREMENTS:
1. FULL BODY - Show complete character from HEAD TO TOE (not cropped)
2. Include: head, torso, arms, hands, legs, feet with shoes/boots
3. **BACKGROUND**: Dark blue to purple gradient background (like Fortnite Item Shop)
4. **PLATFORM**: Character MUST be standing on a glowing circular platform/pedestal at their feet (the Item Shop display platform)
5. 3D rendered look matching official Fortnite promotional art
6. Fortnite proportions (slightly larger head, stylized body)
7. The circular platform should have a subtle glow effect around the edges

Transform the input image into this style while keeping recognizable features from the original.

IMPORTANT: Every generated skin MUST have the gradient background AND the circular standing platform!
"""

    # Add custom prompt if provided
    if custom_prompt:
        full_prompt += f"""
ADDITIONAL INSTRUCTIONS FROM USER:
{custom_prompt}
"""

    full_prompt += """
OUTPUT: Generate the Fortnite skin image with:
- GRADIENT BACKGROUND (dark blue to purple)
- CIRCULAR GLOWING PLATFORM at the character's feet
- Full body character standing on the platform
- Item Shop display style presentation

Also include:
- Skin Name (catchy Fortnite-style name)
- Rarity tier
- Short Item Shop description
"""

    return full_prompt
