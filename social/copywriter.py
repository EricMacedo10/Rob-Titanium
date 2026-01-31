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
        # Seleção de Hashtags Dinâmicas
        cat_key = category.lower() if category else "default"
        tags = self.hashtags_por_categoria.get(cat_key, self.hashtags_por_categoria["default"])
        tags_fixas = "#amazon #mercadolivre #shopee"
        
        # Gatilhos Mentais baseados no Desconto
        if discount > 30:
            header = f"{random.choice(self.emojis_urgencia)} PREÇO DE BLACK FRIDAY! {random.choice(self.emojis_urgencia)}"
            hook = f"Encontramos esse {title} com um desconto ABSURDO de {discount}%!"
        elif discount > 15:
            header = f"{random.choice(self.emojis_sucesso)} OFERTA SELECIONADA {random.choice(self.emojis_sucesso)}"
            hook = f"Oportunidade real! {title} com {discount}% de desconto na {store}."
        else:
            header = f"🔥 ACHADO DO DIA 🔥"
            hook = f"Olha o que acabou de baixar de preço: {title} na {store}!"

        # Corpo da Legenda
        body = (
            f"\n\n{hook}\n\n"
            f"💵 Por apenas: R$ {price}\n"
            f"🏪 Loja: {store}\n"
            f"🛡️ Compra 100% Segura e Verificada pelo Robô Titanium.\n\n"
            f"{random.choice(self.ctas)}\n\n"
            f"👇 Marque alguém que precisa ver isso!\n\n"
            f"{tags} {tags_fixas}"
        )
        
        return header + body

if __name__ == "__main__":
    # Teste rápido
    copy = Copywriter()
    print(copy.generate_caption("Teclado Gamer Mecânico", "199,90", "Amazon", 45))
