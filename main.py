from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
from google import genai as genai_new
from PIL import Image
import io
import os
from dotenv import load_dotenv
import json
import base64
from typing import Optional
import logging
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
import hashlib
from pathlib import Path

from utils.prompts import get_fortnite_skin_prompt, get_skin_styles

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Fortnite Skin Generator - Nano Banana", version="1.0.0")

# Thread pool executor for blocking I/O operations
executor = ThreadPoolExecutor(max_workers=50, thread_name_prefix="skin_generator")

# Cache directory for storing generated skins
CACHE_DIR = Path(os.getenv("CACHE_DIR", "cache"))
CACHE_DIR.mkdir(exist_ok=True, parents=True)

def get_image_hash(image_bytes: bytes, style: str) -> str:
    """Generate a hash of the image bytes and style for caching"""
    combined = image_bytes + style.encode()
    return hashlib.sha256(combined).hexdigest()

def get_cache_path(image_hash: str) -> Path:
    """Get the cache file path for a given image hash"""
    return CACHE_DIR / f"{image_hash}.json"

def load_from_cache(image_hash: str) -> Optional[dict]:
    """Load generated skin from cache if it exists"""
    cache_path = get_cache_path(image_hash)
    if cache_path.exists():
        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
                logger.info(f"Cache hit for image hash: {image_hash[:16]}...")
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
    return None

