<?php
// TITANIUM COMMENT RESPONDER - MÓDULO PESCA TITANIUM
// Script para ler e responder automaticamente DMs e Comentários do Instagram.
// Deve ser hospedado no seu servidor (Hostinger/cPanel) e executado via Cron Job a cada 5 ou 10 minutos.

// -----------------------------------------------------------------------------------
// ⚠️ ATENÇÃO: PREENCHA OS SEUS DADOS AQUI ANTES DE SUBIR PARA O SERVIDOR!
// -----------------------------------------------------------------------------------
$USER_TOKEN = "EAAaEM60tZA1cBRopTTA9h5Y84uLXZAZCVdWIUnV6UR6gS2BfPfSdQkZB0RwXbC2RRcLaThpVCL9dGYT3hpyBuAAXinpZC0umxoxa3tQZB6FgiAFrvoh0YgMFMkXKZAmgnZCfm8QuDRvqF2y4RqtfQkmPuCHIMgpPpDWGFwE3vEa6ZBhyehLZCD4wv47ZCvAZAIHpIQZDZD"; // Aquele token longo de 60 dias da Meta
$PAGE_ID = "1165552696646721"; // ID da página do Facebook atrelada
$IG_BUSINESS_ID = "17841416991677908"; // ID do IG da Pesca Titanium (Já preenchido para você)
$SITE_URL = "guiadodesconto.com.br"; // Mantendo a estrutura principal
// -----------------------------------------------------------------------------------

// Log com timestamp para debug
$debug_log = __DIR__ . "/bot_debug_pesca.log";
function bot_log($msg) {
    global $debug_log;
    $ts = date("Y-m-d H:i:s");
    file_put_contents($debug_log, "[{$ts}] {$msg}\n", FILE_APPEND);
    echo $msg . "<br>";
}

// Função auxiliar para cURL (Obrigatório em Hostinger/CPANEL)
function curl_get_contents($url) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_TIMEOUT, 30);
    $data = curl_exec($ch);
    $error = curl_error($ch);
    curl_close($ch);
    if ($error) bot_log("❌ ERRO cURL: " . $error);
    return $data;
}

// 1. Converter automaticamente o User Token em Page Token para a DM funcionar
$auth_url = "https://graph.facebook.com/v21.0/me/accounts?access_token={$USER_TOKEN}";
$auth_req = json_decode(curl_get_contents($auth_url), true);
$PAGE_TOKEN = $USER_TOKEN; 

if (isset($auth_req['data'])) {
    foreach ($auth_req['data'] as $page) {
        if ($page['id'] == $PAGE_ID) {
            $PAGE_TOKEN = $page['access_token'];
            break;
        }
    }
}

// 2. Banco de Dados Leve e Inteligência de Links (Diretório Isolado para a Pesca)
$log_file = __DIR__ . "/pesca_comment_responses.json";
if (!file_exists($log_file)) file_put_contents($log_file, json_encode([]));
$responded_comments = json_decode(file_get_contents($log_file), true);

$ofertas_file = __DIR__ . "/ofertas_pesca.json";

// 🚀 TITANIUM SYNC (PESCA): Busca o dicionário sempre atualizado do GitHub Raw (CDN da Fastly).
$GITHUB_RAW_OFERTAS = "https://raw.githubusercontent.com/EricMacedo10/Rob-Titanium/main/pesca/ofertas_pesca.json";

$github_json = @file_get_contents($GITHUB_RAW_OFERTAS);
if ($github_json !== false) {
    $github_data = json_decode($github_json, true);
    if (is_array($github_data) && count($github_data) > 0) {
        $dicionario_ofertas = $github_data;
        @file_put_contents($ofertas_file, $github_json); 
        bot_log("✅ ofertas_pesca.json sincronizado do GitHub (" . count($dicionario_ofertas) . " entradas).");
    } else {
        bot_log("⚠️ GitHub retornou JSON inválido. Usando cache local como fallback.");
        if (!file_exists($ofertas_file)) die("Arquivo de ofertas_pesca.json nao encontrado!");
        $dicionario_ofertas = json_decode(file_get_contents($ofertas_file), true);
    }
} else {
    bot_log("⚠️ GitHub Raw inacessível. Usando cache local.");
    if (!file_exists($ofertas_file)) die("Arquivo de ofertas_pesca.json nao encontrado!");
    $dicionario_ofertas = json_decode(file_get_contents($ofertas_file), true);
}

$triggers = ["eu quero", "quero", "link", "valor", "preco", "preço", "eu quero o link"];



/**
 * TITANIUM SHIELD v3.0 (PHP) — Nuclear Shield v5.0
 */
