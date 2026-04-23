# 📸 Titanium Brain: Social Media Automation (v2.4.1)

This document details how Titanium maintains a social presence on Instagram and Pinterest without manual intervention.

## 🤖 The Social Bot Orchestrator (v2.4.0)

O bot opera em três frentes de atuação:

### 1. Curadoria Moda & Beleza (Titanium)
- **Datafeed Scale-up**: O robô se abastece do pool de 100K produtos via `social/queue_csv_products.py`.
- **Media**: Gera Reels automáticos com efeito Ken Burns a partir de imagens oficiais Shopee.

### 2. Vertical Sensual Boutique (New)
- **Estratégia Pinterest**: Foco em estética "Aesthetic" e rituais de autocuidado para evitar shadowbans.
- **Instagram Dark-Mode**: Uso de templates com a paleta Mauve/Gold para diferenciar a vertical no feed.
- **Discrição Mandatória**: Legendas focadas em bem-estar e rituais, com CTA para link na Bio ou DM.

### 3. Fila Agendada (Scheduled Manifesto)
- **File**: `social/fila/schedule.json`.
- **Logic**: Define exatamente qual mídia será postada em datas específicas.

---

## 🎞️ Media Processing & Resilience

Titanium prioriza **Reels** devido ao alcance orgânico superior.
- **Resilient Upload Strategy (v1158)**:
    1.  **Prioridade 1: Hostinger (FTP)** -> `/social/`.
    2.  **Auto-fallback ImgBB**: Ativado se o crawler do Facebook for bloqueado pelo WAF do Hostinger.
    3.  **Smart Polling**: O `InstagramClient` monitora o processamento na nuvem do Meta com loops de retry e timeout inteligente.

---

## 🔗 Instagram Graph API & DM Automation

O sistema usa um PHP Bot (`bot_instagram.php`) para monitorar comentários e enviar links via DM.

### 🔐 Protocolo de Tokens (Permanent Access)
- **Titanium Token Manager**: Script `social/titanium_token_manager.py` automatiza a renovação de tokens.
- **Page Access Token**: O sistema utiliza tokens de página que **nunca expiram**, garantindo que a automação de DM nunca pare por falha de autenticação.
- **Segurança**: **JAMAIS** commitar o arquivo `.env` ou scripts com o `App Secret` preenchido. Use sempre placeholders e variáveis de ambiente.

### 🔑 Gatilhos de Disparo
Ativado por palavras como: `"link"`, `"quero"`, `"valor"`, `"preco"`.

---

## 🎨 Design System para Redes Sociais
- **Titanium Moda**: Laranja Shopee, Branco e Roxo.
- **Sensual Boutique**: Deep Mauve, Soft Gold e Transparências.

---
*Atualizado em: 23/04/2026 - Versão: v3.8.1 (Multivirtines Social Support)*
