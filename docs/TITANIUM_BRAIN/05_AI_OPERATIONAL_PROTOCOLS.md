# 🛡️ Titanium Brain: AI Operational Protocols (Senior Rules)

This document establishes the "Rules of Engagement" for any AI agent or professional interacting with the Titanium codebase.

## 🖋️ The "Senior Workflow" Protocol

1.  **Iterative Analysis**: Before any change, read this Knowledge Base (`docs/TITANIUM_BRAIN/`).
2.  **Implementation Plans**: Every non-trivial task requires an `implementation_plan.md` with:
    - User Review Required section.
    - Detailed File Mapping (MODIFY/NEW/DELETE).
    - Verification Plan (Automated + Manual).
- **Exit Code Compliance**: Scripts de automação executados em CI/CD **DEVEM** usar `sys.exit(1)` em falhas críticas e `sys.exit(0)` em sucesso para integração perfeita com GitHub Actions.
3.  **Verification Walkthrough**: Every task must end with a `walkthrough.md` documenting results with screenshots or logs.

## 🚫 The "Don't Touch" List

- **`index.html` Hierarchy**: Do not restructure the main layout IDs (`deals-grid`, etc.) without updating the JS selectors in `app.js`.
- **Image Safe Zone**: Do not lower the price badge below `y=1270` in vertical arts (1080x1920) to maintain 100% Explore Grid immunity.
- **state/` Directory**: Do not commit this folder. It contains volatile but critical session tokens.
- **Affiliate Tag Logic**: Do not hardcode tags in the middle of functions. Always use `core/settings.py` or the `app.js` config block.

## 🛠️ Troubleshooting Guide

| **Symptom** | **Probable Cause** | **Action** |
| :--- | :--- | :--- |
| **data.json vazio** | Erro de Parser no Datafeed. | O novo parser (v3.7) detecta `;` e `,` automaticamente. Se persistir, verifique se os headers do CSV da Shopee mudaram drasticamente. |
| **Itens Repetidos** | Falha na Deduplicação. | Verifique se `specialist.json` ou `ai_reviews.json` estão corrompidos ou com IDs inválidos. O sistema requer estes arquivos para o cross-check. |
| **Editorial Sem nexo** | Falha de dados no Blog. | Se o blog falar de "Maquiagem" mas injetar "Calças", o robô não conseguiu acessar o pool de 100k e usou o fallback local. Verifique os segredos do Datafeed. |
| **Robô de DM falhando** | Token expirado (190/463). | Renovar token via `python -m social.titanium_token_manager`. |
| **Preço errado na arte** | Parser antigo multiplicava decimais. | Corrigido em v5.1 com `_parse_price()`. Se persistir, limpar `social/fila/` e regenerar via `python -m social.queue_csv_products`. |
| **Imagens genéricas** | Fallback ativado. | O sistema agora usa a API Oficial via `core/shopee_api.py`. Se falhar, use os assets manuais em `site/images`. |
| **Erro 403 Actions** | Permissão de Escrita GITHUB_TOKEN. | O workflow exige `permissions: contents: write` explicitamente para realizar o Auto-Commit de arquivos JSON. |
| **Bot envia link errado** | Falso Positivo na CAMADA 3. | O bot cruzou palavras genéricas da legenda (ex: "Moda") com o `data.json`. Mantido o **Boilerplate Filter** no `bot_instagram.php` para ignorar palavras-chave estruturais. |


## 🚀 Protocolos de Resiliência de Fluxo (v1156)

Para prevenir erros de "timeout" e perda de dados em automações complexas:

1.  **Regra de Rastreabilidade (Unique Temps)**: Qualquer lógica que gere arquivos temporários (ex: conversão de imagem) **DEVE** usar nomes únicos com timestamp (`temp_1713...`). Nunca use o nome do arquivo original como base para arquivos deletáveis.
2.  **Regra de Proximidade de Rede**: Para APIs instáveis (Meta/Instagram), a prioridade de rota de mídia deve ser o servidor Hostinger (Brasil), garantindo latência mínima e maior taxa de sucesso no download iniciado pelo Facebook.
3.  **Check de Integridade Pós-Erro**: Se uma execução falhou, a próxima **DEVE** começar verificando a integridade dos arquivos na pasta `fila/` via `os.listdir()`.

## 🩺 Rotina de Health Check (Auditoria 100%)

Para garantir que o robô não entre em "estado vegetativo", siga esta rotina:

1.  **Check de Frescor**: Verifique o timestamp de `site/data.json`. Se for > 24h, o agendador falhou.
2.  **Check de Conectividade**: Rode `python -m core.arbitrator` para um produto teste.
3.  **Check de Tags**: Inspecione os links no `data.json` local para confirmar se as tags de afiliado estão presentes.
4.  **Check de Fila**: Verifique `social/fila/` para garantir que há conteúdo para os próximos dias.


---
## 🛎️ Decisões Arquiteturais (Lessons Learned 2026-02-20)

### Barra de Ofertas (Lightning Bar)
- **Status atual:** Desativada temporariamente via `display: none !important` no `style.css`.
- **Motivo:** O scraper genérico retornava produtos irrelevantes (ex: liquidificador de brinquedo) e preços sem centavos corretos.
- **Abordagem recomendada para reativação:**
  - **Regra de Ouro (Isolamento de Ambiente)**: 
    - O Robô Titanium em modo **STAGING** é o único autorizado a atualizar arquivos de layout (`index.html`, `js`, `css`). 
    - Em modo **PRODUCTION**, o sistema opera sob **Blindagem**, atualizando exclusivamente o `data.json` e `notifications.json`. Nunca tente "corrigir" o layout de produção via scripts automáticos agendados.
  - Gate obrigatório de preço mínimo por categoria antes de exibir qualquer produto.

### ✍️ Triple-Core Editorial Rotation (v4.0 - 04/05/2026)
- **Protocolo de Renovação Total**: O sistema de editorial não rotaciona apenas um card, mas sim os **3 slots simultâneos** no `index.html` a cada ciclo semanal (Domingos).
- **Simetria de Vertical**: Cada ciclo deve gerar obrigatoriamente um novo artigo para cada pilar:
    1.  **Moda & Estilo** (Alfaiataria, Looks de Trabalho, Fitness, Praia, Vestidos).
    2.  **Beleza & Skincare** (Maquiagem, Rotinas de Pele, K-Beauty).
    3.  **Tendências & Lifestyle** (Calçados, Acessórios, Gadgets).
- **Lógica de Automação (`core/auto_blog_generator.py`)**:
    - Gera 3 slugs amigáveis.
    - Extrai resumos via `BeautifulSoup` para os cards do index.
    - Atualiza os marcadores `EDITORIAL_LATEST`, `EDITORIAL_MID` e `EDITORIAL_OLD` no `index.html`.
    - Realiza o salvamento atômico dos 3 arquivos HTML em `site/blog/`.


### 🎨 Conservadorismo de Visual (The Minimalist Look)
- **Protocolo de Não-Interferência (2026-03-10):** Muitos elementos (ex: barra de busca no Hero, Assets 3D) podem estar ocultos intencionalmente via CSS (`display: none !important`) para manter uma estética minimalista em produção. 
- **Regra de Ouro:** Nunca "corrija" a visibilidade de elementos estruturais sem confirmação explícita do usuário, mesmo que pareçam "quebrados" no ambiente de staging. Foque exclusivamente no escopo do hotfix solicitado.

### 🗓️ Limpeza de Campanhas Sazonais
- **Ocultar > Deletar:** Prefira esconder seções sazonais (ex: Dia da Mulher, Natal) via `style="display: none;"` no HTML e comentários no JS/CSS. Isso preserva a estrutura para o ano seguinte e evita quebras de referências em scripts automatizados.

### 🛒 Mudança de Nicho: Procedimento Correto (2026-03-19)
Esta sessão comprovou um bug crítico: ao mudar a vitrine para um novo nicho (ex: Eletrônicos → Moda Feminina), o **`core/settings.py` deve ser atualizado imediatamente** antes do próximo Cron Job do GitHub Actions. Se não for feito, a Action vai sobrescrever a nova vitrine com os produtos antigos do nicho anterior.

**Procedimento correto de troca de nicho:**
1. Rodar os mineradores do novo nicho (ex: `production_fashion_miner.py`).
2. Rodar `scraper/clean_db.py` para sanitizar o novo banco.
3. Atualizar os `TARGETS` em `core/settings.py` com as palavras-chave do novo nicho.
4. Commit & Push do `settings.py` para o GitHub **antes** da próxima execução agendada.
5. Rodar `infra/upload_data.py` (PRODUCTION mode) para enviar o `data.json` limpo ao servidor.
6. Confirmar o visual da vitrine em produção.

### 💰 Deploy de data.json vs. Assets Estruturais
- **`infra/deploy.py`**: Envia APENAS assets de layout (HTML, CSS, JS, Imagens). Exclui `data.json` por design (proteção contra sobrescrita acidental).
- **`infra/upload_data.py`**: Envia APENAS o `data.json`. Usa `ENV_MODE` para escolher entre produção (`/`) e staging (`/teste`). Use este script para forçar atualização de produtos sem alterar o layout.
- **`sync_staging_v12.py`**: Script legado de sincronização para staging. Usa lista fixa de arquivos.
- **`social/automate_fashion_carousel.py`** *(2026-03-21)*: Lê imagens de modelos IA (geradas pelo assistente) e cria as artes finais do carrossel (1080x1080 JPEG com badge de preço/loja) salvando em `social/fila/`.
### 🛰️ Titanium Social Bot (v2.2.1 - 05/05/2026): 
Bot principal. Posta **1 item por ciclo** da fila como Reel. Executar com `python -m social.core.bot` a partir da raiz do projeto. Integra o Shield Gate para o `ofertas.json`.

### 🛡️ social/bot_instagram.php (v2.5.0 - 05/05/2026): 
Bot PHP com **Real-Time Shield**. Agora possui a função `titanium_shield` que audita cada link de DM antes do envio, prevenindo perda de comissão por links mal formatados no dicionário.
- **`social/ofertas.json`** *(Servidor Hostinger, raiz `/`)*: Dicionário de hashtags→links. Atualizar a cada novo post e fazer upload via `python -m social.upload_ofertas` ou `python -m social.deploy_bot`.
- **`social/validar_ofertas.py`** *(v1.0 - 02/05/2026)*: Ferramenta de validação pré-publicação. Simula a lógica do `bot_instagram.php` localmente para garantir que o link correto será enviado. Uso: `python -m social.validar_ofertas --caption "#sua_hashtag"` ou `--audit` para auditoria completa.
- **`social/deploy_bot.py`** *(v1.0 - 02/05/2026)*: Script de deploy que envia `bot_instagram.php` + `ofertas.json` ao servidor Hostinger via FTP em uma única execução. Uso: `python -m social.deploy_bot`.
- **`social/titanium_token_manager.py`** *(2026-05-07)*: Gerenciador automático de tokens Meta/Instagram. Realiza o upgrade para um **Page Access Token permanente (♾️ nunca expira)**, atualiza o `.env` e sincroniza o `bot_instagram.php` diretamente no servidor via FTP.

### ❄️ Inverno 2026: Hardening do Motor Social (v4.1 - 07/05/2026)
1. **Transição de Campanha**: Alinhamento total para Moda Inverno (Jaquetas, Tricots, Casacos) no pool de dados.
2. **Correção de Orquestração CI/CD**: Workflow `titanium_social_auto.yml` corrigido para injetar `SHOPEE_DATAFEED_URLS`, garantindo acesso ao pool de 100k produtos em produção.
3. **Resiliência de Token**: Implementado bypass de expiração via Page Access Token, eliminando a necessidade de renovação manual mensal.
4. **Proteção Anti-Post Órfão**: Corrigido erro silencioso de compilação no `social/core/bot.py` e adicionada trava arquitetural rígida. O robô aborta a postagem (`sys.exit(1)`) caso não consiga gerar a hashtag única, garantindo 100% de integridade com o funil de DM.


### 🛒 Filtro de Exibição Front-End (Lessons Learned 2026-05-17)
- **Causa:** Produtos de um mesmo banco de dados (ex: `data_sensual.json`) com categorias distintas competiam por espaço no array `.slice(0, 24)` desenhado na tela. Lingeries preenchiam os slots antes dos cosméticos serem renderizados.
- **Solução (v3.8.4):** É obrigatório usar um `.filter()` explícito por categoria no JavaScript (`app_sensual.js`) antes do `.slice()`, garantindo que seções temáticas como "Cosmética & Bem-Estar" renderizem apenas os produtos designados.

### 🛡️ Tratamento de Fallback de Datafeed (2026-05-17)
- As URLs do **Shopee Datafeed** expiram. O orquestrador (`core/orchestrator.py`) foi corrigido para sempre mesclar as ofertas extraídas pelo motor de *fallback local* (`update_manual_targets`) na lista global `unique_new`, impedindo o bloqueio do site por lista vazia.

## 🚀 Hotfixes e Deploy Emergencial (Senior Only) [30/03]

Para correções estruturais (CSS/JS) no Staging ou Produção:

1.  **Cache-Busting Mandatório**: SEMPRE incremente a versão `?v=X.X` nas tags de `<link>` ou `<script>` do HTML ao subir alterações estéticas.
2.  **Upload de HTML Atômico**: O script de Hotfix (`upload_hotfix_js.py`) deve enviar o arquivo HTML versionado **junto** com os ativos modificados.
3.  **Validação Visual de Dispositivo**: Antes de declarar vitória, valide via screenshot a integridade do layout (Overflow, Alinhamento de Badges e Colisões de Estilo).

---
## 🚀 AI-Driven Trend Radar (v3.7)

O Titanium opera agora sob o regime de **Radar de Tendências Ativo**:
1. **Filtro de Desejo**: A IA DeepSeek-V3.2 (Speciale) não apenas analisa preços, mas a "curva de desejo" (Fashion Intensity) de cada item via Extreme Reasoning.
2. **Master Deduplication Strategy**: O motor de IA é instruído a ignorar qualquer item contido no `specialist.json`, focando em novidades puras para o Radar.
3. **Simetria Obrigatória (Compliance Visual)**: O motor `review_engine.py` **deve obrigatoriamente gerar exatos 18 itens**.
4.  **Nuclear Shield v4.0 (Short Link — Anti-Loss Protection)**:
   - O `infra/shield.py` agora gera **Short Links Oficiais** via API Shopee (`s.shopee.com.br`) como método primário. Este é o único método que garante crédito de comissão no painel de afiliados.
   - O parâmetro `utm_source` é **exclusivamente** um fallback para rastreamento GA quando a API estiver indisponível. Ele **NÃO garante comissão Shopee**.
   - NUNCA gerar um link fora do wrapper `build_affiliate_link` ou do `infra/shield.py`.
   - O Gatekeeper `infra/shield.py` validará e converterá qualquer link gerado pela IA para Short Link antes do upload final.

---
## 🌹 Segmentação por Nicho & Luxo Sensorial (v3.9 - 30/04/2026)

O Titanium agora suporta verticais de nicho (ex: Boutique Íntima) com protocolos de linguagem e automação isolados:

1.  **Exclusividade DeepSeek (Cost-Efficiency Strategy)**:
    *   Para nichos de curadoria massiva (Radar de Tendências), o sistema deve operar **100% via DeepSeek API**.
    *   **Isolamento de Chaves**: Cada vertical deve possuir sua própria Secret no GitHub (`DEEPSEEK_API_KEY_SENSUAL`) para monitoramento granular de consumo.

2.  **Dicionário de Sofisticação (Boutique Íntima)**:
    *   O motor de IA **NUNCA** deve utilizar terminologia vulgar ou explícita.
    *   **Mapeamento de Luxo Obrigatório**:
        *   `Vibrador/Toy` ➔ **Estimulador de Precisão / Gadget de Bem-Estar**.
        *   `Sugador` ➔ **Tecnologia de Pulsação Air-Touch**.
        *   `Borracha/Plástico` ➔ **Silicone de Toque Aveludado / Design Ergonômico**.
        *   `Sexo/Tesão` ➔ **Ritual Sensorial / Intimidade / Autoconhecimento**.

3.  **Protocolo de Staging Silencioso**:
    *   Novas boutiques entram em operação via **GitHub Actions Independentes**, minerando dados e gerando reviews em arquivos isolados (`data_sensual.json`), sem conexão física com a `index.html` até a aprovação final do usuário.

### 💎 Premium Visual Standard & Aesthetic Hardening (v3.9.9 - 17/05/2026)
Após auditoria de performance, estabeleceu-se o padrão **"Elite Magazine"** para todo o ecossistema social:

1.  **Regra de Ouro: Qualidade over Pirotecnia**: 
    - É proibido o uso de animações complexas (ex: Ken Burns exagerado) que sacrifiquem a nitidez ou a credibilidade da marca. 
    - O padrão oficial é o **Static-to-Premium-Video**: Uma imagem estática de altíssima qualidade convertida em MP4 de 6 segundos.
2.  **Especificações de Renderização (High-Fidelity Rule)**:
    - **Bitrate**: Mínimo de 5000k.
    - **Compressão**: CRF 18 (Visual Lossless).
    - **Template**: Uso obrigatório do cabeçalho "SELEÇÃO TITANIUM" e badges de preço minimalistas harmonizados.
3.  **Case Study: Andréia (Integridade Confirmada)**:
    - O fluxo de interação (Postagem -> Comentário "QUERO" -> Resposta Pública -> DM Blindada) foi validado como 100% operacional. O uso de hashtags únicas (#titanium_UID) é a âncora de segurança que impede a perda de comissões.

*Última Auditoria Técnica: 17/05/2026 - Status: Datafeed Fallback & Sensual Filtering Active | Nuclear Shield v3.9 | Winter 2026 Strategy | Anti-Hallucination Matrix Active*
