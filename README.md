# 🦾 Robô Titanium: Boutique Shopee Elite (v3.2.0)

O **Robô Titanium** é um ecossistema de automação de alta performance projetado para gerenciar uma boutique de afiliados Shopee 100% autônoma. Ele combina mineração de dados, curadoria por IA e automação de redes sociais em um único ecossistema resiliente.

---

## 🚀 Funcionalidades Principais
- **Curadoria IA Titanium (DeepSeek-V3.2)**: 
  - Geração de artigos editoriais luxuosos.
  - Reviews de tendências complexas com foco em Agentic Reasoning.
  - Decisões de arbitragem de produtos (Arbitro Elite).
- **Social Automation**: Publicação automática de carrosséis (fotos e vídeos Ken Burns) e bot de resposta de comentários ("QUERO").
- **Design Elite**: Interface moderníssima com Glassmorphism, Neon Pulse e Radar de Tendências IA.
- **Deploy Blindado**: CI/CD via GitHub Actions com sincronização atômica via FTP.

---

## 📂 Estrutura do Projeto
- `core/`: O "cérebro" do sistema (Arbitragem, Curação de IA, Orquestração).
- `site/`: Arquivos HTML/JS/CSS do frontend modernizado.
- `social/`: Scripts de postagem no Instagram e automação de engajamento.
- `scraper/`: Motores de extração de dados da Shopee.
- `docs/TITANIUM_BRAIN/`: Documentação técnica profunda de cada módulo.

---

## 🛠️ Como Iniciar
1. Instale as dependências: `pip install -r requirements.txt`
2. Configure o arquivo `.env` com suas chaves (Shopee, DeepSeek, FTP).
3. Execute o minerador: `python core/orchestrator.py`
4. Deploy manual: `python sync_production_v12.py`

---

## 🛡️ Segurança e Estabilidade
- **Stateless Frontend**: Não depende de DB MySql no servidor, apenas JSON.
- **Fail-Safe**: Se uma API de IA falhar, o sistema volta para lógica de menor preço local.
- **Atomic FTP**: Garante que o site só mude se os dados novos forem válidos.

---
**Desenvolvido pelo Time Advanced Agentic Coding - Google DeepMind**
*Mantendo a Trilha da Prosperidade e o Estilo Elite Titanium.*
