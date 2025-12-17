"""
Simple test script to verify API setup.
Run this after setting up your .env file to test the Gemini connection.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

def test_gemini_connection():
    """Test if Gemini API is configured correctly."""
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not found in .env file")
        print("   Make sure you have created backend/.env with your API key")
        return False
    
    if api_key == "your_api_key_here":
        print("ERROR: Please replace 'your_api_key_here' with your actual API key")
        return False
    
    try:
        print("Testing Gemini API connection...")
        genai.configure(api_key=api_key)
        
        model_name = os.getenv("GEMINI_MODEL", "nano-banana-pro-preview")
        print(f"Using model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        
        # Simple text test
        response = model.generate_content("Say 'Hello' if you can read this.")
        print(f"API Connection Successful!")
        print(f"   Response: {response.text}")
        return True
        
    except Exception as e:
        print(f"ERROR: Failed to connect to Gemini API")
        print(f"   Error: {str(e)}")
        print("\n   Common issues:")
        print("   - Invalid API key")
        print("   - API key not activated")
        print("   - Network connectivity issues")
        return False

if __name__ == "__main__":
    import sys
    # Fix Windows encoding for emojis
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("Nano Banana TA Tool - API Test\n")
    success = test_gemini_connection()
    
    if success:
        print("\nAll systems ready! You can now run 'python main.py'")
    else:
        print("\nPlease fix the errors above before running the application")
        exit(1)

