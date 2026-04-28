# 🚀 Guia Completo: Deploy na Hostinger

## 📋 Visão Geral

Este guia ensina como fazer o deploy do site **Guia do Desconto** na Hostinger, incluindo:
- Upload dos arquivos do site
- Configuração do FTP para atualizações automáticas
- Verificação do funcionamento

---

## 🎯 Pré-requisitos

Antes de começar, você precisa ter:

✅ **Conta na Hostinger** com domínio configurado (guiadodesconto.com.br)  
✅ **Acesso ao painel hPanel** da Hostinger  
✅ **Arquivos do site** prontos na pasta `site/`  
✅ **Credenciais FTP** (vamos criar neste guia)

---

## 📁 Parte 1: Preparar Arquivos para Upload

### Arquivos que serão enviados

Todos os arquivos da pasta `site/` devem ser enviados:

```
site/
├── index.html          # Página principal
├── sobre.html          # Página sobre
├── privacidade.html    # Política de privacidade
├── data.json           # Dados dos produtos (atualizado pelo robô)
├── robots.txt          # SEO
├── css/
│   └── style.css       # Estilos
├── js/
│   └── app.js          # JavaScript
└── images/             # Imagens do site
```

### Verificar antes do upload

1. **Abra** `site/index.html` localmente no navegador
2. **Confirme** que tudo está funcionando
3. **Verifique** se `data.json` tem produtos válidos

---

## 🌐 Parte 2: Upload via File Manager (Método Visual)

### Passo 1: Acessar o hPanel

1. Acesse: https://hpanel.hostinger.com/
2. Faça login com suas credenciais
3. Selecione o domínio **guiadodesconto.com.br**

### Passo 2: Abrir File Manager

1. No painel lateral, clique em **Arquivos**
2. Clique em **Gerenciador de Arquivos** (File Manager)
3. Aguarde o File Manager abrir em nova aba

### Passo 3: Navegar para public_html

1. No File Manager, você verá uma lista de pastas
2. **Clique duas vezes** na pasta `public_html`
3. Esta é a pasta raiz do seu site

> [!IMPORTANT]
> **TUDO que estiver dentro de `public_html` será acessível publicamente via seu domínio!**

### Passo 4: Limpar conteúdo antigo (se houver)

Se já existem arquivos antigos:

1. **Selecione todos** os arquivos/pastas antigas
2. Clique com botão direito → **Delete**
3. Confirme a exclusão

> [!CAUTION]
> Cuidado para não deletar arquivos importantes como `.htaccess` se você tiver configurações especiais!

### Passo 5: Upload dos arquivos

**Método 1: Arrastar e Soltar (Recomendado)**

