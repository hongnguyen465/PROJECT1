<?php
$caPath = getenv('MYSQL_ATTR_SSL_CA');
if (!empty($caPath)) {
    if (!file_exists($caPath) || !is_readable($caPath)) {
        fwrite(STDERR, "CA Certificate at {$caPath} cannot be read.\n");
        exit(1);
    }
    $content = file_get_contents($caPath);
    if (!str_contains($content, 'BEGIN CERTIFICATE')) {
        fwrite(STDERR, "CA Certificate at {$caPath} is not a valid PEM certificate.\n");
        exit(1);
    }
}
exit(0);
