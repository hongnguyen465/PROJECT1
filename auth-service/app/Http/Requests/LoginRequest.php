<?php

namespace App\Http\Requests;

use Illuminate\Foundation\Http\FormRequest;

class LoginRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    protected function prepareForValidation(): void
    {
        if (!$this->has('login') && ($this->has('email') || $this->has('phone') || $this->has('phone_number'))) {
            $this->merge([
                'login' => $this->input('email') ?? $this->input('phone') ?? $this->input('phone_number'),
            ]);
        }
    }

    public function rules(): array
    {
        return [
            'login' => ['required', 'string'],
            'email' => ['nullable', 'string'],
            'phone' => ['nullable', 'string'],
            'phone_number' => ['nullable', 'string'],
            'password' => ['required', 'string'],
        ];
    }

    public function messages(): array
    {
        return [
            'login.required' => 'Vui lòng nhập email hoặc số điện thoại.',
            'password.required' => 'Vui lòng nhập mật khẩu.',
        ];
    }
}
