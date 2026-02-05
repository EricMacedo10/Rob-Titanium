# 🛡️ Guia de Ambientes: Robô Titanium

Este guia explica como usar o novo **Ambiente de Staging (Teste)** para trabalhar com segurança em novas funcionalidades.

## 🧪 Ambiente de Staging (Homologação)
Use este ambiente para testar mudanças visuais, novos banners ou ajustes no robô.

- **URL**: [https://teste.guiadodesconto.com.br](https://teste.guiadodesconto.com.br)
- **Como Ativar**: No arquivo `.env`, certifique-se de que a variável está assim:
  ```env
  ENV_MODE=STAGING
  ```
- **O que acontece**:
    - O `deploy_site.py` enviará arquivos para a subpasta `/teste/`.
    - O `run_batch_update.py` atualizará o site de teste.
    - O **Instagram é bloqueado**: Nenhuma postagem real será feita.

---

## 🚀 Ambiente de Produção (Site Oficial)
Use este ambiente apenas quando as mudanças estiverem validadas no Staging.

- **URL**: [https://guiadodesconto.com.br](https://guiadodesconto.com.br)
- **Como Ativar**: No arquivo `.env`, mude a variável para:
  ```env
  ENV_MODE=PRODUCTION
  ```
- **O que acontece**:
    - Todos os deploys vão para a raiz do site oficial.
    - O robô volta a fazer postagens reais no Instagram (se os tokens estiverem ativos).

---

## 🛠️ Comandos Úteis para Amanhã
- `python deploy_site.py`: Sincroniza o visual do site (HTML/CSS/JS).
- `python run_batch_update.py`: Atualiza as ofertas (Produtos e Notificações).

> [!IMPORTANT]
> **Dica de Senior**: Sempre faça o deploy e a atualização no modo `STAGING` primeiro, abra o site de teste, verifique se tudo está bonito e, só então, mude para `PRODUCTION`.
