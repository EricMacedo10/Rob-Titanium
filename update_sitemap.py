import os
from datetime import datetime

def generate_sitemap():
    base_url = "https://guiadodesconto.com.br"
    site_dir = "site"
    blog_dir = os.path.join(site_dir, "blog")
    sitemap_path = os.path.join(site_dir, "sitemap.xml")
    
    urls = []
    
    # 1. Main pages
    main_pages = ["index.html", "sobre.html", "privacidade.html", "termos.html", "blog.html", "categoria.html"]
    for page in main_pages:
        if os.path.exists(os.path.join(site_dir, page)):
            priority = "1.0" if page == "index.html" else "0.8"
            urls.append({
                "loc": f"{base_url}/{page}",
                "lastmod": datetime.now().strftime("%Y-%m-%d"),
                "priority": priority
            })
            
    # 2. Blog posts
    if os.path.exists(blog_dir):
        for post in os.listdir(blog_dir):
            if post.endswith(".html"):
                urls.append({
                    "loc": f"{base_url}/blog/{post}",
                    "lastmod": datetime.now().strftime("%Y-%m-%d"),
                    "priority": "0.7"
                })
                
    # Generate XML
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url in urls:
        xml_content += '    <url>\n'
        xml_content += f'        <loc>{url["loc"]}</loc>\n'
        xml_content += f'        <lastmod>{url["lastmod"]}</lastmod>\n'
        xml_content += f'        <priority>{url["priority"]}</priority>\n'
        xml_content += '    </url>\n'
        
    xml_content += '</urlset>'
    
    with open(sitemap_path, "w", encoding="utf-8") as f:
        f.write(xml_content)
    
    print(f"[Sucesso] Sitemap.xml atualizado com {len(urls)} URLs.")

if __name__ == "__main__":
    generate_sitemap()
