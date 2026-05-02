import json
import os
import time

def test_automation_logic():
    print("="*60)
    print("TESTE DE INTEGRIDADE: AUTOMACAO DE LINKS INSTAGRAM")
    print("="*60)

    data_file = 'site/data.json'
    fila_dir = 'social/fila'
    os.makedirs(fila_dir, exist_ok=True)

    if not os.path.exists(data_file):
        print("❌ Erro: data.json não encontrado.")
        return

    with open(data_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    if not products:
        print("❌ Erro: data.json está vazio.")
        return

    # Pega o primeiro produto (o mais recente minerado)
    prod = products[0]
    print(f"Produto Selecionado: {prod['title']}")
    print(f"Link no Banco de Dados: {prod['link']}")

    # Simula a criação de um metadado de postagem na fila
    post_id = int(time.time())
    metadata = {
        "id": prod['id'],
        "title": prod['title'],
        "price": prod['price'],
        "link": prod['link'], # Aqui deve estar o s.shopee.com.br
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
    }

    meta_path = os.path.join(fila_dir, f"test_post_{post_id}.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=4, ensure_ascii=False)

    print(f"\nMetadado de postagem gerado em: {meta_path}")
    print("\n--- AUDITORIA DE LINK ---")
    if "s.shopee.com.br" in prod['link']:
        print("RESULTADO: SUCESSO! O link e um Shortlink Oficial da Shopee.")
    else:
        print("AVISO: O link ainda nao e um Shortlink. Verifique a API.")
    print("-" * 25)

if __name__ == "__main__":
    test_automation_logic()
