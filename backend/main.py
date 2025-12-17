from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import google.generativeai as genai
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

from utils.prompts import get_ta_prompt
from utils.image_annotator import annotate_chart

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(title="Nano Banana TA Tool", version="1.0.0")

# Thread pool executor for blocking I/O operations (Gemini API, PIL)
# This allows FastAPI to handle many concurrent requests without blocking
executor = ThreadPoolExecutor(max_workers=50, thread_name_prefix="chart_analyzer")

# Cache directory for storing analysis results
# Use persistent disk path on Render, or local cache directory
CACHE_DIR = Path(os.getenv("CACHE_DIR", "cache"))
CACHE_DIR.mkdir(exist_ok=True, parents=True)

def get_image_hash(image_bytes: bytes) -> str:
    """Generate a hash of the image bytes for caching"""
    return hashlib.sha256(image_bytes).hexdigest()

def get_cache_path(image_hash: str, timeframe: str, asset_type: str, trade_direction: Optional[str] = None) -> Path:
    """Get the cache file path for a given image hash and parameters"""
    params = f"{timeframe}_{asset_type}"
    if trade_direction:
        params += f"_{trade_direction}"
    return CACHE_DIR / f"{image_hash}_{params}.json"

def load_from_cache(image_hash: str, timeframe: str, asset_type: str, trade_direction: Optional[str] = None) -> Optional[dict]:
    """Load analysis result from cache if it exists"""
    cache_path = get_cache_path(image_hash, timeframe, asset_type, trade_direction)
    if cache_path.exists():
        try:
            with open(cache_path, 'r') as f:
                cached_data = json.load(f)
                logger.info(f"Cache hit for image hash: {image_hash[:16]}... (timeframe: {timeframe}, asset: {asset_type}, direction: {trade_direction})")
                return cached_data
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
    return None

def save_to_cache(image_hash: str, timeframe: str, asset_type: str, trade_direction: Optional[str], result: dict):
    """Save analysis result to cache"""
    try:
        cache_path = get_cache_path(image_hash, timeframe, asset_type, trade_direction)
        with open(cache_path, 'w') as f:
            json.dump(result, f, indent=2)
        logger.info(f"Cached result for image hash: {image_hash[:16]}... (timeframe: {timeframe}, asset: {asset_type}, direction: {trade_direction})")
    except Exception as e:
        logger.warning(f"Failed to save cache: {e}")

# CORS middleware for frontend
# In production, replace "*" with your actual domain
# For development, "*" allows all origins
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")
if allowed_origins == ["*"]:
    # Development mode - allow all origins
    allow_origins_list = ["*"]
else:
    # Production mode - specific origins
    allow_origins_list = [origin.strip() for origin in allowed_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# Use Nano Banana Pro (preview) - optimized for vision tasks like chart analysis
# Falls back to gemini-2.5-pro if not available
model_name = os.getenv("GEMINI_MODEL", "nano-banana-pro-preview")
model = genai.GenerativeModel(model_name)


@app.get("/")
async def root():
    return {
        "message": "Nano Banana TA Tool API",
        "status": "running",
        "model": model_name,
        "endpoints": {
            "analyze": "/analyze (POST)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model": model_name,
        "api_configured": bool(api_key)
    }


@app.options("/analyze")
async def analyze_options():
    """Handle CORS preflight requests"""
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        }
    )


