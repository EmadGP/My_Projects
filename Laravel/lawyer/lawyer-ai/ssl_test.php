<?php
$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, "https://repo.packagist.org");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_CAINFO, "C:/xampp/php/extras/ssl/cacert.pem"); // Ensure path is correct
$response = curl_exec($ch);

if ($response === false) {
    echo "cURL Error: " . curl_error($ch);
} else {
    echo "Request successful!";
}
curl_close($ch);
?>
