from social.image_generator import ImageGenerator
import os

# Ajuste do caminho dos assets para o teste local
gen = ImageGenerator(assets_path="site/images")

# Produto real extraído do data.json (Simulado)
test_product = {
    "title": "Monitor Gamer LG UltraGear 27' Full HD, 144Hz, 1ms",
    "price": "1.349,00",
    "image": "https://m.media-amazon.com/images/I/71ovN4v2YFL._AC_SL1500_.jpg",
    "store": "amazon"
}

output = "test_instagram_post.jpg"

print(f"🎨 Gerando arte de teste para: {test_product['title']}...")
gen.generate_post(
    test_product['title'],
    test_product['price'],
    test_product['image'],
    test_product['store'],
    output
)

print(f"✅ Arte gerada com sucesso: {os.path.abspath(output)}")
