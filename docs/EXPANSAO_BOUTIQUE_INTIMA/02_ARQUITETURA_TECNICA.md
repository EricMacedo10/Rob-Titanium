# ⚙️ Expansão: Boutique Sensual Íntima (v1.1)
## Documento 02: Arquitetura Técnica e Integração (Status: OPERACIONAL)

> [!TIP]
> **Diferencial Técnico**: Implementado o selo dinâmico `TITANIUM CHOICE` no arquivo `app_sensual.js` para destacar ofertas com desconto superior a 30% via CSS Glassmorphism.

Este documento detalha como a nova vertical se integra ao sistema **Titanium v3.8** existente.

---

### 1. 📂 Estrutura de Arquivos
A expansão utiliza a infraestrutura "Stateless" atual:
*   `site/sensual.html`: Template exclusivo com paleta de cores e scripts específicos.
*   `site/data_sensual.json`: Pool de produtos minerados do Datafeed de 100K exclusivo para este nicho.
*   `site/js/app_sensual.js`: Motor de renderização adaptado para os filtros de bem-estar íntimo.

### 2. 🛰️ Motor de Mineração (Datafeed Elite)
O script `scraper/datafeed_shopee.py` será instruído a rodar um ciclo específico:
1.  **Keywords**: `vibrador`, `sugador`, `lingerie`, `camisola cetim`, `lubrificante intimo`.
2.  **Filtros de Qualidade**: 
    *   `Min_Rating`: 4.5
    *   `Shop_Type`: Preferred / Shopee Mall.
3.  **Saída**: Destino automático para `site/data_sensual.json`.

### 3. 🛡️ Integração com o Nuclear Shield (v3.8)
A nova vertical herda automaticamente todas as proteções:
*   **Global Click Interceptor**: Todos os cliques em lingerie ou toys são capturados e auditados para injetar a tag `an_18318830863`.
*   **MutationObserver**: Links dinâmicos injetados pela IA são corrigidos em milissegundos.
*   **Atomic FTP Sync**: O deploy da Boutique Sensual não afeta a estabilidade da Boutique Titanium principal.

### 4. 📈 Tracking e Analytics
Novas metas de eventos no GA4:
*   `sensual_view`: Visualização de itens da vertical.
*   `sensual_click`: Clique em produtos sensuais.
*   `category_switch_sensual`: Troca entre categorias dentro da boutique.

---
**Regra de Ouro**: O arquivo `sensual.html` deve manter o mesmo cabeçalho (`<header>`) da Titanium para permitir a transição fluida do usuário entre os dois "mundos".
