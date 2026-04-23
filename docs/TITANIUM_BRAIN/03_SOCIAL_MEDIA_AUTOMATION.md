# 📸 Titanium Brain: Social Media Automation

This document details how Titanium maintains a social presence on Instagram without manual intervention.

## 🤖 The Social Bot Orchestrator
Implemented in `social/core/bot.py`.

The bot operates in two distinct modes:

### 1. Curadoria Mode (Priority)
- **Queue**: Looks for files in `social/fila/`.
- **Logic**: Any image (`.jpg`, `.png`) or video (`.mp4`) placed here is treated as a priority post.
- **Workflow (v2.3.0 - Datafeed 100K Support)**:
    - Seleciona **1 item** da fila por ciclo de execução para postagem.
    - **Datafeed Scale-up**: O robô agora se abastece do pool de 100K produtos do Datafeed via `social/queue_csv_products.py`.
    - **Smart Deduplication**: O bot verifica todos os títulos em `social/postados/` para garantir que o Instagram nunca poste o mesmo achadinho duas vezes.
    - **Image Quality**: Utiliza `core/shopee_api.py` para buscar imagens de alta qualidade via GraphQL oficial antes de compor a arte.
    - A imagem é convertida automaticamente em um vídeo de 5 segundos (Reels) usando o efeito Ken Burns (`social/utils/video_utils.py`).
    - Lê metadados de arquivos `.json` vinculados para preencher títulos, preços e o link de afiliado rastreável.
    - **Resolution Standard**: Always use **720p (720x1280)** for Reels to ensure Meta processing success.
    - Post-success: Moves image/video and its JSON metadata to `social/postados/`.

### 2. Category Fallback Mode (Automated)
- **Trigger**: Used when the queue is empty.
- **Schedule**:
    - **Morning**: Shopee Daily Deals.
    - **Afternoon**: Shopee New Arrivals.
    - **Evening**: Shopee Flash Deals.
- **Status**: Amazon and Mercado Livre fallbacks are currently **DEACTIVATED** (Shopee Exclusive Era).
- **Logic**: Selects the best category banner and the top-discounted product for that store.
- **CI/CD Sync**: The automated workflow in GitHub Actions uses a `git pull --rebase` strategy before pushing archival changes to avoid conflicts between local and remote environments.

