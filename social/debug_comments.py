import os
import json
import requests
import sys
import io
from dotenv import load_dotenv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
load_dotenv()

USER_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")

print("Fetching last 3 posts and their comments...")

url = f"https://graph.facebook.com/v21.0/{IG_BUSINESS_ID}/media?fields=id,caption&limit=3&access_token={USER_TOKEN}"
try:
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        print("ERROR:", json.dumps(data['error'], indent=2))
    else:
        for post in data.get('data', []):
            media_id = post['id']
            print(f"\nPOST ID: {media_id}")
            print(f"Caption: {post.get('caption', 'NO CAPTION')[:100]}...")
            
            # Fetch comments
            comments_url = f"https://graph.facebook.com/v21.0/{media_id}/comments?fields=id,text,username&access_token={USER_TOKEN}"
            comments_resp = requests.get(comments_url)
            comments_data = comments_resp.json()
            
            comments = comments_data.get('data', [])
            print(f"Comments found: {len(comments)}")
            for comment in comments:
                print(f"  - @{comment.get('username')}: {comment.get('text')}")
            print("-" * 30)
except Exception as e:
    print("Exception:", e)
