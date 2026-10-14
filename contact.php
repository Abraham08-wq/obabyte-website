<?php
// contact.php — drop-in backend for shared/cPanel hosting (uses PHP mail()).
// The form posts here when you host on cPanel instead of running app.py.
// To use this instead of Flask: in index.html change
//   fetch('/api/contact', ...)  ->  fetch('contact.php', ...)
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['error' => 'Method not allowed']); exit;
}

$raw  = file_get_contents('php://input');
$data = json_decode($raw, true);
if (!is_array($data)) $data = $_POST;

$name    = trim($data['name']    ?? '');
$email   = trim($data['email']   ?? '');
$message = trim($data['message'] ?? '');

if ($name === '' || $email === '' || $message === '') {
    http_response_code(400);
    echo json_encode(['error' => 'Please fill in all three fields.']); exit;
}
if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['error' => "That email address doesn't look right."]); exit;
}

$to      = 'obajeabrham24@gmail.com';
$subject = "New enquiry from {$name} — Oba-Byte website";
$body    = "Name: {$name}\nEmail: {$email}\n\nMessage:\n{$message}\n";
$headers = "From: website@" . ($_SERVER['HTTP_HOST'] ?? 'oba-byte.com') . "\r\n";
$headers .= "Reply-To: {$email}\r\n";

if (@mail($to, $subject, $body, $headers)) {
    echo json_encode(['ok' => true]);
} else {
    http_response_code(502);
    echo json_encode(['error' => 'Could not send right now. Please email us directly.']);
}
