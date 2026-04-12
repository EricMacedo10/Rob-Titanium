import os
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient

load_dotenv()
ig_token = os.getenv("IG_ACCESS_TOKEN")
ig_business_id = os.getenv("IG_BUSINESS_ID")
page_id = os.getenv("PAGE_ID")

client = InstagramClient(ig_token, ig_business_id, page_id=page_id)
media = client.get_latest_media(limit=1)
if media:
    print(f"ID: {media[0]['id']}")
    print(f"Caption: {media[0]['caption'][:100]}...")
    print(f"Permalink: {media[0]['permalink']}")
else:
    print("Nenhuma midia encontrada.")
