# 🔐 Guia Rápido: Configurar GitHub Secrets

## 📋 Passo a Passo

### 1. Acesse as Configurações do Repositório

1. Vá para o seu repositório no GitHub
2. Clique em **Settings** (Configurações)
3. No menu lateral esquerdo, clique em **Secrets and variables** → **Actions**

### 2. Adicione Cada Secret

Para cada credencial abaixo, clique em **New repository secret** e preencha:

---

## 🔑 Secrets Necessários

### Amazon
```
Nome: AMAZON_AFFILIATE_TAG
Valor: guiadodesco00-20
```

### Mercado Livre
```
Nome: MELI_CLIENT_ID
Valor: [Copie do seu arquivo .env]
```

```
Nome: MELI_CLIENT_SECRET
Valor: [Copie do seu arquivo .env]
```

### Shopee
```
Nome: SHOPEE_APP_ID
Valor: [Copie do seu arquivo .env]
```

```
Nome: SHOPEE_SECRET
Valor: [Copie do seu arquivo .env]
```

### Hostinger FTP
```
Nome: FTP_HOST
Valor: [Copie do seu arquivo .env]
```

```
Nome: FTP_USER
Valor: [Copie do seu arquivo .env]
```

```
Nome: FTP_PASS
Valor: [Copie do seu arquivo .env]
```

---

## ✅ Verificação

Após adicionar todos os secrets, você deve ver **8 secrets** na lista:

- ✅ AMAZON_AFFILIATE_TAG
- ✅ MELI_CLIENT_ID
- ✅ MELI_CLIENT_SECRET
- ✅ SHOPEE_APP_ID
- ✅ SHOPEE_SECRET
- ✅ FTP_HOST
- ✅ FTP_USER
- ✅ FTP_PASS

---

## 🚀 Próximos Passos

1. **Commit e Push** dos arquivos criados:
   ```bash
   git add .
   git commit -m "feat: adicionar agendamento automático 3x/dia via GitHub Actions"
   git push origin main
   ```

2. **Teste Manual** do workflow:
   - Vá em **Actions** no GitHub
   - Selecione "🤖 Atualizar Ofertas Automaticamente"
   - Clique em **Run workflow**
   - Aguarde execução e verifique logs

3. **Monitore** as execuções automáticas nos horários programados (07:00, 13:00, 20:00 BRT)

---

> [!TIP]
> Os secrets são criptografados e nunca são expostos nos logs. É totalmente seguro!
