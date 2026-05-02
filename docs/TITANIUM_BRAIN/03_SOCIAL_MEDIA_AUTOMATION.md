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

## 🧠 Smart Link Priority v2.0 (Correção Crítica - 02/05/2026)

### Problema Resolvido
O bot enviava o link do **site** em vez do link do **produto** porque a lógica antiga fazia `break` na primeira hashtag encontrada. Hashtags genéricas como `#modafeminina` (que apontam para o site) "ganhavam" de hashtags específicas como `#blazer_premium` (que apontam para o produto real).

### Nova Lógica de Prioridade
1. **PRODUTO Shopee** (prioridade máxima): Links contendo `shopee.com.br` ou `s.shopee.com.br`. Se múltiplas hashtags de produto forem encontradas, a mais **específica** (nome mais longo) vence.
2. **Site** (fallback): Links do `guiadodesconto.com.br` — usados apenas quando nenhum link de produto é encontrado.
3. **#default** (último recurso): Quando nenhuma hashtag da legenda é encontrada no `ofertas.json`.

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
*Atualizado em: 28/04/2026 - Versão: v3.8.2 (Multivitrines e Bypass Cloud Social)*
