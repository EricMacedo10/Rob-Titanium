import sys
import os
import asyncio
import json
from scraper.shopee_affiliate import search_shopee, ShopeeAffiliateAPI
from scraper.mercadolivre_api import search_mercadolivre
from core.settings import SHOPEE_APP_ID, SHOPEE_SECRET

def test_shopee_auth():
    print(f"\n{'='*20} TESTING SHOPEE AUTH {'='*20}")
    print(f"App ID from env: {SHOPEE_APP_ID}")
    print(f"Secret from env: {SHOPEE_SECRET[:5]}...")
    
    try:
        api = ShopeeAffiliateAPI()
        # Try to generate a link for a generic product to test auth
        test_url = "https://shopee.com.br/product/123/456"
        link = api.generate_short_link(test_url)
        
        if link:
            print(f"✅ Auth Success! Generated Link: {link}")
        else:
            print(f"❌ Auth Failed: returned None")
    except Exception as e:
        print(f"❌ Auth Critical Error: {e}")

def run_diagnostics():
    print("🔍 INITIATING DEEP DIAGNOSTICS...")
    term = "fone bluetooth"
    
    # 1. MERCADO LIVRE
    print(f"\n🔵 TESTING MERCADO LIVRE ('{term}')...")
    try:
        ml_results = search_mercadolivre(term, limit=1)
        if ml_results:
            print(f"✅ Success! Found {len(ml_results)} items.")
            item = ml_results[0]
            print(f"   Title: {item['titulo']}")
            print(f"   Price: R$ {item['preco']}")
            print(f"   Link:  {item['link_afiliado']}")
            if "matt_tool=188269638" in item['link_afiliado']:
                print("   ✅ Affiliate Tag (matt_tool) CONFIRMED")
            else:
                print("   ❌ Affiliate Tag MISSING")
        else:
            print("⚠️ No results from Mercado Livre.")
    except Exception as e:
        print(f"❌ Mercado Livre Error: {e}")

    # 2. SHOPEE
    print(f"\n🟠 TESTING SHOPEE ('{term}')...")
    test_shopee_auth()
    try:
        sh_results = search_shopee(term, limit=1)
        if sh_results:
            print(f"✅ Success! Found {len(sh_results)} items.")
            item = sh_results[0]
            print(f"   Title: {item['titulo']}")
            print(f"   Price: R$ {item['preco']}")
            print(f"   Link:  {item['link_afiliado']}")
        else:
            print("⚠️ No results from Shopee (Is API enabled?).")
    except Exception as e:
        print(f"❌ Shopee Error: {e}")

if __name__ == "__main__":
    run_diagnostics()
