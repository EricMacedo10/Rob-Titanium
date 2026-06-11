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

## 🔗 Deep Link Proxy e Rastreamento (Open Graph)

O robô de pesca possui sua própria ponte de redirecionamento `pesca.php` no servidor Hostinger (diferente da `go.php` usada na moda).
Essa ponte garante:
- **Bypass de Navegador Interno:** Força a abertura do aplicativo da Shopee, protegendo o cookie de afiliado.
- **Open Graph Personalizado:** O Instagram vai mostrar a logo vermelha oficial da Shopee e o título "🎣 Oferta Especial - Pesca Titanium" na miniatura do Direct, melhorando a taxa de cliques e evitando cruzar marcas com o Titanium Boutique.

---

## ♻️ Renovação Automática de Token

A infraestrutura agora conta com o robô de manutenção autônoma `titanium_token_refresh.yml` que roda no GitHub Actions a cada 55 dias.

Este processo garante a conversão e manutenção do **Long-Lived Token (60 dias)** para as contas de Moda e Pesca simultaneamente, sem necessidade de qualquer intervenção humana (a geração manual pelo Graph Explorer foi descontinuada).

O robô:
1. Puxa os tokens antigos direto do código PHP.
2. Renova as chaves via Meta API usando os secrets `APP_ID` e `APP_SECRET` do GitHub.
3. Atualiza via FTP os arquivos `bot_instagram.php` e `bot_instagram_pesca.php` no Hostinger.
4. **Faz um commit automático no GitHub (`[skip ci]`)** atualizando os repositórios locais para sempre terem o token fresco, removendo a necessidade de atualizar Secrets na mão ou estourar erros de permissão.

**Requisitos:**
- Os GitHub Secrets `APP_ID` e `APP_SECRET` devem estar preenchidos nas configurações do repositório para que a renovação funcione automaticamente.

---

## ⚠️ Isolamento de Bots

Este bot usa:
- **Lock file separado:** `state/pesca_post.lock` (≠ `state/post.lock` do bot de moda)
- **Concurrency groups distintos:** `pesca-reels-stories` e `pesca-social`
- **Estado próprio:** `pesca/postados/` e `pesca/fila/`
- **Secrets prefixados:** Todos começam com `PESCA_`

Isso garante que **nenhuma execução do bot de pesca interfere no bot de moda**, e vice-versa.
