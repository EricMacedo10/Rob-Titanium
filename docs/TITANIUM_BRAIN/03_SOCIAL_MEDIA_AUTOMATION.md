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
    - Post-success: Moves the file to `social/postados/`.

### 2. Category Fallback Mode (Automated)
- **Trigger**: Used when the queue is empty.
- **Schedule**:
    - **Morning**: Amazon deals.
    - **Afternoon**: Shopee deals.
    - **Evening**: Mercado Livre deals.
- **Logic**: Selects the best category banner and the top-discounted product for that store.

## 🎞️ Media Processing
Titanium prioritizes **Reels** over static images because of higher algorithmic reach.
- **Ken Burns Effect**: Static images are animated with subtle zoom/pan.
- **Resilient Upload**: 
    1.  Tenta upload via FTP para `guiadodesconto.com.br/social/`.
    2.  Fallback para a API do **ImgBB** caso o FTP falhe.

## 🔗 Instagram Graph API Orchestration
The [InstagramClient](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/social/core/instagram_client.py) handles a 3-step publishing process:
1.  **Media Container**: Sends the public URL to Meta.
2.  **Polling**: Waits for Meta's cloud processing (crucial for videos).
3.  **Publication**: Triggers the `media_publish` command once the container is `FINISHED`.

---
> [!NOTE]
> All social activity honors the `ENV_MODE`. In `STAGING`, actual post calls are bypassed and logged to the console/logs for validation.
