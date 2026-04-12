import json
import os

def diagnose_tags():
    data_path = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\data.json"
    
    if not os.path.exists(data_path):
        print("Erro: data.json não encontrado.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    stats = {
        "total": len(data),
        "amazon_ok": 0, "amazon_fail": 0,
        "shopee_ok": 0, "shopee_fail": 0,
        "meli_ok": 0, "meli_fail": 0
    }
    
    failures = []

    for item in data:
        store = item.get("store", "").lower()
        link = item.get("link", "")
        
        if "amazon" in store:
            if "tag=guiadodesco00-20" in link:
                stats["amazon_ok"] += 1
            else:
                stats["amazon_fail"] += 1
                failures.append(f"[AMAZON] Sem TAG: {item['title'][:50]}")
        
        elif "shopee" in store:
            # Shopee aceita link curto (s.shopee ou shope.ee) ou longo com utm_source
            if "utm_source=an_18318830863" in link or "s.shopee.com.br" in link or "shope.ee" in link:
                stats["shopee_ok"] += 1
            else:
                stats["shopee_fail"] += 1
                failures.append(f"[SHOPEE] Sem TAG: {item['title'][:50]} | Link: {link[:50]}...")
        
        elif "mercado livre" in store or "meli" in store:
            if "matt_tool=188269638" in link:
                stats["meli_ok"] += 1
            else:
                stats["meli_fail"] += 1
                failures.append(f"[MELI] Sem TAG: {item['title'][:50]}")

    print("\n=== RELATÓRIO DE SAÚDE DOS LINKS (Robô Titanium) ===")
    print(f"Total de Produtos Analisados: {stats['total']}")
    print(f"✅ Amazon: {stats['amazon_ok']} OK / {stats['amazon_fail']} Falhas")
    print(f"✅ Shopee: {stats['shopee_ok']} OK / {stats['shopee_fail']} Falhas")
    print(f"✅ Meli:   {stats['meli_ok']} OK / {stats['meli_fail']} Falhas")
    
    if failures:
        print("\n--- Detalhes das Falhas Encontradas ---")
        for f in failures[:15]: # Mostra os primeiros 15
            print(f)
        if len(failures) > 15:
            print(f"... e mais {len(failures)-15} falhas.")
    else:
        print("\n✨ Incrível! Todos os links no banco de dados estão com tags corretas.")

if __name__ == "__main__":
    diagnose_tags()
