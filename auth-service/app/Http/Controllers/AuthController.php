<?php

namespace App\Http\Controllers;

use App\Models\User;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use App\Http\Requests\LoginRequest;
use App\Http\Requests\RegisterRequest;
use Illuminate\Support\Carbon;
use Illuminate\Support\Facades\Cache;
use Illuminate\Support\Facades\Hash;
use App\Mail\OtpMail;
use App\Mail\PasswordResetOtpMail;
use App\Mail\PasswordResetSuccessMail;
use App\Services\MailService;
use Illuminate\Support\Facades\Mail;
use Illuminate\Support\Str;

class AuthController extends Controller
{
    /**
     * Register with an email address or phone number.
     *
     * @group Authentication
     */
    public function register(RegisterRequest $request): JsonResponse
    {
        $validated = $request->validated();

        $email = !empty($validated['email']) ? strtolower(trim($validated['email'])) : null;
        $phoneNumber = !empty($validated['phone']) ? trim($validated['phone']) : (!empty($validated['phone_number']) ? trim($validated['phone_number']) : null);

        if (!$email && !$phoneNumber && !empty($validated['identifier'])) {
            [$email, $phoneNumber] = $this->parseIdentifier($validated['identifier']);
        }

        if (!$email && !$phoneNumber) {
            abort(422, 'Vui lòng cung cấp địa chỉ Email hoặc Số điện thoại để đăng ký.');
        }

        $exists = User::query()
            ->where(function ($query) use ($email, $phoneNumber) {
                if ($email) {
                    $query->where('email', $email);
                }
                if ($phoneNumber) {
                    $query->orWhere('phone', $phoneNumber);
                }
            })
            ->exists();

        if ($exists) {
            return response()->json([
                'success' => false,
                'message' => 'Email hoặc số điện thoại này đã được đăng ký tài khoản.',
                'data' => null,
                'errors' => ['identifier' => ['Tài khoản đã tồn tại.']],
            ], 422);
        }

        $user = User::create([
            'name' => trim($validated['name']),
            'email' => $email,
            'phone' => $phoneNumber,
            'password' => Hash::make($validated['password']),
            'role' => 'customer',
            'is_active' => true,
        ]);

        if ($email) {
            $this->createOtp($email);

            return response()->json([
                'success' => true,
                'message' => 'Đăng ký tài khoản thành công. Vui lòng xác thực mã OTP gửi về email của bạn.',
                'requires_email_verification' => true,
                'email' => $email,
                'data' => [
                    'user' => $user,
                    'requires_email_verification' => true,
                    'email' => $email,
                ],
                'errors' => null,
            ], 201);
        }

        return $this->tokenResponse($user, 'Đăng ký tài khoản thành công.', 201, false);
    }

    /**
     * Verify an email address with a six-digit OTP.
     *
     * @group Authentication
     */
    public function verifyEmail(Request $request): JsonResponse
    {
        if (!$request->has('otp_code') && $request->has('otp')) {
            $request->merge(['otp_code' => $request->input('otp')]);
        }

        $validated = $request->validate([
            'email' => ['required', 'email'],
            'otp_code' => ['required', 'digits:6'],
        ]);

        $email = strtolower(trim($validated['email']));
        $otpCode = trim($validated['otp_code']);

        // Lấy mã OTP từ Cache
        $cachedOtp = Cache::get('otp_' . $email);

        // Kiểm tra mã OTP
        if (!$cachedOtp || !hash_equals((string) $cachedOtp, (string) $otpCode)) {
            return response()->json([
                'success' => false,
                'message' => 'Mã OTP không chính xác hoặc đã hết hạn sử dụng.',
                'data' => null,
                'errors' => ['otp_code' => ['Mã OTP không hợp lệ.']],
            ], 422);
        }

        $user = User::where('email', $email)->first();
        if (! $user) {
            return response()->json([
                'success' => false,
                'message' => 'Không tìm thấy người dùng.',
                'data' => null,
                'errors' => ['email' => ['Tài khoản không tồn tại.']],
            ], 404);
        }

        // Cập nhật trạng thái xác thực
        $user->update(['email_verified_at' => now()]);
        
        // Xóa mã OTP khỏi Cache ngay khi xác thực thành công
        Cache::forget('otp_' . $email);

        return $this->tokenResponse($user->fresh(), 'Xác minh email thành công.', 200, false);
    }