function titanium_shield($url) {
    $already_shielded = ['s.shopee.com.br', 'shope.ee'];
    foreach ($already_shielded as $domain) {
        if (strpos($url, $domain) !== false) {
            return $url; 
        }
    }
    $shopee_domains = ['shopee.com.br'];
    $is_shopee = false;
    foreach ($shopee_domains as $d) {
        if (strpos($url, $d) !== false) { $is_shopee = true; break; }
    }
    if (empty($url) || !$is_shopee) {
        return $url;
    }
    return $url;
}

/**
 * TITANIUM BRIDGE v2.0 — Anti-Instagram In-App Browser
 */
function titanium_bridge($url) {
    if (strpos($url, 'guiadodesconto.com.br') !== false) {
        return $url;
    }
    $shopee_hosts = ['shopee.com.br', 's.shopee.com.br', 'shope.ee'];
    $is_shopee = false;
    foreach ($shopee_hosts as $h) {
        if (strpos($url, $h) !== false) { $is_shopee = true; break; }
    }
    if (!$is_shopee) return $url;

    return "https://guiadodesconto.com.br/pesca.php?url=" . urlencode($url);
}

function escolher_link_inteligente($caption, $dicionario_ofertas, $site_url) {
    $caption_lower = strtolower($caption);
    $links_produto = [];
    
    // CAMADA 1: Hashtags exatas
    foreach ($dicionario_ofertas as $hashtag => $link_oferta) {
        if ($hashtag === "#default" || $hashtag === "#latest_story") continue;
        if (strpos($caption_lower, strtolower($hashtag)) !== false) {
            $links_produto[$hashtag] = $link_oferta;
        }
    }
    
    $final_link = "";
    
    // Seleção do melhor link entre os encontrados
    if (empty($final_link) && !empty($links_produto)) {
        $links_reais = [];
        foreach ($links_produto as $h => $l) {
            if (strpos($l, $site_url) === false) {
                $links_reais[$h] = $l;
            }
        }
        
        $lista_selecao = !empty($links_reais) ? $links_reais : $links_produto;
        
        $melhor_hashtag = "";
        $melhor_link = "";
        foreach ($lista_selecao as $h => $l) {
            if (strlen($h) > strlen($melhor_hashtag)) {
                $melhor_hashtag = $h;
                $melhor_link = $l;
            }
        }
        $final_link = $melhor_link;
    }
    
    if (empty($final_link)) {
        bot_log("⚠️  FALLBACK TOTAL — Nenhuma hashtag ou palavra-chave serviu.");
        $final_link = isset($dicionario_ofertas["#default"]) ? $dicionario_ofertas["#default"] : "https://{$site_url}";
    }

    return titanium_shield($final_link);
}

bot_log("🎣 TITANIUM PESCA CRON INICIADO...");

// 3. Buscar os 20 ultimos posts do Instagram (Feed e Reels)
$media_url = "https://graph.facebook.com/v21.0/{$IG_BUSINESS_ID}/media?fields=id,caption&limit=20&access_token={$USER_TOKEN}";
$media_req = json_decode(curl_get_contents($media_url), true);

if (!isset($media_req['data'])) {
    bot_log("⚠️ Erro na API ou sem posts: " . json_encode($media_req));
    die("Fim da lista de posts sem novidades.");
}

