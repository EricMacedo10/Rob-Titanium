# 📸 Titanium Brain: Social Media Automation (v5.3.0-Validated)

Este documento detalha como o Titanium mantém autoridade estética no Instagram com intervenção zero, preço consistente e DM bot funcional.

---

## 🤖 The Social Bot Orchestrator (v5.3.0 - Production Validated)

O bot opera sob o conceito de **Resiliência Estética com Precisão de Dados**:

### 1. Curadoria & Media Generation
- **Frame Elite Standard**: Todas as artes são geradas em resolução nativa **1080x1920** (9:16) via `image_generator.py`.
- **Price Parser Robusto (`_parse_price`)**: Método centralizado que diferencia separadores decimais de milhares, eliminando erros como `44.9 → R$ 449,00`. Validado em produção.
- **Estratégia de Postagem (Image First)**: 
    - **Ativo**: Postagem de **Imagem Premium** no Feed via Cloud Upload (tmpfiles.org → Meta Graph API).
    - **Roadmap**: Reels via API Hostinger (quando migrado de FTP para HTTPS).
- **Design Magazine Elite**: Cabeçalho "SELEÇÃO TITANIUM" com tipografia espaçada, badge de preço glassmorphism e logo Shopee.

### 2. Formatação de Preço (Padrão BR — Unified)
O preço é formatado de forma idêntica em **dois pontos**:
- **Na Arte (imagem)**: `image_generator.py → _parse_price()` → Renderiza `R$ 38,98`.
- **Na Legenda (texto)**: `bot.py → price_display` → Exibe `R$ 38,98`.
- **Garantia**: Ambos usam a mesma lógica de parsing, eliminando discrepâncias permanentemente.

### 3. Vertical Boutique Íntima
- **Isolated Aesthetics**: Copy provocativo gerado por agentes de IA especializados.
- **Pinterest Engine**: Captura de tráfego via inspiração visual (Top of Funnel).

---

## 🧠 Smart Link Intelligence v5.0 (Nuclear Shield)

### 🛡️ Commission Armor
- **Tag Universal**: Injeção mandatória de `an_18318830863` em 100% dos links.
- **Deep Link Enforcement**: Redirecionamento direto para o App da Shopee.
- **DM Bot**: Resposta automática via `bot_instagram.php` com link rastreado + preview rich-card do produto.

### 🔂 Link Loop Immunity
- Travas de segurança contra redirecionamentos infinitos (`go.php → go.php`).

---

## 🔗 Infraestrutura & Conectividade

### 🛰️ Cloud Sync (Resilient Uploads)
- **tmpfiles.org (Primário)**: Upload de imagens via HTTPS — funciona perfeitamente nos runners do GitHub Actions.
- **Hostinger FTP (Secundário)**: Utilizado para `ofertas.json` e assets do site. Bloqueado para mídias do Instagram por firewall.

### 🔐 Token Lifecycle
- Renovação de permissões via GitHub Secrets para postagem ininterrupta 24/7.

---

## 🎯 Campanhas Sazonais (Modo Inverno 2026)
O `queue_csv_products.py` aplica filtros semânticos ao Datafeed de 100K:
- **Keywords ativas**: jaqueta, casaco, moletom, cardigan, sobretudo, tricot, manga longa, gola alta, peluciada.
- **Deduplicação**: Títulos já postados são excluídos automaticamente via `get_posted_titles()`.

---

## 📋 Horários de Postagem (BRT)

| Horário | Cron (UTC) | Objetivo |
|---|---|---|
| 08:30 | `30 11 * * *` | Feed matinal |
| 14:30 | `30 17 * * *` | Pós-almoço |
| 19:30 | `30 22 * * *` | Prime-time |
| 23:30 | `30 02 * * *` | Night owls |

---
*Atualizado em: 09/05/2026 - Versão: v5.3.0-Validated (Price Parser + DM Bot + Feed Post Confirmado)*

