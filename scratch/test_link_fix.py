import re
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode

def build_affiliate_link_fixed(url, tag):
    if not url or 'shopee.com.br' not in url:
        return url

    # Parse da URL
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    # Força a tag única (substitui qualquer lista de utm_source por uma lista de um único item)
    params['utm_source'] = [tag]

    # Reconstrói a URL
    new_query = urlencode(params, doseq=True)
    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        new_query,
        parsed.fragment
    ))
    
    return new_url

# Testes
tag = "an_18318830863"
test_urls = [
    "https://s.shopee.com.br/W2iYvLXc2",
    "https://s.shopee.com.br/W2iYvLXc2?utm_source=old_tag",
    "https://s.shopee.com.br/W2iYvLXc2?utm_source=an_18318830863&utm_source=an_18318830863",
    "https://shopee.com.br/product/123/456?sp_atk=abc"
]

print("--- Testes de Blindagem ---")
for u in test_urls:
    fixed = build_affiliate_link_fixed(u, tag)
    print(f"Original: {u}")
    print(f"Fixed:    {fixed}")
    print("-" * 20)
