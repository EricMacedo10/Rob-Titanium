# 🛡️ Titanium Brain: AI Operational Protocols (Senior Rules)

This document establishes the "Rules of Engagement" for any AI agent or professional interacting with the Titanium codebase.

## 🖋️ The "Senior Workflow" Protocol

1.  **Iterative Analysis**: Before any change, read this Knowledge Base (`docs/TITANIUM_BRAIN/`).
2.  **Implementation Plans**: Every non-trivial task requires an `implementation_plan.md` with:
    - User Review Required section.
    - Detailed File Mapping (MODIFY/NEW/DELETE).
    - Verification Plan (Automated + Manual).
3.  **Verification Walkthrough**: Every task must end with a `walkthrough.md` documenting results with screenshots or logs.

## 🚫 The "Don't Touch" List

- **`index.html` Hierarchy**: Do not restructure the main layout IDs (`deals-grid`, etc.) without updating the JS selectors in `app.js`.
- **`state/` Directory**: Do not commit this folder. It contains volatile but critical session tokens.
- **Affiliate Tag Logic**: Do not hardcode tags in the middle of functions. Always use `core/settings.py` or the `app.js` config block.

## 🛠️ Troubleshooting Guide

| **Symptom** | **Probable Cause** | **Action** |
| :--- | :--- | :--- |
| **Site Empty** | `data.json` is 0KB or invalid. | Check `orchestrator.log` for Scraper blocks. |
| **Links not tracking** | Tag normalized incorrectly. | Check `normalizeStore` logic in `app.js`. |
| **ML Search Failing** | Token Expired and Refresh failed. | Delete `state/meli_tokens.json` to force re-auth. |
| **Social Bot not posting** | IG Container Timeout / code 9004. | Prioritize Hostinger (FTP) over ImgBB. |
| **File Deletion Bug** | Shared filename in tmp logic. | Use Unique Timestamped Temps (Rule of Traceability). |
| **Lightning Bar não aparece** | `staging-mode` class ausente OU URL não contém 'staging'. | Verificar se `index.html` do subdomínio é o `index_staging.html`. Checar condição de ativação no `app.js`. |
| **Elemento persiste após JS remover** | Cache do browser ou `display:block` inline do JS. | Adicionar `display: none !important` no CSS como camada definitiva. |
| **Upload FTP não navega para subpasta** | `upload_logic.py` sem navegação recursiva. | Usar `_ensure_remote_dir()` que cria subpastas automaticamente. |


## 🚀 Protocolos de Resiliência de Fluxo (v1156)

Para prevenir erros de "timeout" e perda de dados em automações complexas:

1.  **Regra de Rastreabilidade (Unique Temps)**: Qualquer lógica que gere arquivos temporários (ex: conversão de imagem) **DEVE** usar nomes únicos com timestamp (`temp_1713...`). Nunca use o nome do arquivo original como base para arquivos deletáveis.
2.  **Regra de Proximidade de Rede**: Para APIs instáveis (Meta/Instagram), a prioridade de rota de mídia deve ser o servidor Hostinger (Brasil), garantindo latência mínima e maior taxa de sucesso no download iniciado pelo Facebook.
3.  **Check de Integridade Pós-Erro**: Se uma execução falhou, a próxima **DEVE** começar verificando a integridade dos arquivos na pasta `fila/` via `os.listdir()`.

## 🩺 Rotina de Health Check (Auditoria 100%)

Para garantir que o robô não entre em "estado vegetativo", siga esta rotina:

1.  **Check de Frescor**: Verifique o timestamp de `site/data.json`. Se for > 24h, o agendador falhou.
2.  **Check de Conectividade**: Rode `python -m core.arbitrator` para um produto teste.
3.  **Check de Tags**: Inspecione os links no `data.json` local para confirmar se as tags de afiliado estão presentes.
4.  **Check de Fila**: Verifique `social/fila/` para garantir que há conteúdo para os próximos dias.


---
## 🛎️ Decisões Arquiteturais (Lessons Learned 2026-02-20)

### Barra de Ofertas (Lightning Bar)
- **Status atual:** Desativada temporariamente via `display: none !important` no `style.css`.
- **Motivo:** O scraper genérico retornava produtos irrelevantes (ex: liquidificador de brinquedo) e preços sem centavos corretos.
- **Abordagem recomendada para reativação:**
  - Não usar scraping por keyword. Usar **lista curada** dos produtos já presentes nos banners do site.
  - Buscar preço via API do produto específico (PAAPI da Amazon, API do ML), não de resultados de busca.
  - Gate obrigatório de preço mínimo por categoria antes de exibir qualquer produto.

### 🎨 Conservadorismo de Visual (The Minimalist Look)
- **Protocolo de Não-Interferência (2026-03-10):** Muitos elementos (ex: barra de busca no Hero, Assets 3D) podem estar ocultos intencionalmente via CSS (`display: none !important`) para manter uma estética minimalista em produção. 
- **Regra de Ouro:** Nunca "corrija" a visibilidade de elementos estruturais sem confirmação explícita do usuário, mesmo que pareçam "quebrados" no ambiente de staging. Foque exclusivamente no escopo do hotfix solicitado.

### 🗓️ Limpeza de Campanhas Sazonais
- **Ocultar > Deletar:** Prefira esconder seções sazonais (ex: Dia da Mulher, Natal) via `style="display: none;"` no HTML e comentários no JS/CSS. Isso preserva a estrutura para o ano seguinte e evita quebras de referências em scripts automatizados.

## 🤖 Mission Statement for AI Agents
> "Your role is to protect the integrity of the Titanium ecosystem. Priority 1 is a functional site with working affiliate links. Priority 2 is automation freshness. Priority 3 is performance."

**When in doubt, fallback to a working static state.**
