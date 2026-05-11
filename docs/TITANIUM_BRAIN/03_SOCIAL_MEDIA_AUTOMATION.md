# 📸 Titanium Brain: Social Media Automation (v5.4.1-UltraSafe)

Este documento detalha como o Titanium mantém autoridade estética no Instagram com intervenção zero, preço consistente e DM bot funcional.

---

## 🤖 The Social Bot Orchestrator (v5.3.0 - Production Validated)

O bot opera sob o conceito de **Resiliência Estética com Precisão de Dados**:

### 1. Curadoria & Media Generation
- **Frame Elite Standard**: Todas as artes são geradas em resolução nativa **1080x1920** (9:16) via `image_generator.py`.
- **Price Parser Robusto (`_parse_price`)**: Método centralizado que diferencia separadores decimais de milhares, eliminando erros como `44.9 → R$ 449,00`. Validado em produção.
- **Safe Zone Layout (v5.4.1 - UltraSafe)**: O selo de preço foi elevado para `y=1270` (em 1080x1920), garantindo visibilidade imune a qualquer corte de grade (Explore) ou sobreposição de UI. No Feed (1080x1080), a posição é `y=830`.
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
- **Keywords ativas**: jaqueta, casaco, moletom, cardigan, sobretudo, tricot, manga longa, gola alta, peluciada.
- **Deduplicação Nuclear (Master Guard)**: O sistema agora verifica simultaneamente a pasta `postados/` e a `fila/` antes de gerar novas artes, impedindo duplicidade mesmo que os itens ainda não tenham sido publicados.

---

## 📋 Horários de Postagem (BRT)

| Horário | Cron (UTC) | Objetivo |
|---|---|---|
| 08:30 | `30 11 * * *` | Feed matinal |
| 14:30 | `30 17 * * *` | Pós-almoço |
| 19:30 | `30 22 * * *` | Prime-time |
| 23:30 | `30 02 * * *` | Night owls |

---

### 🛡️ Prevenção de Postagens Fantasmas (Lesson Learned 2026-05-11)
- **Causa**: Falhas de infraestrutura do GitHub (Erro 500) durante o passo de `git-auto-commit-action` impediam o robô de salvar o estado de postagem.
- **Solução**: Implementada a verificação redundante na pasta `fila/` dentro do script `queue_csv_products.py`. Se o arquivo está na fila, ele é considerado "em processamento" e nunca será duplicado.

*Última Auditoria Técnica: 11/05/2026 - Status: Ultra-Safe Positioning v5.4.1 | Deduplicação Nuclear | YAML Quoting Active*
