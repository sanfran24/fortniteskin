import requests
import sys

print("Testing Fortnite Skin Generator API...")
print("=" * 50)

try:
    files = {'file': open('image (3).jpg', 'rb')}
    data = {'style': 'anime'}
    
    print("Uploading image and generating skin...")
    print("Style: anime")
    print("This may take 30-60 seconds...")
    print()
    
    r = requests.post('http://localhost:8000/generate', files=files, data=data, timeout=120)
    
    print(f"Status Code: {r.status_code}")
    
    if r.status_code == 200:
        result = r.json()
        print(f"Success: {result.get('success')}")
        print(f"Style: {result.get('style')}")
        print(f"Generated Images: {len(result.get('generated_images', []))} images")
        print(f"Description Length: {len(result.get('description', ''))} characters")
        
        skin_details = result.get('skin_details', {})
        print(f"Skin Name: {skin_details.get('name', 'N/A')}")
        print(f"Rarity: {skin_details.get('rarity', 'N/A')}")
        
        print()
        print("First 500 chars of description:")
        print("-" * 40)
        print(result.get('description', '')[:500])
        print()
        print("API TEST PASSED!")
    else:
        print(f"Error: {r.text[:500]}")
        sys.exit(1)
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)

