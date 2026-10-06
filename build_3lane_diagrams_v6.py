import os
import xml.etree.ElementTree as ET

def build_3lane_diagrams():
    # Style definitions matching Image 2 perfectly
    style_action = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
    style_dec = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
    style_start = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#b85450;"
    style_end = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#b85450;"
    style_edge = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;strokeWidth=1.5;endArrow=classic;fontSize=10;fontColor=#000000;fontFamily=Helvetica;"

    diagrams = [
        # =========================================================================
        # 1. ĐĂNG KÝ TÀI KHOẢN VÀ XÁC THỰC OTP
        # =========================================================================
        {
            "title": "1. Đăng ký tài khoản và Xác thực OTP",
            "lanes": ["Người dùng", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Chọn chức năng\nđăng ký tài khoản"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Hiển thị biểu mẫu\nđăng ký tài khoản"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Nhập Họ tên, Email,\nSĐT và Mật khẩu"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Nhấn nút Đăng ký"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Kiểm tra dữ liệu\nbiểu mẫu"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Kiểm tra trùng lặp\nEmail / SĐT"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 325, "w": 130, "h": 50, "text": "Thông tin hợp lệ?"},
                {"id": "err1", "lane": 1, "type": "end", "x": 195, "y": 338, "w": 24, "h": 24},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Lưu tài khoản pending\nvà gửi mã OTP"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 475, "w": 160, "h": 45, "text": "Hiển thị màn hình\nnhập mã OTP"},
                {"id": "u4", "lane": 0, "type": "action", "x": 30, "y": 475, "w": 160, "h": 45, "text": "Nhập mã OTP từ Email\nvà nhấn Xác thực"},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 550, "w": 160, "h": 45, "text": "Xác thực mã OTP\ntrong CSDL"},
                {"id": "dec2", "lane": 1, "type": "decision", "x": 45, "y": 548, "w": 130, "h": 50, "text": "Mã OTP đúng?"},
                {"id": "err2", "lane": 1, "type": "end", "x": 195, "y": 561, "w": 24, "h": 24},
                {"id": "d4", "lane": 2, "type": "action", "x": 30, "y": 625, "w": 160, "h": 45, "text": "Kích hoạt active &\ncấp JWT Token"},
                {"id": "s4", "lane": 1, "type": "action", "x": 30, "y": 625, "w": 160, "h": 45, "text": "Thông báo thành công\nvà đăng nhập"},
                {"id": "u5", "lane": 0, "type": "action", "x": 30, "y": 700, "w": 160, "h": 45, "text": "Nhận thông báo\nvà vào Trang chủ"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 775, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "u2"},
                {"src": "u2", "tgt": "u3"},
                {"src": "u3", "tgt": "s2"},
                {"src": "s2", "tgt": "d1"},
                {"src": "d1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "err1", "label": "Sai/Trùng"},
                {"src": "dec1", "tgt": "d2", "label": "Hợp lệ"},
                {"src": "d2", "tgt": "s3"},
                {"src": "s3", "tgt": "u4"},
                {"src": "u4", "tgt": "d3"},
                {"src": "d3", "tgt": "dec2"},
                {"src": "dec2", "tgt": "err2", "label": "Sai mã"},
                {"src": "dec2", "tgt": "d4", "label": "Đúng mã"},
                {"src": "d4", "tgt": "s4"},
                {"src": "s4", "tgt": "u5"},
                {"src": "u5", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 2. ĐĂNG NHẬP HỆ THỐNG
        # =========================================================================
        {
            "title": "2. Đăng nhập hệ thống",
            "lanes": ["Người dùng", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Chọn chức năng\nđăng nhập"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Hiển thị biểu mẫu\nđăng nhập"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Nhập Email / SĐT\nvà Mật khẩu"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Nhấn nút Đăng nhập"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Gửi thông tin xác thực"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Truy vấn tài khoản &\nso khớp mật khẩu"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 325, "w": 130, "h": 50, "text": "Đúng mật khẩu?"},
                {"id": "err1", "lane": 1, "type": "end", "x": 195, "y": 338, "w": 24, "h": 24},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Kiểm tra trạng thái\ntài khoản (active/locked)"},
                {"id": "dec2", "lane": 1, "type": "decision", "x": 45, "y": 475, "w": 130, "h": 50, "text": "Tài khoản active?"},
                {"id": "err2", "lane": 1, "type": "end", "x": 195, "y": 488, "w": 24, "h": 24},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 550, "w": 160, "h": 45, "text": "Cấp Bearer JWT Token\nvà lưu LocalStorage"},
                {"id": "u4", "lane": 0, "type": "action", "x": 30, "y": 550, "w": 160, "h": 45, "text": "Đăng nhập thành công\nvà vào Trang chủ"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 625, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "u2"},
                {"src": "u2", "tgt": "u3"},
                {"src": "u3", "tgt": "s2"},
                {"src": "s2", "tgt": "d1"},
                {"src": "d1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "err1", "label": "Sai mật khẩu"},
                {"src": "dec1", "tgt": "d2", "label": "Đúng mật khẩu"},
                {"src": "d2", "tgt": "dec2"},
                {"src": "dec2", "tgt": "err2", "label": "Bị khóa"},
                {"src": "dec2", "tgt": "s3", "label": "Active"},
                {"src": "s3", "tgt": "u4"},
                {"src": "u4", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 3. QUẢN LÝ KHÁCH HÀNG (KHÓA / MỞ KHÓA)
        # =========================================================================
        {
            "title": "3. Quản lý khách hàng",
            "lanes": ["Admin", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Mở chức năng\nQuản lý khách hàng"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Gửi yêu cầu lấy\ndanh sách khách hàng"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Lấy danh sách\ntài khoản khách hàng"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Hiển thị danh sách\nkhách hàng"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Chọn một khách hàng\ntrong danh sách"},
                {"id": "u3", "lane": 0, "type": "decision", "x": 45, "y": 250, "w": 130, "h": 50, "text": "Chọn thao tác?"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Cập nhật trạng thái\nlocked trong CSDL"},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Cập nhật trạng thái\nactive trong CSDL"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Thông báo thành công\nvà làm mới danh sách"},
                {"id": "u4", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Nhận thông báo\nhoàn tất thao tác"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "s2"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "u3"},
                {"src": "u3", "tgt": "d2", "label": "Khóa"},
                {"src": "u3", "tgt": "d3", "label": "Mở khóa"},
                {"src": "d2", "tgt": "s3"},
                {"src": "d3", "tgt": "s3"},
                {"src": "s3", "tgt": "u4"},
                {"src": "u4", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 4. DUYỆT VÀ TÌM KIẾM SẢN PHẨM
        # =========================================================================
        {
            "title": "4. Duyệt và Tìm kiếm sản phẩm",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Truy cập trang Cửa hàng"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Gửi yêu cầu tải Banner\nvà sản phẩm nổi bật"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Lấy danh sách Banner\nvà sản phẩm từ CSDL"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Hiển thị Banner &\ndanh mục sản phẩm"},
                {"id": "u2", "lane": 0, "type": "decision", "x": 45, "y": 173, "w": 130, "h": 50, "text": "Hình thức duyệt?"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Tìm kiếm theo từ khóa\ntên sản phẩm, SKU"},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Lọc sản phẩm theo giá,\nthương hiệu, HOT/NEW"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Hiển thị danh sách\nsản phẩm phù hợp"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Xem danh sách\nsản phẩm kết quả"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "s2"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "d2", "label": "Tìm kiếm"},
                {"src": "u2", "tgt": "d3", "label": "Bộ lọc"},
                {"src": "d2", "tgt": "s3"},
                {"src": "d3", "tgt": "s3"},
                {"src": "s3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 5. XEM CHI TIẾT & TỒN KHO SKU
        # =========================================================================
        {
            "title": "5. Xem chi tiết & Tồn kho SKU",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Chọn xem chi tiết\nmột sản phẩm"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Gửi yêu cầu lấy\nchi tiết sản phẩm & SKU"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Lấy thông tin sản phẩm\nvà các biến thể SKU"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Hiển thị trang\nchi tiết sản phẩm"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Chọn Màu sắc và\nKích thước (SKU)"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Kiểm tra số lượng\ntồn kho SKU"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 248, "w": 130, "h": 50, "text": "Còn hàng?"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Hiển thị Còn hàng\nvà mở nút Mua ngay"},
                {"id": "s4", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Hiển thị Hết hàng\nvà khóa nút Mua ngay"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Xem trạng thái tồn kho\nvà tiến hành mua"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "s2"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "d2"},
                {"src": "d2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "s3", "label": "Còn hàng"},
                {"src": "dec1", "tgt": "s4", "label": "Hết hàng"},
                {"src": "s3", "tgt": "u3"},
                {"src": "s4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 6. QUẢN TRỊ CATALOG SẢN PHẨM
        # =========================================================================
        {
            "title": "6. Quản trị Catalog sản phẩm",
            "lanes": ["Admin", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Mở trang Quản trị Catalog"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Hiển thị dữ liệu quản lý"},
                {"id": "u2", "lane": 0, "type": "decision", "x": 45, "y": 173, "w": 130, "h": 50, "text": "Chọn phân hệ?"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Thêm/Sửa/Xóa mềm\nsản phẩm và biến thể SKU"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Thêm/Sửa/Xóa\ndanh mục & Banner"},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Lưu thay đổi CSDL\n& đồng bộ dữ liệu"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Thông báo cập nhật\nCatalog thành công"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Nhận thông báo\nhoàn tất quản trị"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "u2"},
                {"src": "u2", "tgt": "d1", "label": "Sản phẩm"},
                {"src": "u2", "tgt": "d2", "label": "Danh mục/Banner"},
                {"src": "d1", "tgt": "d3"},
                {"src": "d2", "tgt": "d3"},
                {"src": "d3", "tgt": "s2"},
                {"src": "s2", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 7. QUẢN LÝ GIỎ HÀNG
        # =========================================================================
        {
            "title": "7. Quản lý giỏ hàng",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Chọn SKU & Số lượng\n-> Thêm vào giỏ"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Gửi kiểm tra tồn kho"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Kiểm tra tồn kho\nSKU trong CSDL"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 173, "w": 130, "h": 50, "text": "Đủ số lượng?"},
                {"id": "err1", "lane": 1, "type": "end", "x": 195, "y": 186, "w": 24, "h": 24},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Lưu mặt hàng vào giỏ\nvà tính lại tổng tiền"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Hiển thị Giỏ hàng\nkèm danh sách món"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Mở Giỏ hàng (Drawer)\nvà kiểm tra món"},
                {"id": "u3", "lane": 0, "type": "decision", "x": 45, "y": 400, "w": 130, "h": 50, "text": "Thao tác trên giỏ?"},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Cập nhật SL / Xóa món\ntrong CSDL giỏ hàng"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 475, "w": 160, "h": 45, "text": "Chuyển sang màn hình\nThanh toán (Checkout)"},
                {"id": "u4", "lane": 0, "type": "action", "x": 30, "y": 475, "w": 160, "h": 45, "text": "Xác nhận và tiến hành\nThanh toán đơn"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 550, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "err1", "label": "Không đủ"},
                {"src": "dec1", "tgt": "d2", "label": "Đủ hàng"},
                {"src": "d2", "tgt": "s2"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "u3"},
                {"src": "u3", "tgt": "d3", "label": "Sửa/Xóa"},
                {"src": "u3", "tgt": "s3", "label": "Thanh toán"},
                {"src": "d3", "tgt": "s2"},
                {"src": "s3", "tgt": "u4"},
                {"src": "u4", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 8. CHECKOUT VÀ TẠO ĐƠN HÀNG
        # =========================================================================
        {
            "title": "8. Checkout và Tạo đơn hàng",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL & GHN"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Mở trang Checkout &\nchọn địa chỉ nhận hàng"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Gửi địa chỉ tính cước"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "GHN API tính phí ship &\nCSDL kiểm tra tồn kho"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 173, "w": 130, "h": 50, "text": "Còn đủ hàng?"},
                {"id": "err1", "lane": 1, "type": "end", "x": 195, "y": 186, "w": 24, "h": 24},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Tính Tổng thanh toán =\nTiền hàng + Ship - Voucher"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Nhập Voucher (nếu có)\nvà bấm Xác nhận đặt hàng"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Tạo đơn hàng pending &\nxóa giỏ hàng CSDL"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Chuyển sang bước chọn\nphương thức thanh toán"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Chọn phương thức\nCOD hoặc MoMo"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "err1", "label": "Hết hàng"},
                {"src": "dec1", "tgt": "s2", "label": "Đủ hàng"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "d2"},
                {"src": "d2", "tgt": "s3"},
                {"src": "s3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 9. THANH TOÁN COD
        # =========================================================================
        {
            "title": "9. Thanh toán COD",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL & Admin"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Chọn thanh toán COD\nvà nhấn Xác nhận"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Ghi nhận phương thức COD"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Lưu payment_status = pending\nvào CSDL đơn hàng"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Hiển thị màn hình\nĐặt hàng thành công"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Admin đóng gói & bàn giao\nđơn vị vận chuyển"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Nhận kiện hàng và\nthanh toán tiền mặt"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 325, "w": 130, "h": 50, "text": "Giao thành công?"},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Cập nhật payment = paid\nvà order = delivered"},
                {"id": "d4", "lane": 2, "type": "action", "x": 30, "y": 475, "w": 160, "h": 45, "text": "Cập nhật order = failed\nhoặc hoàn trả hàng"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 475, "w": 160, "h": 45, "text": "Hoàn tất đối soát đơn COD"},
                {"id": "end", "lane": 1, "type": "end", "x": 95, "y": 550, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "s2"},
                {"src": "s2", "tgt": "d2"},
                {"src": "d2", "tgt": "u2"},
                {"src": "u2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "d3", "label": "Thành công"},
                {"src": "dec1", "tgt": "d4", "label": "Thất bại"},
                {"src": "d3", "tgt": "s3"},
                {"src": "d4", "tgt": "s3"},
                {"src": "s3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 10. THANH TOÁN MOMO SANDBOX
        # =========================================================================
        {
            "title": "10. Thanh toán MoMo Sandbox",
            "lanes": ["Khách hàng", "Hệ thống", "Cổng MoMo & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Chọn thanh toán Ví MoMo\nvà nhấn Xác nhận"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Ký số HMAC-SHA256\nvà gửi sang Cổng MoMo"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "MoMo khởi tạo giao dịch\nvà trả về QR Code/PayUrl"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Hiển thị mã QR MoMo\nvà chuyển hướng"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Quét mã QR và xác nhận\nthanh toán trên App MoMo"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "MoMo trừ tiền và gửi\nWebhook IPN bất đồng bộ"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 248, "w": 130, "h": 50, "text": "Xác thực IPN hợp lệ?"},
                {"id": "err1", "lane": 1, "type": "end", "x": 195, "y": 261, "w": 24, "h": 24},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Cập nhật payment = paid\nvào CSDL thanh toán"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Hiển thị màn hình\nThanh toán Thành công!"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Nhận thông báo thanh toán\nvà xem đơn hàng"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "s2"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "d2"},
                {"src": "d2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "err1", "label": "Thất bại"},
                {"src": "dec1", "tgt": "d3", "label": "Thành công"},
                {"src": "d3", "tgt": "s3"},
                {"src": "s3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 11. THEO DÕI & HỦY ĐƠN HÀNG
        # =========================================================================
        {
            "title": "11. Theo dõi & Hủy đơn hàng",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Mở trang Đơn hàng của tôi\nvà chọn xem chi tiết"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Truy vấn dữ liệu đơn"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Lấy chi tiết đơn hàng\nvà trạng thái từ CSDL"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 173, "w": 130, "h": 50, "text": "Trạng thái đơn?"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Hiển thị mã vận đơn &\ntra cứu lộ trình GHN"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Bấm nút Hủy đơn hàng\nvà xác nhận hủy"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Cập nhật order = cancelled\nvà cộng lại tồn kho SKU"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Thông báo hủy đơn\nthành công"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Xem trạng thái\nđơn hàng Đã hủy"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "s2", "label": "shipping"},
                {"src": "dec1", "tgt": "u2", "label": "pending"},
                {"src": "u2", "tgt": "d2"},
                {"src": "d2", "tgt": "s3"},
                {"src": "s3", "tgt": "u3"},
                {"src": "s2", "tgt": "end"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 12. ĐÁNH GIÁ SẢN PHẨM
        # =========================================================================
        {
            "title": "12. Đánh giá sản phẩm",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Chọn sản phẩm trong\nđơn hàng đã mua"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Gửi kiểm tra điều kiện"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Kiểm tra đơn delivered\nvà chưa từng đánh giá"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 173, "w": 130, "h": 50, "text": "Đủ điều kiện?"},
                {"id": "err1", "lane": 1, "type": "end", "x": 195, "y": 186, "w": 24, "h": 24},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Hiển thị biểu mẫu\nđánh giá (Sao & Nhận xét)"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Chọn số sao (1-5 sao),\nnhập nhận xét & Gửi"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Lưu bản ghi đánh giá &\ntính lại điểm trung bình"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Thông báo thành công\nvà cập nhật điểm sao"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Xem đánh giá mới\ntrên trang sản phẩm"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "err1", "label": "Chưa đủ ĐK"},
                {"src": "dec1", "tgt": "s2", "label": "Đủ ĐK"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "d2"},
                {"src": "d2", "tgt": "s3"},
                {"src": "s3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 13. QUẢN TRỊ ĐƠN HÀNG & GHN
        # =========================================================================
        {
            "title": "13. Quản trị Đơn hàng & GHN",
            "lanes": ["Admin", "Hệ thống", "CSDL & GHN"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Mở Quản lý đơn hàng &\nchọn một đơn hàng"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Hiển thị chi tiết đơn"},
                {"id": "u2", "lane": 0, "type": "decision", "x": 45, "y": 173, "w": 130, "h": 50, "text": "Thao tác xử lý?"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "GHN tạo mã vận đơn 1-Click\n& CSDL lưu shipping"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Xác nhận đã thu COD ->\npayment_status = paid"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Thông báo thành công và\nlàm mới thông tin đơn"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Nhận thông báo\nhoàn tất quản trị"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 400, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "u2"},
                {"src": "u2", "tgt": "d1", "label": "Tạo đơn GHN"},
                {"src": "u2", "tgt": "d2", "label": "Thu tiền COD"},
                {"src": "d1", "tgt": "s2"},
                {"src": "d2", "tgt": "s2"},
                {"src": "s2", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 14. TƯ VẤN TRỰC TUYẾN LIVECHAT (LAB 7)
        # =========================================================================
        {
            "title": "14. Tư vấn trực tuyến LiveChat (Lab 7)",
            "lanes": ["Khách hàng", "Hệ thống", "CSDL & CSKH"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Mở ChatWidget tại cửa hàng\nvà gửi câu hỏi tư vấn"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Gửi tin nhắn qua Chat API"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Lưu tin nhắn vào CSDL\nvà phát chuông báo CSKH"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Admin CSKH nhập câu trả lời\nvà gửi phản hồi"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Lưu tin nhắn phản hồi\nvào CSDL (is_read = true)"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Khách hàng nhận được\ntin nhắn tư vấn giải đáp"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 325, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "d2"},
                {"src": "d2", "tgt": "s2"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ]
        },

        # =========================================================================
        # 15. BÁO CÁO TÀI CHÍNH & HOÀN TIỀN (LAB 9)
        # =========================================================================
        {
            "title": "15. Báo cáo Tài chính & Hoàn tiền (Lab 9)",
            "lanes": ["Admin", "Hệ thống", "CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 95, "y": 40, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Mở trang Quản trị\nTài chính (Finance)"},
                {"id": "s1", "lane": 1, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Yêu cầu tổng hợp số liệu"},
                {"id": "d1", "lane": 2, "type": "action", "x": 30, "y": 100, "w": 160, "h": 45, "text": "Tổng hợp doanh thu thực &\nbảng đối soát MoMo/COD"},
                {"id": "s2", "lane": 1, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Hiển thị 4 thẻ KPI,\nSpline Chart & Giao dịch"},
                {"id": "u2", "lane": 0, "type": "action", "x": 30, "y": 175, "w": 160, "h": 45, "text": "Chọn đơn cần hoàn tiền\nvà chuyển sang refunded"},
                {"id": "d2", "lane": 2, "type": "action", "x": 30, "y": 250, "w": 160, "h": 45, "text": "Kiểm tra ràng buộc\nState Machine trong CSDL"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 45, "y": 248, "w": 130, "h": 50, "text": "Hợp lệ chu trình?"},
                {"id": "err1", "lane": 1, "type": "end", "x": 195, "y": 261, "w": 24, "h": 24},
                {"id": "d3", "lane": 2, "type": "action", "x": 30, "y": 325, "w": 160, "h": 45, "text": "Cập nhật refunded &\ntrừ lại doanh thu thực"},
                {"id": "s3", "lane": 1, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Thông báo hoàn tiền\nthành công và làm mới"},
                {"id": "u3", "lane": 0, "type": "action", "x": 30, "y": 400, "w": 160, "h": 45, "text": "Nhận thông báo\nđối soát hoàn tất"},
                {"id": "end", "lane": 0, "type": "end", "x": 95, "y": 475, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "s1"},
                {"src": "s1", "tgt": "d1"},
                {"src": "d1", "tgt": "s2"},
                {"src": "s2", "tgt": "u2"},
                {"src": "u2", "tgt": "d2"},
                {"src": "d2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "err1", "label": "Vi phạm"},
                {"src": "dec1", "tgt": "d3", "label": "Hợp lệ"},
                {"src": "d3", "tgt": "s3"},
                {"src": "s3", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ]
        }
    ]

    lane_w = 220
    pool_w = 660

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T21:22:00.000Z", agent="Striker 3-Lane Waterfall V6", version="21.0.0", type="device")
    os.makedirs('docs/drawio_xml', exist_ok=True)

    for diag_idx, diag in enumerate(diagrams):
        max_y = max([node["y"] for node in diag["nodes"]]) + 80
        pool_h = max(600, max_y)

        diagram = ET.SubElement(mxfile, "diagram", name=diag["title"], id=f"v6_diag_{diag_idx+1}")
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
            
            w = n.get("w", 160)
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
    print("SUCCESS: Generated all 15 diagrams in 3-lane Waterfall architecture matching Image 2!")

build_3lane_diagrams()
