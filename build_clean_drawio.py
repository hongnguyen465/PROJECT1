import xml.etree.ElementTree as ET

def build_clean_activity_diagrams():
    # 15 Clean Business Activity Diagrams formatted exactly like classic UML (Image 2 style)
    diagrams = [
        {
            "title": "1. Đăng ký tài khoản và Xác thực OTP",
            "lanes": ["Người dùng", "Giao diện (Frontend)", "Dịch vụ Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 110, "w": 160, "h": 45, "text": "Chọn chức năng\nđăng ký tài khoản"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 110, "w": 160, "h": 45, "text": "Hiển thị biểu mẫu\nđăng ký tài khoản"},
                {"id": "act3", "lane": 0, "type": "action", "x": 35, "y": 190, "w": 160, "h": 45, "text": "Nhập Họ tên, Email,\nSĐT và Mật khẩu"},
                {"id": "act4", "lane": 0, "type": "action", "x": 35, "y": 270, "w": 160, "h": 45, "text": "Nhấn nút Đăng ký"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 265, "w": 130, "h": 55, "text": "Kiểm tra\nbiểu mẫu?"},
                {"id": "err1", "lane": 1, "type": "action", "x": 35, "y": 350, "w": 160, "h": 40, "text": "Báo lỗi định dạng\n(Thiếu/Sai trường)"},
                {"id": "dec2", "lane": 2, "type": "decision", "x": 50, "y": 265, "w": 130, "h": 55, "text": "Tài khoản\nđã tồn tại?"},
                {"id": "err2", "lane": 1, "type": "action", "x": 35, "y": 420, "w": 160, "h": 40, "text": "Báo Email / SĐT\nđã được đăng ký"},
                {"id": "act5", "lane": 2, "type": "action", "x": 35, "y": 350, "w": 160, "h": 45, "text": "Tạo tài khoản pending\nvà gửi mã OTP"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 490, "w": 160, "h": 45, "text": "Hiển thị màn hình\nnhập mã OTP"},
                {"id": "act7", "lane": 0, "type": "action", "x": 35, "y": 490, "w": 160, "h": 45, "text": "Nhập mã OTP từ Email\nvà nhấn Xác thực"},
                {"id": "dec3", "lane": 2, "type": "decision", "x": 50, "y": 485, "w": 130, "h": 55, "text": "Kiểm tra\nmã OTP?"},
                {"id": "err3", "lane": 1, "type": "action", "x": 35, "y": 570, "w": 160, "h": 40, "text": "Báo sai mã OTP\nhoặc hết hạn"},
                {"id": "act8", "lane": 2, "type": "action", "x": 35, "y": 570, "w": 160, "h": 45, "text": "Kích hoạt tài khoản active\nvà cấp JWT Token"},
                {"id": "act9", "lane": 1, "type": "action", "x": 35, "y": 640, "w": 160, "h": 45, "text": "Thông báo thành công\nvà đăng nhập tự động"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 720, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "act4", "label": ""},
                {"src": "act4", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "dec2", "label": "Hợp lệ"},
                {"src": "dec1", "tgt": "err1", "label": "Không hợp lệ"},
                {"src": "dec2", "tgt": "act5", "label": "Chưa tồn tại"},
                {"src": "dec2", "tgt": "err2", "label": "Đã tồn tại"},
                {"src": "act5", "tgt": "act6", "label": ""},
                {"src": "act6", "tgt": "act7", "label": ""},
                {"src": "act7", "tgt": "dec3", "label": ""},
                {"src": "dec3", "tgt": "act8", "label": "Chính xác"},
                {"src": "dec3", "tgt": "err3", "label": "Sai mã"},
                {"src": "act8", "tgt": "act9", "label": ""},
                {"src": "act9", "tgt": "end", "label": ""},
                {"src": "err1", "tgt": "end", "label": ""},
                {"src": "err2", "tgt": "end", "label": ""},
                {"src": "err3", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "2. Đăng nhập hệ thống",
            "lanes": ["Người dùng", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Chọn chức năng\nđăng nhập"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Hiển thị biểu mẫu\nđăng nhập"},
                {"id": "act3", "lane": 0, "type": "action", "x": 35, "y": 210, "w": 160, "h": 45, "text": "Nhập Email / SĐT\nvà Mật khẩu"},
                {"id": "act4", "lane": 0, "type": "action", "x": 35, "y": 300, "w": 160, "h": 45, "text": "Nhấn nút Đăng nhập"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 295, "w": 130, "h": 55, "text": "Kiểm tra\nthông tin?"},
                {"id": "err1", "lane": 1, "type": "action", "x": 35, "y": 390, "w": 160, "h": 40, "text": "Hiển thị thông báo lỗi\nsai tài khoản / mật khẩu"},
                {"id": "dec2", "lane": 1, "type": "decision", "x": 50, "y": 460, "w": 130, "h": 55, "text": "Trạng thái\ntài khoản?"},
                {"id": "err2", "lane": 1, "type": "action", "x": 35, "y": 550, "w": 160, "h": 40, "text": "Thông báo tài khoản\nđã bị khóa"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 630, "w": 160, "h": 45, "text": "Cấp mã JWT Bearer Token\nvà đăng nhập thành công"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 710, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "act4", "label": ""},
                {"src": "act4", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "dec2", "label": "Đúng mật khẩu"},
                {"src": "dec1", "tgt": "err1", "label": "Sai thông tin"},
                {"src": "dec2", "tgt": "act5", "label": "Active"},
                {"src": "dec2", "tgt": "err2", "label": "Locked"},
                {"src": "act5", "tgt": "end", "label": ""},
                {"src": "err1", "tgt": "end", "label": ""},
                {"src": "err2", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "3. Quản lý khách hàng",
            "lanes": ["Admin", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở chức năng\nQuản lý khách hàng"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Truy vấn và hiển thị\ndanh sách khách hàng"},
                {"id": "act3", "lane": 0, "type": "action", "x": 35, "y": 210, "w": 160, "h": 45, "text": "Chọn một khách hàng\ntrong danh sách"},
                {"id": "dec1", "lane": 0, "type": "decision", "x": 50, "y": 290, "w": 130, "h": 55, "text": "Chọn thao tác?"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 380, "w": 160, "h": 45, "text": "Cập nhật trạng thái\ntài khoản thành locked"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 460, "w": 160, "h": 45, "text": "Cập nhật trạng thái\ntài khoản thành active"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 540, "w": 160, "h": 45, "text": "Thông báo thành công\nvà làm mới danh sách"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 620, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act4", "label": "Khóa tài khoản"},
                {"src": "dec1", "tgt": "act5", "label": "Mở khóa"},
                {"src": "act4", "tgt": "act6", "label": ""},
                {"src": "act5", "tgt": "act6", "label": ""},
                {"src": "act6", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "4. Duyệt và Tìm kiếm sản phẩm",
            "lanes": ["Khách hàng", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Truy cập trang Cửa hàng"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Tải Banner & danh mục\nsản phẩm nổi bật"},
                {"id": "dec1", "lane": 0, "type": "decision", "x": 50, "y": 210, "w": 130, "h": 55, "text": "Chọn hình thức\nduyệt hàng?"},
                {"id": "act3", "lane": 1, "type": "action", "x": 35, "y": 290, "w": 160, "h": 40, "text": "Tìm kiếm theo từ khóa\ntên sản phẩm, SKU"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 350, "w": 160, "h": 40, "text": "Lọc theo giá, thương hiệu,\ntag HOT / NEW"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 410, "w": 160, "h": 40, "text": "Lấy sản phẩm theo\ndanh mục đã chọn"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 490, "w": 160, "h": 45, "text": "Hiển thị danh sách\nsản phẩm phù hợp"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 570, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act3", "label": "Tìm kiếm"},
                {"src": "dec1", "tgt": "act4", "label": "Bộ lọc"},
                {"src": "dec1", "tgt": "act5", "label": "Danh mục"},
                {"src": "act3", "tgt": "act6", "label": ""},
                {"src": "act4", "tgt": "act6", "label": ""},
                {"src": "act5", "tgt": "act6", "label": ""},
                {"src": "act6", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "5. Xem chi tiết & Tồn kho SKU",
            "lanes": ["Khách hàng", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Chọn xem chi tiết\nmột sản phẩm"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Truy vấn thông tin\nsản phẩm và các SKU"},
                {"id": "act3", "lane": 0, "type": "action", "x": 35, "y": 210, "w": 160, "h": 45, "text": "Chọn Màu sắc và\nKích thước (SKU)"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 205, "w": 130, "h": 55, "text": "Kiểm tra\ntồn kho SKU?"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 290, "w": 160, "h": 45, "text": "Hiển thị Còn hàng\nvà mở nút Thêm giỏ"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 360, "w": 160, "h": 45, "text": "Hiển thị Hết hàng\nvà khóa nút Thêm giỏ"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 440, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act4", "label": "Còn hàng"},
                {"src": "dec1", "tgt": "act5", "label": "Hết hàng"},
                {"src": "act4", "tgt": "end", "label": ""},
                {"src": "act5", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "6. Quản trị Catalog sản phẩm",
            "lanes": ["Admin", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở trang Quản trị Catalog"},
                {"id": "dec1", "lane": 0, "type": "decision", "x": 50, "y": 200, "w": 130, "h": 55, "text": "Chọn phân hệ\nquản lý?"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 280, "w": 160, "h": 40, "text": "Thêm/Sửa/Xóa mềm\nsản phẩm & SKU"},
                {"id": "act3", "lane": 1, "type": "action", "x": 35, "y": 340, "w": 160, "h": 40, "text": "Thêm/Sửa/Xóa\ndanh mục sản phẩm"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 400, "w": 160, "h": 40, "text": "Thêm/Sửa/Xóa\nBanner quảng cáo"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 460, "w": 160, "h": 40, "text": "Tự động cộng lại\ntồn kho SKU đơn hủy"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 530, "w": 160, "h": 45, "text": "Lưu thay đổi CSDL\nvà thông báo thành công"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 610, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act2", "label": "Sản phẩm & SKU"},
                {"src": "dec1", "tgt": "act3", "label": "Danh mục"},
                {"src": "dec1", "tgt": "act4", "label": "Banner"},
                {"src": "dec1", "tgt": "act5", "label": "Hoàn tồn kho"},
                {"src": "act2", "tgt": "act6", "label": ""},
                {"src": "act3", "tgt": "act6", "label": ""},
                {"src": "act4", "tgt": "act6", "label": ""},
                {"src": "act5", "tgt": "act6", "label": ""},
                {"src": "act6", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "7. Quản lý giỏ hàng",
            "lanes": ["Khách hàng", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Chọn SKU & Số lượng\n-> Thêm vào giỏ"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 115, "w": 130, "h": 55, "text": "Kiểm tra\ntồn kho SKU?"},
                {"id": "err1", "lane": 1, "type": "action", "x": 35, "y": 200, "w": 160, "h": 40, "text": "Báo lỗi không đủ tồn kho"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 260, "w": 160, "h": 45, "text": "Thêm vào giỏ hàng\nvà tính lại tổng tiền"},
                {"id": "act3", "lane": 0, "type": "action", "x": 35, "y": 330, "w": 160, "h": 45, "text": "Mở Giỏ hàng (Drawer)"},
                {"id": "dec2", "lane": 0, "type": "decision", "x": 50, "y": 410, "w": 130, "h": 55, "text": "Chọn thao tác\ntrên giỏ?"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 480, "w": 160, "h": 40, "text": "Cập nhật số lượng mới\nvà tính lại tổng tiền"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 540, "w": 160, "h": 40, "text": "Xóa món khỏi giỏ\nvà tính lại tổng tiền"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 600, "w": 160, "h": 40, "text": "Chuyển sang Checkout"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 670, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act2", "label": "Đủ hàng"},
                {"src": "dec1", "tgt": "err1", "label": "Không đủ"},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "dec2", "label": ""},
                {"src": "dec2", "tgt": "act4", "label": "Cập nhật SL"},
                {"src": "dec2", "tgt": "act5", "label": "Xóa món"},
                {"src": "dec2", "tgt": "act6", "label": "Thanh toán"},
                {"src": "act4", "tgt": "end", "label": ""},
                {"src": "act5", "tgt": "end", "label": ""},
                {"src": "act6", "tgt": "end", "label": ""},
                {"src": "err1", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "8. Checkout và Tạo đơn hàng",
            "lanes": ["Khách hàng", "Hệ thống & GHN"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở trang Checkout &\nchọn địa chỉ nhận hàng"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "GHN tính cước phí\nvận chuyển động"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 200, "w": 130, "h": 55, "text": "Kiểm tra tồn kho\ntoàn bộ giỏ?"},
                {"id": "err1", "lane": 1, "type": "action", "x": 35, "y": 280, "w": 160, "h": 40, "text": "Báo hết hàng và\ndừng Checkout"},
                {"id": "dec2", "lane": 0, "type": "decision", "x": 50, "y": 350, "w": 130, "h": 55, "text": "Áp dụng mã\nVoucher giảm giá?"},
                {"id": "act3", "lane": 1, "type": "action", "x": 35, "y": 430, "w": 160, "h": 45, "text": "Kiểm tra mã Voucher &\ntính số tiền giảm giá"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 500, "w": 160, "h": 45, "text": "Tính Tổng thanh toán =\nTiền hàng + Ship - Voucher"},
                {"id": "act5", "lane": 0, "type": "action", "x": 35, "y": 570, "w": 160, "h": 45, "text": "Nhấn nút Xác nhận Đặt hàng"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 570, "w": 160, "h": 45, "text": "Tạo đơn hàng pending &\nxóa giỏ hàng"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 650, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "dec2", "label": "Đủ hàng"},
                {"src": "dec1", "tgt": "err1", "label": "Hết hàng"},
                {"src": "dec2", "tgt": "act3", "label": "Có Voucher"},
                {"src": "dec2", "tgt": "act4", "label": "Không dùng"},
                {"src": "act3", "tgt": "act4", "label": ""},
                {"src": "act4", "tgt": "act5", "label": ""},
                {"src": "act5", "tgt": "act6", "label": ""},
                {"src": "act6", "tgt": "end", "label": ""},
                {"src": "err1", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "9. Thanh toán COD",
            "lanes": ["Khách hàng", "Hệ thống & Admin"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Chọn phương thức COD\nvà nhấn Xác nhận"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Ghi nhận COD &\nđặt payment_status = pending"},
                {"id": "act3", "lane": 1, "type": "action", "x": 35, "y": 200, "w": 160, "h": 45, "text": "Đóng gói & bàn giao\nđơn vị vận chuyển"},
                {"id": "act4", "lane": 0, "type": "action", "x": 35, "y": 280, "w": 160, "h": 45, "text": "Nhận kiện hàng và\nthanh toán tiền mặt cho shipper"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 350, "w": 130, "h": 55, "text": "Giao hàng và\nthu tiền COD?"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 430, "w": 160, "h": 45, "text": "Cập nhật payment_status = paid\nvà order_status = delivered"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 500, "w": 160, "h": 45, "text": "Cập nhật đơn thất bại / hoàn trả"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 580, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "act4", "label": ""},
                {"src": "act4", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act5", "label": "Thành công"},
                {"src": "dec1", "tgt": "act6", "label": "Thất bại"},
                {"src": "act5", "tgt": "end", "label": ""},
                {"src": "act6", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "10. Thanh toán MoMo Sandbox",
            "lanes": ["Khách hàng", "Hệ thống", "Cổng MoMo"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Chọn thanh toán Ví MoMo\nvà Xác nhận"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Ký số HMAC-SHA256\nvà gửi sang MoMo"},
                {"id": "act3", "lane": 2, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Khởi tạo giao dịch &\ntrả về mã QR / PayUrl"},
                {"id": "act4", "lane": 0, "type": "action", "x": 35, "y": 200, "w": 160, "h": 45, "text": "Quét mã QR và xác nhận\nthanh toán trên App MoMo"},
                {"id": "dec1", "lane": 2, "type": "decision", "x": 50, "y": 270, "w": 130, "h": 55, "text": "Kết quả\ngiao dịch MoMo?"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 350, "w": 160, "h": 45, "text": "Tiếp nhận Webhook IPN &\nxác thực chữ ký số"},
                {"id": "act6", "lane": 1, "type": "action", "x": 35, "y": 420, "w": 160, "h": 45, "text": "Cập nhật payment_status = paid\nvà thông báo thành công"},
                {"id": "act7", "lane": 1, "type": "action", "x": 35, "y": 490, "w": 160, "h": 45, "text": "Cập nhật trạng thái failed\nvà thông báo thất bại"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 570, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "act4", "label": ""},
                {"src": "act4", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act5", "label": "Thành công"},
                {"src": "dec1", "tgt": "act7", "label": "Thất bại"},
                {"src": "act5", "tgt": "act6", "label": ""},
                {"src": "act6", "tgt": "end", "label": ""},
                {"src": "act7", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "11. Theo dõi & Hủy đơn hàng",
            "lanes": ["Khách hàng", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở trang Đơn hàng của tôi\nvà chọn xem chi tiết"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 190, "w": 130, "h": 55, "text": "Trạng thái\nđơn hàng?"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 270, "w": 160, "h": 45, "text": "Hiển thị mã vận đơn &\ntra cứu lộ trình GHN"},
                {"id": "act3", "lane": 0, "type": "action", "x": 35, "y": 350, "w": 160, "h": 45, "text": "Nhấn nút Hủy đơn hàng &\nxác nhận hủy"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 430, "w": 160, "h": 45, "text": "Cập nhật order = cancelled &\nhoàn trả lại tồn kho SKU"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 510, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act2", "label": "shipping"},
                {"src": "dec1", "tgt": "act3", "label": "pending"},
                {"src": "act3", "tgt": "act4", "label": ""},
                {"src": "act2", "tgt": "end", "label": ""},
                {"src": "act4", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "12. Đánh giá sản phẩm",
            "lanes": ["Khách hàng", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Chọn sản phẩm trong\nđơn hàng đã mua"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 190, "w": 130, "h": 55, "text": "Đơn hàng\nđã delivered?"},
                {"id": "err1", "lane": 1, "type": "action", "x": 35, "y": 270, "w": 160, "h": 40, "text": "Báo đơn phải giao xong\nmới được đánh giá"},
                {"id": "dec2", "lane": 1, "type": "decision", "x": 50, "y": 330, "w": 130, "h": 55, "text": "Sản phẩm đã\nđược đánh giá?"},
                {"id": "err2", "lane": 1, "type": "action", "x": 35, "y": 410, "w": 160, "h": 40, "text": "Báo sản phẩm đã gửi\nđánh giá trước đó"},
                {"id": "act2", "lane": 0, "type": "action", "x": 35, "y": 480, "w": 160, "h": 45, "text": "Chọn số sao (1-5 sao),\nnhập nhận xét & Gửi"},
                {"id": "act3", "lane": 1, "type": "action", "x": 35, "y": 480, "w": 160, "h": 45, "text": "Lưu đánh giá & tính lại\nđiểm sao trung bình"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 560, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "dec2", "label": "Đã giao"},
                {"src": "dec1", "tgt": "err1", "label": "Chưa giao"},
                {"src": "dec2", "tgt": "act2", "label": "Chưa đánh giá"},
                {"src": "dec2", "tgt": "err2", "label": "Đã đánh giá"},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "end", "label": ""},
                {"src": "err1", "tgt": "end", "label": ""},
                {"src": "err2", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "13. Quản trị Đơn hàng & GHN",
            "lanes": ["Admin", "Hệ thống & GHN"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở Quản lý đơn hàng &\nchọn một đơn hàng"},
                {"id": "dec1", "lane": 0, "type": "decision", "x": 50, "y": 200, "w": 130, "h": 55, "text": "Chọn thao tác\nquản trị?"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 280, "w": 160, "h": 40, "text": "Cập nhật trạng thái thủ công\n(processing / delivered)"},
                {"id": "act3", "lane": 1, "type": "action", "x": 35, "y": 340, "w": 160, "h": 45, "text": "Gửi dữ liệu sang GHN &\ncấp mã Tracking 1-Click"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 410, "w": 160, "h": 40, "text": "Xác nhận thu tiền COD ->\npayment_status = paid"},
                {"id": "act5", "lane": 1, "type": "action", "x": 35, "y": 480, "w": 160, "h": 45, "text": "Thông báo thành công và\nlàm mới thông tin đơn"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 560, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act2", "label": "Chuyển trạng thái"},
                {"src": "dec1", "tgt": "act3", "label": "Tạo đơn GHN"},
                {"src": "dec1", "tgt": "act4", "label": "Thu tiền COD"},
                {"src": "act2", "tgt": "act5", "label": ""},
                {"src": "act3", "tgt": "act5", "label": ""},
                {"src": "act4", "tgt": "act5", "label": ""},
                {"src": "act5", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "14. Tư vấn trực tuyến LiveChat (Lab 7)",
            "lanes": ["Khách hàng", "Hệ thống", "Admin CSKH"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở ChatWidget tại cửa hàng\nvà nhập câu hỏi tư vấn"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Lưu tin nhắn vào CSDL\n(is_read = false)"},
                {"id": "act3", "lane": 2, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở AdminChatModal &\nnhập câu trả lời giải đáp"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 200, "w": 160, "h": 45, "text": "Lưu phản hồi và\nđánh dấu is_read = true"},
                {"id": "act5", "lane": 0, "type": "action", "x": 35, "y": 280, "w": 160, "h": 45, "text": "Khách hàng nhận được\ntin nhắn tư vấn giải đáp"},
                {"id": "end", "lane": 0, "type": "end", "x": 100, "y": 360, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "act4", "label": ""},
                {"src": "act4", "tgt": "act5", "label": ""},
                {"src": "act5", "tgt": "end", "label": ""}
            ]
        },
        {
            "title": "15. Báo cáo Tài chính & Hoàn tiền (Lab 9)",
            "lanes": ["Admin", "Hệ thống"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "x": 100, "y": 50, "w": 30, "h": 30, "text": ""},
                {"id": "act1", "lane": 0, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Mở trang Quản trị\nTài chính (Finance)"},
                {"id": "act2", "lane": 1, "type": "action", "x": 35, "y": 120, "w": 160, "h": 45, "text": "Tổng hợp doanh thu thực &\nbảng đối soát MoMo/COD"},
                {"id": "act3", "lane": 0, "type": "action", "x": 35, "y": 210, "w": 160, "h": 45, "text": "Chọn đơn hàng cần hoàn tiền\nvà chuyển sang refunded"},
                {"id": "dec1", "lane": 1, "type": "decision", "x": 50, "y": 280, "w": 130, "h": 55, "text": "Kiểm tra ràng buộc\nState Machine?"},
                {"id": "act4", "lane": 1, "type": "action", "x": 35, "y": 360, "w": 160, "h": 45, "text": "Cập nhật refunded &\ntrừ lại doanh thu thực"},
                {"id": "err1", "lane": 1, "type": "action", "x": 35, "y": 430, "w": 160, "h": 40, "text": "Báo lỗi vi phạm quy tắc\nchu trình State Machine"},
                {"id": "end", "lane": 1, "type": "end", "x": 100, "y": 510, "w": 30, "h": 30, "text": ""}
            ],
            "edges": [
                {"src": "start", "tgt": "act1", "label": ""},
                {"src": "act1", "tgt": "act2", "label": ""},
                {"src": "act2", "tgt": "act3", "label": ""},
                {"src": "act3", "tgt": "dec1", "label": ""},
                {"src": "dec1", "tgt": "act4", "label": "Hợp lệ"},
                {"src": "dec1", "tgt": "err1", "label": "Không hợp lệ"},
                {"src": "act4", "tgt": "end", "label": ""},
                {"src": "err1", "tgt": "end", "label": ""}
            ]
        }
    ]

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T21:05:00.000Z", agent="Striker Clean UML V3", version="21.0.0", type="device")

    for diag_idx, diag in enumerate(diagrams):
        diagram = ET.SubElement(mxfile, "diagram", name=diag["title"], id=f"diag_clean_{diag_idx+1}")
        num_lanes = len(diag["lanes"])
        lane_width = 230
        pool_width = num_lanes * lane_width
        
        max_y = max([node["y"] for node in diag["nodes"]]) + 100
        pool_height = max(800, max_y)

        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="700", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(pool_width + 100), pageHeight=str(pool_height + 100), math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        # Pool
        pool_id = f"pool_{diag_idx+1}"
        pool_cell = ET.SubElement(root, "mxCell", id=pool_id, value="Pool", style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=24;horizontal=1;horizontalStack=1;whiteSpace=wrap;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;", vertex="1", parent="1")
        ET.SubElement(pool_cell, "mxGeometry", x="40", y="40", width=str(pool_width), height=str(pool_height), as_="geometry")

        lane_ids = []
        for l_idx, l_name in enumerate(diag["lanes"]):
            l_id = f"lane_{diag_idx+1}_{l_idx}"
            lane_ids.append(l_id)
            l_cell = ET.SubElement(root, "mxCell", id=l_id, value=l_name, style="swimlane;html=1;startSize=28;fillColor=#ffffff;strokeColor=#000000;fontStyle=1;fontSize=12;align=center;", vertex="1", parent=pool_id)
            ET.SubElement(l_cell, "mxGeometry", x=str(l_idx * lane_width), y="24", width=str(lane_width), height=str(pool_height - 24), as_="geometry")

        # Nodes
        node_map = {}
        for n in diag["nodes"]:
            n_id = f"node_{diag_idx+1}_{n['id']}"
            node_map[n["id"]] = n_id
            parent_lane = lane_ids[n["lane"]]
            
            if n["type"] == "start":
                style = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#b85450;"
            elif n["type"] == "end":
                style = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#b85450;"
            elif n["type"] == "decision":
                style = "rhombus;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;align=center;"
            else: # action
                style = "rounded=1;whiteSpace=wrap;html=1;arcSize=40;fillColor=#fff2cc;strokeColor=#d6b656;fontColor=#000000;fontSize=11;align=center;"

            n_cell = ET.SubElement(root, "mxCell", id=n_id, value=n["text"], style=style, vertex="1", parent=parent_lane)
            ET.SubElement(n_cell, "mxGeometry", x=str(n["x"]), y=str(n["y"]), width=str(n["w"]), height=str(n["h"]), as_="geometry")

        # Edges
        for e_idx, e in enumerate(diag["edges"]):
            e_id = f"edge_{diag_idx+1}_{e_idx}"
            src = node_map[e["src"]]
            tgt = node_map[e["tgt"]]
            lbl = e.get("label", "")
            e_style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#b85450;strokeWidth=1.5;endArrow=classic;fontSize=10;fontColor=#000000;"
            
            e_cell = ET.SubElement(root, "mxCell", id=e_id, value=lbl, style=e_style, edge="1", source=src, target=tgt, parent="1")
            ET.SubElement(e_cell, "mxGeometry", relative="1", as_="geometry")

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write("c:/xampp/htdocs/PROJECT-main/PROJECT-main/docs/striker_activity_diagrams.drawio", encoding="utf-8", xml_declaration=True)
    print("Done building 15 perfectly neat UML activity diagrams!")

build_clean_activity_diagrams()
