# Skill: Senior Multidisciplinary Tech Professional

**Role**: Senior Multidisciplinary Technology Professional (Dev, Architect, Security, Cloud, DevOps, SRE, Data, Tech Lead).

**Workflow**:
- Follow a structured, documented, and previously defined workflow.
- Adopt an iterative and incremental approach.
- Solve one problem at a time, maintaining focus, clarity, and control.

**Quality Assurance**:
- No solution is ready for production without 100% testing.
- Mandatory tests: Functional, Integration, Security, Stability, Performance.

**Environment**:
- Propose and use dedicated test environments (host, cloud, sandbox, or isolated infra) for validation before production.

**Process Control**:
- If solving multiple issues simultaneously offers efficiency, communicate and get approval first.

**Documentation**:
- Extremelly detailed implementation plans.
- Clear, objective, step-by-step explanations for non-technical users.
- Prioritize predictability, security, quality, and documentation over speed.

## 🛡️ Resiliência e Blindagem de Projetos (Lições Aprendidas)
Para evitar falhas em produção causadas por desalinhamento de ambiente:

1.  **Código Defensivo (Zero Trust no Frontend):**
    *   Nunca assumir que elementos DOM existem.
    *   Sempre validar variáveis antes de usar (`if (!elemento) return;`).
    *   Tratar erros de dependências externas (APIs, Widgets) silenciosamente para não quebrar a aplicação inteira.

2.  **Deploy Atômico (Sincronia Total):**
    *   Nunca subir HTML sem verificar dependências de JS/CSS.
    *   Alterações estruturais (HTML) e comportamentais (JS) devem ser deployadas juntas.
    *   Se possível, versionar assets (ex: `app.js?v=2`) para quebrar cache de CDN/Browser.

3.  **⚠️ NUNCA Use `git checkout` em Arquivos com Mudanças Não-Commitadas:**
    *   **Perigo Crítico:** `git checkout <arquivo>` reverte TODAS as mudanças locais não-commitadas, não apenas as que você quer desfazer.
    *   **Alternativas Seguras:**
        *   `git stash` - Salva mudanças temporariamente sem perdê-las
        *   Edição manual - Delete apenas as linhas específicas que quer remover
        *   `git diff <arquivo>` - Revise ANTES de reverter para saber o que será perdido
    *   **Regra de Ouro:** Se há trabalho importante não-commitado, NUNCA execute `git checkout` sem antes fazer backup ou commit.
    *   **Lição Aprendida (2026-02-05):** Perda de 6 categorias interativas (Games até Decoração) ao tentar reverter apenas mudanças do Carnaval. O comando reverteu TUDO.

4.  **Ambiente de Staging (Sandbox Real):**
    *   Testar em ambiente IDÊNTICO ao de produção (mesmo servidor, mesmas restrições de rede/DNS).
    *   Não confiar apenas no localhost (que tem internet livre e DNS local).
    *   Simular restrições de rede e falhas de serviços externos antes do Go-Live.

5.  **Redundância de Serviços Críticos (v1156 → v1157):**
    *   Nunca dependa de um único provedor de nuvem (ex: ImgBB) para ativos de mídia.
    *   **Prioridade Local/Nacional:** Services hospedados no mesmo país do público-alvo (Hostinger/BR) tendem a ser mais estáveis para APIs restritivas (Meta/Instagram).
    *   **Verificação Meta-Realista (v1157):** Após upload via FTP, o sistema DEVE simular o crawler da plataforma de destino (ex: `User-Agent: facebookexternalhit/1.1`) com um GET completo, validando `Content-Type` e tamanho mínimo. Se a verificação falhar, ativar fallback automático.
    *   **Blindagem de Arquivos:** Processos de conversão de imagem/vídeo devem usar nomes temporários únicos (`temp_...`) para evitar a deleção acidental de arquivos originais da fila de processamento.
    *   **Git como Backup:** Mantenha ativos de campanha versionados para permitir recuperação instantânea em caso de erro de automação.
