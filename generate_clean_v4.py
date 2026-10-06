import os
import xml.etree.ElementTree as ET

def generate_perfect_activity_diagrams():
    diagrams = [
        # --- 1. ĐĂNG KÝ VÀ XÁC THỰC OTP ---
        {
            "title": "1. Đăng ký tài khoản và Xác thực OTP",
            "lanes": ["Người dùng", "Giao diện (Frontend)", "Dịch vụ Hệ thống"],
            "lane_w": 240,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_reg", "lane": 0, "type": "action", "y": 100, "text": "Chọn chức năng\nđăng ký tài khoản"},
                {"id": "show_form", "lane": 1, "type": "action", "y": 100, "text": "Hiển thị biểu mẫu\nđăng ký tài khoản"},
                {"id": "input_info", "lane": 0, "type": "action", "y": 170, "text": "Nhập Họ tên, Email,\nSĐT và Mật khẩu"},
                {"id": "click_reg", "lane": 0, "type": "action", "y": 240, "text": "Nhấn nút Đăng ký"},
                {"id": "check_form", "lane": 1, "type": "decision", "y": 305, "text": "Kiểm tra\nbiểu mẫu?"},
                {"id": "err_format", "lane": 1, "type": "action", "y": 380, "text": "Báo lỗi định dạng\n(Thiếu / Sai thông tin)"},
                {"id": "check_exist", "lane": 2, "type": "decision", "y": 375, "text": "Kiểm tra\ntrùng lặp?"},
                {"id": "err_exist", "lane": 1, "type": "action", "y": 450, "text": "Báo Email hoặc SĐT\nđã được đăng ký"},
                {"id": "send_otp", "lane": 2, "type": "action", "y": 450, "text": "Tạo tài khoản pending\nvà gửi mã OTP qua Email"},
                {"id": "show_otp_ui", "lane": 1, "type": "action", "y": 520, "text": "Hiển thị màn hình\nnhập mã OTP"},
                {"id": "input_otp", "lane": 0, "type": "action", "y": 590, "text": "Nhập mã OTP từ Email\nvà nhấn Xác thực"},
                {"id": "check_otp", "lane": 2, "type": "decision", "y": 655, "text": "Kiểm tra\nmã OTP?"},
                {"id": "err_otp", "lane": 1, "type": "action", "y": 725, "text": "Báo sai mã OTP\nhoặc mã đã hết hạn"},
                {"id": "activate", "lane": 2, "type": "action", "y": 725, "text": "Kích hoạt tài khoản active\nvà cấp JWT Token"},
                {"id": "success_login", "lane": 1, "type": "action", "y": 795, "text": "Thông báo thành công\nvà tự động đăng nhập"},
                {"id": "end_success", "lane": 1, "type": "end", "y": 870},
                {"id": "end_err1", "lane": 1, "type": "end", "y": 415, "w": 24, "h": 24, "x_offset": 80},
                {"id": "end_err2", "lane": 1, "type": "end", "y": 485, "w": 24, "h": 24, "x_offset": 80},
                {"id": "end_err3", "lane": 1, "type": "end", "y": 760, "w": 24, "h": 24, "x_offset": 80}
            ],
            "edges": [
                {"src": "start", "tgt": "open_reg"},
                {"src": "open_reg", "tgt": "show_form"},
                {"src": "show_form", "tgt": "input_info"},
                {"src": "input_info", "tgt": "click_reg"},
                {"src": "click_reg", "tgt": "check_form"},
                {"src": "check_form", "tgt": "check_exist", "label": "Hợp lệ"},
                {"src": "check_form", "tgt": "err_format", "label": "Không hợp lệ"},
                {"src": "err_format", "tgt": "end_err1"},
                {"src": "check_exist", "tgt": "send_otp", "label": "Chưa tồn tại"},
                {"src": "check_exist", "tgt": "err_exist", "label": "Đã tồn tại"},
                {"src": "err_exist", "tgt": "end_err2"},
                {"src": "send_otp", "tgt": "show_otp_ui"},
                {"src": "show_otp_ui", "tgt": "input_otp"},
                {"src": "input_otp", "tgt": "check_otp"},
                {"src": "check_otp", "tgt": "activate", "label": "Chính xác"},
                {"src": "check_otp", "tgt": "err_otp", "label": "Sai mã"},
                {"src": "err_otp", "tgt": "end_err3"},
                {"src": "activate", "tgt": "success_login"},
                {"src": "success_login", "tgt": "end_success"}
            ]
        },

        # --- 2. ĐĂNG NHẬP HỆ THỐNG ---
        {
            "title": "2. Đăng nhập hệ thống",
            "lanes": ["Người dùng", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_login", "lane": 0, "type": "action", "y": 100, "text": "Chọn chức năng\nđăng nhập"},
                {"id": "show_login", "lane": 1, "type": "action", "y": 100, "text": "Hiển thị biểu mẫu\nđăng nhập"},
                {"id": "input_cred", "lane": 0, "type": "action", "y": 180, "text": "Nhập Email / SĐT\nvà Mật khẩu"},
                {"id": "click_login", "lane": 0, "type": "action", "y": 260, "text": "Nhấn nút Đăng nhập"},
                {"id": "check_auth", "lane": 1, "type": "decision", "y": 325, "text": "Kiểm tra\nthông tin?"},
                {"id": "err_auth", "lane": 1, "type": "action", "y": 400, "text": "Thông báo sai Email / SĐT\nhoặc mật khẩu"},
                {"id": "check_status", "lane": 1, "type": "decision", "y": 475, "text": "Trạng thái\ntài khoản?"},
                {"id": "err_locked", "lane": 1, "type": "action", "y": 550, "text": "Thông báo tài khoản\nđã bị khóa"},
                {"id": "login_ok", "lane": 1, "type": "action", "y": 625, "text": "Cấp Bearer JWT Token\nvà chuyển về Trang chủ"},
                {"id": "end_ok", "lane": 1, "type": "end", "y": 705},
                {"id": "end_err1", "lane": 1, "type": "end", "y": 435, "w": 24, "h": 24, "x_offset": 80},
                {"id": "end_err2", "lane": 1, "type": "end", "y": 585, "w": 24, "h": 24, "x_offset": 80}
            ],
            "edges": [
                {"src": "start", "tgt": "open_login"},
                {"src": "open_login", "tgt": "show_login"},
                {"src": "show_login", "tgt": "input_cred"},
                {"src": "input_cred", "tgt": "click_login"},
                {"src": "click_login", "tgt": "check_auth"},
                {"src": "check_auth", "tgt": "check_status", "label": "Đúng mật khẩu"},
                {"src": "check_auth", "tgt": "err_auth", "label": "Sai thông tin"},
                {"src": "err_auth", "tgt": "end_err1"},
                {"src": "check_status", "tgt": "login_ok", "label": "Active"},
                {"src": "check_status", "tgt": "err_locked", "label": "Locked"},
                {"src": "err_locked", "tgt": "end_err2"},
                {"src": "login_ok", "tgt": "end_ok"}
            ]
        },

        # --- 3. QUẢN LÝ KHÁCH HÀNG ---
        {
            "title": "3. Quản lý khách hàng",
            "lanes": ["Admin", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_cust", "lane": 0, "type": "action", "y": 100, "text": "Mở chức năng\nQuản lý khách hàng"},
                {"id": "get_cust", "lane": 1, "type": "action", "y": 100, "text": "Truy vấn và hiển thị\ndanh sách khách hàng"},
                {"id": "select_cust", "lane": 0, "type": "action", "y": 180, "text": "Chọn một khách hàng\ntrong danh sách"},
                {"id": "choose_op", "lane": 0, "type": "decision", "y": 255, "text": "Chọn\nthao tác?"},
                {"id": "do_lock", "lane": 1, "type": "action", "y": 330, "text": "Cập nhật trạng thái\ntài khoản thành locked"},
                {"id": "do_unlock", "lane": 1, "type": "action", "y": 405, "text": "Cập nhật trạng thái\ntài khoản thành active"},
                {"id": "refresh_ui", "lane": 1, "type": "action", "y": 480, "text": "Thông báo thành công\nvà làm mới danh sách"},
                {"id": "end", "lane": 1, "type": "end", "y": 555}
            ],
            "edges": [
                {"src": "start", "tgt": "open_cust"},
                {"src": "open_cust", "tgt": "get_cust"},
                {"src": "get_cust", "tgt": "select_cust"},
                {"src": "select_cust", "tgt": "choose_op"},
                {"src": "choose_op", "tgt": "do_lock", "label": "Khóa tài khoản"},
                {"src": "choose_op", "tgt": "do_unlock", "label": "Mở khóa"},
                {"src": "do_lock", "tgt": "refresh_ui"},
                {"src": "do_unlock", "tgt": "refresh_ui"},
                {"src": "refresh_ui", "tgt": "end"}
            ]
        },

        # --- 4. DUYỆT VÀ TÌM KIẾM SẢN PHẨM ---
        {
            "title": "4. Duyệt và Tìm kiếm sản phẩm",
            "lanes": ["Khách hàng", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_shop", "lane": 0, "type": "action", "y": 100, "text": "Truy cập trang Cửa hàng"},
                {"id": "load_home", "lane": 1, "type": "action", "y": 100, "text": "Tải Banner quảng cáo\nvà danh mục nổi bật"},
                {"id": "choose_browse", "lane": 0, "type": "decision", "y": 185, "text": "Chọn hình thức\nduyệt hàng?"},
                {"id": "search_kw", "lane": 1, "type": "action", "y": 260, "text": "Tìm kiếm theo từ khóa\ntên sản phẩm, SKU"},
                {"id": "filter_opts", "lane": 1, "type": "action", "y": 325, "text": "Lọc theo giá, thương hiệu,\ntag HOT / NEW"},
                {"id": "by_cat", "lane": 1, "type": "action", "y": 390, "text": "Lấy sản phẩm theo\ndanh mục đã chọn"},
                {"id": "show_res", "lane": 1, "type": "action", "y": 465, "text": "Hiển thị danh sách\nsản phẩm phù hợp"},
                {"id": "end", "lane": 1, "type": "end", "y": 540}
            ],
            "edges": [
                {"src": "start", "tgt": "open_shop"},
                {"src": "open_shop", "tgt": "load_home"},
                {"src": "load_home", "tgt": "choose_browse"},
                {"src": "choose_browse", "tgt": "search_kw", "label": "Tìm kiếm"},
                {"src": "choose_browse", "tgt": "filter_opts", "label": "Bộ lọc"},
                {"src": "choose_browse", "tgt": "by_cat", "label": "Danh mục"},
                {"src": "search_kw", "tgt": "show_res"},
                {"src": "filter_opts", "tgt": "show_res"},
                {"src": "by_cat", "tgt": "show_res"},
                {"src": "show_res", "tgt": "end"}
            ]
        },

        # --- 5. XEM CHI TIẾT & TỒN KHO SKU ---
        {
            "title": "5. Xem chi tiết & Tồn kho SKU",
            "lanes": ["Khách hàng", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "select_prod", "lane": 0, "type": "action", "y": 100, "text": "Chọn xem chi tiết\nmột sản phẩm"},
                {"id": "get_detail", "lane": 1, "type": "action", "y": 100, "text": "Truy vấn thông tin\nsản phẩm và các SKU"},
                {"id": "pick_sku", "lane": 0, "type": "action", "y": 180, "text": "Chọn Màu sắc và\nKích thước (SKU)"},
                {"id": "check_stock", "lane": 1, "type": "decision", "y": 245, "text": "Kiểm tra\ntồn kho SKU?"},
                {"id": "in_stock", "lane": 1, "type": "action", "y": 320, "text": "Hiển thị Còn hàng\nvà mở nút Thêm giỏ"},
                {"id": "out_stock", "lane": 1, "type": "action", "y": 395, "text": "Hiển thị Hết hàng\nvà khóa nút Thêm giỏ"},
                {"id": "end", "lane": 1, "type": "end", "y": 470}
            ],
            "edges": [
                {"src": "start", "tgt": "select_prod"},
                {"src": "select_prod", "tgt": "get_detail"},
                {"src": "get_detail", "tgt": "pick_sku"},
                {"src": "pick_sku", "tgt": "check_stock"},
                {"src": "check_stock", "tgt": "in_stock", "label": "Còn hàng"},
                {"src": "check_stock", "tgt": "out_stock", "label": "Hết hàng"},
                {"src": "in_stock", "tgt": "end"},
                {"src": "out_stock", "tgt": "end"}
            ]
        },

        # --- 6. QUẢN TRỊ CATALOG SẢN PHẨM ---
        {
            "title": "6. Quản trị Catalog sản phẩm",
            "lanes": ["Admin", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_catalog", "lane": 0, "type": "action", "y": 100, "text": "Mở trang Quản trị Catalog"},
                {"id": "choose_module", "lane": 0, "type": "decision", "y": 180, "text": "Chọn phân hệ\nquản lý?"},
                {"id": "crud_prod", "lane": 1, "type": "action", "y": 260, "text": "Thêm/Sửa/Xóa mềm\nsản phẩm & SKU"},
                {"id": "crud_cat", "lane": 1, "type": "action", "y": 325, "text": "Thêm/Sửa/Xóa\ndanh mục sản phẩm"},
                {"id": "crud_banner", "lane": 1, "type": "action", "y": 390, "text": "Thêm/Sửa/Xóa\nBanner quảng cáo"},
                {"id": "refund_stock", "lane": 1, "type": "action", "y": 455, "text": "Tự động cộng lại\ntồn kho SKU đơn hủy"},
                {"id": "save_catalog", "lane": 1, "type": "action", "y": 530, "text": "Lưu thay đổi CSDL\nvà thông báo thành công"},
                {"id": "end", "lane": 1, "type": "end", "y": 605}
            ],
            "edges": [
                {"src": "start", "tgt": "open_catalog"},
                {"src": "open_catalog", "tgt": "choose_module"},
                {"src": "choose_module", "tgt": "crud_prod", "label": "Sản phẩm & SKU"},
                {"src": "choose_module", "tgt": "crud_cat", "label": "Danh mục"},
                {"src": "choose_module", "tgt": "crud_banner", "label": "Banner"},
                {"src": "choose_module", "tgt": "refund_stock", "label": "Hoàn tồn kho"},
                {"src": "crud_prod", "tgt": "save_catalog"},
                {"src": "crud_cat", "tgt": "save_catalog"},
                {"src": "crud_banner", "tgt": "save_catalog"},
                {"src": "refund_stock", "tgt": "save_catalog"},
                {"src": "save_catalog", "tgt": "end"}
            ]
        },

        # --- 7. QUẢN LÝ GIỎ HÀNG ---
        {
            "title": "7. Quản lý giỏ hàng",
            "lanes": ["Khách hàng", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "add_cart", "lane": 0, "type": "action", "y": 100, "text": "Chọn SKU & Số lượng\n-> Thêm vào giỏ"},
                {"id": "check_stock", "lane": 1, "type": "decision", "y": 165, "text": "Kiểm tra\ntồn kho SKU?"},
                {"id": "err_stock", "lane": 1, "type": "action", "y": 240, "text": "Báo lỗi không đủ tồn kho"},
                {"id": "add_ok", "lane": 1, "type": "action", "y": 310, "text": "Thêm vào giỏ hàng\nvà tính lại tổng tiền"},
                {"id": "open_drawer", "lane": 0, "type": "action", "y": 380, "text": "Mở Giỏ hàng (Drawer)"},
                {"id": "choose_cart_op", "lane": 0, "type": "decision", "y": 455, "text": "Chọn thao tác\ntrên giỏ?"},
                {"id": "update_qty", "lane": 1, "type": "action", "y": 530, "text": "Cập nhật số lượng mới\nvà tính lại tổng tiền"},
                {"id": "remove_item", "lane": 1, "type": "action", "y": 595, "text": "Xóa món khỏi giỏ\nvà tính lại tổng tiền"},
                {"id": "go_checkout", "lane": 1, "type": "action", "y": 660, "text": "Chuyển sang trang Checkout"},
                {"id": "end", "lane": 1, "type": "end", "y": 735},
                {"id": "end_err", "lane": 1, "type": "end", "y": 250, "w": 24, "h": 24, "x_offset": 80}
            ],
            "edges": [
                {"src": "start", "tgt": "add_cart"},
                {"src": "add_cart", "tgt": "check_stock"},
                {"src": "check_stock", "tgt": "add_ok", "label": "Đủ hàng"},
                {"src": "check_stock", "tgt": "err_stock", "label": "Không đủ"},
                {"src": "err_stock", "tgt": "end_err"},
                {"src": "add_ok", "tgt": "open_drawer"},
                {"src": "open_drawer", "tgt": "choose_cart_op"},
                {"src": "choose_cart_op", "tgt": "update_qty", "label": "Cập nhật SL"},
                {"src": "choose_cart_op", "tgt": "remove_item", "label": "Xóa món"},
                {"src": "choose_cart_op", "tgt": "go_checkout", "label": "Thanh toán"},
                {"src": "update_qty", "tgt": "end"},
                {"src": "remove_item", "tgt": "end"},
                {"src": "go_checkout", "tgt": "end"}
            ]
        },

        # --- 8. CHECKOUT VÀ TẠO ĐƠN HÀNG ---
        {
            "title": "8. Checkout và Tạo đơn hàng",
            "lanes": ["Khách hàng", "Hệ thống & GHN"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_chk", "lane": 0, "type": "action", "y": 100, "text": "Mở trang Checkout &\nchọn địa chỉ nhận hàng"},
                {"id": "ghn_fee", "lane": 1, "type": "action", "y": 100, "text": "GHN tính cước phí\nvận chuyển động"},
                {"id": "chk_stock", "lane": 1, "type": "decision", "y": 180, "text": "Kiểm tra tồn kho\ntoàn bộ giỏ?"},
                {"id": "err_out", "lane": 1, "type": "action", "y": 255, "text": "Báo hết hàng và\ndừng Checkout"},
                {"id": "opt_vouch", "lane": 0, "type": "decision", "y": 325, "text": "Áp dụng mã\nVoucher giảm giá?"},
                {"id": "calc_vouch", "lane": 1, "type": "action", "y": 400, "text": "Kiểm tra mã Voucher &\ntính số tiền giảm giá"},
                {"id": "calc_total", "lane": 1, "type": "action", "y": 470, "text": "Tính Tổng thanh toán =\nTiền hàng + Ship - Voucher"},
                {"id": "confirm_ord", "lane": 0, "type": "action", "y": 540, "text": "Nhấn nút Xác nhận Đặt hàng"},
                {"id": "create_ord", "lane": 1, "type": "action", "y": 540, "text": "Tạo đơn hàng pending &\nxóa giỏ hàng"},
                {"id": "end_ok", "lane": 1, "type": "end", "y": 620},
                {"id": "end_err", "lane": 1, "type": "end", "y": 265, "w": 24, "h": 24, "x_offset": 80}
            ],
            "edges": [
                {"src": "start", "tgt": "open_chk"},
                {"src": "open_chk", "tgt": "ghn_fee"},
                {"src": "ghn_fee", "tgt": "chk_stock"},
                {"src": "chk_stock", "tgt": "opt_vouch", "label": "Đủ hàng"},
                {"src": "chk_stock", "tgt": "err_out", "label": "Hết hàng"},
                {"src": "err_out", "tgt": "end_err"},
                {"src": "opt_vouch", "tgt": "calc_vouch", "label": "Có Voucher"},
                {"src": "opt_vouch", "tgt": "calc_total", "label": "Không dùng"},
                {"src": "calc_vouch", "tgt": "calc_total"},
                {"src": "calc_total", "tgt": "confirm_ord"},
                {"src": "confirm_ord", "tgt": "create_ord"},
                {"src": "create_ord", "tgt": "end_ok"}
            ]
        },

        # --- 9. THANH TOÁN COD ---
        {
            "title": "9. Thanh toán COD",
            "lanes": ["Khách hàng", "Hệ thống & Admin"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "choose_cod", "lane": 0, "type": "action", "y": 100, "text": "Chọn phương thức COD\nvà nhấn Xác nhận"},
                {"id": "rec_cod", "lane": 1, "type": "action", "y": 100, "text": "Ghi nhận COD &\nđặt payment_status = pending"},
                {"id": "pack_ship", "lane": 1, "type": "action", "y": 180, "text": "Đóng gói & bàn giao\nđơn vị vận chuyển"},
                {"id": "pay_cash", "lane": 0, "type": "action", "y": 260, "text": "Nhận kiện hàng và\nthanh toán tiền mặt cho shipper"},
                {"id": "check_delivery", "lane": 1, "type": "decision", "y": 335, "text": "Giao hàng và\nthu tiền COD?"},
                {"id": "cod_ok", "lane": 1, "type": "action", "y": 410, "text": "Cập nhật payment_status = paid\nvà order_status = delivered"},
                {"id": "cod_fail", "lane": 1, "type": "action", "y": 480, "text": "Cập nhật đơn thất bại / hoàn trả"},
                {"id": "end", "lane": 1, "type": "end", "y": 555}
            ],
            "edges": [
                {"src": "start", "tgt": "choose_cod"},
                {"src": "choose_cod", "tgt": "rec_cod"},
                {"src": "rec_cod", "tgt": "pack_ship"},
                {"src": "pack_ship", "tgt": "pay_cash"},
                {"src": "pay_cash", "tgt": "check_delivery"},
                {"src": "check_delivery", "tgt": "cod_ok", "label": "Thành công"},
                {"src": "check_delivery", "tgt": "cod_fail", "label": "Thất bại"},
                {"src": "cod_ok", "tgt": "end"},
                {"src": "cod_fail", "tgt": "end"}
            ]
        },

        # --- 10. THANH TOÁN MOMO SANDBOX ---
        {
            "title": "10. Thanh toán MoMo Sandbox",
            "lanes": ["Khách hàng", "Hệ thống", "Cổng MoMo"],
            "lane_w": 240,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "choose_momo", "lane": 0, "type": "action", "y": 100, "text": "Chọn thanh toán Ví MoMo\nvà Xác nhận"},
                {"id": "sign_hmac", "lane": 1, "type": "action", "y": 100, "text": "Ký số HMAC-SHA256\nvà gửi sang MoMo"},
                {"id": "gen_qr", "lane": 2, "type": "action", "y": 100, "text": "Khởi tạo giao dịch &\ntrả về mã QR / PayUrl"},
                {"id": "scan_pay", "lane": 0, "type": "action", "y": 180, "text": "Quét mã QR và xác nhận\nthanh toán trên App MoMo"},
                {"id": "check_momo", "lane": 2, "type": "decision", "y": 250, "text": "Kết quả\ngiao dịch MoMo?"},
                {"id": "recv_ipn", "lane": 1, "type": "action", "y": 325, "text": "Tiếp nhận Webhook IPN &\nxác thực chữ ký số"},
                {"id": "momo_ok", "lane": 1, "type": "action", "y": 395, "text": "Cập nhật payment_status = paid\nvà thông báo thành công"},
                {"id": "momo_fail", "lane": 1, "type": "action", "y": 465, "text": "Cập nhật trạng thái failed\nvà thông báo thất bại"},
                {"id": "end", "lane": 1, "type": "end", "y": 540}
            ],
            "edges": [
                {"src": "start", "tgt": "choose_momo"},
                {"src": "choose_momo", "tgt": "sign_hmac"},
                {"src": "sign_hmac", "tgt": "gen_qr"},
                {"src": "gen_qr", "tgt": "scan_pay"},
                {"src": "scan_pay", "tgt": "check_momo"},
                {"src": "check_momo", "tgt": "recv_ipn", "label": "Thành công"},
                {"src": "check_momo", "tgt": "momo_fail", "label": "Thất bại"},
                {"src": "recv_ipn", "tgt": "momo_ok"},
                {"src": "momo_ok", "tgt": "end"},
                {"src": "momo_fail", "tgt": "end"}
            ]
        },

        # --- 11. THEO DÕI & HỦY ĐƠN HÀNG ---
        {
            "title": "11. Theo dõi & Hủy đơn hàng",
            "lanes": ["Khách hàng", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_orders", "lane": 0, "type": "action", "y": 100, "text": "Mở trang Đơn hàng của tôi\nvà chọn xem chi tiết"},
                {"id": "check_status", "lane": 1, "type": "decision", "y": 175, "text": "Trạng thái\nđơn hàng?"},
                {"id": "track_ghn", "lane": 1, "type": "action", "y": 250, "text": "Hiển thị mã vận đơn &\ntra cứu lộ trình GHN"},
                {"id": "click_cancel", "lane": 0, "type": "action", "y": 325, "text": "Nhấn nút Hủy đơn hàng &\nxác nhận hủy"},
                {"id": "do_cancel", "lane": 1, "type": "action", "y": 400, "text": "Cập nhật order = cancelled &\nhoàn trả lại tồn kho SKU"},
                {"id": "end", "lane": 1, "type": "end", "y": 480}
            ],
            "edges": [
                {"src": "start", "tgt": "open_orders"},
                {"src": "open_orders", "tgt": "check_status"},
                {"src": "check_status", "tgt": "track_ghn", "label": "shipping"},
                {"src": "check_status", "tgt": "click_cancel", "label": "pending"},
                {"src": "click_cancel", "tgt": "do_cancel"},
                {"src": "track_ghn", "tgt": "end"},
                {"src": "do_cancel", "tgt": "end"}
            ]
        },

        # --- 12. ĐÁNH GIÁ SẢN PHẨM ---
        {
            "title": "12. Đánh giá sản phẩm",
            "lanes": ["Khách hàng", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "select_review_item", "lane": 0, "type": "action", "y": 100, "text": "Chọn sản phẩm trong\nđơn hàng đã mua"},
                {"id": "check_delivered", "lane": 1, "type": "decision", "y": 175, "text": "Đơn hàng\nđã delivered?"},
                {"id": "err_not_deliv", "lane": 1, "type": "action", "y": 250, "text": "Báo đơn phải giao xong\nmới được đánh giá"},
                {"id": "check_reviewed", "lane": 1, "type": "decision", "y": 325, "text": "Sản phẩm đã\nđược đánh giá?"},
                {"id": "err_already", "lane": 1, "type": "action", "y": 400, "text": "Báo sản phẩm đã gửi\nđánh giá trước đó"},
                {"id": "submit_review", "lane": 0, "type": "action", "y": 475, "text": "Chọn số sao (1-5 sao),\nnhập nhận xét & Gửi"},
                {"id": "save_review", "lane": 1, "type": "action", "y": 475, "text": "Lưu đánh giá & tính lại\nđiểm sao trung bình"},
                {"id": "end_ok", "lane": 1, "type": "end", "y": 555},
                {"id": "end_err1", "lane": 1, "type": "end", "y": 260, "w": 24, "h": 24, "x_offset": 80},
                {"id": "end_err2", "lane": 1, "type": "end", "y": 410, "w": 24, "h": 24, "x_offset": 80}
            ],
            "edges": [
                {"src": "start", "tgt": "select_review_item"},
                {"src": "select_review_item", "tgt": "check_delivered"},
                {"src": "check_delivered", "tgt": "check_reviewed", "label": "Đã giao"},
                {"src": "check_delivered", "tgt": "err_not_deliv", "label": "Chưa giao"},
                {"src": "err_not_deliv", "tgt": "end_err1"},
                {"src": "check_reviewed", "tgt": "submit_review", "label": "Chưa đánh giá"},
                {"src": "check_reviewed", "tgt": "err_already", "label": "Đã đánh giá"},
                {"src": "err_already", "tgt": "end_err2"},
                {"src": "submit_review", "tgt": "save_review"},
                {"src": "save_review", "tgt": "end_ok"}
            ]
        },

        # --- 13. QUẢN TRỊ ĐƠN HÀNG & GHN ---
        {
            "title": "13. Quản trị Đơn hàng & GHN",
            "lanes": ["Admin", "Hệ thống & GHN"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_admin_orders", "lane": 0, "type": "action", "y": 100, "text": "Mở Quản lý đơn hàng &\nchọn một đơn hàng"},
                {"id": "choose_action", "lane": 0, "type": "decision", "y": 180, "text": "Chọn thao tác\nquản trị?"},
                {"id": "do_update_st", "lane": 1, "type": "action", "y": 260, "text": "Cập nhật trạng thái thủ công\n(processing / delivered)"},
                {"id": "do_ghn", "lane": 1, "type": "action", "y": 325, "text": "Gửi dữ liệu sang GHN &\ncấp mã Tracking 1-Click"},
                {"id": "do_cod", "lane": 1, "type": "action", "y": 390, "text": "Xác nhận thu tiền COD ->\npayment_status = paid"},
                {"id": "save_and_refresh", "lane": 1, "type": "action", "y": 465, "text": "Thông báo thành công và\nlàm mới thông tin đơn"},
                {"id": "end", "lane": 1, "type": "end", "y": 540}
            ],
            "edges": [
                {"src": "start", "tgt": "open_admin_orders"},
                {"src": "open_admin_orders", "tgt": "choose_action"},
                {"src": "choose_action", "tgt": "do_update_st", "label": "Chuyển trạng thái"},
                {"src": "choose_action", "tgt": "do_ghn", "label": "Tạo đơn GHN"},
                {"src": "choose_action", "tgt": "do_cod", "label": "Thu tiền COD"},
                {"src": "do_update_st", "tgt": "save_and_refresh"},
                {"src": "do_ghn", "tgt": "save_and_refresh"},
                {"src": "do_cod", "tgt": "save_and_refresh"},
                {"src": "save_and_refresh", "tgt": "end"}
            ]
        },

        # --- 14. TƯ VẤN TRỰC TUYẾN LIVECHAT (LAB 7) ---
        {
            "title": "14. Tư vấn trực tuyến LiveChat (Lab 7)",
            "lanes": ["Khách hàng", "Hệ thống", "Admin CSKH"],
            "lane_w": 240,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_chat", "lane": 0, "type": "action", "y": 100, "text": "Mở ChatWidget tại cửa hàng\nvà nhập câu hỏi tư vấn"},
                {"id": "save_msg", "lane": 1, "type": "action", "y": 100, "text": "Lưu tin nhắn vào CSDL\n(is_read = false)"},
                {"id": "reply_cskh", "lane": 2, "type": "action", "y": 100, "text": "Mở AdminChatModal &\nnhập câu trả lời giải đáp"},
                {"id": "save_reply", "lane": 1, "type": "action", "y": 180, "text": "Lưu phản hồi và\nđánh dấu is_read = true"},
                {"id": "recv_reply", "lane": 0, "type": "action", "y": 260, "text": "Khách hàng nhận được\ntin nhắn tư vấn giải đáp"},
                {"id": "end", "lane": 0, "type": "end", "y": 340}
            ],
            "edges": [
                {"src": "start", "tgt": "open_chat"},
                {"src": "open_chat", "tgt": "save_msg"},
                {"src": "save_msg", "tgt": "reply_cskh"},
                {"src": "reply_cskh", "tgt": "save_reply"},
                {"src": "save_reply", "tgt": "recv_reply"},
                {"src": "recv_reply", "tgt": "end"}
            ]
        },

        # --- 15. BÁO CÁO TÀI CHÍNH & HOÀN TIỀN (LAB 9) ---
        {
            "title": "15. Báo cáo Tài chính & Hoàn tiền (Lab 9)",
            "lanes": ["Admin", "Hệ thống"],
            "lane_w": 280,
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 40},
                {"id": "open_fin", "lane": 0, "type": "action", "y": 100, "text": "Mở trang Quản trị\nTài chính (Finance)"},
                {"id": "calc_fin", "lane": 1, "type": "action", "y": 100, "text": "Tổng hợp doanh thu thực &\nbảng đối soát MoMo/COD"},
                {"id": "req_refund", "lane": 0, "type": "action", "y": 180, "text": "Chọn đơn hàng cần hoàn tiền\nvà chuyển sang refunded"},
                {"id": "check_state", "lane": 1, "type": "decision", "y": 255, "text": "Kiểm tra ràng buộc\nState Machine?"},
                {"id": "do_refund", "lane": 1, "type": "action", "y": 330, "text": "Cập nhật refunded &\ntrừ lại doanh thu thực"},
                {"id": "err_state", "lane": 1, "type": "action", "y": 400, "text": "Báo lỗi vi phạm quy tắc\nchu trình State Machine"},
                {"id": "end_ok", "lane": 1, "type": "end", "y": 480},
                {"id": "end_err", "lane": 1, "type": "end", "y": 410, "w": 24, "h": 24, "x_offset": 80}
            ],
            "edges": [
                {"src": "start", "tgt": "open_fin"},
                {"src": "open_fin", "tgt": "calc_fin"},
                {"src": "calc_fin", "tgt": "req_refund"},
                {"src": "req_refund", "tgt": "check_state"},
                {"src": "check_state", "tgt": "do_refund", "label": "Hợp lệ"},
                {"src": "check_state", "tgt": "err_state", "label": "Không hợp lệ"},
                {"src": "err_state", "tgt": "end_err"},
                {"src": "do_refund", "tgt": "end_ok"}
            ]
        }
    ]

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T21:10:00.000Z", agent="Striker Clean UML V4", version="21.0.0", type="device")
    os.makedirs('docs/drawio_xml', exist_ok=True)

    for diag_idx, diag in enumerate(diagrams):
        diagram = ET.SubElement(mxfile, "diagram", name=diag["title"], id=f"clean_diag_{diag_idx+1}")
        num_lanes = len(diag["lanes"])
        lane_w = diag["lane_w"]
        pool_w = num_lanes * lane_w
        
        max_y = max([node["y"] for node in diag["nodes"]]) + 100
        pool_h = max(700, max_y)

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
            
            w = n.get("w", 170)
            h = n.get("h", 45)
            x_center = (lane_w - w) / 2 + n.get("x_offset", 0)
            
            if n["type"] == "start":
                style = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#b85450;"
                w, h = 30, 30
                x_center = (lane_w - 30) / 2
            elif n["type"] == "end":
                style = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#b85450;"
                w = n.get("w", 30)
                h = n.get("h", 30)
                x_center = (lane_w - w) / 2 + n.get("x_offset", 0)
            elif n["type"] == "decision":
                style = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
                w, h = 140, 55
                x_center = (lane_w - 140) / 2
            else: # action
                style = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"

            n_cell = ET.SubElement(root, "mxCell", id=n_id, value=n.get("text", ""), style=style, vertex="1", parent=parent_lane)
            ET.SubElement(n_cell, "mxGeometry", x=str(int(x_center)), y=str(n["y"]), width=str(w), height=str(h), as_="geometry")

        for e_idx, e in enumerate(diag["edges"]):
            e_id = f"edge_{diag_idx+1}_{e_idx}"
            src = node_map[e["src"]]
            tgt = node_map[e["tgt"]]
            lbl = e.get("label", "")
            e_style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;strokeWidth=1.5;endArrow=classic;fontSize=10;fontColor=#000000;fontFamily=Helvetica;"
            
            e_cell = ET.SubElement(root, "mxCell", id=e_id, value=lbl, style=e_style, edge="1", source=src, target=tgt, parent="1")
            ET.SubElement(e_cell, "mxGeometry", relative="1", as_="geometry")

        # Export individual XML
        xml_str = ET.tostring(mxGraphModel, encoding='unicode')
        with open(f"docs/drawio_xml/So_do_{diag_idx+1}.xml", "w", encoding="utf-8") as f:
            f.write(xml_str)

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write("docs/striker_activity_diagrams.drawio", encoding="utf-8", xml_declaration=True)
    print("ALL 15 DIAGRAMS GENERATED WITH CLEAN NO-COLLISION WATERFALL LAYOUT!")

generate_perfect_activity_diagrams()
