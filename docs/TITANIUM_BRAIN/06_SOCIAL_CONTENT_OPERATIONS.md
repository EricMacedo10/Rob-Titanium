# 📸 Titanium Brain: Social Content Operations

Este documento descreve como gerenciar manualmente a fila de postagens do Robô Titanium.

## 📂 Gerenciamento da Fila (`social/fila/`)

O robô prioriza arquivos nesta pasta antes de gerar banners automáticos.

### 🏷️ Regras de Nomenclatura
Os arquivos devem seguir o padrão: `YYYY-MM-DD_loja_categoria.ext`
*   **Exemplo**: `2026-02-20_amazon_ofertas_do_dia.jpeg`
*   **Data**: Define quando a postagem será realizada.
*   **Loja**: `amazon`, `shopee`, `mercadolivre` ou combinados.
*   **Categoria**: Descrição curta do conteúdo.

### 🖼️ Formatos Suportados
- **Imagens**: `.jpeg`, `.jpg`, `.png` (Serão convertidas para vídeo com efeito Zoom).
- **Vídeos**: `.mp4` (Máximo 60 segundos, 720p preferencial).

### 📝 Legendas Automáticas
O robô utiliza o **Copywriter AI** para gerar a legenda com base no nome do arquivo e na data. Se quiser uma legenda específica, o sistema busca um arquivo `.txt` com o mesmo nome da imagem.

## 📅 Estratégia de Conteúdo
- **Frequência**: 1 postagem por dia (ciclo automático).
- **Buffer**: Recomenda-se manter pelo menos **7 dias** de fila preenchida.
- **Datas Comemorativas**: Priorizar artes manuais na fila para eventos como "Dia da Mulher", "Black Friday", etc.