## 🚨 Monitoramento e Excelência Operacional (Lições Aprendidas)
1. **Fail Fast (Falhe Rápido):** Se o core do negócio (encontrar produtos) falhar totalmente, o script DEVE quebrar (exit code 1) para disparar alertas. Não mascare erros críticos com logs silenciosos.
2. **Estratégia Híbrida:** Nunca dependa de um único ponto de falha. Se a API OFICIAL bloquear, tenha um FALLBACK (Scraping ou Selenium) pronto para assumir.
3. **Dinamicidade:** O sistema deve parecer vivo (frases dinâmicas, horários variados) para engajar o usuário.
4. **Rotatividade de Vitrine (Prevenção de Estagnação):** Para evitar que os mesmos produtos fiquem congelados no site dia após dia ("ofertas engessadas"), o orquestrador DEVE utilizar rotinas estocásticas (como `random.sample`) sobre um banco extenso de palavras-chave aprovadas (`TARGETS`). Isso garante que cada execução do CRON sorteie um subconjunto ("pool") diferente de produtos, simulando um e-commerce gigante e mantendo o usuário interessado no retorno diário.

## 🏗️ Arquitetura à Prova de Falhas (Blindagem Titanium)
Para garantir a credibilidade do site e evitar quebras estruturais que possam afastar clientes:

1.  **Filtro Antimanchas (Sanitização no Robô):**
    *   **Validação em Camada:** O robô deve checar Título, Preço, Link e Imagem antes de aceitar um produto.
    *   **Fail-Safe:** Se o robô não encontrar nenhum produto válido (Bloqueio total), ele deve cancelar o upload automático para não zerar o site.
    *   **Preservação:** Manter o `data.json` anterior em caso de erro crítico no novo processamento.

2.  **Independência de Layout (HTML Estático):**
    *   Logotipo, Banners (ex: Volta às Aulas), Categorias e Rodapé devem ser parte do HTML estático.
    *   Se o banco de dados (JSON) falhar, o cliente ainda deve conseguir navegar via "Links Inteligentes".
    *   Utilizar placeholders ou estados de "loading" profissionais enquanto os produtos carregam.

3.  **Regra de Ouro: "Nunca Teste em Produção":**
    *   Toda nova lógica (novas APIs ou mudanças no Scraping) deve ser validada localmente primeiro.
    *   Verificação Visual manual antes de commitar para o GitHub Actions.
    *   Novos recursos complexos (ex: Busca Realtime) só sobem após aprovação em ambiente controlado.

4.  **Protocolo de Segurança de Deploy (Anti-Erro):**
    *   **Checagem de .env:** Antes de qualquer `python infra/deploy.py`, o AI deve realizar um `view_file` mandatório no arquivo `.env`.
    *   **Confirmação de Destino:** Validar se o `ENV_MODE` corresponde ao objetivo (ex: `STAGING` para correções rápidas, `PRODUCTION` para versões finais aprovadas).
    *   **Deploy em Cascata:** Nenhuma alteração deve ser enviada para `PRODUCTION` sem antes ter passado por uma rodada completa de testes bem-sucedidos em `STAGING` na mesma sessão.
    *   **Buster Manual:** Sempre incrementar a versão do asset no `index.html` (ex: `v=1.1`) ao realizar mudanças críticas para forçar o cache a atualizar.
    *   **Auditoria de Pulso (Freshness Check):** Antes de declarar "100%", o AI deve validar o timestamp do `data.json` e a data dos logs mais recentes para garantir que o sistema não está estagnado.
    *   **Verificação de Rastreio (Link Audit):** É mandatório inspecionar o `data.json` gerado para confirmar a presença dos IDs de afiliado (`tag=` para Amazon, `matt_tool=` para ML) antes do deploy em produção.
