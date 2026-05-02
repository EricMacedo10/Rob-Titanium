<?php
/**
 * Titanium Bridge - Redirecionador Sênior (Item 4)
 * Protege a tag de afiliado contra filtros de redes sociais e garante o Deep Link.
 */

$target_url = isset($_GET['url']) ? $_GET['url'] : '';

if (empty($target_url) || !filter_var($target_url, FILTER_VALIDATE_URL)) {
    header("Location: index.html");
    exit;
}

// --- LOG DE SEGURANÇA (Mesmo formato do track_clicks.php) ---
$log_entry = [
    "id" => uniqid(),
    "type" => "BRIDGE_REDIRECT",
    "target" => $target_url,
    "server_time" => date('Y-m-d H:i:s'),
    "user_ip" => $_SERVER['REMOTE_ADDR'],
    "user_agent" => $_SERVER['HTTP_USER_AGENT'],
    "referrer" => isset($_SERVER['HTTP_REFERER']) ? $_SERVER['HTTP_REFERER'] : 'Direct'
];

$file = 'analytics.json';
$logs = [];
if (file_exists($file)) {
    $logs = json_decode(file_get_contents($file), true) ?: [];
}
array_unshift($logs, $log_entry);
if (count($logs) > 2000) { $logs = array_slice($logs, 0, 2000); }
file_put_contents($file, json_encode($logs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

// --- REDIRECIONAMENTO LIMPO ---
// Usamos 302 (Found) para evitar que o navegador "vicie" no redirecionamento e ignore mudanças futuras
header("Cache-Control: no-store, no-cache, must-revalidate, max-age=0");
header("Cache-Control: post-check=0, pre-check=0", false);
header("Pragma: no-cache");
header("Location: " . $target_url, true, 302);
exit;
?>
