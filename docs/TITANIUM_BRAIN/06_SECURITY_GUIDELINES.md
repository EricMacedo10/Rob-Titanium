# 🛡️ Diretrizes de Segurança e Higiene de Documentação

Este documento estabelece as regras de ouro para o desenvolvimento e manutenção do projeto Robô Titanium.
Como este é um projeto de código aberto, a segurança contra vazamento de dados e credenciais é **A PRIORIDADE NÚMERO UM**.

## 1. Mapeamento de Variáveis em vez de Hardcoding
**Nunca escreva senhas, tokens, chaves de API ou segredos nos arquivos de documentação, nem mesmo como "exemplos reais".**

### ❌ Errado (Exemplo Vulnerável)
> "Coloque a sua senha do FTP: Exemplo: `MinhaSenhaSuperForte123`"
> "A chave do ImgBB é `89a87s98d798a7s9d`"

O cérebro humano tem a tendência de preencher lacunas ou testar coisas copiando e colando, e as vezes commita sem querer o dado sensível.

### ✅ Correto (Higiene de Documentação)
> "Acesse o seu painel e pegue a sua senha do FTP. Salve-a no seu arquivo `.env` sob a variável `$FTP_PASS`. NUNCA escreva essa senha aqui."
> "Referencie a variável de ambiente: `$IMGBB_API_KEY`."

## 2. A Camada do `.env` e Github Secrets
*   Nenhum script Python ou PHP deve ter credenciais "chumbadas" (hardcoded).
*   Sempre utilize `os.getenv("MINHA_VARIAVEL")`.
*   O arquivo `.env` deve sempre estar listado no `.gitignore`.
*   As automações (Actions) não leem do `.env`, elas leem dos **Github Secrets**. Mantenha os secrets estritamente atualizados lá na aba Settings do repositório.

## 3. Hook Pre-commit (Bloqueio Automático de Vazamento)
O repositório utiliza mecanismos para prevenir que desenvolvedores cometam erros e deem push em senhas acidentalmente.
Nós utilizamos o **detect-secrets** como pre-commit hook. Ao detectar uma senha, o commit é cancelado.

*Versão: 1.0 (Segurança do Titanium Brain)*