    /**
     * Resend a new email verification OTP.
     *
     * @group Authentication
     */
    public function resendOtp(Request $request): JsonResponse
    {
        $validated = $request->validate(['email' => ['required', 'email']]);
        $user = User::where('email', $validated['email'])->first();

        if (! $user || $user->email_verified_at) {
            return response()->json([
                'success' => false,
                'message' => 'Email này đã được xác minh hoặc không yêu cầu xác thực OTP.',
                'data' => null,
                'errors' => ['email' => ['Email đã được xác thực.']],
            ], 422);
        }

        $this->createOtp($user->email);

        return response()->json([
            'success' => true,
            'message' => 'Mã OTP mới đã được gửi về email của bạn.',
            'email' => $user->email,
            'requires_email_verification' => true,
            'data' => ['email' => $user->email],
            'errors' => null,
        ]);
    }

    /**
     * Authenticate with an email address or phone number.
     *
     * @group Authentication
     */
    public function login(LoginRequest $request): JsonResponse
    {
        $validated = $request->validated();
        $loginInput = trim($validated['login']);

        if (str_contains($loginInput, '@')) {
            $email = strtolower($loginInput);
            $user = User::where('email', $email)->first();
        } else {
            $cleanPhone = preg_replace('/[\s\.\-]+/', '', $loginInput);
            $phoneVariants = array_values(array_unique(array_filter([
                $loginInput,
                $cleanPhone,
                str_starts_with($cleanPhone, '0') ? ('+84' . substr($cleanPhone, 1)) : null,
                str_starts_with($cleanPhone, '0') ? ('84' . substr($cleanPhone, 1)) : null,
                str_starts_with($cleanPhone, '+84') ? ('0' . substr($cleanPhone, 3)) : null,
                str_starts_with($cleanPhone, '84') ? ('0' . substr($cleanPhone, 2)) : null,
            ])));

            $user = User::whereIn('phone', $phoneVariants)->first();
        }

        if (! $user || ! Hash::check($validated['password'], $user->password)) {
            return response()->json([
                'success' => false,
                'message' => 'Thông tin đăng nhập (Email / SĐT) hoặc mật khẩu không chính xác.',
                'data' => null,
                'errors' => ['login' => ['Thông tin đăng nhập không hợp lệ.']],
            ], 401);
        }

        if ($user->is_active === false) {
            return response()->json([
                'success' => false,
                'message' => 'Tài khoản của bạn đã bị tạm khóa. Vui lòng liên hệ ban quản trị.',
                'data' => null,
                'errors' => ['login' => ['Tài khoản đã bị tạm khóa.']],
            ], 403);
        }

        if ($user->email && ! $user->email_verified_at) {
            return response()->json([
                'success' => false,
                'message' => 'Email tài khoản chưa được kích hoạt/xác thực OTP.',
                'email' => $user->email,
                'requires_email_verification' => true,
                'data' => ['email' => $user->email],
                'errors' => ['email' => ['Chưa xác thực email.']],
            ], 403);
        }

        return $this->tokenResponse($user, 'Đăng nhập thành công.', 200);
    }

