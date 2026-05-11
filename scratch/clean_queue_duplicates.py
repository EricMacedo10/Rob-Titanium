import os
import json

QUEUE_DIR = "social/fila"

def clean_queue():
    if not os.path.exists(QUEUE_DIR):
        print("Diretório da fila não existe.")
        return

    files = os.listdir(QUEUE_DIR)
    json_files = [f for f in files if f.endswith('.json')]
    
    seen_titles = set()
    removed_count = 0
    
    # Ordenar por nome para processar os mais antigos primeiro (timestamp no nome)
    json_files.sort()
    
    for f in json_files:
        path = os.path.join(QUEUE_DIR, f)
        try:
            with open(path, 'r', encoding='utf-8') as j:
                data = json.load(j)
                title = data.get('title', '').lower().strip()
                
                if not title or title in seen_titles:
                    # Remover duplicata
                    os.remove(path)
                    # Remover imagem correspondente
                    img_path = path.replace('.json', '.jpg')
                    if os.path.exists(img_path):
                        os.remove(img_path)
                    removed_count += 1
                    print(f"Removido: {title}")
                else:
                    seen_titles.add(title)
        except Exception as e:
            print(f"Erro ao processar {f}: {e}")
            
    print(f"\nLimpeza concluída. Removidos {removed_count} itens duplicados da fila.")

if __name__ == "__main__":
    clean_queue()
