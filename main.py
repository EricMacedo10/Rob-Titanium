import json
import time
import random
from datetime import datetime
from scraper.settings import TARGETS, MIN_DELAY, MAX_DELAY
from scraper.link_builder import build_affiliate_link
from scraper.upload import upload_to_hostinger
from scraper.amazon import search_amazon  # Scraper Amazon

def main():
    start_time = datetime.now()
    print("="*60)
    print("🤖 Robô Titanium Iniciado [MODO ULTRACONSERVADOR]")
    print(f"📅 Data/Hora: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📋 Lista de alvos: {len(TARGETS)} produtos para monitorar.")
    print("="*60)
    
    products_found = []
    errors = []

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
                error_msg = f"Erro ao buscar no ML ({term}): {e}"
                print(f"⚠ {error_msg}")
                errors.append(error_msg)
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
    print("\n" + "="*60)
    if products_found:
        with open(local_path, 'w', encoding='utf-8') as f:
            json.dump(products_found, f, indent=4, ensure_ascii=False)
        print(f"💾 Arquivo {local_path} atualizado com {len(products_found)} ofertas reais.")
    else:
        print("⚠ Nenhuma oferta nova encontrada. Arquivo data.json mantido.")

    # 6. Upload FTP para Hostinger
    if products_found:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        ftp_host = os.getenv('FTP_HOST')
        ftp_user = os.getenv('FTP_USER')
        ftp_pass = os.getenv('FTP_PASS')
        
        if ftp_host and ftp_user and ftp_pass:
            print("\n🌐 Iniciando upload para Hostinger...")
            upload_success = upload_to_hostinger(
                local_file_path=local_path,
                ftp_host=ftp_host,
                ftp_user=ftp_user,
                ftp_pass=ftp_pass,
                remote_path='public_html/data.json'
            )
            if upload_success:
                print("🎉 Site atualizado com sucesso!")
            else:
                print("⚠️ Upload falhou, mas arquivo local foi salvo.")
        else:
            print("⚠️ Credenciais FTP não configuradas. Apenas salvando localmente.")
    
    # 7. Resumo da Execução
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print("=" * 60)
    print("📊 RESUMO DA EXECUÇÃO")
    print("=" * 60)
    print(f"✅ Produtos encontrados: {len(products_found)}")
    print(f"❌ Erros encontrados: {len(errors)}")
    print(f"⏱️  Tempo total: {duration:.1f}s ({duration/60:.1f} min)")
    print(f"📅 Finalizado em: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    if errors:
        print("\n⚠️  ERROS DETALHADOS:")
        for i, error in enumerate(errors, 1):
            print(f"  {i}. {error}")
    
    print("=" * 60)
    print("🎉 Robô Titanium finalizado!")
    print("=" * 60)

if __name__ == "__main__":
    main()
