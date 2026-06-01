<?php
// TITANIUM COMMENT RESPONDER - A MENTE CENTRAL 🛡️💎
// v2.1.0 - Nuclear Shield PHP v4.0: Respeita Short Links Oficiais (s.shopee.com.br)
$USER_TOKEN = "EAAaEM60tZA1cBRdsRAyvi6ZBsuiNZAYZCb8oD834L4jJhr0AN9Ve39BZAsBTOzirx6BOZCxOO8w1wBuHjZB082MyJNpqZBUclig5KHsDIJKCEe6Pn2bJoS4p7yVNwJ7AoHyg5lRCd8ofHMnlhcbwQTBP19ByHzhUP34BLrFseWqBvZCWrbNefsoUi99ZCtZA9DZCwOhskA7ZAbXLn06BW728ftQZDZD";
$PAGE_ID = "1032000233318987";
$IG_BUSINESS_ID = "17841480460125461";

// URL do site (usada para detectar links genéricos vs. links de produto)
$SITE_URL = "guiadodesconto.com.br";

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
 * 🧠 INTELIGÊNCIA DE SELEÇÃO DE LINK v2.1
 * 
 * Regras de prioridade (da maior para a menor):
 *   1. Hashtag Match: Encontrou hashtag específica na legenda.
 *   2. Keyword Match (NOVA): Se não tem hashtag, procura palavras da legenda no dicionário.
 *   3. Default: Fallback para o site.
 */
/**
 * 🛡️ TITANIUM SHIELD v2.0 (PHP Version) — Nuclear Shield v4.0
 * 
 * Política de Blindagem:
 * 1. Links já no formato s.shopee.com.br (Short Links Oficiais) são passados sem modificação.
 *    Estes já contêm a tag de afiliado injetada pelo script Python (shield.py).
 * 2. Links shopee.com.br brutos (que escaparam da blindagem Python) recebem utm_source como
 *    fallback de segurança. Este cenário não deveria ocorrer em operação normal.
 * 3. Links não-Shopee passam sem modificação.
 */
function titanium_shield($url) {
    if (empty($url) || strpos($url, 'shopee.com.br') === false) {
        return $url; // Não é um link Shopee — passa livre
    }

    // CAMADA 1: Short Link Oficial já blindado pelo Python — passa sem modificação
    if (strpos($url, 's.shopee.com.br') !== false) {
        return $url;
    }

    // CAMADA 2 (Fallback de Segurança): Link bruto que escapou da blindagem Python
    // Injeta utm_source como sinal de rastreamento mínimo
    $tag = "an_18318830863";
    $query = parse_url($url, PHP_URL_QUERY);
    $params = [];
    if ($query) {
        parse_str($query, $params);
    }
    // Só injeta se ainda não tiver a tag
    if (!isset($params['utm_source']) || $params['utm_source'] !== $tag) {
        $params['utm_source'] = $tag;
    }
    $new_query = http_build_query($params);
    $path   = parse_url($url, PHP_URL_PATH);
    $scheme = parse_url($url, PHP_URL_SCHEME);
    $host   = parse_url($url, PHP_URL_HOST);
    return "{$scheme}://{$host}{$path}?{$new_query}";
}

