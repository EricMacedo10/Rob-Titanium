import os
import json

QUEUE_DIR = "social/fila"

def clean_queue():
    if not os.path.exists(QUEUE_DIR):
        print("Diretório da fila não existe.")
        return

    files = os.listdir(QUEUE_DIR)
    json_files = [f for f in files if f.endswith('.json')]
    json_files.sort()
    
    seen_titles = set()
    to_remove = []
    
    for f in json_files:
        path = os.path.join(QUEUE_DIR, f)
        title = None
        try:
            with open(path, 'r', encoding='utf-8') as j:
                data = json.load(j)
                title = data.get('title', '').lower().strip()
        except Exception as e:
            print(f"Erro ao ler {f}: {e}")
            continue
            
        if title:
            if title in seen_titles:
                to_remove.append(path)
            else:
                seen_titles.add(title)
    
    removed_count = 0
    for path in to_remove:
        try:
            # Tentar remover o JSON
            if os.path.exists(path):
                os.remove(path)
            
            # Tentar remover a imagem correspondente
            img_path = path.replace('.json', '.jpg')
            if os.path.exists(img_path):
                os.remove(img_path)
                
            removed_count += 1
            print(f"Removido: {path}")
        except Exception as e:
            print(f"Erro ao remover {path}: {e}")
            
    print(f"\nLimpeza concluída. Removidos {removed_count} itens duplicados da fila.")

if __name__ == "__main__":
    clean_queue()
