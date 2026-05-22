import os

docs_dir = r"c:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\docs\TITANIUM_BRAIN"

# 1. Update 01_SCRAPER_ENGINES_AND_ARBITRATION.md
f1 = os.path.join(docs_dir, "01_SCRAPER_ENGINES_AND_ARBITRATION.md")
with open(f1, "r", encoding="utf-8") as f: content = f.read()
content = content.replace("v5.2.0-Stable (Freshness Policy + Header Aliasing)", "v5.4.2-Elite (Freshness Policy + Fallback Deduplication Fix)")
content = content.replace("10/05/2026", "17/05/2026")
if "Fallback API Resilience (v5.4.2)" not in content:
    content = content.replace("## 🤖 3. Curadoria com IA & Arbitragem (v3.2.0)", "## 🤖 3. Curadoria com IA & Arbitragem (v3.2.0)\n\n### 🛡️ Fallback API Resilience (v5.4.2)\nO `orchestrator.py` garante inclusão atômica de ofertas provindas da API GraphQL de Fallback, caso as URLs do Datafeed de 100K expirem, preservando a consistência da vitrine (evitando travamento por Lista Vazia).")
with open(f1, "w", encoding="utf-8") as f: f.write(content)

# 2. Update 02_FRONTEND_ENGINEERING.md
f2 = os.path.join(docs_dir, "02_FRONTEND_ENGINEERING.md")
with open(f2, "r", encoding="utf-8") as f: content = f.read()
content = content.replace("06/05/2026 - Versão: 3.8.3-Nuclear", "17/05/2026 - Versão: 3.8.4-Sensual (Category Filter Active)")
if "Sensual Category Isolation" not in content:
    content = content.replace("### 2. A Vitrine Aberta & Especializada", "### 2. A Vitrine Aberta & Especializada\n\n#### 🛡️ Sensual Category Isolation (v3.8.4)\nPara prevenir que Lingeries ('Moda & Luxo') transbordem para a seção de Cosméticos no `sensual.html`, o `deals-grid` implementa filtro explícito via JavaScript para `Cosmética Sensorial` e `Tecnologia Íntima`.")
with open(f2, "w", encoding="utf-8") as f: f.write(content)

# 3. Update 05_AI_OPERATIONAL_PROTOCOLS.md
f3 = os.path.join(docs_dir, "05_AI_OPERATIONAL_PROTOCOLS.md")
with open(f3, "r", encoding="utf-8") as f: content = f.read()
content = content.replace("08/05/2026", "17/05/2026")
content = content.replace("Premium Reels Active | Nuclear Shield v3.9", "Datafeed Fallback & Sensual Filtering Active | Nuclear Shield v3.9")
lesson = """
### 🛒 Filtro de Exibição Front-End (Lessons Learned 2026-05-17)
- **Causa:** Produtos de um mesmo banco de dados (ex: `data_sensual.json`) com categorias distintas competiam por espaço no array `.slice(0, 24)` desenhado na tela. Lingeries preenchiam os slots antes dos cosméticos serem renderizados.
- **Solução (v3.8.4):** É obrigatório usar um `.filter()` explícito por categoria no JavaScript (`app_sensual.js`) antes do `.slice()`, garantindo que seções temáticas como "Cosmética & Bem-Estar" renderizem apenas os produtos designados.

### 🛡️ Tratamento de Fallback de Datafeed (2026-05-17)
- As URLs do **Shopee Datafeed** expiram. O orquestrador (`core/orchestrator.py`) foi corrigido para sempre mesclar as ofertas extraídas pelo motor de *fallback local* (`update_manual_targets`) na lista global `unique_new`, impedindo o bloqueio do site por lista vazia.
"""
if "Filtro de Exibição Front-End" not in content:
    content = content.replace("## 🚀 Hotfixes e Deploy Emergencial", lesson + "\n## 🚀 Hotfixes e Deploy Emergencial")
with open(f3, "w", encoding="utf-8") as f: f.write(content)

# Update remaining files dates
def bump_date(filename, old_str, new_str):
    p = os.path.join(docs_dir, filename)
    with open(p, "r", encoding="utf-8") as f: c = f.read()
    c = c.replace(old_str, new_str)
    with open(p, "w", encoding="utf-8") as f: f.write(c)

bump_date("00_SYSTEM_ARCHITECTURE.md", "10/05/2026 - Versão: v5.2.0-Elite", "17/05/2026 - Versão: v5.4.2-Elite")
bump_date("03_SOCIAL_MEDIA_AUTOMATION.md", "11/05/2026 - Status: Ultra-Safe Positioning v5.4.1", "17/05/2026 - Status: Ultra-Safe Positioning v5.4.2")
bump_date("04_CI_CD_WORKFLOWS.md", "10/05/2026 - Versão: v5.2.0-Stable", "17/05/2026 - Versão: v5.4.2-Stable")
bump_date("06_SECURITY_GUIDELINES.md", "Versão: 1.0 (Segurança do Titanium Brain)", "Versão: 1.1 (Segurança do Titanium Brain - v5.4.2)")

print("Documentação atualizada com sucesso!")
