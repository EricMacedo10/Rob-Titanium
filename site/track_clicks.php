<?php
/**
 * Titanium Metrics - Click Tracker (PHP Version)
 * For Hostinger Compatibility
 */

header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');
header('Content-Type: application/json');

// Handle preflight
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Get raw POST data (sendBeacon sends text/plain usually)
    $json = file_get_contents('php://input');
    $data = json_decode($json, true);

    if ($data) {
        $file = 'analytics.json';
        $jsFile = 'analytics.js';

        // Load existing
        $logs = [];
        if (file_exists($file)) {
            $logs = json_decode(file_get_contents($file), true) ?: [];
        }

        // Enrich
        $data['log_time'] = date('Y-m-d H:i:s');
        $data['env'] = 'production_staging';

        $logs[] = $data;

        // Keep last 1000
        if (count($logs) > 1000) {
            $logs = array_slice($logs, -1000);
        }

        // Save JSON
        file_put_contents($file, json_encode($logs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE));

        // Save JS (CORS Bypass for offline dashboard viewing)
        file_put_contents($jsFile, "const titanium_analytics_data = " . json_encode($logs, JSON_PRETTY_PRINT | JSON_UNESCAPED_UNICODE) . ";");

        echo json_encode(["status" => "ok"]);
    } else {
        http_response_code(400);
        echo json_encode(["status" => "error", "message" => "Invalid JSON"]);
    }
}
?>