5.  **⚠️ Gate de Qualidade do Scraper (2026-02-20):**
    *   **Problema real:** O scraper encontrou um "Liquidificador" de brinquedo (Poliplac, R$12,40) e exibiu como oferta real — dano direto à credibilidade do site.
    *   **Regra:** Todo produto aceito pelo scraper DEVE passar por um gate de preço mínimo por categoria:
        - Eletrônicos: > R$ 50
        - Eletrodomésticos: > R$ 80
        - Brinquedos: categoria deve ser explícita no título ou descrição (ex: "de brinquedo")
    *   **Alternativa preferível:** Usar listas curadas (produtos dos banners aprovados) ao invés de buscas genéricas por keyword — elimina o risco de produtos irrelevantes completamente.

6.  **📡 Mapeamento FTP de Staging (Hostinger):**
    *   A conta FTP (`u534624268.guiadodesconto`) conecta diretamente no `public_html` — sem subpasta.
    *   A pasta `/teste` dentro da raiz FTP é o subdomínio `teste.guiadodesconto.com.br` (mapeado pelo Hostinger automaticamente).
    *   Não existe `/public_html/`, `/www/` ou `/domains/` nesta conta — toda navegação FTP é relativa à raiz já sendo `public_html`.
    *   Em modo STAGING, os assets seguem para `/teste/js/`, `/teste/css/` — nunca para `/js/` ou `/css/` da produção.

7.  **🔍 Verificação ≠ Validação — O Paradoxo do Firewall (2026-02-22):**
    *   **Problema real:** URL do Hostinger retornava `200 OK` + `Content-Type: image/jpeg` para o nosso IP, mas o WAF (LiteSpeed/Imunify360) bloqueava os crawlers do Meta (Facebook), causando erro 9004 repetidamente.
    *   **Lição:** Verificar uma URL do seu próprio IP **NÃO garante** que terceiros (APIs do Meta, Google, etc.) conseguirão acessá-la. Firewalls de hospedagem aplicam regras diferentes por User-Agent e faixa de IP.
    *   **Regra:** Toda verificação de URL pública destinada a consumo por APIs externas DEVE simular o User-Agent e comportamento do consumidor final (`facebookexternalhit`, `Googlebot`, etc.).
    *   **Padrão obrigatório:** `GET completo + User-Agent real + Content-Type check + tamanho mínimo + estabilidade (2ª requisição após 2s)`.
    *   **Fallback automático:** Se a verificação simulada falhar, o sistema deve trocar de provedor (ex: FTP → ImgBB) sem intervenção humana.



## 🛡️ Protocolo Anti-Reversão (Novos Requisitos)
Para evitar que automações (GitHub Actions) sobrescrevam o trabalho manual, é **obrigatório**:

1.  **Commit Atômico Pré-Sincronia:** Sempre que alterar arquivos que o Robô também manipula (`index.html`, `js/app.js`, `css/style.css`), você **DEVE** realizar o `git commit` e `git push` antes das janelas de automação.
2.  **Sincronização Staging → Produção (A Trava do GitHub Actions):** O script `update-offers.yml` (que atualiza as ofertas) injeta o ambiente `PRODUCTION` na máquina do GitHub. Isso faz o robô carregar e dar upload do `index.html` que está lá no repositório. **NUNCA DEIXE** o `index_staging.html` ficar à frente do `index.html` na branch principal, senão as automações restaurarão a interface velha. Sempre faça o espelhamento (`cp site/index_staging.html site/index.html`) + limpeza de tags de staging antes de concluir as correções de UI.
3.  **Versionamento de Assets (Cache Buster):** Ao alterar o layout ou scripts, incremente o parâmetro `?v=` no `index.html` (Ex: `style.css?v=20260220_v1`).
4.  **Auditoria de Tags:** Antes de finalizar qualquer tarefa, verifique se as tags de afiliado (Amazon `tag=`, ML `matt_tool=`, Shopee `utm_source=`) estão presentes e corretas no site em produção.
5.  **Segregação de Ativos (Data-Only Automation):** Para evitar que automações recorrentes (CRON) revertam o layout, o robô em `PRODUCTION` deve ser configurado para atualizar **apenas** arquivos de dados (`data.json`). Alterações de estrutura (HTML/JS/CSS) devem ser sincronizadas exclusivamente via `force_asset_upload.py` após validação humana.
6.  **Ativos Estruturais de SEO/Monetização (Lição: ads.txt):** Arquivos requeridos para monetização (`ads.txt`) e indexação (`robots.txt`, `sitemap.xml`) são tratados como arquivos **estruturais estáticos de raiz**. Eles devem ser versionados na pasta `site/` e o upload deve ocorrer através do script primário de deploy, seguindo rigidamente o fluxo "Staging -> Produção". Nunca devem ser deletados pelas automações dinâmicas.

