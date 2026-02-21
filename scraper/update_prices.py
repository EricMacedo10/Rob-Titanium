#!/usr/bin/env python3
"""
==============================================
 TITANIUM PRICE UPDATER (Senior Workflow v2026)
 Atualiza preços de produtos Amazon no data.json
 usando o seletor .apex-pricetopay-value .a-offscreen
==============================================
"""
import json
import os
import sys
import time
import random
import re
from datetime import datetime

# Adiciona o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from bs4 import BeautifulSoup
    from core.browser import get_driver
except ImportError:
    print("⚠️  Dependências não encontradas. Instale: pip install beautifulsoup4 selenium")
    sys.exit(1)

# Caminhos
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_JSON_PATH = os.path.join(PROJECT_ROOT, 'site', 'data.json')
BACKUP_DIR = os.path.join(PROJECT_ROOT, 'backups')

# Configuração
AMAZON_TAG = "guiadodesco00-20"  # Tag de afiliado - NUNCA perder!


def extract_amazon_price(driver, url, retries=2):
    """
    Extrai o preço atual de um produto Amazon usando Selenium.
    Usa a cadeia de seletores identificada (Senior Workflow):
      1. .apex-pricetopay-value .a-offscreen
      2. .a-price[data-a-color="base"] .a-offscreen
      3. .a-price .a-offscreen  
      4. .a-price-whole (fallback legado)
    """
    for attempt in range(retries):
        try:
            driver.get(url)
            time.sleep(random.uniform(2.5, 4.5))

            # Check for bot detection
            if "Algo deu errado" in driver.title or "captcha" in driver.page_source.lower():
                print(f"      ⚠️  Bot detectado (tentativa {attempt + 1})")
                time.sleep(random.uniform(5, 10))
                driver.refresh()
                time.sleep(3)
                continue

            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Cadeia de seletores (prioridade)
            selectors = [
                '.apex-pricetopay-value .a-offscreen',
                '.a-price[data-a-color="base"] .a-offscreen',
                '.a-price .a-offscreen',
            ]

            for selector in selectors:
                el = soup.select_one(selector)
                if el:
                    price_text = el.text.strip()
                    # Ex: "R$3,90" ou "R$2.999,00"
                    price_str = price_text.replace('R$', '').replace('.', '').replace(',', '.').strip()
                    try:
                        price = float(price_str)
                        if price > 0:
                            return price
                    except ValueError:
                        continue

            # Fallback: .a-price-whole
            whole_el = soup.select_one('.a-price-whole')
            if whole_el:
                price_str = whole_el.text.strip().replace('.', '').replace(',', '.').strip()
                try:
                    return float(price_str)
                except ValueError:
                    pass

            print(f"      ❌ Preço não encontrado (tentativa {attempt + 1})")

        except Exception as e:
            print(f"      ❌ Erro na extração: {e}")

    return None


def update_prices():
    """
    Lê data.json, atualiza os preços de todos os produtos Amazon,
    faz backup e salva o arquivo atualizado.
    """
    print("=" * 60)
    print("🔧 TITANIUM PRICE UPDATER (Senior Workflow)")
    print("=" * 60)

    # Verificar data.json
    if not os.path.exists(DATA_JSON_PATH):
        print(f"❌ data.json não encontrado em: {DATA_JSON_PATH}")
        return False

    # Carregar dados
    with open(DATA_JSON_PATH, 'r', encoding='utf-8') as f:
        deals = json.load(f)

    print(f"📦 {len(deals)} produtos carregados")

    # Filtrar apenas Amazon
    amazon_deals = [d for d in deals if d.get('store', '').lower() == 'amazon']
    print(f"🔍 {len(amazon_deals)} produtos Amazon para atualizar")

    if not amazon_deals:
        print("⚠️  Nenhum produto Amazon encontrado.")
        return True

    # Backup antes de alterar
    os.makedirs(BACKUP_DIR, exist_ok=True)
    backup_name = f"data_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path = os.path.join(BACKUP_DIR, backup_name)
    with open(backup_path, 'w', encoding='utf-8') as f:
        json.dump(deals, f, ensure_ascii=False, indent=4)
    print(f"💾 Backup salvo: {backup_name}")

    # Iniciar Selenium
    driver = None
    updated = 0
    failed = 0

    try:
        driver = get_driver(headless=True)
        print("🌐 Selenium iniciado\n")

        for i, deal in enumerate(deals):
            if deal.get('store', '').lower() != 'amazon':
                continue

            link = deal.get('link', '')
            old_price = deal.get('price', 0)
            title = deal.get('title', 'Sem título')[:50]

            # Garantir tag de afiliado no link
            if 'tag=' not in link:
                link += ('&' if '?' in link else '?') + f'tag={AMAZON_TAG}'
                deal['link'] = link
                print(f"   🏷️  Tag de afiliado injetada: {AMAZON_TAG}")

            print(f"\n[{i+1}/{len(deals)}] {title}...")

            new_price = extract_amazon_price(driver, link)

            if new_price is not None:
                if new_price != old_price:
                    deal['price'] = new_price
                    deal['old_price'] = round(new_price * 1.25, 2)  # Desconto estimado de 20%
                    print(f"   ✅ Preço atualizado: R$ {old_price:.2f} → R$ {new_price:.2f}")
                    updated += 1
                else:
                    print(f"   ✔️  Preço inalterado: R$ {old_price:.2f}")
            else:
                print(f"   ⚠️  Não foi possível obter preço")
                failed += 1

            # Delay anti-bot
            time.sleep(random.uniform(2, 4))

    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
    finally:
        if driver:
            driver.quit()

    # Salvar dados atualizados
    with open(DATA_JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(deals, f, ensure_ascii=False, indent=4)

    print(f"\n{'=' * 60}")
    print(f"📊 Resultado: {updated} atualizados, {failed} falharam")
    print(f"💾 data.json salvo com preços atualizados")
    print(f"{'=' * 60}")

    return True


if __name__ == "__main__":
    update_prices()
""", "Complexity": 6, "Description": "Creating the update_prices.py script that reads data.json, visits each Amazon product link with Selenium, extracts the current price using the improved selector chain, backs up the data, and saves the updated prices. Affiliate tags are verified and preserved during the process. Following Senior Workflow.", "EmptyFile": false, "IsArtifact": false, "Overwrite": false}
