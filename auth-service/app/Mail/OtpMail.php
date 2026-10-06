<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class OtpMail extends Mailable
{
    use Queueable, SerializesModels;

    public function __construct(
        public string $otp
    ) {}

    public function envelope(): Envelope
    {
        return new Envelope(
            subject: 'Mã xác thực OTP tài khoản STRIKER',
        );
    }

    public function content(): Content
    {
        return new Content(
            htmlString: "<h2>Mã xác thực OTP của bạn là: <strong style='color:#10b981;font-size:24px;'>{$this->otp}</strong></h2><p>Mã có hiệu lực trong vòng 10 phút. Vui lòng không chia sẻ mã này cho bất kỳ ai.</p>",
        );
    }
}