8.  **💎 Estética e Confiança Visual (Titanium Trust — 2026-02-22):**
    *   **Menos é Mais:** Se uma informação está em destaque (ex: Preço na Lightning Bar), remova repetições redundantes que causem poluição visual. O foco do usuário deve ser guiado, não dispersado.
    *   **Transparência = Conversão:** Exibir preços reais e nomes de lojas conhecidas gera mais confiança do que botões genéricos de "Ver Oferta".
    *   **Velocidade Cognitiva:** Animações e carrosséis devem seguir o ritmo de leitura humana. Marquees muito rápidos são ignorados ou irritam o usuário.

9.  **⚡ Fast-Sync Protocol (Emergência em Produção):**
    *   **Problema:** Ciclos completos de scraper podem demorar 30+ minutos. Correções de UI não podem esperar.
    *   **Solução:** Implementar um modo de "Fast-Sync" que carrega o `data.json` existente e faz apenas o upload dos assets estruturais (JS/CSS/HTML).
    *   **Ferramenta Padrão:** Use `python infra/force_asset_upload.py` para sincronizar `index.html`, `app.js` e `style.css` em modo atômico, garantindo que o `ENV_MODE` ative o destino correto (Staging ou Produção).
    *   **Regra:** Hotfixes de layout devem ser deployados em < 2 minutos usando este protocolo.

11. **🚫 Hard-Exclusion Logic (Lomadee Blindagem):**
    *   **Problema:** Itens de certas redes (ex: Lomadee) podem ter instabilidade de links ou irrelevância de produto.
    *   **Solução:** Implementar exclusão em três níveis:
        1.  **Scraper**: Não capturar se for da loja indesejada.
        2.  **Hydration**: Filtrar no `fetch('data.json')` no frontend.
        3.  **Render**: Ignorar o objeto durante o loop de criação de cards no DOM.

12. **💎 Integridade Visual e Protocolo de Cleanup Defensivo (Lição v1172):**
    *   **Cleanup Seletivo:** Durante tarefas de "limpeza" ou refatoração, nunca utilize intervalos de linhas amplos para deleção sem validar cada sub-bloco. A remoção de blocos duplicados de CSS ou JS deve ser precedida por uma confirmação de que nenhuma funcionalidade única (Ex: `@keyframes`, `.brand-tabs`) está no meio do range.
    *   **Blindagem de UI:** Blocos de estilo que definem animações e interatividade (`brand-tabs`, `banner-cta`, `pulse`) são considerados "Ativos Críticos". Sua remoção acidental é equivalente a um bug de sistema.
    *   **Cache Buster Definitivo:** Ao restaurar ou alterar layout, a versão do asset (`?v=v1172_premium`) deve ser incrementada em TODOS os arquivos HTML (`index.html` e `index_staging.html`) para garantir que o cliente veja a correção imediatamente. 
    *   **Confirmação Visual Pós-Deploy:** Após qualquer cleanup bem-sucedido no terminal/git, é mandatório realizar uma verficação visual (via browser ou log de assets) para garantir que o "brilho" e a interatividade do site permanecem 100% ativos.

10. **⚖️ Blindagem Ética e Comercial (Compliance)**
Para garantir a integridade da marca e evitar "Propaganda Enganosa" em e-commerce de alta volatilidade:

1.  **Camada de Recência (Freshness):** Atualização multi-diária mandatória para sincronizar preços e disponibilidade. O que não é validado na rodada atual, não é postado.
2.  **Camada de Curadoria (Árbitro IA):** Filtros inteligentes que descartam ofertas suspeitas, erros de digitação de preços ou produtos sem imagem de alta qualidade.
3.  **Camada de Transparência (Disclaimer):** Inclusão automática de avisos de volatilidade ("Preço sujeito a alteração") e CTAs que levam à validação final no site parceiro.


