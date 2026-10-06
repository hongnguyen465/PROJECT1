import os
import xml.etree.ElementTree as ET

def build_flawless_2lane_diagrams():
    diagrams = [
        # =========================================================================
        # 1. ĐĂNG KÝ TÀI KHOẢN VÀ XÁC THỰC OTP
        # =========================================================================
        {
            "title": "1. Đăng ký tài khoản và Xác thực OTP",
            "lane1_title": "Người dùng",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 760,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Chọn chức năng\nđăng ký tài khoản"},
                {"id": "s_show", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Hiển thị biểu mẫu\nđăng ký tài khoản"},
                {"id": "u_input", "lane": 0, "type": "action", "x": 55, "y": 180, "w": 170, "h": 45, "text": "Nhập Họ tên, Email,\nSĐT và Mật khẩu"},
                {"id": "u_click", "lane": 0, "type": "action", "x": 55, "y": 260, "w": 170, "h": 45, "text": "Nhấn nút Đăng ký"},
                {"id": "s_dec1", "lane": 1, "type": "decision", "x": 45, "y": 255, "w": 150, "h": 55, "text": "Kiểm tra thông tin\nvà trùng lặp?"},
                {"id": "s_err1", "lane": 1, "type": "action", "x": 230, "y": 260, "w": 130, "h": 45, "text": "Hiển thị thông báo lỗi\n(Sai định dạng / Đã tồn tại)"},
                {"id": "s_otp", "lane": 1, "type": "action", "x": 40, "y": 350, "w": 160, "h": 45, "text": "Tạo tài khoản pending\nvà gửi mã OTP qua Email"},
                {"id": "u_enter_otp", "lane": 0, "type": "action", "x": 55, "y": 430, "w": 170, "h": 45, "text": "Nhập mã OTP từ Email\nvà nhấn Xác thực"},
                {"id": "s_dec2", "lane": 1, "type": "decision", "x": 45, "y": 425, "w": 150, "h": 55, "text": "Kiểm tra\nmã OTP?"},
                {"id": "s_err2", "lane": 1, "type": "action", "x": 230, "y": 430, "w": 130, "h": 45, "text": "Thông báo sai mã OTP\nhoặc mã hết hạn"},
                {"id": "s_ok", "lane": 1, "type": "action", "x": 40, "y": 520, "w": 160, "h": 45, "text": "Kích hoạt tài khoản active,\ncấp Token & Đăng nhập"},
                {"id": "end", "lane": 1, "type": "end", "x": 105, "y": 610, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "s_show", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_show", "tgt": "u_input", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_input", "tgt": "u_click", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_click", "tgt": "s_dec1", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec1", "tgt": "s_err1", "label": "Không hợp lệ", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_err1", "tgt": "s_show", "pts": "exitX=0.5;exitY=0;entryX=1;entryY=0.5;"},
                {"src": "s_dec1", "tgt": "s_otp", "label": "Hợp lệ", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_otp", "tgt": "u_enter_otp", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_enter_otp", "tgt": "s_dec2", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec2", "tgt": "s_err2", "label": "Sai mã", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_err2", "tgt": "s_otp", "pts": "exitX=0.5;exitY=0;entryX=1;entryY=0.5;"},
                {"src": "s_dec2", "tgt": "s_ok", "label": "Đúng mã", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_ok", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}
            ]
        },

        # =========================================================================
        # 2. ĐĂNG NHẬP HỆ THỐNG
        # =========================================================================
        {
            "title": "2. Đăng nhập hệ thống",
            "lane1_title": "Người dùng",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 680,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Chọn chức năng\nđăng nhập"},
                {"id": "s_show", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Hiển thị biểu mẫu\nđăng nhập"},
                {"id": "u_input", "lane": 0, "type": "action", "x": 55, "y": 180, "w": 170, "h": 45, "text": "Nhập Email / SĐT\nvà Mật khẩu"},
                {"id": "u_click", "lane": 0, "type": "action", "x": 55, "y": 260, "w": 170, "h": 45, "text": "Nhấn nút Đăng nhập"},
                {"id": "s_dec1", "lane": 1, "type": "decision", "x": 45, "y": 255, "w": 150, "h": 55, "text": "Kiểm tra\nthông tin?"},
                {"id": "s_err1", "lane": 1, "type": "action", "x": 230, "y": 260, "w": 130, "h": 45, "text": "Hiển thị thông báo lỗi\nsai tài khoản / mật khẩu"},
                {"id": "s_dec2", "lane": 1, "type": "decision", "x": 45, "y": 350, "w": 150, "h": 55, "text": "Trạng thái\ntài khoản?"},
                {"id": "s_err2", "lane": 1, "type": "action", "x": 230, "y": 355, "w": 130, "h": 45, "text": "Thông báo tài khoản\nđã bị khóa"},
                {"id": "s_ok", "lane": 1, "type": "action", "x": 40, "y": 450, "w": 160, "h": 45, "text": "Cấp Bearer JWT Token\nvà đăng nhập thành công"},
                {"id": "end", "lane": 1, "type": "end", "x": 105, "y": 540, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "s_show", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_show", "tgt": "u_input", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_input", "tgt": "u_click", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_click", "tgt": "s_dec1", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec1", "tgt": "s_err1", "label": "Sai thông tin", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_err1", "tgt": "s_show", "pts": "exitX=0.5;exitY=0;entryX=1;entryY=0.5;"},
                {"src": "s_dec1", "tgt": "s_dec2", "label": "Đúng mật khẩu", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_dec2", "tgt": "s_err2", "label": "Locked", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_err2", "tgt": "s_show", "pts": "exitX=0.5;exitY=0;entryX=1;entryY=0.75;"},
                {"src": "s_dec2", "tgt": "s_ok", "label": "Active", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_ok", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}
            ]
        },

        # =========================================================================
        # 3. QUẢN LÝ KHÁCH HÀNG (KHÓA / MỞ KHÓA)
        # =========================================================================
        {
            "title": "3. Quản lý khách hàng",
            "lane1_title": "Admin",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 620,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Mở chức năng\nQuản lý khách hàng"},
                {"id": "s_get", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Truy vấn và hiển thị\ndanh sách khách hàng"},
                {"id": "u_select", "lane": 0, "type": "action", "x": 55, "y": 180, "w": 170, "h": 45, "text": "Chọn một khách hàng\ntrong danh sách"},
                {"id": "u_dec", "lane": 0, "type": "decision", "x": 70, "y": 255, "w": 140, "h": 55, "text": "Chọn\nthao tác?"},
                {"id": "s_lock", "lane": 1, "type": "action", "x": 40, "y": 260, "w": 160, "h": 45, "text": "Cập nhật trạng thái\ntài khoản thành locked"},
                {"id": "s_unlock", "lane": 1, "type": "action", "x": 220, "y": 260, "w": 140, "h": 45, "text": "Cập nhật trạng thái\ntài khoản thành active"},
                {"id": "s_refresh", "lane": 1, "type": "action", "x": 110, "y": 360, "w": 160, "h": 45, "text": "Thông báo thành công\nvà làm mới danh sách"},
                {"id": "end", "lane": 1, "type": "end", "x": 175, "y": 450, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "s_get", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_get", "tgt": "u_select", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_select", "tgt": "u_dec", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_dec", "tgt": "s_lock", "label": "Khóa tài khoản", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "u_dec", "tgt": "s_unlock", "label": "Mở khóa", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_lock", "tgt": "s_refresh", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_unlock", "tgt": "s_refresh", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"},
                {"src": "s_refresh", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}
            ]
        },

        # =========================================================================
        # 4. DUYỆT VÀ TÌM KIẾM SẢN PHẨM
        # =========================================================================
        {
            "title": "4. Duyệt và Tìm kiếm sản phẩm",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 580,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Truy cập trang Cửa hàng"},
                {"id": "s_load", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Tải Banner quảng cáo\nvà danh mục nổi bật"},
                {"id": "u_dec", "lane": 0, "type": "decision", "x": 70, "y": 185, "w": 140, "h": 55, "text": "Chọn hình thức\nduyệt hàng?"},
                {"id": "s_search", "lane": 1, "type": "action", "x": 40, "y": 190, "w": 150, "h": 45, "text": "Tìm theo từ khóa\ntên sản phẩm, SKU"},
                {"id": "s_filter", "lane": 1, "type": "action", "x": 210, "y": 190, "w": 150, "h": 45, "text": "Lọc theo giá, brand,\ntag HOT / NEW"},
                {"id": "s_show", "lane": 1, "type": "action", "x": 120, "y": 290, "w": 160, "h": 45, "text": "Hiển thị danh sách\nsản phẩm phù hợp"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 380, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "s_load", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_load", "tgt": "u_dec", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_dec", "tgt": "s_search", "label": "Tìm kiếm", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "u_dec", "tgt": "s_filter", "label": "Bộ lọc/Danh mục", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_search", "tgt": "s_show", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_filter", "tgt": "s_show", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"},
                {"src": "s_show", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}
            ]
        },

        # =========================================================================
        # 5. XEM CHI TIẾT & TỒN KHO SKU
        # =========================================================================
        {
            "title": "5. Xem chi tiết & Tồn kho SKU",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 540,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_select", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Chọn xem chi tiết\nmột sản phẩm"},
                {"id": "s_get", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Truy vấn thông tin\nsản phẩm và các SKU"},
                {"id": "u_pick", "lane": 0, "type": "action", "x": 55, "y": 180, "w": 170, "h": 45, "text": "Chọn Màu sắc và\nKích thước (SKU)"},
                {"id": "s_dec", "lane": 1, "type": "decision", "x": 45, "y": 175, "w": 150, "h": 55, "text": "Kiểm tra\ntồn kho SKU?"},
                {"id": "s_in", "lane": 1, "type": "action", "x": 40, "y": 270, "w": 160, "h": 45, "text": "Hiển thị Còn hàng\nvà mở nút Thêm giỏ"},
                {"id": "s_out", "lane": 1, "type": "action", "x": 220, "y": 270, "w": 140, "h": 45, "text": "Hiển thị Hết hàng\nvà khóa nút Thêm giỏ"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 360, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_select", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_select", "tgt": "s_get", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_get", "tgt": "u_pick", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_pick", "tgt": "s_dec", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec", "tgt": "s_in", "label": "Còn hàng", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_dec", "tgt": "s_out", "label": "Hết hàng", "pts": "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"},
                {"src": "s_in", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_out", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"}
            ]
        },

        # =========================================================================
        # 6. QUẢN TRỊ CATALOG SẢN PHẨM
        # =========================================================================
        {
            "title": "6. Quản trị Catalog sản phẩm",
            "lane1_title": "Admin",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 600,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Mở trang Quản trị Catalog"},
                {"id": "u_dec", "lane": 0, "type": "decision", "x": 70, "y": 180, "w": 140, "h": 55, "text": "Chọn phân hệ\nquản lý?"},
                {"id": "s_prod", "lane": 1, "type": "action", "x": 40, "y": 185, "w": 150, "h": 45, "text": "Thêm/Sửa/Xóa mềm\nsản phẩm & SKU"},
                {"id": "s_cat", "lane": 1, "type": "action", "x": 210, "y": 185, "w": 150, "h": 45, "text": "Thêm/Sửa/Xóa\ndanh mục & Banner"},
                {"id": "s_save", "lane": 1, "type": "action", "x": 120, "y": 280, "w": 160, "h": 45, "text": "Lưu thay đổi CSDL\nvà thông báo thành công"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 370, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "u_dec", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_dec", "tgt": "s_prod", "label": "Sản phẩm/SKU", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "u_dec", "tgt": "s_cat", "label": "Danh mục/Banner", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_prod", "tgt": "s_save", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_cat", "tgt": "s_save", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"},
                {"src": "s_save", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}
            ]
        },

        # =========================================================================
        # 7. QUẢN LÝ GIỎ HÀNG
        # =========================================================================
        {
            "title": "7. Quản lý giỏ hàng",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 660,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_add", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Chọn SKU & Số lượng\n-> Thêm vào giỏ"},
                {"id": "s_dec1", "lane": 1, "type": "decision", "x": 45, "y": 95, "w": 150, "h": 55, "text": "Kiểm tra\ntồn kho SKU?"},
                {"id": "s_err1", "lane": 1, "type": "action", "x": 230, "y": 100, "w": 130, "h": 45, "text": "Báo lỗi không đủ\nsố lượng tồn kho"},
                {"id": "s_add_ok", "lane": 1, "type": "action", "x": 40, "y": 190, "w": 160, "h": 45, "text": "Thêm vào giỏ hàng\nvà tính lại tổng tiền"},
                {"id": "u_open_cart", "lane": 0, "type": "action", "x": 55, "y": 270, "w": 170, "h": 45, "text": "Mở Giỏ hàng (Drawer)"},
                {"id": "u_dec2", "lane": 0, "type": "decision", "x": 70, "y": 355, "w": 140, "h": 55, "text": "Chọn thao tác\ntrên giỏ?"},
                {"id": "s_update", "lane": 1, "type": "action", "x": 40, "y": 360, "w": 150, "h": 45, "text": "Cập nhật SL / Xóa món\nvà tính lại tổng tiền"},
                {"id": "s_checkout", "lane": 1, "type": "action", "x": 210, "y": 360, "w": 150, "h": 45, "text": "Chuyển hướng sang\ntrang Thanh toán"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 450, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_add", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_add", "tgt": "s_dec1", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec1", "tgt": "s_err1", "label": "Không đủ", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec1", "tgt": "s_add_ok", "label": "Đủ hàng", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_add_ok", "tgt": "u_open_cart", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_open_cart", "tgt": "u_dec2", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_dec2", "tgt": "s_update", "label": "Sửa/Xóa món", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "u_dec2", "tgt": "s_checkout", "label": "Thanh toán", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_update", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_checkout", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"},
                {"src": "s_err1", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"}
            ]
        },

        # =========================================================================
        # 8. CHECKOUT VÀ TẠO ĐƠN HÀNG
        # =========================================================================
        {
            "title": "8. Checkout và Tạo đơn hàng",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống & GHN",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 680,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Mở trang Checkout &\nchọn địa chỉ nhận hàng"},
                {"id": "s_ghn", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "GHN tính cước phí\nvận chuyển động"},
                {"id": "s_dec1", "lane": 1, "type": "decision", "x": 45, "y": 180, "w": 150, "h": 55, "text": "Kiểm tra tồn kho\ntoàn bộ giỏ?"},
                {"id": "s_err1", "lane": 1, "type": "action", "x": 230, "y": 185, "w": 130, "h": 45, "text": "Báo hết hàng và\ndừng Checkout"},
                {"id": "u_vouch", "lane": 0, "type": "action", "x": 55, "y": 270, "w": 170, "h": 45, "text": "Nhập mã Voucher\ngiảm giá (nếu có)"},
                {"id": "s_calc", "lane": 1, "type": "action", "x": 40, "y": 270, "w": 160, "h": 45, "text": "Tính Tổng thanh toán =\nTiền hàng + Ship - Giảm giá"},
                {"id": "u_confirm", "lane": 0, "type": "action", "x": 55, "y": 360, "w": 170, "h": 45, "text": "Nhấn nút Xác nhận Đặt hàng"},
                {"id": "s_create", "lane": 1, "type": "action", "x": 40, "y": 360, "w": 160, "h": 45, "text": "Tạo đơn hàng pending &\nxóa giỏ hàng"},
                {"id": "end", "lane": 1, "type": "end", "x": 105, "y": 450, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "s_ghn", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_ghn", "tgt": "s_dec1", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_dec1", "tgt": "s_err1", "label": "Hết hàng", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec1", "tgt": "u_vouch", "label": "Đủ hàng", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_vouch", "tgt": "s_calc", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_calc", "tgt": "u_confirm", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_confirm", "tgt": "s_create", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_create", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_err1", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=1;entryY=0.5;"}
            ]
        },

        # =========================================================================
        # 9. THANH TOÁN COD
        # =========================================================================
        {
            "title": "9. Thanh toán COD",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống & Admin",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 620,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_cod", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Chọn phương thức COD\nvà nhấn Xác nhận"},
                {"id": "s_rec", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Ghi nhận COD &\nđặt payment_status = pending"},
                {"id": "s_pack", "lane": 1, "type": "action", "x": 40, "y": 180, "w": 160, "h": 45, "text": "Đóng gói & bàn giao\nđơn vị vận chuyển"},
                {"id": "u_pay", "lane": 0, "type": "action", "x": 55, "y": 260, "w": 170, "h": 45, "text": "Nhận kiện hàng và\nthanh toán tiền mặt cho shipper"},
                {"id": "s_dec", "lane": 1, "type": "decision", "x": 45, "y": 255, "w": 150, "h": 55, "text": "Giao hàng và\nthu tiền COD?"},
                {"id": "s_ok", "lane": 1, "type": "action", "x": 40, "y": 350, "w": 160, "h": 45, "text": "Cập nhật payment_status = paid\nvà order_status = delivered"},
                {"id": "s_fail", "lane": 1, "type": "action", "x": 220, "y": 350, "w": 140, "h": 45, "text": "Cập nhật đơn thất bại / hoàn trả"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 440, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_cod", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_cod", "tgt": "s_rec", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_rec", "tgt": "s_pack", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_pack", "tgt": "u_pay", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_pay", "tgt": "s_dec", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec", "tgt": "s_ok", "label": "Thành công", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_dec", "tgt": "s_fail", "label": "Thất bại", "pts": "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"},
                {"src": "s_ok", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_fail", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"}
            ]
        },

        # =========================================================================
        # 10. THANH TOÁN MOMO SANDBOX
        # =========================================================================
        {
            "title": "10. Thanh toán MoMo Sandbox",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống & Cổng MoMo",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 620,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_momo", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Chọn thanh toán Ví MoMo\nvà Xác nhận"},
                {"id": "s_init", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Ký số HMAC-SHA256 &\ntạo mã QR / PayUrl"},
                {"id": "u_scan", "lane": 0, "type": "action", "x": 55, "y": 180, "w": 170, "h": 45, "text": "Quét mã QR và xác nhận\nthanh toán trên App MoMo"},
                {"id": "s_dec", "lane": 1, "type": "decision", "x": 45, "y": 175, "w": 150, "h": 55, "text": "Xác thực IPN\n& Kết quả MoMo?"},
                {"id": "s_ok", "lane": 1, "type": "action", "x": 40, "y": 270, "w": 160, "h": 45, "text": "Cập nhật payment_status = paid\nvà thông báo thành công"},
                {"id": "s_fail", "lane": 1, "type": "action", "x": 220, "y": 270, "w": 140, "h": 45, "text": "Cập nhật trạng thái failed\nvà thông báo thất bại"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 360, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_momo", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_momo", "tgt": "s_init", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_init", "tgt": "u_scan", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_scan", "tgt": "s_dec", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec", "tgt": "s_ok", "label": "Thành công", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_dec", "tgt": "s_fail", "label": "Thất bại", "pts": "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"},
                {"src": "s_ok", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_fail", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"}
            ]
        },

        # =========================================================================
        # 11. THEO DÕI & HỦY ĐƠN HÀNG
        # =========================================================================
        {
            "title": "11. Theo dõi & Hủy đơn hàng",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 540,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Mở trang Đơn hàng của tôi\nvà chọn xem chi tiết"},
                {"id": "s_dec", "lane": 1, "type": "decision", "x": 45, "y": 95, "w": 150, "h": 55, "text": "Trạng thái\nđơn hàng?"},
                {"id": "s_track", "lane": 1, "type": "action", "x": 40, "y": 190, "w": 160, "h": 45, "text": "Hiển thị mã vận đơn &\ntra cứu lộ trình GHN"},
                {"id": "u_cancel", "lane": 0, "type": "action", "x": 55, "y": 190, "w": 170, "h": 45, "text": "Nhấn nút Hủy đơn hàng &\nxác nhận hủy"},
                {"id": "s_cancel", "lane": 1, "type": "action", "x": 220, "y": 190, "w": 140, "h": 45, "text": "Cập nhật order = cancelled &\nhoàn trả lại tồn kho SKU"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 280, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "s_dec", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec", "tgt": "s_track", "label": "shipping", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_dec", "tgt": "u_cancel", "label": "pending", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_cancel", "tgt": "s_cancel", "pts": "exitX=1;exitY=0.75;entryX=0;entryY=0.75;"},
                {"src": "s_track", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_cancel", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"}
            ]
        },

        # =========================================================================
        # 12. ĐÁNH GIÁ SẢN PHẨM
        # =========================================================================
        {
            "title": "12. Đánh giá sản phẩm",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 600,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_pick", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Chọn sản phẩm trong\nđơn hàng đã mua"},
                {"id": "s_dec", "lane": 1, "type": "decision", "x": 45, "y": 95, "w": 150, "h": 55, "text": "Đơn đã delivered\n& chưa đánh giá?"},
                {"id": "s_err", "lane": 1, "type": "action", "x": 230, "y": 100, "w": 130, "h": 45, "text": "Báo chưa đủ điều kiện\nhoặc đã đánh giá"},
                {"id": "u_review", "lane": 0, "type": "action", "x": 55, "y": 190, "w": 170, "h": 45, "text": "Chọn số sao (1-5 sao),\nnhập nhận xét & Gửi"},
                {"id": "s_save", "lane": 1, "type": "action", "x": 40, "y": 190, "w": 160, "h": 45, "text": "Lưu đánh giá & tính lại\nđiểm sao trung bình"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 280, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_pick", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_pick", "tgt": "s_dec", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec", "tgt": "s_err", "label": "Không đủ ĐK", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec", "tgt": "u_review", "label": "Đủ ĐK", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_review", "tgt": "s_save", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_save", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_err", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"}
            ]
        },

        # =========================================================================
        # 13. QUẢN TRỊ ĐƠN HÀNG & GHN
        # =========================================================================
        {
            "title": "13. Quản trị Đơn hàng & GHN",
            "lane1_title": "Admin",
            "lane2_title": "Hệ thống & GHN",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 600,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Mở Quản lý đơn hàng &\nchọn một đơn hàng"},
                {"id": "u_dec", "lane": 0, "type": "decision", "x": 70, "y": 180, "w": 140, "h": 55, "text": "Chọn thao tác\nquản trị?"},
                {"id": "s_ghn", "lane": 1, "type": "action", "x": 40, "y": 185, "w": 150, "h": 45, "text": "Tạo vận đơn GHN 1-Click\n& Cập nhật shipping"},
                {"id": "s_cod", "lane": 1, "type": "action", "x": 210, "y": 185, "w": 150, "h": 45, "text": "Xác nhận thu tiền COD ->\npayment_status = paid"},
                {"id": "s_save", "lane": 1, "type": "action", "x": 120, "y": 280, "w": 160, "h": 45, "text": "Thông báo thành công và\nlàm mới thông tin đơn"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 370, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "u_dec", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_dec", "tgt": "s_ghn", "label": "Tạo đơn GHN", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "u_dec", "tgt": "s_cod", "label": "Thu tiền COD", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_ghn", "tgt": "s_save", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_cod", "tgt": "s_save", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"},
                {"src": "s_save", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}
            ]
        },

        # =========================================================================
        # 14. TƯ VẤN TRỰC TUYẾN LIVECHAT (LAB 7)
        # =========================================================================
        {
            "title": "14. Tư vấn trực tuyến LiveChat (Lab 7)",
            "lane1_title": "Khách hàng",
            "lane2_title": "Hệ thống & CSKH",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 540,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_msg", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Mở ChatWidget tại cửa hàng\nvà gửi câu hỏi tư vấn"},
                {"id": "s_save_msg", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Lưu tin nhắn vào CSDL\nvà báo cho Admin CSKH"},
                {"id": "s_reply", "lane": 1, "type": "action", "x": 40, "y": 180, "w": 160, "h": 45, "text": "Admin CSKH nhập phản hồi\nvà gửi giải đáp"},
                {"id": "u_recv", "lane": 0, "type": "action", "x": 55, "y": 260, "w": 170, "h": 45, "text": "Khách hàng nhận được\ntin nhắn tư vấn giải đáp"},
                {"id": "end", "lane": 0, "type": "end", "x": 125, "y": 350, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_msg", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_msg", "tgt": "s_save_msg", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_save_msg", "tgt": "s_reply", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_reply", "tgt": "u_recv", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_recv", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"}
            ]
        },

        # =========================================================================
        # 15. BÁO CÁO TÀI CHÍNH & HOÀN TIỀN (LAB 9)
        # =========================================================================
        {
            "title": "15. Báo cáo Tài chính & Hoàn tiền (Lab 9)",
            "lane1_title": "Admin",
            "lane2_title": "Hệ thống",
            "lane1_w": 280,
            "lane2_w": 380,
            "pool_h": 580,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 125, "y": 40, "w": 30, "h": 30},
                {"id": "u_open", "lane": 0, "type": "action", "x": 55, "y": 100, "w": 170, "h": 45, "text": "Mở trang Quản trị\nTài chính (Finance)"},
                {"id": "s_calc", "lane": 1, "type": "action", "x": 40, "y": 100, "w": 160, "h": 45, "text": "Tổng hợp doanh thu thực &\nbảng đối soát MoMo/COD"},
                {"id": "u_req", "lane": 0, "type": "action", "x": 55, "y": 180, "w": 170, "h": 45, "text": "Chọn đơn hàng cần hoàn tiền\nvà chuyển sang refunded"},
                {"id": "s_dec", "lane": 1, "type": "decision", "x": 45, "y": 175, "w": 150, "h": 55, "text": "Kiểm tra ràng buộc\nState Machine?"},
                {"id": "s_ok", "lane": 1, "type": "action", "x": 40, "y": 270, "w": 160, "h": 45, "text": "Cập nhật refunded &\ntrừ lại doanh thu thực"},
                {"id": "s_err", "lane": 1, "type": "action", "x": 220, "y": 270, "w": 140, "h": 45, "text": "Báo lỗi vi phạm quy tắc\nchu trình State Machine"},
                {"id": "end", "lane": 1, "type": "end", "x": 185, "y": 360, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u_open", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "u_open", "tgt": "s_calc", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_calc", "tgt": "u_req", "pts": "exitX=0;exitY=0.75;entryX=1;entryY=0.25;"},
                {"src": "u_req", "tgt": "s_dec", "pts": "exitX=1;exitY=0.5;entryX=0;entryY=0.5;"},
                {"src": "s_dec", "tgt": "s_ok", "label": "Hợp lệ", "pts": "exitX=0.5;exitY=1;entryX=0.5;entryY=0;"},
                {"src": "s_dec", "tgt": "s_err", "label": "Không hợp lệ", "pts": "exitX=1;exitY=0.5;entryX=0.5;entryY=0;"},
                {"src": "s_ok", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.25;entryY=0;"},
                {"src": "s_err", "tgt": "end", "pts": "exitX=0.5;exitY=1;entryX=0.75;entryY=0;"}
            ]
        }
    ]

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T21:18:00.000Z", agent="Striker Flawless 2-Lane V5", version="21.0.0", type="device")
    os.makedirs('docs/drawio_xml', exist_ok=True)

    for diag_idx, diag in enumerate(diagrams):
        diagram = ET.SubElement(mxfile, "diagram", name=diag["title"], id=f"flawless_diag_{diag_idx+1}")
        lane1_w = diag["lane1_w"]
        lane2_w = diag["lane2_w"]
        pool_w = lane1_w + lane2_w
        pool_h = diag["pool_h"]

        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="700", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(pool_w + 100), pageHeight=str(pool_h + 100), math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        # Pool
        pool_id = f"pool_{diag_idx+1}"
        pool_cell = ET.SubElement(root, "mxCell", id=pool_id, value=diag["title"], style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=26;horizontal=1;horizontalStack=1;whiteSpace=wrap;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;fontFamily=Helvetica;", vertex="1", parent="1")
        ET.SubElement(pool_cell, "mxGeometry", x="40", y="40", width=str(pool_w), height=str(pool_h), as_="geometry")

        # Lane 1
        lane1_id = f"lane_{diag_idx+1}_0"
        lane1_cell = ET.SubElement(root, "mxCell", id=lane1_id, value=diag["lane1_title"], style="swimlane;html=1;startSize=28;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;fontFamily=Helvetica;align=center;", vertex="1", parent=pool_id)
        ET.SubElement(lane1_cell, "mxGeometry", x="0", y="26", width=str(lane1_w), height=str(pool_h - 26), as_="geometry")

        # Lane 2
        lane2_id = f"lane_{diag_idx+1}_1"
        lane2_cell = ET.SubElement(root, "mxCell", id=lane2_id, value=diag["lane2_title"], style="swimlane;html=1;startSize=28;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;fontFamily=Helvetica;align=center;", vertex="1", parent=pool_id)
        ET.SubElement(lane2_cell, "mxGeometry", x=str(lane1_w), y="26", width=str(lane2_w), height=str(pool_h - 26), as_="geometry")

        lane_ids = [lane1_id, lane2_id]
        node_map = {}

        for n in diag["nodes"]:
            n_id = f"node_{diag_idx+1}_{n['id']}"
            node_map[n["id"]] = n_id
            parent_lane = lane_ids[n["lane"]]
            
            w = n.get("w", 160)
            h = n.get("h", 45)
            
            if n["type"] == "start":
                style = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#b85450;"
            elif n["type"] == "end":
                style = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#b85450;"
            elif n["type"] == "decision":
                style = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
            else: # action
                style = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"

            n_cell = ET.SubElement(root, "mxCell", id=n_id, value=n.get("text", ""), style=style, vertex="1", parent=parent_lane)
            ET.SubElement(n_cell, "mxGeometry", x=str(n["x"]), y=str(n["y"]), width=str(w), height=str(h), as_="geometry")

        for e_idx, e in enumerate(diag["edges"]):
            e_id = f"edge_{diag_idx+1}_{e_idx}"
            src = node_map[e["src"]]
            tgt = node_map[e["tgt"]]
            lbl = e.get("label", "")
            pts = e.get("pts", "")
            
            e_style = f"edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;strokeWidth=1.5;endArrow=classic;fontSize=10;fontColor=#000000;fontFamily=Helvetica;{pts}"
            
            e_cell = ET.SubElement(root, "mxCell", id=e_id, value=lbl, style=e_style, edge="1", source=src, target=tgt, parent="1")
            ET.SubElement(e_cell, "mxGeometry", relative="1", as_="geometry")

        # Export individual XML
        xml_str = ET.tostring(mxGraphModel, encoding='unicode')
        with open(f"docs/drawio_xml/So_do_{diag_idx+1}.xml", "w", encoding="utf-8") as f:
            f.write(xml_str)

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write("docs/striker_activity_diagrams.drawio", encoding="utf-8", xml_declaration=True)
    print("ALL 15 DIAGRAMS GENERATED WITH 2-LANE FLAWLESS ZERO-OVERLAP LAYOUT!")

build_flawless_2lane_diagrams()
