import os
from dotenv import load_dotenv
from social.core.instagram_client import InstagramClient

load_dotenv()
ig_token = os.getenv("IG_ACCESS_TOKEN")
ig_business_id = os.getenv("IG_BUSINESS_ID")
page_id = os.getenv("PAGE_ID")

print("--- Testando Conexão ---")
try:
    client = InstagramClient(ig_token, ig_business_id, page_id=page_id)
    print(f"Page Token: {'OK' if client.page_access_token else 'FALHA'}")
    media = client.get_latest_media(limit=1)
    print(f"Ultima postagem: {media[0]['id'] if media else 'Nenhuma'}")
except Exception as e:
    print(f"Erro: {e}")
