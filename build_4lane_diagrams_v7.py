import os
import xml.etree.ElementTree as ET

def build_4lane_diagrams():
    # Style definitions matching clean Draw.io standards
    style_action = "rounded=1;whiteSpace=wrap;html=1;arcSize=30;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
    style_dec = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
    style_start = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#b85450;"
    style_end = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#b85450;"
    style_edge = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;strokeWidth=1.5;endArrow=classic;fontSize=10;fontColor=#000000;fontFamily=Helvetica;"

    lane_w = 185
    pool_w = lane_w * 4 # 740px

    diagrams = [
        # =========================================================================
        # 1. ĐĂNG KÝ TÀI KHOẢN VÀ XÁC THỰC OTP
        # =========================================================================
        {
            "title": "1. Đăng ký tài khoản và Xác thực OTP",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL & Mail"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Chọn chức năng\nĐăng ký tài khoản"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Hiển thị biểu mẫu\nđăng ký tài khoản"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Nhập Họ tên, Email,\nSĐT, Mật khẩu & Bấm ĐK"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Gửi thông tin đăng ký\nlên Backend"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Kiểm tra định dạng\nvà quy chuẩn dữ liệu"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Truy vấn kiểm tra\ntrùng lặp Email/SĐT"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 325, "w": 130, "h": 50, "text": "Thông tin hợp lệ?"},
                {"id": "ui_err1", "lane": 1, "type": "action", "x": 22, "y": 328, "w": 140, "h": 45, "text": "Hiển thị thông báo\nlỗi / đã tồn tại"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 395, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Lưu tài khoản Pending\nvà gửi mã OTP qua Mail"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Hiển thị màn hình\nnhập mã OTP"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Nhập mã OTP từ Email\nvà nhấn Xác thực"},
                {"id": "ui4", "lane": 1, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Gửi mã OTP xác thực"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Kiểm tra thời hạn\nvà tính hợp lệ của OTP"},
                {"id": "db3", "lane": 3, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "So khớp mã OTP\ntrong CSDL"},
                {"id": "dec2", "lane": 2, "type": "decision", "x": 27, "y": 625, "w": 130, "h": 50, "text": "Mã OTP đúng?"},
                {"id": "ui_err2", "lane": 1, "type": "action", "x": 22, "y": 628, "w": 140, "h": 45, "text": "Báo sai mã OTP\nhoặc mã đã hết hạn"},
                {"id": "err2", "lane": 1, "type": "end", "x": 78, "y": 695, "w": 28, "h": 28},
                {"id": "db4", "lane": 3, "type": "action", "x": 22, "y": 700, "w": 140, "h": 45, "text": "Cập nhật tài khoản\nsang trạng thái Active"},
                {"id": "be3", "lane": 2, "type": "action", "x": 22, "y": 775, "w": 140, "h": 45, "text": "Cấp JWT Token\nphiên đăng nhập"},
                {"id": "ui5", "lane": 1, "type": "action", "x": 22, "y": 775, "w": 140, "h": 45, "text": "Thông báo thành công\nvà chuyển Trang chủ"},
                {"id": "u4", "lane": 0, "type": "action", "x": 22, "y": 850, "w": 140, "h": 45, "text": "Đăng nhập thành công\nvào hệ thống"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 925, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "u2"},
                {"src": "u2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err1", "label": "Sai/Trùng"},
                {"src": "ui_err1", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "u3"},
                {"src": "u3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "be2"},
                {"src": "be2", "tgt": "db3"},
                {"src": "db3", "tgt": "dec2"},
                {"src": "dec2", "tgt": "ui_err2", "label": "Sai OTP"},
                {"src": "ui_err2", "tgt": "err2"},
                {"src": "dec2", "tgt": "db4", "label": "Đúng OTP"},
                {"src": "db4", "tgt": "be3"},
                {"src": "be3", "tgt": "ui5"},
                {"src": "ui5", "tgt": "u4"},
                {"src": "u4", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 2. ĐĂNG NHẬP HỆ THỐNG
        # =========================================================================
        {
            "title": "2. Đăng nhập hệ thống",
            "lanes": ["Người dùng", "Giao diện", "Hệ thống xử lý", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Chọn chức năng\nĐăng nhập"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Hiển thị biểu mẫu\nđăng nhập"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Nhập Email / SĐT\nvà Mật khẩu"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Gửi thông tin xác thực"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Tiếp nhận & Kiểm tra\nđịnh dạng dữ liệu"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Truy vấn tài khoản &\nso khớp pass (bcrypt)"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 325, "w": 130, "h": 50, "text": "Đúng mật khẩu?"},
                {"id": "ui_err1", "lane": 1, "type": "action", "x": 22, "y": 328, "w": 140, "h": 45, "text": "Thông báo sai thông tin\nđăng nhập"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 395, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Kiểm tra trạng thái\n(status = active / locked)"},
                {"id": "dec2", "lane": 2, "type": "decision", "x": 27, "y": 475, "w": 130, "h": 50, "text": "Tài khoản active?"},
                {"id": "ui_err2", "lane": 1, "type": "action", "x": 22, "y": 478, "w": 140, "h": 45, "text": "Thông báo tài khoản\nđã bị khóa"},
                {"id": "err2", "lane": 1, "type": "end", "x": 78, "y": 545, "w": 28, "h": 28},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Tạo JWT Token &\nUser Payload"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Lưu Token vào Storage\nvà chuyển Trang chủ"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 625, "w": 140, "h": 45, "text": "Đăng nhập thành công\nvào hệ thống"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "u2"},
                {"src": "u2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err1", "label": "Sai pass"},
                {"src": "ui_err1", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Đúng pass"},
                {"src": "db2", "tgt": "dec2"},
                {"src": "dec2", "tgt": "ui_err2", "label": "Bị khóa"},
                {"src": "ui_err2", "tgt": "err2"},
                {"src": "dec2", "tgt": "be2", "label": "Active"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 3. QUẢN LÝ KHÁCH HÀNG (KHÓA / MỞ KHÓA)
        # =========================================================================
        {
            "title": "3. Quản lý khách hàng (Khóa / Mở khóa)",
            "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Mở trang Quản lý\nkhách hàng"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi request lấy DS\nkhách hàng (kèm Token)"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Xác thực quyền Admin\nvà phân trang"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Truy vấn bảng Users\nlấy danh sách KH"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Hiển thị danh sách &\ntrạng thái (Active/Locked)"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Chọn tài khoản &\nnhấn Khóa / Mở khóa"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Gửi yêu cầu đổi\ntrạng thái tài khoản"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Kiểm tra ràng buộc\n(không tự khóa Admin)"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 400, "w": 130, "h": 50, "text": "Thao tác hợp lệ?"},
                {"id": "ui_err1", "lane": 1, "type": "action", "x": 22, "y": 403, "w": 140, "h": 45, "text": "Báo lỗi không thể\nthực hiện thao tác"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 470, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Cập nhật status user\ntrong CSDL"},
                {"id": "be3", "lane": 2, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Hủy Token phiên\nđăng nhập của User"},
                {"id": "ui4", "lane": 1, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Thông báo thành công\nvà cập nhật giao diện"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 625, "w": 140, "h": 45, "text": "Nhìn thấy trạng thái mới\ncủa khách hàng"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 700, "w": 30, "h": 30}
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
                {"src": "dec1", "tgt": "ui_err1", "label": "Vi phạm"},
                {"src": "ui_err1", "tgt": "err1"},
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
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Nhập từ khóa tìm kiếm /\nchọn bộ lọc danh mục"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi query parameters\nlên Catalog Service"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Chuẩn hóa từ khóa &\nxử lý logic bộ lọc"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Truy vấn bảng products\ntheo tên, giá, danh mục"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 250, "w": 130, "h": 50, "text": "Có kết quả?"},
                {"id": "ui_empty", "lane": 1, "type": "action", "x": 22, "y": 253, "w": 140, "h": 45, "text": "Hiển thị thông báo\nkhông tìm thấy SP"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 320, "w": 28, "h": 28},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Format dữ liệu ảnh,\ngiá bán & phân trang"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Render danh sách SP\ndưới dạng lưới (Grid)"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Xem danh sách kết quả\nvà lựa chọn sản phẩm"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_empty", "label": "Không thấy"},
                {"src": "ui_empty", "tgt": "err1"},
                {"src": "dec1", "tgt": "be2", "label": "Có SP"},
                {"src": "be2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 5. XEM CHI TIẾT SẢN PHẨM VÀ TỒN KHO SKU
        # =========================================================================
        {
            "title": "5. Xem chi tiết & Tồn kho SKU",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Nhấn vào một SP\ntrên trang sản phẩm"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi request lấy chi tiết\nSP theo Slug / ID"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Tiếp nhận & điều phối\ntruy vấn Catalog"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Truy vấn Products,\nImages và bảng SKUs"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Hiển thị thông tin SP\nvà danh sách biến thể"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Chọn biến thể Màu sắc\nvà Kích thước (SKU)"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Gửi yêu cầu kiểm tra\nbiến thể SKU đã chọn"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Xác định mã SKU &\ntra cứu tồn kho"},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Lấy giá bán & số lượng\ntồn kho (stock_quantity)"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 400, "w": 130, "h": 50, "text": "SKU còn hàng?"},
                {"id": "ui_out", "lane": 1, "type": "action", "x": 22, "y": 403, "w": 140, "h": 45, "text": "Báo Tạm hết hàng &\nkhóa nút Thêm giỏ"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 470, "w": 28, "h": 28},
                {"id": "ui4", "lane": 1, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Cập nhật giá chính xác\nvà mở nút Thêm giỏ"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Xem giá chính xác &\nsẵn sàng đặt mua"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 550, "w": 30, "h": 30}
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
                {"src": "db2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_out", "label": "Hết hàng"},
                {"src": "ui_out", "tgt": "err1"},
                {"src": "dec1", "tgt": "ui4", "label": "Còn hàng"},
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
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Chọn chức năng\nThêm sản phẩm mới"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Hiển thị biểu mẫu nhập\nthông tin SP & SKU"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Nhập tên, danh mục,\nupload ảnh & cấu hình SKU"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Gửi dữ liệu Multipart\nlên Backend"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Kiểm tra dữ liệu\n(tên, giá > 0, ảnh hợp lệ)"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 325, "w": 130, "h": 50, "text": "Dữ liệu hợp lệ?"},
                {"id": "ui_err", "lane": 1, "type": "action", "x": 22, "y": 328, "w": 140, "h": 45, "text": "Thông báo lỗi nhập liệu\ntrên biểu mẫu"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 395, "w": 28, "h": 28},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Lưu file ảnh vào Storage\n& Lưu Product, SKUs"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Xóa Cache danh mục\nđể đồng bộ SP mới"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Thông báo tạo thành công\nvà chuyển về Danh sách"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Nhìn thấy sản phẩm mới\ntrong Catalog"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 625, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "u2"},
                {"src": "u2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Sai dữ liệu"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db1", "label": "Hợp lệ"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 7. QUẢN LÝ GIỎ HÀNG
        # =========================================================================
        {
            "title": "7. Quản lý giỏ hàng",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL & Redis"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Chọn số lượng & bấm\nThêm vào giỏ hàng"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi thông tin (user_id,\nsku_id, quantity)"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Tiếp nhận & kiểm tra\ntồn kho khả dụng"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Truy vấn tồn kho\ncủa SKU trong CSDL"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 250, "w": 130, "h": 50, "text": "Đủ số lượng tồn?"},
                {"id": "ui_err", "lane": 1, "type": "action", "x": 22, "y": 253, "w": 140, "h": 45, "text": "Báo số lượng tồn kho\nkhông đủ đáp ứng"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 320, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Thêm/cập nhật item\nvào bảng cart_items"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Tính lại tổng số lượng\nvà tạm tính giỏ hàng"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Cập nhật Badge giỏ\nvà mở Drawer giỏ hàng"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Nhìn thấy sản phẩm đã\nđược thêm vào giỏ"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 550, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Thiếu hàng"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Đủ hàng"},
                {"src": "db2", "tgt": "be2"},
                {"src": "be2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 8. CHECKOUT VÀ TẠO ĐƠN HÀNG (GHN + VOUCHER)
        # =========================================================================
        {
            "title": "8. Checkout và Tạo đơn hàng (GHN + Voucher)",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL & API GHN"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Nhập địa chỉ giao hàng\n& nhập mã Voucher"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi request tính ship\nvà áp dụng Voucher"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Gọi API GHN tính cước\n& kiểm tra hạn Voucher"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Áp dụng giảm giá &\ntính tổng tiền đơn hàng"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Hiển thị bảng tóm tắt\n(Tạm tính + Ship - Giảm)"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Chọn phương thức TT\n& bấm Xác nhận đặt hàng"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Gửi payload tạo đơn\nhàng lên Order Service"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Khởi tạo Transaction\ntạo đơn hàng mới"},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Khóa tồn kho SKU, Lưu\nOrders & Xóa giỏ hàng"},
                {"id": "be3", "lane": 2, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Tạo Order Code &\nchuyển tiếp thanh toán"},
                {"id": "ui4", "lane": 1, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Thông báo tạo đơn thành\ncông và chuyển hướng"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Nhận mã đơn hàng &\nhướng dẫn thanh toán"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 625, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "db1"},
                {"src": "db1", "tgt": "be1"},
                {"src": "be1", "tgt": "ui2"},
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
        # 9. THANH TOÁN KHI NHẬN HÀNG (COD)
        # =========================================================================
        {
            "title": "9. Thanh toán khi nhận hàng (COD)",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Chọn phương thức\nThanh toán COD & bấm TT"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi yêu cầu thanh toán\nCOD cho đơn hàng"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Tiếp nhận & xác thực\nđơn hàng của khách"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Kiểm tra trạng thái đơn\n(order_status = pending)"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 250, "w": 130, "h": 50, "text": "Đơn hàng hợp lệ?"},
                {"id": "ui_err", "lane": 1, "type": "action", "x": 22, "y": 253, "w": 140, "h": 45, "text": "Báo lỗi trạng thái\nđơn hàng không hợp lệ"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 320, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Cập nhật payment_method\n= COD, status = unpaid"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Kích hoạt chuyển đơn sang\ntrạng thái processing"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Hiển thị màn hình đặt\nhàng COD thành công"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Xem thông tin đơn hàng\nvà chờ nhận hàng"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 550, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Không hợp lệ"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be2"},
                {"src": "be2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 10. THANH TOÁN MOMO SANDBOX
        # =========================================================================
        {
            "title": "10. Thanh toán MoMo Sandbox",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cổng MoMo & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Chọn phương thức Ví MoMo\nvà bấm Thanh toán"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi yêu cầu khởi tạo\ngiao dịch MoMo"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Tạo chữ ký HMAC-SHA256\n& gửi payload sang MoMo"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "MoMo sinh mã giao dịch\nvà trả về payUrl / QR Code"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Hiển thị mã QR MoMo /\nchuyển hướng MoMo Gateway"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Quét mã QR & xác nhận\nthanh toán trên App"},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "MoMo trừ tiền & gửi\nWebhook IPN về Backend"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Xác thực chữ ký IPN\ntừ MoMo Server"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 400, "w": 130, "h": 50, "text": "Giao dịch thành công?"},
                {"id": "ui_fail", "lane": 1, "type": "action", "x": 22, "y": 403, "w": 140, "h": 45, "text": "Báo thanh toán thất bại\nhoặc KH hủy giao dịch"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 470, "w": 28, "h": 28},
                {"id": "db3", "lane": 3, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Cập nhật payment = paid,\norder = processing"},
                {"id": "be3", "lane": 2, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Kích hoạt gửi hóa đơn &\nđồng bộ trạng thái"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Hiển thị thông báo\nThanh toán MoMo thành công"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 625, "w": 140, "h": 45, "text": "Nhận thông báo xác nhận\ngiao dịch hoàn tất"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 700, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "db2"},
                {"src": "db2", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_fail", "label": "Thất bại"},
                {"src": "ui_fail", "tgt": "err1"},
                {"src": "dec1", "tgt": "db3", "label": "Thành công"},
                {"src": "db3", "tgt": "be3"},
                {"src": "be3", "tgt": "ui3"},
                {"src": "ui3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 11. THEO DÕI & HỦY ĐƠN HÀNG
        # =========================================================================
        {
            "title": "11. Theo dõi & Hủy đơn hàng",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Vào mục Đơn mua &\nchọn đơn hàng cần xem"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi request lấy chi tiết\nvà lịch sử đơn hàng"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Xác thực quyền sở hữu\nđơn hàng của User"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Truy vấn Orders, Items\nvà OrderTrackings"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Hiển thị tiến trình đơn\n(Pending/Ship/Delivered)"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Chọn lý do & nhấn nút\nHủy đơn hàng"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Gửi yêu cầu hủy đơn\nlên Order Service"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Kiểm tra điều kiện hủy\n(chỉ cho phép khi pending)"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 400, "w": 130, "h": 50, "text": "Trạng thái Pending?"},
                {"id": "ui_err", "lane": 1, "type": "action", "x": 22, "y": 403, "w": 140, "h": 45, "text": "Báo không thể hủy đơn\nđang giao/đã hoàn tất"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 470, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Cập nhật order = cancelled\nvà hoàn lại tồn kho SKU"},
                {"id": "be3", "lane": 2, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Kích hoạt hoàn trả và ghi\nlog lịch sử hủy đơn"},
                {"id": "ui4", "lane": 1, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Cập nhật trạng thái Đã hủy\nvà thông báo thành công"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 625, "w": 140, "h": 45, "text": "Nhận thông báo hủy đơn\nhàng thành công"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 700, "w": 30, "h": 30}
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
                {"src": "dec1", "tgt": "ui_err", "label": "Đang giao"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Pending"},
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
            "title": "12. Đánh giá sản phẩm",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Vào đơn đã nhận &\nbấm Đánh giá sản phẩm"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Hiển thị form đánh giá\n(Số sao, bình luận, ảnh)"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Chọn 1-5 sao, viết review\nvà bấm Gửi đánh giá"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Gửi payload đánh giá\nlên Backend"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Kiểm tra điều kiện KH\nđã mua & nhận SP chưa"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Truy vấn bảng Orders &\nbảng Reviews kiểm tra"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 325, "w": 130, "h": 50, "text": "Hợp lệ đánh giá?"},
                {"id": "ui_err", "lane": 1, "type": "action", "x": 22, "y": 328, "w": 140, "h": 45, "text": "Báo lỗi không đủ điều kiện\nhoặc đã đánh giá rồi"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 395, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Lưu bản ghi review mới\nvào bảng reviews"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Tính lại điểm rating TB\nvà cập nhật vào Products"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Thông báo Cảm ơn &\nhiển thị đánh giá mới"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Nhìn thấy review của mình\ntrên trang sản phẩm"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 625, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "u2"},
                {"src": "u2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Không hợp lệ"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Hợp lệ"},
                {"src": "db2", "tgt": "be2"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 13. QUẢN TRỊ ĐƠN HÀNG & GHN 1-CLICK
        # =========================================================================
        {
            "title": "13. Quản trị Đơn hàng & GHN 1-Click",
            "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "CSDL & API GHN"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Mở danh sách đơn hàng\ncần xử lý"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Hiển thị các đơn hàng\ntrạng thái processing"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Chọn đơn hàng & bấm\nTạo vận đơn GHN"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Gửi request đẩy đơn\nvận chuyển sang GHN"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Đóng gói payload ship\n(Người nhận, SĐT, Kích thước)"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Gọi API GHN Create Order\nsinh mã vận đơn"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 325, "w": 130, "h": 50, "text": "GHN tạo thành công?"},
                {"id": "ui_err", "lane": 1, "type": "action", "x": 22, "y": 328, "w": 140, "h": 45, "text": "Thông báo lỗi kết nối\nhoặc sai địa chỉ từ GHN"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 395, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 400, "w": 140, "h": 45, "text": "Lưu tracking_code GHN\nvà đổi trạng thái shipping"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Tạo đường dẫn in phiếu\ngiao hàng chuẩn GHN"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Thông báo thành công &\nmở pop-up in phiếu gửi"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "In phiếu vận chuyển và\ndán lên gói hàng"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 625, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "u2"},
                {"src": "u2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Lỗi GHN"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Thành công"},
                {"src": "db2", "tgt": "be2"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 14. TƯ VẤN TRỰC TUYẾN LIVECHAT CSKH (LAB 7)
        # =========================================================================
        {
            "title": "14. Tư vấn trực tuyến LiveChat CSKH (Lab 7)",
            "lanes": ["Khách hàng", "Giao diện Chat", "WebSocket Gateway", "CSKH & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Mở khung chat & nhập\nnội dung câu hỏi tư vấn"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Phát sự kiện WebSocket\nsocket.emit('send_msg')"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Tiếp nhận gói tin socket\nvà xác thực phiên chat"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Lưu tin nhắn vào CSDL\n& đẩy sang Admin Chat"},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Nhân viên CSKH đọc tin\nvà nhập nội dung trả lời"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Broadcast sự kiện realtime\nvề kênh của Khách hàng"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Render tin nhắn phản hồi\nlên khung chat client"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Đọc câu trả lời và tiếp\ntục trao đổi hỗ trợ"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 400, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "db2"},
                {"src": "db2", "tgt": "be2"},
                {"src": "be2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 15. BÁO CÁO TÀI CHÍNH & HOÀN TIỀN (LAB 9)
        # =========================================================================
        {
            "title": "15. Báo cáo Tài chính & Hoàn tiền (Lab 9)",
            "lanes": ["Quản trị viên", "Giao diện Admin", "Hệ thống xử lý", "CSDL & Cổng MoMo"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 78, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Mở trang Quản trị\nTài chính (Finance)"},
                {"id": "ui1", "lane": 1, "type": "action", "x": 22, "y": 100, "w": 140, "h": 45, "text": "Gửi request tổng hợp số\nliệu doanh thu theo kỳ"},
                {"id": "be1", "lane": 2, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Tiếp nhận & thực hiện\ntính toán thống kê"},
                {"id": "db1", "lane": 3, "type": "action", "x": 22, "y": 175, "w": 140, "h": 45, "text": "Tổng hợp doanh thu thực &\nbảng đối soát MoMo/COD"},
                {"id": "ui2", "lane": 1, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Hiển thị 4 thẻ KPI,\nSpline Chart & Giao dịch"},
                {"id": "u2", "lane": 0, "type": "action", "x": 22, "y": 250, "w": 140, "h": 45, "text": "Chọn đơn cần hoàn tiền\nvà bấm Duyệt hoàn tiền"},
                {"id": "ui3", "lane": 1, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Gửi yêu cầu hoàn tiền\ncho đơn hàng"},
                {"id": "be2", "lane": 2, "type": "action", "x": 22, "y": 325, "w": 140, "h": 45, "text": "Kiểm tra ràng buộc\nState Machine hoàn tiền"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 27, "y": 400, "w": 130, "h": 50, "text": "Hợp lệ chu trình?"},
                {"id": "ui_err", "lane": 1, "type": "action", "x": 22, "y": 403, "w": 140, "h": 45, "text": "Báo lỗi đơn hàng không\nđủ điều kiện hoàn tiền"},
                {"id": "err1", "lane": 1, "type": "end", "x": 78, "y": 470, "w": 28, "h": 28},
                {"id": "db2", "lane": 3, "type": "action", "x": 22, "y": 475, "w": 140, "h": 45, "text": "Gọi MoMo Refund API &\ncập nhật trạng thái refunded"},
                {"id": "be3", "lane": 2, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Trừ doanh thu thực tế &\nghi log đối soát"},
                {"id": "ui4", "lane": 1, "type": "action", "x": 22, "y": 550, "w": 140, "h": 45, "text": "Thông báo hoàn tất &\ncập nhật lại biểu đồ"},
                {"id": "u3", "lane": 0, "type": "action", "x": 22, "y": 625, "w": 140, "h": 45, "text": "Nhận thông báo đối soát\nhoàn tất thành công"},
                {"id": "end", "lane": 0, "type": "end", "x": 78, "y": 700, "w": 30, "h": 30}
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

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T21:25:00.000Z", agent="Striker 4-Lane Architecture V7", version="21.0.0", type="device")
    os.makedirs('docs/drawio_xml', exist_ok=True)

    for diag_idx, diag in enumerate(diagrams):
        max_y = max([node["y"] for node in diag["nodes"]]) + 80
        pool_h = max(600, max_y)

        diagram = ET.SubElement(mxfile, "diagram", name=diag["title"], id=f"v7_diag_{diag_idx+1}")
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="700", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(pool_w + 100), pageHeight=str(pool_h + 100), math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        # Pool
        pool_id = f"pool_{diag_idx+1}"
        pool_cell = ET.SubElement(root, "mxCell", id=pool_id, value=diag["title"], style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=26;horizontal=1;horizontalStack=1;whiteSpace=wrap;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;fontFamily=Helvetica;", vertex="1", parent="1")
        ET.SubElement(pool_cell, "mxGeometry", x="40", y="40", width=str(pool_w), height=str(pool_h), as_="geometry")

        lane_ids = []
        for l_idx, l_name in enumerate(diag["lanes"]):
            l_id = f"lane_{diag_idx+1}_{l_idx}"
            lane_ids.append(l_id)
            l_cell = ET.SubElement(root, "mxCell", id=l_id, value=l_name, style="swimlane;html=1;startSize=28;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;fontFamily=Helvetica;align=center;", vertex="1", parent=pool_id)
            ET.SubElement(l_cell, "mxGeometry", x=str(l_idx * lane_w), y="26", width=str(lane_w), height=str(pool_h - 26), as_="geometry")

        node_map = {}
        for n in diag["nodes"]:
            n_id = f"node_{diag_idx+1}_{n['id']}"
            node_map[n["id"]] = n_id
            parent_lane = lane_ids[n["lane"]]
            
            w = n.get("w", 140)
            h = n.get("h", 45)
            
            if n["type"] == "start":
                style = style_start
            elif n["type"] == "end":
                style = style_end
            elif n["type"] == "decision":
                style = style_dec
            else: # action
                style = style_action

            n_cell = ET.SubElement(root, "mxCell", id=n_id, value=n.get("text", ""), style=style, vertex="1", parent=parent_lane)
            ET.SubElement(n_cell, "mxGeometry", x=str(n["x"]), y=str(n["y"]), width=str(w), height=str(h), as_="geometry")

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
    print("SUCCESS: Generated all 15 diagrams in full 4-Lane Standard UML Architecture!")

if __name__ == "__main__":
    build_4lane_diagrams()
