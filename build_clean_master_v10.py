import os
import xml.etree.ElementTree as ET

def build_master_diagrams():
    # Style definitions matching Image 2 perfectly (Crisp Black & White, elegant rounded boxes, orthogonal arrows)
    style_action = "rounded=1;whiteSpace=wrap;html=1;arcSize=30;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
    style_dec = "rhombus;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#000000;fontColor=#000000;fontSize=10;fontFamily=Helvetica;align=center;"
    style_start = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#000000;"
    style_end = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
    style_edge = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#000000;strokeWidth=1.2;endArrow=classic;fontSize=10;fontColor=#000000;fontFamily=Helvetica;"
    style_lane = "swimlane;html=1;startSize=28;fillColor=#FFFFFF;strokeColor=#000000;fontStyle=1;fontSize=12;fontFamily=Helvetica;align=center;collapsible=0;"

    lane_defs = [
        {"x": 40, "w": 180, "node_x": 60, "node_w": 140, "circle_x": 115},
        {"x": 220, "w": 180, "node_x": 240, "node_w": 140, "circle_x": 295},
        {"x": 400, "w": 190, "node_x": 425, "node_w": 140, "dec_x": 430, "dec_w": 130, "circle_x": 480},
        {"x": 590, "w": 180, "node_x": 610, "node_w": 140, "circle_x": 665}
    ]

    diagrams = [
        # =========================================================================
        # 1. ĐĂNG KÝ TÀI KHOẢN
        # =========================================================================
        {
            "title": "1. Đăng ký tài khoản",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Đăng ký và\nnhập thông tin cá nhân"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Kiểm tra hợp lệ form &\ngửi dữ liệu lên Server"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tiếp nhận & Chuẩn hóa\ndữ liệu người dùng"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn kiểm tra\ntrùng lặp Email / SĐT"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị trạng thái kiểm tra\nvà xác nhận thông tin"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Xác nhận Điều khoản &\nbấm nút Tạo tài khoản"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu đăng ký\nchính thức lên Auth"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra tính duy nhất\ncủa Email và SĐT"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Hợp lệ chu trình?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo lỗi tài khoản đã\ntồn tại / Sai dữ liệu"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Lưu bản ghi User mới\nvào bảng users (Active)"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Mã hóa Bcrypt mật khẩu\nvà khởi tạo hồ sơ KH"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Thông báo Đăng ký thành công\nvà chuyển sang Đăng nhập"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhận thông báo và sẵn\nsàng đăng nhập hệ thống"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Vi phạm"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 2. ĐĂNG NHẬP HỆ THỐNG
        # =========================================================================
        {
            "title": "2. Đăng nhập hệ thống",
            "lanes": ["Người dùng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Đăng nhập\nvà điền Email / Mật khẩu"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi request xác thực\nlên Auth Service"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tiếp nhận & kiểm tra\nđịnh dạng dữ liệu"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn tài khoản &\nlấy hash Bcrypt mật khẩu"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị trạng thái xử lý\nxác thực người dùng"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Tích Ghi nhớ đăng nhập\nvà bấm nút Đăng nhập"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi thông tin đăng nhập\nchính thức lên hệ thống"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "So khớp Password &\nkiểm tra status active"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Đúng thông tin?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Thông báo sai thông tin\nđăng nhập hoặc bị khóa"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật thời gian\nđăng nhập gần nhất"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Tạo JWT Token phiên &\nUser Data Payload"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Lưu Token vào Storage\nvà chuyển về Trang chủ"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Đăng nhập thành công &\nxem menu tài khoản cá nhân"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Sai thông tin"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Chính xác"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 3. QUẢN LÝ KHÁCH HÀNG (KHÓA / MỞ KHÓA)
        # =========================================================================
        {
            "title": "3. Quản lý khách hàng (Khóa / Mở khóa)",
            "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Quản lý\nkhách hàng trên Admin"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi request lấy DS\nkhách hàng (kèm Token)"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Xác thực quyền Admin\nvà phân trang dữ liệu"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn bảng users\nlấy danh sách khách hàng"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị danh sách khách,\ntổng chi tiêu & trạng thái"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn tài khoản vi phạm &\nnhấn nút Khóa / Mở khóa"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu đổi trạng\nthái tài khoản lên Backend"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra ràng buộc\n(không tự khóa tài khoản)"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Thao tác hợp lệ?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo lỗi không được phép\ntự khóa tài khoản Admin"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật status user\ntrong CSDL (is_active)"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Hủy Token phiên làm\nviệc nếu tài khoản bị khóa"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Cập nhật Badge trạng thái\nvà thông báo thành công"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhìn thấy trạng thái mới\ncủa khách hàng trên bảng"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Vi phạm"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 4. DUYỆT VÀ TÌM KIẾM SẢN PHẨM
        # =========================================================================
        {
            "title": "4. Duyệt và Tìm kiếm sản phẩm",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL & Cache"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Truy cập Cửa hàng (Shop)\nvà nhập từ khóa tìm kiếm"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi query parameters\nlên Catalog Service"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Chuẩn hóa từ khóa &\nxử lý logic bộ lọc"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn bảng products\ntheo tên, giá, danh mục"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị bộ lọc nâng cao\n(Hãng, Khoảng giá, Size)"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn lọc Danh mục, Hãng\nvà Sắp xếp theo giá"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu lọc danh\nsách sản phẩm kết hợp"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Thực hiện truy vấn lọc\nvà đếm số lượng kết quả"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Có kết quả SP?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo không tìm thấy SP\n& gợi ý xóa bộ lọc"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Lấy danh sách SP, ảnh\nvà khoảng giá biến thể"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Format dữ liệu ảnh,\ngiá bán & phân trang"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Render danh sách SP\ndưới dạng lưới (Grid)"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Lướt xem danh sách và\nnhấp chọn SP xem chi tiết"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Không thấy"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Có SP"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 5. XEM CHI TIẾT SẢN PHẨM & TỒN KHO SKU
        # =========================================================================
        {
            "title": "5. Xem chi tiết & Tồn kho SKU",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Nhấn chọn một sản phẩm\ntừ danh sách hoặc trang chủ"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi request lấy chi tiết\nSP theo Slug / ID"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tiếp nhận & điều phối\ntruy vấn Catalog"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn Products,\nImages và bảng SKUs"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị thông tin SP, ảnh,\nmô tả và bảng chọn Size"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Nhấp chọn Màu sắc, Size\nvà số lượng muốn mua"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu kiểm tra tồn\nkho biến thể SKU đã chọn"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Xác định mã SKU &\ntra cứu tồn kho khả dụng"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "SKU còn hàng?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo Tạm hết hàng &\nkhóa nút Thêm giỏ"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Lấy giá bán & số lượng\ntồn kho (stock_quantity)"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Xác nhận SKU còn hàng\nvà mở khóa nút mua hàng"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Cập nhật giá chính xác &\nmở nút Thêm vào giỏ"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Bấm Thêm vào giỏ hàng &\nkiểm tra Drawer giỏ hàng"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Hết hàng"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Còn hàng"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 6. QUẢN TRỊ CATALOG SẢN PHẨM
        # =========================================================================
        {
            "title": "6. Quản trị Catalog sản phẩm",
            "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "CSDL & Storage"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở Quản trị Catalog và\nbấm Thêm sản phẩm mới"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị biểu mẫu nhập\nthông tin SP & SKU"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tải danh mục và hãng\nphục vụ tạo sản phẩm"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Lấy categories, brands\ntrong CSDL Catalog"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Render form điền tên, giá,\nmô tả và album ảnh"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Nhập thông tin, cấu hình\nbiến thể & bấm Lưu"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi dữ liệu Multipart\nlên Backend Catalog"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra dữ liệu\n(tên, giá > 0, ảnh hợp lệ)"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Dữ liệu hợp lệ?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Thông báo lỗi nhập liệu\ntrên biểu mẫu Admin"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Lưu file ảnh vào Storage\n& Lưu Product, SKUs"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Xóa Cache danh mục\nđể đồng bộ sản phẩm"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Thông báo tạo thành công\nvà tải lại danh sách"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhìn thấy sản phẩm mới\ntrên bảng Catalog"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Lỗi dữ liệu"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 7. QUẢN LÝ GIỎ HÀNG
        # =========================================================================
        {
            "title": "7. Quản lý giỏ hàng",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở Giỏ hàng (Drawer)\ntừ Header trang web"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị danh sách món\nvà tổng tiền tạm tính"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Lấy chi tiết từng món\nkèm giá và tồn kho"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn cart_items\nvà bảng product_variants"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị nút tăng/giảm SL,\nnút xóa và ô nhập Voucher"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Tăng/Giảm số lượng hoặc\nnhập mã giảm giá Coupon"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi request cập nhật giỏ\nvà voucher lên Backend"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra tồn kho khả dụng\nvà điều kiện áp Voucher"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Đủ tồn kho & Hạn?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Cảnh báo vượt quá tồn kho\nhoặc mã Voucher hết hạn"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật bảng cart_items\nvà lưu voucher đã áp dụng"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Tính lại Tạm tính, Tiền\ngiảm giá và Tổng tiền"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Cập nhật Badge giỏ hàng,\nbảng giá & mở nút Checkout"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Xem tổng tiền chính xác và\nbấm Tiến hành Đặt hàng"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Không hợp lệ"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 8. CHECKOUT VÀ TẠO ĐƠN HÀNG (GHN + VOUCHER)
        # =========================================================================
        {
            "title": "8. Checkout và Tạo đơn hàng (GHN + Voucher)",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "GHN Logistics & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Truy cập Checkout và\nchọn Địa chỉ giao hàng"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi địa chỉ nhận (Tỉnh,\nHuyện, Xã) lên Backend"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Điều phối request tính phí\nqua Giao Hàng Nhanh"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Gọi API GHN lấy phí ship\n& kiểm tra bảng coupons"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị phí ship GHN &\ncác phương thức thanh toán"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn PTTT (COD/MoMo) &\nbấm Xác nhận Đặt hàng"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu tạo đơn hàng\nchính thức lên hệ thống"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Khóa giữ tồn kho SKU &\nxác thực dữ liệu đơn hàng"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Giữ hàng tồn kho?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo sản phẩm trong giỏ\nvừa hết hàng đột xuất"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Lưu đơn vào orders &\ntrừ tồn kho các SKUs"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Khởi tạo giao dịch &\nxóa sạch giỏ hàng đã mua"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Điều hướng cổng thanh toán\nhoặc trang Đặt hàng thành công"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhận mã tra cứu đơn hàng\nvà theo dõi tiến độ giao"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Hết hàng"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Thành công"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 9. THANH TOÁN KHI NHẬN HÀNG (COD)
        # =========================================================================
        {
            "title": "9. Thanh toán khi nhận hàng (COD)",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL & Mail"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Chọn phương thức COD\ntại trang Checkout"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị thông tin đơn &\ntiền thu hộ khi nhận hàng"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Kiểm tra tính hợp lệ\ncủa thông tin địa chỉ"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Xác nhận địa chỉ và\nsố điện thoại người nhận"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị nút xác nhận\nđặt hàng phương thức COD"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Kiểm tra lại thông tin và\nbấm nút Đặt hàng COD"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi request khởi tạo đơn\nCOD lên Payment & Order"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Khởi tạo giao dịch COD\nvới payment_status = 'pending'"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Hợp lệ đơn hàng?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo lỗi không thể khởi\ntạo đơn hàng COD"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật order_status = 'pending'\nvà xóa sạch giỏ hàng"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Gửi Email xác nhận đơn\nkèm hóa đơn điện tử cho KH"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Hiển thị màn hình Đặt hàng\nthành công & mã tra cứu"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Xem thông tin đơn, kiểm tra\nEmail và sẵn sàng nhận hàng"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Vi phạm"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 10. THANH TOÁN MOMO SANDBOX
        # =========================================================================
        {
            "title": "10. Thanh toán MoMo Sandbox",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cổng MoMo & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Chọn thanh toán MoMo\nvà bấm Đặt hàng"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi yêu cầu tạo phiên\nthanh toán MoMo AIO"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Ký số HMAC-SHA256\ntừ secretKey bảo mật"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Gọi API MoMo Sandbox và\nnhận payUrl, qrCodeUrl"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Điều hướng khách sang\nCổng thanh toán MoMo"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Mở App MoMo quét mã QR\nhoặc xác nhận thanh toán"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Chờ phản hồi kết quả\ntừ Cổng MoMo Sandbox"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra chữ ký số IPN\nxác thực dữ liệu từ MoMo"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Giao dịch MoMo OK?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Hiển thị thông báo thanh\ntoán MoMo thất bại / Hủy"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật payment_status = 'paid'\nvà order_status = 'paid'"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Ghi log giao dịch MoMo\nvà gửi Mail hóa đơn điện tử"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Điều hướng về /payment/callback\n& báo Thanh toán thành công!"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhận biên lai điện tử và\ntheo dõi tiến độ giao hàng"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Thất bại"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Thành công"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 11. THEO DÕI VÀ HỦY ĐƠN HÀNG
        # =========================================================================
        {
            "title": "11. Theo dõi & Hủy đơn hàng",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Đơn hàng của tôi\ntừ menu tài khoản Header"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi request lấy lịch sử\nđơn hàng kèm Token KH"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn danh sách đơn\ntheo user_id của khách"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Lấy orders, order_items\nvà trạng thái giao hàng"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị danh sách đơn &\ntiến độ vận chuyển GHN"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn đơn Pending và\nbấm Yêu cầu Hủy đơn"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu hủy đơn hàng\nlên Order Service"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra trạng thái đơn\n(order_status == 'pending')"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Được phép hủy?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Thông báo đơn đã bàn giao GHN,\nkhông thể tự hủy trực tuyến"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật order_status = 'cancelled'\nvà hoàn tồn kho các SKU"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Ghi log lý do hủy đơn và\ngửi thông báo hoàn tất"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Báo Hủy đơn thành công &\ncập nhật trạng thái giao diện"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhìn thấy trạng thái đơn\nchuyển sang Đã hủy"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Từ chối"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Cho phép"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 12. ĐÁNH GIÁ SẢN PHẨM
        # =========================================================================
        {
            "title": "12. Đánh giá sản phẩm (Review/Rating)",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở đơn hàng đã nhận\nvà bấm Viết đánh giá SP"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị Modal đánh giá\n(sao, bình luận, ảnh)"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Kiểm tra điều kiện khách\nđã mua và nhận sản phẩm"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn bảng orders kiểm tra\nstatus = 'delivered'"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Mở khung chấm 1-5 sao\nvà nhập nhận xét trải nghiệm"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn số sao, viết bình luận\nvà bấm nút Gửi đánh giá"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi nội dung đánh giá kèm\nAuth Token lên Backend"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Xác thực tính hợp lệ của\nnội dung và quyền đánh giá"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Đủ điều kiện?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo lỗi bạn chỉ có thể\nđánh giá khi đã nhận hàng"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Lưu bản ghi mới vào bảng\nreviews trong CSDL"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Tính lại điểm đánh giá\ntrung bình của sản phẩm"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Báo Cảm ơn đánh giá &\nrender bình luận mới"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhìn thấy nhận xét và số\nsao của mình trên trang SP"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Chưa nhận"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 13. QUẢN TRỊ ĐƠN HÀNG & GHN 1-CLICK
        # =========================================================================
        {
            "title": "13. Quản trị Đơn hàng & GHN 1-Click",
            "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "GHN Logistics & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Quản lý đơn hàng\ntrên Dashboard Admin"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Lọc đơn hàng Đã thanh toán /\nChờ xử lý giao hàng"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Xác thực quyền Admin và\ntruy vấn danh sách đơn"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Lấy thông tin đơn hàng,\nđịa chỉ và tiền COD"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị danh sách đơn &\nnút 1-Click Tạo đơn GHN"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Kiểm tra chi tiết kiện hàng &\nbấm 1-Click Tạo đơn GHN"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu tạo vận đơn\ngiao hàng lên Backend"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Đóng gói dữ liệu người nhận,\ntrọng lượng và tiền COD"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Hợp lệ bưu kiện?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo lỗi địa chỉ hoặc trọng\nlượng GHN không hợp lệ"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Gọi API GHN tạo đơn và\nnhận Mã vận đơn tracking"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Lưu mã tracking vào đơn &\ncập nhật status = 'shipping'"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Hiển thị mã vận đơn GHN &\ncập nhật Đang giao hàng"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "In phiếu gửi hàng GHN, dán\ntem và bàn giao bưu tá"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Vi phạm"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 14. TƯ VẤN TRỰC TUYẾN LIVECHAT CSKH
        # =========================================================================
        {
            "title": "14. Tư vấn trực tuyến LiveChat CSKH",
            "lanes": ["Khách hàng", "Giao diện Chat", "WebSocket Gateway", "CSKH & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở khung chat & nhập\nnội dung câu hỏi tư vấn"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Phát sự kiện WebSocket\nsocket.emit('send_msg')"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tiếp nhận gói tin socket\nvà xác thực phiên chat"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Lưu tin nhắn vào CSDL\n& đẩy sang Admin Chat"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị tin nhắn đã gửi\ntrong khung chat client"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chờ nhân viên CSKH\ntiếp nhận và trả lời"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Admin Chat hiển thị badge\ntin nhắn mới từ khách"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Điều phối phiên chat trực\ntuyến giữa Khách & Admin"},
                {"id": "db2", "lane": 3, "type": "action", "y": 420, "w": 140, "h": 45, "text": "Nhân viên CSKH đọc tin\nvà nhập nội dung trả lời"},
                {"id": "be3", "lane": 2, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Broadcast sự kiện realtime\nvề kênh của Khách hàng"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Render tin nhắn phản hồi\nlên khung chat client"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Đọc câu trả lời và tiếp\ntục trao đổi hỗ trợ"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "db2"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 15. BÁO CÁO TÀI CHÍNH & HOÀN TIỀN (LAB 9) - HÌNH 2 GỐC
        # =========================================================================
        {
            "title": "15. Báo cáo Tài chính & Hoàn tiền (Lab 9)",
            "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "CSDL & Cổng MoMo"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Quản trị\nTài chính (Finance)"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi request tổng hợp số\nliệu doanh thu theo kỳ"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tiếp nhận & thực hiện\ntính toán thống kê"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tổng hợp doanh thu thực &\nbảng đối soát MoMo/COD"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị 4 thẻ KPI,\nSpline Chart & Giao dịch"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn đơn cần hoàn tiền\nvà bấm Duyệt hoàn tiền"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi yêu cầu hoàn tiền\ncho đơn hàng"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra ràng buộc\nState Machine hoàn tiền"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Hợp lệ chu trình?"},
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo lỗi đơn hàng không\nđủ điều kiện hoàn tiền"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Gọi MoMo Refund API &\ncập nhật trạng thái refunded"},
                {"id": "be3", "lane": 2, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Trừ doanh thu thực tế &\nghi log đối soát"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Thông báo hoàn tất &\ncập nhật lại biểu đồ"},
                {"id": "u3", "lane": 0, "type": "action", "y": 630, "w": 140, "h": 45, "text": "Nhận thông báo đối soát\nhoàn tất thành công"},
                {"id": "end", "lane": 0, "type": "end", "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Vi phạm"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        }
    ]

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T22:15:00.000Z", agent="Striker Master 4-Lane Generator V10", version="21.0.0", type="device")
    os.makedirs('docs/drawio_xml', exist_ok=True)

    for diag_idx, diag in enumerate(diagrams):
        max_y = max([node["y"] for node in diag["nodes"]]) + 80
        pool_h = max(600, max_y)

        diagram = ET.SubElement(mxfile, "diagram", name=diag["title"], id=f"master_diag_{diag_idx+1}")
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="700", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="850", pageHeight=str(pool_h + 80), math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        # 4 Flat Swimlanes
        for l_idx, l_name in enumerate(diag["lanes"]):
            l_def = lane_defs[l_idx]
            l_id = f"lane_{diag_idx+1}_{l_idx}"
            l_cell = ET.SubElement(root, "mxCell", id=l_id, value=l_name, style=style_lane, vertex="1", parent="1")
            ET.SubElement(l_cell, "mxGeometry", x=str(l_def["x"]), y="40", width=str(l_def["w"]), height=str(pool_h), as_="geometry")

        node_map = {}
        for n in diag["nodes"]:
            n_id = f"node_{diag_idx+1}_{n['id']}"
            node_map[n["id"]] = n_id
            l_def = lane_defs[n["lane"]]
            
            w = n.get("w", 140)
            h = n.get("h", 45)
            
            if n["type"] == "start":
                style = style_start
                x = l_def["circle_x"]
            elif n["type"] == "end":
                style = style_end
                x = l_def["circle_x"]
            elif n["type"] == "decision":
                style = style_dec
                x = l_def.get("dec_x", l_def["node_x"])
            else: # action
                style = style_action
                x = l_def["node_x"]

            n_cell = ET.SubElement(root, "mxCell", id=n_id, value=n.get("text", ""), style=style, vertex="1", parent="1")
            ET.SubElement(n_cell, "mxGeometry", x=str(x), y=str(n["y"]), width=str(w), height=str(h), as_="geometry")

        for e_idx, e in enumerate(diag["edges"]):
            e_id = f"edge_{diag_idx+1}_{e_idx}"
            src = node_map[e["src"]]
            tgt = node_map[e["tgt"]]
            lbl = e.get("label", "")
            
            e_cell = ET.SubElement(root, "mxCell", id=e_id, value=lbl, style=style_edge, edge="1", source=src, target=tgt, parent="1")
            ET.SubElement(e_cell, "mxGeometry", relative="1", as_="geometry")

        # Export individual XML
        xml_str = ET.tostring(mxGraphModel, encoding='unicode')
        with open(f"docs/drawio_xml/So_do_{diag_idx+1}.xml", "w", encoding="utf-8") as f:
            f.write(xml_str)

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write("docs/striker_activity_diagrams.drawio", encoding="utf-8", xml_declaration=True)
    print("SUCCESS: Generated all 15 Master Draw.io XML files matching Image 2 perfectly!")

if __name__ == "__main__":
    build_master_diagrams()
