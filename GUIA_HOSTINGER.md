# 🚀 Guia de Deploy: Hostinger & Robô Titanium

Este guia explica como colocar seu site no ar e configurar a atualização automática.

## Parte 1: Colocando o Site no Ar (Feito 1x)
Siga estes passos para "inaugurar" o site:

1.  **Acesse a Hostinger**:
    *   Entre no painel de Arquivos (onde você tirou o print).
    *   **Importante**: Dê um duplo clique na pasta **`public_html`** para entrar nela.
    *   (Se houver uma pasta "Guia do Desconto" lá dentro, **não entre nela**, use a `public_html` como raiz).
    *   Apague qualquer arquivo padrão (como `default.php`).

2.  **Upload dos Arquivos (O Segredo)**:
    *   No seu computador, abra a pasta `Robô Titanium`.
    *   Entre na pasta **`site`**.
    *   Selecione **TUDO** o que está dentro da pasta `site` (`index.html`, `robots.txt`, pasta `css`, pasta `js`, etc).
    *   Arraste esses arquivos para dentro da janela do **`public_html`** na Hostinger.
    *   **Resultado**: O arquivo `index.html` deve ficar solto direto dentro de `public_html`.

3.  **Teste**:
    *   Acesse `www.guiadodesconto.com.br` (ou seu domínio).
    *   O site deve carregar perfeitamente!

---

## Parte 2: Configurando a Automação (FTP)
Para que o Robô atualize o site sozinho, ele precisa de "permissão" para enviar arquivos.

1.  **Criar Conta FTP (Na Hostinger)**:
    *   No Painel, procure por **Contas FTP**.
    *   Crie um novo usuário (ex: `robo_updater`).
    *   Anote a **Senha** e o **Host** (geralmente `ftp.guiadodesconto.com.br`).

2.  **Configurar o Robô (No seu PC)**:
    *   Abra o arquivo `main.py` no VS Code.
    *   Lá no final, preencha os dados:
        ```python
        FTP_HOST = "ftp.guiadodesconto.com.br"
        FTP_USER = "u123456789" # Seu usuario criado
        FTP_PASS = "SuaSenhaSegura"
        ```
    *   Descomente (tire o `#`) da linha: `upload_to_hostinger(...)`.

## 🎉 Resultado Final
1.  O Robô roda no seu PC.
2.  Ele acha as ofertas.
3.  Ele conecta no FTP.
4.  Ele atualiza o `data.json` na Hostinger.
5.  O cliente entra no site e vê os preços novos na hora.
