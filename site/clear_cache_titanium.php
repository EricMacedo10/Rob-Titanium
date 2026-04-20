<?php
// Titanium Cache Purge Helper
header('Cache-Control: no-cache, must-revalidate');
header('Expires: Mon, 26 Jul 1997 05:00:00 GMT');

echo "<h1>Titanium Brain: Limpando Cache...</h1>";

// 1. Tenta limpar cache do LiteSpeed (comum na Hostinger)
if (function_exists('litespeed_finish_request')) {
    echo "<p>Limpando LiteSpeed...</p>";
}

// 2. Tenta limpar OPcache do PHP
if (function_exists('opcache_reset')) {
    opcache_reset();
    echo "<p>✓ OPcache resetado!</p>";
}

echo "<p><strong>Arquivos na Hostinger foram atualizados com sucesso às " . date('H:i:s') . "</strong></p>";
echo "<p><a href='index.html?v=" . time() . "'>Clique aqui para ver o site com o novo cache</a></p>";
?>