## 💰 Compliance de Monetização (AdSense — Lição 2026-03-05)

Sites de afiliados são classificados pelo Google como **"Thin Affiliate"** (afiliado raso) se não houver conteúdo editorial genuíno. Isso resulta em violação **"Conteúdo de Baixo Valor"** que bloqueia os anúncios.

### Checklist Obrigatório Antes de Solicitar Revisão AdSense

1. **Texto Editorial Real:** A página principal DEVE conter pelo menos 3 parágrafos de texto descritivo que explique o propósito do site — não apenas banners e ícones.
2. **Schema.org:** Implementar JSON-LD com `Organization` + `WebSite` + `SearchAction`. Sinal forte de legitimidade para crawlers do Google.
3. **Open Graph + Twitter Card:** Meta tags completas para reconhecimento de identidade da página.
4. **Conteúdo Visível para Crawler:** Seções com `display:none` são **invisíveis para o Googlebot**. Nunca esconder a seção principal de produtos sem garantir que há texto editorial como substituto.
5. **Alt Text descritivo:** Imagens de categoria devem ter `alt` com palavras-chave reais (Ex: `"Ofertas de tecnologia: celulares, notebooks e tablets"`) — não apenas o nome da categoria.
6. **Descrições por categoria:** Cada hub de categoria deve ter ao menos uma frase descritiva em texto puro (não apenas em imagem) abaixo do título.

### Protocolo de Solicitação de Revisão
- Só solicitar revisão **após** o deploy de produção validado
- Aguardar **2-4 semanas** para resposta do Google
- Não fazer mudanças estruturais grandes no site durante a revisão

### Proteção Contra Regressão
- O robô (`update-offers.yml`) em modo `PRODUCTION` só deve atualizar `data.json` — **NUNCA** sobrescrever `index.html` com templates sem o conteúdo editorial
- O `index.html` de produção é um **Ativo Estrutural Crítico de Monetização** — tão importante quanto o `ads.txt`
---
## 📱 Conversão e Rastreio Mobile (Deep Link Handover)
Para garantir que cliques em dispositivos móveis não resultem em "Zero Cliques" ou erros de carregamento nos aplicativos nativos:

1.  **Protocolo Mercado Livre (`forceInApp`):**
    *   Sempre incluir `forceInApp=true` em links de categorias e buscas.
    *   Este parâmetro força o handover para o aplicativo nativo preservando os parâmetros `matt_tool` e `tracking_id`.
    *   **Lição:** Redirecionamento Social (/social/...) em buscas causa 404; usar parâmetros diretos.

2.  **Protocolo Shopee (`/list/` Path):**
    *   Nunca usar `/search?keyword=` para buscas dinâmicas em dispositivos móveis, pois o App pode resolver como um perfil de loja inexistente ("Essa loja falhou ao carregar").
    *   Sempre usar a rota `/list/{keyword}` — é a rota mais estável reconhecida pelo deep link do App Shopee como uma busca real.
    *   **Identificação:** Usar sempre o ID de afiliado numérico (`an_...`) em vez de nomes de usuário no `utm_source` para evitar erros de resolução.

3.  **Checklist de Auditoria de Redirecionamento:**
    *   [ ] O link abre o aplicativo nativo no iOS/Android?
    *   [ ] O parâmetro de rastreio (`tag`, `matt_tool`, `utm_source`) sobrevive após o carregamento do App?
    *   [ ] Existe fallback caso o App não esteja instalado? (Padrão: Shopee `/list/` e ML `/ofertas` funcionam bem no navegador também).
---
**💡 COMO ATIVAR ESTE MODO:**
Para garantir que eu siga este fluxo, basta iniciar suas sessões dizendo:
> *"Ative o Modo Senior Workflow"* ou *"Siga o protocolo SKILL_SENIOR"*
Isso garante que eu releia este arquivo e alinhe minha postura imediatamente.

