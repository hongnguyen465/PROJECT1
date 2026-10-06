<!DOCTYPE html>
<html lang="vi" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Striker Auth Service • Lab 10 Cloud Deployment</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    fontFamily: {
                        sans: ['"Plus Jakarta Sans"', 'sans-serif'],
                    },
                    colors: {
                        brand: {
                            50: '#f0fdf4',
                            500: '#22c55e',
                            600: '#16a34a',
                            700: '#15803d',
                        }
                    }
                }
            }
        }
    </script>
    <style>
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #0b0f19;
            color: #f3f4f6;
        }
        .glass-card {
            background: rgba(17, 24, 39, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }
        .glow-green {
            box-shadow: 0 0 25px -5px rgba(34, 197, 94, 0.3);
        }
        .glow-blue {
            box-shadow: 0 0 25px -5px rgba(59, 130, 246, 0.3);
        }
    </style>
</head>
<body class="min-h-screen flex flex-col justify-between antialiased selection:bg-brand-500 selection:text-black">

    <!-- Top Navigation -->
    <header class="border-b border-gray-800/80 bg-gray-950/60 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-green-500 to-emerald-400 flex items-center justify-center font-extrabold text-black text-xl shadow-lg shadow-green-500/20">
                    ⚽
                </div>
                <div>
                    <h1 class="text-base font-bold text-white tracking-wide flex items-center gap-2">
                        STRIKER SHOP <span class="text-xs bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 px-2 py-0.5 rounded-full font-semibold">Lab 10 Live</span>
                    </h1>
                    <p class="text-xs text-gray-400">Microservices • Auth & Identity Service</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-3">
                <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-emerald-950/80 text-emerald-400 border border-emerald-800">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    Render Docker: Live
                </span>
                <a href="https://github.com/hongnguyen465/PROJECT-main" target="_blank" class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-medium bg-gray-800 hover:bg-gray-700 text-gray-200 transition border border-gray-700">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
                    GitHub Repo
                </a>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full">

        <!-- Hero Status Banner -->
        <div class="glass-card rounded-2xl p-6 sm:p-8 mb-8 relative overflow-hidden glow-green">
            <div class="absolute -right-16 -bottom-16 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
            
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
                <div>
                    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 mb-3">
                        <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Lab 10: Project Deployment Thành Công
                    </div>
                    <h2 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                        Hệ Thống Đã Triển Khai Lên Cloud Internet
                    </h2>
                    <p class="text-gray-400 mt-1 max-w-2xl text-sm sm:text-base">
                        Ứng dụng Laravel 12 được đóng gói tự động bằng Docker container trên <span class="text-white font-medium">Render</span> và kết nối cơ sở dữ liệu MySQL bảo mật SSL CA trên <span class="text-white font-medium">Aiven Cloud</span>.
                    </p>
                </div>
                
                <div class="flex flex-wrap items-center gap-3">
                    <a href="/up" target="_blank" class="px-4 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-black font-bold text-sm shadow-lg shadow-emerald-500/20 transition flex items-center gap-2">
                        <span>⚡</span> Health Check (/up)
                    </a>
                    <a href="/api/users" target="_blank" class="px-4 py-2.5 rounded-xl bg-gray-800 hover:bg-gray-700 text-white font-semibold text-sm border border-gray-700 transition flex items-center gap-2">
                        <span>👥</span> JSON Users API
                    </a>
                </div>
            </div>

            <!-- Metric Cards -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mt-8 pt-6 border-t border-gray-800">
                <div class="p-3 bg-gray-900/60 rounded-xl border border-gray-800/80">
                    <span class="text-xs text-gray-400 uppercase tracking-wider block">Cơ sở dữ liệu Aiven</span>
                    <span class="text-base font-bold text-emerald-400 flex items-center gap-1.5 mt-0.5">
                        <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                        {{ $dbConnected ? 'Đã kết nối SSL' : 'Mất kết nối' }}
                    </span>
                    <span class="text-xs text-gray-400 block mt-0.5 font-mono truncate">{{ $dbName ?: 'defaultdb' }}</span>
                </div>

                <div class="p-3 bg-gray-900/60 rounded-xl border border-gray-800/80">
                    <span class="text-xs text-gray-400 uppercase tracking-wider block">Tài khoản User (Aiven)</span>
                    <span class="text-lg font-bold text-white block mt-0.5">{{ $userCount }} Users</span>
                    <span class="text-xs text-emerald-400 block mt-0.5">Đã seed tự động</span>
                </div>

                <div class="p-3 bg-gray-900/60 rounded-xl border border-gray-800/80">
                    <span class="text-xs text-gray-400 uppercase tracking-wider block">PHP Runtime</span>
                    <span class="text-lg font-bold text-white block mt-0.5">PHP {{ PHP_VERSION }}</span>
                    <span class="text-xs text-gray-400 block mt-0.5">FPM + Alpine Linux</span>
                </div>

                <div class="p-3 bg-gray-900/60 rounded-xl border border-gray-800/80">
                    <span class="text-xs text-gray-400 uppercase tracking-wider block">Web Server</span>
                    <span class="text-lg font-bold text-white block mt-0.5">Nginx Reverse Proxy</span>
                    <span class="text-xs text-gray-400 block mt-0.5">Port 10000 • HTTPS</span>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            
            <!-- Left Column: Database Users List -->
            <div class="lg:col-span-2 space-y-6">
                <div class="glass-card rounded-2xl p-6">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="text-lg font-bold text-white flex items-center gap-2">
                                <span>📋</span> Dữ liệu Người Dùng trên Aiven MySQL
                            </h3>
                            <p class="text-xs text-gray-400">Dữ liệu được truy vấn trực tiếp từ bảng <code class="text-emerald-400">users</code></p>
                        </div>
                        <span class="text-xs font-semibold px-2.5 py-1 bg-gray-800 text-gray-300 rounded-lg border border-gray-700">
                            {{ $users->count() }} tài khoản mẫu
                        </span>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm text-gray-300">
                            <thead class="text-xs uppercase bg-gray-900/80 text-gray-400 border-b border-gray-800">
                                <tr>
                                    <th class="px-4 py-3 rounded-l-lg">ID</th>
                                    <th class="px-4 py-3">Họ và tên</th>
                                    <th class="px-4 py-3">Email</th>
                                    <th class="px-4 py-3">Vai trò</th>
                                    <th class="px-4 py-3 rounded-r-lg">Trạng thái</th>
                                </tr>
                            </thead>
                            <tbody class="divide-y divide-gray-800/60">
                                @forelse($users as $user)
                                <tr class="hover:bg-gray-800/40 transition">
                                    <td class="px-4 py-3 font-mono text-xs text-gray-400">#{{ $user->id }}</td>
                                    <td class="px-4 py-3 font-medium text-white">{{ $user->name }}</td>
                                    <td class="px-4 py-3 text-gray-300 font-mono text-xs">{{ $user->email }}</td>
                                    <td class="px-4 py-3">
                                        @if($user->role === 'admin')
                                            <span class="px-2 py-0.5 rounded-md text-xs font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">Admin</span>
                                        @else
                                            <span class="px-2 py-0.5 rounded-md text-xs font-medium bg-blue-500/10 text-blue-400 border border-blue-500/30">Customer</span>
                                        @endif
                                    </td>
                                    <td class="px-4 py-3">
                                        <span class="inline-flex items-center gap-1 text-xs text-emerald-400">
                                            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span> Đã kích hoạt
                                        </span>
                                    </td>
                                </tr>
                                @empty
                                <tr>
                                    <td colspan="5" class="px-4 py-6 text-center text-gray-400">Chưa có dữ liệu người dùng.</td>
                                </tr>
                                @endforelse
                            </tbody>
                        </table>
                    </div>
                </div>

                <!-- API Endpoints Card -->
                <div class="glass-card rounded-2xl p-6">
                    <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        <span>🔌</span> Danh sách REST API Endpoints Sẵn Sàng
                    </h3>
                    <div class="space-y-2.5 font-mono text-xs">
                        <div class="p-3 bg-gray-900/80 rounded-xl border border-gray-800 flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-bold">GET</span>
                                <span class="text-gray-200">/up</span>
                            </div>
                            <span class="text-gray-400 font-sans text-xs">Health check container</span>
                        </div>

                        <div class="p-3 bg-gray-900/80 rounded-xl border border-gray-800 flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-0.5 rounded bg-blue-500/20 text-blue-400 font-bold">GET</span>
                                <span class="text-gray-200">/api/users</span>
                            </div>
                            <span class="text-gray-400 font-sans text-xs">Danh sách tài khoản người dùng</span>
                        </div>

                        <div class="p-3 bg-gray-900/80 rounded-xl border border-gray-800 flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-0.5 rounded bg-green-500/20 text-green-400 font-bold">POST</span>
                                <span class="text-gray-200">/api/auth/login</span>
                            </div>
                            <span class="text-gray-400 font-sans text-xs">Đăng nhập JWT Token</span>
                        </div>

                        <div class="p-3 bg-gray-900/80 rounded-xl border border-gray-800 flex items-center justify-between">
                            <div class="flex items-center gap-2">
                                <span class="px-2 py-0.5 rounded bg-green-500/20 text-green-400 font-bold">POST</span>
                                <span class="text-gray-200">/api/auth/register</span>
                            </div>
                            <span class="text-gray-400 font-sans text-xs">Đăng ký tài khoản khách hàng</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Architecture & Deployment Info -->
            <div class="space-y-6">
                <!-- Info Card -->
                <div class="glass-card rounded-2xl p-6">
                    <h3 class="text-lg font-bold text-white mb-4 flex items-center gap-2">
                        <span>⚙️</span> Thông Tin Kiến Trúc Triển Khai
                    </h3>
                    <ul class="space-y-3 text-xs sm:text-sm text-gray-300">
                        <li class="flex items-start gap-2.5">
                            <span class="text-emerald-400 text-base">✓</span>
                            <div>
                                <strong class="text-white block">Docker Multi-Stage Build</strong>
                                <span class="text-gray-400 text-xs">Đóng gói PHP-FPM 8.3 + Nginx Alpine tối ưu hóa dung lượng image.</span>
                            </div>
                        </li>
                        <li class="flex items-start gap-2.5">
                            <span class="text-emerald-400 text-base">✓</span>
                            <div>
                                <strong class="text-white block">Aiven MySQL SSL Encryption</strong>
                                <span class="text-gray-400 text-xs">Nạp chứng chỉ CA (`ca.pem`) từ Render Secret Files để bảo vệ dữ liệu.</span>
                            </div>
                        </li>
                        <li class="flex items-start gap-2.5">
                            <span class="text-emerald-400 text-base">✓</span>
                            <div>
                                <strong class="text-white block">Auto Migration & Seeder</strong>
                                <span class="text-gray-400 text-xs">Entrypoint tự động chạy migration và khởi tạo tài khoản quản trị khi khởi động.</span>
                            </div>
                        </li>
                    </ul>
                </div>

                <!-- Admin Credentials Card -->
                <div class="glass-card rounded-2xl p-6 border-emerald-500/30">
                    <h3 class="text-base font-bold text-white mb-3 flex items-center gap-2">
                        <span>🔑</span> Tài Khoản Quản Trị Khởi Tạo
                    </h3>
                    <div class="bg-gray-950/80 p-3.5 rounded-xl border border-gray-800 space-y-2 text-xs font-mono">
                        <div>
                            <span class="text-gray-500 block">Email Admin:</span>
                            <span class="text-emerald-400 font-bold select-all">admin@striker.vn</span>
                        </div>
                        <div>
                            <span class="text-gray-500 block">Mật khẩu mặc định:</span>
                            <span class="text-gray-300 select-all">password</span>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-800/80 bg-gray-950/80 py-6 mt-12">
        <div class="max-w-7xl mx-auto px-4 text-center text-xs text-gray-500">
            © 2026 STRIKER E-COMMERCE • MÔ HÌNH KIẾN TRÚC MICROSERVICES • LAB 10 CLOUD DEPLOYMENT
        </div>
    </footer>

</body>
</html>
