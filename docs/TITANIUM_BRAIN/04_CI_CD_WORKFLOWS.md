# 🚀 Titanium Brain: CI/CD & Deployment (v2026 - Elite)

Este documento mapeia a espinha dorsal de automação que mantém a Boutique Titanium viva e atualizada 24/7.

---

## 🤖 1. GitHub Actions: O Pulso do Sistema

O Titanium utiliza três fluxos de trabalho principais (Workflows) localizados em `.github/workflows/`:

| Workflow | Gatilho (Trigger) | Ação Principal |
| :--- | :--- | :--- |
| `shopee-gold-exclusive.yml` | Cron (3x ao dia) | Atualiza a vitrine de ofertas principal via API Oficial. |
| `titanium_radar_auto.yml` | Cron (4 em 4 dias) | Roda o motor de IA para mudar o Radar de Tendências. |
| `titanium_blog_auto.yml` | Cron (Domingos) | Gera e publica o artigo editorial da semana. |

---

## 🔐 2. Gestão de Segredos (GitHub Secrets)

Para que as automações funcionem, os seguintes segredos **DEVEM** estar configurados no GitHub:

### Servidor:
- `FTP_HOST`, `FTP_USER`, `FTP_PASS`: Credenciais da Hostinger.

### APIs:
- `SHOPEE_APP_ID`, `SHOPEE_SECRET`: Autenticação na API de Afiliados.
- `DEEPSEEK_API_KEY`: Acesso ao cérebro de IA.

---

## 📦 3. Mecânica de Deploy

### Sincronização Atômica (`sync_production_v12.py`)
O sistema utiliza um script inteligente de sincronização que:
1.  Faz o checkout do código mais recente no GitHub.
2.  Determina o modo de execução (`PRODUCTION`).
3.  Compara o hash dos arquivos locais com o servidor (se necessário).
4.  Realiza o upload via FTP apenas dos dados necessários, garantindo a integridade do site.

---

## 🛡️ 4. Protocolo de Blindagem Antigravity

Para garantir que o site nunca "volte atrás" no tempo ou no design:
- **Git Push First**: Mudanças visuais no `index.html` devem ser enviadas ao GitHub ANTES da automação rodar.
- **Pythonpath Fix**: Todas as Actions utilizam a variável `PYTHONPATH: .` para garantir que os módulos internos do sistema sejam carregados sem erros no ambiente Linux do GitHub.
- **Fail-Safe Monitoring**: Caso um ciclo falhe, ele não afeta o site em produção (o site continua online com os dados da última atualização bem-sucedida).

---
*Atualizado em: 11/04/2026 - Documento Técnico de Automação Elite*
