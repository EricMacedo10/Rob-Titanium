<?php
/**
 * Titanium Metrics Elite - Receptor de Metricas
 * Monitoramento Direto de Visitas e Cliques (Anti-Delay Shopee)
 */

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { exit; }

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    if ($data) {
        $file = 'analytics.json';
        $logFile = 'titanium_access.log';

        // Load existing JSON
        $logs = [];
        if (file_exists($file)) {
            $logs = json_decode(file_get_contents($file), true) ?: [];
        }

        // Enrich with Server-side data
        $data['id'] = uniqid();
        $data['server_time'] = date('Y-m-d H:i:s');
        $data['user_ip'] = $_SERVER['REMOTE_ADDR'];
        $data['user_agent'] = $_SERVER['HTTP_USER_AGENT'];

        // Add to JSON list (keeping last 2000 events)
        array_unshift($logs, $data); 
        if (count($logs) > 2000) {
            $logs = array_slice($logs, 0, 2000);
        }

        // Save JSON
        file_put_contents($file, json_encode($logs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        // Save to a "Readable" Text Log (para voce abrir rapido)
        $type = isset($data['type']) ? strtoupper($data['type']) : 'LOG';
        $summary = "[$data[server_time]] $type | IP: $data[user_ip] | ";
        if ($type === 'PAGE_VIEW') {
            $summary .= "Referrer: $data[referrer] | Device: $data[device_type]\n";
        } else {
            $summary .= "Loja: $data[store] | Item: $data[title]\n";
        }
        
        file_put_contents($logFile, $summary, FILE_APPEND);

        echo json_encode(["status" => "success", "monitor" => "active"]);
    } else {
        http_response_code(400);
        echo json_encode(["status" => "error"]);
    }
}
?>