# 📸 Titanium Brain: Social Media Automation (v4.1.0)

This document details how Titanium maintains a social presence on Instagram and Pinterest without manual intervention, focusing on high-end aesthetic authority.

## 🤖 The Social Bot Orchestrator (v2.5.0 - Elite Standard)

O bot opera em três frentes de atuação com foco em **Zero-Intervention** e **Premium Visuals**:

### 1. Curadoria Moda & Beleza (Titanium Premium)
- **Datafeed Scale-up**: O robô se abastece do pool de 100K produtos via `social/queue_csv_products.py`.
- **Media (Premium Static Reel)**: Substituição do efeito Ken Burns (instável) por **Vídeos Estáticos de Alta Fidelidade**. 
    - **Visual**: Design de revista de luxo ("Seleção Titanium") com tipografia minimalista e badges harmonizados.
    - **Técnica**: Conversão de frames 1080x1920 em MP4 com bitrate de **5000k** e **CRF 18** para garantir nitidez cristalina e dibrar o algoritmo do Instagram como Reels.

### 2. Vertical Boutique Íntima (Isolated)
- **Estratégia Pinterest**: Foco em estética "Aesthetic" e rituais de autocuidado para evitar shadowbans.
- **Instagram Dark-Mode**: Uso de templates com a paleta Mauve/Gold para diferenciar a vertical no feed.

---

## 🧠 Smart Link Intelligence v2.5 (Hybrid Response & Armor)

### 🛡️ Blindagem de Comissão (Commission Armor)
O robô aplica uma **camada tripla de rastreio**:
- **Link Curto Oficial**: Uso de links `s.shopee.com.br`.
- **Redundância UTM**: Injeção automática de `?utm_source=an_18318830863`.
- **PHP Real-Time Shield**: O `bot_instagram.php` executa uma auditoria final antes de enviar a DM, corrigindo qualquer link mal formatado no dicionário.

### 🔂 Imunidade de Link (Link Loop Immunity v3.9.6)
Para evitar o erro de "Verify Traffic" da Shopee (causador de zero vendas histórico), o sistema agora possui uma trava de recursividade:
- **Lógica**: O `titaniumLinkAuditor` no Javascript e o PHP de redirecionamento detectam se a URL já passou por um tratamento prévio.
- **Prevenção**: Impede o empilhamento de `go.php?url=go.php...`, garantindo um caminho limpo até o checkout.

---

## 🔗 Redes e Conectividade (Hostinger Bypass)

### 🛰️ Protocolo cURL (Obrigatório)
O bot utiliza **cURL** com bypass de SSL e timeout de 30s para garantir estabilidade em servidores Hostinger.
- **Varredura Ampla**: Monitoramento de **20 posts recentes**.

### 🔐 Protocolo de Tokens (Permanent Access)
- **Inject & Deploy**: O deploy via `social/inject_and_deploy.py` garante que os tokens reais do `.env` sejam inseridos no servidor sem expor segredos no Git.

---

## 🎯 Campanhas Sazonais Isoladas (ex: Modo Inverno)
Para focar o Instagram em estações específicas (como o Inverno) sem interferir no site principal, o `social/queue_csv_products.py` implementa um **Filtro de Extração**. Ele consome do Datafeed global (100K+) e adiciona uma barreira semântica, aceitando apenas produtos com palavras-chave específicas da estação (ex: "jaqueta", "casaco", "moletom") para enviar à fila de postagem.

---

## 🎞️ Media Processing & Resilience

Titanium prioriza **Reels** devido ao alcance orgânico superior para não-seguidores.
- **High-Fidelity Rendering**: Uso de `moviepy` para garantir que frames estáticos de luxo se tornem vídeos MP4 de 6 segundos sem artefatos de compressão.
- **Cloud Bypass (Tmpfiles.org)**: Dribla bloqueios de IP da Meta na hospedagem primária durante o upload de mídia para a API Graph.

---
*Atualizado em: 08/05/2026 - Versão: v4.1.0 (Premium Elite & Static-to-Video Hack)*
