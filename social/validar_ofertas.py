"""
🛡️ Titanium Link Validator v1.0
================================
Simula a lógica de seleção de link do bot_instagram.php ANTES de postar.
Garante que o link correto será enviado via DM.

Uso:
  python -m social.validar_ofertas                       # Valida todas as hashtags
  python -m social.validar_ofertas --caption "#blazer_premium #modafeminina"  # Simula um post
  python -m social.validar_ofertas --audit               # Auditoria completa
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import json
import os
import sys
import argparse

SITE_URL = "guiadodesconto.com.br"
OFERTAS_PATH = os.path.join(os.path.dirname(__file__), "ofertas.json")


def load_ofertas():
    with open(OFERTAS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def is_product_link(link: str) -> bool:
    """Verifica se é um link de produto real da Shopee (não do nosso site)."""
    return SITE_URL not in link


def escolher_link_inteligente(caption: str, ofertas: dict) -> tuple:
    """
    Replica EXATAMENTE a lógica v2.2 do bot_instagram.php em Python.
    Retorna (link_escolhido, tipo, hashtag_usada).
    """
    caption_lower = caption.lower()
    links_produto = {}
    
    # CAMADA 1: Hashtags exatas
    for hashtag, link in ofertas.items():
        if hashtag == "#default":
            continue
        if hashtag.lower() in caption_lower:
            links_produto[hashtag] = link

    # CAMADA 2: Keyword Match
    if not links_produto:
        for hashtag, link in ofertas.items():
            if hashtag == "#default":
                continue
            keyword = hashtag.replace('#', '').lower()
            keyword_clean = keyword.replace('_', ' ')
            if keyword in caption_lower or keyword_clean in caption_lower:
                links_produto[hashtag] = link

    # Prioridade: hashtag mais longa
    if links_produto:
        melhor = max(links_produto.keys(), key=len)
        tipo = "PRODUTO (Keyword/Hashtag) ✅" if is_product_link(links_produto[melhor]) else "SITE (Match) ⚠️"
        return links_produto[melhor], tipo, melhor

    # CAMADA 3: Deep Search (data.json)
    data_path = os.path.join(os.path.dirname(__file__), "..", "site", "data.json")
    if os.path.exists(data_path):
        with open(data_path, "r", encoding="utf-8") as f:
            data_json = json.load(f)
            for item in data_json:
                item_title = item['title'].lower()
                caption_words = set(caption_lower.split())
                title_words = set(item_title.split())
                intersection = caption_words.intersection(title_words)
                
                if len(intersection) >= 3:
                    return item['link'], "DEEP DATABASE MATCH 💎", item['title']

    # Prioridade 4: Default
    default = ofertas.get("#default", f"https://{SITE_URL}")
    return default, "DEFAULT (sem match) ⚠️", "#default"


def simulate_caption(caption: str, ofertas: dict):
    """Simula o que o bot faria com uma legenda específica."""
    print("\n" + "=" * 60)
    print("🧪 SIMULAÇÃO DE LEGENDA")
    print("=" * 60)
    print(f"📝 Caption: {caption[:100]}...")
    
    link, tipo, hashtag = escolher_link_inteligente(caption, ofertas)
    
    print(f"\n🎯 Resultado:")
    print(f"   Hashtag match: {hashtag}")
    print(f"   Tipo:          {tipo}")
    print(f"   Link enviado:  {link}")
    
    if "fallback" in tipo.lower() or "default" in tipo.lower():
        print(f"\n   ❌ ALERTA: O bot NÃO enviaria um link de produto!")
        print(f"   💡 Ação: Adicione a hashtag correta no ofertas.json com o link da Shopee.")
        return False
    
    print(f"\n   ✅ O bot enviaria o link do PRODUTO corretamente!")
    return True


def audit_all(ofertas: dict):
    """Auditoria completa do ofertas.json."""
    print("\n" + "=" * 60)
    print("🔍 AUDITORIA COMPLETA DO ofertas.json")
    print("=" * 60)

    sem_link = []
    com_link = []
    
    for hashtag, link in ofertas.items():
        if hashtag == "#default":
            continue
        if is_product_link(link):
            com_link.append((hashtag, link))
        else:
            sem_link.append((hashtag, link))

    print(f"\n✅ Hashtags com link de PRODUTO ({len(com_link)}):")
    for h, l in com_link:
        link_short = l[:60] + "..." if len(l) > 60 else l
        print(f"   {h:30s} → {link_short}")

    print(f"\n⚠️  Hashtags apontando para o SITE ({len(sem_link)}):")
    for h, l in sem_link:
        print(f"   {h:30s} → {l}")

    if sem_link:
        print(f"\n💡 RECOMENDAÇÃO: As {len(sem_link)} hashtags acima vão enviar o link do SITE")
        print(f"   em vez de um link de produto. Se alguma delas for usada em posts com")
        print(f"   produtos específicos, adicione o link correto da Shopee no ofertas.json.")

    # Teste de conflito: simula posts com múltiplas hashtags genéricas + específicas
    print(f"\n{'=' * 60}")
    print("🧪 TESTE DE CONFLITO (hashtag genérica vs. específica)")
    print("=" * 60)
    
    for h_prod, l_prod in com_link[:3]:  # Testa os primeiros 3 produtos
        # Simula uma legenda com a hashtag do produto + uma genérica
        if sem_link:
            h_gen = sem_link[0][0]
            fake_caption = f"Post de teste {h_prod} {h_gen} #modafeminina"
            link, tipo, matched = escolher_link_inteligente(fake_caption, ofertas)
            status = "✅ OK" if is_product_link(link) else "❌ FALHA"
            print(f"   {status} | Caption com '{h_prod}' + '{h_gen}' → Link: {tipo} via {matched}")

    print()


def main():
    parser = argparse.ArgumentParser(description="Titanium Link Validator")
    parser.add_argument("--caption", type=str, help="Simula uma legenda de post")
    parser.add_argument("--audit", action="store_true", help="Auditoria completa do ofertas.json")
    args = parser.parse_args()

    ofertas = load_ofertas()

    if args.caption:
        success = simulate_caption(args.caption, ofertas)
        sys.exit(0 if success else 1)
    elif args.audit:
        audit_all(ofertas)
    else:
        # Modo padrão: auditoria + testes
        audit_all(ofertas)


if __name__ == "__main__":
    main()
