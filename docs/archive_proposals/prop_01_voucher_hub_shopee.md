# Proposta de Implementação: Hub de Cupons Automático Shopee
**Status:** Aguardando Aprovação (Opção 1 Selecionada)
**Data:** 12/04/2026

## 1. Conceito
Implementar um ponto de contato estratégico no topo da **Boutique Titanium** que redireciona o usuário para a Central de Cupons Oficial da Shopee através do seu link de afiliado.

## 2. Benefícios Técnicos
- **Manutenção Zero:** Como o link aponta para a página oficial de cupons da Shopee, os descontos são atualizados pela própria Shopee diariamente.
- **Cookies de Elite:** Ao clicar no link de cupons, o usuário recebe o seu cookie de afiliado. Qualquer compra que ele fizer nas próximas 24h a 7 dias (dependendo da regra da Shopee) gerará comissão para você.
- **Autoridade:** Passa a imagem de que a Boutique Titanium tem acesso direto aos benefícios da plataforma.

## 3. Implementação Visual (Sugestão)
O banner será inserido logo abaixo do "API Sync Banner", com as seguintes características:
- **Estilo:** Glassmorphism (Fundo translúcido com blur).
- **Cores:** Laranja Shopee (#FF4500) com Neon Pulse.
- **Texto:** `🎟️ CENTRAL DE CUPONS: Resgate seus descontos de hoje aqui!`
- **Ação:** Botão flutuante ou banner de largura total.

## 4. Lógica de Link (Automática)
O script `core/link_builder.py` ou `scraper/engines/shopee_affiliate.py` será configurado para processar a URL base de cupons:
`URL_BASE = "https://shopee.com.br/m/cupons-diarios"`

Toda vez que o site for carregado, o sistema garantirá que o link do banner esteja "encurtado" e rastreado com seu `AFFILIATE_ID`.

---
**IA Titanium**
*Pronto para implementar sob demanda.*
