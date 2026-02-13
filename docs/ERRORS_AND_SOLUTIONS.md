# 🛠️ Erros e Soluções - Robô Titanium

Este documento registra os desafios técnicos encontrados durante o desenvolvimento e as soluções implementadas para garantir a estabilidade do sistema.

## 1. Bloqueio de Scraping (Mercado Livre)

**Erro:** O GitHub Actions retornava erro `403 Forbidden` ou `Timeout` ao tentar rodar o Selenium para extrair dados do Mercado Livre, devido à detecção de bot por IP de datacenter.

**Solução:** 
- Implementação de um **Scraper Híbrido**.
- Substituição da navegação via browser por chamadas à **API Oficial do Mercado Livre**.
- Uso de `MELI_REFRESH_TOKEN` para autenticação persistente.
- Caso a API falhe, o sistema redireciona o usuário para o termo de busca pesquisado via URL de afiliado.

## 2. Busca Travada e Label "(cache)"

**Erro:** A busca no site exibia a etiqueta "(cache)" em todos os resultados e, ocasionalmente, parava de funcionar (Uncaught TypeError).

**Causa:** Existência de código legado e duplicado no `app.js`. Dois blocos de funções de busca (`searchRealTime` e `renderSearchResults`) estavam competindo entre si e referenciando elementos que nem sempre estavam no DOM.

**Solução:**
- **Consolidação de Logística:** Remoção de mais de 280 linhas de código obsoleto.
- Implementação de uma busca unificada que verifica a existência de elementos (`if (searchInput)`) antes de adicionar listeners.
- Limpeza da interface para remover labels confusas de debug.

## 3. Falha no Deploy Automático (Paths)

**Erro:** O workflow do GitHub Actions concluía com sucesso, mas os novos produtos ou mudanças de CSS não apareciam no site.

**Causa:** 
1. O caminho remoto no FTP estava incorreto (tentava subir em pastas como `public_html` que não existem na raiz da Hostinger contratada).
2. O browser mantinha arquivos antigos em cache.

**Solução:**
- **Debug de FTP:** Criação de script `debug_ftp_path.py` para mapear a raiz do servidor.
- **Correção de Workflow:** Ajuste do destino para a raiz `/` do FTP.
- **Cache Busting:** Implementação de versionamento agressivo no `index.html` (ex: `style.css?v=v9_clean`).

## 4. Limite de Rate (Groq API)

**Erro:** Erro `429 Too Many Requests` ao usar a IA para curadoria de produtos (mais de 100k tokens consumidos no plano gratuito).

**Solução:**
- Implementação de **Mecanismo de Fallback**.
- Caso a IA falhe, o robô ordena os produtos encontrados por preço e seleciona o item mais barato automaticamente, garantindo que a atualização do `data.json` nunca seja interrompida por fatores externos.

## 5. UI: Imagens e Layout

**Erro:** Imagens de produtos vinham com tamanhos desproporcionais ou links quebrados (placeholder do ML).

**Solução:**
- Padronização de containers CSS (250px fixos com fundo branco e `object-fit: contain`).
- Implementação do `handleImageError` em JS para substituir imagens quebradas por logos estilizados das lojas parceiras.

## 6. Interface Hub: Sincronização de Abas (v1136)

**Erro:** Ao carregar a página, a aba ativa definida pelo rodízio automático não sincronizava visualmente com a imagem do banner inicial.

**Solução:** 
- Adição de um disparo programático de evento: `activeTab.click()`.
- Isso garante que a lógica de troca de imagem e redirecionamento seja disparada no segundo zero, mantendo a UI 100% alinhada com o conteúdo.

## 7. Z-Index: Sobreposição de Header (v1137)

**Erro:** As abas flutuantes de marcas do Hub interativo apareciam "na frente" do menu principal (sticky header) durante a rolagem da página.

**Solução:** 
- Elevação do `z-index` do header para `1000` (camada de prioridade máxima).
- Ajuste das `.brand-tabs` para `z-index: 80`, garantindo que fiquem acima do banner mas abaixo da navegação principal.

## 8. Design: Visibilidade de Logos (v1139)

**Erro:** Logos com cores claras ou símbolos finos (como o aperto de mãos do Mercado Livre) perdiam definição ou "sumiam" em fundos claros/amarelos.

**Solução:** 
- Aplicação de filtro `drop-shadow` multi-direcional no CSS.
- Criação de um contorno (stroke) nítido de 1.5px ao redor dos símbolos usando a cor azul marinho oficial, aumentando drasticamente o contraste e a legibilidade.

## 9. Segurança: Injeção de Scripts e Proteção de Ganhos (v1140)

**Risco:** Vulnerabilidade a ataques de injeção e sequestro de links de afiliados (hijacking).

**Solução (Blindagem Titanium):** 
- **CSP (Content Security Policy):** Implementação de meta-tags rigorosas que impedem o carregamento de qualquer script não autorizado.
- **SRI (Subresource Integrity):** Adição de hashes criptográficos aos links do FontAwesome para garantir que os ícones baixados não foram alterados.
- **Bot Honeypot:** Criação de armadilhas invisíveis para detectar robôs maliciosos tentando copiar o site.

## 10. Reels: Processamento Infinito ("Pendente")

**Erro:** Vídeos enviados via API ficavam travados em status "Pendente" por horas, causando timeout no script.

**Causa:** Vídeos em alta resolução (1080p/38MB) sobrecarregam a transcodificação na nuvem da Meta para contas automatizadas.

**Solução:**
- Padronização para **720p (720x1280)**.
- Redução de tamanho para ~2.5MB, garantindo processamento instantâneo (< 60s).

## 11. Automação: Conflitos de Sincronia (Archival)

**Erro:** O robô falhava ao tentar mover arquivos no GitHub Actions porque a pasta local estava "desalinhada" com o repositório remoto.

**Solução:**
- Implementação de `git pull --rebase` antes do push no workflow de CI/CD.
- Isso garante que o executor do GitHub sempre tenha o estado mais recente antes de arquivar novas postagens.

## 12. Instagram API: Erro 400 no Polling

**Erro:** O polling de status de vídeo retornava `400 Bad Request` aleatoriamente.

**Causa:** Solicitar o campo `failure_reason` antes que um erro ocorra é considerado inválido por certas versões da Graph API.

**Solução (Smart Polling):**
- O script agora solicita apenas o `status_code` durante a espera.
- O campo `failure_reason` só é requisitado se o status for explicitamente `ERROR`.

---
*Última atualização: 13/02/2026 (v1151 - Senior Workflow Fix)*
