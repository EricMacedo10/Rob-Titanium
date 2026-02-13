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
- `MELI_REFRESH_TOKEN`: For Mercado Livre API continuity.

## 📦 Deployment Mechanics
Implemented in [deploy.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/infra/deploy.py).

### Atomic Synchronization
Titanium avoids partial site updates. The deployer:
1.  Iterates through local `/site` files.
2.  Compares sizes or hashes (depending on the run mode).
3.  Uploads changed files.
4.  **Verification**: Performs a health check on `data.json` post-upload to ensure the site's "Heart" is beating.

### Sync-Safe Archival (Automation)
For workflows that write back to the repository (e.g., `post-scheduled`), a `git pull --rebase` strategy is used before pushing. This prevents archival failures caused by transient conflicts between automated runs and manual commits.

## 🛡️ Staging vs Production
- **Staging**: Hosted in a protected subdirectory (via `.htaccess`). Used for validating new scraper logic.
- **Production**: Main domain. Automated updates only target production once staging tests pass.

---
> [!WARNING]
> Never manually edit `data.json` on the server. Always update the local manual targets in `core/settings.py` or the `state/` directory and let the CI/CD handle the sync.
