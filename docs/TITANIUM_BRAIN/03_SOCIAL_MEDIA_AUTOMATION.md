# 📸 Titanium Brain: Social Media Automation

This document details how Titanium maintains a social presence on Instagram without manual intervention.

## 🤖 The Social Bot Orchestrator
Implemented in [bot.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/social/core/bot.py).

The bot operates in two distinct modes:

### 1. Curadoria Mode (Priority)
- **Queue**: Looks for files in `social/fila/`.
- **Logic**: Any image (`.jpg`, `.png`) or video (`.mp4`) placed here is treated as a priority post.
- **Workflow (v2.0.0 - Cluster Mode)**:
    - Agrupa automaticamente até **10 itens** da fila para criar um **Carrossel**.
    - Se houver apenas 1 item, converte automaticamente para Reels (Ken Burns).
    - Lê metadados de arquivos `.json` vinculados (mesmo nome da imagem) para preencher títulos e preços na legenda.
    - Se for uma imagem única, ela é convertida em um vídeo de 5 segundos (Reels) usando o efeito Ken Burns (`social/utils/video_utils.py`).
    - **Resolution Standard**: Always use **720p (720x1280)** for Reels. Higher resolutions (1080p) often cause Meta processing timeouts quando postado via API.
    - Post-success: Moves image/video and its JSON metadata to `social/postados/`.
    - **CI/CD Compliance**: Usa `sys.exit(0)` para sucesso e `sys.exit(1)` para falha, permitindo que o GitHub Actions reporte erros de postagem fielmente.

