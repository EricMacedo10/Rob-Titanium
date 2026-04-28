# 🌐 Roadmap: Integração com a API da Hostinger

**Documentação Oficial da Hostinger API**: [https://developers.hostinger.com/#description/overview](https://developers.hostinger.com/#description/overview)

Este documento detalha o planejamento arquitetural para substituir processos manuais e protocolos antigos (como FTP) por requisições modernas (REST API) diretamente nos servidores da Hostinger.

## 🎯 Por Que Integrar a API? (Objetivos)

O uso da API nativa da Hostinger permitirá que o Robô Titanium alcance o nível máximo de confiabilidade em CI/CD. Os principais alvos desta integração são:

### 1. Extinção do FTP (Substituição pelo File Manager API)
O FTP é vulnerável a timeouts durante execuções no GitHub Actions. Usando a API REST (via HTTPS), poderemos enviar o arquivo `data.json` e mídias estáticas de forma atômica e validada, sem os problemas de "socket hang up".
*   **Vantagem**: Redução de 90% nas falhas silenciosas de upload. Maior velocidade na publicação de novas vitrines.

### 2. Automação de Cache Purge (LiteSpeed)
Atualmente, as vitrines atualizadas podem demorar a aparecer para usuários finais devido a políticas agressivas de cache do servidor e do navegador.
*   **Ação**: Integrar um endpoint na API para enviar um comando `purge-all` imediatamente após o Titanium terminar de fazer o upload do `data.json`.
*   **Vantagem**: O cliente sempre verá a oferta e preço mais recentes na exata fração de segundo em que o robô terminar o ciclo. Sem necessidade de mandar o usuário dar "F5".

### 3. Bypass Programático do Firewall (ModSecurity/WAF)
Como vimos no "Erro 9004", a Hostinger bloqueia dinamicamente bots como o *crawler* do Facebook.
*   **Ação**: Caso precisemos utilizar o servidor como fonte primária para a Meta API, podemos usar a API da Hostinger para inserir o IP do Facebook em uma "Whitelist" segundos antes do post, e remover logo em seguida.

---

## 🛠️ Plano de Ação (Próximos Passos)

Para iniciarmos o desenvolvimento amanhã, este será o nosso fluxo de trabalho:

### Passo 1: Gerar a Chave da API (API Key)
1.  Acessar o **hPanel da Hostinger**.
2.  Navegar até a seção de **Avançado > API REST** (ou Gerenciamento de Tokens).
3.  Gerar um novo token de acesso com permissões restritas (apenas File Manager e Cache, se aplicável).

### Passo 2: Higiene de Segurança
1.  **NUNCA** colar a chave gerada neste documento.
2.  Armazenar a chave gerada como `$HOSTINGER_API_TOKEN` no arquivo `.env` local.
3.  Salvar a mesma chave no **GitHub Secrets**, garantindo a segurança do repositório aberto.

### Passo 3: Prototipagem do Novo Módulo (`hostinger_client.py`)
1.  Criar a nova classe `HostingerAPIClient`.
2.  Fazer os primeiros testes de *Ping* e Autenticação.
3.  Substituir as funções antigas do `uploader.py` pelas novas requisições API.

---
*Documento preparado para a sessão de arquitetura. O Titanium Brain está pronto para assumir o controle total da infraestrutura.*
