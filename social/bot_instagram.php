<?php
// TITANIUM COMMENT RESPONDER - A MENTE CENTRAL 🛡️💎
// v2.0.0 - Smart Link Priority: Shopee Product Links > Site Links
$USER_TOKEN = "YOUR_IG_ACCESS_TOKEN";
$PAGE_ID = "YOUR_PAGE_ID";
$IG_BUSINESS_ID = "YOUR_IG_BUSINESS_ID";

// URL do site (usada para detectar links genéricos vs. links de produto)
$SITE_URL = "guiadodesconto.com.br";

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

$triggers = ["eu quero", "quero", "link", "valor", "preco", "preço", "eu quero o link"];

// Log com timestamp para debug
$debug_log = __DIR__ . "/bot_debug.log";
function bot_log($msg) {
    global $debug_log;
    $ts = date("Y-m-d H:i:s");
    file_put_contents($debug_log, "[{$ts}] {$msg}\n", FILE_APPEND);
    echo $msg . "<br>";
}

/**
 * 🧠 INTELIGÊNCIA DE SELEÇÃO DE LINK v2.0
 * 
 * Regras de prioridade (da maior para a menor):
 *   1. Link de PRODUTO Shopee (shopee.com.br/product ou s.shopee.com.br) 
 *      com a hashtag MAIS ESPECÍFICA (mais longa) encontrada na legenda.
 *   2. Link genérico do site (guiadodesconto.com.br) — usado apenas como fallback.
 *   3. #default — último recurso absoluto.
 */
function escolher_link_inteligente($caption, $dicionario_ofertas, $site_url) {
    $links_produto = [];  // hashtag => link (apenas links da Shopee)
    $links_site = [];     // hashtag => link (links do nosso site)
    
    foreach ($dicionario_ofertas as $hashtag => $link_oferta) {
        if ($hashtag === "#default") continue;
        
        // Verifica se a hashtag existe na legenda do post
        if (strpos($caption, strtolower($hashtag)) === false) continue;
        
        // Classifica: é link de produto Shopee ou link genérico do site?
        if (strpos($link_oferta, $site_url) !== false) {
            $links_site[$hashtag] = $link_oferta;
        } else {
            // É um link da Shopee (produto real) — PRIORIDADE MÁXIMA
            $links_produto[$hashtag] = $link_oferta;
        }
    }
    
    // PRIORIDADE 1: Se encontrou links de produto, pega o da hashtag mais específica
    if (!empty($links_produto)) {
        $melhor_hashtag = "";
        $melhor_link = "";
        foreach ($links_produto as $h => $l) {
            if (strlen($h) > strlen($melhor_hashtag)) {
                $melhor_hashtag = $h;
                $melhor_link = $l;
            }
        }
        bot_log("🎯 LINK PRODUTO selecionado via hashtag '{$melhor_hashtag}'");
        return $melhor_link;
    }
    
    // PRIORIDADE 2: Links genéricos do site (não ideal, mas funciona)
    if (!empty($links_site)) {
        $primeira_hashtag = array_key_first($links_site);
        bot_log("⚠️  FALLBACK SITE via hashtag '{$primeira_hashtag}' — considere adicionar link de produto no ofertas.json");
        return $links_site[$primeira_hashtag];
    }
    
    // PRIORIDADE 3: Default absoluto
    bot_log("⚠️  FALLBACK #default — nenhuma hashtag da legenda encontrada no ofertas.json");
    return isset($dicionario_ofertas["#default"]) ? $dicionario_ofertas["#default"] : "https://{$site_url}";
}

bot_log("🤖 TITANIUM CRON INICIADO...");

// 3. Buscar os 6 ultimos posts do Instagram
$media_url = "https://graph.facebook.com/v21.0/{$IG_BUSINESS_ID}/media?fields=id,caption&limit=6&access_token={$USER_TOKEN}";
$media_req = json_decode(file_get_contents($media_url), true);

if (!isset($media_req['data'])) die("Fim da lista de posts sem novidades.");

foreach ($media_req['data'] as $post) {
    if (!isset($post['id'])) continue;
    $media_id = $post['id'];
    $caption = isset($post['caption']) ? strtolower($post['caption']) : "";
    
    // 💡 INTELIGÊNCIA DE LINKS v2.0: Prioridade para links de PRODUTO
    $link_escolhido = escolher_link_inteligente($caption, $dicionario_ofertas, $SITE_URL);

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
            // Verificar se o link é de produto real ou apenas do site
            $is_product_link = (strpos($link_escolhido, $SITE_URL) === false);
            $link_label = $is_product_link ? "PRODUTO SHOPEE" : "SITE (fallback)";
            bot_log("🎯 Usuário: {$user} | Tipo: {$link_label} | Link: {$link_escolhido}");
            
            $public_msg = "Olá, {$user}! 🎁 Te enviei o link com todos os detalhes lá no seu Direct (Inbox)! Corre lá pra conferir. 🏃💨";
            
            // DM personalizada: se é link de produto, destaca o produto; se é site, direciona para o site
            if ($is_product_link) {
                $private_msg = "Olá, {$user}! 🎁 Aqui está o link certinho da oferta que você pediu no nosso post:\n\n🔗 Acessar Produto: {$link_escolhido}\n\nEspero que aproveite as condições especiais! Visite nossa página oficial: https://guiadodesconto.com.br \n\nEquipe Robô Titanium 🛡️💎";
            } else {
                $private_msg = "Olá, {$user}! 🎁 Confira as melhores ofertas na nossa página:\n\n🔗 Acessar Ofertas: {$link_escolhido}\n\nEquipe Robô Titanium 🛡️💎";
            }

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
            bot_log("✅ Disparo inteligente concluído para @{$user}");
        }
    }
}

file_put_contents($log_file, json_encode($responded_comments));
bot_log("✅ Fim do ciclo Titanium.");
?>
