# HƯỚNG DẪN TRIỂN KHAI DỰ ÁN LÊN DOCKER & CLOUD (RENDER + AIVEN)

Tài liệu này hướng dẫn chi tiết quy trình đóng gói và triển khai toàn bộ hệ thống Microservices STRIKER Cyber-Sport lên nền tảng **Docker** (chạy cục bộ bằng `docker-compose`) và **Cloud (Render.com + Aiven MySQL)** theo đúng tiêu chuẩn kỹ thuật trong tài liệu hướng dẫn.

---

## 1. Cấu trúc Đóng gói Docker của Hệ thống

Dự án sử dụng mô hình Microservices phân tán với các thành phần:
- **`api-gateway`** (Port `8000`): Cổng điều hướng tập trung, xác thực chữ ký và cân bằng tải.
- **`auth-service`** (Port `8001`): Quản lý tài khoản, phân quyền Admin/User, địa chỉ giao hàng.
- **`catalog-service`** (Port `8002`): Danh mục sản phẩm, biến thể (size, color), banner quảng cáo.
- **`order-service`** (Port `8003`): Quản lý giỏ hàng, đặt hàng, mã giảm giá (voucher), tích hợp vận chuyển GHN.
- **`payment-service`** (Port `8004`): Tích hợp cổng thanh toán MoMo ATM / QR và COD.
- **`crs-frontend`** (Port `5173` / `80`): Giao diện Single Page Application (React + Vite + TailwindCSS).

Mỗi dịch vụ Laravel đều được trang bị bộ tệp cấu hình Docker chuẩn hóa:
- **`Dockerfile`**: Kỹ thuật Multi-stage build (`php-base` -> `build` -> `production`) dựa trên nền `php:8.3-fpm-alpine`, tích hợp `Nginx`, `Tini`, `Composer`, các PHP extensions (`pdo_mysql`, `mbstring`, `zip`, `gd`, `bcmath`, `opcache`).
- **`docker/nginx.conf`**: Cấu hình Nginx tối ưu phục vụ FastCGI qua `127.0.0.1:9000`, nạp biến cổng động `${PORT}`, bảo mật ẩn mã nguồn PHP và tệp tin ẩn.
- **`docker/php.ini`**: Tối ưu hóa hiệu năng production (`opcache.enable=1`, `memory_limit=256M`, `display_errors=Off`).
- **`docker/php-fpm.conf`**: Quản lý tiến trình PHP theo nhu cầu (`pm = ondemand`, `pm.max_children = 5`).
- **`docker/entrypoint.sh`**: Script tự động hóa khởi động: giải nén chứng chỉ SSL Aiven, chạy `migrate`, `seed` (nếu bật), tối ưu cache `config/route/view`, và giám sát song song Nginx + PHP-FPM qua signal trap.
- **`docker/check-ca.php`**: Kiểm tra định dạng chứng chỉ CA trước khi kết nối cơ sở dữ liệu.
- **`.dockerignore`**: Loại trừ các tệp tin thừa, tệp môi trường local và logs khỏi image build.

---

## 2. Cách 1: Triển khai Chạy Cục bộ Bằng Docker Compose (Khuyên dùng)

Nếu máy đã cài đặt Docker Desktop, bạn có thể khởi động toàn bộ hệ sinh thái (bao gồm MySQL, 5 Microservices và Frontend) chỉ bằng 1 câu lệnh duy nhất:

### Bước 1: Khởi động hệ thống
Mở terminal (PowerShell / Command Prompt) tại thư mục gốc `PROJECT`:
```powershell
docker compose up --build -d
```

