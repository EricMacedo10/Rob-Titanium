# 📸 Titanium Brain: Social Media Automation (v3.9.6)

This document details how Titanium maintains a social presence on Instagram and Pinterest without manual intervention.

## 🤖 The Social Bot Orchestrator (v2.4.6)

O bot opera em três frentes de atuação com foco em **Zero-Intervention**:

### 1. Curadoria Moda & Beleza (Titanium)
- **Datafeed Scale-up**: O robô se abastece do pool de 100K produtos via `social/queue_csv_products.py`.
- **Media**: Gera Reels automáticos com efeito Ken Burns a partir de imagens oficiais Shopee.

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

Titanium prioriza **Reels** devido ao alcance orgânico superior.
- **Cloud Bypass (Tmpfiles.org)**: Dribla bloqueios de IP da Meta na hospedagem primária.

---
*Atualizado em: 07/05/2026 - Versão: v4.0.0 (Winter Campaign & Boilerplate Filter)*
