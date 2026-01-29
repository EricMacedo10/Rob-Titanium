# 🎯 Robô Titanium - Guia do Desconto

> Sistema 100% automatizado de comparação de preços e geração de links de afiliado para Amazon, Mercado Livre e Shopee. Atualizações automáticas 3x ao dia via GitHub Actions.

[![Status](https://img.shields.io/badge/status-automated-success)](https://guiadodesconto.com.br)
[![Automation](https://img.shields.io/badge/updates-3x%2Fday-blue)](https://github.com/EricMacedo10/Rob-Titanium/actions)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

---

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Deploy](#deploy)
- [Segurança](#segurança)
- [Roadmap](#roadmap)
- [Erros e Soluções](#erros-e-soluções)

---

## 🎯 Sobre o Projeto

O **Robô Titanium** é um sistema completo de comparação de preços que:

1. **Scraping Automatizado**: Coleta preços de produtos nas principais lojas brasileiras
2. **Geração de Links de Afiliado**: Cria links rastreáveis com tags de afiliado
3. **Site Estático**: Interface moderna e responsiva hospedada na Hostinger
4. **Integração API**: Conexão nativa com APIs oficiais (Shopee, Mercado Livre)

**Site em Produção**: [guiadodesconto.com.br](https://guiadodesconto.com.br)

---

## ✨ Funcionalidades

### **Frontend (Site)**
- ✅ 6 Categorias de Produtos (Tecnologia, Casa, Decoração, Moda, Beleza, Esportes)
- ✅ Redirecionamento inteligente com links de afiliado
- ✅ Design responsivo e moderno
- ✅ SEO otimizado
- ✅ Headers de segurança implementados
- ✅ **Campanha Sazonal**: Volta às Aulas (Banners Dinâmicos)
- ✅ **Filtro Inteligente**: Ordenação automática "Menor Preço"

### **Backend (Robô)**
- ✅ Scraping de preços (Amazon, Mercado Livre, Shopee)
- ✅ Geração automática de links de afiliado
- ✅ Autenticação SHA256 (Shopee API)
- ✅ OAuth 2.0 (Mercado Livre)
- ✅ **Atualização automática 3x/dia via GitHub Actions**
- ✅ **Upload automático via FTP para Hostinger**
- ✅ **Selenium headless otimizado para CI**

### **Integrações**
- 🟢 **Amazon Associates**: Tag `guiadodesco00-20`
- 🟢 **Mercado Livre**: User ID `188269638`
- 🟢 **Shopee**: API Nativa com fallback inteligente

---

## 🛠️ Tecnologias

### **Frontend**
- HTML5, CSS3, JavaScript (Vanilla)
- Design System customizado
- Glassmorphism e gradientes modernos

### **Backend**
- Python 3.9+
- Requests (HTTP)
- BeautifulSoup4 (Scraping)
- python-dotenv (Variáveis de ambiente)

### **Infraestrutura**
- Hostinger (Hospedagem)
- FTP (Deploy automático)
- Git (Controle de versão)

---

## 📂 Estrutura do Projeto

```
Robô Titanium/
├── .env                    # Credenciais (NÃO COMMITAR)
├── .env.example            # Template de configuração
├── .gitignore              # Proteção de arquivos sensíveis
├── requirements.txt        # Dependências Python
├── main.py                 # Entry point do robô
├── GUIA_HOSTINGER.md       # Instruções de deploy
│
├── scraper/                # Backend (Robô)
│   ├── __init__.py
│   ├── settings.py         # Configurações centralizadas
│   ├── shopee_affiliate.py # Cliente Shopee API
│   ├── mercadolivre.py     # Cliente ML API
│   └── amazon.py           # Scraper Amazon
│
└── site/                   # Frontend (Produção)
    ├── index.html          # Página principal
    ├── sobre.html          # Sobre o projeto
    ├── privacidade.html    # Política de privacidade
    ├── robots.txt          # SEO
    ├── data.json           # Dados de produtos
    ├── css/
    │   └── style.css       # Estilos globais
    ├── js/
    │   └── app.js          # Lógica do site
    └── images/             # Assets visuais
```

---

## 🚀 Instalação

### **Pré-requisitos**
- Python 3.9+
- pip
- Git

### **Passo a Passo**

1. **Clone o repositório**
```bash
git clone https://github.com/seu-usuario/robo-titanium.git
cd robo-titanium
```

2. **Crie ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure variáveis de ambiente**
```bash
cp .env.example .env
# Edite .env com suas credenciais
```

---

## ⚙️ Configuração

### **Arquivo `.env`**

```env
# Amazon Associates
AMAZON_TAG=guiadodesco00-20

# Mercado Livre
ML_USER_ID=188269638
ML_SOURCE=guiadodesconto

# Shopee Open Platform
SHOPEE_APP_ID=seu_app_id
SHOPEE_SECRET=sua_secret_key
```

### **Obter Credenciais**

#### **Amazon Associates**
1. Acesse [Amazon Associates](https://associados.amazon.com.br)
2. Crie uma conta
3. Copie sua tag de afiliado

#### **Mercado Livre**
1. Acesse [Mercado Livre Developers](https://developers.mercadolivre.com.br)
2. Crie um aplicativo
3. Configure OAuth 2.0
4. Obtenha User ID

#### **Shopee**
1. Acesse [Shopee Open Platform](https://open.shopee.com/documents)
2. Registre-se como afiliado
3. Crie um App
4. Copie App ID e Secret

---

## 🌐 Deploy

### **Hostinger (Produção)**

1. **Acesse o File Manager**
   - Entre em `public_html`

2. **Upload dos arquivos**
   - Arraste todo o conteúdo da pasta `site/`
   - Aguarde upload completar

3. **Teste**
   - Acesse seu domínio
   - Verifique funcionamento

**Guia Completo**: Consulte [GUIA_HOSTINGER.md](GUIA_HOSTINGER.md)

---

## 🔒 Segurança

### **Implementado**
- ✅ Headers de segurança (X-Content-Type-Options, Referrer-Policy)
- ✅ Credenciais em `.env` (não versionadas)
- ✅ `.gitignore` configurado
- ✅ Autenticação SHA256 (Shopee)
- ✅ OAuth 2.0 (Mercado Livre)

### **Boas Práticas**
- 🔐 Nunca commite `.env`
- 🔐 Rotacione credenciais periodicamente
- 🔐 Use HTTPS em produção
- 🔐 Monitore logs de acesso

---

## 🗺️ Roadmap

### **v1.0 (MVP)** ✅
- [x] Site estático funcional
- [x] Links de afiliado (Amazon, ML, Shopee)
- [x] Deploy na Hostinger
- [x] SEO básico

### **v2.0 (Planejado)**
- [ ] Busca em tempo real
- [ ] Sistema de votação de ofertas
- [ ] Curadorias personalizadas
- [ ] API REST para mobile
- [ ] Dashboard de analytics
- [ ] Integração com mais lojas

### **v3.0 (Futuro)**
- [ ] App mobile (React Native)
- [ ] Notificações push
- [ ] Comparação de preços históricos
- [ ] Machine Learning para recomendações

---

## 📊 Métricas

**Lançamento**: 21/01/2026  
**Tráfego (Primeiro dia)**: 296 requests em 6 minutos  
**Taxa de erro**: <2% (excelente)  
**Países alcançados**: 5+ (EUA, Suíça, Irlanda, Alemanha, Dinamarca)

---

## 🛠️ Erros e Soluções

Para detalhes técnicos sobre desafios enfrentados e como foram resolvidos, consulte o [Guia de Erros e Soluções](docs/ERRORS_AND_SOLUTIONS.md).

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 👤 Autor

**Eric Macedo**  
- Instagram: [@oferta.certa10](https://instagram.com/oferta.certa10)
- Email: contato@guiadodesconto.com.br

---

## 🙏 Agradecimentos

- Amazon Associates
- Mercado Livre Developers
- Shopee Open Platform
- Hostinger

---

**⭐ Se este projeto te ajudou, considere dar uma estrela!**
