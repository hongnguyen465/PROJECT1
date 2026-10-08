<?php

namespace App\Services;

class EmailValidator
{
    /**
     * Validate whether an email is valid, has real MX records, and conforms to provider standards.
     * 
     * @return array [bool $isValid, string|null $errorMessage]
     */
    public static function validate(string $email): array
    {
        $email = strtolower(trim($email));

        // 1. Kiểm tra cú pháp cơ bản
        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            return [false, 'Định dạng địa chỉ Email không hợp lệ.'];
        }

        $parts = explode('@', $email);
        if (count($parts) !== 2) {
            return [false, 'Địa chỉ Email không đúng định dạng.'];
        }

        [$username, $domain] = $parts;

        // 2. Chặn các tên miền email rác / ảo / tạm thời
        $disposableDomains = [
            'mailinator.com', 'tempmail.com', '10minutemail.com', 'guerrillamail.com',
            'yopmail.com', 'trashmail.com', 'sharklasers.com', 'getairmail.com',
            'temp-mail.org', 'dispostable.com', 'fakeinbox.com', 'throwawaymail.com',
            'maildrop.cc', 'inboxkitten.com'
        ];
        if (in_array($domain, $disposableDomains, true)) {
            return [false, 'Hệ thống không chấp nhận email ảo/tạm thời. Vui lòng sử dụng địa chỉ email chính thức của bạn.'];
        }

        // 3. Kiểm tra quy chuẩn riêng của Gmail (Google)
        if ($domain === 'gmail.com' || $domain === 'googlemail.com') {
            $cleanUser = str_replace('.', '', $username);
            if (strlen($cleanUser) < 6 || strlen($cleanUser) > 30) {
                return [false, 'Địa chỉ Gmail này không tồn tại (Google yêu cầu tên tài khoản từ 6 đến 30 ký tự).'];
            }
            if (!preg_match('/^[a-z0-9.]+$/', $username)) {
                return [false, 'Địa chỉ Gmail chứa ký tự không hợp lệ.'];
            }
        }

        // 4. Kiểm tra bản ghi DNS MX / A để xác thực tên miền email có thực sự tồn tại trên Internet không
        if ($domain !== 'striker.vn' && function_exists('checkdnsrr')) {
            $hasMx = @checkdnsrr($domain, 'MX');
            $hasA = @checkdnsrr($domain, 'A');
            if (!$hasMx && !$hasA) {
                return [false, "Tên miền email '@{$domain}' không tồn tại trên Internet. Vui lòng kiểm tra lại!"];
            }
        }

        return [true, null];
    }
}