foreach ($media_req['data'] as $post) {
    if (!isset($post['id'])) continue;
    $media_id = $post['id'];
    $caption = isset($post['caption']) ? strtolower($post['caption']) : "";
    
    $link_escolhido = escolher_link_inteligente($caption, $dicionario_ofertas, $SITE_URL);

    // Buscar comentários daquele post
    $comments_url = "https://graph.facebook.com/v21.0/{$media_id}/comments?fields=id,text,username&access_token={$USER_TOKEN}";
    $comments_req = json_decode(curl_get_contents($comments_url), true);
    if (!isset($comments_req['data'])) continue;

    foreach ($comments_req['data'] as $comment) {
        $comment_id = $comment['id'];
        $text = strtolower($comment['text']);
        $user = isset($comment['username']) ? $comment['username'] : "pescador";

        if (in_array($comment_id, $responded_comments)) continue;

        $triggered = false;
        foreach ($triggers as $trigger) {
            if (strpos($text, $trigger) !== false) {
                $triggered = true;
                break;
            }
        }

        if ($triggered) {
            $is_product_link = (strpos($link_escolhido, $SITE_URL) === false);
            bot_log("🎯 Usuário: {$user} | Link Feed/Reels: {$link_escolhido}");
            
            $public_msg = "Olá, pescador(a)! 🎣 Te enviei o link com todos os detalhes lá no seu Direct (Inbox)! Boa pescaria! 🏃💨";
            
            $link_dm = titanium_bridge($link_escolhido);

            if ($is_product_link) {
                $private_msg = "Ola! Aqui esta o link direto para a isca/tralha que voce pediu:\n\nACESSAR PRODUTO: {$link_dm}\n\nEquipe Pesca Titanium";
            } else {
                $private_msg = "Ola! Aqui esta o link direto para a isca/tralha que voce pediu:\n\nACESSAR PRODUTO: {$link_dm}\n\nEquipe Pesca Titanium";
            }

            // Envia COMENTÁRIO PÚBLICO
            $ch_pub = curl_init();
            curl_setopt($ch_pub, CURLOPT_URL, "https://graph.facebook.com/v21.0/{$comment_id}/replies");
            curl_setopt($ch_pub, CURLOPT_POST, 1);
            curl_setopt($ch_pub, CURLOPT_POSTFIELDS, http_build_query(["message" => $public_msg, "access_token" => $USER_TOKEN]));
            curl_setopt($ch_pub, CURLOPT_RETURNTRANSFER, true); curl_exec($ch_pub); curl_close($ch_pub);

            // Envia MENSAGEM DIRETA (DM)
            $ch_priv = curl_init();
            curl_setopt($ch_priv, CURLOPT_URL, "https://graph.facebook.com/v21.0/{$PAGE_ID}/messages?access_token={$PAGE_TOKEN}");
            curl_setopt($ch_priv, CURLOPT_POST, 1);
            curl_setopt($ch_priv, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
            $payload = json_encode([ "recipient" => ["comment_id" => $comment_id], "message" => ["text" => $private_msg] ]);
            curl_setopt($ch_priv, CURLOPT_POSTFIELDS, $payload);
            curl_setopt($ch_priv, CURLOPT_RETURNTRANSFER, true); curl_exec($ch_priv); curl_close($ch_priv);

            array_push($responded_comments, $comment_id);
            bot_log("✅ Disparo inteligente concluído para @{$user}");
        }
    }
}

// 4. Bônus: Buscar DMs Recentes (Respostas a Stories)
bot_log("🔍 Verificando DMs Recentes (Stories)...");
$conv_url = "https://graph.facebook.com/v21.0/{$PAGE_ID}/conversations?platform=instagram&fields=messages.limit(2){id,message,from,created_time}&limit=5&access_token={$PAGE_TOKEN}";
$conv_req = json_decode(curl_get_contents($conv_url), true);

if (isset($conv_req['data'])) {
    foreach ($conv_req['data'] as $conv) {
        if (!isset($conv['messages']['data'])) continue;
        foreach ($conv['messages']['data'] as $msg) {
            $msg_id = $msg['id'];
            $text = isset($msg['message']) ? strtolower($msg['message']) : "";
            
            if (!isset($msg['from']) || !isset($msg['from']['id'])) continue;
            
            $sender_id = $msg['from']['id'];
            
            if ($sender_id == $PAGE_ID || $sender_id == $IG_BUSINESS_ID) continue; 
            if (in_array($msg_id, $responded_comments)) continue;
            
            $triggered = false;
            foreach ($triggers as $trigger) {
                if (strpos($text, $trigger) !== false) {
                    $triggered = true;
                    break;
                }
            }
            
            if ($triggered) {
                bot_log("🎯 DM Detectada (Story) de Sender {$sender_id}: {$text}");
                $link_story = isset($dicionario_ofertas["#latest_story"]) ? $dicionario_ofertas["#latest_story"] : "https://{$SITE_URL}";
                $link_story = titanium_shield($link_story);
                
                $link_story_dm = titanium_bridge($link_story);

                $is_product = (strpos($link_story, $SITE_URL) === false);
                if ($is_product) {
                    $dm_reply = "Ola! Aqui esta o link direto para a isca/tralha que voce pediu:\n\nACESSAR PRODUTO: {$link_story_dm}\n\nEquipe Pesca Titanium";
                } else {
                    $dm_reply = "Ola! Aqui esta o link direto para a isca/tralha que voce pediu:\n\nACESSAR PRODUTO: {$link_story_dm}\n\nEquipe Pesca Titanium";
                }
                
                $ch_priv = curl_init();
                curl_setopt($ch_priv, CURLOPT_URL, "https://graph.facebook.com/v21.0/{$PAGE_ID}/messages?access_token={$PAGE_TOKEN}");
                curl_setopt($ch_priv, CURLOPT_POST, 1);
                curl_setopt($ch_priv, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
                $payload = json_encode([ "recipient" => ["id" => $sender_id], "message" => ["text" => $dm_reply] ]);
                curl_setopt($ch_priv, CURLOPT_POSTFIELDS, $payload);
                curl_setopt($ch_priv, CURLOPT_RETURNTRANSFER, true); curl_exec($ch_priv); curl_close($ch_priv);
                
                array_push($responded_comments, $msg_id);
                bot_log("✅ Disparo DM Story concluído para Sender {$sender_id}");
            }
        }
    }
}

file_put_contents($log_file, json_encode($responded_comments));
bot_log("✅ Fim do ciclo Titanium Pesca.");
?>