### 3. Fila Agendada (Scheduled Manifesto)
- **File**: `social/fila/schedule.json`.
- **Logic**: Defines exactly which image/video will be posted on specific dates.
- **Maintenance**: Requires periodic updates (at least once a week) to ensure the queue never dries up. If the current date is not in the manifesto, the automation will skip the post to avoid errors.
- **Manual Overrides**: For special dates (e.g., International Women's Day), a dedicated script `post_manual_X.py` can be used. These scripts should follow the `ResilientUploader` protocol and manually archive the image after success to keep the queue in sync.

## 🎞️ Media Processing
Titanium prioritizes **Reels** over static images because of higher algorithmic reach.
- **Ken Burns Effect**: Static images are animated with subtle zoom/pan.
- **720p Rule**: Videos are encoded/resized to 720p (Original Size) to ensure instant cloud transcoding.
- **Resilient Upload Strategy (v1157 — Tri-Layer Defense)**:
    1.  **Prioridade 1: Hostinger (FTP)** -> `guiadodesconto.com.br/social/`. Esta rota é mais estável para os servidores do Meta devido à proximidade geográfica e menor latência.
    2.  **Verificação Meta-Realista**: Após upload FTP, `_verify_link_for_meta()` simula o crawler do Facebook (`User-Agent: facebookexternalhit/1.1`) com GET completo, valida `Content-Type` e tamanho mínimo. Se o WAF do Hostinger bloquear → fallback automático.
    3.  **Prioridade 2: ImgBB** (Fallback). Ativado automaticamente quando a verificação Meta falha no Hostinger, ou quando o container retorna erro 9004.
    4.  **Retry 9004**: Se o container falhar com erro 9004 mesmo após verificações, o `post_scheduled_feed.py` retenta com ImgBB (`force_cloud=True`) sem intervenção humana.
    5.  **Conversão Segura**: O script obrigatoriamente gera arquivos temporários com nomes únicos (`temp_...`) para evitar destruir o arquivo original da fila em caso de erro no processo de upload.

## 🛠️ Troubleshooting: Falhas Comuns
### 1. Erro 9004 — WAF Hostinger Bloqueando Meta (v1157)
- **Sintoma**: Upload FTP sucede, `_verify_link()` retorna 200, mas Meta rejeita com `error_subcode: 2207052`.
- **Causa Raiz**: O WAF do Hostinger (LiteSpeed / Imunify360) bloqueia intermitentemente os crawlers do Facebook por IP ou User-Agent, retornando HTML ao invés da imagem.
- **Solução Automática (Defesa em 3 Camadas)**:
    1.  **Verificação Meta-realista**: `_verify_link_for_meta()` simula o crawler do Facebook com `User-Agent: facebookexternalhit/1.1`, faz GET completo, valida `Content-Type` e tamanho mínimo.
    2.  **Auto-fallback ImgBB**: Se a verificação Meta falha, o upload é refeito automaticamente via ImgBB.
    3.  **Retry 9004**: Se o container falhar com erro 9004 mesmo após verificação, o `post_scheduled_feed.py` retenta com ImgBB (`force_cloud=True`).

### 2. File Not Found (Encoding Issues)
- **Causa**: Caminhos com acentos (ex: "Área de Trabalho") no Windows.
- **Solução**: O script agora utiliza busca dinâmica via `os.listdir()` e matching em lowercase para garantir que o arquivo seja encontrado independente do encoding do sistema operacional.

## 🔗 Instagram Graph API Orchestration
O `InstagramClient` (`social/core/instagram_client.py`) handles an optimized 3-step publishing process:
1.  **Media Container**: Sends the public URL to Meta.
2.  **Smart Polling (v1158)**:
    - Waits for Meta's cloud processing.
    - After 20 consecutive `null` status polls, the client assumes the video is ready and proceeds to prevent indefinite timeouts.
3.  **Publication (Resilient Publish)**: Triggers `media_publish` with a 5-attempt retry loop to handle the "Media ID is not available" transient error.

---
## 🎯 DM Automation & Link Injection Strategy (MANDATORY RULE)
Titanium uses a 24/7 standalone PHP Bot (`bot_instagram.php`) deployed on Hostinger via Cron Job to monitor comments and send direct messages (DMs) with affiliate links.

1. **Rule for the AI Copywriter**: **EVERY SINGLE POST** generated for Instagram MUST contain a unique internal tracking hashtag in the caption (e.g., `#ofertaX`, `#panela1`, `#drone4k`). This hashtag can be placed subtly at the end of the text.
2. **Rule for the Operator (Human)**: Every time a new post is scheduled or published, update the `ofertas.json` file on Hostinger via FTP running: `python -m social.upload_ofertas`
   - Example format: `{"#drone4k": "https://shopee.com.br/...", "#default": "https://guiadodesconto.com.br"}`
3. **Execution**: The `bot_instagram.php` reads the caption of the post being commented on, extracts the hashtag, lookups the `ofertas.json` dictionary, and sends the corresponding link straight to the user's Inbox via Meta Graph API edge `/{PAGE_ID}/messages`.

### 📂 Arquivos do Robô de DM no Servidor (Hostinger)
- **`/bot_instagram.php`** (raiz do servidor): O cérebro do robô. Monitora os últimos 6 posts, detecta gatilhos nos comentários e dispara DM + resposta pública.
- **`/ofertas.json`** (raiz do servidor): O dicionário de links. Mapeia cada hashtag ao seu link de produto. Deve ser atualizado a cada novo post.
- **`/comment_responses.json`** (raiz do servidor): Log de IDs de comentários já respondidos. Nunca deletar — evita duplo disparo.

### 🔑 Gatilhos de Disparo do Robô
Comentários que contêm qualquer uma das palavras abaixo ativam o envio do DM:
`"eu quero"`, `"quero"`, `"link"`, `"valor"`, `"preco"`, `"eu quero o link"`

### ⚠️ Regra de Atualização do Token — Titanium Token Manager (CRÍTICO)

O sistema usa um **Page Access Token** (token permanente ♾️) gerado a partir de um Long-Lived User Token. Este token **não expira** enquanto o App "Robo Titanium Social" estiver ativo.

#### 🔄 Como renovar (quando necessário):
```powershell
# Rodar da raiz do projeto
python -m social.titanium_token_manager
```
O script faz **tudo automaticamente**:
1. Pega o `IG_ACCESS_TOKEN` atual do `.env`
2. Troca pelo **Long-Lived User Token** (60 dias) via `/oauth/access_token`
3. Usa o Long-Lived Token para buscar o **Page Access Token** (nunca expira) via `/me/accounts`
4. Atualiza o `.env` local
5. Atualiza o `bot_instagram.php` local (`social/bot_instagram.php`)
6. Faz upload automático para o servidor Hostinger via FTP

#### 📋 Credenciais do App Meta (necessárias para o script):
- **App ID**: armazenado no GitHub Secrets / `.env` local (`META_APP_ID`)
- **App Secret**: armazenado no `social/titanium_token_manager.py` — **NÃO commitar este arquivo com secrets no GitHub**
- **Page ID**: armazenado no GitHub Secrets / `.env` local (`META_PAGE_ID`)
- **IG Business ID**: armazenado no GitHub Secrets / `.env` local (`IG_BUSINESS_ID`)

#### 🩺 Sintomas de Token Expirado:
- `bot_instagram.php` para de enviar DMs
- Script Python retorna `OAuthException code: 190, subcode: 463`
- O `social/core/bot.py` falha na criação do container

**Último token renovado**: 2026-03-21 (Page Token permanente ativo)

---
## 🎨 Posts com Modelos IA

Fluxo completo para criar e publicar posts de moda com modelos geradas por Inteligência Artificial:

### Passo 1: Geração das Modelos IA
- Usar o assistente para criar imagens com prompts de **moda premium, alta costura e iluminação cinematográfica**.
- Salvas na pasta de trabalho do assistente para uso nos scripts de composição.

### Passo 2: Composição das Artes Finais
- Script: `social/automate_fashion_carousel.py`
- Lê as imagens da IA e sobrepõe **preço (badge Shopee laranja)**, **título do produto** e **logo da loja**.
- **Output**: Salva as artes em **`social/fila/`** para processamento pelo bot.
- Dimensões: **1080x1080 (1:1)** — formato padrão do Instagram.

### Passo 3: Upload e Publicação (Automático via CI/CD)
- O `social/core/bot.py` pega 1 item da fila por ciclo, converte em Reel (Ken Burns) e publica.
- A **legenda DEVE conter a hashtag de DM** (ex: `#look_shopee1`) para que o robô de DM funcione.
- Para publicação manual: `python -m social.core.bot` (rodar da raiz do projeto).

### Hashtags Atualmente Mapeadas no ofertas.json
| Hashtag | Destino |
| :--- | :--- |
| `#look_shopee1` | guiadodesconto.com.br |
| `#pantalona` | Link Shopee direto |
| `#blazer` | Link Shopee direto |
| `#vestido` | Link Shopee direto |
| `#perfume` | Link Shopee direto |
| `#bolsa` | Link Shopee direto |
| `#relogio` | Link Shopee direto |
| `#make` | Link Shopee direto |
| `#default` | guiadodesconto.com.br |

---
## 🤖 Python Comment Bot (Active Monitor)
Titanium usa `social/bot_comentario_brick3d.py` para monitoramento local de alta prioridade.

### 🚀 Features:
- **Keyword Trigger**: Detects "QUERO", "LINK", "VALOR".
- **Dual Action**:
  1.  **Public Reply**: Comments back on the user's thread to increase post engagement.
  2.  **Private DM**: Sends the long-format pitch + affiliate link directly to the user's inbox.
- **Persistence**: Uses `state/brick3d_replied_users.json` to ensure nobody receives a duplicate DM.
- **Interval**: Set to 60s to stay under Meta's rate-limit thresholds for automated actions.

---
*Atualizado em: 23/04/2026 - Versão: v3.8.0 (Nuclear Shield Logic Applied to Queue)*
