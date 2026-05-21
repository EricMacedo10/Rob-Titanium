Este documento explica como o Titanium ingere dados da Shopee e decide qual oferta é o "Melhor Negócio" (v3.8.0-Nuclear).

---

## 🏗️ 1. Arquitetura Shopee Exclusive
Implementado em [orchestrator.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/core/orchestrator.py) e [arbitrator.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/core/arbitrator.py).

O sistema foi simplificado para foco total na **Shopee API v2**, garantindo máxima velocidade e 100% de precisão nos links de comissão.

### 🚫 Motores Desativados (Archive Legacy)
- **Mercado Livre**: Removido devido a instabilidade de rede e bloqueios de IP (SVG Soft-Blocks).
- **Amazon**: Removido para simplificar o funil de vendas e focar na audiência de "Achadinhos" da Shopee.
- **Ação**: Todo o código legado foi movido para a pasta `archive_legacy/`.

---

## 🛰️ 2. Motor Shopee Massive Datafeed (`scraper/datafeed_shopee.py`)
- **Método**: Download de CSV oficial (100.000+ produtos).
- **Domínio Absoluto (v4.0)**: O Datafeed de Moda & Beleza é agora o coração 100% autônomo do site. Ele alimenta OBRIGATORIAMENTE 3 setores primários de forma autônoma:
  1. `core/orchestrator.py` (Vitrines Diárias)
  2. `core/review_engine.py` (Radar de Tendências IA com 18 itens de grade simétrica)
  3. `core/curator_csv_to_json.py` (Coleção Platinum/Seleção da Especialista)
  4. `core/auto_blog_generator.py` (Triple-Core Editorial: 3 categorias renovadas semanalmente)
- **Filtragem**: O sistema filtra por categorias de interesse (Moda e Beleza) e palavras-chave de "luxo".
- **Busca de Imagem**: Como o CSV não contém imagens, o sistema usa o `TitaniumArbitrator._fetch_image_for_product()` para buscar a miniatura oficial via GraphQL usando as 5 primeiras palavras do título.
- **Vantagem**: Escala massiva sem risco de banimento de IP por excesso de requisições e 100% rastreabilidade via API.

## 📡 3. Motor Shopee API (`scraper/engines/shopee_affiliate.py`)
- **Método**: GraphQL Open API v2 (Oficial).
- **Papel Atual**: Atua como **Fonte de Fallback** e buscador de imagens para o Datafeed.
- **Autenticação**: Protocolo **SHA256 Direct** para segurança máxima.
- **Deep Link Strategy**: Gerador automático de links curtos (`s.shopee.com.br`) que forçam a abertura direta no App Shopee.

---

## 🤖 3. Curadoria com IA & Arbitragem (v3.2.0)

### 🛡️ Fallback API Resilience (v5.4.2)
O `orchestrator.py` garante inclusão atômica de ofertas provindas da API GraphQL de Fallback, caso as URLs do Datafeed de 100K expirem, preservando a consistência da vitrine (evitando travamento por Lista Vazia).
Mesmo sendo exclusivo Shopee, o sistema usa IA para garantir que apenas produtos de alta qualidade cheguem à vitrine.

### Lógica `decidir_com_fallback`:
1.  **Motor DeepSeek-V3.2 (Speciale)**: Analisa os resultados da busca com Extreme Reasoning, garantindo curadoria de elite.
2.  **Filtro de Relevância**: A IA descarta acessórios (capas, cabos) se o usuário buscou por vestuário.
3.  **Sanatização**: O `ArbitroDePreco` valida se a imagem é real (`http`) e se o preço não é um placeholder (infinito).
4.  **Fallback**: Se a API da IA falhar, o sistema escolhe automaticamente o produto com **Maior Desconto** ou **Menor Preço**.

---

## 💾 4. Gerenciamento de Estado & Cache (Refresh Strategy 80+100)
- **Localização**: `site/data.json` (Produção) e `state/arbitro_cache.json` (Debug).
- **Refresh Strategy**: A cada rodada, o sistema preserva até **80 produtos históricos** do Shopee e injeta até **100 novas ofertas** válidas.
- **Master Deduplication**: Antes de salvar o `data.json`, o sistema realiza o cross-check mandatório contra `specialist.json` (Platinum) e `ai_reviews.json` (IA Radar). Qualquer ID duplicado é removido da vitrine principal para dar lugar a itens novos.
- **Atomic Sync**: O sistema atualiza o JSON no servidor via FTP atômico, garantindo que o site nunca fique "quebrado" durante a atualização.

---

## 🛠️ 5. Ferramentas de Manutenção
| Script | Função |
| :--- | :--- |
| `core/orchestrator.py` | Robô principal de mineração e deploy de dados. |
| `core/arbitrator.py` | Cérebro que valida e seleciona os produtos. |
| `infra/upload_logic.py` | Sistema de blindagem de upload FTP (Production/Staging). |
| `scraper/datafeed_shopee.py` | Engine de download do CSV. Reconfigura stdout para utf-8 no Windows preventivamente e suporta múltiplas URLs (separadas por pipe no `.env`). |

---
---
**IA Titanium**
*Atualizado em: 21/05/2026 - Versão: v5.4.3-Elite (Multi-URL Datafeed & Unicode Fix)*
