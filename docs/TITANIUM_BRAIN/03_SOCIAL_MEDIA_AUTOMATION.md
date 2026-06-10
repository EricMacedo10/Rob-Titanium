# 📸 Titanium Brain: Social Media Automation (v5.5.0-UltraSafe)

Este documento detalha como o Titanium mantém autoridade estética no Instagram com intervenção zero, preço consistente e DM bot funcional.

---

## 🤖 The Social Bot Orchestrator (v5.3.0 - Production Validated)

O bot opera sob o conceito de **Resiliência Estética com Precisão de Dados**:

### 1. Curadoria & Media Generation
- **Frame Elite Standard**: Todas as artes são geradas em resolução nativa **1080x1920** (9:16) via `image_generator.py` e `video_generator.py`.
- **Price Parser Robusto (`_parse_price`)**: Método centralizado que diferencia separadores decimais de milhares, eliminando erros como `44.9 → R$ 449,00`. Validado em produção.
- **Safe Zone Layout (v5.4.1 - UltraSafe)**: O selo de preço foi elevado para `y=1270` (em 1080x1920), garantindo visibilidade imune a qualquer corte de grade (Explore) ou sobreposição de UI. No Feed (1080x1080), a posição é `y=830`.
- **Estratégia de Postagem (Multicanal)**: 
    - **Ativo (Imagens)**: Postagem de **Imagem Premium** no Feed via Cloud Upload (tmpfiles.org → Meta Graph API).
    - **Ativo (Vídeos)**: **Máquina de Reels & Stories** nativa usando `moviepy` (`social/core/video_generator.py`). Gera e publica simultaneamente Reels e Stories via Meta Graph API com fundos estéticos lofi e tipografia clean.
- **Visual Call-to-Action (v5.6.0)**: O `video_generator.py` aplica uma faixa dark/orange chamativa no meio do card ("💬 COMENTE 'QUERO'") para forçar a interação do usuário e disparar o Bot de DMs, solucionando gargalos de conversão no tráfego frio.
- **Post Logger Automático**: Ao postar com sucesso, o `bot.py` registra o item no `site/instagram_posts.json`. Em seguida, o `upload_ofertas.py` sincroniza simultaneamente o `ofertas.json` (para o Bot de DM em PHP) e o `instagram_posts.json` (para a Link-in-Bio em HTML), fechando o funil de forma 100% autônoma.

### 2. Formatação de Preço (Padrão BR — Unified)
O preço é formatado de forma idêntica em **dois pontos**:
- **Na Arte (imagem)**: `image_generator.py → _parse_price()` → Renderiza `R$ 38,98`.
- **Na Legenda (texto)**: `bot.py → price_display` → Exibe `R$ 38,98`.
- **Garantia**: Ambos usam a mesma lógica de parsing, eliminando discrepâncias permanentemente.

### 3. Vertical Boutique Íntima
- **Isolated Aesthetics**: Copy provocativo gerado por agentes de IA especializados.
- **Pinterest Engine**: Captura de tráfego via inspiração visual (Top of Funnel).

---

## 🧠 Smart Link Intelligence v7.0 (Nuclear Shield v5.0 + Deep Link Proxy)

### 🛡️ Commission Armor
- **Short Link Oficial (Método Primário)**: `infra/shield.py` e `core/link_builder.py` chamam o motor de API moderna `ShopeeAffiliateAPI` para gerar short links oficiais (`s.shopee.com.br` ou `shope.ee`) com a tag de afiliado embarcada. Este é o único canal que garante atribuição real de comissão no painel da Shopee.
- **Remoção do utm_source**: O fallback legado de injetar `?utm_source=an_18318830863` foi totalmente removido em Python (`shield.py` e `link_builder.py`) e PHP (`bot_instagram.php`). Como essa tag não garante comissão, sua injeção mascarava falhas de API. Agora, se a API falhar, o link original é preservado sem modificações.
- **Deep Link Proxy (go.php v2.0)**: Ponte que detecta o User-Agent do Instagram In-App Browser. Se acessado por um dispositivo móvel no direct do Instagram, tenta abrir o aplicativo da Shopee diretamente (via esquema `shopee://` no Android ou redirecionamento de Universal Link no iOS). Navegadores normais são redirecionados de forma silenciosa via PHP/JS.
- **DM Bot (Anti-Instagram In-App Browser)**: O `bot_instagram.php` (v3.0.0) agora utiliza a função `titanium_bridge()` para envolver todos os links de produtos Shopee enviados via DMs de comentários ou stories na rota de proxy `https://guiadodesconto.com.br/go.php?url=...`.
- **Story Auto-Responder (DM Inbox Polling)**: O bot PHP varre a caixa de entrada (`/conversations`) identificando clientes que responderam aos Stories. Ele vincula instantaneamente as menções de "Quero" à tag `#latest_story` em `ofertas.json`, enviando o link afiliado envelopado no Deep Link Proxy.
- **Preview Rich-Card**: Resposta via DM com link proxy e chamada para ação nativa.

### 🔂 Link Loop Immunity & CLI Fallback (v2.2)
- Travas de segurança contra redirecionamentos infinitos (`go.php → go.php`).
- Resolução dinâmica de paths para execução do Bot PHP em ambiente CLI (Cron), garantindo o acesso ao `data.json` da vitrine principal mesmo sem variáveis de sessão Apache/Nginx.

---

## 🔗 Infraestrutura & Conectividade

### 🛰️ Cloud Sync (Resilient Uploads)
- **tmpfiles.org (Primário)**: Upload de imagens e vídeos (Reels/Stories) via Cloud CDN — bloqueia problemas de firewall na Hostinger limitados pela porta 21 (FTP) via Actions.
- **GitHub Raw (Primary Source)**: O `ofertas.json` agora é persistido exclusivamente no repositório (via `git-auto-commit`) e servido pelo CDN do GitHub para o `bot_instagram.php`, eliminando a dependência de FTP.

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
| 08:30 | `30 11 * * *` | Feed matinal (Imagens) |
| 12:30 | `30 15 * * *` | **Reels & Stories (Moda & Beleza)** |
| 14:30 | `30 17 * * *` | Pós-almoço (Imagens) |
| 19:30 | `30 22 * * *` | Prime-time (Imagens) |
| 23:30 | `30 02 * * *` | Night owls (Imagens) |

---

### 🛡️ Prevenção de Postagens Fantasmas (Lesson Learned 2026-05-11)
- **Causa**: Falhas de infraestrutura do GitHub (Erro 500) durante o passo de `git-auto-commit-action` impediam o robô de salvar o estado de postagem.
- **Solução**: Implementada a verificação redundante na pasta `fila/` dentro do script `queue_csv_products.py`. Se o arquivo está na fila, ele é considerado "em processamento" e nunca será duplicado.

*Última Auditoria Técnica: 08/06/2026 - Status: Commission Security v7.0.0 | Deep Link Proxy v2.0 | ShopeeAffiliateAPI | Video Generation Engine | Story Inbox Polling | Fastly CDN Sync*