@app.post("/analyze")
async def analyze_chart(
    file: UploadFile = File(...),
    timeframe: str = Form(default="auto"),
    asset_type: str = Form(default="auto"),
    trade_direction: Optional[str] = Form(default=None)
):
    """
    Analyze a trading chart screenshot using Gemini vision model.
    Returns technical analysis with entry/exit points and annotated image.
    
    This endpoint is designed to handle concurrent requests efficiently:
    - Uses thread pool executor for blocking I/O operations
    - Can handle up to 50+ concurrent requests
    - Each request runs independently without blocking others
    
    Args:
        file: Chart image file
        timeframe: Timeframe (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1w, 1M, or 'auto')
        asset_type: Asset type (btc, sol, eth, alts, memecoin, or 'auto')
        trade_direction: Trade direction ('long', 'short', or None for both)
    """
    request_id = f"{file.filename}_{id(file)}"
    logger.info(f"[{request_id}] Received upload request: {file.filename}, content_type: {file.content_type}, timeframe: {timeframe}, asset_type: {asset_type}, trade_direction: {trade_direction}")
    
    try:
        # Read image bytes first
        image_bytes = await file.read()
        
        # Generate image hash for caching
        image_hash = get_image_hash(image_bytes)
        logger.info(f"[{request_id}] Image hash: {image_hash[:16]}...")
        
        # Check cache first
        cached_result = load_from_cache(image_hash, timeframe, asset_type, trade_direction)
        if cached_result:
            logger.info(f"[{request_id}] Returning cached result")
            return JSONResponse(content=cached_result)
        logger.info(f"[{request_id}] Image size: {len(image_bytes)} bytes")
        
        if len(image_bytes) == 0:
            raise HTTPException(status_code=400, detail="Empty file uploaded")
        
        # Validate file size (max 10MB)
        max_size = 10 * 1024 * 1024  # 10MB
        if len(image_bytes) > max_size:
            raise HTTPException(status_code=400, detail=f"File too large ({len(image_bytes) / 1024 / 1024:.2f}MB). Max size: 10MB")
        
        # Process image in thread pool to avoid blocking event loop
        def process_image(image_bytes_data, req_id):
            """Process image synchronously - runs in thread pool"""
            try:
                img = Image.open(io.BytesIO(image_bytes_data))
                logger.info(f"[{req_id}] Image opened successfully: {img.size}, mode: {img.mode}, format: {img.format}")
                
                # Verify it's actually an image by checking format
                if img.format not in ['PNG', 'JPEG', 'JPG', 'GIF', 'WEBP']:
                    logger.warning(f"[{req_id}] Unusual image format: {img.format}")
                
                # Convert to RGB if necessary (required for some image formats and Gemini API)
                if img.mode == 'RGBA':
                    # Convert RGBA to RGB with white background
                    logger.info(f"[{req_id}] Converting RGBA to RGB with white background")
                    rgb_image = Image.new('RGB', img.size, (255, 255, 255))
                    if len(img.split()) == 4:
                        rgb_image.paste(img, mask=img.split()[3])
                    else:
                        rgb_image.paste(img)
                    img = rgb_image
                elif img.mode != 'RGB':
                    logger.info(f"[{req_id}] Converting image from {img.mode} to RGB")
                    img = img.convert("RGB")
                
                return img
            except Exception as e:
                logger.error(f"[{req_id}] Failed to open image: {str(e)}")
                raise ValueError(f"Invalid image file. Please upload a valid image (PNG, JPG, etc.). Error: {str(e)}")
        
        # Run image processing in thread pool
        try:
            image = await asyncio.get_event_loop().run_in_executor(
                executor, process_image, image_bytes, request_id
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"[{request_id}] Failed to process image: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Invalid image file. Error: {str(e)}")
        
        # Validate file type by content (more reliable than MIME type)
        if file.content_type:
            valid_mime_types = ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']
            if not any(mime in file.content_type.lower() for mime in ['image/png', 'image/jpeg', 'image/jpg', 'image/gif', 'image/webp']):
                logger.warning(f"[{request_id}] Unusual content type: {file.content_type}, but image opened successfully")
        
        # Get TA prompt with timeframe, asset type, and trade direction context
        prompt = get_ta_prompt(
            timeframe=timeframe if timeframe != "auto" else None,
            asset_type=asset_type if asset_type != "auto" else None,
            trade_direction=trade_direction
        )
        logger.info(f"[{request_id}] Sending request to Gemini API with timeframe: {timeframe}, asset_type: {asset_type}, trade_direction: {trade_direction}...")
        
        # Call Gemini API in thread pool to avoid blocking event loop
        def call_gemini_api(prompt_text, img, req_id):
            """Call Gemini API synchronously - runs in thread pool"""
            logger.info(f"[{req_id}] Calling Gemini API with model: {model_name}")
            logger.info(f"[{req_id}] Prompt length: {len(prompt_text)} chars")
            logger.info(f"[{req_id}] Image size: {img.size}, mode: {img.mode}")
            
            # Create a new model instance for this thread (thread-safe)
            thread_model = genai.GenerativeModel(model_name)
            
            return thread_model.generate_content(
                [
                    prompt_text,
                    img
                ],
                generation_config={
                    "temperature": 0.0,  # Zero temperature for maximum accuracy and consistency
                    "top_p": 0.95,
                    "top_k": 40,
                    "max_output_tokens": 4096,  # Increased for longer responses
                },
                safety_settings=[
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_NONE",
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_NONE",
                    },
                ]
            )
        
        # Run Gemini API call in thread pool
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                executor, call_gemini_api, prompt, image, request_id
            )
            
            logger.info(f"Response received successfully")
            
            # Handle multi-part responses properly
            analysis_text = ""
            logger.info(f"Response received: {type(response)}")
            logger.info(f"Response attributes: {[attr for attr in dir(response) if not attr.startswith('_')]}")
            
            try:
                # Try the simple text accessor first (works for single-part responses)
                analysis_text = response.text
                logger.info(f"Got text from response.text: {len(analysis_text)} chars")
            except ValueError as e:
                # If that fails, extract text from parts (multi-part response)
                logger.info(f"Multi-part response detected, extracting from parts: {str(e)}")
                if response.candidates and len(response.candidates) > 0:
                    logger.info(f"Found {len(response.candidates)} candidates")
                    if hasattr(response.candidates[0], 'content') and hasattr(response.candidates[0].content, 'parts'):
                        parts = response.candidates[0].content.parts
                        logger.info(f"Found {len(parts)} parts in candidate content")
                        text_parts = []
                        for i, part in enumerate(parts):
                            logger.info(f"Part {i}: type={type(part)}, has_text={hasattr(part, 'text')}")
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
                                logger.info(f"Part {i} text length: {len(part.text)}")
                        analysis_text = "\n".join(text_parts)
                    else:
                        # Try direct parts access
                        parts = response.parts if hasattr(response, 'parts') else []
                        logger.info(f"Trying direct parts access: {len(parts)} parts")
                        text_parts = []
                        for part in parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
                        analysis_text = "\n".join(text_parts)
                elif hasattr(response, 'parts'):
                    text_parts = []
                    for part in response.parts:
                        if hasattr(part, 'text') and part.text:
                            text_parts.append(part.text)
                    analysis_text = "\n".join(text_parts)
                else:
                    logger.error("Could not extract text from response structure")
                    logger.error(f"Response type: {type(response)}, attributes: {dir(response)}")
                    # Try to get any text from response
                    if hasattr(response, '__str__'):
                        logger.error(f"Response string representation: {str(response)[:500]}")
                    raise HTTPException(status_code=500, detail="Could not extract text from AI response. Response structure not recognized.")
            except Exception as e:
                logger.error(f"Unexpected error extracting text: {str(e)}\n{traceback.format_exc()}")
                raise HTTPException(status_code=500, detail=f"Error extracting text from AI response: {str(e)}")
            
            if not analysis_text or len(analysis_text.strip()) == 0:
                logger.error("Empty response from Gemini API")
                logger.error(f"Response object: {response}")
                logger.error(f"Response candidates: {getattr(response, 'candidates', 'N/A')}")
                logger.error(f"Response finish_reason: {getattr(response, 'finish_reason', 'N/A')}")
                logger.error(f"Response prompt_feedback: {getattr(response, 'prompt_feedback', 'N/A')}")
                
                # Check if there's a safety block
                if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                    if hasattr(response.prompt_feedback, 'block_reason'):
                        block_reason = response.prompt_feedback.block_reason
                        logger.error(f"Response blocked: {block_reason}")
                        raise HTTPException(
                            status_code=500, 
                            detail=f"AI response was blocked. Reason: {block_reason}. Try a different chart image."
                        )
                
                raise HTTPException(
                    status_code=500, 
                    detail="Empty response from AI model. The model may have been blocked or encountered an error. Try uploading a different chart image."
                )
            
            logger.info(f"Received analysis (length: {len(analysis_text)} chars)")
            
            # Try to extract JSON from response
            json_data = extract_json_from_response(analysis_text)
            
            # Create annotated version of the chart (run in thread pool)
            def create_annotated_chart(img, analysis_data, req_id):
                """Create annotated chart synchronously - runs in thread pool"""
                try:
                    logger.info(f"[{req_id}] Creating annotated chart image...")
                    logger.info(f"[{req_id}] JSON data type: {type(analysis_data)}")
                    logger.info(f"[{req_id}] JSON data keys: {list(analysis_data.keys()) if isinstance(analysis_data, dict) else 'Not a dict'}")
                    
                    # Always try to annotate - even if parsing failed, we can still try
                    if isinstance(analysis_data, dict):
                        # Check if we have price data to annotate
                        has_price_data = (
                            analysis_data.get('entry') or 
                            analysis_data.get('stop_loss') or 
                            analysis_data.get('take_profits') or
                            analysis_data.get('support_levels') or
                            analysis_data.get('resistance_levels') or
                            analysis_data.get('current_price')
                        )
                        
                        if has_price_data or analysis_data.get('parsed') != False:
                            logger.info(f"[{req_id}] Attempting to create annotations...")
                            annotated = annotate_chart(img.copy(), analysis_data)
                            
                            # Verify annotation worked
                            if annotated and annotated.size == img.size:
                                # Convert annotated image to base64
                                buffer = io.BytesIO()
                                annotated.save(buffer, format="PNG")
                                annotated_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
                                logger.info(f"[{req_id}] ✅ Annotated chart created successfully! Base64 size: {len(annotated_base64)} bytes")
                                return annotated_base64
                            else:
                                logger.warning(f"[{req_id}] ⚠️ Annotation returned invalid image. Original size: {img.size}, Annotated size: {annotated.size if annotated else 'None'}")
                                return None
                        else:
                            logger.warning(f"[{req_id}] ⚠️ No price data found in analysis")
                            return None
                    else:
                        logger.warning(f"[{req_id}] ⚠️ JSON data is not a dict, cannot annotate")
                        return None
                except Exception as annotate_error:
                    logger.error(f"[{req_id}] ❌ Error during annotation: {str(annotate_error)}\n{traceback.format_exc()}")
                    return None
            
            annotated_base64 = None
            try:
                annotated_base64 = await asyncio.get_event_loop().run_in_executor(
                    executor, create_annotated_chart, image, json_data, request_id
                )
            except Exception as e:
                logger.error(f"[{request_id}] Failed to create annotated chart: {str(e)}\n{traceback.format_exc()}")
                annotated_base64 = None
            
            # Convert original image to base64 for response (run in thread pool)
            def convert_image_to_base64(img, req_id):
                """Convert image to base64 synchronously - runs in thread pool"""
                buffer = io.BytesIO()
                img.save(buffer, format="PNG")
                result = base64.b64encode(buffer.getvalue()).decode("utf-8")
                logger.info(f"[{req_id}] Image converted to base64: {len(result)} chars")
                return result
            
            img_base64 = await asyncio.get_event_loop().run_in_executor(
                executor, convert_image_to_base64, image, request_id
            )
            
            logger.info(f"[{request_id}] Analysis complete, returning results")
            
            response_data = {
                "success": True,
                "analysis": json_data,
                "raw_response": analysis_text,
                "original_image": f"data:image/png;base64,{img_base64}",
                "annotated_image": f"data:image/png;base64,{annotated_base64}" if annotated_base64 else None,
                "metadata": {
                    "timeframe": timeframe,
                    "asset_type": asset_type,
                    "trade_direction": trade_direction
                }
            }
            
            # Save to cache for future requests
            save_to_cache(image_hash, timeframe, asset_type, trade_direction, response_data)
            
            logger.info("Analysis complete, returning results")
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
            logger.error(f"Gemini API error: {str(e)}\n{traceback.format_exc()}")
            raise HTTPException(
                status_code=500,
                detail=f"AI analysis error: {str(e)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}\n{traceback.format_exc()}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image: {str(e)}"
        )


def extract_json_from_response(text: str) -> dict:
    """
    Extract JSON from Gemini response text.
    Handles cases where JSON is wrapped in markdown code blocks.
    """
    import re
    
    # Try to find JSON in code blocks
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try to find JSON object directly
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        try:
            return json.loads(json_match.group(0))
        except json.JSONDecodeError:
            pass
    
    # Fallback: return structured text response
    return {
        "raw_text": text,
        "parsed": False
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

