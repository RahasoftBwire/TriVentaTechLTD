<?php
header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: POST');
header('Access-Control-Allow-Headers: Content-Type');

// Email configuration
$smtp_host = 'smtp.gmail.com';
$smtp_port = 587;
$smtp_username = 'rahasoft.app@gmail.com';
$smtp_password = 'lcxlgwxwpktzmtgw';
$from_email = 'rahasoft.app@gmail.com';
$from_name = 'TriVenta Tech Ltd';
$to_email = 'bilfordderek917@gmail.com';

// Get form data
$data = json_decode(file_get_contents('php://input'), true);

if (!$data) {
    $data = $_POST;
}

$name = isset($data['name']) ? htmlspecialchars(trim($data['name'])) : '';
$email = isset($data['email']) ? htmlspecialchars(trim($data['email'])) : '';
$phone = isset($data['phone']) ? htmlspecialchars(trim($data['phone'])) : '';
$subject = isset($data['subject']) ? htmlspecialchars(trim($data['subject'])) : 'New Contact Form Submission';
$message = isset($data['message']) ? htmlspecialchars(trim($data['message'])) : '';
$formType = isset($data['formType']) ? htmlspecialchars(trim($data['formType'])) : 'contact';

// Validation
if (empty($name) || empty($email) || empty($message)) {
    echo json_encode([
        'success' => false,
        'message' => 'Please fill in all required fields.'
    ]);
    exit;
}

if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
    echo json_encode([
        'success' => false,
        'message' => 'Please enter a valid email address.'
    ]);
    exit;
}

// Prepare email content
$emailSubject = "TriVenta Tech - $subject";
$emailBody = "
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }
        .content { background: #f9f9f9; padding: 30px; border: 1px solid #ddd; }
        .field { margin-bottom: 20px; }
        .field-label { font-weight: bold; color: #667eea; margin-bottom: 5px; }
        .field-value { background: white; padding: 10px; border-left: 3px solid #667eea; }
        .footer { background: #333; color: white; padding: 20px; text-align: center; border-radius: 0 0 10px 10px; font-size: 12px; }
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>TriVenta Tech Ltd</h1>
            <p>Engineering Intelligence, Powering Progress</p>
        </div>
        <div class='content'>
            <h2>New $formType Form Submission</h2>
            
            <div class='field'>
                <div class='field-label'>Name:</div>
                <div class='field-value'>$name</div>
            </div>
            
            <div class='field'>
                <div class='field-label'>Email:</div>
                <div class='field-value'>$email</div>
            </div>
            
            " . (!empty($phone) ? "
            <div class='field'>
                <div class='field-label'>Phone:</div>
                <div class='field-value'>$phone</div>
            </div>
            " : "") . "
            
            <div class='field'>
                <div class='field-label'>Subject:</div>
                <div class='field-value'>$subject</div>
            </div>
            
            <div class='field'>
                <div class='field-label'>Message:</div>
                <div class='field-value'>$message</div>
            </div>
        </div>
        <div class='footer'>
            <p>&copy; " . date('Y') . " TriVenta Tech Ltd. All rights reserved.</p>
            <p>Email: bilfordderek917@gmail.com | Phone: 0722206805</p>
        </div>
    </div>
</body>
</html>
";

// Send email using PHPMailer
require 'PHPMailer/PHPMailer.php';
require 'PHPMailer/SMTP.php';
require 'PHPMailer/Exception.php';

use PHPMailer\PHPMailer\PHPMailer;
use PHPMailer\PHPMailer\Exception;

try {
    $mail = new PHPMailer(true);
    
    // Server settings
    $mail->isSMTP();
    $mail->Host = $smtp_host;
    $mail->SMTPAuth = true;
    $mail->Username = $smtp_username;
    $mail->Password = $smtp_password;
    $mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
    $mail->Port = $smtp_port;
    
    // Recipients
    $mail->setFrom($from_email, $from_name);
    $mail->addAddress($to_email);
    $mail->addReplyTo($email, $name);
    
    // Content
    $mail->isHTML(true);
    $mail->Subject = $emailSubject;
    $mail->Body = $emailBody;
    
    $mail->send();
    
    echo json_encode([
        'success' => true,
        'message' => 'Thank you! Your message has been sent successfully. We will get back to you soon.'
    ]);
    
} catch (Exception $e) {
    echo json_encode([
        'success' => false,
        'message' => 'Sorry, there was an error sending your message. Please try again or contact us directly at bilfordderek917@gmail.com',
        'error' => $mail->ErrorInfo
    ]);
}
?>