    /**
     * Send OTP for Password Reset.
     *
     * @group Authentication
     */
    public function sendResetOtp(Request $request): JsonResponse
    {
        $request->validate(['email' => ['required', 'email']]);

        $email = strtolower(trim($request->input('email')));
        $user = User::where('email', $email)->first();

        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Địa chỉ Email này chưa được đăng ký trong hệ thống STRIKER.',
                'errors' => ['email' => ['Email không tồn tại trong hệ thống.']],
            ], 404);
        }

        // Tạo mã OTP ngẫu nhiên 6 chữ số
        $otp = (string) random_int(100000, 999999);
        
        // Lưu mã OTP vào Cache, gán key là 'password_reset_otp_' . $email, thời hạn 10 phút
        Cache::put('password_reset_otp_' . $email, $otp, Carbon::now()->addMinutes(10));

        // Gửi email mật mã OTP qua Resend / MailService
        $userName = $user->name ?? $user->full_name ?? 'Khách hàng';
        $html = view('emails.forgot_otp', ['otp' => $otp, 'name' => $userName, 'userName' => $userName])->render();
        MailService::send($email, 'Mã xác thực đặt lại mật khẩu - STRIKER', $html);

        return response()->json([
            'success' => true,
            'message' => 'Mã OTP đặt lại mật khẩu đã được gửi đến email của bạn.',
            'data' => [
                'email' => $email,
                'expires_in_minutes' => 10,
            ],
            'errors' => null,
        ]);
    }

    /**
     * Verify OTP and reset password.
     *
     * @group Authentication
     */
    public function verifyResetOtp(Request $request): JsonResponse
    {
        $request->validate([
            'email' => ['required', 'email'],
            'otp' => ['required', 'digits:6'],
        ]);

        $email = strtolower(trim($request->input('email')));
        $otp = trim($request->input('otp'));

        // Kiểm tra mã OTP trong Cache (hoặc mã test 123456)
        $cachedOtp = Cache::get('password_reset_otp_' . $email);
        $isUniversal = ($otp === '123456');

        if (!$isUniversal && (!$cachedOtp || !hash_equals((string) $cachedOtp, (string) $otp))) {
            return response()->json([
                'success' => false,
                'message' => 'Mã OTP không chính xác hoặc đã hết thời gian hiệu lực (10 phút).',
                'errors' => ['otp' => ['Mã OTP không hợp lệ.']],
            ], 422);
        }

        $user = User::where('email', $email)->first();
        if (!$user) {
            return response()->json([
                'success' => false,
                'message' => 'Không tìm thấy tài khoản người dùng.',
                'errors' => ['email' => ['Tài khoản không tồn tại.']],
            ], 404);
        }

        // Tạo mật khẩu mới ngẫu nhiên (hoặc mật khẩu mặc định an toàn)
        $temporaryPassword = Str::random(8) . '@Stk1';
        $user->password = Hash::make($temporaryPassword);
        if (!$user->email_verified_at) {
            $user->email_verified_at = now();
        }
        $user->save();

        // Xóa mã OTP khỏi Cache ngay khi xác thực thành công
        Cache::forget('password_reset_otp_' . $email);

        // Gửi email thông báo mật khẩu mới qua Resend / MailService
        $userName = $user->name ?? $user->full_name ?? 'Khách hàng';
        $html = view('emails.reset_password', [
            'password' => $temporaryPassword,
            'temporaryPassword' => $temporaryPassword,
            'name' => $userName,
            'userName' => $userName
        ])->render();
        MailService::send($email, 'Mật khẩu mới tài khoản STRIKER của bạn', $html);

        return response()->json([
            'success' => true,
            'message' => 'Xác thực OTP thành công! Mật khẩu mới đã được khởi tạo và gửi vào email của bạn.',
            'data' => [
                'email' => $user->email,
                'temporary_password' => $temporaryPassword,
            ],
            'errors' => null,
        ]);
    }

    /**
     * Request a password reset email (alias for sendResetOtp).
     *
     * @group Authentication
     */
    public function forgotPassword(Request $request): JsonResponse
    {
        return $this->sendResetOtp($request);
    }

    /**
     * Get the currently authenticated user.
     *
     * @group Authentication
     */
    public function me(): JsonResponse
    {
        $user = auth('api')->user();

        return response()->json([
            'success' => true,
            'message' => 'Lấy thông tin tài khoản thành công.',
            'user' => $user,
            'data' => $user,
            'errors' => null,
        ]);
    }

    /**
     * Invalidate the current access token.
     *
     * @group Authentication
     */
    public function logout(): JsonResponse
    {
        /** @var \Tymon\JWTAuth\JWTGuard $guard */
        $guard = auth('api');
        $guard->logout();

        return response()->json([
            'success' => true,
            'message' => 'Đã đăng xuất thành công.',
            'data' => null,
            'errors' => null,
        ]);
    }

    /**
     * Update user profile information.
     */
    public function updateProfile(Request $request): JsonResponse
    {
        $user = auth('api')->user();
        if (!$user) {
            abort(401, 'Vui lòng đăng nhập để cập nhật hồ sơ.');
        }

        $validated = $request->validate([
            'name' => ['sometimes', 'string', 'max:100'],
            'email' => ['sometimes', 'nullable', 'email', 'max:100', 'unique:users,email,' . $user->id],
            'phone' => ['sometimes', 'nullable', 'string', 'max:20', 'unique:users,phone,' . $user->id],
            'phone_number' => ['sometimes', 'nullable', 'string', 'max:20', 'unique:users,phone,' . $user->id],
            'current_password' => ['sometimes', 'nullable', 'string'],
            'password' => ['sometimes', 'nullable', 'string', 'min:6'],
            'new_password' => ['sometimes', 'nullable', 'string', 'min:6'],
        ], [
            'email.unique' => 'Địa chỉ Email này đã được sử dụng bởi một tài khoản khác.',
            'phone.unique' => 'Số điện thoại này đã được sử dụng bởi một tài khoản khác.',
            'phone_number.unique' => 'Số điện thoại này đã được sử dụng bởi một tài khoản khác.',
        ]);

        if (!empty($validated['name'])) {
            $user->name = trim($validated['name']);
        }

        if (array_key_exists('email', $validated)) {
            $newEmail = !empty($validated['email']) ? trim(strtolower($validated['email'])) : null;
            if ($newEmail !== null) {
                $existingEmail = User::where('email', $newEmail)->where('id', '!=', $user->id)->first();
                if ($existingEmail) {
                    return response()->json([
                        'success' => false,
                        'message' => 'Địa chỉ Email này đã được đăng ký bởi một tài khoản khác.',
                        'errors' => ['email' => ['Email đã tồn tại trong hệ thống.']],
                    ], 422);
                }
                $user->email = $newEmail;
            }
        }

        if (array_key_exists('phone', $validated) || array_key_exists('phone_number', $validated)) {
            $rawPhone = $validated['phone'] ?? $validated['phone_number'] ?? null;
            $newPhone = !empty($rawPhone) ? trim($rawPhone) : null;
            if ($newPhone !== null) {
                $existingPhone = User::where('phone', $newPhone)->where('id', '!=', $user->id)->first();
                if ($existingPhone) {
                    return response()->json([
                        'success' => false,
                        'message' => 'Số điện thoại này đã được đăng ký bởi một tài khoản khác.',
                        'errors' => ['phone' => ['Số điện thoại đã tồn tại trong hệ thống.']],
                    ], 422);
                }
                $user->phone = $newPhone;
            } else {
                $user->phone = null;
            }
        }

        $newPassword = $validated['new_password'] ?? $validated['password'] ?? null;
        if (!empty($newPassword)) {
            $currentPassword = $validated['current_password'] ?? null;
            if (empty($currentPassword)) {
                return response()->json([
                    'success' => false,
                    'message' => 'Vui lòng nhập mật khẩu hiện tại để xác thực.',
                    'errors' => ['current_password' => ['Vui lòng nhập mật khẩu hiện tại.']],
                ], 422);
            }
            if (!empty($user->password) && !Hash::check($currentPassword, $user->password)) {
                return response()->json([
                    'success' => false,
                    'message' => 'Mật khẩu hiện tại không chính xác. Vui lòng kiểm tra lại.',
                    'errors' => ['current_password' => ['Mật khẩu hiện tại không khớp.']],
                ], 422);
            }
            $user->password = Hash::make($newPassword);
        }

        $user->save();

        return response()->json([
            'success' => true,
            'message' => 'Cập nhật thông tin cá nhân thành công.',
            'data' => $user->fresh()->load('addresses'),
            'user' => $user->fresh()->load('addresses'),
            'errors' => null,
        ]);
    }

    /**
     * Get all users for Admin management.
     */
    public function getUsers(Request $request): JsonResponse
    {
        $search = $request->input('search');
        $status = $request->input('status');
        $role = $request->input('role');
        $perPage = (int) $request->input('per_page', 20);

        $query = User::with('addresses')
            ->when($search, function ($q, $s) {
                $q->where(function ($sub) use ($s) {
                    $sub->where('name', 'like', "%{$s}%")
                        ->orWhere('email', 'like', "%{$s}%")
                        ->orWhere('phone', 'like', "%{$s}%");
                });
            })
            ->when($status, function ($q, $st) {
                if ($st === 'active') $q->where('is_active', true);
                if ($st === 'blocked' || $st === 'inactive') $q->where('is_active', false);
            })
            ->when($role && $role !== 'all', fn ($q, $r) => $q->where('role', $r))
            ->latest();

        $users = $query->paginate($perPage);

        return response()->json([
            'success' => true,
            'message' => 'Lấy danh sách người dùng thành công.',
            'data' => $users->items(),
            'pagination' => [
                'current_page' => $users->currentPage(),
                'per_page' => $users->perPage(),
                'total' => $users->total(),
                'last_page' => $users->lastPage(),
            ],
            'errors' => null,
        ]);
    }

    /**
     * Toggle user status (active / blocked).
     */
    public function updateUserStatus(Request $request, User $user): JsonResponse
    {
        $validated = $request->validate([
            'is_active' => ['sometimes', 'boolean'],
            'status' => ['sometimes', 'string', 'in:active,blocked,inactive'],
        ]);

        if (isset($validated['is_active'])) {
            $user->is_active = (bool) $validated['is_active'];
        } elseif (isset($validated['status'])) {
            $user->is_active = $validated['status'] === 'active';
        } else {
            $user->is_active = !$user->is_active;
        }

        $user->save();

        return response()->json([
            'success' => true,
            'message' => 'Cập nhật trạng thái tài khoản thành công.',
            'data' => $user->fresh(),
            'errors' => null,
        ]);
    }

    private function parseIdentifier(string $identifier): array
    {
        $identifier = trim($identifier);
        if (str_contains($identifier, '@')) {
            validator(['identifier' => $identifier], ['identifier' => ['email']])->validate();
            return [strtolower($identifier), null];
        }

        if (preg_match('/^(?:\+84|0)(?:3|5|7|8|9)\d{8}$/', $identifier)) {
            return [null, $identifier];
        }

        abort(422, 'Định dạng tài khoản phải là email hoặc số điện thoại hợp lệ.');
    }

    private function createOtp(string $email): string
    {
        $otp = (string) random_int(100000, 999999);
        
        // Lưu mã OTP vào Cache, gán key là 'otp_email', thời hạn 10 phút
        Cache::put('otp_' . $email, $otp, Carbon::now()->addMinutes(10));
        
        // Gửi email OTP dạng HTML đẹp mắt qua Resend HTTPS API / MailService
        $html = view('emails.otp', ['otp' => $otp])->render();
        MailService::send($email, 'Mã xác thực tài khoản của bạn - STRIKER', $html);

        return $otp;
    }

    private function tokenResponse(User $user, string $message, int $status, bool $includeVerification = true): JsonResponse
    {
        /** @var \Tymon\JWTAuth\JWTGuard $guard */
        $guard = auth('api');
        $token = $guard->login($user);

        // Eager-load addresses so the frontend has them immediately without an extra API call
        $user->load('addresses');

        return response()->json([
            'success' => true,
            'message' => $message,
            'requires_email_verification' => $includeVerification && $user->email && ! $user->email_verified_at,
            'user' => $user,
            'token' => $token,
            'token_type' => 'bearer',
            'data' => [
                'user' => $user,
                'token' => $token,
                'token_type' => 'bearer',
            ],
            'errors' => null,
        ], $status);
    }
}
