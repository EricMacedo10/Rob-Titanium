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

## 4. GitHub Advanced Security (Nuvem)
Além do bloqueio local, o repositório conta com três camadas de proteção ativa nos servidores do GitHub (configurados em `Settings > Code security and analysis`):
1. **Push Protection**: Rejeita ativamente qualquer comando `git push` que contenha tokens de parceiros identificáveis (AWS, Meta, Github, etc).
2. **Secret Scanning**: Varredura assíncrona constante em busca de vazamentos de chaves de API não cobertas pelo Push Protection.
3. **Dependabot Alerts & Updates**: Monitoramento contínuo do arquivo `requirements.txt`. O GitHub notifica proativamente sobre vulnerabilidades descobertas em dependências Python (ex: `requests`, `pillow`) e gera *Pull Requests* automáticos de segurança.

## 5. Prevenção de Fraude de Afiliado (Autocompra)
*   **Regra de Ouro**: A Shopee possui um mecanismo antifraude que invalida o rastreamento de comissões se o link de afiliado gerado for utilizado para realizar uma compra **pela mesma conta** que gerou o link (ou pelo mesmo IP / aparelho associado ao afiliado).
*   **Consequência**: A compra não entra no relatório de comissões, gerando perda financeira.
*   **Testes**: Se precisar testar o fluxo de vendas do site, sempre gere a conversão usando uma conta limpa de um terceiro que **não resida no mesmo domicílio (IP)**, utilizando a rede 4G. 

## 6. Padronização de Execução Segura (UTF-8)
*   **Ameaça de Crash Oculto**: A execução de scripts Python em ambientes Windows frequentemente causa falhas `UnicodeEncodeError` ao tentar logar emojis (como `❌`, `✅`, `⚠️`) quando o console padrão adota `cp1252` (charmap).
*   **Regra de Codificação**: **TODOS** os scripts de execução agendada, monitoramento e APIs locais que utilizem `print()` com símbolos enriquecidos devem forçar a reconfiguração defensiva do `sys.stdout` no cabeçalho do arquivo:
```python
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
```

*Versão: 1.3 (Segurança do Titanium Brain - v5.4.4)*
