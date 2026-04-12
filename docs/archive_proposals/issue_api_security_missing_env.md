# ISSUE: Configuração de Segurança da API Pendente (.env)

## Status: Pendente
**Data:** 30/03/2026
**Prioridade:** Alta (Segurança)

---

## Descrição do Problema
A lógica de segurança do servidor API (`core/api_server.py`) foi atualizada para exigir um token administrativo (**ADMIN_API_KEY**) para funções sensíveis, como a limpeza de cache. 

No entanto, a tentativa de atualizar o arquivo `.env` automaticamente via assistente falhou devido a travamentos no sistema (timeouts/cancelamentos).

## O que foi feito
- [x] Implementação do Middleware de segurança em `core/api_server.py`.
- [x] Verificação da estrutura do endpoint `/api/limpar-cache`.

## O que falta fazer (Manual)
O arquivo `.env` precisa ser atualizado manualmente para que o servidor consiga validar os acessos administrativos.

### Instruções:
1. Abra o arquivo `.env` na raiz do projeto.
2. Adicione a seguinte linha ao final do arquivo:
   ```env
   # API Security
   ADMIN_API_KEY=titanium_admin_sk_9482
   ```
3. Reinicie o processo Python do servidor (`python core/api_server.py`) para aplicar a nova configuração.

## Observação Técnica
O assistente tentou rodar `replace_file_content` no `.env`, mas a interface travou sem fornecer feedback visual (thinking indicator). Recomenda-se a edição manual para evitar novos congelamentos até que a conexão estabilize.
