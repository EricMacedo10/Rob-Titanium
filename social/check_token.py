import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

USER_TOKEN = os.getenv("IG_ACCESS_TOKEN")
IG_BUSINESS_ID = os.getenv("IG_BUSINESS_ID")
PAGE_ID = os.getenv("PAGE_ID")

print("Checking tokens...")

url = f"https://graph.facebook.com/v21.0/{IG_BUSINESS_ID}/media?fields=id,caption&limit=6&access_token={USER_TOKEN}"
try:
    response = requests.get(url)
    data = response.json()
    if 'error' in data:
        print("ERROR:", json.dumps(data['error'], indent=2))
    else:
        print("SUCCESS:", len(data.get('data', [])), "posts fetched.")
except Exception as e:
    print("Exception:", e)
