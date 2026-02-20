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

| Symptom | Probable Cause | Action |
| :--- | :--- | :--- |
| **Site Empty** | `data.json` is 0KB or invalid. | Check `orchestrator.log` for Scraper blocks. |
| **Links not tracking** | Tag normalized incorrectly. | Check `normalizeStore` logic in `app.js`. |
| **ML Search Failing** | Token Expired and Refresh failed. | Delete `state/meli_tokens.json` to force re-auth. |
| **Social Bot not posting** | IG Container Timeout. | Increase `max_attempts` in `instagram_client.py`. |

## 🩺 Rotina de Health Check (Auditoria 100%)

Para garantir que o robô não entre em "estado vegetativo", siga esta rotina:

1.  **Check de Frescor**: Verifique o timestamp de `site/data.json`. Se for > 24h, o agendador falhou.
2.  **Check de Conectividade**: Rode `python -m core.arbitrator` para um produto teste.
3.  **Check de Tags**: Inspecione os links no `data.json` local para confirmar se as tags de afiliado estão presentes.
4.  **Check de Fila**: Verifique `social/fila/` para garantir que há conteúdo para os próximos dias.


---
## 🤖 Mission Statement for AI Agents
> "Your role is to protect the integrity of the Titanium ecosystem. Priority 1 is a functional site with working affiliate links. Priority 2 is automation freshness. Priority 3 is performance."

**When in doubt, fallback to a working static state.**
