<?php

namespace App\Services;

use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Mail;

class MailService
{
    /**
     * Send email via Resend REST API (HTTPS port 443) with SMTP fallback.
     */
    public static function send(string $to, string $subject, string $htmlContent): bool
    {
        $apiKey = config('services.resend.key') ?: env('RESEND_API_KEY') ?: getenv('RESEND_API_KEY');

        if (!empty($apiKey)) {
            try {
                $response = Http::withHeaders([
                    'Authorization' => 'Bearer ' . $apiKey,
                    'Content-Type' => 'application/json',
                ])->timeout(10)->post('https://api.resend.com/emails', [
                    'from' => 'STRIKER SHOP <onboarding@resend.dev>',
                    'to' => [$to],
                    'subject' => $subject,
                    'html' => $htmlContent,
                ]);

                if ($response->successful()) {
                    Log::info("Email successfully sent via Resend API to {$to}");
                    return true;
                }

                Log::warning("Resend API response error: " . $response->body());
            } catch (\Throwable $e) {
                Log::warning("Resend API exception: " . $e->getMessage());
            }
        }

        // Standard Laravel Mailer (Gmail SMTP)
        try {
            Mail::html($htmlContent, function ($message) use ($to, $subject) {
                $fromAddress = config('mail.from.address') ?: env('MAIL_FROM_ADDRESS') ?: 'nttranq5@gmail.com';
                $fromName = config('mail.from.name') ?: env('MAIL_FROM_NAME') ?: 'STRIKER SPORT';
                $message->to($to)
                        ->from($fromAddress, $fromName)
                        ->subject($subject);
            });
            Log::info("Email successfully sent via SMTP to {$to}");
            return true;
        } catch (\Throwable $e) {
            Log::warning("SMTP Mailer exception: " . $e->getMessage());
            return false;
        }
    }
}