def save_to_cache(image_hash: str, result: dict):
    """Save generated skin to cache"""
    try:
        cache_path = get_cache_path(image_hash)
        with open(cache_path, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Cached result for image hash: {image_hash[:16]}...")
    except Exception as e:
        logger.warning(f"Failed to save cache: {e}")

# CORS middleware
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if allowed_origins == ["*"]:
    allow_origins_list = ["*"]
else:
    allow_origins_list = [origin.strip() for origin in allowed_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini / Nano Banana
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Configure both old and new API clients
genai.configure(api_key=api_key)

# Nano Banana models for image generation
# gemini-2.0-flash-exp supports image generation
IMAGE_MODEL = os.getenv("IMAGE_MODEL", "gemini-2.0-flash-exp")
VISION_MODEL = os.getenv("VISION_MODEL", "gemini-2.0-flash-exp")

# Initialize the new Genai client for image generation
try:
    client = genai_new.Client(api_key=api_key)
    logger.info(f"Initialized Nano Banana client with models: IMAGE={IMAGE_MODEL}, VISION={VISION_MODEL}")
except Exception as e:
    logger.warning(f"Could not initialize new genai client: {e}. Falling back to standard API.")
    client = None


@app.get("/")
async def root():
    return {
        "message": "🎮 Fortnite Skin Generator - Powered by Nano Banana",
        "status": "running",
        "models": {
            "image_generation": IMAGE_MODEL,
            "vision": VISION_MODEL
        },
        "endpoints": {
            "generate": "/generate (POST)",
            "styles": "/styles (GET)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "image_model": IMAGE_MODEL,
        "vision_model": VISION_MODEL,
        "api_configured": bool(api_key)
    }


@app.get("/styles")
async def get_styles():
    """Get available Fortnite skin styles"""
    return {
        "styles": get_skin_styles()
    }


@app.options("/generate")
async def generate_options():
    """Handle CORS preflight requests"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )


@app.post("/generate")
async def generate_fortnite_skin(
    file: UploadFile = File(...),
    style: str = Form(default="legendary"),
    custom_prompt: str = Form(default="")
):
    """
    Transform an uploaded image into a Fortnite-style character skin.
    
    Uses Google's Nano Banana (Gemini Image Generation) to create 
    stylized Fortnite character skins from any input image.
    
    Args:
        file: Source image file (person, character, object, etc.)
        style: Skin style (legendary, epic, rare, uncommon, collab, meme, anime, cyberpunk)
        custom_prompt: Optional custom instructions for the transformation
    """
    request_id = f"{file.filename}_{id(file)}"
    logger.info(f"[{request_id}] Received generation request: {file.filename}, style: {style}")
    
    try:
        # Read image bytes
        image_bytes = await file.read()
        
        # Generate cache key
        cache_key = get_image_hash(image_bytes, style + custom_prompt)
        
        # Check cache
        cached_result = load_from_cache(cache_key)
        if cached_result:
            logger.info(f"[{request_id}] Returning cached result")
            return JSONResponse(content=cached_result)
        
        logger.info(f"[{request_id}] Image size: {len(image_bytes)} bytes")
        
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024
        if len(image_bytes) > max_size:
            raise HTTPException(status_code=400, detail=f"File too large. Max size: 10MB")
        
        # Process image
        def process_image(image_bytes_data, req_id):
            """Process image synchronously"""
            try:
                img = Image.open(io.BytesIO(image_bytes_data))
                logger.info(f"[{req_id}] Image opened: {img.size}, mode: {img.mode}")
                
                # Convert to RGB if necessary
                if img.mode == 'RGBA':
                    rgb_image = Image.new('RGB', img.size, (255, 255, 255))
                    if len(img.split()) == 4:
                        rgb_image.paste(img, mask=img.split()[3])
                    else:
                        rgb_image.paste(img)
                    img = rgb_image
                elif img.mode != 'RGB':
                    img = img.convert("RGB")
                
                return img
            except Exception as e:
                logger.error(f"[{req_id}] Failed to open image: {str(e)}")
                raise ValueError(f"Invalid image file: {str(e)}")
        
        # Run image processing
        try:
            image = await asyncio.get_event_loop().run_in_executor(
                executor, process_image, image_bytes, request_id
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Get the transformation prompt
        prompt = get_fortnite_skin_prompt(style, custom_prompt)
        logger.info(f"[{request_id}] Using style: {style}")
        
        # Generate Fortnite skin using Nano Banana
        def generate_skin(prompt_text, img, req_id):
            """Generate Fortnite skin using Gemini's image capabilities"""
            logger.info(f"[{req_id}] Generating Fortnite skin with Nano Banana...")
            
            generated_images = []
            description = None
            
            try:
                if client:
                    # Use new Genai client for image generation (Nano Banana)
                    logger.info(f"[{req_id}] Using new Genai client with model: {IMAGE_MODEL}")
                    
                    # First, analyze the input image to understand what to transform
                    analysis_prompt = f"""Analyze this image and describe the main subject in detail.
                    I want to transform this into a Fortnite character skin.
                    Describe: the pose, colors, clothing/features, and any distinctive elements.
                    Be specific so we can recreate this as a Fortnite character."""
                    
                    # Convert PIL image to bytes for the API
                    img_buffer = io.BytesIO()
                    img.save(img_buffer, format="PNG")
                    img_bytes = img_buffer.getvalue()
                    
                    # Analyze the image first
                    vision_model = genai.GenerativeModel(VISION_MODEL)
                    analysis_response = vision_model.generate_content([
                        analysis_prompt,
                        img
                    ])
                    
                    image_description = analysis_response.text if hasattr(analysis_response, 'text') else "a character"
                    logger.info(f"[{req_id}] Image analysis: {image_description[:200]}...")
                    
                    # Now generate the Fortnite skin
                    full_prompt = f"""{prompt_text}

Based on this source image description: {image_description}

Generate a Fortnite character skin that captures the essence of this subject while 
applying the Fortnite art style. The skin should be ready for the Item Shop!"""
                    
                    # Try to generate image using the Gemini 2.0 model
                    try:
                        response = client.models.generate_content(
                            model=IMAGE_MODEL,
                            contents=full_prompt,
                            config=genai_new.types.GenerateContentConfig(
                                response_modalities=['TEXT', 'IMAGE']
                            )
                        )
                        
                        # Extract generated images and text from response
                        for part in response.candidates[0].content.parts:
                            if hasattr(part, 'inline_data') and part.inline_data:
                                # This is an image
                                img_data = part.inline_data.data
                                generated_images.append(base64.b64encode(img_data).decode('utf-8'))
                                logger.info(f"[{req_id}] Generated image extracted!")
                            elif hasattr(part, 'text') and part.text:
                                description = part.text
                                
                    except Exception as gen_error:
                        logger.warning(f"[{req_id}] Image generation failed: {gen_error}. Falling back to description-only mode.")
                        
                        # Fallback: Generate detailed description of the Fortnite skin
                        fallback_prompt = f"""{prompt_text}

Based on this source image: {image_description}

Since you cannot generate images directly, provide an extremely detailed description of what this 
Fortnite skin would look like. Include:
1. Skin name and rarity
2. Full character design (head to toe)
3. Color palette with exact colors
4. Special effects and reactive features
5. Back bling suggestion
6. Pickaxe design
7. Glider design
8. Built-in emote idea

Make it sound like official Fortnite patch notes!"""
                        
                        fallback_response = vision_model.generate_content([fallback_prompt, img])
                        description = fallback_response.text if hasattr(fallback_response, 'text') else "Fortnite skin generated"
                
                else:
                    # Fallback to old API
                    logger.info(f"[{req_id}] Using legacy Genai API")
                    model = genai.GenerativeModel(VISION_MODEL)
                    response = model.generate_content([prompt_text, img])
                    description = response.text if hasattr(response, 'text') else "Fortnite skin concept"
                    
            except Exception as e:
                logger.error(f"[{req_id}] Generation error: {str(e)}\n{traceback.format_exc()}")
                raise
            
            return {
                "generated_images": generated_images,
                "description": description
            }
        
        # Run generation
        try:
            result = await asyncio.get_event_loop().run_in_executor(
                executor, generate_skin, prompt, image, request_id
            )
        except Exception as e:
            logger.error(f"[{request_id}] Generation failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Skin generation failed: {str(e)}")
        
        # Convert original image to base64
        def convert_to_base64(img, req_id):
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            return base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        original_base64 = await asyncio.get_event_loop().run_in_executor(
            executor, convert_to_base64, image, request_id
        )
        
        # Build response
        response_data = {
            "success": True,
            "style": style,
            "original_image": f"data:image/png;base64,{original_base64}",
            "generated_images": [f"data:image/png;base64,{img}" for img in result.get("generated_images", [])],
            "description": result.get("description", ""),
            "skin_details": extract_skin_details(result.get("description", ""))
        }
        
        # Cache the result
        save_to_cache(cache_key, response_data)
        
        logger.info(f"[{request_id}] Generation complete!")
        return JSONResponse(
            content=response_data,
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*",
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


def extract_skin_details(description: str) -> dict:
    """Extract structured skin details from the description"""
    import re
    
    details = {
        "name": None,
        "rarity": None,
        "set": None,
        "features": [],
        "colors": [],
        "back_bling": None,
        "pickaxe": None,
        "emote": None
    }
    
    if not description:
        return details
    
    # Try to extract skin name
    name_patterns = [
        r'(?:skin name|called|named|introducing)[:\s]+["\']?([^"\'\n,]+)["\']?',
        r'["\']([^"\']+)["\'](?:\s+skin|\s+outfit)',
    ]
    for pattern in name_patterns:
        match = re.search(pattern, description, re.IGNORECASE)
        if match:
            details["name"] = match.group(1).strip()
            break
    
    # Try to extract rarity
    rarities = ["legendary", "epic", "rare", "uncommon", "common", "mythic", "icon series", "marvel series", "dc series", "gaming legends", "star wars series"]
    for rarity in rarities:
        if rarity.lower() in description.lower():
            details["rarity"] = rarity.title()
            break
    
    return details


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
