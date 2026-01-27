import os
import sys
import logging
import time

# Adicionar root ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Importar scrapers
from scraper.mercadolivre_api import search_mercadolivre
from scraper.shopee_affiliate import search_shopee
from scraper.amazon import search_amazon

# Config logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ml():
    print("\n" + "="*50)
    print("Testing Mercado Livre Scraper")
    print("="*50)
    try:
        results = search_mercadolivre("iPhone 15", limit=3)
        print(f"Count: {len(results)}")
        for r in results:
            print(f" - {r['titulo']}")
            print(f"   Price: {r['preco']}")
            print(f"   Link: {r['link_afiliado'][:50]}...")
            if r['preco'] == 0:
                print("   ⚠️  WARNING: Price is zero!")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_shopee():
    print("\n" + "="*50)
    print("Testing Shopee Scraper")
    print("="*50)
    try:
        results = search_shopee("iPhone 15", limit=3)
        print(f"Count: {len(results)}")
        for r in results:
            print(f" - {r['titulo']}")
            print(f"   Price: {r['preco']}")
            print(f"   Link: {r['link_afiliado'][:50]}...")
            if r['preco'] == 0:
                print("   ⚠️  WARNING: Price is zero!")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_amazon():
    print("\n" + "="*50)
    print("Testing Amazon Scraper")
    print("="*50)
    try:
        # Amazon scraper returns a SINGLE dict or None
        result = search_amazon("iPhone 15")
        if result:
            print(f" - {result['title']}")
            print(f"   Price: {result['price']}")
            print(f"   Link: {result['link'][:50]}...")
            if result['price'] == 0:
                print("   ⚠️  WARNING: Price is zero!")
        else:
            print("❌ No finding for Amazon")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Debug Session...")
    
    test_ml()
    test_shopee()
    test_amazon()
