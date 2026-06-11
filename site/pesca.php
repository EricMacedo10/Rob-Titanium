<?php
/**
 * Titanium Bridge v2.0 - Deep Link Proxy Anti-Instagram
 * Detecta o In-App Browser do Instagram e força a abertura no App nativo da Shopee.
 * Garante que o cookie/crédito de afiliado seja preservado.
 */

$target_url = isset($_GET['url']) ? $_GET['url'] : '';

if (empty($target_url) || !filter_var($target_url, FILTER_VALIDATE_URL)) {
    header("Location: index.html");
    exit;
}

// Validação de segurança: apenas URLs da Shopee são permitidas
$allowed_hosts = ['shopee.com.br', 's.shopee.com.br', 'shope.ee'];
$parsed_url = parse_url($target_url);
$target_host = isset($parsed_url['host']) ? strtolower($parsed_url['host']) : '';

$is_allowed = false;
foreach ($allowed_hosts as $host) {
    if (str_ends_with($target_host, $host)) {
        $is_allowed = true;
        break;
    }
}

if (!$is_allowed) {
    header("Location: index.html");
    exit;
}

// --- LOG DE ANALYTICS ---
$log_entry = [
    "id"          => uniqid(),
    "type"        => "BRIDGE_REDIRECT",
    "target"      => $target_url,
    "server_time" => date('Y-m-d H:i:s'),
    "user_ip"     => $_SERVER['REMOTE_ADDR'],
    "user_agent"  => $_SERVER['HTTP_USER_AGENT'],
    "referrer"    => isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'Direct'
];

$file = 'analytics.json';
$logs = [];
if (file_exists($file)) {
    $logs = json_decode(file_get_contents($file), true) ?: [];
}
array_unshift($logs, $log_entry);
if (count($logs) > 2000) { $logs = array_slice($logs, 0, 2000); }
file_put_contents($file, json_encode($logs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES));

// Detecta se é o In-App Browser do Instagram (via User-Agent)
$user_agent = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : '';
$is_instagram = (strpos($user_agent, 'Instagram') !== false);

// Escaping seguro para uso no HTML/JS
$safe_url = htmlspecialchars($target_url, ENT_QUOTES, 'UTF-8');
$json_url  = json_encode($target_url);

?><!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Abrindo oferta... | Guia do Desconto</title>
    <meta name="robots" content="noindex, nofollow">
    <meta property="og:title" content="🎣 Oferta Especial - Pesca Titanium">
    <meta property="og:description" content="Acesse o link seguro para abrir no aplicativo oficial da Shopee e garantir o seu desconto!">
    <meta property="og:image" content="https://guiadodesconto.com.br/images/logo-shopee.png">
    <meta property="og:image:width" content="600">
    <meta property="og:image:height" content="600">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #ee4d2d 0%, #ff7849 100%);
            min-height: 100vh; display: flex; align-items: center;
            justify-content: center; padding: 20px;
        }
        .card {
            background: #fff; border-radius: 20px; padding: 40px 30px;
            text-align: center; max-width: 380px; width: 100%;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        }
        .logo { font-size: 48px; margin-bottom: 16px; }
        h1 { font-size: 22px; color: #1a1a1a; margin-bottom: 8px; }
        p  { color: #666; font-size: 15px; line-height: 1.5; margin-bottom: 24px; }
        .btn-primary {
            display: block; background: #ee4d2d; color: #fff;
            padding: 16px 24px; border-radius: 12px; text-decoration: none;
            font-size: 16px; font-weight: 700; margin-bottom: 12px;
            transition: transform .15s, box-shadow .15s;
        }
        .btn-primary:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(238,77,45,.35); }
        .btn-secondary {
            display: block; color: #ee4d2d; padding: 12px;
            font-size: 14px; text-decoration: none;
        }
        .tip {
            background: #fff8f0; border: 1px solid #ffd0a0; border-radius: 10px;
            padding: 12px 14px; font-size: 13px; color: #b45309; margin-top: 16px;
            display: none;
        }
        .tip.show { display: block; }
        .spinner {
            width: 36px; height: 36px; border: 4px solid #fde8e3;
            border-top-color: #ee4d2d; border-radius: 50%;
            animation: spin .8s linear infinite; margin: 0 auto 20px;
        }
        @keyframes spin { to { transform: rotate(360deg); } }
    </style>
</head>
<body>
<div class="card">
    <div class="logo">&#x1F6CD;</div>
    <div class="spinner" id="spinner"></div>
    <h1 id="title">Abrindo sua oferta...</h1>
    <p id="desc">Redirecionando para a Shopee. Aguarde um instante.</p>

    <a href="<?= $safe_url ?>" id="btn-open" class="btn-primary" style="display:none;">
        Abrir Oferta na Shopee
    </a>

    <a href="<?= $safe_url ?>" class="btn-secondary" id="btn-browser" style="display:none;">
        Abrir no navegador
    </a>

    <div class="tip" id="tip-instagram">
        <strong>Dica:</strong> Para garantir o desconto, abra este link no seu navegador (Chrome ou Safari). Toque nos 3 pontos acima e selecione "Abrir no navegador".
    </div>
</div>

<script>
(function() {
    var targetUrl = <?= $json_url ?>;
    var isInstagram = <?= $is_instagram ? 'true' : 'false' ?>;
    var ua = navigator.userAgent;
    var isAndroid = /Android/i.test(ua);
    var isiOS = /iPhone|iPad|iPod/i.test(ua);

    function showFallback() {
        document.getElementById('spinner').style.display = 'none';
        document.getElementById('title').textContent = 'Toque para abrir a oferta';
        document.getElementById('desc').textContent = 'Clique no botao abaixo para ver o produto com desconto.';
        document.getElementById('btn-open').style.display = 'block';
        if (isInstagram) {
            document.getElementById('tip-instagram').classList.add('show');
            document.getElementById('btn-browser').style.display = 'block';
        }
    }

    if (isInstagram && isAndroid) {
        // Estrategia Android: usa intent:// para escapar do in-app browser e abrir app Shopee
        // O scheme shopee:// força a abertura do app nativo
        var shopeeDeepLink = targetUrl.replace(/^https?:\/\//, 'shopee://');
        
        // Tenta abrir o app via deep link
        window.location.href = shopeeDeepLink;

        // Se o usuario ainda esta aqui apos 1.5s, o app nao abriu -> mostra botao fallback
        setTimeout(function() {
            window.location.href = targetUrl; // fallback para URL normal
            setTimeout(showFallback, 1000);
        }, 1500);

    } else if (isInstagram && isiOS) {
        // iOS: Universal Links da Shopee normalmente abrem o app
        window.location.href = targetUrl;
        // Se nao abrir em 1s, mostra fallback
        setTimeout(showFallback, 1000);

    } else {
        // Navegador normal: redirect direto e silencioso
        window.location.replace(targetUrl);
        // Fallback visual caso o redirect demore
        setTimeout(showFallback, 2000);
    }
})();
</script>
</body>
</html>
