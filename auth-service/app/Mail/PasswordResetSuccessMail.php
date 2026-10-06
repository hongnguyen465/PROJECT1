<?php

namespace App\Mail;

use Illuminate\Bus\Queueable;
use Illuminate\Mail\Mailable;
use Illuminate\Mail\Mailables\Content;
use Illuminate\Mail\Mailables\Envelope;
use Illuminate\Queue\SerializesModels;

class PasswordResetSuccessMail extends Mailable
{
    use Queueable, SerializesModels;

    public function __construct(
        public string $temporaryPassword,
        public ?string $name = null
    ) {}

    public function envelope(): Envelope
    {
        return new Envelope(
            subject: 'Khởi tạo mật khẩu mới thành công - STRIKER',
        );
    }

    public function content(): Content
    {
        $userName = $this->name ?? 'Quý khách';
        return new Content(
            htmlString: "<h2>Chào {$userName},</h2><p>Mật khẩu tạm thời mới của bạn là: <strong style='color:#3b82f6;font-size:20px;'>{$this->temporaryPassword}</strong></p><p>Vui lòng đăng nhập và đổi lại mật khẩu của bạn trong phần Hồ sơ cá nhân.</p>",
        );
    }
}