### 3. Fila Agendada (Scheduled Manifesto)
- **File**: `social/fila/schedule.json`.
- **Logic**: Defines exactly which image/video will be posted on specific dates.
- **Maintenance**: Requires periodic updates (at least once a week) to ensure the queue never dries up. If the current date is not in the manifesto, the automation will skip the post to avoid errors.
- **Manual Overrides**: For special dates (e.g., International Women's Day), a dedicated script `post_manual_X.py` can be used. These scripts should follow the `ResilientUploader` protocol and manually archive the image after success to keep the queue in sync.

### 2. Category Fallback Mode (Automated)
- **Trigger**: Used when the queue is empty.
- **Schedule**:
    - **Morning**: Amazon deals.
    - **Afternoon**: Shopee deals.
    - **Evening**: Mercado Livre deals.
- **Logic**: Selects the best category banner and the top-discounted product for that store.
- **CI/CD Sync**: The automated workflow in GitHub Actions uses a `git pull --rebase` strategy before pushing archival changes to avoid conflicts between local and remote environments.

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
The [InstagramClient](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/social/core/instagram_client.py) handles a optimized 3-step publishing process:
1.  **Media Container**: Sends the public URL to Meta.
2.  **Smart Polling (v1158 — Carousel Video Fix)**: 
    - Waits for Meta's cloud processing.
    - **Fix**: Detects `is_carousel_item`. For carousel videos, Meta often returns `status_code: null`. After 20 consecutive `null` polls, the client now assumes the video is ready for private assembling and proceeds to prevent indefinite timeouts.
3.  **Publication (Resilient Publish)**: Triggers `media_publish` with a 5-attempt retry loop to handle the "Media ID is not available" transient error commonly seen in mixed carousels.

---
## 🎭 Mixed Carousels (Photo + Video — New 2026-03-27)
Titanium now supports mixed albums (up to 10 items) combining high-quality videos and static photos in the same feed post.

### 🛠️ Technical Protocol
- **Method**: `InstagramClient.post_carousel(media_items, caption)`.
- **Input Format**: 
  ```python
  media_items = [
    {"url": "...", "type": "VIDEO"},
    {"url": "...", "type": "IMAGE"},
    ...
  ]
  ```
- **Video Requirements**: Must be MP4/MOV, up to 2 minutes, ideally 1080x1080 or 4:5.
- **Hosting**: **MANDATORY FTP/Hostinger** for videos. Cloud services like ImgBB often convert to `.webp`, which Instagram REJECTS in carousel containers.

### 🏗️ Reference Implementation (Brick 3D)
- **Script**: `social/post_brick3d_carousel.py`.
- **Logic**: Orchestrates a 5-slide post (1 video + 4 images) for the Amazon/Shopee affiliate campaign. 
- **Automation**: Automatically injects the affiliate tag `af_id` (Shopee) or `tag` (Amazon) into the product URL before generating the state file.

---
## 🎯 DM Automation & Link Injection Strategy (MANDATORY RULE)
Titanium uses a 24/7 standalone PHP Bot (`bot_instagram.php`) deployed on Hostinger via Cron Job to monitor comments and send direct messages (DMs) with affiliate links.
To make the link routing intelligent and dynamic without changing the codebase:

1. **Rule for the AI Copywriter**: **EVERY SINGLE POST** generated for Instagram MUST contain a unique internal tracking hashtag in the caption (e.g., `#ofertaX`, `#panela1`, `#drone4k`). This hashtag can be placed subtly at the end of the text.
2. **Rule for the Operator (Human)**: Every time a new post is scheduled or published, the user must update the `ofertas.json` file hosted on Hostinger via FTP (ou rodar `python c:/tmp/upload_bot.py`).
   - Example format: `{"#drone4k": "https://mercadolivre.com.br/...", "#default": "https://guiadodesconto.com.br"}`
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
- **App ID**: `1834207343896407`
- **App Secret**: armazenado no `social/titanium_token_manager.py` (NÃO commitar este arquivo com secrets no GitHub)
- **Page ID**: `1032000233318987`
- **IG Business ID**: `17841480460125461`

#### 🩺 Sintomas de Token Expirado:
- `bot_instagram.php` para de enviar DMs
- Script Python retorna `OAuthException code: 190, subcode: 463`
- O `post_fashion_carousel.py` falha na criação do container

**Último token renovado**: 2026-03-21 (Page Token permanente ativo)

---
## 🎨 Carrossel com Modelos IA (Implementado em 2026-03-21)

Fluxo completo para criar e publicar carrosséis de moda com modelos geradas por Inteligência Artificial:

### Passo 1: Geração das Modelos IA
- Usar o `generate_image` tool do assistente para criar 6 imagens (1 capa + 5 looks).
- As imagens são geradas com prompts de **moda premium, alta costura e iluminação cinematográfica**.
- Salvas em: `C:/Users/ericm/.gemini/antigravity/brain/{conversation_id}/`.

### Passo 2: Composição das Artes Finais
- Script: `social/automate_fashion_carousel.py`
- Lê as imagens da IA e sobrepõe **preço (badge Shopee laranja)**, **título do produto** e **logo da loja**.
- **Output**: Salva 6 arquivos `fashion_post_00.jpg` a `fashion_post_05.jpg` em **`social/fila/`**.
- Dimensões: **1080x1080 (1:1)** — formato padrão de carrossel do Instagram.

### Passo 3: Upload e Publicação
- Script: `social/post_fashion_carousel.py`
- Usa `ResilientUploader` para fazer upload de cada imagem para `guiadodesconto.com.br/social/`.
- Usa `InstagramClient.post_carousel(image_urls, caption)` para postar o álbum.
- A **legenda DEVE conter a hashtag de DM** (ex: `#look_shopee1`) para que o robô funcione.
- Executar com: `python -m social.post_fashion_carousel` (rodar da raiz do projeto).

### Hashtags Atualmente Mapeadas no ofertas.json
| Hashtag | Destino |
| :--- | :--- |
| `#look_shopee1` | guiadodesconto.com.br |
| `#pantalona` | Link Shopee direto |
| `#blazer` | Link Shopee direto |
| `#vestido` | Link Shopee direto |
| `#perfume` | Link Amazon com tag afiliado |
| `#bolsa` | Link Amazon com tag afiliado |
| `#relogio` | Link Amazon com tag afiliado |
| `#make` | Link Amazon com tag afiliado |
| `#default` | guiadodesconto.com.br |

---
## 🤖 Python Comment Bot (Active Monitor)
While the PHP bot handles general scaling, Titanium uses `social/bot_comentario_brick3d.py` for high-priority local monitoring.

### 🚀 Features:
- **Keyword Trigger**: Detects "QUERO", "LINK", "VALOR".
- **Dual Action**:
  1.  **Public Reply**: Comments back on the user's thread to increase post engagement.
  2.  **Private DM**: Sends the long-format pitch + affiliate link directly to the user's inbox.
- **Persistence**: Uses `state/brick3d_replied_users.json` to ensure nobody receives a duplicate DM.
- **Interval**: Set to 60s to stay under Meta's rate-limit thresholds for automated actions.

---
# 📸 Titanium Brain: Social Media Automation

This document details how Titanium maintains a social presence on Instagram without manual intervention.

## 🤖 The Social Bot Orchestrator
Implemented in [bot.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/social/core/bot.py).

The bot operates in two distinct modes:

### 1. Curadoria Mode (Priority)
- **Queue**: Looks for files in `social/fila/`.
- **Logic**: Any image (`.jpg`, `.png`) or video (`.mp4`) placed here is treated as a priority post.
- **Workflow**:
    - Selects the oldest file in the queue.
    - Generates a category-aware caption via the **Copywriter**.
    - If it's an image, it converts it to a 5-second video (Reels) using the Ken Burns effect (`social/utils/video_utils.py`).
    - **Resolution Standard**: Always use **720p (720x1280)** for Reels. Higher resolutions (1080p) often cause Meta processing timeouts when posted via API.
    - Post-success: Moves the file to `social/postados/`.

### 3. Fila Agendada (Scheduled Manifesto)
- **File**: `social/fila/schedule.json`.
- **Logic**: Defines exactly which image/video will be posted on specific dates.
- **Maintenance**: Requires periodic updates (at least once a week) to ensure the queue never dries up. If the current date is not in the manifesto, the automation will skip the post to avoid errors.
- **Manual Overrides**: For special dates (e.g., International Women's Day), a dedicated script `post_manual_X.py` can be used. These scripts should follow the `ResilientUploader` protocol and manually archive the image after success to keep the queue in sync.

### 2. CSV Import Mode (Bulk Inventory)
- **Source**: `site/specialist.json` and external CSVs.
- **Logic**: O script `social/queue_csv_products.py` lê os links de produtos selecionados, valida o estoque e cria automaticamente a fila de imagens para postagem.
- **AI Copywriter (DeepSeek)**: A legenda é gerada exclusivamente pela **IA DeepSeek Chat**, focando em elegância e desejo de compra.
- **CI/CD Sync**: A branch `main` atua como fonte da verdade, sincronizando arquivos de estado (`social/state_csv.json`) para evitar postagens duplicadas entre as rodadas do GitHub Actions.

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

### 3. Postagem Duplicada / Processos Paralelos (v1159 — Lockfile API)
- **Sintoma**: O mesmo carrossel é postado 2 ou 3 vezes consecutivas.
- **Causa Raiz**: O processamento do Meta Cloud Container pode demorar até 3 minutos. Se o operador achar que a postagem travou e executar o script de postagem novamente, as requisições entrarão em concorrência, gerando publicações idênticas na mesma página.
- **Solução (Implementada em 2026-04-09)**: `InstagramClient` agora processa todas as rotinas críticas (`_create_and_publish`, `post_carousel`) usando o Decorator `@prevent_concurrent_posts`.
    - **Como funciona**: Ele crava um Lock temporário em `state/post.lock`. Se outro processo tentar publicar, ele aborta instantaneamente com erro `❌🚨 ERRO DE CONCORRÊNCIA`. O lock expira por Timeout automático após 600s para evitar travamento infinito após eventuais perdas de conexão (`Deadlocks`).

## 🔗 Instagram Graph API Orchestration
The [InstagramClient](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/social/core/instagram_client.py) handles a optimized 3-step publishing process:
1.  **Media Container**: Sends the public URL to Meta.
2.  **Smart Polling (v1158 — Carousel Video Fix)**: 
    - Waits for Meta's cloud processing.
    - **Fix**: Detects `is_carousel_item`. For carousel videos, Meta often returns `status_code: null`. After 20 consecutive `null` polls, the client now assumes the video is ready for private assembling and proceeds to prevent indefinite timeouts.
3.  **Publication (Resilient Publish)**: Triggers `media_publish` with a 5-attempt retry loop to handle the "Media ID is not available" transient error commonly seen in mixed carousels.

---
## 🎭 Mixed Carousels (Photo + Video — New 2026-03-27)
Titanium now supports mixed albums (up to 10 items) combining high-quality videos and static photos in the same feed post.

### 🛠️ Technical Protocol
- **Method**: `InstagramClient.post_carousel(media_items, caption)`.
- **Input Format**: 
  ```python
  media_items = [
    {"url": "...", "type": "VIDEO"},
    {"url": "...", "type": "IMAGE"},
    ...
  ]
  ```
- **Video Requirements**: Must be MP4/MOV, up to 2 minutes, ideally 1080x1080 or 4:5.
- **Hosting**: **MANDATORY FTP/Hostinger** for videos. Cloud services like ImgBB often convert to `.webp`, which Instagram REJECTS in carousel containers.

### 🏗️ Reference Implementation (Brick 3D)
- **Script**: `social/post_brick3d_carousel.py`.
- **Logic**: Orchestrates a 5-slide post (1 video + 4 images) for the Amazon/Shopee affiliate campaign. 
- **Automation**: Automatically injects the affiliate tag `af_id` (Shopee) or `tag` (Amazon) into the product URL before generating the state file.

---
## 🎯 DM Automation & Link Injection Strategy (MANDATORY RULE)
Titanium uses a 24/7 standalone PHP Bot (`bot_instagram.php`) deployed on Hostinger via Cron Job to monitor comments and send direct messages (DMs) with affiliate links.
To make the link routing intelligent and dynamic without changing the codebase:

1. **Rule for the AI Copywriter**: **EVERY SINGLE POST** generated for Instagram MUST contain a unique internal tracking hashtag in the caption (e.g., `#ofertaX`, `#panela1`, `#drone4k`). This hashtag can be placed subtly at the end of the text.
2. **Rule for the Operator (Human)**: Every time a new post is scheduled or published, the user must update the `ofertas.json` file hosted on Hostinger via FTP (ou rodar `python c:/tmp/upload_bot.py`).
   - Example format: `{"#drone4k": "https://mercadolivre.com.br/...", "#default": "https://guiadodesconto.com.br"}`
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
- **App ID**: `1834207343896407`
- **App Secret**: armazenado no `social/titanium_token_manager.py` (NÃO commitar este arquivo com secrets no GitHub)
- **Page ID**: `1032000233318987`
- **IG Business ID**: `17841480460125461`

#### 🩺 Sintomas de Token Expirado:
- `bot_instagram.php` para de enviar DMs
- Script Python retorna `OAuthException code: 190, subcode: 463`
- O `post_fashion_carousel.py` falha na criação do container

**Último token renovado**: 2026-03-21 (Page Token permanente ativo)

---
## 🎨 Carrossel com Modelos IA (Implementado em 2026-03-21)

Fluxo completo para criar e publicar carrosséis de moda com modelos geradas por Inteligência Artificial:

### Passo 1: Geração das Modelos IA
- Usar o `generate_image` tool do assistente para criar 6 imagens (1 capa + 5 looks).
- As imagens são geradas com prompts de **moda premium, alta costura e iluminação cinematográfica**.
- Salvas em: `C:/Users/ericm/.gemini/antigravity/brain/{conversation_id}/`.

### Passo 2: Composição das Artes Finais
- Script: `social/automate_fashion_carousel.py`
- Lê as imagens da IA e sobrepõe **preço (badge Shopee laranja)**, **título do produto** e **logo da loja**.
- **Output**: Salva 6 arquivos `fashion_post_00.jpg` a `fashion_post_05.jpg` em **`social/fila/`**.
- Dimensões: **1080x1080 (1:1)** — formato padrão de carrossel do Instagram.

### Passo 3: Upload e Publicação
- Script: `social/post_fashion_carousel.py`
- Usa `ResilientUploader` para fazer upload de cada imagem para `guiadodesconto.com.br/social/`.
- Usa `InstagramClient.post_carousel(image_urls, caption)` para postar o álbum.
- A **legenda DEVE conter a hashtag de DM** (ex: `#look_shopee1`) para que o robô funcione.
- Executar com: `python -m social.post_fashion_carousel` (rodar da raiz do projeto).

### Hashtags Atualmente Mapeadas no ofertas.json
| Hashtag | Destino |
| :--- | :--- |
| `#look_shopee1` | guiadodesconto.com.br |
| `#pantalona` | Link Shopee direto |
| `#blazer` | Link Shopee direto |
| `#vestido` | Link Shopee direto |
| `#perfume` | Link Amazon com tag afiliado |
| `#bolsa` | Link Amazon com tag afiliado |
| `#relogio` | Link Amazon com tag afiliado |
| `#make` | Link Amazon com tag afiliado |
| `#default` | guiadodesconto.com.br |

---
## 🤖 Python Comment Bot (Active Monitor)
While the PHP bot handles general scaling, Titanium uses `social/bot_comentario_brick3d.py` for high-priority local monitoring.

### 🚀 Features:
- **Keyword Trigger**: Detects "QUERO", "LINK", "VALOR".
- **Dual Action**:
  1.  **Public Reply**: Comments back on the user's thread to increase post engagement.
  2.  **Private DM**: Sends the long-format pitch + affiliate link directly to the user's inbox.
- **Persistence**: Uses `state/brick3d_replied_users.json` to ensure nobody receives a duplicate DM.
- **Interval**: Set to 60s to stay under Meta's rate-limit thresholds for automated actions.

---
> [!NOTE]
> All social activity honors the `ENV_MODE`. In `STAGING`, actual post calls are bypassed and logged to the console/logs for validation.

> [!IMPORTANT]
> Para Carrosséis Mistos, NUNCA use ImgBB (ele converte para WEBP). Use sempre o upload via FTP para manter o codec original aceito pelo Instagram.

> [!TIP]
> Se o robô de comentários parar, verifique o `state/brick3d_active_post.json`. Ele deve refletir o ID do post mais recente para que o bot saiba onde olhar.

---
## 🚀 Protocolo: Campanhas de Post Único Manual (MANDATÓRIO)
Para posts de oportunidade (links manuais com imagem única na pasta `/fila/`), o fluxo deve seguir estas etapas:

1. **Escrita do Script**: Criar script dedicado `post_[nome]_manual.py` (ex: `post_lacta_pascoa.py`).
2. **Sincronização de Links**: O script **DEVE** incluir a função `sync_ofertas()` para subir o arquivo `ofertas.json` para a raiz do servidor Hostinger antes da postagem. Isso garante que o Robô de DM (PHP) reconheça a hashtag imediatamente.
3. **Forçar Produção**: O script deve setar `os.environ["ENV_MODE"] = "PRODUCTION"` explicitamente apenas para a execução da postagem, garantindo que o link final não contenha o prefixo `/teste/`.
4. **Bot de Monitoramento**: Após o sucesso da postagem, deve ser gerado um bot de comentário específico baseado no template `bot_comentario_pantalona.py`, salvando o `state` em um `.json` único para evitar duplicidade de mensagens.
