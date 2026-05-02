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

print("Fetching last 6 posts captions...")

url = f"https://graph.facebook.com/v21.0/{IG_BUSINESS_ID}/media?fields=id,caption&limit=6&access_token={USER_TOKEN}"
try:
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        print("ERROR:", json.dumps(data['error'], indent=2))
    else:
        for post in data.get('data', []):
            print(f"ID: {post['id']}")
            print(f"Caption: {post.get('caption', 'NO CAPTION')}")
            print("-" * 30)
except Exception as e:
    print("Exception:", e)
