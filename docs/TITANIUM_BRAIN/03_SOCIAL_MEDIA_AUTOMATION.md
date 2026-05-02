# 📸 Titanium Brain: Social Media Automation (v3.9.0)

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

## 🧠 Smart Link Intelligence v2.2.1 (Hybrid Response - 02/05/2026)

### Problema de Transição Resolvido
Posts realizados sem hashtags específicas (posts antigos ou manuais) causavam falha no bot de resposta, que caía no link genérico. A v2.2 introduz a **Redundância Híbrida**.

### Camadas de Inteligência de Resposta (Prioridade)
1.  **Camada 1: Hashtag Match (OFERTAS.JSON):** Busca exata por hashtags como `#titanium_123` ou `#blazer_premium`.
2.  **Camada 2: Keyword Match (OFERTAS.JSON):** Busca por palavras isoladas no dicionário de hashtags (ex: a palavra "Short" ativa o link de `#kit_short`).
3.  **Camada 3: Deep Database Search (DATA.JSON) - 🎯 SOLUÇÃO DEFINITIVA:** 
    *   Se as camadas acima falharem, o robô abre o banco de dados mestre `data.json` na raiz do servidor.
    *   **Algoritmo de Interseção:** Compara as palavras da legenda com os títulos dos produtos. Se houver 2 ou mais palavras significativas (ex: "Calcinha" + "Modeladora"), o robô identifica o produto e envia o link direto da Shopee.
    *   **Independência de Hashtag:** Garante que 100% dos comentários em qualquer post (antigo ou novo) recebam o link correto.

### Protocolo de Entrega Dupla (Double Delivery)
Para maximizar a conversão, o robô agora envia na mesma DM:
1.  **Link Direto do Produto** (Shopee)
2.  **Link da Vitrine Oficial** (Site) como navegação secundária.

### Protocolo Obrigatório Pré-Publicação
Antes de publicar qualquer post com CTA "Comente QUERO", **SEMPRE** rodar:
```bash
python -m social.validar_ofertas --caption "#sua_hashtag_do_post"
```
Este comando simula exatamente o que o bot fará e alerta se o link está incorreto.

### Protocolo Pós-Atualização do ofertas.json
Após qualquer alteração no `ofertas.json`, **DEVE** sincronizar com o servidor:
```bash
python -m social.upload_ofertas
```

---

## 🎞️ Media Processing & Resilience


Titanium prioriza **Reels** devido ao alcance orgânico superior.
- **Resilient Upload Strategy (v2.4.2)**:
    1.  **Prioridade 1: Cloud Bypass (Tmpfiles.org)** -> Usado como `force_cloud=True` para driblar bloqueios ativos da Meta na hospedagem primária.
    2.  **Por que Tmpfiles?**: Substituiu o ImgBB porque o domínio `ibb.co` foi bloqueado pelo crawler do Facebook (resultando no Erro OAuthException 9004: "Only photo or video can be accepted").
    3.  **Hostinger WAF**: A Hostinger bloqueava o User-Agent do Facebook via ModSecurity dinâmico. A migração para a nuvem resolveu este impasse garantindo 100% de acessibilidade.
    4.  **Smart Polling**: O `InstagramClient` monitora o processamento na nuvem do Meta com loops de retry e timeout tolerantes a containers nulos (especial para mídias mistas).

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
*Atualizado em: 02/05/2026 - Versão: v3.9.0 (Hybrid Intelligence & Deep Database Search)*
