import json
import time
import random
from scraper.settings import TARGETS, MIN_DELAY, MAX_DELAY
from scraper.link_builder import build_affiliate_link
from scraper.upload import upload_to_hostinger
from scraper.amazon import search_amazon  # Scraper Amazon

def main():
    print("🤖 Robô Titanium Iniciado [MODO ULTRACONSERVADOR]")
    print(f"📋 Lista de alvos: {len(TARGETS)} produtos para monitorar.")
    
    products_found = []

    for target in TARGETS:
        # 1. Delay de Segurança (Anti-Ban)
        wait_time = random.uniform(MIN_DELAY, MAX_DELAY)
        print(f"⏳ Aguardando {wait_time:.1f}s para segurança...")
        time.sleep(wait_time)

        # 2. Busca (Scraping)
        term = target['term']
        store = target['store']
        max_price = target.get('max_price', 1000)
        
        product = None
        
        if store == 'amazon':
            product = search_amazon(term)
            
        elif store == 'mercadolivre':
            # Usa scraper do ML (requer Selenium)
            try:
                from scraper.mercadolivre import search_mercadolivre
                from scraper.amazon import get_driver
                
                print(f"🔍 Buscando no Mercado Livre: {term}")
                driver = get_driver()
                
                try:
                    product = search_mercadolivre(term, driver, max_price=int(max_price))
                finally:
                    driver.quit()
                    
            except Exception as e:
                print(f"⚠ Erro ao buscar no ML: {e}")
                continue
                
        # elif store == 'shopee': product = search_shopee(term) # Aguardando API (23/01)
        else:
            print(f"⚠ Loja {store} ainda não implementada.")
            continue

        if product:
            # 3. Filtro de Preço (Compara apenas parte inteira)
            price_integer = int(product['price'])
            max_price_integer = int(target['max_price'])
            
            print(f"   💰 Preço: R$ {product['price']:.2f} (parte inteira: {price_integer}) | Máximo: {max_price_integer}")
            
            if price_integer <= max_price_integer:
                print(f"🔥 OFERTA APROVADA: {product['title'][:30]}... por R$ {product['price']:.2f}")
                
                # 4. Link de Afiliado (com suporte a ML via meli_api)
                product['link'] = build_affiliate_link(
                    product['link'], 
                    target['store'],
                    keyword=term  # Passa palavra-chave para ML
                )
                
                products_found.append(product)
            else:
                print(f"❌ Preço alto ({price_integer} > {max_price_integer}). Ignorando.")
        else:
             print(f"💨 Produto não encontrado ou erro na busca.")

    # 5. Salvar JSON Local
    local_path = 'site/data.json'
    if products_found:
        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(products_found, f, indent=4, ensure_ascii=False)
        print(f"💾 Arquivo {local_path} atualizado com {len(products_found)} ofertas reais.")
    else:
        print("⚠ Nenhuma oferta nova encontrada. Arquivo data.json mantido.")

    # 6. Upload FTP (Mockado por enquanto)
    # upload_to_hostinger(...) 

if __name__ == "__main__":
    main()

