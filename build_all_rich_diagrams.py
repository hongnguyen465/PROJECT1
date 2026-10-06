import os
import xml.etree.ElementTree as ET

# ==============================================================================
# 15 RICH ACTIVITY DIAGRAMS DEFINITIONS
# ==============================================================================
DIAGRAM_DATA = [
    # --------------------------------------------------------------------------
    # 1. ĐĂNG KÝ TÀI KHOẢN
    # --------------------------------------------------------------------------
    {
        "id": 1,
        "title": "1. Đăng ký tài khoản",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Truy cập Trang chủ và bấm "Đăng ký tài khoản";
:Điền đầy đủ thông tin: Họ tên, Email, SĐT, Mật khẩu & Nhập lại MK;
:Tích chọn "Đồng ý với Điều khoản dịch vụ" & Bấm "Tạo tài khoản";

|Giao diện|
:Kiểm tra tính hợp lệ của biểu mẫu (Validate client);
:Gửi yêu cầu đăng ký lên Auth Service;

|Hệ thống xử lý|
:Tiếp nhận và chuẩn hóa dữ liệu người dùng;

|Cơ sở dữ liệu|
:Truy vấn kiểm tra trùng lặp Email hoặc Số điện thoại;

|Hệ thống xử lý|
if (Thông tin hợp lệ & Chưa tồn tại?) then (Trùng lặp / Lỗi)
  |Giao diện|
  :Hiển thị thông báo lỗi (Email hoặc SĐT đã tồn tại);
  |Khách hàng|
  :Xem thông báo lỗi và chỉnh sửa lại thông tin đăng ký;
  stop
else (Hợp lệ)
  |Hệ thống xử lý|
  :Mã hóa mật khẩu bảo mật bằng thuật toán Bcrypt;
  |Cơ sở dữ liệu|
  :Lưu bản ghi người dùng mới vào bảng users;
  |Giao diện|
  :Hiển thị thông báo "Đăng ký tài khoản thành công!";
  :Tự động chuyển hướng sang trang Đăng nhập;
  |Khách hàng|
  :Nhận thông báo và sẵn sàng đăng nhập vào hệ thống;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Truy cập Trang chủ và bấm\nĐăng ký tài khoản"},
            {"lane": 0, "type": "action", "text": "Nhập Họ tên, Email, SĐT,\nMật khẩu & Xác nhận MK"},
            {"lane": 0, "type": "action", "text": "Tích Điều khoản dịch vụ &\nBấm Tạo tài khoản"},
            {"lane": 1, "type": "action", "text": "Kiểm tra hợp lệ biểu mẫu\nvà gửi dữ liệu lên Server"},
            {"lane": 2, "type": "action", "text": "Tiếp nhận & chuẩn hóa\ndữ liệu người dùng"},
            {"lane": 3, "type": "action", "text": "Truy vấn kiểm tra\ntrùng lặp Email / SĐT"},
            {"lane": 2, "type": "decision", "text": "Hợp lệ & Chưa có?"},
            # False branch
            {"lane": 1, "type": "action", "text": "Hiển thị thông báo lỗi\n(Email/SĐT đã tồn tại)", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo lỗi &\nchỉnh sửa lại thông tin", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # True branch
            {"lane": 2, "type": "action", "text": "Mã hóa mật khẩu an toàn\n(Bcrypt Hash)", "branch": "ok"},
            {"lane": 3, "type": "action", "text": "Lưu bản ghi User mới\nvào bảng users (Active)", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Thông báo Đăng ký thành công\nvà chuyển sang Đăng nhập", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Nhận thông báo và\nsẵn sàng đăng nhập", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 2. ĐĂNG NHẬP HỆ THỐNG
    # --------------------------------------------------------------------------
    {
        "id": 2,
        "title": "2. Đăng nhập hệ thống",
        "lanes": ["Người dùng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Người dùng",
        "puml_body": """
|Người dùng|
start
:Mở trang Đăng nhập từ thanh điều hướng Header;
:Nhập Email / Số điện thoại và Mật khẩu;
:Tích chọn "Ghi nhớ đăng nhập" và bấm nút "Đăng nhập";

|Giao diện|
:Gửi thông tin xác thực lên API Gateway / Auth Service;

|Hệ thống xử lý|
:Tiếp nhận và kiểm tra định dạng dữ liệu;

|Cơ sở dữ liệu|
:Truy vấn tài khoản theo Email/SĐT và lấy Hash mật khẩu;

|Hệ thống xử lý|
if (Tài khoản tồn tại & đúng mật khẩu?) then (Sai thông tin)
  |Giao diện|
  :Hiển thị thông báo sai tài khoản hoặc mật khẩu;
  |Người dùng|
  :Xem thông báo lỗi (có thể chọn Quên mật khẩu);
  stop
else (Chính xác)
  |Cơ sở dữ liệu|
  :Kiểm tra trạng thái tài khoản (status = active / locked);
  |Hệ thống xử lý|
  if (Tài khoản đang hoạt động (Active)?) then (Bị khóa)
    |Giao diện|
    :Thông báo tài khoản của bạn đã bị khóa;
    |Người dùng|
    :Xem thông báo và liên hệ CSKH để hỗ trợ;
    stop
  else (Active)
    |Hệ thống xử lý|
    :Tạo JWT Token phiên làm việc & thông tin User;
    |Giao diện|
    :Lưu JWT Token vào Storage & Cập nhật AppContext;
    :Điều hướng về Trang chủ / Trang trước đó;
    |Người dùng|
    :Nhìn thấy thông tin cá nhân trên Header & sẵn sàng mua sắm;
    stop
  endif
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở trang Đăng nhập\ntừ thanh điều hướng Header"},
            {"lane": 0, "type": "action", "text": "Nhập Email / SĐT\nvà Mật khẩu tài khoản"},
            {"lane": 0, "type": "action", "text": "Tích Ghi nhớ đăng nhập\nvà bấm nút Đăng nhập"},
            {"lane": 1, "type": "action", "text": "Gửi thông tin xác thực\nlên Auth Service"},
            {"lane": 2, "type": "action", "text": "Tiếp nhận & kiểm tra\nđịnh dạng dữ liệu"},
            {"lane": 3, "type": "action", "text": "Truy vấn tài khoản &\nso khớp Bcrypt Password"},
            {"lane": 2, "type": "decision", "text": "Đúng mật khẩu?"},
            # False branch
            {"lane": 1, "type": "action", "text": "Thông báo sai thông tin\nđăng nhập", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo lỗi &\nchọn nhập lại hoặc Quên MK", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # True branch
            {"lane": 3, "type": "action", "text": "Kiểm tra trạng thái\n(status = active / locked)", "branch": "ok"},
            {"lane": 2, "type": "decision", "text": "Tài khoản active?", "branch": "ok"},
            # Locked branch
            {"lane": 1, "type": "action", "text": "Thông báo tài khoản\nđã bị khóa / vô hiệu hóa", "branch": "locked"},
            {"lane": 0, "type": "action", "text": "Xem thông báo và\nliên hệ Admin CSKH", "branch": "locked"},
            {"lane": 0, "type": "end", "branch": "locked"},
            # Active branch
            {"lane": 2, "type": "action", "text": "Tạo JWT Token phiên &\nUser Data Payload", "branch": "active"},
            {"lane": 1, "type": "action", "text": "Lưu Token vào Storage\nvà chuyển về Trang chủ", "branch": "active"},
            {"lane": 0, "type": "action", "text": "Đăng nhập thành công &\nxem menu tài khoản cá nhân", "branch": "active"},
            {"lane": 0, "type": "end", "branch": "active"}
        ]
    },

    # --------------------------------------------------------------------------
    # 3. QUẢN LÝ KHÁCH HÀNG (KHÓA / MỞ KHÓA)
    # --------------------------------------------------------------------------
    {
        "id": 3,
        "title": "3. Quản lý khách hàng (Khóa / Mở khóa)",
        "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Quản trị viên",
        "puml_body": """
|Quản trị viên|
start
:Mở trang "Quản lý khách hàng" trên Dashboard Admin;
:Nhập từ khóa tìm kiếm khách hàng (Tên, Email, SĐT);

|Giao diện Admin|
:Gửi request lấy danh sách khách hàng (kèm Token Admin);

|Hệ thống xử lý|
:Xác thực quyền Admin và phân trang kết quả;

|Cơ sở dữ liệu|
:Truy vấn danh sách người dùng từ bảng users;

|Giao diện Admin|
:Hiển thị bảng danh sách khách hàng, tổng chi tiêu & trạng thái;

|Quản trị viên|
:Xem xét tài khoản vi phạm và bấm nút "Khóa" (hoặc "Mở khóa");
:Xác nhận hành động trên hộp thoại xác nhận Modal;

|Giao diện Admin|
:Gửi yêu cầu đổi trạng thái tài khoản lên Backend;

|Hệ thống xử lý|
if (Hợp lệ (không tự khóa tài khoản Admin đang đăng nhập)?) then (Vi phạm)
  |Giao diện Admin|
  :Hiển thị cảnh báo không được phép tự khóa tài khoản Admin;
  |Quản trị viên|
  :Xem cảnh báo và hủy thao tác;
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Cập nhật cột is_active trong bảng users;
  |Hệ thống xử lý|
  :Hủy toàn bộ phiên làm việc (Revoke Token) nếu bị khóa;
  |Giao diện Admin|
  :Cập nhật Badge trạng thái mới (Active/Locked) và báo thành công;
  |Quản trị viên|
  :Nhìn thấy trạng thái tài khoản khách hàng đã thay đổi thành công;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở trang Quản lý khách hàng\ntrên Dashboard Admin"},
            {"lane": 0, "type": "action", "text": "Tìm kiếm khách hàng theo\nTên, Email hoặc Số ĐT"},
            {"lane": 1, "type": "action", "text": "Gửi request lấy danh sách\nkhách hàng (kèm Token)"},
            {"lane": 2, "type": "action", "text": "Xác thực quyền Admin\nvà phân trang dữ liệu"},
            {"lane": 3, "type": "action", "text": "Truy vấn bảng users\nlấy thông tin khách hàng"},
            {"lane": 1, "type": "action", "text": "Hiển thị danh sách khách hàng,\ntổng chi tiêu & trạng thái"},
            {"lane": 0, "type": "action", "text": "Chọn tài khoản vi phạm &\nnhấn nút Khóa / Mở khóa"},
            {"lane": 0, "type": "action", "text": "Xác nhận hành động trên\nhộp thoại xác nhận Modal"},
            {"lane": 1, "type": "action", "text": "Gửi yêu cầu đổi trạng thái\ntài khoản lên Backend"},
            {"lane": 2, "type": "decision", "text": "Thao tác hợp lệ?"},
            # Vi pham
            {"lane": 1, "type": "action", "text": "Cảnh báo không được phép\ntự khóa tài khoản Admin", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem cảnh báo lỗi và\nhủy bỏ thao tác", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Hop le
            {"lane": 3, "type": "action", "text": "Cập nhật status user\ntrong CSDL (is_active)", "branch": "ok"},
            {"lane": 2, "type": "action", "text": "Hủy phiên làm việc nếu\ntài khoản khách bị khóa", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Cập nhật Badge trạng thái mới\nvà thông báo thành công", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Nhìn thấy trạng thái mới\ncủa khách hàng trên bảng", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 4. DUYỆT VÀ TÌM KIẾM SẢN PHẨM
    # --------------------------------------------------------------------------
    {
        "id": 4,
        "title": "4. Duyệt và Tìm kiếm sản phẩm",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu & Cache"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Truy cập trang Cửa hàng (Shop) trên thanh điều hướng;
:Nhập từ khóa tìm kiếm (ví dụ: "Áo Real Madrid", "Giày Nike");
:Chọn bộ lọc: Danh mục, Thương hiệu, Khoảng giá & Sắp xếp giá;

|Giao diện|
:Gửi query parameters (search, category, price, sort) lên Catalog;

|Hệ thống xử lý|
:Chuẩn hóa từ khóa và xây dựng câu lệnh truy vấn lọc;

|Cơ sở dữ liệu & Cache|
:Truy vấn bảng products theo các điều kiện lọc và tìm kiếm;

|Hệ thống xử lý|
if (Tìm thấy sản phẩm phù hợp?) then (Không có SP)
  |Giao diện|
  :Hiển thị thông báo "Không tìm thấy sản phẩm phù hợp";
  :Hiển thị nút "Xóa bộ lọc" và các sản phẩm gợi ý;
  |Khách hàng|
  :Xem thông báo, xóa bộ lọc hoặc thử từ khóa tìm kiếm khác;
  stop
else (Có kết quả)
  |Hệ thống xử lý|
  :Format dữ liệu ảnh, giá bán, giảm giá và phân trang;
  |Giao diện|
  :Render danh sách sản phẩm dạng lưới (Product Grid);
  |Khách hàng|
  :Lướt xem danh sách, xem mức giá và nhấp chọn SP để xem chi tiết;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Truy cập trang Cửa hàng (Shop)\ntrên thanh điều hướng"},
            {"lane": 0, "type": "action", "text": "Nhập từ khóa tìm kiếm\n(Áo đấu, Giày bóng đá...)"},
            {"lane": 0, "type": "action", "text": "Chọn lọc Danh mục, Hãng,\nKhoảng giá & Sắp xếp"},
            {"lane": 1, "type": "action", "text": "Gửi query parameters lên\nCatalog Service"},
            {"lane": 2, "type": "action", "text": "Chuẩn hóa từ khóa và\nxử lý logic bộ lọc"},
            {"lane": 3, "type": "action", "text": "Truy vấn bảng products\ntheo tên, giá, danh mục"},
            {"lane": 2, "type": "decision", "text": "Có kết quả SP?"},
            # Empty
            {"lane": 1, "type": "action", "text": "Hiển thị thông báo không\ntìm thấy SP & gợi ý tìm", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo, bấm Xóa lọc\nhoặc thử từ khóa mới", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Found
            {"lane": 2, "type": "action", "text": "Format dữ liệu ảnh,\ngiá bán & phân trang", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Render danh sách SP\ndưới dạng lưới (Grid)", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Lướt xem kết quả và nhấp\nchọn SP ưng ý xem chi tiết", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 5. XEM CHI TIẾT SẢN PHẨM & TỒN KHO SKU
    # --------------------------------------------------------------------------
    {
        "id": 5,
        "title": "5. Xem chi tiết & Tồn kho SKU",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Nhấn chọn một sản phẩm từ danh mục hoặc trang chủ;

|Giao diện|
:Gửi yêu cầu lấy chi tiết sản phẩm theo Slug / ID;

|Hệ thống xử lý|
:Tiếp nhận và điều phối truy vấn Catalog;

|Cơ sở dữ liệu|
:Truy vấn chi tiết Product, Album ảnh và bảng SKUs biến thể;

|Giao diện|
:Hiển thị hình ảnh, mô tả, bảng chọn size và đánh giá khách hàng;

|Khách hàng|
:Xem ảnh, đọc mô tả và nhấp chọn Màu sắc + Kích thước (SKU);
:Chọn số lượng muốn mua (tăng / giảm số lượng);

|Giao diện|
:Gửi yêu cầu kiểm tra tồn kho của SKU đã chọn;

|Hệ thống xử lý|
:Xác định mã SKU và tra cứu tồn kho khả dụng;

|Cơ sở dữ liệu|
:Lấy giá bán và số lượng tồn kho (stock_quantity);

|Hệ thống xử lý|
if (Số lượng tồn kho > 0?) then (Hết hàng)
  |Giao diện|
  :Hiển thị nhãn "Tạm hết hàng" & Khóa nút "Thêm vào giỏ";
  |Khách hàng|
  :Xem thông báo hết hàng và có thể chọn biến thể khác;
  stop
else (Còn hàng)
  |Giao diện|
  :Cập nhật giá bán chính xác & Mở nút "Thêm vào giỏ hàng";
  |Khách hàng|
  :Bấm nút "Thêm vào giỏ hàng" (hoặc "Mua ngay");
  |Giao diện|
  :Thêm vào giỏ, mở Cart Drawer & Báo thêm giỏ thành công;
  |Khách hàng|
  :Kiểm tra món hàng trong giỏ và sẵn sàng bấm Thanh toán;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Nhấn chọn một sản phẩm\ntừ danh sách hoặc trang chủ"},
            {"lane": 1, "type": "action", "text": "Gửi request lấy chi tiết\nSP theo Slug / ID"},
            {"lane": 2, "type": "action", "text": "Tiếp nhận & điều phối\ntruy vấn Catalog"},
            {"lane": 3, "type": "action", "text": "Truy vấn Product, Album\nảnh và bảng SKUs biến thể"},
            {"lane": 1, "type": "action", "text": "Hiển thị thông tin SP, ảnh,\nmô tả và tùy chọn Màu / Size"},
            {"lane": 0, "type": "action", "text": "Nhấp chọn Màu sắc, Size\nvà chọn số lượng cần mua"},
            {"lane": 1, "type": "action", "text": "Gửi yêu cầu kiểm tra tồn\nkho biến thể SKU đã chọn"},
            {"lane": 2, "type": "action", "text": "Xác định mã SKU &\ntra cứu tồn kho khả dụng"},
            {"lane": 3, "type": "action", "text": "Lấy giá bán & số lượng\ntồn kho (stock_quantity)"},
            {"lane": 2, "type": "decision", "text": "SKU còn hàng?"},
            # Out of stock
            {"lane": 1, "type": "action", "text": "Báo Tạm hết hàng &\nkhóa nút Thêm giỏ", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo hết hàng\nvà chọn biến thể khác", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # In stock
            {"lane": 1, "type": "action", "text": "Cập nhật giá chính xác &\nmở nút Thêm vào giỏ", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Bấm nút Thêm vào giỏ hàng\n(hoặc Mua ngay)", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Mở Cart Drawer và báo\nđã thêm vào giỏ thành công", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Kiểm tra giỏ hàng và\nsẵn sàng bấm Thanh toán", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 6. QUẢN TRỊ CATALOG SẢN PHẨM
    # --------------------------------------------------------------------------
    {
        "id": 6,
        "title": "6. Quản trị Catalog sản phẩm",
        "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Quản trị viên",
        "puml_body": """
|Quản trị viên|
start
:Mở menu "Quản lý sản phẩm" trên Dashboard Admin;
:Nhấn nút "Thêm sản phẩm mới" (hoặc chọn "Sửa" sản phẩm);
:Nhập Tên sản phẩm, Danh mục, Thương hiệu, Mô tả và tải Album ảnh;
:Thiết lập danh sách biến thể SKU (Màu sắc, Size, Giá bán, Tồn kho);
:Bấm nút "Lưu sản phẩm";

|Giao diện Admin|
:Gửi dữ liệu sản phẩm kèm Auth Token lên Catalog Service;

|Hệ thống xử lý|
:Xác thực quyền Admin & Kiểm tra tính hợp lệ của dữ liệu;

|Hệ thống xử lý|
if (Dữ liệu hợp lệ & Mã SKU không bị trùng?) then (Lỗi dữ liệu / Trùng SKU)
  |Giao diện Admin|
  :Hiển thị chi tiết lỗi các trường dữ liệu chưa hợp lệ;
  |Quản trị viên|
  :Xem thông báo lỗi và chỉnh sửa lại thông tin sản phẩm;
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Lưu bảng products và tạo các bản ghi trong product_variants;
  |Hệ thống xử lý|
  :Xóa Cache danh mục và làm mới dữ liệu tìm kiếm;
  |Giao diện Admin|
  :Thông báo "Lưu sản phẩm thành công" & Tải lại danh sách;
  |Quản trị viên|
  :Xem sản phẩm mới xuất hiện trên bảng Admin & ngoài Cửa hàng;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở menu Quản lý sản phẩm\ntrên Dashboard Admin"},
            {"lane": 0, "type": "action", "text": "Bấm Thêm sản phẩm mới\n(hoặc chọn Sửa sản phẩm)"},
            {"lane": 0, "type": "action", "text": "Nhập thông tin, mô tả, ảnh\nvà bảng biến thể SKU"},
            {"lane": 0, "type": "action", "text": "Bấm nút Lưu sản phẩm"},
            {"lane": 1, "type": "action", "text": "Gửi dữ liệu sản phẩm kèm\nAuth Token lên Backend"},
            {"lane": 2, "type": "action", "text": "Xác thực quyền Admin &\nkiểm tra tính hợp lệ dữ liệu"},
            {"lane": 2, "type": "decision", "text": "Dữ liệu hợp lệ?"},
            # Error
            {"lane": 1, "type": "action", "text": "Hiển thị thông báo chi tiết\ncác trường dữ liệu bị lỗi", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo lỗi và\nchỉnh sửa lại form SP", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Success
            {"lane": 3, "type": "action", "text": "Lưu bảng products và\ntạo các product_variants", "branch": "ok"},
            {"lane": 2, "type": "action", "text": "Xóa Cache danh mục và\nlàm mới dữ liệu tìm kiếm", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Báo Lưu thành công và\ntải lại danh sách sản phẩm", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Xem sản phẩm mới trên bảng\nAdmin và ngoài Cửa hàng", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 7. QUẢN LÝ GIỎ HÀNG
    # --------------------------------------------------------------------------
    {
        "id": 7,
        "title": "7. Quản lý giỏ hàng",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Nhấp biểu tượng Giỏ hàng trên Header để mở Cart Drawer / Page;
:Xem danh sách các sản phẩm, biến thể màu sắc, size và đơn giá;
:Thao tác Tăng/Giảm số lượng hoặc bấm Thùng rác để Xóa món hàng;
:Nhập mã Coupon giảm giá vào ô khuyến mãi và bấm "Áp dụng";

|Giao diện|
:Gửi yêu cầu cập nhật giỏ hàng và kiểm tra Voucher lên Order Service;

|Hệ thống xử lý|
:Kiểm tra tồn kho khả dụng của SKU & Điều kiện áp dụng Coupon;

|Cơ sở dữ liệu|
:Truy vấn tồn kho trong CSDL & Kiểm tra hạn dùng bảng coupons;

|Hệ thống xử lý|
if (Số lượng yêu cầu <= Tồn kho & Voucher hợp lệ?) then (Không hợp lệ / Quá tồn kho)
  |Giao diện|
  :Hiển thị cảnh báo số lượng vượt quá tồn kho hoặc Voucher hết hạn;
  |Khách hàng|
  :Xem cảnh báo và điều chỉnh lại số lượng / mã giảm giá;
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Cập nhật bảng cart_items & Lưu trạng thái voucher đã áp dụng;
  |Hệ thống xử lý|
  :Tính toán lại Tạm tính, Tiền giảm giá và Tổng tiền giỏ hàng;
  |Giao diện|
  :Cập nhật lại Badge giỏ hàng, bảng tổng tiền và mở nút Checkout;
  |Khách hàng|
  :Xem tổng tiền thanh toán mới và bấm "Tiến hành Đặt hàng";
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở Giỏ hàng (Cart Drawer)\ntrên thanh điều hướng Header"},
            {"lane": 0, "type": "action", "text": "Xem danh sách món hàng,\nbiến thể Màu/Size và giá"},
            {"lane": 0, "type": "action", "text": "Tăng/Giảm số lượng hoặc\nxóa sản phẩm khỏi giỏ"},
            {"lane": 0, "type": "action", "text": "Nhập mã Voucher giảm giá\nvà bấm Áp dụng"},
            {"lane": 1, "type": "action", "text": "Gửi request cập nhật giỏ\nvà voucher lên Backend"},
            {"lane": 2, "type": "action", "text": "Kiểm tra tồn kho khả dụng\nvà điều kiện áp dụng Voucher"},
            {"lane": 3, "type": "action", "text": "Truy vấn tồn kho SKU &\nbảng coupons trong CSDL"},
            {"lane": 2, "type": "decision", "text": "SL & Voucher hợp lệ?"},
            # Error
            {"lane": 1, "type": "action", "text": "Cảnh báo vượt quá tồn kho\nhoặc mã Voucher không hợp lệ", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem cảnh báo và điều chỉnh\nlại số lượng / mã giảm giá", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Success
            {"lane": 3, "type": "action", "text": "Cập nhật bảng cart_items\nvà áp dụng mã giảm giá", "branch": "ok"},
            {"lane": 2, "type": "action", "text": "Tính lại Tạm tính, Tiền\ngiảm giá và Tổng thanh toán", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Cập nhật Badge giỏ hàng,\nbảng giá & kích hoạt Checkout", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Xem tổng tiền chính xác và\nbấm Tiến hành Đặt hàng", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 8. CHECKOUT VÀ TẠO ĐƠN HÀNG (GHN + VOUCHER)
    # --------------------------------------------------------------------------
    {
        "id": 8,
        "title": "8. Checkout và Tạo đơn hàng (GHN + Voucher)",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "GHN Logistics & CSDL"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Truy cập trang Checkout từ Giỏ hàng;
:Chọn hoặc thêm Địa chỉ nhận hàng (Tỉnh/Thành, Quận/Huyện, Phường/Xã);

|Giao diện|
:Gửi thông tin địa chỉ giao hàng lên API Gateway;

|Hệ thống xử lý|
:Điều phối tính phí ship qua API Giao Hàng Nhanh;

|GHN Logistics & CSDL|
:Gọi API GHN (v2/shipping-order/fee) lấy cước phí giao hàng chuẩn xác;

|Hệ thống xử lý|
:Tổng hợp Tiền hàng + Cước phí GHN - Tiền giảm giá = Tổng thanh toán;

|Giao diện|
:Hiển thị chi tiết bảng tính tiền và các phương thức thanh toán;

|Khách hàng|
:Chọn Phương thức thanh toán (COD hoặc MoMo QR/ATM);
:Nhập ghi chú giao hàng (nếu có) và bấm "Xác nhận Đặt hàng";

|Giao diện|
:Gửi yêu cầu tạo đơn hàng chính thức kèm Auth Token;

|Hệ thống xử lý|
:Khóa giữ tồn kho SKU và xác thực dữ liệu đơn hàng;

|Hệ thống xử lý|
if (Giữ hàng tồn kho SKU thành công?) then (Hết hàng đột xuất)
  |Giao diện|
  :Thông báo có sản phẩm vừa hết hàng trong quá trình thanh toán;
  |Khách hàng|
  :Xem thông báo lỗi và quay lại giỏ hàng cập nhật;
  stop
else (Thành công)
  |GHN Logistics & CSDL|
  :Lưu đơn hàng vào bảng orders, lưu order_items và trừ tồn kho SKU;
  :Xóa các sản phẩm đã đặt mua khỏi bảng cart_items;
  |Giao diện|
  :Điều hướng sang Cổng thanh toán (nếu MoMo) hoặc trang Thành công (nếu COD);
  |Khách hàng|
  :Nhận Mã đơn hàng (Order Code) và hướng dẫn hoàn tất đơn;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Truy cập trang Checkout\ntừ giỏ hàng"},
            {"lane": 0, "type": "action", "text": "Chọn / Nhập địa chỉ nhận\n(Tỉnh, Huyện, Xã GHN)"},
            {"lane": 1, "type": "action", "text": "Gửi địa chỉ nhận hàng\nlên Backend tính phí ship"},
            {"lane": 2, "type": "action", "text": "Điều phối request tính phí\nqua Giao Hàng Nhanh"},
            {"lane": 3, "type": "action", "text": "Gọi API GHN lấy cước phí\ngiao hàng chuẩn xác"},
            {"lane": 2, "type": "action", "text": "Tổng hợp Tiền hàng + Phí GHN\n- Giảm giá = Tổng thanh toán"},
            {"lane": 1, "type": "action", "text": "Hiển thị chi tiết bảng giá &\ncác phương thức thanh toán"},
            {"lane": 0, "type": "action", "text": "Chọn phương thức thanh toán\nvà bấm Xác nhận Đặt hàng"},
            {"lane": 1, "type": "action", "text": "Gửi yêu cầu tạo đơn hàng\nchính thức lên hệ thống"},
            {"lane": 2, "type": "decision", "text": "Khóa tồn kho SKU?"},
            # Out of stock
            {"lane": 1, "type": "action", "text": "Báo sản phẩm trong giỏ vừa\nhết hàng trong lúc thanh toán", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo lỗi và\nquay lại giỏ hàng cập nhật", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Success
            {"lane": 3, "type": "action", "text": "Lưu orders, order_items,\ntrừ kho & xóa cart_items", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Điều hướng cổng thanh toán\nhoặc trang Đặt hàng thành công", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Nhận mã tra cứu đơn hàng &\ntheo dõi tiến độ xử lý", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 9. THANH TOÁN KHI NHẬN HÀNG (COD)
    # --------------------------------------------------------------------------
    {
        "id": 9,
        "title": "9. Thanh toán khi nhận hàng (COD)",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu & Mail"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Chọn phương thức "Thanh toán khi nhận hàng (COD)" tại Checkout;
:Kiểm tra lại thông tin nhận hàng, số điện thoại & Bấm "Đặt hàng COD";

|Giao diện|
:Gửi yêu cầu khởi tạo đơn hàng COD lên Payment & Order Service;

|Hệ thống xử lý|
:Khởi tạo giao dịch COD với payment_status = 'pending';

|Cơ sở dữ liệu & Mail|
:Cập nhật trạng thái đơn hàng (order_status = 'pending');
:Xóa sạch các mặt hàng đã mua khỏi Giỏ hàng;
:Gửi Email xác nhận đơn hàng kèm hóa đơn tới email khách hàng;

|Giao diện|
:Hiển thị màn hình "Đặt hàng thành công!";
:Hiển thị mã tra cứu đơn hàng, tổng tiền cần trả khi nhận và nút mua tiếp;

|Khách hàng|
:Xem thông tin đơn hàng, kiểm tra Email xác nhận & sẵn sàng nhận hàng;
stop
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Chọn phương thức COD tại\ntrang Checkout thanh toán"},
            {"lane": 0, "type": "action", "text": "Kiểm tra lại địa chỉ, SĐT\nvà bấm Đặt hàng COD"},
            {"lane": 1, "type": "action", "text": "Gửi request khởi tạo đơn\nCOD lên Payment & Order Service"},
            {"lane": 2, "type": "action", "text": "Khởi tạo giao dịch COD\nvới payment_status = 'pending'"},
            {"lane": 3, "type": "action", "text": "Cập nhật order_status = 'pending',\nxóa giỏ hàng & gửi Mail xác nhận"},
            {"lane": 1, "type": "action", "text": "Hiển thị màn hình Đặt hàng\nthành công & mã tra cứu đơn"},
            {"lane": 0, "type": "action", "text": "Xem thông tin đơn, kiểm tra\nEmail và sẵn sàng nhận hàng"},
            {"lane": 0, "type": "end"}
        ]
    },

    # --------------------------------------------------------------------------
    # 10. THANH TOÁN MOMO SANDBOX
    # --------------------------------------------------------------------------
    {
        "id": 10,
        "title": "10. Thanh toán MoMo Sandbox",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cổng MoMo & CSDL"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Chọn phương thức "Thanh toán Ví MoMo (QR / ATM)" tại Checkout;
:Bấm nút "Tiến hành Thanh toán MoMo";

|Giao diện|
:Gửi yêu cầu tạo phiên giao dịch MoMo lên Payment Service;

|Hệ thống xử lý|
:Tạo chữ ký số HMAC-SHA256 từ secretKey bảo mật;

|Cổng MoMo & CSDL|
:Gọi API MoMo Sandbox (POST /v2/gateway/api/create);
:MoMo phản hồi mã payUrl và qrCodeUrl thanh toán;

|Giao diện|
:Điều hướng khách hàng sang Cổng thanh toán MoMo;

|Khách hàng|
:Mở ứng dụng MoMo trên điện thoại để Quét mã QR thanh toán;
:Xác nhận số tiền và nhập mã PIN / FaceID trên App MoMo;

|Cổng MoMo & CSDL|
:MoMo gửi Webhook IPN thông báo kết quả giao dịch ngầm;

|Hệ thống xử lý|
:Xác thực chữ ký số IPN từ MoMo để tránh giả mạo;

|Hệ thống xử lý|
if (Chữ ký hợp lệ & Giao dịch thành công (resultCode = 0)?) then (Thất bại / Hủy)
  |Cổng MoMo & CSDL|
  :Cập nhật payment_status = 'failed' trong bảng payments;
  |Giao diện|
  :Hiển thị thông báo "Thanh toán MoMo thất bại hoặc đã bị hủy";
  |Khách hàng|
  :Xem thông báo thất bại và có thể chọn thanh toán lại;
  stop
else (Thành công)
  |Cổng MoMo & CSDL|
  :Cập nhật payment_status = 'paid' và order_status = 'paid';
  |Giao diện|
  :Điều hướng về /payment/callback & Hiển thị "Thanh toán thành công!";
  |Khách hàng|
  :Nhận biên lai thanh toán và theo dõi tiến độ giao hàng;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Chọn thanh toán MoMo QR/ATM\ntại bước Checkout"},
            {"lane": 0, "type": "action", "text": "Bấm nút Tiến hành\nThanh toán MoMo"},
            {"lane": 1, "type": "action", "text": "Gửi yêu cầu tạo giao dịch\nMoMo lên Payment Service"},
            {"lane": 2, "type": "action", "text": "Tạo chữ ký số bảo mật\nHMAC-SHA256 từ secretKey"},
            {"lane": 3, "type": "action", "text": "Gọi API MoMo Sandbox và\nnhận payUrl, qrCodeUrl"},
            {"lane": 1, "type": "action", "text": "Điều hướng khách hàng sang\nCổng thanh toán MoMo"},
            {"lane": 0, "type": "action", "text": "Mở App MoMo quét mã QR\nhoặc xác nhận trên điện thoại"},
            {"lane": 3, "type": "action", "text": "MoMo gửi Webhook IPN\nthông báo kết quả giao dịch"},
            {"lane": 2, "type": "action", "text": "Kiểm tra chữ ký số IPN\nxác thực dữ liệu từ MoMo"},
            {"lane": 2, "type": "decision", "text": "Giao dịch MoMo OK?"},
            # Fail
            {"lane": 3, "type": "action", "text": "Cập nhật payment_status = 'failed'\ntrong bảng payments", "branch": "err"},
            {"lane": 1, "type": "action", "text": "Hiển thị thông báo thanh toán\nMoMo thất bại / Đã hủy", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo thất bại và\nchọn thử lại phương thức khác", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Success
            {"lane": 3, "type": "action", "text": "Cập nhật payment_status = 'paid'\nvà order_status = 'paid'", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Điều hướng về /payment/callback &\nbáo Thanh toán thành công!", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Nhận biên lai điện tử và\ntheo dõi tiến độ giao hàng", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 11. THEO DÕI VÀ HỦY ĐƠN HÀNG
    # --------------------------------------------------------------------------
    {
        "id": 11,
        "title": "11. Theo dõi & Hủy đơn hàng",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Mở menu tài khoản và chọn trang "Đơn hàng của tôi";
:Xem danh sách các đơn hàng và lọc theo trạng thái (Chờ xử lý, Đang giao...);
:Nhấp chọn đơn hàng muốn hủy và bấm nút "Yêu cầu Hủy đơn hàng";
:Chọn lý do hủy đơn trên Modal xác nhận và bấm "Xác nhận hủy";

|Giao diện|
:Gửi yêu cầu hủy đơn hàng lên Order Service;

|Hệ thống xử lý|
:Kiểm tra trạng thái hiện tại của đơn hàng;

|Cơ sở dữ liệu|
:Truy vấn bảng orders để lấy order_status;

|Hệ thống xử lý|
if (Trạng thái đơn hàng đang là 'pending' (Chưa gửi ship)?) then (Đang giao / Hoàn tất)
  |Giao diện|
  :Thông báo đơn hàng đã được gửi giao, không thể tự hủy trực tuyến;
  :Hiển thị hotline CSKH để khách liên hệ hỗ trợ;
  |Khách hàng|
  :Xem thông báo từ chối hủy và liên hệ hỗ trợ nếu cần;
  stop
else (Cho phép hủy)
  |Cơ sở dữ liệu|
  :Cập nhật order_status = 'cancelled' trong bảng orders;
  :Hoàn trả lại số lượng tồn kho cho các SKU trong đơn;
  |Giao diện|
  :Thông báo "Hủy đơn hàng thành công" & Cập nhật Badge trạng thái;
  |Khách hàng|
  :Nhìn thấy trạng thái đơn hàng chuyển sang Đã hủy (Cancelled);
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở trang Đơn hàng của tôi\ntừ menu tài khoản Header"},
            {"lane": 0, "type": "action", "text": "Xem danh sách và nhấp\nchọn đơn hàng muốn hủy"},
            {"lane": 0, "type": "action", "text": "Chọn lý do hủy đơn và bấm\nXác nhận Hủy đơn hàng"},
            {"lane": 1, "type": "action", "text": "Gửi yêu cầu hủy đơn hàng\nlên Order Service"},
            {"lane": 2, "type": "action", "text": "Kiểm tra trạng thái hiện\ntại của đơn hàng"},
            {"lane": 3, "type": "action", "text": "Truy vấn bảng orders để\nlấy giá trị order_status"},
            {"lane": 2, "type": "decision", "text": "Đơn đang là Pending?"},
            # Denied
            {"lane": 1, "type": "action", "text": "Thông báo đơn đã bàn giao GHN,\nkhông thể tự hủy trực tuyến", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo từ chối và\nliên hệ CSKH nếu cần", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Allowed
            {"lane": 3, "type": "action", "text": "Cập nhật order_status = 'cancelled'\nvà hoàn tồn kho các SKU", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Báo Hủy đơn thành công &\ncập nhật trạng thái giao diện", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Nhìn thấy trạng thái đơn\nchuyển sang Đã hủy", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 12. ĐÁNH GIÁ SẢN PHẨM
    # --------------------------------------------------------------------------
    {
        "id": 12,
        "title": "12. Đánh giá sản phẩm (Review/Rating)",
        "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Mở đơn hàng đã giao thành công và bấm "Viết đánh giá sản phẩm";
:Chọn số sao trải nghiệm (từ 1 đến 5 sao);
:Nhập nội dung nhận xét chi tiết về sản phẩm và chất lượng dịch vụ;
:Bấm nút "Gửi đánh giá";

|Giao diện|
:Kiểm tra form đánh giá & Gửi dữ liệu kèm Token lên Backend;

|Hệ thống xử lý|
:Kiểm tra điều kiện khách hàng đã thực sự mua và nhận đơn hàng;

|Cơ sở dữ liệu|
:Kiểm tra điều kiện order_status = 'delivered' trong bảng orders;

|Hệ thống xử lý|
if (Đủ điều kiện đánh giá sản phẩm?) then (Chưa mua / Chưa nhận)
  |Giao diện|
  :Báo lỗi bạn chỉ có thể đánh giá sản phẩm khi đã nhận hàng thành công;
  |Khách hàng|
  :Xem thông báo từ chối và quay lại sau khi nhận hàng;
  stop
else (Hợp lệ)
  |Cơ sở dữ liệu|
  :Lưu bản ghi vào bảng reviews (rating, comment, user_id, product_id);
  |Hệ thống xử lý|
  :Tính toán lại điểm đánh giá trung bình (rating avg) của sản phẩm;
  |Giao diện|
  :Hiển thị thông báo "Cảm ơn bạn đã đánh giá!" & Render bình luận mới;
  |Khách hàng|
  :Nhìn thấy đánh giá và số sao của mình hiển thị trên trang sản phẩm;
  stop
endif
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở đơn hàng đã nhận và\nbấm Viết đánh giá sản phẩm"},
            {"lane": 0, "type": "action", "text": "Chọn số sao (1-5 sao) và\nnhập nội dung nhận xét"},
            {"lane": 0, "type": "action", "text": "Bấm nút Gửi đánh giá"},
            {"lane": 1, "type": "action", "text": "Gửi nội dung đánh giá kèm\nAuth Token lên Backend"},
            {"lane": 2, "type": "action", "text": "Kiểm tra điều kiện khách\nđã mua và nhận sản phẩm"},
            {"lane": 3, "type": "action", "text": "Kiểm tra order_status = 'delivered'\ntrong bảng orders"},
            {"lane": 2, "type": "decision", "text": "Đủ điều kiện?"},
            # Error
            {"lane": 1, "type": "action", "text": "Báo lỗi bạn chỉ có thể đánh\ngiá khi đã nhận hàng thành công", "branch": "err"},
            {"lane": 0, "type": "action", "text": "Xem thông báo từ chối và\nquay lại sau khi nhận hàng", "branch": "err"},
            {"lane": 0, "type": "end", "branch": "err"},
            # Success
            {"lane": 3, "type": "action", "text": "Lưu bản ghi mới vào bảng\nreviews trong CSDL", "branch": "ok"},
            {"lane": 2, "type": "action", "text": "Tính lại điểm đánh giá\ntrung bình của sản phẩm", "branch": "ok"},
            {"lane": 1, "type": "action", "text": "Báo Cảm ơn đánh giá &\nrender bình luận mới", "branch": "ok"},
            {"lane": 0, "type": "action", "text": "Nhìn thấy nhận xét và số\nsao của mình trên trang SP", "branch": "ok"},
            {"lane": 0, "type": "end", "branch": "ok"}
        ]
    },

    # --------------------------------------------------------------------------
    # 13. QUẢN TRỊ ĐƠN HÀNG & GHN 1-CLICK
    # --------------------------------------------------------------------------
    {
        "id": 13,
        "title": "13. Quản trị Đơn hàng & GHN 1-Click",
        "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "GHN Logistics & CSDL"],
        "actor_title": "Quản trị viên",
        "puml_body": """
|Quản trị viên|
start
:Mở trang "Quản lý đơn hàng" trên Dashboard Admin;
:Lọc danh sách các đơn hàng ở trạng thái "Đã thanh toán / Chờ xử lý";
:Xem chi tiết kiện hàng: Người nhận, Địa chỉ, Sản phẩm, Tiền thu hộ;
:Bấm nút "1-Click Tạo vận đơn GHN";

|Giao diện Admin|
:Gửi yêu cầu tạo vận đơn giao hàng lên Order Service;

|Hệ thống xử lý|
:Đóng gói dữ liệu bưu kiện: Kích thước, trọng lượng, địa chỉ & tiền COD;

|GHN Logistics & CSDL|
:Gọi API Giao Hàng Nhanh (POST /v2/shipping-order/create);
:GHN tiếp nhận thành công và cấp Mã vận đơn (tracking_code);
:Lưu mã vận đơn vào đơn hàng và cập nhật order_status = 'shipping';

|Giao diện Admin|
:Hiển thị mã vận đơn GHN, cập nhật trạng thái "Đang giao hàng" & nút In phiếu;

|Quản trị viên|
:Bấm nút "In phiếu gửi hàng GHN", dán tem và bàn giao bưu tá;
stop
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở trang Quản lý đơn hàng\ntrên Dashboard Admin"},
            {"lane": 0, "type": "action", "text": "Lọc đơn hàng Đã thanh toán /\nChờ xử lý giao hàng"},
            {"lane": 0, "type": "action", "text": "Kiểm tra chi tiết kiện hàng &\nbấm 1-Click Tạo đơn GHN"},
            {"lane": 1, "type": "action", "text": "Gửi yêu cầu tạo vận đơn\ngiao hàng lên Backend"},
            {"lane": 2, "type": "action", "text": "Đóng gói dữ liệu người nhận,\ntrọng lượng và tiền COD"},
            {"lane": 3, "type": "action", "text": "Gọi API GHN tạo đơn và\nnhận Mã vận đơn tracking_code"},
            {"lane": 3, "type": "action", "text": "Lưu mã tracking vào đơn &\ncập nhật status = 'shipping'"},
            {"lane": 1, "type": "action", "text": "Hiển thị mã vận đơn GHN &\ncập nhật Đang giao hàng"},
            {"lane": 0, "type": "action", "text": "In phiếu gửi hàng GHN, dán\ntem và bàn giao bưu tá"},
            {"lane": 0, "type": "end"}
        ]
    },

    # --------------------------------------------------------------------------
    # 14. TƯ VẤN TRỰC TUYẾN LIVECHAT CSKH
    # --------------------------------------------------------------------------
    {
        "id": 14,
        "title": "14. Tư vấn trực tuyến LiveChat CSKH",
        "lanes": ["Khách hàng", "Giao diện Client", "Hệ thống Chat & CSDL", "Giao diện Admin", "Quản trị viên / CSKH"],
        "actor_title": "Khách hàng",
        "puml_body": """
|Khách hàng|
start
:Nhấp vào biểu tượng Chat nổi ở góc phải màn hình để mở LiveChat;
:Nhập nội dung câu hỏi cần tư vấn (chọn size, hỏi tồn kho, tư vấn áo đấu);
:Bấm nút "Gửi tin nhắn";

|Giao diện Client|
:Phát sự kiện gửi tin nhắn qua WebSocket / REST API;

|Hệ thống Chat & CSDL|
:Lưu tin nhắn của khách vào bảng messages (is_read = false);
:Đẩy thông báo Real-time đến phiên làm việc của Quản trị viên;

|Giao diện Admin|
:Hiển thị badge tin nhắn mới và mở khung chat với khách hàng;

|Quản trị viên / CSKH|
:Đọc câu hỏi của khách và nhập nội dung trả lời giải đáp thắc mắc;
:Bấm nút "Gửi phản hồi";

|Hệ thống Chat & CSDL|
:Lưu tin nhắn phản hồi của Admin vào CSDL;
:Phát sóng tin nhắn tức thì tới phiên duyệt của khách hàng;

|Giao diện Client|
:Render tin nhắn phản hồi ngay lập tức trong khung LiveChat;

|Khách hàng|
:Đọc câu trả lời tư vấn từ CSKH, cảm ơn và tiếp tục đặt mua sản phẩm;
stop
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở khung LiveChat ở góc\nmàn hình Cửa hàng"},
            {"lane": 0, "type": "action", "text": "Nhập nội dung câu hỏi tư vấn\nvà bấm Gửi tin nhắn"},
            {"lane": 1, "type": "action", "text": "Phát sự kiện gửi tin qua\nWebSocket / REST API"},
            {"lane": 2, "type": "action", "text": "Lưu tin nhắn vào CSDL và\nđẩy thông báo Real-time"},
            {"lane": 1, "type": "action", "text": "Hiển thị hội thoại khách\ntrên màn hình Admin Chat"},
            {"lane": 0, "type": "action", "text": "CSKH đọc câu hỏi và nhập\nnội dung tư vấn phản hồi"},
            {"lane": 2, "type": "action", "text": "Lưu tin phản hồi và phát sóng\ntức thì tới máy khách"},
            {"lane": 1, "type": "action", "text": "Render tin phản hồi ngay\ntức thì trên khung Chat"},
            {"lane": 0, "type": "action", "text": "Khách hàng đọc tư vấn,\ncảm ơn và tiếp tục đặt mua"},
            {"lane": 0, "type": "end"}
        ]
    },

    # --------------------------------------------------------------------------
    # 15. BÁO CÁO DOANH THU & XỬ LÝ HOÀN TIỀN
    # --------------------------------------------------------------------------
    {
        "id": 15,
        "title": "15. Báo cáo Doanh thu & Xử lý Hoàn tiền",
        "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "Cơ sở dữ liệu"],
        "actor_title": "Quản trị viên",
        "puml_body": """
|Quản trị viên|
start
:Mở Dashboard Quản trị Báo cáo Tài chính & Doanh thu (Lab 9);
:Chọn khoảng thời gian thống kê (Hôm nay, 7 ngày qua, Tháng này);

|Giao diện Admin|
:Gửi yêu cầu lấy số liệu tài chính lên Payment Service;

|Hệ thống xử lý|
:Tính toán KPI Doanh thu theo nguyên tắc Tài chính:
Chỉ tính các đơn hàng có trạng thái 'delivered' hoặc 'paid';

|Cơ sở dữ liệu|
:Truy vấn tổng doanh thu, số đơn, top sản phẩm bán chạy;

|Giao diện Admin|
:Vẽ Biểu đồ Doanh thu (Neon Spline) và hiển thị thẻ KPI;

|Quản trị viên|
:Chuyển sang tab Yêu cầu Hoàn tiền (Refund Pending);
:Kiểm tra lý do trả hàng và bấm nút "Phê duyệt Hoàn tiền";

|Giao diện Admin|
:Gửi lệnh phê duyệt hoàn tiền lên hệ thống;

|Hệ thống xử lý|
:Xác thực giao dịch và khởi tạo lệnh hoàn tiền;

|Cơ sở dữ liệu|
:Cập nhật trạng thái giao dịch sang 'refunded';
:Cập nhật trạng thái đơn hàng sang 'refunded';

|Giao diện Admin|
:Cập nhật lại số liệu Doanh thu thực tế và báo duyệt thành công;

|Quản trị viên|
:Nhìn thấy báo cáo tài chính đã được cân bằng chính xác;
stop
""",
        "flow": [
            {"lane": 0, "type": "start"},
            {"lane": 0, "type": "action", "text": "Mở Dashboard Báo cáo\nTài chính & Doanh thu"},
            {"lane": 0, "type": "action", "text": "Chọn khoảng thời gian thống kê\n(Hôm nay, 7 ngày, Tháng này)"},
            {"lane": 1, "type": "action", "text": "Gửi request lấy số liệu\ntài chính lên Payment Service"},
            {"lane": 2, "type": "action", "text": "Tính KPI Doanh thu theo rule:\nChỉ tính đơn delivered/paid"},
            {"lane": 3, "type": "action", "text": "Truy vấn tổng doanh thu,\nsố đơn và Top bán chạy"},
            {"lane": 1, "type": "action", "text": "Render Biểu đồ Neon Spline\nvà hiển thị các thẻ KPI"},
            {"lane": 0, "type": "action", "text": "Xem tab Yêu cầu hoàn tiền và\nbấm Phê duyệt Hoàn tiền"},
            {"lane": 1, "type": "action", "text": "Gửi lệnh phê duyệt hoàn\ntiền lên hệ thống"},
            {"lane": 2, "type": "action", "text": "Xác thực giao dịch và\nkhởi tạo lệnh hoàn tiền"},
            {"lane": 3, "type": "action", "text": "Cập nhật status giao dịch\nvà đơn hàng sang 'refunded'"},
            {"lane": 1, "type": "action", "text": "Cập nhật lại số liệu Doanh thu\nthực tế và báo thành công"},
            {"lane": 0, "type": "action", "text": "Nhìn thấy báo cáo tài chính\nđược cân bằng chính xác"},
            {"lane": 0, "type": "end"}
        ]
    }
]

# ==============================================================================
# GENERATE PLANTUML FILES
# ==============================================================================
puml_header = """@startuml
skinparam backgroundColor #FFFFFF
skinparam defaultFontName Arial
skinparam roundCorner 8
skinparam shadowing false

skinparam activity {
  BackgroundColor #FFFFFF
  BorderColor #000000
  BorderThickness 1.2
  FontColor #000000
  FontSize 11
}

skinparam diamond {
  BackgroundColor #FFFFFF
  BorderColor #000000
  BorderThickness 1.2
  FontColor #000000
  FontSize 10
}

skinparam swimlane {
  BorderColor #000000
  BorderThickness 1.2
  TitleBackgroundColor #FFFFFF
  TitleFontColor #000000
  TitleFontSize 12
  TitleFontStyle bold
}

skinparam arrow {
  Color #000000
  FontColor #000000
  FontSize 10
}
"""

os.makedirs("docs/plantuml", exist_ok=True)

filenames = [
    "1_Dang_ky_tai_khoan.puml",
    "2_Dang_nhap_he_thong.puml",
    "3_Quan_ly_khach_hang.puml",
    "4_Duyet_va_Tim_kiem_san_pham.puml",
    "5_Xem_chi_tiet_va_Ton_kho_SKU.puml",
    "6_Quan_tri_Catalog_san_pham.puml",
    "7_Quan_ly_gio_hang.puml",
    "8_Checkout_va_Tao_don_hang.puml",
    "9_Thanh_toan_khi_nhan_hang_COD.puml",
    "10_Thanh_toan_MoMo_Sandbox.puml",
    "11_Theo_doi_va_Huy_don_hang.puml",
    "12_Danh_gia_san_pham.puml",
    "13_Quan_tri_Don_hang_va_GHN_1Click.puml",
    "14_Tu_van_truc_tuyen_LiveChat.puml",
    "15_Bao_cao_Doanh_thu_va_Hoan_tien.puml"
]

for idx, diag in enumerate(DIAGRAM_DATA):
    fn = filenames[idx]
    puml_content = puml_header + diag["puml_body"].strip() + "\n@enduml\n"
    with open(f"docs/plantuml/{fn}", "w", encoding="utf-8") as f:
        f.write(puml_content)
    print(f"Generated PUML: {fn}")

# ==============================================================================
# GENERATE FLAWLESS DRAWIO XML (FLAT ABSOLUTE POSITIONING - ZERO OVERLAP)
# ==============================================================================
style_action = "rounded=1;whiteSpace=wrap;html=1;arcSize=30;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
style_dec = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
style_start = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#b85450;"
style_end = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#b85450;"
style_edge = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;strokeWidth=1.5;endArrow=classic;fontSize=10;fontColor=#000000;fontFamily=Helvetica;"
style_lane = "swimlane;html=1;startSize=28;fillColor=#f8cecc;strokeColor=#b85450;fontStyle=1;fontSize=12;fontFamily=Helvetica;align=center;collapsible=0;"

lane_defs_4 = [
    {"x": 40, "w": 180, "node_x": 60, "node_w": 140, "circle_x": 115},
    {"x": 220, "w": 180, "node_x": 240, "node_w": 140, "circle_x": 295},
    {"x": 400, "w": 190, "node_x": 425, "node_w": 140, "dec_x": 430, "dec_w": 130, "circle_x": 480},
    {"x": 590, "w": 180, "node_x": 610, "node_w": 140, "circle_x": 665}
]

# 5 lanes for LiveChat
lane_defs_5 = [
    {"x": 30, "w": 150, "node_x": 45, "node_w": 120, "circle_x": 90},
    {"x": 180, "w": 150, "node_x": 195, "node_w": 120, "circle_x": 240},
    {"x": 330, "w": 160, "node_x": 345, "node_w": 130, "circle_x": 395},
    {"x": 490, "w": 150, "node_x": 505, "node_w": 120, "circle_x": 550},
    {"x": 640, "w": 150, "node_x": 655, "node_w": 120, "circle_x": 700}
]

mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T22:00:00.000Z", agent="Striker Rich Diagram Generator V9", version="21.0.0", type="device")
os.makedirs('docs/drawio_xml', exist_ok=True)

# Generate individual XML and multi-page drawio
for diag_idx, diag in enumerate(DIAGRAM_DATA):
    num_lanes = len(diag["lanes"])
    defs = lane_defs_5 if num_lanes == 5 else lane_defs_4
    
    # Calculate vertical spacing cleanly
    # Every step gets its own clean Y-level to guarantee ZERO overlap
    current_y = 80
    y_step = 68
    
    nodes_built = []
    edges_built = []
    
    # Track sequence of nodes for main flow and branch flow
    prev_node_id = None
    dec_node_id = None
    
    # We lay out the nodes step-by-step
    for item_idx, item in enumerate(diag["flow"]):
        lane_idx = min(item["lane"], num_lanes - 1)
        l_def = defs[lane_idx]
        n_type = item["type"]
        n_id = f"n_{diag_idx+1}_{item_idx}"
        
        branch = item.get("branch", "main")
        
        # Dimensions
        if n_type == "start":
            w, h = 30, 30
            x = l_def["circle_x"]
            y = current_y
            current_y += 55
            style = style_start
            txt = ""
        elif n_type == "end":
            w, h = 28, 28
            x = l_def["circle_x"]
            y = current_y
            current_y += 65
            style = style_end
            txt = ""
        elif n_type == "decision":
            w, h = 130, 48
            x = l_def.get("dec_x", l_def["node_x"])
            y = current_y
            current_y += 68
            style = style_dec
            txt = item["text"]
            dec_node_id = n_id
        else: # action
            w, h = l_def.get("node_w", 140), 45
            x = l_def["node_x"]
            y = current_y
            current_y += y_step
            style = style_action
            txt = item["text"]
            
        nodes_built.append({
            "id": n_id,
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "style": style,
            "text": txt,
            "type": n_type,
            "branch": branch
        })

    # Connect edges cleanly
    for i in range(len(nodes_built)):
        curr = nodes_built[i]
        if i == 0:
            continue
            
        # If this is right after a decision diamond
        if nodes_built[i-1]["type"] == "decision":
            # First branch after decision (usually error/false branch)
            edges_built.append({
                "src": nodes_built[i-1]["id"],
                "tgt": curr["id"],
                "label": "Không / Lỗi"
            })
        elif curr["branch"] == "ok" and (nodes_built[i-1]["branch"] != "ok"):
            # Connect decision to the OK branch
            # Find the decision node
            dec = [n for n in nodes_built if n["type"] == "decision"]
            if dec:
                edges_built.append({
                    "src": dec[-1]["id"],
                    "tgt": curr["id"],
                    "label": "Hợp lệ / Thành công"
                })
        elif curr["branch"] == "locked" and (nodes_built[i-1]["branch"] != "locked"):
            dec = [n for n in nodes_built if n["type"] == "decision"]
            if dec:
                edges_built.append({
                    "src": dec[-1]["id"],
                    "tgt": curr["id"],
                    "label": "Bị khóa"
                })
        elif curr["branch"] == "active" and (nodes_built[i-1]["branch"] != "active"):
            dec = [n for n in nodes_built if n["type"] == "decision"]
            if dec:
                edges_built.append({
                    "src": dec[-1]["id"],
                    "tgt": curr["id"],
                    "label": "Active"
                })
        elif nodes_built[i-1]["type"] == "end":
            # Don't connect from an end node
            pass
        else:
            edges_built.append({
                "src": nodes_built[i-1]["id"],
                "tgt": curr["id"],
                "label": ""
            })

    pool_h = current_y + 40
    
    diagram = ET.SubElement(mxfile, "diagram", name=diag["title"], id=f"v9_diag_{diag_idx+1}")
    mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="700", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="950", pageHeight=str(pool_h + 100), math="0", shadow="0")
    root = ET.SubElement(mxGraphModel, "root")
    
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    # Swimlanes
    for l_idx, l_name in enumerate(diag["lanes"]):
        l_def = defs[l_idx]
        l_id = f"lane_{diag_idx+1}_{l_idx}"
        l_cell = ET.SubElement(root, "mxCell", id=l_id, value=l_name, style=style_lane, vertex="1", parent="1")
        ET.SubElement(l_cell, "mxGeometry", x=str(l_def["x"]), y="40", width=str(l_def["w"]), height=str(pool_h), as_="geometry")

    # Nodes
    for n in nodes_built:
        n_cell = ET.SubElement(root, "mxCell", id=n["id"], value=n["text"], style=n["style"], vertex="1", parent="1")
        ET.SubElement(n_cell, "mxGeometry", x=str(n["x"]), y=str(n["y"]), width=str(n["w"]), height=str(n["h"]), as_="geometry")

    # Edges
    for e_idx, e in enumerate(edges_built):
        e_id = f"edge_{diag_idx+1}_{e_idx}"
        e_cell = ET.SubElement(root, "mxCell", id=e_id, value=e["label"], style=style_edge, edge="1", source=e["src"], target=e["tgt"], parent="1")
        ET.SubElement(e_cell, "mxGeometry", relative="1", as_="geometry")

    # Export individual XML
    xml_str = ET.tostring(mxGraphModel, encoding='unicode')
    with open(f"docs/drawio_xml/So_do_{diag_idx+1}.xml", "w", encoding="utf-8") as f:
        f.write(xml_str)

tree = ET.ElementTree(mxfile)
ET.indent(tree, space="  ", level=0)
tree.write("docs/striker_activity_diagrams.drawio", encoding="utf-8", xml_declaration=True)
print("SUCCESS: Generated all 15 Rich Activity Diagrams (PlantUML + DrawIO XML)!")
