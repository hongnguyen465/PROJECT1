import os

PLANTUML_DIAGRAMS = {
    "1_Dang_ky_tai_khoan.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Chọn chức năng Đăng ký tài khoản;
:Nhập thông tin (Họ tên, Email, SĐT, Mật khẩu);
:Nhấn nút "Đăng ký";

|Giao diện|
:Kiểm tra tính hợp lệ của biểu mẫu;
:Gửi yêu cầu đăng ký lên Backend;

|Hệ thống xử lý|
:Tiếp nhận và chuẩn hóa dữ liệu đầu vào;

|Cơ sở dữ liệu|
:Truy vấn kiểm tra trùng lặp Email / SĐT;

|Hệ thống xử lý|
if (Thông tin hợp lệ & Chưa tồn tại?) then (Không / Trùng lặp)
  |Giao diện|
  :Hiển thị thông báo lỗi (Tài khoản đã tồn tại);
  stop
else (Hợp lệ)
  |Hệ thống xử lý|
  :Mã hóa mật khẩu an toàn (Bcrypt Hash);
  |Cơ sở dữ liệu|
  :Lưu thông tin tài khoản mới vào CSDL;
  |Giao diện|
  :Hiển thị thông báo Đăng ký thành công;
  :Chuyển hướng người dùng sang trang Đăng nhập;
  |Khách hàng|
  :Nhận thông báo và hoàn tất đăng ký;
  stop
endif
@enduml
""",

    "1b_Dang_ky_va_Xac_thuc_OTP.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Chọn chức năng Đăng ký tài khoản;
:Nhập thông tin (Họ tên, Email, Mật khẩu);
:Nhấn nút "Đăng ký";

|Giao diện|
:Gửi yêu cầu đăng ký lên hệ thống;

|Hệ thống xử lý|
:Kiểm tra quy chuẩn dữ liệu;

|CSDL & Dịch vụ Mail|
:Kiểm tra trùng lặp Email trong CSDL;

|Hệ thống xử lý|
if (Email đã tồn tại?) then (Đã tồn tại)
  |Giao diện|
  :Hiển thị thông báo Email đã đăng ký;
  stop
else (Chưa tồn tại)
  |Hệ thống xử lý|
  :Tạo mã xác thực OTP (6 chữ số);
  |CSDL & Dịch vụ Mail|
  :Lưu OTP vào Cache và gửi Email cho khách hàng;
  |Giao diện|
  :Hiển thị màn hình nhập mã OTP;
  |Khách hàng|
  :Kiểm tra Email và nhập mã OTP xác thực;
  |Giao diện|
  :Gửi mã OTP lên máy chủ;
  |Hệ thống xử lý|
  :Kiểm tra thời hạn và so khớp mã OTP;
  if (Mã OTP chính xác?) then (Sai OTP / Hết hạn)
    |Giao diện|
    :Thông báo mã OTP không hợp lệ;
    stop
  else (Đúng OTP)
    |CSDL & Dịch vụ Mail|
    :Lưu người dùng mới & kích hoạt tài khoản;
    |Giao diện|
    :Hiển thị thông báo Đăng ký thành công;
    :Chuyển hướng về Trang chủ / Đăng nhập;
    |Khách hàng|
    :Đăng nhập thành công vào hệ thống;
    stop
  endif
endif
@enduml
""",

    "2_Dang_nhap_he_thong.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Người dùng|
start
:Chọn chức năng Đăng nhập;
:Nhập Email / SĐT và Mật khẩu;
:Bấm nút "Đăng nhập";

|Giao diện|
:Gửi thông tin xác thực lên Auth Service;

|Hệ thống xử lý|
:Tiếp nhận và kiểm tra định dạng;

|Cơ sở dữ liệu|
:Truy vấn tài khoản theo Email/SĐT;

|Hệ thống xử lý|
if (Tài khoản tồn tại & đúng mật khẩu?) then (Sai thông tin)
  |Giao diện|
  :Hiển thị thông báo sai tài khoản hoặc mật khẩu;
  stop
else (Chính xác)
  |Cơ sở dữ liệu|
  :Kiểm tra trạng thái tài khoản (Active / Locked);
  |Hệ thống xử lý|
  if (Tài khoản đang hoạt động (Active)?) then (Bị khóa)
    |Giao diện|
    :Thông báo tài khoản của bạn đã bị khóa;
    stop
  else (Active)
    |Hệ thống xử lý|
    :Tạo JWT Token phiên đăng nhập;
    |Giao diện|
    :Lưu JWT Token vào Storage & Cập nhật State;
    :Chuyển hướng về Trang chủ;
    |Người dùng|
    :Đăng nhập thành công vào hệ thống;
    stop
  endif
endif
@enduml
""",

    "3_Quan_ly_khach_hang.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Quản trị viên|
start
:Mở trang Quản lý khách hàng;

|Giao diện Admin|
:Gửi request lấy danh sách khách hàng (kèm Token);

|Hệ thống xử lý|
:Xác thực quyền Admin và phân trang;

|Cơ sở dữ liệu|
:Truy vấn danh sách người dùng từ bảng users;

|Giao diện Admin|
:Hiển thị bảng danh sách khách hàng & trạng thái;

|Quản trị viên|
:Chọn tài khoản khách hàng và bấm Khóa / Mở khóa;

|Giao diện Admin|
:Gửi yêu cầu cập nhật trạng thái tài khoản;

|Hệ thống xử lý|
if (Hợp lệ (không tự khóa tài khoản Admin đang dùng)?) then (Vi phạm)
  |Giao diện Admin|
  :Hiển thị cảnh báo không được phép thao tác;
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Cập nhật cột is_active trong bảng users;
  |Hệ thống xử lý|
  :Hủy phiên làm việc nếu tài khoản bị khóa;
  |Giao diện Admin|
  :Cập nhật trạng thái mới trên giao diện;
  |Quản trị viên|
  :Xem kết quả thay đổi trạng thái thành công;
  stop
endif
@enduml
""",

    "4_Duyet_va_Tim_kiem_san_pham.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Nhập từ khóa tìm kiếm hoặc chọn bộ lọc (danh mục, giá, thương hiệu);

|Giao diện|
:Gửi query parameters lên Catalog Service;

|Hệ thống xử lý|
:Chuẩn hóa từ khóa và xây dựng câu lệnh lọc;

|Cơ sở dữ liệu & Cache|
:Truy vấn bảng products khớp với điều kiện tìm kiếm;

|Hệ thống xử lý|
if (Có sản phẩm thỏa mãn điều kiện?) then (Không có)
  |Giao diện|
  :Hiển thị thông báo "Không tìm thấy sản phẩm phù hợp";
  stop
else (Có kết quả)
  |Hệ thống xử lý|
  :Định dạng dữ liệu, hình ảnh, giá bán và phân trang;
  |Giao diện|
  :Render danh sách sản phẩm dạng lưới (Grid);
  |Khách hàng|
  :Xem kết quả và lựa chọn sản phẩm mong muốn;
  stop
endif
@enduml
""",

    "5_Xem_chi_tiet_va_Ton_kho_SKU.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Nhấn chọn một sản phẩm từ danh sách;

|Giao diện|
:Gửi yêu cầu lấy chi tiết sản phẩm theo Slug / ID;

|Hệ thống xử lý|
:Tiếp nhận và điều phối truy vấn dữ liệu sản phẩm;

|Cơ sở dữ liệu|
:Truy vấn chi tiết Product, Images và danh sách SKUs biến thể;

|Giao diện|
:Hiển thị thông tin mô tả, ảnh và các tùy chọn Màu / Size;

|Khách hàng|
:Chọn biến thể Màu sắc và Kích cỡ cụ thể;

|Giao diện|
:Gửi yêu cầu kiểm tra tồn kho của SKU đã chọn;

|Hệ thống xử lý|
:Tra cứu bảng product_variants theo SKU;

|Cơ sở dữ liệu|
:Lấy số lượng tồn kho (stock_quantity) và giá biến thể;

|Hệ thống xử lý|
if (Số lượng tồn kho > 0?) then (Hết hàng)
  |Giao diện|
  :Hiển thị nhãn "Tạm hết hàng" & Khóa nút Mua hàng;
  stop
else (Còn hàng)
  |Giao diện|
  :Cập nhật giá bán chính xác & Kích hoạt nút "Thêm vào giỏ";
  |Khách hàng|
  :Xem giá chính xác và sẵn sàng bấm Thêm giỏ hàng;
  stop
endif
@enduml
""",

    "6_Quan_tri_Catalog_san_pham.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Quản trị viên|
start
:Mở Quản trị Catalog và chọn Thêm mới / Chỉnh sửa SP;
:Nhập tên, danh mục, giá, mô tả, ảnh và bảng biến thể SKU;
:Bấm nút "Lưu sản phẩm";

|Giao diện Admin|
:Gửi dữ liệu sản phẩm kèm Auth Token lên Backend;

|Hệ thống xử lý|
:Xác thực quyền Admin & Kiểm tra hợp lệ dữ liệu (Form Request);

|Hệ thống xử lý|
if (Dữ liệu hợp lệ và SKU không bị trùng lặp?) then (Lỗi dữ liệu)
  |Giao diện Admin|
  :Hiển thị chi tiết các trường thông tin bị lỗi;
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Lưu bảng products và tạo các bản ghi trong product_variants;
  |Hệ thống xử lý|
  :Xóa Cache danh mục và danh sách sản phẩm cũ;
  |Giao diện Admin|
  :Thông báo "Lưu sản phẩm thành công" & Tải lại danh sách;
  |Quản trị viên|
  :Xem sản phẩm mới xuất hiện trên bảng quản trị;
  stop
endif
@enduml
""",

    "7_Quan_ly_gio_hang.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Chọn số lượng và bấm "Thêm vào giỏ hàng" (hoặc Tăng/Giảm SL/Xóa);

|Giao diện|
:Gửi yêu cầu cập nhật giỏ hàng lên Order Service;

|Hệ thống xử lý|
:Kiểm tra số lượng tồn kho của SKU trong kho;

|Cơ sở dữ liệu|
:Truy vấn tồn kho thực tế trong CSDL;

|Hệ thống xử lý|
if (Số lượng yêu cầu <= Tồn kho khả dụng?) then (Vượt quá tồn kho)
  |Giao diện|
  :Hiển thị cảnh báo "Số lượng trong kho không đủ";
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Lưu / Cập nhật sản phẩm vào bảng cart_items;
  |Hệ thống xử lý|
  :Tính toán lại Tạm tính, Thuế và Tổng tiền giỏ hàng;
  |Giao diện|
  :Cập nhật số lượng trên Cart Drawer & Badge Header;
  |Khách hàng|
  :Xem giỏ hàng đã được cập nhật thành công;
  stop
endif
@enduml
""",

    "8_Checkout_va_Tao_don_hang.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Mở trang Checkout, chọn Địa chỉ giao hàng và nhập Mã giảm giá;

|Giao diện|
:Gửi thông tin Tỉnh/Huyện/Xã và Voucher lên hệ thống;

|Hệ thống xử lý|
:Điều phối tính phí vận chuyển & kiểm tra hạn sử dụng Voucher;

|GHN Logistics & CSDL|
:Gọi API Giao Hàng Nhanh lấy cước phí & kiểm tra bảng coupons;

|Hệ thống xử lý|
:Tổng hợp Tiền hàng + Phí ship GHN - Giảm giá = Tổng thanh toán;

|Giao diện|
:Hiển thị chi tiết bảng giá thanh toán cuối cùng;

|Khách hàng|
:Chọn Phương thức thanh toán và bấm "Xác nhận Đặt hàng";

|Giao diện|
:Gửi yêu cầu tạo đơn hàng chính thức;

|Hệ thống xử lý|
if (Khóa giữ tồn kho SKU thành công?) then (Hết hàng đột xuất)
  |Giao diện|
  :Thông báo sản phẩm trong giỏ vừa hết hàng;
  stop
else (Thành công)
  |GHN Logistics & CSDL|
  :Tạo đơn hàng trong orders, lưu order_items và trừ kho SKU;
  |Giao diện|
  :Điều hướng sang cổng thanh toán hoặc trang xác nhận đơn;
  |Khách hàng|
  :Nhận mã đơn hàng (Order Code) đã khởi tạo;
  stop
endif
@enduml
""",

    "9_Thanh_toan_khi_nhan_hang_COD.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Chọn phương thức "Thanh toán khi nhận hàng (COD)";
:Bấm nút "Xác nhận Đặt hàng";

|Giao diện|
:Gửi yêu cầu thanh toán COD lên Payment & Order Service;

|Hệ thống xử lý|
:Khởi tạo giao dịch COD với payment_status = 'pending';

|Cơ sở dữ liệu & Mail|
:Cập nhật trạng thái đơn hàng (order_status = 'pending');
:Xóa sạch các mặt hàng đã mua khỏi Giỏ hàng;
:Gửi Email xác nhận đơn hàng tới hộp thư khách hàng;

|Giao diện|
:Hiển thị màn hình "Đặt hàng thành công!";
:Hiển thị mã tra cứu đơn hàng và nút tiếp tục mua sắm;

|Khách hàng|
:Xem thông tin đơn hàng và nhận Email xác nhận;
stop
@enduml
""",

    "10_Thanh_toan_MoMo_Sandbox.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Chọn thanh toán MoMo QR / ATM & Bấm "Đặt hàng";

|Giao diện|
:Gửi yêu cầu tạo phiên thanh toán MoMo;

|Hệ thống xử lý|
:Tạo chữ ký số bảo mật HMAC-SHA256 từ secretKey;

|Cổng MoMo & CSDL|
:Gọi API MoMo Sandbox tạo yêu cầu thanh toán AIO;
:MoMo trả về payUrl và qrCodeUrl;

|Giao diện|
:Điều hướng khách hàng sang Cổng thanh toán MoMo;

|Khách hàng|
:Quét mã QR MoMo hoặc xác nhận thanh toán trên App;

|Cổng MoMo & CSDL|
:MoMo gửi Webhook IPN thông báo kết quả giao dịch;

|Hệ thống xử lý|
:Kiểm tra chữ ký số IPN từ MoMo;

|Hệ thống xử lý|
if (Chữ ký hợp lệ & Giao dịch thành công (resultCode = 0)?) then (Thất bại)
  |Cơ sở dữ liệu|
  :Cập nhật payment_status = 'failed';
  |Giao diện|
  :Hiển thị thông báo "Thanh toán MoMo thất bại / Đã hủy";
  stop
else (Thành công)
  |Cơ sở dữ liệu|
  :Cập nhật payment_status = 'paid' và order_status = 'paid';
  |Giao diện|
  :Điều hướng về /payment/callback và hiển thị Đặt hàng thành công;
  |Khách hàng|
  :Nhận hóa đơn điện tử thanh toán thành công;
  stop
endif
@enduml
""",

    "11_Theo_doi_va_Huy_don_hang.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Mở trang Lịch sử đơn hàng cá nhân;
:Chọn đơn hàng muốn hủy và bấm "Yêu cầu Hủy đơn";

|Giao diện|
:Gửi yêu cầu hủy đơn hàng lên Order Service;

|Hệ thống xử lý|
:Kiểm tra trạng thái hiện tại của đơn hàng;

|Cơ sở dữ liệu|
:Truy vấn bảng orders để lấy order_status;

|Hệ thống xử lý|
if (Trạng thái đơn hàng đang là 'pending' (Chưa gửi ship)?) then (Đang giao / Đã hoàn tất)
  |Giao diện|
  :Thông báo đơn hàng đã được bàn giao, không thể tự hủy;
  stop
else (Cho phép hủy)
  |Cơ sở dữ liệu|
  :Cập nhật order_status = 'cancelled';
  :Hoàn lại số lượng tồn kho cho các SKU trong đơn;
  |Giao diện|
  :Thông báo "Hủy đơn hàng thành công" & Cập nhật Badge;
  |Khách hàng|
  :Nhìn thấy trạng thái đơn chuyển sang Đã hủy;
  stop
endif
@enduml
""",

    "12_Danh_gia_san_pham.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Mở đơn hàng đã giao thành công và bấm "Đánh giá sản phẩm";
:Chọn số sao (1-5 sao) và viết nhận xét trải nghiệm;
:Bấm nút "Gửi đánh giá";

|Giao diện|
:Gửi nội dung đánh giá kèm Auth Token lên Backend;

|Hệ thống xử lý|
:Kiểm tra điều kiện khách hàng đã thực sự mua và nhận sản phẩm;

|Cơ sở dữ liệu|
:Kiểm tra order_status = 'delivered' trong bảng orders;

|Hệ thống xử lý|
if (Đủ điều kiện đánh giá?) then (Không hợp lệ)
  |Giao diện|
  :Báo lỗi bạn chưa đủ điều kiện đánh giá sản phẩm này;
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Lưu bản ghi vào bảng reviews;
  |Hệ thống xử lý|
  :Tính toán lại điểm đánh giá trung bình (rating) của sản phẩm;
  |Giao diện|
  :Hiển thị thông báo Cảm ơn đánh giá & Render bình luận mới;
  |Khách hàng|
  :Nhìn thấy đánh giá và số sao của mình trên trang sản phẩm;
  stop
endif
@enduml
""",

    "13_Quan_tri_Don_hang_va_GHN_1Click.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Quản trị viên|
start
:Mở trang Quản lý đơn hàng Admin;
:Chọn đơn hàng ở trạng thái Đã thanh toán / Chờ xử lý;
:Bấm nút "1-Click Tạo vận đơn GHN";

|Giao diện Admin|
:Gửi yêu cầu tạo vận đơn giao hàng lên Backend;

|Hệ thống xử lý|
:Đóng gói dữ liệu người nhận, trọng lượng và kích thước bưu kiện;

|GHN Logistics & CSDL|
:Gọi API Giao Hàng Nhanh (v2/shipping-order/create);
:GHN xác nhận và cấp Mã vận đơn (tracking_code);
:Lưu mã vận đơn vào đơn hàng và cập nhật order_status = 'shipping';

|Giao diện Admin|
:Hiển thị mã vận đơn GHN và cập nhật trạng thái "Đang giao hàng";

|Quản trị viên|
:In phiếu gửi hàng GHN và chuẩn bị bàn giao bưu tá;
stop
@enduml
""",

    "14_Tu_van_truc_tuyen_LiveChat.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Khách hàng|
start
:Mở widget Chat góc màn hình và nhập tin nhắn hỏi tư vấn;
:Bấm nút Gửi tin nhắn;

|Giao diện Client|
:Phát sự kiện gửi tin nhắn qua WebSocket / REST API;

|Hệ thống Chat & CSDL|
:Tiếp nhận nội dung và lưu tin nhắn vào bảng messages;
:Đẩy thông báo Real-time đến phiên làm việc của Quản trị viên;

|Giao diện Admin|
:Hiển thị badge tin nhắn mới và mở khung chat với khách;

|Quản trị viên / CSKH|
:Đọc câu hỏi và nhập nội dung trả lời tư vấn cho khách;
:Bấm Gửi phản hồi;

|Hệ thống Chat & CSDL|
:Lưu tin nhắn phản hồi của Admin vào CSDL;
:Phát sóng tin nhắn tức thì tới màn hình của khách hàng;

|Giao diện Client|
:Render tin nhắn phản hồi ngay lập tức trong khung Chat;

|Khách hàng|
:Đọc câu trả lời tư vấn từ CSKH và tiếp tục mua hàng;
stop
@enduml
""",

    "15_Bao_cao_Doanh_thu_va_Hoan_tien.puml": """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam activity {
  BackgroundColor #E1F5FE
  BorderColor #0288D1
  FontColor #000000
}
skinparam diamond {
  BackgroundColor #FFF9C4
  BorderColor #FBC02D
  FontColor #000000
}
skinparam swimlane {
  BorderColor #78909C
  TitleBackgroundColor #ECEFF1
  TitleFontColor #263238
}

|Quản trị viên|
start
:Mở Dashboard Quản trị Báo cáo Tài chính & Doanh thu;

|Giao diện Admin|
:Gửi yêu cầu lấy thống kê tài chính lên Payment Service;

|Hệ thống xử lý|
:Tính toán KPI Doanh thu theo nguyên tắc Tài chính:
Chỉ tính các đơn hàng có trạng thái 'delivered' hoặc 'paid';

|Cơ sở dữ liệu|
:Truy vấn tổng doanh thu, số đơn, top sản phẩm bán chạy;

|Giao diện Admin|
:Vẽ Biểu đồ Doanh thu (Neon Spline) và hiển thị thẻ KPI;

|Quản trị viên|
:Xem danh sách yêu cầu hoàn tiền (Refund Pending) và bấm "Duyệt hoàn tiền";

|Giao diện Admin|
:Gửi lệnh phê duyệt hoàn tiền lên hệ thống;

|Hệ thống xử lý|
:Xác thực giao dịch và lập phiếu hoàn tiền;

|Cơ sở dữ liệu|
:Cập nhật trạng thái giao dịch sang 'refunded';
:Cập nhật trạng thái đơn hàng sang 'refunded';

|Giao diện Admin|
:Cập nhật lại số liệu Doanh thu thực tế và báo thành công;

|Quản trị viên|
:Nhìn thấy báo cáo tài chính đã được cân bằng chính xác;
stop
@enduml
"""
}

output_dir = "docs/plantuml"
os.makedirs(output_dir, exist_ok=True)

for filename, content in PLANTUML_DIAGRAMS.items():
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"Generated: {filepath}")

print("All PlantUML files generated successfully!")
