import os
import json
import re

def update_blog_index():
    blog_dir = 'site/blog'
    output_file = 'site/blog/list.json'
    
    if not os.path.exists(blog_dir):
        print("Diretório de blog não encontrado.")
        return

    articles = []
    for filename in os.listdir(blog_dir):
        if filename.endswith('.html') and filename != 'list.json':
            path = os.path.join(blog_dir, filename)
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extrai o título (H1)
                title_match = re.search(r'<h1>(.*?)</h1>', content)
                title = title_match.group(1) if title_match else filename.replace('.html', '').replace('-', ' ').title()
                
                articles.append({
                    "slug": filename.replace('.html', ''),
                    "title": title
                })

    # Ordena alfabeticamente ou poderia ser por data se tivéssemos
    articles.sort(key=lambda x: x['title'])

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)
    
    print(f"[Sucesso] Índice de blog atualizado com {len(articles)} artigos.")

if __name__ == "__main__":
    update_blog_index()
