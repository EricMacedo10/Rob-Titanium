# 🚀 Titanium Brain: CI/CD & Deployment (v3.9.0 - Nuclear)

Este documento mapeia a espinha dorsal de automação que mantém a Boutique Titanium viva e atualizada 24/7.

---

## 🤖 1. GitHub Actions: O Pulso do Sistema

O Titanium utiliza três fluxos de trabalho principais (Workflows) localizados em `.github/workflows/`:

| Workflow | Gatilho (Trigger) | Ação Principal |
| :--- | :--- | :--- |
| `shopee-gold-exclusive.yml` | Cron (3x ao dia) | Atualiza a vitrine de ofertas principal (Maestro). |
| `titanium_radar_auto.yml` | Cron (4 em 4 dias) | Roda a IA DeepSeek para atualizar o Radar de Tendências. |
| `titanium_blog_auto.yml` | Cron (Domingos) | Gera e publica o artigo editorial da semana (SEO). |
| `titanium_social_post.yml` | Cron (4x ao dia) | Gera artes e publica automaticamente no Instagram. |
| `shopee_specialist_roleta.yml`| Cron (2x ao dia) | Atualiza a Seleção da Especialista (Fundo Platinum). |
| `sensual_auto_update.yml` | Cron (4x ao dia) | Automação isolada da Boutique Sensual (Staging). |

---

## 🔐 2. Gestão de Segredos (GitHub Secrets)

Para que as automações funcionem, os seguintes segredos **DEVEM** estar configurados no GitHub:

### Servidor:
- `FTP_HOST`, `FTP_USER`, `FTP_PASS`: Credenciais da Hostinger.

### APIs de IA e Dados:
- `SHOPEE_APP_ID`, `SHOPEE_SECRET`: Autenticação na API de Afiliados Shopee.
- `SHOPEE_DATAFEED_URLS`: URLs do Datafeed oficial para extração em massa (Formato: `url1 | url2`).
- `DEEPSEEK_API_KEY`: Acesso ao cérebro de IA principal (Moda).
- `DEEPSEEK_API_KEY_SENSUAL`: Chave dedicada para a vertical de Bem-Estar Íntimo (Controle de Custos).

---

## 📦 3. Mecânica de Deploy & Dependências

### Gestão de Bibliotecas:
- O sistema utiliza o arquivo `requirements.txt` para garantir que bibliotecas como `beautifulsoup4` e `Pillow` estejam sempre presentes no ambiente de nuvem.
- **Protocolo**: O Workflow executa `pip install -r requirements.txt` antes de rodar os scripts core.

### Sincronização Atômica (`sync_production_v12.py`):
O sistema utiliza um script inteligente de sincronização que:
2.  **Nuclear Shield Audit Gate**: Executa `infra/shield.py` para validar e corrigir 100% das tags de afiliado antes do upload.
3.  Realiza o upload via FTP apenas dos dados (`data.json`) no dia a dia.
4.  Sincroniza assets estruturais (`index.html`, `js`, `css`) apenas em deploys manuais ou de hotfix.

### Deploy do Social Bot & Hybrid Intelligence *(v2.2.1 - 02/05/2026)*:
O fluxo de postagem social (`titanium_social_auto.yml`) agora é totalmente autossuficiente:
1.  **Auto-Hashtagging**: O bot gera `#titanium_ID` automaticamente em cada post.
2.  **Auto-Sync**: Atualiza o `social/ofertas.json` local e faz o upload imediato via FTP para o servidor.
3.  **Auto-Commit**: Salva o novo dicionário no GitHub para persistência histórica.
4.  **Deep Database Search**: O robô de resposta (`bot_instagram.php`) agora utiliza o `data.json` da raiz como backup inteligente para garantir 100% de match, mesmo em posts manuais.

**Uso Manual**: `python -m social.deploy_bot` ou `python -m social.upload_database` para sincronia total.

---

## 🛡️ 4. Protocolo de Blindagem Antigravity

Para garantir que o site nunca "volte atrás" no tempo ou no design:
- **Git Push First**: Mudanças visuais no `index.html` devem ser enviadas ao GitHub ANTES da automação rodar.
- **Structural Locking**: O robô principal (`orchestrator.py`) é bloqueado para NÃO sobrescrever arquivos de layout em produção por acidente.
- **Fail-Safe Monitoring**: Se o GitHub Actions falhar, o site em produção permanece intacto e funcional com os últimos dados válidos.

---
---
**IA Titanium**
*Atualizado em: 02/05/2026 - Tecnologia Shopee Datafeed 100K + Nuclear Shield v3.9 + Hybrid Intelligence v2.2*

