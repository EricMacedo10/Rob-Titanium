# 🧠 Titanium Brain: System Architecture Map (v5.5.0-Elite)

Este documento descreve a topologia de alto nível e o fluxo de dados do ecossistema **Titanium Shopee Exclusive** — validado em produção com postagem automática, preço BR e DM bot funcional.

---

## 🏗️ 1. Filosofia: Desacoplamento & Resiliência Visual

O sistema evoluiu para um modelo de **Máxima Autoridade Visual**:
- **Aesthetics First**: O design das artes (frames 1080x1920) segue o padrão "Magazine Elite", priorizando tipografia luxuosa e espaços negativos.
- **Media Resilience (V5)**: O robô agora detecta gargalos de infraestrutura em tempo real. Se o processamento de Reels (vídeo) falhar por instabilidade da API ou FTP, o sistema executa um fallback atômico para **Imagem Premium**, garantindo 100% de presença diária.
- **Deduplicação Master**: Sistema de exclusividade hierárquica aprimorado para evitar cross-posting entre Moda e Boutique Íntima.

---

## 🛰️ 2. Titanium Control Tower (Monitoramento)

Implementada a lógica de observabilidade centralizada:
- **monitor.json**: Arquivo de estado persistente que rastreia KPIs (Posts realizados, Erros de API, Status de Processamento).
- **Dashboard em Tempo Real**: Interface visual que consome o log de saúde para fornecer uma visão executiva do bot sem necessidade de ler logs de console.

---

## 🗺️ 3. Topologia de Componentes

```mermaid
graph TD
    subgraph "Automação GitHub (Nuvem)"
        ACTION["GitHub Actions (Cron/Manual)"]
        PYTHON["Python Engine (Core v5.0)"]
        AI["IA DeepSeek-V3.2 (Premium Copywriter)"]
    end

    subgraph "Fontes de Dados (Elite)"
        SHP["Shopee API v2 (Elite Media Assets)"]
        FEED["Shopee Datafeed (100K Pool Integration)"]
    end

    subgraph "Infra de Mídia (Hybrid)"
        HOST["Hostinger FTP (Primary Storage)"]
        CLOUD["Cloud Backup (Resilient Delivery)"]
    end

    subgraph "Produção (Instagram/Web)"
        INSTA["Instagram API (Postage & DMs)"]
        SITE["Elite Frontend (data.json)"]
    end

    ACTION --> PYTHON
    PYTHON -- "Context Injection" --> AI
    AI -- "High-Conversion Copy" --> PYTHON
    PYTHON -- "FTP Sync" --> HOST
    PYTHON -- "Hybrid Upload" --> CLOUD
    PYTHON -- "Post Logic" --> INSTA
```

---

## 📊 4. Ciclo de Vida do Dado & Postagem

1.  **Gatilho (Trigger)**: GitHub Actions atua nos 4 horários nobres (08:30, 14:30, 19:30, 23:30 BRT).
2.  **Curação Elite**: Mineração via Datafeed 100K filtrada por semântica sazonal (Inverno 2026).
3.  **Arte Premium**: Frame 1080x1920 com preço formatado em padrão BR (`_parse_price`) e design Magazine Elite.
4.  **Upload Resiliente**: Cloud bypass via tmpfiles.org para imagens (HTTPS), com FTP Hostinger como backup.
5.  **Postagem**: Imagem Premium no Feed do Instagram via Graph API.
6.  **DM Bot**: Resposta automática com link rastreado (`an_18318830863`) + preview do produto.
7.  **Security Gate**: `infra/shield.py` valida 100% dos links antes do deploy.

---

## 🔐 5. Protocolo de Segurança (Nuclear Shield)

- **Secrets Only**: Blindagem total de credenciais.
- **Nuclear Shield (v5.0)**: 100% dos links auditados. Tag Universal `an_18318830863` injetada via Deep Link para garantir comissão em dispositivos móveis.
- **Bypass Estratégico**: Implementação de rotas HTTPS para download de mídias pela Meta API, evitando bloqueios de firewall da Hostinger.

---
*Atualizado em: 01/06/2026 - Versão: v5.5.0-Elite (Freshness Policy + Visual Rotation + Senior Shield Encoding)*
