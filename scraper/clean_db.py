import json

with open('site/data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

bad_count = 0
valid_data = []

for item in data:
    img = item.get("image", "")
    title = item.get("title", "Sem título")
    link = item.get("link", "")
    
    # Check if the image starts with "data:image" (Base64 placeholder), is missing entirely, or is an SVG placeholder
    if not img or img.startswith("data:image") or ".svg" in img:
        print(f"🗑️ Removendo item defeituoso (Imagem ausente/SVG/Base64): {title[:40]}")
        bad_count += 1
    elif not link or "javascript:" in link or not link.startswith("http"):
        print(f"🗑️ Removendo item defeituoso (Link inválido): {title[:40]}")
        bad_count += 1
    else:
        valid_data.append(item)

if bad_count > 0:
    with open('site/data.json', 'w', encoding='utf-8') as f:
        json.dump(valid_data, f, indent=4, ensure_ascii=False)
    print(f"✅ {bad_count} itens defeituosos removidos. Banco de dados salvo com {len(valid_data)} itens limpos.")
else:
    print("✅ Nenhum defeito encontrado nas imagens ou links.")