function escolher_link_inteligente($caption, $dicionario_ofertas, $site_url) {
    $caption_lower = strtolower($caption);
    $links_produto = [];
    
    // CAMADA 1: Hashtags exatas (OFERTAS.JSON)
    foreach ($dicionario_ofertas as $hashtag => $link_oferta) {
        if ($hashtag === "#default") continue;
        if (strpos($caption_lower, strtolower($hashtag)) !== false) {
            $links_produto[$hashtag] = $link_oferta;
        }
    }
    
    // CAMADA 2: Keyword Match (OFERTAS.JSON)
    if (empty($links_produto)) {
        foreach ($dicionario_ofertas as $hashtag => $link_oferta) {
            if ($hashtag === "#default") continue;
            $keyword = str_replace('#', '', strtolower($hashtag));
            $keyword_clean = str_replace('_', ' ', $keyword);
            if (strpos($caption_lower, $keyword) !== false || strpos($caption_lower, $keyword_clean) !== false) {
                $links_produto[$hashtag] = $link_oferta;
            }
        }
    }
    
    // CAMADA 3: BUSCA DINÂMICA NO BANCO DE DADOS (DATA.JSON) - 🎯 SOLUÇÃO DEFINITIVA
    $db_path = __DIR__ . "/data.json"; 
    if (!file_exists($db_path) && isset($_SERVER['DOCUMENT_ROOT'])) $db_path = $_SERVER['DOCUMENT_ROOT'] . "/data.json"; 
    if (!file_exists($db_path)) $db_path = __DIR__ . "/../site/data.json"; 
    
    $final_link = "";

    if (empty($links_produto) && file_exists($db_path)) {
        $data_json = json_decode(file_get_contents($db_path), true);
        if (is_array($data_json)) {
            foreach ($data_json as $item) {
                $item_title = strtolower($item['title']);
                
                // Limpeza básica para match mais preciso
                $caption_words = explode(' ', preg_replace('/[^\p{L}\p{N}\s]/u', ' ', $caption_lower));
                $title_words = explode(' ', preg_replace('/[^\p{L}\p{N}\s]/u', ' ', $item_title));
                $intersection = array_intersect($title_words, $caption_words);
                
                // Filtra palavras curtas (de, com, o, a) e palavras genéricas (boilerplate) para evitar falsos positivos
                $boilerplate = ['shopee', 'selecao', 'exclusiva', 'novidades', 'incriveis', 'comente', 'quero', 'nosso', 'robo', 'titanium', 'manda', 'todos', 'links', 'direct', 'titaniumbot', 'shopeebrasil', 'achadinhos', 'moda', 'curadoria', 'para', 'voce', 'aqui', 'seu', 'que'];
                $intersection = array_filter($intersection, function($word) use ($boilerplate) {
                    return strlen($word) > 2 && !in_array($word, $boilerplate);
                });
                
                // Se 2 ou mais palavras SIGNIFICATIVAS batem, é o produto! (Mais agressivo)
                if (count($intersection) >= 2) {
                    bot_log("💎 BANCO DE DADOS MATCH: '{$item['title']}' encontrado na legenda!");
                    $final_link = $item['link'];
                    break;
                }
            }
        }
    } else if (empty($links_produto)) {
        bot_log("⚠️ Alerta: Banco de dados data.json nao encontrado em: {$db_path}");
    }
    
    // Seleção do melhor link entre os encontrados (Camada 1 e 2)
    if (empty($final_link) && !empty($links_produto)) {
        // Filtrar e priorizar links de produto reais (que não contêm o site_url)
        $links_reais = [];
        foreach ($links_produto as $h => $l) {
            if (strpos($l, $site_url) === false) {
                $links_reais[$h] = $l;
            }
        }
        
        // Se houver algum link de produto real, usamos apenas eles para a seleção
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

    // APLICA BLINDAGEM ANTES DE RETORNAR
    return titanium_shield($final_link);
}

bot_log("🤖 TITANIUM CRON INICIADO...");

// 3. Buscar os 20 ultimos posts do Instagram (Varredura Ampla)
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
    
    // 💡 INTELIGÊNCIA DE LINKS v2.0: Prioridade para links de PRODUTO
    $link_escolhido = escolher_link_inteligente($caption, $dicionario_ofertas, $SITE_URL);

    // Buscar comentários daquele post
    $comments_url = "https://graph.facebook.com/v21.0/{$media_id}/comments?fields=id,text,username&access_token={$USER_TOKEN}";
    $comments_req = json_decode(curl_get_contents($comments_url), true);
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
            
            // DM personalizada: Sempre envia o link direto E o link do site para conveniência
            if ($is_product_link) {
                $private_msg = "Olá, {$user}! 🎁 Aqui está o link direto para o produto que você amou:\n\n🔗 ACESSAR PRODUTO: {$link_escolhido}\n\nE se quiser ver mais achadinhos incríveis da Shopee, visite nossa vitrine completa:\n🌐 SITE OFICIAL: https://guiadodesconto.com.br\n\nEquipe Robô Titanium 🛡️💎";
            } else {
                $private_msg = "Olá, {$user}! 🎁 Como o post é novo, o link direto está sendo processado, mas você já pode conferir esta e outras ofertas na nossa vitrine oficial:\n\n🔗 VITRINE TITANIUM: {$link_escolhido}\n\nEquipe Robô Titanium 🛡️💎";
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
            
            // Tratamento defensivo para $msg['from']
            if (!isset($msg['from']) || !isset($msg['from']['id'])) continue;
            
            $sender_id = $msg['from']['id'];
            
            if ($sender_id == $PAGE_ID || $sender_id == $IG_BUSINESS_ID) continue; // Ignora as proprias respostas
            if (in_array($msg_id, $responded_comments)) continue;
            
            $triggered = false;
            foreach ($triggers as $trigger) {
                if (strpos($text, $trigger) !== false) {
                    $triggered = true;
                    break;
                }
            }
            
            if ($triggered) {
                bot_log("🎯 DM Detectada de Sender {$sender_id}: {$text}");
                $link_story = isset($dicionario_ofertas["#latest_story"]) ? $dicionario_ofertas["#latest_story"] : "https://{$SITE_URL}";
                $link_story = titanium_shield($link_story);
                
                $is_product = (strpos($link_story, $SITE_URL) === false);
                if ($is_product) {
                    $dm_reply = "Olá! 🎁 Aqui está o link direto para o produto do Story que você amou:\n\n🔗 ACESSAR PRODUTO: {$link_story}\n\nE se quiser ver mais achadinhos incríveis da Shopee, visite nossa vitrine completa:\n🌐 SITE OFICIAL: https://guiadodesconto.com.br\n\nEquipe Robô Titanium 🛡️💎";
                } else {
                    $dm_reply = "Olá! 🎁 Confira esta e outras ofertas na nossa vitrine oficial:\n\n🔗 VITRINE TITANIUM: {$link_story}\n\nEquipe Robô Titanium 🛡️💎";
                }
                
                // Envia a resposta no inbox
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
bot_log("✅ Fim do ciclo Titanium.");
?>
