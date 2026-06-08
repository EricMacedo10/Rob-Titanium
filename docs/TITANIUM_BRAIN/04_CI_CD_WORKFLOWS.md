# 🚀 Titanium Brain: CI/CD & Deployment (v5.2.0-Stable)

Este documento mapeia a espinha dorsal de automação que mantém a Boutique Titanium viva e atualizada 24/7.

---

## 🤖 1. GitHub Actions: O Pulso do Sistema

O Titanium utiliza seis fluxos de trabalho (Workflows) localizados em `.github/workflows/`. Todos operam sob o regime de **Concorrência Controlada** (impedindo colisões) e possuem o **Shield Gate** mandatório.

| Workflow | Gatilho (Trigger) | Ação Principal |
| :--- | :--- | :--- |
| `shopee-gold-exclusive.yml` | Cron (3x ao dia) | Atualiza a vitrine principal. **Shield Gate Active.** |
| `titanium_radar_auto.yml` | Cron (4 em 4 dias) | Roda a IA para o Radar de Tendências. **Shield Gate Active.** |
| `titanium_blog_auto.yml` | Cron (Domingos) | Gera e publica o editorial semanal. **Shield Gate Active.** |
| `titanium_social_auto.yml` | Cron (4x ao dia) | Gera artes estáticas e posta no IG. **Shield Gate Active.** |
| `titanium_reels_auto.yml` | Cron (1x ao dia) | **NEW:** Gera vídeos (Reels/Stories) de Moda e Beleza. **Auto-Commits postados/ e ofertas.json.** |
| `titanium_specialist_auto.yml`| Cron (2x ao dia) | Atualiza a Roleta Premium. **Shield Gate Active.** |
| `sensual_auto_update.yml` | Cron (4x ao dia) | Automação isolada da vertical Íntima. **Shield Gate & Auto-FTP Active.** |
| `sensual_specialist_auto.yml` | Cron (2x ao dia) | Curadoria da vertical Íntima. **Shield Gate & Auto-FTP Active.** |
| `titanium_sales_tracker.yml` | Cron (A cada 2h) | Monitoramento financeiro da Shopee via API GraphQL. Envia alertas de vendas (Plim!) via Telegram Bot. |

---

## 🔐 2. Gestão de Segredos (GitHub Secrets)

Para que as automações funcionem, os seguintes segredos **DEVEM** estar configurados no GitHub:

### Servidor & CDN:
- `FTP_HOST`, `FTP_USER`, `FTP_PASS`: Credenciais da Hostinger (apenas para arquivos do site estático).
- `IMGBB_API_KEY`: Necessário para o bypass da CDN `tmpfiles.org` na postagem de mídias (Reels e Imagens) no Instagram via Actions (porta 21 de FTP é bloqueada pela Github).

### APIs de IA e Dados:
- `SHOPEE_APP_ID`, `SHOPEE_SECRET`: Autenticação na API de Afiliados Shopee.
- `SHOPEE_DATAFEED_URLS`: URLs do Datafeed oficial para extração em massa (Formato: `url1 | url2`).
- `DEEPSEEK_API_KEY`: Acesso ao cérebro de IA principal (Moda).
- `DEEPSEEK_API_KEY_SENSUAL`: Chave dedicada para a vertical de Bem-Estar Íntimo (Controle de Custos).

