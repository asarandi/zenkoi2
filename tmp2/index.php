<?php
$headers = getallheaders();
$data = "--------------------------------------\n";

foreach ($headers as $k => $v) {
    $data .= "$k: $v\n";
}

if (isset($_POST)) {
    $data .= "---[post]------------\n";
    foreach ($_POST as $k => $v) {
        $data .= "$k: $v\n";
    }
}

file_put_contents("http.requests.log", $data, FILE_APPEND);
echo "muchas gracias!\n";
?>
