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
2.  **Smart Polling**: 
    - Waits for Meta's cloud processing.
    - **Fix**: Only requests `status_code` during polling. Only requests `failure_reason` if an `ERROR` is detected (requesting it prematurely causes API Error 400).
3.  **Publication**: Triggers the `media_publish` command once the container is `FINISHED`.

---
> [!NOTE]
> All social activity honors the `ENV_MODE`. In `STAGING`, actual post calls are bypassed and logged to the console/logs for validation.