### Redes Sociais (Instagram/Facebook) & Telegram:
- `IG_ACCESS_TOKEN`, `IG_BUSINESS_ID`, `PAGE_ID`: Tokens necessários para automação de postagens e DMs na Graph API da Meta.
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`: Acesso à API do Telegram para o disparo de notificações financeiras e de vendas em tempo real.

---

## 📦 3. Mecânica de Deploy & Dependências

### Gestão de Bibliotecas:
- O sistema utiliza o arquivo `requirements.txt` para garantir que bibliotecas como `beautifulsoup4` e `Pillow` estejam sempre presentes no ambiente de nuvem.
- **Protocolo**: O Workflow executa `pip install -r requirements.txt` antes de rodar os scripts core.

### Sincronização Atômica & Deploy Cirúrgico:
O sistema utiliza um motor de deploy ultra-resiliente:
1.  **Deploy Cirúrgico (v5.2.0)**: Otimização para workflows de nicho (Sensual, Radar, Roleta). O sistema realiza o upload **apenas do arquivo modificado**, reduzindo o tempo de deploy de 35 minutos para 30 segundos e eliminando travamentos por timeout de FTP.
2.  **Pathspec Guard (Fix #128)**: Workflow do Blog corrigido para apontar explicitamente para `site/index.html`, evitando o erro fatal de git.
3.  **Nuclear Shield Audit Gate**: Executa `infra/shield.py` para validar e corrigir 100% das tags de afiliado antes do upload.
4.  Realiza o upload via FTP apenas dos dados (`data.json`, `data_sensual.json`, etc) no dia a dia.
5.  Sincroniza assets estruturais (`index.html`, `js`, `css`) apenas em deploys manuais ou de hotfix.

### Deploy do Social Bot & Price Integrity *(v5.1.0 - 09/05/2026)*:
O fluxo de postagem social (`titanium_social_auto.yml`) agora é totalmente autossuficiente:
1.  **Price Parser Centralizado**: `_parse_price()` no `image_generator.py` e lógica espelhada no `bot.py` garantem que preço na imagem e na legenda sejam sempre idênticos (padrão BR: R$ 38,98).
2.  **Auto-Hashtagging**: O bot gera `#titanium_ID` automaticamente em cada post.
3.  **Auto-Sync via GitHub Raw**: O dicionário `ofertas.json` deixou de usar FTP. Ele é salvo localmente.
4.  **Auto-Commit**: O `git-auto-commit` salva o novo dicionário no GitHub para persistência histórica, servindo também como CDN para o `bot_instagram.php` ler.
5.  **DM Bot**: `bot_instagram.php` responde automaticamente com link rastreado + preview do produto.
6.  **Deep Database Search**: O robô utiliza `data.json` como backup inteligente para garantir 100% de match.

**Uso Manual**: `python -m social.deploy_bot` ou `python -m social.upload_database`.

---

## 🛡️ 4. Protocolo de Blindagem Antigravity

Para garantir que o site nunca "volte atrás" no tempo ou no design:
- **Git Push First**: Mudanças visuais no `index.html` devem ser enviadas ao GitHub ANTES da automação rodar.
- **Structural Locking**: O robô principal (`orchestrator.py`) é bloqueado para NÃO sobrescrever arquivos de layout em produção por acidente.
- **Fail-Safe Monitoring**: Se o GitHub Actions falhar, o site em produção permanece intacto e funcional com os últimos dados válidos.

### 🛡️ Prevenção de Falhas Silenciosas (Lesson Learned 2026-06-02)
- **Causa**: A ausência de variáveis de ambiente (`SHOPEE_APP_ID`, `SHOPEE_SECRET`) no workflow fazia com que scripts como `automate_reels.py` falhassem na extração de imagens, porém, ao invés de acionar um erro crítico, o script encerrava usando `return` (Exit 0).
- **Consequência**: O GitHub Actions interpretava a execução como bem-sucedida, não gerava alertas de falha, e o passo de auto-commit ignorava o fim da fila, resultando em uma **Falha Silenciosa** sem geração de conteúdo.
- **Protocolo Sênior**: Todos os scripts do CI/CD devem obrigatoriamente chamar `sys.exit(1)` ao capturar exceções críticas (ex: falha de API ou erro na imagem), forçando o workflow a falhar explicitamente e acionar os alertas por e-mail (ver `05_AI_OPERATIONAL_PROTOCOLS.md`).

---
**IA Titanium**
*Atualizado em: 08/06/2026 - Versão: v5.8.0-SalesTracker (Integração Shopee GraphQL e Telegram Bot)*