1. Abra o Windows Explorer
2. Navegue até `C:\Users\ericm\OneDrive\Área de Trabalho\PESSOAL\Robô Titanium\site\`
3. **Selecione TODOS os arquivos e pastas** dentro de `site/`
4. **Arraste** para a janela do File Manager (dentro de `public_html`)
5. Aguarde o upload completar

**Método 2: Botão Upload**

1. Clique no botão **Upload** no topo do File Manager
2. Clique em **Select Files**
3. Selecione todos os arquivos da pasta `site/`
4. Clique em **Open**
5. Aguarde upload completar

### Passo 6: Verificar estrutura

Após o upload, `public_html` deve conter:

```
public_html/
├── index.html
├── sobre.html
├── privacidade.html
├── data.json
├── robots.txt
├── css/
├── js/
└── images/
```

> [!TIP]
> Se você vir uma pasta `site/` dentro de `public_html`, você arrastou a pasta errada! Delete e arraste apenas o **conteúdo** de `site/`, não a pasta em si.

---

## ✅ Parte 3: Testar o Site

### Teste 1: Acessar o domínio

1. Abra um navegador **em modo anônimo** (Ctrl + Shift + N)
2. Acesse: https://guiadodesconto.com.br
3. Verifique se o site carrega corretamente

### Teste 2: Verificar funcionalidades

- ✅ Design aparece corretamente
- ✅ Produtos são exibidos
- ✅ Links de afiliado funcionam
- ✅ Navegação entre páginas funciona
- ✅ Imagens carregam

### Teste 3: Verificar data.json

1. Acesse: https://guiadodesconto.com.br/data.json
2. Você deve ver o JSON com os produtos
3. Confirme que os dados estão corretos

---

## 🔐 Parte 4: Configurar FTP para Atualizações Automáticas

### Por que precisamos do FTP?

O GitHub Actions precisa fazer upload do `data.json` atualizado automaticamente. Para isso, precisamos de credenciais FTP.

### Passo 1: Criar conta FTP

1. No **hPanel**, vá em **Arquivos** → **Contas FTP**
2. Clique em **Criar conta FTP**
3. Preencha:
   - **Nome de usuário**: `robo-titanium` (ou outro nome)
   - **Senha**: Gere uma senha forte (ex: `<SUA_SENHA_AQUI>`)
   - **Diretório**: `/public_html` (ou deixe padrão)
4. Clique em **Criar**

### Passo 2: Anotar credenciais FTP

Após criar, você terá:

```
FTP_HOST: ftp.guiadodesconto.com.br
FTP_USER: robo-titanium@guiadodesconto.com.br
FTP_PASS: <SUA_SENHA_FTP>
```

> [!IMPORTANT]
> **Guarde essas credenciais com segurança!** Você precisará delas no próximo passo.

### Passo 3: Testar conexão FTP (Opcional)

Você pode testar a conexão usando FileZilla:

1. Baixe FileZilla: https://filezilla-project.org/
2. Abra FileZilla
3. Preencha:
   - **Host**: `ftp.guiadodesconto.com.br`
   - **Usuário**: `robo-titanium@guiadodesconto.com.br`
   - **Senha**: `<SUA_SENHA_FTP>`
   - **Porta**: `21`
4. Clique em **Quickconnect**
5. Se conectar, está funcionando! ✅

---

## 🤖 Parte 5: Adicionar Credenciais FTP no GitHub

Agora que temos as credenciais FTP, vamos adicioná-las ao GitHub Secrets.

### Passo 1: Acessar GitHub Secrets

1. Vá para: https://github.com/EricMacedo10/Rob-Titanium/settings/secrets/actions
2. Você já deve ter 3 secrets configurados

### Passo 2: Adicionar FTP_HOST

1. Clique em **New repository secret**
2. **Name**: `FTP_HOST`
3. **Secret**: `ftp.guiadodesconto.com.br`
4. Clique em **Add secret**

### Passo 3: Adicionar FTP_USER

1. Clique em **New repository secret**
2. **Name**: `FTP_USER`
3. **Secret**: `robo-titanium@guiadodesconto.com.br` (use o usuário que você criou)
4. Clique em **Add secret**

### Passo 4: Adicionar FTP_PASS

1. Clique em **New repository secret**
2. **Name**: `FTP_PASS`
3. **Secret**: `<SUA_SENHA_FTP>` (use a senha que você criou)
4. Clique em **Add secret**

### Passo 5: Atualizar .env local

Edite o arquivo `.env` local e descomente as linhas FTP:

```env
# ========================================
# FTP HOSTINGER (Para deploy)
# ========================================
FTP_HOST=ftp.guiadodesconto.com.br
FTP_USER=robo-titanium@guiadodesconto.com.br
FTP_PASS=<SUA_SENHA_FTP>
```

> [!WARNING]
> **NUNCA** faça commit do arquivo `.env` no Git! Ele já está no `.gitignore`.

---

## 🧪 Parte 6: Testar Atualização Automática

### Teste 1: Executar robô localmente

1. Abra o terminal na pasta do projeto
2. Execute:
   ```bash
   python main.py
   ```
3. Aguarde o robô buscar ofertas
4. Verifique se o upload FTP foi bem-sucedido:
   ```
   🌐 Iniciando upload para Hostinger...
   ✅ Upload concluído com sucesso! O site foi atualizado.
   ```

### Teste 2: Verificar no site

1. Acesse: https://guiadodesconto.com.br/data.json
2. Pressione **Ctrl + F5** para forçar atualização
3. Confirme que os dados foram atualizados

### Teste 3: Executar via GitHub Actions

1. Vá para: https://github.com/EricMacedo10/Rob-Titanium/actions
2. Clique no workflow **"🤖 Atualizar Ofertas Automaticamente"**
3. Clique em **Run workflow** → **Run workflow**
4. Aguarde execução (~3-5 minutos)
5. Verifique logs para confirmar sucesso

---

## 📊 Parte 7: Monitoramento

### Ver logs de atualização

**GitHub Actions:**
- Acesse: https://github.com/EricMacedo10/Rob-Titanium/actions
- Veja histórico completo de execuções
- Logs detalhados de cada run

**Hostinger:**
- hPanel → **Estatísticas** → **Logs de Acesso**
- Veja quando o `data.json` foi atualizad o

### Horários de atualização automática

O robô roda automaticamente em:
- **07:00 BRT** - Manhã
- **13:00 BRT** - Tarde
- **20:00 BRT** - Noite

---

## 🚨 Troubleshooting

### Site não carrega

- ✅ Verifique se os arquivos estão em `public_html` (não em subpasta)
- ✅ Confirme que `index.html` existe
- ✅ Aguarde 5-10 minutos para propagação DNS

### Upload FTP falha

- ✅ Verifique credenciais FTP nos GitHub Secrets
- ✅ Teste conexão com FileZilla
- ✅ Confirme que o caminho é `/public_html/data.json`

### Produtos não aparecem

- ✅ Verifique se `data.json` existe e tem conteúdo
- ✅ Abra console do navegador (F12) e veja erros
- ✅ Confirme que `app.js` está carregando

### Workflow falha no GitHub

- ✅ Veja logs detalhados na aba Actions
- ✅ Confirme que todos os 6 secrets estão configurados
- ✅ Verifique se o repositório está público ou tem minutos Actions disponíveis

---

## 🎉 Conclusão

Parabéns! Seu site está no ar e sendo atualizado automaticamente! 🚀

**Resumo do que foi feito:**
1. ✅ Upload do site para Hostinger via File Manager
2. ✅ Criação de conta FTP
3. ✅ Configuração de GitHub Secrets (FTP)
4. ✅ Testes de atualização automática
5. ✅ Monitoramento configurado

**Próximos passos:**
- Monitore as execuções automáticas
- Adicione mais produtos em `settings.py`
- Configure credenciais do Mercado Livre quando disponível
- Promova o site nas redes sociais!

---

## 📞 Suporte

Se encontrar problemas:
1. Consulte a seção Troubleshooting acima
2. Veja os logs no GitHub Actions
3. Revise a documentação: `docs/SCHEDULING.md`
4. Entre em contato: contato@guiadodesconto.com.br
