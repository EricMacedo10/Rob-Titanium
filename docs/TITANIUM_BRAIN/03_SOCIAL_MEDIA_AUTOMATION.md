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
- **Resilient Upload Strategy (v1156)**: 
    1.  **Prioridade 1: Hostinger (FTP)** -> `guiadodesconto.com.br/social/`. Esta rota é mais estável para os servidores do Meta devido à proximidade geográfica e menor latência.
    2.  **Prioridade 2: ImgBB** (Fallback). Usado apenas se o Hostinger estiver offline ou bloqueado.
    3.  **Conversão Segura**: O script obrigatoriamente gera arquivos temporários com nomes únicos (`temp_...`) para evitar destruir o arquivo original da fila em caso de erro no processo de upload.

## 🛠️ Troubleshooting: Falhas Comuns
### 1. Erro 9004 (Media download took too long)
- **Causa**: Meta não conseguiu baixar a imagem da URL pública em 30-60 segundos.
- **Solução**: Mudar a prioridade de upload para o Hostinger ou tentar converter a imagem para um tamanho menor (KB).
### 2. File Not Found (Encoding Issues)
- **Causa**: Caminhos com acentos (ex: "Área de Trabalho") no Windows.
- **Solução**: O script agora utiliza busca dinâmica via `os.listdir()` e matching em lowercase para garantir que o arquivo seja encontrado independente do encoding do sistema operacional.

## 🔗 Instagram Graph API Orchestration
The [InstagramClient](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/social/core/instagram_client.py) handles a optimized 3-step publishing process:
1.  **Media Container**: Sends the public URL to Meta.
2.  **Smart Polling**: 
    - Waits for Meta's cloud processing.
    - **Fix**: Only requests `status_code` during polling. Only requests `failure_reason` if an `ERROR` is detected (requesting it prematurely causes API Error 400).
3.  **Publication**: Triggers the `media_publish` command once the container is `FINISHED`.

---
> [!NOTE]
> All social activity honors the `ENV_MODE`. In `STAGING`, actual post calls are bypassed and logged to the console/logs for validation.
