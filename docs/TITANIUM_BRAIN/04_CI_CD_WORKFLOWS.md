# 🚀 Titanium Brain: CI/CD & Deployment

This document maps the automation backbone that keeps Titanium updated 24/7.

## 🤖 GitHub Actions: The Pulse

Titanium uses three primary workflows located in `.github/workflows/`:

| Workflow | Trigger | Action |
| :--- | :--- | :--- |
| `update-offers.yml` | Cron (Hourly) | Runs `core/orchestrator.py` to refresh `data.json`. |
| `deploy-site.yml` | Push to `main` | Synchronizes the `/site` folder to Hostinger via FTP. |
| `post-scheduled` | Cron (Daily) | Triggers the Social Bot daily cycle. |

## 🔑 Secret Management (GitHub Secrets)

The following secrets are mandatory for full automation:
- `FTP_HOST`, `FTP_USER`, `FTP_PASS`: Credentials for Hostinger.
- `GROQ_API_KEY`: For AI curation.
- `IG_ACCESS_TOKEN`, `IG_BUSINESS_ID`: For social posting.
- `MELI_CLIENT_ID`, `MELI_CLIENT_SECRET`: Official Mercado Livre API App credentials.
- `MELI_REFRESH_TOKEN`: The primary token for ML OAuth 2.0 continuity.

## 📦 Deployment Mechanics
Implemented in [deploy.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/infra/deploy.py).

### Atomic Synchronization
Titanium avoids partial site updates. The deployer:
1.  Iterates through local `/site` files.
2.  Compares sizes or hashes (depending on the run mode).
3.  Uploads changed files.
4.  **Verification**: Performs a health check on `data.json` post-upload to ensure the site's "Heart" is beating.

### Manual Force-Sync (Hotfixes)
Para correções de emergência que afetam apenas a interface (HTML/CSS/JS), utilize o script dedicado:
- **Entry point**: `python infra/force_asset_upload.py`
- **Logic**: Sincroniza apenas assets estruturais sem rodar os scrapers de produto. Ideal para Go-Live visual após validação em Staging.

### Sync-Safe Archival (Automation)
For workflows that write back to the repository (e.g., `post-scheduled`), a `git pull --rebase` strategy is used before pushing. This prevents archival failures caused by transient conflicts between automated runs and manual commits.

### Deployment Security Protocol (Safe Sync)
To prevent accidental production outages, the following protocol is enforced:
1.  **Environment Lock**: The `ENV_MODE` in `.env` must be explicitly verified before any manual or automated deploy.
2.  **Staging-First Validation**: Production deploys are restricted unless a successful synchronization and verification cycle has been completed in the `/teste` environment during the same session.
3.  **Atomic Assets**: Script updates (like `app.js`) must be accompanied by version bumps in `index.html` to prevent stale cache execution.
4.  **Anti-Reversion Protocol (Critical)**: Modificações locais em arquivos estruturais (`index.html`, `js/app.js`, `css/style.css`) **DEVEM** obrigatoriamente ser "commitadas" e enviadas via `git push origin main` ANTES do próximo ciclo automático do Github Actions. Caso contrário, quando o workflow acordar de hora em hora, ele usará a versão antiga em nuvem como fonte da verdade, fazendo FTP por cima do site novo e revertendo o design para a versão desatualizada.
5.  **Strict Asset Separation (Data-Only)**: Em produção, o robô `orchestrator.py` foi blindado para atualizar APENAS e EXCLUSIVAMENTE o `data.json` e o `notifications.json`. Essa blindagem garante que atualizações de escraprons não esmaguem o design HTML/CSS da página.Mudanças na interface gráfica são exclusivas de deploys manuais de código Git.
6.  **Atomic Assets & Versioning**: Ao realizar o deploy de correções estruturais (ex: remoção dos caminhões), é mandatório alinhar o `index.html` de produção com o `index_staging.html` aprovado para evitar reversões por cache ou rotinas automáticas paralalelas.
7.  **Unicode Safety (Deploy)**: Scripts de deploy (`infra/deploy.py`) devem evitar o uso de Emojis ou caracteres Unicode não-ASCII em logs de console para prevenir `UnicodeEncodeError` em terminais Windows/CP1252.

## 🛡️ Staging vs Production
- **Staging**: Subdomínio `teste.guiadodesconto.com.br` → mapeado para a pasta `/teste` na raiz FTP (`u534624268.guiadodesconto`). Usado para validar novas lógicas de scraper e features experimentais do frontend. O orchestrator em modo `ENV_MODE=STAGING` envia apenas: `data.json`, `notifications.json`, `index_staging.html`, `js/app.js` e `css/style.css` para `/teste/`. **Nunca altera `index.html` de produção.**
- **Production**: Domínio raiz `guiadodesconto.com.br` → pasta `/` na raiz FTP. Recebe apenas releases estáveis e aprovados no staging.

---
> [!WARNING]
> Never manually edit `data.json` on the server. Always update the local manual targets in `core/settings.py` or the `state/` directory and let the CI/CD handle the sync.
