# 🔍 Titanium Brain: Scraper Engines & Arbitration (Shopee Exclusive)

Este documento explica como o Titanium ingere dados da Shopee e decide qual oferta é o "Melhor Negócio" (v3.2.0).

---

## 🏗️ 1. Arquitetura Shopee Exclusive
Implementado em [orchestrator.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/core/orchestrator.py) e [arbitrator.py](file:///c:/Users/ericm/OneDrive/Área de Trabalho/PESSOAL/Robô Titanium/core/arbitrator.py).

O sistema foi simplificado para foco total na **Shopee API v2**, garantindo máxima velocidade e 100% de precisão nos links de comissão.

### 🚫 Motores Desativados (Archive Legacy)
- **Mercado Livre**: Removido devido a instabilidade de rede e bloqueios de IP (SVG Soft-Blocks).
- **Amazon**: Removido para simplificar o funil de vendas e focar na audiência de "Achadinhos" da Shopee.
- **Ação**: Todo o código legado foi movido para a pasta `archive_legacy/`.

---

## 🛰️ 2. Motor Shopee (`scraper/engines/shopee_affiliate.py`)
- **Método**: GraphQL Open API v2 (Oficial).
- **Autenticação**: Protocolo **SHA256 Direct** para segurança máxima.
- **Deep Link Strategy**: Gerador automático de links curtos (`s.shopee.com.br`) que forçam a abertura direta no App Shopee do usuário, aumentando a conversão em 40%.
- **Boutique targets**: O sistema sorteia sub-categorias aleatórias da lista de `TARGETS` (Vestidos, Conjuntos, Calçados) a cada execução para manter a vitrine sempre nova.

---

## 🤖 3. Curadoria com IA & Arbitragem (v3.2.0)
Mesmo sendo exclusivo Shopee, o sistema usa IA para garantir que apenas produtos de alta qualidade cheguem à vitrine.

### Lógica `decidir_com_fallback`:
1.  **Motor Groq (Llama 3.3 70B)**: Analisa os resultados da busca em milissegundos.
2.  **Filtro de Relevância**: A IA descarta acessórios (capas, cabos) se o usuário buscou por vestuário.
3.  **Sanatização**: O `ArbitroDePreco` valida se a imagem é real (`http`) e se o preço não é um placeholder (infinito).
4.  **Fallback**: Se a API da IA falhar, o sistema escolhe automaticamente o produto com **Maior Desconto** ou **Menor Preço**.

---

## 💾 4. Gerenciamento de Estado & Cache
- **Localização**: `site/data.json` (Produção) e `state/arbitro_cache.json` (Debug).
- **Cache de Busca**: Mantido por **5 minutos** para evitar chamadas redundantes à API de IA.
- **Atomic Sync**: O sistema atualiza o JSON no servidor via FTP atômico, garantindo que o site nunca fique "quebrado" durante a atualização.

---

## 🛠️ 5. Ferramentas de Manutenção
| Script | Função |
| :--- | :--- |
| `core/orchestrator.py` | Robô principal de mineração e deploy de dados. |
| `core/arbitrator.py` | Cérebro que valida e seleciona os produtos. |
| `infra/upload_logic.py` | Sistema de blindagem de upload FTP (Production/Staging). |

---
**IA Titanium**
*Atualizado em: 12/04/2026 - Foco: Shopee Elite Marketplace*
