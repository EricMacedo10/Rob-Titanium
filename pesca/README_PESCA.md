# 🎣 Robô Pesca Titanium — Guia de Configuração

Bot de publicação automática para a conta **@pescatitanium** no Instagram.
Completamente independente do **Titanium Boutique** (bot de moda).

---

## 📁 Estrutura de Arquivos

```
pesca/
├── __init__.py                  ← Módulo Python
├── automate_pesca.py            ← Script principal (Reels + Stories)
├── datafeed_pesca.py            ← Acesso ao feed de produtos de pesca
├── video_generator_pesca.py     ← Gerador de vídeo (visual de pesca)
├── ofertas_pesca.json           ← Mapa hashtag → link (bot de comentários)
├── postados/                    ← Estado: produtos já publicados
├── fila/                        ← Estado: produtos na fila de publicação
└── README_PESCA.md              ← Este arquivo
```

---

## 🔑 Secrets Necessários no GitHub

Configure em: **Repositório → Settings → Secrets and variables → Actions → New repository secret**

| Secret Name | Valor | Descrição |
|---|---|---|
| `PESCA_IG_ACCESS_TOKEN` | (token longo) | Token de acesso da Pesca Titanium |
| `PESCA_IG_BUSINESS_ID` | `17841416991677908` | ID da conta IG Business |
| `PESCA_PAGE_ID` | `1165552696646721` | ID da Página do Facebook vinculada |
| `PESCA_IMGBB_API_KEY` | (chave ImgBB) | CDN para upload de vídeos |
| `PESCA_SHOPEE_DATAFEED_URLS` | (URL do feed CSV) | Feed de produtos de pesca Shopee |

> **Nota:** O secret `IMGBB_API_KEY` (sem prefixo) já existente é usado como fallback automático se `PESCA_IMGBB_API_KEY` não for criado.

---

## 📅 Agendamento dos Workflows

| Workflow | Horário BRT | Tipo de Post |
|---|---|---|
| `pesca_reels_stories_auto.yml` | 10h e 16h | Reel + Story |
| `pesca_social_auto.yml` | 07h e 18h | Reel no Feed |

---

## 🚀 Como Testar Manualmente

1. Acesse o repositório no GitHub
2. Clique em **Actions**
3. Selecione **🎣 PESCA TITANIUM: Reels & Stories**
4. Clique em **Run workflow** → **Run workflow** (botão verde)
5. Acompanhe os logs em tempo real

---

## 🎨 Identidade Visual

- **Fundo:** Gradiente azul-marinho profundo (#081C3C → #043C50)
- **Card:** Branco com borda dourada (#B88E28)
- **Preço:** Azul royal (#0064B4)
- **Label:** "🎣 PESCA TITANIUM"
- **CTA:** "Comente QUERO para receber o link 🎣"

---

## ♻️ Renovação do Token

O token de acesso **expira em 10/08/2026**. Para renovar:
1. Acesse [developers.facebook.com](https://developers.facebook.com)
2. Ferramentas → Explorador da Graph API
3. Gere novo token com escopos: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`
4. Troque o valor do secret `PESCA_IG_ACCESS_TOKEN` no GitHub

---

## ⚠️ Isolamento de Bots

Este bot usa:
- **Lock file separado:** `state/pesca_post.lock` (≠ `state/post.lock` do bot de moda)
- **Concurrency groups distintos:** `pesca-reels-stories` e `pesca-social`
- **Estado próprio:** `pesca/postados/` e `pesca/fila/`
- **Secrets prefixados:** Todos começam com `PESCA_`

Isso garante que **nenhuma execução do bot de pesca interfere no bot de moda**, e vice-versa.