### Bước 2: Kiểm tra trạng thái các Container
```powershell
docker compose ps
```
Khi các container chuyển sang trạng thái `healthy` / `running`, bạn có thể truy cập:
- 🌐 **Giao diện người dùng (Frontend)**: [http://localhost:5173](http://localhost:5173)
- 🚪 **API Gateway**: [http://localhost:8000](http://localhost:8000)
- 🗄️ **MySQL Database**: `localhost:3306` (User: `root`, Password: `Trang2005`)

### Bước 3: Dừng hệ thống
```powershell
docker compose down
```

---

## 3. Cách 2: Triển khai Lên Cloud (Render.com + Aiven.io)

### Bước A: Chuẩn bị cơ sở dữ liệu trên Aiven (https://aiven.io)
1. Đăng nhập vào Aiven, nhấn **Create service** -> chọn **MySQL**.
2. Chọn Cloud Provider gần Việt Nam (ví dụ: `Singapore` / `Asia-Southeast`).
3. Chọn gói dịch vụ (hoặc bản Free trial). Đặt tên service và nhấn **Create service**.
4. Khi dịch vụ sẵn sàng, ghi lại các thông số kết nối:
   - **Host** (ví dụ: `mysql-xxxx.aivencloud.com`)
   - **Port** (ví dụ: `16933`)
   - **User** (ví dụ: `avnadmin`)
   - **Password** (mật khẩu Aiven cấp)
   - **CA certificate**: Nhấn nút **Download** hoặc copy nội dung chứng chỉ CA (lưu lại để dán vào Render Secret Files).

### Bước B: Tạo Web Service trên Render (https://render.com)
1. Đăng nhập Render, liên kết với tài khoản GitHub chứa mã nguồn dự án.
2. Nhấn **New +** -> chọn **Web Service**.
3. Chọn Repository dự án và chỉ định đúng nhánh triển khai (ví dụ: `main` hoặc `feat/auth-service`).
4. Cấu hình chi tiết cho từng dịch vụ:
   - **Language / Environment**: `Docker`
   - **Region**: `Singapore`
   - **Root Directory**: Để trống nếu deploy từ thư mục gốc hoặc trỏ đúng vào thư mục service (ví dụ: `auth-service`, `catalog-service`, ...).
   - **Health Check Path**: `/up`

### Bước C: Khai báo Biến Môi Trường (Environment Variables) trên Render
Mở tab **Environment** của từng service và thiết lập các biến tương ứng (tham khảo tệp `docker/render.env.example` của từng service):

```env
APP_NAME=striker-service
APP_ENV=production
APP_DEBUG=false
APP_URL=https://YOUR-SERVICE.onrender.com
APP_KEY=base64:YOUR_APP_KEY_GENERATED
TRUSTED_PROXIES=*
PORT=10000

DB_CONNECTION=mysql
DB_HOST=YOUR-AIVEN-HOST.aivencloud.com
DB_PORT=YOUR-AIVEN-PORT
DB_DATABASE=defaultdb
DB_USERNAME=avnadmin
DB_PASSWORD=YOUR-AIVEN-PASSWORD
MYSQL_ATTR_SSL_CA=/etc/secrets/ca.pem

SESSION_DRIVER=database
SESSION_SECURE_COOKIE=true
CACHE_STORE=database
QUEUE_CONNECTION=sync
LOG_CHANNEL=stderr
LOG_LEVEL=info

RUN_MIGRATIONS=true
RUN_SEEDERS=false
```

### Bước D: Cấu hình Chứng chỉ CA (Secret Files trên Render)
1. Tại trang quản trị Web Service trên Render, vào mục **Environment** -> cuộn xuống phần **Secret Files**.
2. Nhấn **Add Secret File**:
   - **Filename**: `ca.pem`
   - **Contents**: Dán toàn bộ nội dung file chứng chỉ đã tải từ Aiven (bao gồm cả `-----BEGIN CERTIFICATE-----` và `-----END CERTIFICATE-----`).
3. Nhấn **Save Changes**. Render sẽ tự động mount chứng chỉ vào đường dẫn `/etc/secrets/ca.pem` bên trong container.

### Bước E: Khởi tạo Dữ liệu Mẫu (Seeder)
1. Trong lần deploy đầu tiên, tại mục **Environment Variables** trên Render, bạn có thể tạm thời bật:
   ```env
   RUN_SEEDERS=true
   ```
2. Nhấn **Manual Deploy** -> **Clear build cache & deploy**.
3. Sau khi hệ thống khởi tạo xong dữ liệu danh mục, sản phẩm mẫu và tài khoản quản trị viên, hãy đổi lại `RUN_SEEDERS=false` để tránh chạy lại seeder trong các lần deploy sau.

---

## 4. Kiểm tra và Nghiệm thu Hệ thống

1. **Kiểm tra Healthcheck công khai**:
   ```powershell
   (Invoke-WebRequest -Uri "https://YOUR-SERVICE.onrender.com/up" -UseBasicParsing).StatusCode
   ```
   Kết quả trả về mã `200` chứng tỏ dịch vụ đang vận hành ổn định.
2. **Kiểm tra nghiệp vụ**:
   - Truy cập trang chủ, xem danh mục và chi tiết sản phẩm.
   - Đăng ký tài khoản, đăng nhập, thêm hàng vào giỏ.
   - Thử nghiệm tạo đơn hàng COD và liên kết thanh toán MoMo.
