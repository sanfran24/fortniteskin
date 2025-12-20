"""
Fortnite Skin Generator prompts for Nano Banana (Gemini Image Generation).
"""
from typing import Optional

def get_skin_styles() -> list:
    """Returns all available Fortnite skin styles"""
    return [
        {
            "id": "legendary",
            "name": "Legendary",
            "description": "Ultra-detailed legendary skin with glowing effects, elaborate armor, and premium design",
            "color": "#f5a623",
            "icon": "⭐"
        },
        {
            "id": "epic",
            "name": "Epic",
            "description": "High-quality skin with unique features and standout design",
            "color": "#9b59b6",
            "icon": "💜"
        },
        {
            "id": "rare",
            "name": "Rare",
            "description": "Cool skin with distinctive style and good detail",
            "color": "#3498db",
            "icon": "💙"
        },
        {
            "id": "uncommon",
            "name": "Uncommon",
            "description": "Clean, simple skin with nice colors",
            "color": "#2ecc71",
            "icon": "💚"
        },
        {
            "id": "collab",
            "name": "Collaboration",
            "description": "Crossover style inspired by iconic franchises",
            "color": "#e74c3c",
            "icon": "🤝"
        },
        {
            "id": "meme",
            "name": "Meme Lord",
            "description": "Hilarious, viral-worthy skin design",
            "color": "#f39c12",
            "icon": "😂"
        },
        {
            "id": "anime",
            "name": "Anime",
            "description": "Anime/manga inspired character design",
            "color": "#ff6b9d",
            "icon": "🌸"
        },
        {
            "id": "cyberpunk",
            "name": "Cyberpunk",
            "description": "Futuristic neon-lit cyber warrior",
            "color": "#00ffff",
            "icon": "🤖"
        },
        {
            "id": "fantasy",
            "name": "Fantasy",
            "description": "Magical fantasy warrior with mystical elements",
            "color": "#8e44ad",
            "icon": "🧙"
        },
        {
            "id": "horror",
            "name": "Horror",
            "description": "Spooky, creepy skin perfect for Fortnitemares",
            "color": "#1a1a2e",
            "icon": "👻"
        },
        {
            "id": "peely",
            "name": "Peely Style",
            "description": "Banana-inspired goofy fun character",
            "color": "#ffeb3b",
            "icon": "🍌"
        },
        {
            "id": "slurp",
            "name": "Slurp Series",
            "description": "Translucent slurp juice character",
            "color": "#00bcd4",
            "icon": "💧"
        }
    ]


