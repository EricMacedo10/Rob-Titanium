# 🚀 Expansão de Banners Interativos (Padrão Titanium)

Este documento detalha o "Blueprinting" do sistema de banners interativos que implementamos com sucesso e como replicá-lo para novas categorias.

## 🎯 O Conceito
Transformar banners estáticos em "Hubs de Compra" minúsculos. O usuário escolhe a loja de preferência antes mesmo de ser redirecionado, aumentando o CTR (taxa de cliques) e a confiança.

## ✅ Status Atual - 13 Categorias Implementadas

| Categoria | Amazon | Mercado Livre | Shopee | Status |
|-----------|--------|---------------|--------|--------|
| 💻 Tecnologia | computador pc gamer hardware | notebook computador pc | notebook barato chromebook | ✅ ATIVO |
| 🏠 Casa e Jardim | organizador cozinha utilidades | moveis decoracao casa | decoracao casa barato | ✅ ATIVO |
| 🚗 Automotivo | acessorios carro automotivo | pecas carro acessorios | acessorios automotivos barato | ✅ ATIVO |
| 👗 Moda | roupas femininas masculinas | roupas moda vestuario | roupas baratas moda | ✅ ATIVO |
| 💄 Beleza | maquiagem skincare perfumes | cosmeticos beleza cuidados pele | maquiagem barata skincare coreano | ✅ ATIVO |
| 🏃 Esportes | equipamentos fitness musculacao | bicicleta patins skate | roupas esportivas fitness barato | ✅ ATIVO |
| 🎮 Games | playstation xbox nintendo jogos | video game console controle | jogos baratos acessorios gamer | ✅ ATIVO |
| 🐾 Pet Shop | racao cachorro gato petiscos | acessorios pet coleira caminha | brinquedos pet roupas cachorro | ✅ ATIVO |
| 🔌 Eletrodomésticos | liquidificador air fryer panela | geladeira fogao microondas | eletrodomesticos cozinha barato | ✅ ATIVO |
| 🔧 Ferramentas | furadeira parafusadeira kit | ferramentas construcao reforma | ferramentas manuais barato | ✅ ATIVO |
| 📚 Papelaria | caderno caneta mochila escolar | material escolar papelaria | cadernos baratos material escolar | ✅ ATIVO |
| 🎨 Decoração | quadros decorativos almofadas | decoracao casa sala quarto | decoracao barata enfeites casa | ✅ ATIVO |
| 🎭 Carnaval | fantasias carnaval glitter | caixa de som jbl termica cooler | fantasias baratas decoracao festa | ✅ ATIVO (SAZONAL) |

**Versão atual:** v=1103  
**Última atualização:** 05/02/2026

## 🛠️ Como Adicionar Nova Categoria

### 1. Estrutura HTML (index.html)
```html
<!-- Categoria: [Nome] (Interativo) -->
<div class="hub-card [classe] interactive-card" id="[id]-hub-card" data-category="[categoria]">
    <div class="brand-tabs">
        <button class="tab-btn active" data-store="amazon" title="Ver na Amazon">
            <i class="fab fa-amazon"></i>
        </button>
        <button class="tab-btn" data-store="mercadolivre" title="Ver no Mercado Livre">
            <i class="fas fa-handshake"></i>
        </button>
        <button class="tab-btn" data-store="shopee" title="Ver na Shopee">
            <i class="fa-solid fa-bag-shopping"></i>
        </button>
    </div>
    <img src="images/banner_[nome]_amazon.png?v=[versao]" alt="[Nome]" id="[id]-banner-img">
    <h3>[Nome da Categoria]</h3>
</div>
```

### 2. Configuração JavaScript (app.js)
```javascript
setupTitaniumInteractiveBanner('[id]-hub-card', {
    defaultStore: 'amazon',
    banners: {
        amazon: 'images/banner_[nome]_amazon.png?v=[versao]',
        mercadolivre: 'images/banner_[nome]_mercadolivre.png?v=[versao]',
        shopee: 'images/banner_[nome]_shopee.png?v=[versao]'
    },
    searchTerms: {
        amazon: 'termos específicos amazon',
        mercadolivre: 'termos específicos ml',
        shopee: 'termos específicos shopee'
    }
});
```

### 3. Incrementar Versão (index.html)
```html
<link rel="stylesheet" href="css/style.css?v=[nova_versao]">
<script src="js/app.js?v=[nova_versao]"></script>
```

### 4. Deploy (CRÍTICO!)
**Execute 2-3 deploys** para garantir sincronização FTP:
```bash
python deploy_site.py  # 1º deploy
python deploy_site.py  # 2º deploy (obrigatório)
python deploy_site.py  # 3º deploy (se necessário)
```

## 💎 Regras de Ouro

1. **Termos de Busca Anti-Erro:** Use produtos específicos, nunca categorias genéricas
   - ❌ Ruim: "tecnologia", "casa"
   - ✅ Bom: "notebook computador pc", "organizador cozinha"

2. **Cache-Busting:** Sempre incremente a versão `?v=` ao mudar código

3. **Deploy Múltiplo:** FTP requer 2-3 deploys para sincronizar HTML + JS corretamente

4. **Verificação de Tags:** Confirme que as tags de afiliado estão corretas:
   - Amazon: `guiadodesco00-20`
   - Mercado Livre: `matt_tool=188269638`
   - Shopee: `utm_source=ericmacedo`

## 🔐 Segurança - Tags de Afiliado

Todas as categorias utilizam as tags configuradas em `TITANIUM_CONFIG`:
- ✅ Amazon Associates: `guiadodesco00-20`
- ✅ Mercado Livre User ID: `188269638`
- ✅ Shopee: `ericmacedo`

**Verificação completa:** Ver `affiliate_tags_verification.md`

## 📊 Métricas de Sucesso

- **13 categorias** com banners interativos (incluindo 1 sazonal)
- **39 banners** únicos (3 por categoria)
- **100% das URLs** com tags de afiliado corretas
- **3 lojas** integradas (Amazon, ML, Shopee)

---
*Documento atualizado pelo Robô Titanium em 05/02/2026*
