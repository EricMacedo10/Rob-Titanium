import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('IG_ACCESS_TOKEN')
business_id = os.getenv('IG_BUSINESS_ID')

url = f"https://graph.facebook.com/v21.0/{business_id}/media?fields=id,caption&limit=10&access_token={token}"
response = requests.get(url)
data = response.json()

print(f"Status Code: {response.status_code}")
if 'data' in data:
    print(f"Found {len(data['data'])} posts:")
    for post in data['data']:
        print(f"- ID: {post.get('id')} | Caption: {post.get('caption', 'NO CAPTION')[:50]}...")
        
        # Check comments for each post
        comment_url = f"https://graph.facebook.com/v21.0/{post['id']}/comments?fields=id,text,username&access_token={token}"
        c_res = requests.get(comment_url).json()
        if 'data' in c_res:
            print(f"  Found {len(c_res['data'])} comments:")
            for c in c_res['data']:
                print(f"    [{c['username']}] {c['text']}")
else:
    print("Error or No Data:")
    print(data)
