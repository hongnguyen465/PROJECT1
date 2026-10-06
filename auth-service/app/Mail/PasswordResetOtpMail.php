<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class PasswordResetOtpMail extends Mailable
{
    use Queueable, SerializesModels;

    public function __construct(
        public string $otp,
        public ?string $name = null
    ) {}

    public function envelope(): Envelope
    {
        return new Envelope(
            subject: 'Mã OTP đặt lại mật khẩu STRIKER',
        );
    }

    public function content(): Content
    {
        $userName = $this->name ?? 'Quý khách';
        return new Content(
            htmlString: "<h2>Chào {$userName},</h2><p>Mã OTP đặt lại mật khẩu của bạn là: <strong style='color:#ef4444;font-size:24px;'>{$this->otp}</strong></p><p>Mã có hiệu lực trong vòng 10 phút. Vui lòng không chia sẻ mã này cho bất kỳ ai.</p>",
        );
    }
}
