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
- **`state/` Directory**: Do not commit this folder. It contains volatile but critical session tokens.
- **Affiliate Tag Logic**: Do not hardcode tags in the middle of functions. Always use `core/settings.py` or the `app.js` config block.

## 🛠️ Troubleshooting Guide

| **Symptom** | **Probable Cause** | **Action** |
| :--- | :--- | :--- |
| **Site Empty** | `data.json` is 0KB or invalid. | Check `orchestrator.log` for Scraper blocks. |
| **Links not tracking** | Tag normalized incorrectly. | Check `normalizeStore` logic in `app.js`. |
| **ML Search Failing** | (LEGACY) Mercado Livre desativado. | Consultar `archive_legacy/` se necessário. |
| **Social Bot not posting** | IG Container Timeout / code 9004. | Prioritize Hostinger (FTP) over ImgBB. |
| **File Deletion Bug** | Shared filename in tmp logic. | Use Unique Timestamped Temps (Rule of Traceability). |
| **Lightning Bar não aparece** | `staging-mode` class ausente OU URL não contém 'staging'. | Verificar se `index.html` do subdomínio é o `index_staging.html`. Checar condição de ativação no `app.js`. |
| **Elemento persiste após JS remover** | Cache do browser ou `display:block` inline do JS. | Adicionar `display: none !important` no CSS como camada definitiva. |
| **Upload FTP não navega para subpasta** | `upload_logic.py` sem navegação recursiva. | Usar `_ensure_remote_dir()` que cria subpastas automaticamente. |
| **ML produtos com erro** | (LEGACY) Mercado Livre desativado. | Engine atualizado para foco 100% Shopee. |
| **GitHub Action sobrescreve vitrine temática** | `core/settings.py` com keywords antigas (e.g. Ring Light). | Atualizar TARGETS no `settings.py` para as palavras-chave do novo nicho ANTES do próximo cron run. |
| **data.json no server ainda mostra conteúdo antigo após deploy.py** | `deploy.py` exclui `data.json` por design (segurança). | Rodar manualmente `infra/upload_data.py` para fazer o override do JSON no servidor. |
| **Robô de DM (`bot_instagram.php`) parou de funcionar** | Token expirado (OAuthException 190/463). | Renovar token, atualizar `.env` e `social/bot_instagram.php`, depois rodar `python c:/tmp/upload_bot.py` para subir ao servidor. |
| **Robô de DM envia o link errado** | `ofertas.json` está desatualizado ou sem a hashtag do post. | Atualizar `social/ofertas.json` com a hashtag do novo post e rodar `python c:/tmp/upload_bot.py`. |


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
- **`social/post_fashion_carousel.py`** *(2026-03-21)*: Faz upload das imagens da fila via `ResilientUploader` e publica como Carrossel no Instagram via `InstagramClient.post_carousel()`. Executar com `python -m social.post_fashion_carousel` a partir da raiz do projeto.
- **`social/bot_instagram.php`** *(Servidor Hostinger, raiz `/`)*: Bot PHP do robô de DM. Monitora comentários dos últimos 6 posts, detecta gatilhos e envia DM com link correto baseado no `ofertas.json`.
- **`social/ofertas.json`** *(Servidor Hostinger, raiz `/`)*: Dicionário de hashtags→links. Atualizar a cada novo post e fazer upload via `python c:/tmp/upload_bot.py`.
- **`social/titanium_token_manager.py`** *(2026-03-21)*: Gerenciador automático de tokens Meta/Instagram. Troca o User Token por um **Page Access Token permanente (♾️ nunca expira)** e atualiza o `.env`, `bot_instagram.php` e faz upload para o servidor em uma única execução. Executar com `python -m social.titanium_token_manager`.

## 🚀 Hotfixes e Deploy Emergencial (Senior Only) [30/03]

Para correções estruturais (CSS/JS) no Staging ou Produção:

1.  **Cache-Busting Mandatório**: SEMPRE incremente a versão `?v=X.X` nas tags de `<link>` ou `<script>` do HTML ao subir alterações estéticas.
2.  **Upload de HTML Atômico**: O script de Hotfix (`upload_hotfix_js.py`) deve enviar o arquivo HTML versionado **junto** com os ativos modificados.
3.  **Validação Visual de Dispositivo**: Antes de declarar vitória, valide via screenshot a integridade do layout (Overflow, Alinhamento de Badges e Colisões de Estilo).

---
## 🚀 AI-Driven Trend Radar (v3.5)

O Titanium opera agora sob o regime de **Radar de Tendências Ativo**:
1. **Filtro de Desejo**: A IA DeepSeek-V3.2 (Speciale) não apenas analisa preços, mas a "curva de desejo" (Fashion Intensity) de cada item via Extreme Reasoning.
2. **Editorial On-the-Fly**: Textos curtos e persuasivos são injetados no frontend para evitar o estigma de "site de links" (Thin Affiliate Defense).
3. **Blindagem de Atribuição (Universal Linker)**: 
   - NUNCA gerar um link fora do wrapper `build_affiliate_link`.
   - Garantir que o `utm_source` seja sempre `titanium_radar` para facilitar a auditoria no painel da Shopee.

*Última Auditoria Técnica: 15/04/2026 - Status: 100% Shopee Exclusive.*
