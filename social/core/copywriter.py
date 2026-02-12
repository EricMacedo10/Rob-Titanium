import random

class Copywriter:
    """
    Motor de Copywriting para o Robô Titanium.
    Gera legendas persuasivas e dinâmicas para Instagram.
    """
    
    def __init__(self):
        self.emojis_urgencia = ["🚨", "🔥", "⚠️", "⏳", "💣"]
        self.emojis_sucesso = ["✅", "🏆", "💎", "⭐", "💰"]
        self.ctas = [
            "Link na Bio! 🔗",
            "Garanta o seu no link da Bio! 🛒",
            "Corre pro link na Bio antes que acabe! 🏃‍♂️",
            "Confira essa e outras ofertas no link da Bio! ✨",
            "Acesse o link na Bio e aproveite! 🚀"
        ]
        # Hashtags Dinâmicas por Categoria
        self.hashtags_por_categoria = {
            "tecnologia": "#tecnologia #setupgamer #gadgets #informatica #ti",
            "casa": "#decoracao #utilidades #casanova #cozinha #home",
            "beleza": "#autocuidado #maquiagem #skincare #beleza #cosmeticos",
            "esportes": "#fitness #academia #treino #vidasaudavel #esporte",
            "volta-aulas": "#papelaria #estudos #volta-aulas #concurso #organizacao",
            "default": "#compras #ofertas #desconto #promocao #titanium"
        }
        
    def generate_caption(self, title, price, store, discount=0, category="default"):
        """
        Gera uma legenda completa baseada nos dados do produto.
        """
        cat_key = category.lower() if category else "default"
        tags = self.hashtags_por_categoria.get(cat_key, self.hashtags_por_categoria["default"])
        tags_fixas = "#amazon #mercadolivre #shopee #guiadodesconto"
        
        if discount > 30:
            header = f"{random.choice(self.emojis_urgencia)} PREÇO DE BLACK FRIDAY! {random.choice(self.emojis_urgencia)}"
            hook = f"Encontramos esse {title} com um desconto ABSURDO de {discount}%!"
        elif discount > 15:
            header = f"{random.choice(self.emojis_sucesso)} OFERTA SELECIONADA {random.choice(self.emojis_sucesso)}"
            hook = f"Oportunidade real! {title} com {discount}% de desconto na {store}."
        else:
            header = f"🔥 ACHADO DO DIA 🔥"
            hook = f"Olha o que acabou de baixar de preço: {title} na {store}!"

        body = (
            f"\n\n{hook}\n\n"
            f"💵 Por apenas: R$ {price}\n"
            f"🏪 Loja: {store}\n"
            f"🛡️ Compra Segura e Verificada pelo Robô Titanium.\n\n"
            f"🌐 Confira no nosso site:\n"
            f"👉 guiadodesconto.com.br\n\n"
            f"{random.choice(self.ctas)}\n\n"
            f"{tags} {tags_fixas}"
        )
        
        return header + body

    def generate_category_caption(self, store, category):
        """
        Gera legenda para postagens temáticas de categorias.
        """
        header = f"🚀 {category.upper()} NA {store.upper()}! 🚀"
        
        frases = [
            f"Selecionamos as melhores ofertas de {category} na {store} especialmente para você!",
            f"Procurando por {category}? A {store} está com promoções imperdíveis hoje.",
            f"O Robô Titanium vasculhou a {store} e encontrou os maiores descontos em {category}."
        ]
        
        tags = self.hashtags_por_categoria.get(category.lower(), self.hashtags_por_categoria["default"])
        tags_fixas = f"#{store.lower()} #guiadodesconto #ofertas #promocao"
        
        body = (
            f"\n\n{random.choice(frases)}\n\n"
            f"Não perca mais tempo procurando! Os melhores preços e cupons já estão organizados no nosso site.\n\n"
            f"🌐 Acesse agora:\n"
            f"👉 guiadodesconto.com.br\n\n"
            f"🔗 {random.choice(self.ctas)}\n\n"
            f"{tags} {tags_fixas}"
        )
        
        return header + body

if __name__ == "__main__":
    # Teste rápido
    copy = Copywriter()
    print(copy.generate_caption("Teclado Gamer Mecânico", "199,90", "Amazon", 45))
