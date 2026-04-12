# 🤖 Robô Titanium: Documentação Mestre (v2026 - Elite)

Bem-vindo à documentação oficial do **Robô Titanium**, a plataforma autônoma de curadoria de moda e beleza premium exclusiva para a **Shopee**.

---

## 🏛️ 1. Arquitetura do Sistema (Shopee-Exclusive)

O sistema opera em um modelo **Híbrido de Alta Performance**:
- **Backend (Python 3.10)**: Responsável pela mineração de dados via API Oficial Shopee v2 e geração de conteúdo via IA (DeepSeek).
- **Frontend (Elite Design)**: Interface estática (HTML/CSS/JS) otimizada para SEO, velocidade e conversão, hospedada na Hostinger.
- **Data Flow**: Os dados são injetados na interface via arquivos JSON (`data.json`, `ai_reviews.json`) sincronizados via FTP.

### Componentes Core:
1.  **Minerador de Elite (`core/orchestrator.py`)**: Atualiza a vitrine principal 3x ao dia.
2.  **Radar de Tendências (`core/review_engine.py`)**: IA que seleciona 3 itens destaque a cada 4 dias.
3.  **Editorial Hub (`core/auto_blog_generator.py`)**: Gera um artigo semanal de autoridade sobre moda.

---

## 🚀 2. Automação CI/CD (GitHub Actions)

O sistema é 100% autônomo. As rotinas são gerenciadas pelo GitHub:

| Nome da Action | Frequência | Objetivo |
| :--- | :--- | :--- |
| `🛰️ Shopee Gold Exclusive` | 3x ao dia | Atualiza preços e estoque da vitrine principal. |
| `🛰️ Radar de Tendências IA` | 4 em 4 dias | Troca os destaques do Radar e gera novos reviews. |
| `✍️ Editorial Semanal` | Todo Domingo | Publica um novo artigo completo no blog. |

---

## 🔐 3. Gestão de Segredos e Segurança

Para manter a segurança, **nenhuma senha é gravada no código**. O sistema utiliza:

### GitHub Secrets (Mandatórios):
- `SHOPEE_APP_ID` / `SHOPEE_SECRET`: Acesso à API Oficial de Afiliados.
- `DEEPSEEK_API_KEY`: Token do motor de IA para geração de conteúdo.
- `FTP_HOST` / `FTP_USER` / `FTP_PASS`: Acesso ao servidor de produção (Hostinger).

### Blindagem de Produção:
O sistema possui uma trava de segurança no script de sincronização (`sync_production_v12.py`):
- **O robô nunca sobrescreve o design estrutural** automaticamente.
- Atualizações de layout (mudar botões, cores, etc) devem ser enviadas manualmente via `git push origin main`.

---

## 📂 4. Estrutura de Diretórios

- `/core`: Cérebro e lógica de mineração/IA.
- `/site`: Todos os arquivos que o usuário vê (HTML, CSS, JS).
- `/state`: Arquivos que guardam o estado atual dos links e ofertas.
- `.github/workflows`: Os "maestros" que agendam as tarefas.
- `archive_legacy/`: Scripts antigos e de teste isolados (ML, Amazon, etc).

---

## 🛠️ 5. Como Realizar Manutenções

1.  **Mudar o Design**: Edite o arquivo em `site/index.html` localmente e faça um `git push`. A automação usará esse novo design como base.
2.  **Testar Links**: Utilize o script `core/tester.py` (se disponível) ou valide via `state/links.json`.
3.  **Forçar Sincronia**: Rode `python sync_production_v12.py` para empurrar mudanças manuais imediatas.

---
> [!IMPORTANT]
> A Boutique Titanium agora é um sistema **Stateless**. Todo o seu "conhecimento" sobre produtos vem do `data.json`. Se o site parecer desatualizado, verifique o status da Action `Shopee Gold Exclusive` no GitHub.

---
*Documentação atualizada em 2026 - Robô Titanium: Inteligência a serviço da sua comissão.*
