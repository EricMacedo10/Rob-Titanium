import os
import requests
from dotenv import load_dotenv

def test_single_post():
    load_dotenv()
    token = os.getenv("IG_ACCESS_TOKEN")
    business_id = os.getenv("IG_BUSINESS_ID")
    
    # Image from ImgBB (already uploaded in previous attempt)
    img_url = "https://i.ibb.co/6JDBKzZF/43dcf70be5c2.jpg"
    
    print(f"Testing post with: {img_url}")
    
    base_url = f"https://graph.facebook.com/v21.0/{business_id}/media"
    payload = {
        "image_url": img_url,
        "caption": "Test post from Titanium Bot",
        "access_token": token
    }
    
    resp = requests.post(base_url, data=payload)
    print(f"Response: {resp.json()}")

if __name__ == "__main__":
    test_single_post()
