<?php
// TITANIUM COMMENT RESPONDER - A MENTE CENTRAL 🛡️💎
$USER_TOKEN = "YOUR_IG_ACCESS_TOKEN";
$PAGE_ID = "YOUR_PAGE_ID";
$IG_BUSINESS_ID = "YOUR_IG_BUSINESS_ID";

// 1. Converter automaticamente o User Token em Page Token para a DM funcionar
$auth_url = "https://graph.facebook.com/v21.0/me/accounts?access_token={$USER_TOKEN}";
$auth_req = json_decode(file_get_contents($auth_url), true);
$PAGE_TOKEN = $USER_TOKEN; 

if (isset($auth_req['data'])) {
    foreach ($auth_req['data'] as $page) {
        if ($page['id'] == $PAGE_ID) {
            $PAGE_TOKEN = $page['access_token'];
            break;
        }
    }
}

// 2. Banco de Dados Leve e Inteligência de Links
$log_file = __DIR__ . "/comment_responses.json";
if (!file_exists($log_file)) file_put_contents($log_file, json_encode([]));
$responded_comments = json_decode(file_get_contents($log_file), true);

$ofertas_file = __DIR__ . "/ofertas.json";
if (!file_exists($ofertas_file)) {
    die("Arquivo de ofertas.json nao encontrado!");
}
$dicionario_ofertas = json_decode(file_get_contents($ofertas_file), true);

$triggers = ["eu quero", "quero", "link", "valor", "preco", "preco", "eu quero o link"];

echo "🤖 TITANIUM CRON INICIADO...<br>";

// 3. Buscar os 6 ultimos posts do Instagram
$media_url = "https://graph.facebook.com/v21.0/{$IG_BUSINESS_ID}/media?fields=id,caption&limit=6&access_token={$USER_TOKEN}";
$media_req = json_decode(file_get_contents($media_url), true);

if (!isset($media_req['data'])) die("Fim da lista de posts sem novidades.");

foreach ($media_req['data'] as $post) {
    if (!isset($post['id'])) continue;
    $media_id = $post['id'];
    $caption = isset($post['caption']) ? strtolower($post['caption']) : "";
    
    // 💡 INTELIGÊNCIA DE LINKS: Identificando a hashtag secreta na legenda
    $link_escolhido = isset($dicionario_ofertas["#default"]) ? $dicionario_ofertas["#default"] : "https://guiadodesconto.com.br";
    foreach ($dicionario_ofertas as $hashtag => $link_oferta) {
        if ($hashtag !== "#default" && strpos($caption, strtolower($hashtag)) !== false) {
            $link_escolhido = $link_oferta;
            break;
        }
    }

    // Buscar comentários daquele post
    $comments_url = "https://graph.facebook.com/v21.0/{$media_id}/comments?fields=id,text,username&access_token={$USER_TOKEN}";
    $comments_req = json_decode(file_get_contents($comments_url), true);
    if (!isset($comments_req['data'])) continue;

    foreach ($comments_req['data'] as $comment) {
        $comment_id = $comment['id'];
        $text = strtolower($comment['text']);
        $user = isset($comment['username']) ? $comment['username'] : "usuario";

        if (in_array($comment_id, $responded_comments)) continue;

        // Verificar o Gatilho
        $triggered = false;
        foreach ($triggers as $trigger) {
            if (strpos($text, $trigger) !== false) {
                $triggered = true;
                break;
            }
        }

        if ($triggered) {
            echo "🎯 Usuário: {$user} | Link Injetado: {$link_escolhido} <br>";
            $public_msg = "Olá, {$user}! 🎁 Te enviei o link com todos os detalhes lá no seu Direct (Inbox)! Corre lá pra conferir. 🏃💨";
            $private_msg = "Olá, {$user}! 🎁 Aqui está o link certinho da oferta que você pediu no nosso post:\n\n🔗 Acessar Produto: {$link_escolhido}\n\nEspero que aproveite as condições especiais! Visite nossa página oficial: https://guiadodesconto.com.br \n\nEquipe Robô Titanium 🛡️💎";

            // Envia COMENTÁRIO PÚBLICO
            $ch_pub = curl_init();
            curl_setopt($ch_pub, CURLOPT_URL, "https://graph.facebook.com/v21.0/{$comment_id}/replies");
            curl_setopt($ch_pub, CURLOPT_POST, 1);
            curl_setopt($ch_pub, CURLOPT_POSTFIELDS, http_build_query(["message" => $public_msg, "access_token" => $USER_TOKEN]));
            curl_setopt($ch_pub, CURLOPT_RETURNTRANSFER, true); curl_exec($ch_pub); curl_close($ch_pub);

            // Envia MENSAGEM DIRETA (DM) COM LINK INTELIGENTE
            $ch_priv = curl_init();
            curl_setopt($ch_priv, CURLOPT_URL, "https://graph.facebook.com/v21.0/{$PAGE_ID}/messages?access_token={$PAGE_TOKEN}");
            curl_setopt($ch_priv, CURLOPT_POST, 1);
            curl_setopt($ch_priv, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            $payload = json_encode([ "recipient" => ["comment_id" => $comment_id], "message" => ["text" => $private_msg] ]);
            curl_setopt($ch_priv, CURLOPT_POSTFIELDS, $payload);
            curl_setopt($ch_priv, CURLOPT_RETURNTRANSFER, true); curl_exec($ch_priv); curl_close($ch_priv);

            // Grava para nao responder 2 vezes
            array_push($responded_comments, $comment_id);
            echo "✅ Disparo inteligente concluído. <br>";
        }
    }
}

file_put_contents($log_file, json_encode($responded_comments));
echo "✅ Fim do ciclo Titanium.<br>";
?>