def get_fortnite_skin_prompt(style: str = "legendary", custom_prompt: str = "") -> str:
    """
    Returns the prompt for generating a Fortnite skin based on style.
    
    Args:
        style: The skin style/rarity (legendary, epic, rare, uncommon, collab, meme, anime, cyberpunk)
        custom_prompt: Optional custom instructions to add
    """
    
    base_prompt = """You are the lead character artist at Epic Games, responsible for creating iconic Fortnite skins.
    
Your task is to transform the provided image into an authentic Fortnite character skin design.

**FORTNITE ART STYLE REQUIREMENTS:**
- Slightly stylized proportions (larger heads, expressive features)
- Clean, readable silhouettes that work in-game
- Vibrant, saturated colors
- Smooth, polished 3D render look
- Bold outlines and shapes
- Exaggerated but appealing features
- Battle Royale ready design

**TECHNICAL REQUIREMENTS:**
- Full body character design (head to toe)
- T-pose or action pose
- Clean background (solid color or gradient)
- High detail on face and accessories
- Proper Fortnite character proportions
- Ready for the Item Shop showcase

"""

    style_prompts = {
        "legendary": """**LEGENDARY RARITY SKIN**

Create an ULTRA-PREMIUM legendary tier skin with:
- Elaborate, detailed costume with multiple layers
- Glowing/reactive elements that pulse with energy
- Unique particle effects (flames, electricity, magic)
- Premium materials (chrome, gold, crystals)
- Imposing, powerful presence
- Multiple selectable styles
- Built-in emote worthy design
- Back bling that complements the main skin

Think: Omega, Ragnarok, Ice King, The Reaper level quality.
This skin should be the crown jewel of any locker!
""",

        "epic": """**EPIC RARITY SKIN**

Create a HIGH-QUALITY epic tier skin with:
- Distinctive, memorable design
- Unique theme and color palette
- Quality materials and textures
- Some special effects or glowing elements
- Strong silhouette recognition
- Professional, polished look
- Possible alternate style

Think: Dark Voyager, Drift, Lynx quality level.
A skin that stands out in the lobby!
""",

        "rare": """**RARE RARITY SKIN**

Create a SOLID rare tier skin with:
- Clean, appealing design
- Good use of the blue rarity aesthetic
- Interesting costume without being over-designed
- Nice color combinations
- Clear theme or concept
- Good value proposition

Think: Brite Bomber, Raptor, Cuddle Team Leader tier.
A reliable favorite that looks great!
""",

        "uncommon": """**UNCOMMON RARITY SKIN**

Create a CLEAN uncommon tier skin with:
- Simple but effective design
- Nice color scheme
- Clean lines and shapes
- Accessible, friendly appearance
- Good starter skin vibes
- Understated cool factor

Think: Commando, Survival Specialist tier.
Simple, clean, and still cool!
""",

        "collab": """**COLLABORATION SKIN**

Create an ICON SERIES / GAMING LEGENDS style skin:
- Authentic to the source material
- Fortnite-ified but recognizable
- Premium crossover quality
- Unique loading screen worthy
- Multiple styles from the source
- Matching accessories

Think: Kratos, Master Chief, Naruto, Travis Scott tier.
A crossover event everyone remembers!
""",

        "meme": """**MEME LORD SKIN**

Create a HILARIOUS viral-worthy skin:
- Immediately funny and recognizable
- Perfect for content creators
- Meme template potential
- Absurd but lovable
- Trolling potential in-game
- Instant classic vibes

Think: Peely, Fishstick, Guff, Lil Whip tier.
A skin that makes everyone laugh!
""",

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
A skin straight from your favorite anime!
""",

        "cyberpunk": """**CYBERPUNK SKIN**

Create a NEON-SOAKED cyber warrior:
- Glowing neon accents (pink, cyan, purple)
- Futuristic tech armor/clothing
- Holographic elements
- Cyber implants and augments
- Dark base with bright neon highlights
- LED patterns and circuits
- Visor or mask with digital display

Think: Neo-future, blade runner aesthetic.
Ready to hack the simulation!
""",

        "fantasy": """**FANTASY SKIN**

Create a MAGICAL fantasy character:
- Mystical robes, armor, or clothing
- Magical effects (runes, auras, enchantments)
- Fantasy race features (elf, orc, fairy, etc.)
- Enchanted weapons or accessories
- Medieval-fantasy meets Fortnite
- Magical creature companion back bling

Think: Wizards, elves, knights, druids.
A skin from another realm!
""",

        "horror": """**HORROR/FORTNITEMARES SKIN**

Create a SPOOKY terrifying skin:
- Creepy, unsettling design
- Horror movie inspired
- Dark color palette with accent colors
- Scary masks or faces
- Undead or monster features
- Perfect for Fortnitemares
- Nightmare fuel but still cool

Think: Skull Trooper, Chaos Agent, Cube Queen tier.
A skin that haunts your dreams!
""",

        "peely": """**PEELY STYLE SKIN**

Create a BANANA-INSPIRED goofy character:
- Yellow banana aesthetic
- Silly, lovable expression
- Various banana stages or styles
- Fruit-based humor
- Wholesome and funny
- Perfect for casual vibes

Think: All the Peely variants!
Embrace the BANANA life!
""",

        "slurp": """**SLURP SERIES SKIN**

Create a SLURP JUICE character:
- Translucent blue slurp body
- Liquid/gel texture
- Internal glow effect
- Slurp barrel elements
- Healing vibes
- Sloshy, fluid design

Think: Slurp Leviathan, Rippley, Slurp Jonesy.
Hydration is key!
"""
    }

    # Get style-specific prompt
    style_prompt = style_prompts.get(style.lower(), style_prompts["legendary"])
    
    # Build full prompt
    full_prompt = base_prompt + style_prompt
    
    # Add custom prompt if provided
    if custom_prompt:
        full_prompt += f"""

**CUSTOM REQUIREMENTS:**
{custom_prompt}
"""

    full_prompt += """

**OUTPUT:**
Generate a stunning Fortnite character skin based on the input image.
Transform the subject into an authentic Fortnite skin while maintaining 
recognizable elements from the original.

Include a description with:
1. **Skin Name** - A catchy, Fortnite-style name
2. **Rarity** - Confirm the rarity tier
3. **Description** - Item shop description text
4. **Set Name** - What set it belongs to
5. **Reactive Features** - Any reactive/dynamic elements
6. **Styles** - Available alternate styles
7. **Back Bling** - Matching back bling design
8. **Harvesting Tool** - Matching pickaxe design
9. **Glider** - Matching glider concept
10. **Built-in Emote** - Special emote idea

Make it feel like official Fortnite content!
"""

    return full_prompt
