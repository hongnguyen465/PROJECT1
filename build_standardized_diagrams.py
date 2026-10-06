import os
import xml.etree.ElementTree as ET

def build_perfect_diagrams():
    # Style definitions matching the user's reference image (PlantUML Classic Rose theme)
    # Background: Soft warm cream/yellow (#FEFECE), Border & Arrows: Crimson maroon (#A80036), Text: Black (#000000)
    style_action = "rounded=1;whiteSpace=wrap;html=1;arcSize=35;fillColor=#FEFECE;strokeColor=#A80036;strokeWidth=1.2;fontColor=#000000;fontSize=11;fontFamily=Helvetica;align=center;"
    style_dec = "rhombus;whiteSpace=wrap;html=1;fillColor=#FEFECE;strokeColor=#A80036;strokeWidth=1.2;fontColor=#000000;fontSize=10;fontFamily=Helvetica;align=center;"
    style_start = "ellipse;html=1;shape=startState;fillColor=#000000;strokeColor=#000000;"
    style_end = "ellipse;html=1;shape=endState;fillColor=#000000;strokeColor=#000000;"
    style_edge = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#A80036;strokeWidth=1.2;endArrow=classic;fillColor=#A80036;fontSize=10;fontColor=#000000;fontFamily=Helvetica;labelBackgroundColor=#FFFFFF;"
    style_lane = "swimlane;html=1;startSize=28;fillColor=#FFFFFF;strokeColor=#000000;fontStyle=1;fontSize=12;fontFamily=Helvetica;align=center;collapsible=0;strokeWidth=1.2;"

    lane_defs = [
        {"x": 40, "w": 180, "node_x": 60, "node_w": 140, "circle_x": 115},
        {"x": 220, "w": 180, "node_x": 240, "node_w": 140, "circle_x": 295},
        {"x": 400, "w": 190, "node_x": 425, "node_w": 140, "dec_x": 430, "dec_w": 130, "circle_x": 480},
        {"x": 590, "w": 180, "node_x": 610, "node_w": 140, "circle_x": 665}
    ]

    diagrams = [
        # =========================================================================
        # 01. USER: ĐĂNG KÝ TÀI KHOẢN (REGISTER FLOW)
        # =========================================================================
        {
            "id": "01_User_Register",
            "title": "1. [User] Đăng ký tài khoản mới",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Đăng ký &\nNhập Tên, Email, SĐT, Pass"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Validate Regex form &\nGửi POST /api/auth/register"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Gateway định tuyến request\nsang Auth Service"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn kiểm tra\ntrùng lặp Email / SĐT"},
                {"id": "be2", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Kiểm tra tính duy nhất\ncủa tài khoản người dùng"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 345, "w": 130, "h": 50, "text": "Email / SĐT khả dụng?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 348, "w": 140, "h": 45, "text": "Thông báo Email hoặc SĐT\nđã được đăng ký"},
                {"id": "err1", "lane": 1, "type": "end", "y": 425, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "be3", "lane": 2, "type": "action", "y": 435, "w": 140, "h": 45, "text": "Mã hóa Bcrypt mật khẩu &\nGán role = 'customer'"},
                {"id": "db2", "lane": 3, "type": "action", "y": 435, "w": 140, "h": 45, "text": "Lưu bản ghi mới vào\nbảng users (status: active)"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 505, "w": 140, "h": 45, "text": "Toast 'Đăng ký thành công'\n& Chuyển sang Đăng nhập"},
                {"id": "u2", "lane": 0, "type": "action", "y": 505, "w": 140, "h": 45, "text": "Sẵn sàng đăng nhập vào\nhệ thống để mua sắm"},
                {"id": "end", "lane": 0, "type": "end", "y": 575, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Đã tồn tại", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "be3", "label": "Hợp lệ", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be3", "tgt": "db2"},
                {"src": "db2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Mở trang Đăng ký &\nNhập Tên, Email, SĐT, Pass"),
                    (1, "Validate Regex form &\nGửi POST /api/auth/register"),
                    (2, "Gateway định tuyến request\nsang Auth Service"),
                    (3, "Truy vấn kiểm tra\ntrùng lặp Email / SĐT"),
                    (2, "Kiểm tra tính duy nhất\ncủa tài khoản người dùng")
                ],
                "decision": (2, "Email / SĐT khả dụng?", "Không hợp lệ (Đã tồn tại)", "Hợp lệ (Khả dụng)"),
                "err_branch": [
                    (1, "Thông báo Email hoặc SĐT\nđã được đăng ký")
                ],
                "ok_branch": [
                    (2, "Mã hóa Bcrypt mật khẩu &\nGán role = 'customer'"),
                    (3, "Lưu bản ghi mới vào\nbảng users (status: active)"),
                    (1, "Toast 'Đăng ký thành công'\n& Chuyển sang Đăng nhập"),
                    (0, "Sẵn sàng đăng nhập vào\nhệ thống để mua sắm")
                ]
            }
        },

        # =========================================================================
        # 02. USER: ĐĂNG NHẬP HỆ THỐNG (LOGIN & JWT AUTH FLOW)
        # =========================================================================
        {
            "id": "02_User_Login_JWT",
            "title": "2. [User] Đăng nhập & Xác thực JWT",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang Đăng nhập\nNhập Email & Mật khẩu"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Validate Client &\nGửi POST /api/auth/login"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Gateway định tuyến request\nsang Auth Service"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn Users bảng &\nLấy hash Bcrypt password"},
                {"id": "be2", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "So khớp Bcrypt password\n& Kiểm tra status active"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 345, "w": 130, "h": 50, "text": "Thông tin hợp lệ?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 348, "w": 140, "h": 45, "text": "Hiển thị thông báo lỗi\nSai mật khẩu / Bị khóa"},
                {"id": "err1", "lane": 1, "type": "end", "y": 425, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "be3", "lane": 2, "type": "action", "y": 435, "w": 140, "h": 45, "text": "Khởi tạo chuỗi JWT Token\n(user_id, role, expires)"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 435, "w": 140, "h": 45, "text": "Lưu Token vào LocalStorage\n& Set Axios Header Auth"},
                {"id": "u2", "lane": 0, "type": "action", "y": 505, "w": 140, "h": 45, "text": "Đăng nhập thành công &\nTruy cập tài khoản / Mua hàng"},
                {"id": "end", "lane": 0, "type": "end", "y": 575, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Không đúng", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "be3", "label": "Hợp lệ", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be3", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Mở trang Đăng nhập\nNhập Email & Mật khẩu"),
                    (1, "Validate Client &\nGửi POST /api/auth/login"),
                    (2, "Gateway định tuyến request\nsang Auth Service"),
                    (3, "Truy vấn Users bảng &\nLấy hash Bcrypt password"),
                    (2, "So khớp Bcrypt password\n& Kiểm tra status active")
                ],
                "decision": (2, "Thông tin hợp lệ?", "Không đúng (Sai Pass/Khóa)", "Hợp lệ (Đúng Pass)"),
                "err_branch": [
                    (1, "Hiển thị thông báo lỗi\nSai mật khẩu / Bị khóa")
                ],
                "ok_branch": [
                    (2, "Khởi tạo chuỗi JWT Token\n(user_id, role, expires)"),
                    (1, "Lưu Token vào LocalStorage\n& Set Axios Header Auth"),
                    (0, "Đăng nhập thành công &\nTruy cập tài khoản / Mua hàng")
                ]
            }
        },

        # =========================================================================
        # 03. USER: KHÁM PHÁ SẢN PHẨM & GIỎ HÀNG (DISCOVERY & CART FLOW)
        # =========================================================================
        {
            "id": "03_User_Discovery_Cart",
            "title": "3. [User] Khám phá sản phẩm & Quản lý giỏ hàng",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Tìm kiếm theo từ khóa\nhoặc lọc Danh mục / Giá"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi request GET /products\nkèm query params"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Catalog Service xử lý\nphân trang & truy vấn"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Lấy danh sách Products &\nVariants (Color/Size/Price)"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị Grid sản phẩm &\nChi tiết tồn kho từng SKU"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn Size, Màu sắc &\nBấm 'Thêm vào giỏ hàng'"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi POST /api/cart/items\n(user_id, sku_id, qty)"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Order Service kiểm tra\nsố lượng tồn kho khả dụng"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Đủ số lượng tồn?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Thông báo sản phẩm\nđã hết hàng hoặc vượt tồn"},
                {"id": "err1", "lane": 1, "type": "end", "y": 485, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "db2", "lane": 3, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Lưu / Cập nhật bản ghi\ntrong bảng cart_items"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Cập nhật Badge giỏ hàng &\nHiển thị Toast thành công"},
                {"id": "u3", "lane": 0, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Kiểm tra giỏ hàng &\nChuẩn bị Checkout"},
                {"id": "end", "lane": 0, "type": "end", "y": 630, "w": 30, "h": 30}
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
                {"src": "dec1", "tgt": "ui_err", "label": "Hết hàng", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db2", "label": "Đủ hàng", "exit": "exitX=1;exitY=0.5;", "entry": "entryX=0;entryY=0.5;"},
                {"src": "db2", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Tìm kiếm theo từ khóa\nhoặc lọc Danh mục / Giá"),
                    (1, "Gửi request GET /products\nkèm query params"),
                    (2, "Catalog Service xử lý\nphân trang & truy vấn"),
                    (3, "Lấy danh sách Products &\nVariants (Color/Size/Price)"),
                    (1, "Hiển thị Grid sản phẩm &\nChi tiết tồn kho từng SKU"),
                    (0, "Chọn Size, Màu sắc &\nBấm 'Thêm vào giỏ hàng'"),
                    (1, "Gửi POST /api/cart/items\n(user_id, sku_id, qty)"),
                    (2, "Order Service kiểm tra\nsố lượng tồn kho khả dụng")
                ],
                "decision": (2, "Đủ số lượng tồn kho?", "Hết hàng / Vượt tồn", "Đủ hàng khả dụng"),
                "err_branch": [
                    (1, "Thông báo sản phẩm\nđã hết hàng hoặc vượt tồn")
                ],
                "ok_branch": [
                    (3, "Lưu / Cập nhật bản ghi\ntrong bảng cart_items"),
                    (1, "Cập nhật Badge giỏ hàng &\nHiển thị Toast thành công"),
                    (0, "Kiểm tra giỏ hàng &\nChuẩn bị Checkout")
                ]
            }
        },

        # =========================================================================
        # 04. USER: CHECKOUT, TÍNH PHÍ GHN & VOUCHER (LOGISTICS & CHECKOUT FLOW)
        # =========================================================================
        {
            "id": "04_User_Checkout_GHN_Voucher",
            "title": "4. [User] Đặt hàng, Tính phí GHN & Voucher",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "GHN API & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Chọn địa chỉ nhận hàng\n(Tỉnh/Huyện/Xã) & Mã giảm"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gọi API tính phí ship &\nKiểm tra mã Voucher"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Order Service gọi GHN API\n& Tính giá trị giảm giá"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "GHN trả cước ship chính xác\n& DB trả % discount voucher"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 275, "w": 130, "h": 50, "text": "Dữ liệu hợp lệ?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 278, "w": 140, "h": 45, "text": "Báo lỗi địa chỉ chưa đúng\nhoặc Voucher hết hạn"},
                {"id": "err1", "lane": 1, "type": "end", "y": 348, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "ui2", "lane": 1, "type": "action", "y": 355, "w": 140, "h": 45, "text": "Render tổng tiền:\nTiền hàng + Ship - Voucher"},
                {"id": "u2", "lane": 0, "type": "action", "y": 355, "w": 140, "h": 45, "text": "Chọn PTTT (COD/MoMo ATM)\nvà bấm 'Đặt hàng ngay'"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Gửi POST /api/orders\nkèm toàn bộ payload đơn"},
                {"id": "be2", "lane": 2, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Kiểm tra hợp lệ lần cuối\n& Khởi tạo Transaction"},
                {"id": "db2", "lane": 3, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Lưu orders, order_items\nvà xóa giỏ hàng cart"},
                {"id": "be3", "lane": 2, "type": "action", "y": 565, "w": 140, "h": 45, "text": "Thiết lập trạng thái\nstatus = 'pending' (Chờ duyệt)"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 565, "w": 140, "h": 45, "text": "Điều hướng sang trang\nThanh toán hoặc Hoàn tất"},
                {"id": "u3", "lane": 0, "type": "action", "y": 635, "w": 140, "h": 45, "text": "Nhận mã đơn hàng &\nTheo dõi trạng thái"},
                {"id": "end", "lane": 0, "type": "end", "y": 705, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Không hợp lệ", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "ui2", "label": "Hợp lệ", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "db2"},
                {"src": "db2", "tgt": "be3"},
                {"src": "be3", "tgt": "ui4"},
                {"src": "ui4", "tgt": "u3"},
                {"src": "u3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Chọn địa chỉ nhận hàng\n(Tỉnh/Huyện/Xã) & Mã giảm"),
                    (1, "Gọi API tính phí ship &\nKiểm tra mã Voucher"),
                    (2, "Order Service gọi GHN API\n& Tính giá trị giảm giá"),
                    (3, "GHN trả cước ship chính xác\n& DB trả % discount voucher")
                ],
                "decision": (2, "Dữ liệu hợp lệ?", "Không hợp lệ (Sai địa chỉ/Hạn)", "Hợp lệ"),
                "err_branch": [
                    (1, "Báo lỗi địa chỉ chưa đúng\nhoặc Voucher hết hạn")
                ],
                "ok_branch": [
                    (1, "Render tổng tiền:\nTiền hàng + Ship - Voucher"),
                    (0, "Chọn PTTT (COD/MoMo ATM)\nvà bấm 'Đặt hàng ngay'"),
                    (1, "Gửi POST /api/orders\nkèm toàn bộ payload đơn"),
                    (2, "Kiểm tra hợp lệ lần cuối\n& Khởi tạo Transaction"),
                    (3, "Lưu orders, order_items\nvà xóa giỏ hàng cart"),
                    (2, "Thiết lập trạng thái\nstatus = 'pending' (Chờ duyệt)"),
                    (1, "Điều hướng sang trang\nThanh toán hoặc Hoàn tất"),
                    (0, "Nhận mã đơn hàng &\nTheo dõi trạng thái")
                ]
            }
        },

        # =========================================================================
        # 05. USER: XỬ LÝ THANH TOÁN (TỔNG HỢP 2 NHÁNH COD & MOMO ATM)
        # =========================================================================
        {
            "id": "05_User_Payment_COD_MoMo",
            "title": "5. [User] Thanh toán (COD & MoMo Thẻ ATM nội địa)",
            "lanes": ["Khách hàng", "Giao diện", "Payment Service", "Cổng MoMo & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Chọn Phương thức thanh toán\n(COD / Thẻ ATM MoMo)"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi yêu cầu khởi tạo GD\nPOST /api/payment/checkout"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Kiểm tra phương thức\nthanh toán đã chọn"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 275, "w": 130, "h": 50, "text": "Phương thức?"},
                # Nhánh COD (Trái)
                {"id": "be_cod", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Ghi nhận COD: unpaid\nChờ shipper GHN thu tiền"},
                {"id": "ui_cod", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Hiển thị màn hình\n'Đặt hàng COD thành công'"},
                {"id": "end_cod", "lane": 0, "type": "end", "y": 353, "w": 30, "h": 30},
                # Nhánh MoMo Thẻ ATM Nội địa (Phải)
                {"id": "be_momo", "lane": 2, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Ký số HMAC-SHA256 &\nTạo link MoMo payUrl"},
                {"id": "momo_gw", "lane": 3, "type": "action", "y": 425, "w": 140, "h": 45, "text": "MoMo cấp URL Cổng thanh toán\nThẻ ATM nội địa (Napas)"},
                {"id": "ui_redirect", "lane": 1, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Chuyển hướng trình duyệt\nsang Cổng thanh toán MoMo"},
                {"id": "u_atm", "lane": 0, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Chọn Ngân hàng, nhập Số thẻ\nATM nội địa & Nhập mã OTP"},
                {"id": "dec_otp", "lane": 3, "type": "decision", "y": 565, "w": 130, "h": 50, "text": "Xác thực OTP đúng?"},
                # OTP Sai
                {"id": "ui_otp_err", "lane": 1, "type": "action", "y": 568, "w": 140, "h": 45, "text": "Báo lỗi sai mã OTP\nhoặc số dư thẻ không đủ"},
                {"id": "end_otp_err", "lane": 1, "type": "end", "y": 638, "w": 30, "h": 30},
                # OTP Đúng
                {"id": "momo_ipn", "lane": 3, "type": "action", "y": 645, "w": 140, "h": 45, "text": "MoMo trừ tiền thẻ thành công\n& Gửi Webhook IPN (code=0)"},
                {"id": "be_ipn", "lane": 2, "type": "action", "y": 645, "w": 140, "h": 45, "text": "Xác thực chữ ký IPN &\nCập nhật status = 'paid'"},
                {"id": "ui_success", "lane": 1, "type": "action", "y": 715, "w": 140, "h": 45, "text": "Điều hướng về /payment/callback\nBáo 'Thanh toán ATM thành công'"},
                {"id": "end_momo", "lane": 0, "type": "end", "y": 723, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "be_cod", "label": "COD", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be_cod", "tgt": "ui_cod"},
                {"src": "ui_cod", "tgt": "end_cod"},
                {"src": "dec1", "tgt": "be_momo", "label": "MoMo ATM", "exit": "exitX=1;exitY=0.5;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be_momo", "tgt": "momo_gw"},
                {"src": "momo_gw", "tgt": "ui_redirect"},
                {"src": "ui_redirect", "tgt": "u_atm"},
                {"src": "u_atm", "tgt": "dec_otp"},
                {"src": "dec_otp", "tgt": "ui_otp_err", "label": "Sai OTP", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_otp_err", "tgt": "end_otp_err"},
                {"src": "dec_otp", "tgt": "momo_ipn", "label": "Thành công", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "momo_ipn", "tgt": "be_ipn"},
                {"src": "be_ipn", "tgt": "ui_success"},
                {"src": "ui_success", "tgt": "end_momo"}
            ],
            "custom_puml": """|Khách hàng|
start
:Chọn Phương thức thanh toán\\n(COD hoặc MoMo ATM);

|Giao diện|
:Gửi yêu cầu khởi tạo đơn\\nPOST /api/payment/checkout;

|Payment Service|
:Kiểm tra phương thức đã chọn;

if (Phương thức thanh toán?) then (Nhánh 1: Tiền mặt COD)
  |Payment Service|
  :Ghi nhận đơn hàng COD (unpaid)\\nChờ shipper GHN thu tiền mặt;

  |Giao diện|
  :Hiển thị màn hình\\n'Đặt hàng COD thành công';

  |Khách hàng|
  :Hoàn tất đặt đơn COD\\nChờ nhận hàng;
  stop
  detach
else (Nhánh 2: MoMo Thẻ ATM Napas)
  |Payment Service|
  :Ký số HMAC-SHA256 &\\nTạo link MoMo payUrl;

  |Cổng MoMo & CSDL|
  :MoMo cấp URL Cổng thanh toán\\nThẻ ATM nội địa (Napas);

  |Giao diện|
  :Chuyển hướng trình duyệt\\nsang Cổng thanh toán MoMo;

  |Khách hàng|
  :Chọn Ngân hàng, nhập Số thẻ\\nATM nội địa & Nhập mã OTP;

  |Cổng MoMo & CSDL|
  if (Xác thực thẻ & OTP đúng?) then (Thất bại / Sai OTP)
    |Giao diện|
    :Báo lỗi sai mã OTP\\nhoặc số dư thẻ không đủ;
    stop
    detach
  else (Thành công)
    |Cổng MoMo & CSDL|
    :MoMo trừ tiền thẻ thành công\\n& Gửi Webhook IPN (code=0);

    |Payment Service|
    :Xác thực chữ ký IPN &\\nCập nhật status = 'paid';

    |Giao diện|
    :Điều hướng về /payment/callback\\nBáo 'Thanh toán ATM thành công';

    |Khách hàng|
    :Nhận hóa đơn điện tử;
    stop
    detach
  endif
endif"""
        },

        # =========================================================================
        # 05a. USER: THANH TOÁN COD (STANDALONE CLEAN FLOW)
        # =========================================================================
        {
            "id": "05a_User_Payment_COD",
            "title": "5a. [User] Thanh toán Tiền mặt khi nhận hàng (COD)",
            "lanes": ["Khách hàng", "Giao diện", "Payment Service", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Chọn phương thức 'COD'\n& Bấm 'Đặt hàng ngay'"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi POST /api/orders\n(payment_method: 'COD')"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Payment Service khởi tạo đơn\npayment_status = 'unpaid'"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Lưu orders, order_items\n& Trừ tồn kho khả dụng"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Hiển thị màn hình\n'Đặt hàng COD thành công'"},
                {"id": "u2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Nhận mã đơn hàng & Chờ\nshipper GHN giao thu tiền"},
                {"id": "end", "lane": 0, "type": "end", "y": 345, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Chọn phương thức 'COD'\n& Bấm 'Đặt hàng ngay'"),
                    (1, "Gửi POST /api/orders\n(payment_method: 'COD')"),
                    (2, "Payment Service khởi tạo đơn\npayment_status = 'unpaid'"),
                    (3, "Lưu orders, order_items\n& Trừ tồn kho khả dụng"),
                    (1, "Hiển thị màn hình\n'Đặt hàng COD thành công'"),
                    (0, "Nhận mã đơn hàng & Chờ\nshipper GHN giao thu tiền")
                ],
                "decision": None,
                "ok_branch": []
            }
        },

        # =========================================================================
        # 05b. USER: THANH TOÁN MOMO THẺ ATM NỘI ĐỊA (STANDALONE CLEAN FLOW)
        # =========================================================================
        {
            "id": "05b_User_Payment_MoMo_ATM",
            "title": "5b. [User] Thanh toán MoMo qua Thẻ ATM nội địa (Napas)",
            "lanes": ["Khách hàng", "Giao diện", "Payment Service", "Cổng MoMo & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Chọn 'MoMo Thẻ ATM nội địa'\n& Bấm 'Thanh toán MoMo'"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi POST /api/payment/momo/start\n(payType: 'payWithATM')"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Ký số HMAC-SHA256 &\nGọi API MoMo Gateway"},
                {"id": "momo_gw", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "MoMo tiếp nhận & Cấp URL\nCổng thanh toán ATM Napas"},
                {"id": "ui_redirect", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chuyển hướng trình duyệt\nsang Cổng thanh toán MoMo"},
                {"id": "u_atm", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chọn Ngân hàng, nhập Số thẻ\nATM nội địa & Nhập mã OTP"},
                {"id": "dec_otp", "lane": 3, "type": "decision", "y": 345, "w": 130, "h": 50, "text": "Xác thực thẻ & OTP?"},
                # Thất bại
                {"id": "ui_err", "lane": 1, "type": "action", "y": 348, "w": 140, "h": 45, "text": "Báo lỗi sai mã OTP\nhoặc số dư thẻ không đủ"},
                {"id": "err1", "lane": 1, "type": "end", "y": 425, "w": 30, "h": 30},
                # Thành công
                {"id": "momo_ipn", "lane": 3, "type": "action", "y": 435, "w": 140, "h": 45, "text": "MoMo trừ tiền thẻ thành công\n& Gửi Webhook IPN (code=0)"},
                {"id": "be_ipn", "lane": 2, "type": "action", "y": 435, "w": 140, "h": 45, "text": "Xác thực chữ ký IPN &\nCập nhật status = 'paid'"},
                {"id": "db1", "lane": 3, "type": "action", "y": 505, "w": 140, "h": 45, "text": "Lưu trans_id vào bảng\npayment_transactions"},
                {"id": "ui_success", "lane": 1, "type": "action", "y": 505, "w": 140, "h": 45, "text": "Điều hướng về /payment/callback\nToast 'Thanh toán MoMo thành công'"},
                {"id": "u2", "lane": 0, "type": "action", "y": 575, "w": 140, "h": 45, "text": "Nhận hóa đơn điện tử &\nTheo dõi trạng thái đơn"},
                {"id": "end", "lane": 0, "type": "end", "y": 645, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "momo_gw"},
                {"src": "momo_gw", "tgt": "ui_redirect"},
                {"src": "ui_redirect", "tgt": "u_atm"},
                {"src": "u_atm", "tgt": "dec_otp"},
                {"src": "dec_otp", "tgt": "ui_err", "label": "Sai OTP", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec_otp", "tgt": "momo_ipn", "label": "Thành công", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "momo_ipn", "tgt": "be_ipn"},
                {"src": "be_ipn", "tgt": "db1"},
                {"src": "db1", "tgt": "ui_success"},
                {"src": "ui_success", "tgt": "u2"},
                {"src": "u2", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Chọn 'MoMo Thẻ ATM nội địa'\n& Bấm 'Thanh toán MoMo'"),
                    (1, "Gửi POST /api/payment/momo/start\n(payType: 'payWithATM')"),
                    (2, "Ký số HMAC-SHA256 &\nGọi API MoMo Gateway"),
                    (3, "MoMo tiếp nhận & Cấp URL\nCổng thanh toán ATM Napas"),
                    (1, "Chuyển hướng trình duyệt\nsang Cổng thanh toán MoMo"),
                    (0, "Chọn Ngân hàng, nhập Số thẻ\nATM nội địa & Nhập mã OTP")
                ],
                "decision": (3, "Xác thực thẻ & OTP đúng?", "Thất bại (Sai OTP/Số dư)", "Thành công"),
                "err_branch": [
                    (1, "Báo lỗi sai mã OTP\nhoặc số dư thẻ không đủ")
                ],
                "ok_branch": [
                    (3, "MoMo trừ tiền thẻ thành công\n& Gửi Webhook IPN (code=0)"),
                    (2, "Xác thực chữ ký IPN &\nCập nhật status = 'paid'"),
                    (3, "Lưu trans_id vào bảng\npayment_transactions"),
                    (1, "Điều hướng về /payment/callback\nToast 'Thanh toán MoMo thành công'"),
                    (0, "Nhận hóa đơn điện tử &\nTheo dõi trạng thái đơn")
                ]
            }
        },

        # =========================================================================
        # 06. USER: VÒNG ĐỜI SAU MUA (THEO DÕI, HỦY ĐƠN & ĐÁNH GIÁ)
        # =========================================================================
        {
            "id": "06_User_PostPurchase_Tracking_Review",
            "title": "6. [User] Theo dõi GHN, Hủy đơn & Đánh giá",
            "lanes": ["Khách hàng", "Giao diện", "Hệ thống xử lý", "GHN API & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "u1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Xem danh sách đơn hàng\ntại 'Lịch sử mua hàng'"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị trạng thái đơn &\nTracking Code GHN"},
                {"id": "u2", "lane": 0, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Chọn thao tác:\nTra cứu / Hủy / Đánh giá"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 275, "w": 130, "h": 50, "text": "Trạng thái đơn?"},
                # Hủy đơn
                {"id": "be_cancel", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Xử lý hủy đơn 'pending'\n& Hoàn lại kho SKU"},
                {"id": "ui_cancel", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Cập nhật status = cancelled"},
                {"id": "end_cancel", "lane": 0, "type": "end", "y": 353, "w": 30, "h": 30},
                # Tra cứu GHN
                {"id": "be_ghn", "lane": 2, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Order gọi GHN Tracking\nlấy lịch trình bưu tá"},
                {"id": "ui_ghn", "lane": 1, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Render Timeline lộ trình\nvận chuyển gói hàng"},
                # Đánh giá sau giao
                {"id": "u_rev", "lane": 0, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Nhận hàng (completed) &\nGửi Form 5 Sao + Review"},
                {"id": "be_rev", "lane": 2, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Catalog Service kiểm tra\nquyền mua & lưu Review"},
                {"id": "db_rev", "lane": 3, "type": "action", "y": 565, "w": 140, "h": 45, "text": "Lưu bảng reviews &\nTính lại Rating trung bình"},
                {"id": "ui_done", "lane": 1, "type": "action", "y": 565, "w": 140, "h": 45, "text": "Hiển thị đánh giá công khai\ntrên trang chi tiết SP"},
                {"id": "end_all", "lane": 0, "type": "end", "y": 635, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "u1"},
                {"src": "u1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "u2"},
                {"src": "u2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "be_cancel", "label": "Chờ duyệt (Hủy)", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be_cancel", "tgt": "ui_cancel"},
                {"src": "ui_cancel", "tgt": "end_cancel"},
                {"src": "dec1", "tgt": "be_ghn", "label": "Đang giao", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be_ghn", "tgt": "ui_ghn"},
                {"src": "ui_ghn", "tgt": "u_rev"},
                {"src": "dec1", "tgt": "u_rev", "label": "Đã giao", "exit": "exitX=1;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "u_rev", "tgt": "be_rev"},
                {"src": "be_rev", "tgt": "db_rev"},
                {"src": "db_rev", "tgt": "ui_done"},
                {"src": "ui_done", "tgt": "end_all"}
            ],
            "custom_puml": """|Khách hàng|
start
:Xem danh sách đơn hàng\\ntại 'Lịch sử mua hàng';

|Giao diện|
:Hiển thị trạng thái đơn &\\nTracking Code GHN;

|Khách hàng|
:Chọn thao tác:\\nTra cứu / Hủy / Đánh giá;

|Hệ thống xử lý|
if (Trạng thái đơn hàng?) then (Đơn chưa duyệt - Hủy đơn)
  |Hệ thống xử lý|
  :Xử lý hủy đơn 'pending'\\n& Hoàn lại kho SKU;

  |Giao diện|
  :Cập nhật status = cancelled;
  stop
  detach
else (Đơn đã hoàn tất - Đánh giá)
  |Khách hàng|
  :Nhận hàng (completed) &\\nGửi Form 5 Sao + Review;

  |Hệ thống xử lý|
  :Catalog Service kiểm tra\\nquyền mua & lưu Review;

  |GHN API & CSDL|
  :Lưu bảng reviews &\\nTính lại Rating trung bình;

  |Giao diện|
  :Hiển thị đánh giá công khai\\ntrên trang chi tiết SP;

  |Khách hàng|
  :Hoàn tất đánh giá;
  stop
  detach
endif"""
        },

        # =========================================================================
        # 07. ADMIN: QUẢN LÝ DANH MỤC & THƯƠNG HIỆU (CATEGORIES & BRANDS)
        # =========================================================================
        {
            "id": "07_Admin_Category_Brand",
            "title": "7. [Admin] Quản lý Danh mục & Thương hiệu",
            "lanes": ["Quản trị viên", "Giao diện", "Catalog Service", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Vào 'Danh mục & Hãng'\nChọn 'Thêm Danh mục mới'"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở Form nhập Tên danh mục,\nSlug, Danh mục cha & Icon"},
                {"id": "a2", "lane": 0, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Chọn Thương hiệu liên kết\nvà Bấm 'Lưu Danh mục'"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Validate Client &\nGửi POST /api/admin/categories"},
                {"id": "be1", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Kiểm tra tính duy nhất\ncủa Slug & Cây phân cấp"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 345, "w": 130, "h": 50, "text": "Slug khả dụng?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 348, "w": 140, "h": 45, "text": "Báo lỗi trùng tên danh mục\nhoặc vòng lặp cha-con"},
                {"id": "err1", "lane": 1, "type": "end", "y": 418, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "db1", "lane": 3, "type": "action", "y": 420, "w": 140, "h": 45, "text": "Lưu bản ghi vào bảng\ncategories và brands"},
                {"id": "be2", "lane": 2, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Xây dựng lại Cây danh mục\nvà Xóa Cache menu"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật Danh mục trên cây\nquản trị & Toast báo"},
                {"id": "a3", "lane": 0, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Danh mục sẵn sàng để\ngán cho Sản phẩm mới"},
                {"id": "end", "lane": 0, "type": "end", "y": 630, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "a2"},
                {"src": "a2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Trùng lặp", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db1", "label": "Hợp lệ", "exit": "exitX=1;exitY=0.5;", "entry": "entryX=0;entryY=0.5;"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "a3"},
                {"src": "a3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Vào 'Danh mục & Hãng'\nChọn 'Thêm Danh mục mới'"),
                    (1, "Mở Form nhập Tên danh mục,\nSlug, Danh mục cha & Icon"),
                    (0, "Chọn Thương hiệu liên kết\nvà Bấm 'Lưu Danh mục'"),
                    (1, "Validate Client &\nGửi POST /api/admin/categories"),
                    (2, "Kiểm tra tính duy nhất\ncủa Slug & Cây phân cấp")
                ],
                "decision": (2, "Slug khả dụng?", "Không hợp lệ (Trùng lặp/Vòng lặp)", "Hợp lệ (Khả dụng)"),
                "err_branch": [
                    (1, "Báo lỗi trùng tên danh mục\nhoặc vòng lặp cha-con")
                ],
                "ok_branch": [
                    (3, "Lưu bản ghi vào bảng\ncategories và brands"),
                    (2, "Xây dựng lại Cây danh mục\nvà Xóa Cache menu"),
                    (1, "Cập nhật Danh mục trên cây\nquản trị & Toast báo"),
                    (0, "Danh mục sẵn sàng để\ngán cho Sản phẩm mới")
                ]
            }
        },

        # =========================================================================
        # 08. ADMIN: QUẢN LÝ SẢN PHẨM & BIẾN THỂ SKUs (PRODUCTS & VARIANTS)
        # =========================================================================
        {
            "id": "08_Admin_Product_SKU",
            "title": "8. [Admin] Quản lý Sản phẩm & Biến thể SKUs",
            "lanes": ["Quản trị viên", "Giao diện", "Catalog Service", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Truy cập 'Quản lý Sản phẩm'\n& Bấm 'Thêm Sản phẩm'"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở Form nhập Tên, Danh mục,\nBrand, Mô tả chi tiết"},
                {"id": "a2", "lane": 0, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Tạo Ma trận SKU (Size, Color,\nGiá, Tồn kho) & Upload ảnh"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Validate Form &\nGửi POST /api/admin/products"},
                {"id": "be1", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Xác thực JWT Role = Admin\n& Xử lý Upload Media Gallery"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 345, "w": 130, "h": 50, "text": "Dữ liệu & SKU hợp lệ?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 348, "w": 140, "h": 45, "text": "Báo lỗi trùng mã SKU\nhoặc thiếu trường bắt buộc"},
                {"id": "err1", "lane": 1, "type": "end", "y": 418, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "db1", "lane": 3, "type": "action", "y": 420, "w": 140, "h": 45, "text": "Transaction lưu products,\nproduct_variants, images"},
                {"id": "be2", "lane": 2, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Tạo chỉ mục tìm kiếm &\nĐồng bộ kho khả dụng"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Hiển thị SP mới trên bảng\nvà Toast thông báo"},
                {"id": "a3", "lane": 0, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Sản phẩm chính thức mở bán\ntrên Storefront"},
                {"id": "end", "lane": 0, "type": "end", "y": 630, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "a2"},
                {"src": "a2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Lỗi dữ liệu", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db1", "label": "Hợp lệ", "exit": "exitX=1;exitY=0.5;", "entry": "entryX=0;entryY=0.5;"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "a3"},
                {"src": "a3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Truy cập 'Quản lý Sản phẩm'\n& Bấm 'Thêm Sản phẩm'"),
                    (1, "Mở Form nhập Tên, Danh mục,\nBrand, Mô tả chi tiết"),
                    (0, "Tạo Ma trận SKU (Size, Color,\nGiá, Tồn kho) & Upload ảnh"),
                    (1, "Validate Form &\nGửi POST /api/admin/products"),
                    (2, "Xác thực JWT Role = Admin\n& Xử lý Upload Media Gallery")
                ],
                "decision": (2, "Dữ liệu & SKU hợp lệ?", "Không hợp lệ (Lỗi SKU/Form)", "Hợp lệ"),
                "err_branch": [
                    (1, "Báo lỗi trùng mã SKU\nhoặc thiếu trường bắt buộc")
                ],
                "ok_branch": [
                    (3, "Transaction lưu products,\nproduct_variants, images"),
                    (2, "Tạo chỉ mục tìm kiếm &\nĐồng bộ kho khả dụng"),
                    (1, "Hiển thị SP mới trên bảng\nvà Toast thông báo"),
                    (0, "Sản phẩm chính thức mở bán\ntrên Storefront")
                ]
            }
        },

        # =========================================================================
        # 09. ADMIN: QUẢN TRỊ KHÁCH HÀNG & PHÂN QUYỀN
        # =========================================================================
        {
            "id": "09_Admin_Customer_Management",
            "title": "9. [Admin] Quản trị Khách hàng & Tài khoản",
            "lanes": ["Quản trị viên", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang 'Quản lý Người dùng'\n& Tìm kiếm Email / SĐT"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi GET /api/admin/users\nkèm filter status/role"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Auth Service xác thực quyền\nAdmin & lấy danh sách"},
                {"id": "db1", "lane": 3, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Truy vấn bảng users &\nuser_addresses"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Render danh sách khách hàng\nkèm nút Khóa / Đổi Role"},
                {"id": "a2", "lane": 0, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Bấm 'Khóa tài khoản' (Ban)\nhoặc Cấp quyền Admin"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Gửi PUT /api/admin/users/{id}\n(status = 'banned')"},
                {"id": "be2", "lane": 2, "type": "action", "y": 345, "w": 140, "h": 45, "text": "Kiểm tra User tồn tại &\nKhông cho tự khóa chính mình"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 415, "w": 130, "h": 50, "text": "Thao tác hợp lệ?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 418, "w": 140, "h": 45, "text": "Báo lỗi không thể khóa\nSuper Admin / Không tìm thấy"},
                {"id": "err1", "lane": 1, "type": "end", "y": 488, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "be3", "lane": 2, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Thu hồi toàn bộ Refresh\nToken của User bị khóa"},
                {"id": "db2", "lane": 3, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Cập nhật status = 'banned'\ntrong bảng users"},
                {"id": "ui4", "lane": 1, "type": "action", "y": 565, "w": 140, "h": 45, "text": "Cập nhật Badge trạng thái\nkhóa đỏ trên giao diện"},
                {"id": "a3", "lane": 0, "type": "action", "y": 565, "w": 140, "h": 45, "text": "Tài khoản bị vô hiệu hóa\nngay lập tức"},
                {"id": "end", "lane": 0, "type": "end", "y": 635, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "db1"},
                {"src": "db1", "tgt": "ui2"},
                {"src": "ui2", "tgt": "a2"},
                {"src": "a2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "be2"},
                {"src": "be2", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Vi phạm", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "be3", "label": "Hợp lệ", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be3", "tgt": "db2"},
                {"src": "db2", "tgt": "ui4"},
                {"src": "ui4", "tgt": "a3"},
                {"src": "a3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Mở trang 'Quản lý Người dùng'\n& Tìm kiếm Email / SĐT"),
                    (1, "Gửi GET /api/admin/users\nkèm filter status/role"),
                    (2, "Auth Service xác thực quyền\nAdmin & lấy danh sách"),
                    (3, "Truy vấn bảng users &\nuser_addresses"),
                    (1, "Render danh sách khách hàng\nkèm nút Khóa / Đổi Role"),
                    (0, "Bấm 'Khóa tài khoản' (Ban)\nhoặc Cấp quyền Admin"),
                    (1, "Gửi PUT /api/admin/users/{id}\n(status = 'banned')"),
                    (2, "Kiểm tra User tồn tại &\nKhông cho tự khóa chính mình")
                ],
                "decision": (2, "Thao tác hợp lệ?", "Không hợp lệ (Khóa Admin/Không tìm thấy)", "Hợp lệ"),
                "err_branch": [
                    (1, "Báo lỗi không thể khóa\nSuper Admin / Không tìm thấy")
                ],
                "ok_branch": [
                    (2, "Thu hồi toàn bộ Refresh\nToken của User bị khóa"),
                    (3, "Cập nhật status = 'banned'\ntrong bảng users"),
                    (1, "Cập nhật Badge trạng thái\nkhóa đỏ trên giao diện"),
                    (0, "Tài khoản bị vô hiệu hóa\nngay lập tức")
                ]
            }
        },

        # =========================================================================
        # 10. ADMIN: QUẢN TRỊ VOUCHER & KHUYẾN MÃI
        # =========================================================================
        {
            "id": "10_Admin_Voucher_Management",
            "title": "10. [Admin] Quản trị Voucher & Khuyến mãi",
            "lanes": ["Quản trị viên", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở trang 'Quản trị Voucher'\n& Chọn 'Tạo mã mới'"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị Form nhập Mã code,\n% giảm, Max giảm & Hạn dùng"},
                {"id": "a2", "lane": 0, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Thiết lập điều kiện: Đơn tối thiểu\n& Giới hạn lượt sử dụng"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Gửi POST /api/admin/coupons\nkèm cấu hình khuyến mãi"},
                {"id": "be1", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Kiểm tra trùng lặp mã Code\n& Hạn sử dụng tương lai"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 345, "w": 130, "h": 50, "text": "Mã hợp lệ?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 348, "w": 140, "h": 45, "text": "Báo lỗi mã Voucher đã tồn tại\nhoặc hạn dùng không hợp lệ"},
                {"id": "err1", "lane": 1, "type": "end", "y": 418, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "db1", "lane": 3, "type": "action", "y": 420, "w": 140, "h": 45, "text": "Lưu bản ghi vào bảng coupons\n(usage_limit, discount_val)"},
                {"id": "be2", "lane": 2, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Kích hoạt trạng thái Active\nvà trả về danh sách mới"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Hiển thị Voucher mới trên\nbảng quản trị & Toast báo"},
                {"id": "a3", "lane": 0, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Voucher sẵn sàng áp dụng\ntại bước Checkout KH"},
                {"id": "end", "lane": 0, "type": "end", "y": 630, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "a2"},
                {"src": "a2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Trùng mã", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db1", "label": "Hợp lệ", "exit": "exitX=1;exitY=0.5;", "entry": "entryX=0;entryY=0.5;"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "a3"},
                {"src": "a3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Mở trang 'Quản trị Voucher'\n& Chọn 'Tạo mã mới'"),
                    (1, "Hiển thị Form nhập Mã code,\n% giảm, Max giảm & Hạn dùng"),
                    (0, "Thiết lập điều kiện: Đơn tối thiểu\n& Giới hạn lượt sử dụng"),
                    (1, "Gửi POST /api/admin/coupons\nkèm cấu hình khuyến mãi"),
                    (2, "Kiểm tra trùng lặp mã Code\n& Hạn sử dụng tương lai")
                ],
                "decision": (2, "Mã Voucher hợp lệ?", "Không hợp lệ (Trùng mã/Hết hạn)", "Hợp lệ"),
                "err_branch": [
                    (1, "Báo lỗi mã Voucher đã tồn tại\nhoặc hạn dùng không hợp lệ")
                ],
                "ok_branch": [
                    (3, "Lưu bản ghi vào bảng coupons\n(usage_limit, discount_val)"),
                    (2, "Kích hoạt trạng thái Active\nvà trả về danh sách mới"),
                    (1, "Hiển thị Voucher mới trên\nbảng quản trị & Toast báo"),
                    (0, "Voucher sẵn sàng áp dụng\ntại bước Checkout KH")
                ]
            }
        },

        # =========================================================================
        # 11. ADMIN: QUẢN TRỊ BANNER & CÀI ĐẶT GIAO DIỆN
        # =========================================================================
        {
            "id": "11_Admin_Banner_Settings",
            "title": "11. [Admin] Quản trị Banner & Giao diện",
            "lanes": ["Quản trị viên", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở mục 'Quản lý Banner'\n& Chọn Thêm Banner mới"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở Form Upload ảnh Banner,\nTiêu đề & Link điều hướng"},
                {"id": "a2", "lane": 0, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Chọn ảnh Poster khuyến mãi\nvà nhập thứ tự hiển thị (Order)"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Validate file ảnh &\nGửi POST /api/admin/banners"},
                {"id": "be1", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Kiểm tra định dạng (JPG/PNG)\n& Kích thước tệp tin ảnh"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 345, "w": 130, "h": 50, "text": "Ảnh hợp lệ?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 348, "w": 140, "h": 45, "text": "Báo lỗi file ảnh sai định dạng\nhoặc vượt quá 5MB"},
                {"id": "err1", "lane": 1, "type": "end", "y": 418, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "be2", "lane": 2, "type": "action", "y": 420, "w": 140, "h": 45, "text": "Xử lý nén ảnh &\nLưu vào Storage public"},
                {"id": "db1", "lane": 3, "type": "action", "y": 420, "w": 140, "h": 45, "text": "Lưu bản ghi vào bảng banners\n(image_url, link, status)"},
                {"id": "be3", "lane": 2, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Xóa Cache Banner trang chủ\n& Đồng bộ dữ liệu mới"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 490, "w": 140, "h": 45, "text": "Cập nhật Preview Slider\ntrực tiếp trên Admin"},
                {"id": "a3", "lane": 0, "type": "action", "y": 560, "w": 140, "h": 45, "text": "Banner hiển thị trực tiếp\ntại Slider Trang chủ Store"},
                {"id": "end", "lane": 0, "type": "end", "y": 630, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "a2"},
                {"src": "a2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Lỗi file", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "be2", "label": "Hợp lệ", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "be2", "tgt": "db1"},
                {"src": "db1", "tgt": "be3"},
                {"src": "be3", "tgt": "ui3"},
                {"src": "ui3", "tgt": "a3"},
                {"src": "a3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Mở mục 'Quản lý Banner'\n& Chọn Thêm Banner mới"),
                    (1, "Mở Form Upload ảnh Banner,\nTiêu đề & Link điều hướng"),
                    (0, "Chọn ảnh Poster khuyến mãi\nvà nhập thứ tự hiển thị (Order)"),
                    (1, "Validate file ảnh &\nGửi POST /api/admin/banners"),
                    (2, "Kiểm tra định dạng (JPG/PNG)\n& Kích thước tệp tin ảnh")
                ],
                "decision": (2, "Ảnh hợp lệ?", "Không hợp lệ (Sai định dạng/Size)", "Hợp lệ"),
                "err_branch": [
                    (1, "Báo lỗi file ảnh sai định dạng\nhoặc vượt quá 5MB")
                ],
                "ok_branch": [
                    (2, "Xử lý nén ảnh &\nLưu vào Storage public"),
                    (3, "Lưu bản ghi vào bảng banners\n(image_url, link, status)"),
                    (2, "Xóa Cache Banner trang chủ\n& Đồng bộ dữ liệu mới"),
                    (1, "Cập nhật Preview Slider\ntrực tiếp trên Admin"),
                    (0, "Banner hiển thị trực tiếp\ntại Slider Trang chủ Store")
                ]
            }
        },

        # =========================================================================
        # 12. ADMIN: QUẢN TRỊ ĐƠN HÀNG & ĐẨY GHN 1-CLICK
        # =========================================================================
        {
            "id": "12_Admin_Order_GHN_1Click",
            "title": "12. [Admin] Quản trị Đơn hàng & GHN 1-Click",
            "lanes": ["Quản trị viên", "Giao diện", "Hệ thống xử lý", "GHN API & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Vào 'Quản lý Đơn hàng'\nXem danh sách đơn 'pending'"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị chi tiết khách,\nđịa chỉ & nút '1-Click GHN'"},
                {"id": "a2", "lane": 0, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Kiểm tra hàng trong kho &\nBấm nút 'Đẩy đơn sang GHN'"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Gửi POST /api/orders/{id}/ghn\nkèm trọng lượng & kích thước"},
                {"id": "be1", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Chuẩn hóa địa chỉ & Gọi API\nGHN: /shipping-order/create"},
                {"id": "dec1", "lane": 3, "type": "decision", "y": 275, "w": 130, "h": 50, "text": "GHN tiếp nhận?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 278, "w": 140, "h": 45, "text": "Báo lỗi GHN: Địa chỉ ngoài\nvùng phục vụ / Token hết hạn"},
                {"id": "err1", "lane": 1, "type": "end", "y": 348, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "ghn1", "lane": 3, "type": "action", "y": 355, "w": 140, "h": 45, "text": "GHN cấp mã vận đơn\nchính thức (tracking_code)"},
                {"id": "be2", "lane": 2, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Cập nhật order_status = 'shipping'\nkèm tracking_code & Phiếu in"},
                {"id": "db1", "lane": 3, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Lưu tracking_code vào\nbảng orders và order_logs"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Hiển thị mã vận đơn GHN\nvà nút 'In phiếu giao A5'"},
                {"id": "a3", "lane": 0, "type": "action", "y": 495, "w": 140, "h": 45, "text": "In vận đơn dán lên kiện hàng\nchờ shipper GHN tới lấy"},
                {"id": "end", "lane": 0, "type": "end", "y": 565, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "a2"},
                {"src": "a2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Lỗi GHN", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "ghn1", "label": "Thành công", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "ghn1", "tgt": "be2"},
                {"src": "be2", "tgt": "db1"},
                {"src": "db1", "tgt": "ui3"},
                {"src": "ui3", "tgt": "a3"},
                {"src": "a3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Vào 'Quản lý Đơn hàng'\nXem danh sách đơn 'pending'"),
                    (1, "Hiển thị chi tiết khách,\nđịa chỉ & nút '1-Click GHN'"),
                    (0, "Kiểm tra hàng trong kho &\nBấm nút 'Đẩy đơn sang GHN'"),
                    (1, "Gửi POST /api/orders/{id}/ghn\nkèm trọng lượng & kích thước"),
                    (2, "Chuẩn hóa địa chỉ & Gọi API\nGHN: /shipping-order/create")
                ],
                "decision": (3, "GHN tiếp nhận thành công?", "Thất bại (Lỗi địa chỉ/Token)", "Thành công (Cấp Tracking Code)"),
                "err_branch": [
                    (1, "Báo lỗi GHN: Địa chỉ ngoài\nvùng phục vụ / Token hết hạn")
                ],
                "ok_branch": [
                    (3, "GHN cấp mã vận đơn\nchính thức (tracking_code)"),
                    (2, "Cập nhật order_status = 'shipping'\nkèm tracking_code & Phiếu in"),
                    (3, "Lưu tracking_code vào\nbảng orders và order_logs"),
                    (1, "Hiển thị mã vận đơn GHN\nvà nút 'In phiếu giao A5'"),
                    (0, "In vận đơn dán lên kiện hàng\nchờ shipper GHN tới lấy")
                ]
            }
        },

        # =========================================================================
        # 13. ADMIN: BÁO CÁO DOANH THU & THỐNG KÊ (REVENUE REPORT)
        # =========================================================================
        {
            "id": "13_Admin_Revenue_Report",
            "title": "13. [Admin] Báo cáo & Thống kê Doanh thu",
            "lanes": ["Quản trị viên", "Giao diện", "Hệ thống xử lý", "Cơ sở dữ liệu"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Vào 'Báo cáo Doanh thu'\nChọn Ngày/Tháng/Năm"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Gửi GET /api/finance/revenue\n(from_date, to_date, filter)"},
                {"id": "be1", "lane": 2, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Kiểm tra tính hợp lệ\ncủa khoảng thời gian lọc"},
                {"id": "dec1", "lane": 2, "type": "decision", "y": 275, "w": 130, "h": 50, "text": "Mốc ngày hợp lệ?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 278, "w": 140, "h": 45, "text": "Báo lỗi: Ngày bắt đầu\nphải nhỏ hơn ngày kết thúc"},
                {"id": "err1", "lane": 1, "type": "end", "y": 348, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "db1", "lane": 3, "type": "action", "y": 355, "w": 140, "h": 45, "text": "Truy vấn SUM(total_amount)\ntheo thời gian & danh mục"},
                {"id": "be2", "lane": 2, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Tổng hợp doanh số bán hàng\n& Tỷ trọng COD vs MoMo"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Render Biểu đồ Cột/Đường &\nChỉ số KPI (AOV, GMV)"},
                {"id": "a2", "lane": 0, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Xem phân tích hoặc bấm\n'Xuất Excel / PDF Doanh thu'"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Tải file thống kê doanh thu\nvề máy tính Admin"},
                {"id": "end", "lane": 0, "type": "end", "y": 565, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Sai ngày", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "db1", "label": "Hợp lệ", "exit": "exitX=1;exitY=0.5;", "entry": "entryX=0;entryY=0.5;"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "a2"},
                {"src": "a2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Vào 'Báo cáo Doanh thu'\nChọn Ngày/Tháng/Năm"),
                    (1, "Gửi GET /api/finance/revenue\n(from_date, to_date, filter)"),
                    (2, "Kiểm tra tính hợp lệ\ncủa khoảng thời gian lọc")
                ],
                "decision": (2, "Mốc ngày hợp lệ?", "Không hợp lệ (Ngày bắt đầu > Ngày kết thúc)", "Hợp lệ"),
                "err_branch": [
                    (1, "Báo lỗi: Ngày bắt đầu\nphải nhỏ hơn ngày kết thúc")
                ],
                "ok_branch": [
                    (3, "Truy vấn SUM(total_amount)\ntheo thời gian & danh mục"),
                    (2, "Tổng hợp doanh số bán hàng\n& Tỷ trọng COD vs MoMo"),
                    (1, "Render Biểu đồ Cột/Đường &\nChỉ số KPI (AOV, GMV)"),
                    (0, "Xem phân tích hoặc bấm\n'Xuất Excel / PDF Doanh thu'"),
                    (1, "Tải file thống kê doanh thu\nvề máy tính Admin")
                ]
            }
        },

        # =========================================================================
        # 14. ADMIN: QUẢN LÝ TÀI CHÍNH & HOÀN TIỀN (FINANCE & REFUND)
        # =========================================================================
        {
            "id": "14_Admin_Finance_Refund",
            "title": "14. [Admin] Quản lý Tài chính & Hoàn tiền MoMo",
            "lanes": ["Quản trị viên", "Giao diện", "Payment Service", "Cổng MoMo & CSDL"],
            "nodes": [
                {"id": "start", "lane": 0, "type": "start", "y": 80, "w": 30, "h": 30},
                {"id": "a1", "lane": 0, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Mở tab 'Tài chính & Hoàn tiền'\nXem yêu cầu hoàn tiền"},
                {"id": "ui1", "lane": 1, "type": "action", "y": 135, "w": 140, "h": 45, "text": "Hiển thị mã giao dịch,\nsố tiền & lý do hủy đơn"},
                {"id": "a2", "lane": 0, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Kiểm tra điều kiện &\nBấm 'Duyệt hoàn tiền MoMo'"},
                {"id": "ui2", "lane": 1, "type": "action", "y": 205, "w": 140, "h": 45, "text": "Gửi POST /api/finance/refund\n(trans_id, amount)"},
                {"id": "be1", "lane": 2, "type": "action", "y": 275, "w": 140, "h": 45, "text": "Ký số HMAC-SHA256 &\nGọi API MoMo Refund"},
                {"id": "dec1", "lane": 3, "type": "decision", "y": 275, "w": 130, "h": 50, "text": "MoMo hoàn tất?"},
                # Nhánh Lỗi
                {"id": "ui_err", "lane": 1, "type": "action", "y": 278, "w": 140, "h": 45, "text": "Báo lỗi số dư MoMo Merchant\nhoặc giao dịch quá hạn"},
                {"id": "err1", "lane": 1, "type": "end", "y": 348, "w": 30, "h": 30},
                # Nhánh Hợp lệ
                {"id": "momo_ref", "lane": 3, "type": "action", "y": 355, "w": 140, "h": 45, "text": "MoMo xử lý chuyển tiền\nvề tài khoản của Khách hàng"},
                {"id": "db1", "lane": 3, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Cập nhật refund_status='success'\nvà lưu sổ financial_logs"},
                {"id": "be2", "lane": 2, "type": "action", "y": 425, "w": 140, "h": 45, "text": "Đồng bộ trạng thái đơn\norder_status = 'refunded'"},
                {"id": "ui3", "lane": 1, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Hiển thị Badge 'Đã hoàn tiền'\nvà Toast thông báo thành công"},
                {"id": "a3", "lane": 0, "type": "action", "y": 495, "w": 140, "h": 45, "text": "Đối soát thành công khoản\ntiền hoàn trả khách hàng"},
                {"id": "end", "lane": 0, "type": "end", "y": 565, "w": 30, "h": 30}
            ],
            "edges": [
                {"src": "start", "tgt": "a1"},
                {"src": "a1", "tgt": "ui1"},
                {"src": "ui1", "tgt": "a2"},
                {"src": "a2", "tgt": "ui2"},
                {"src": "ui2", "tgt": "be1"},
                {"src": "be1", "tgt": "dec1"},
                {"src": "dec1", "tgt": "ui_err", "label": "Thất bại", "exit": "exitX=0;exitY=0.5;", "entry": "entryX=1;entryY=0.5;"},
                {"src": "ui_err", "tgt": "err1"},
                {"src": "dec1", "tgt": "momo_ref", "label": "Thành công", "exit": "exitX=0.5;exitY=1;", "entry": "entryX=0.5;entryY=0;"},
                {"src": "momo_ref", "tgt": "db1"},
                {"src": "db1", "tgt": "be2"},
                {"src": "be2", "tgt": "ui3"},
                {"src": "ui3", "tgt": "a3"},
                {"src": "a3", "tgt": "end"}
            ],
            "puml_spec": {
                "pre": [
                    (0, "Mở tab 'Tài chính & Hoàn tiền'\nXem yêu cầu hoàn tiền"),
                    (1, "Hiển thị mã giao dịch,\nsố tiền & lý do hủy đơn"),
                    (0, "Kiểm tra điều kiện &\nBấm 'Duyệt hoàn tiền MoMo'"),
                    (1, "Gửi POST /api/finance/refund\n(trans_id, amount)"),
                    (2, "Ký số HMAC-SHA256 &\nGọi API MoMo Refund")
                ],
                "decision": (3, "MoMo hoàn tất hoàn tiền?", "Thất bại (Hết số dư/Quá hạn)", "Thành công"),
                "err_branch": [
                    (1, "Báo lỗi số dư MoMo Merchant\nhoặc giao dịch quá hạn")
                ],
                "ok_branch": [
                    (3, "MoMo xử lý chuyển tiền\nvề tài khoản của Khách hàng"),
                    (3, "Cập nhật refund_status='success'\nvà lưu sổ financial_logs"),
                    (2, "Đồng bộ trạng thái đơn\norder_status = 'refunded'"),
                    (1, "Hiển thị Badge 'Đã hoàn tiền'\nvà Toast thông báo thành công"),
                    (0, "Đối soát thành công khoản\ntiền hoàn trả khách hàng")
                ]
            }
        }
    ]

    # Create directories if not exist
    os.makedirs("docs/drawio_xml", exist_ok=True)
    os.makedirs("docs/plantuml", exist_ok=True)

    # Clean old files in docs/drawio_xml and docs/plantuml
    for f in os.listdir("docs/drawio_xml"):
        if f.endswith(".xml"):
            os.remove(os.path.join("docs/drawio_xml", f))
    for f in os.listdir("docs/plantuml"):
        if f.endswith(".puml"):
            os.remove(os.path.join("docs/plantuml", f))

    # Generate multi-page Draw.io XML
    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-05T00:25:00.000Z", agent="PlantUML Classic Rose Theme", version="21.0.0", type="device")

    for diag in diagrams:
        diagram_tag = ET.SubElement(mxfile, "diagram", id=f"diag_{diag['id']}", name=diag["title"])
        mxGraphModel = ET.SubElement(diagram_tag, "mxGraphModel", dx="1000", dy="800", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth="827", pageHeight="1169", math="0", shadow="0")
        
        # Calculate pool height dynamically
        max_y = max([n["y"] + n.get("h", 45) for n in diag["nodes"]])
        pool_h = max_y + 80

        root = ET.SubElement(mxGraphModel, "root")
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        # 4 Swimlanes
        for l_idx, l_name in enumerate(diag["lanes"]):
            l_def = lane_defs[l_idx]
            l_id = f"lane_{diag['id']}_{l_idx}"
            l_cell = ET.SubElement(root, "mxCell", id=l_id, value=l_name, style=style_lane, vertex="1", parent="1")
            ET.SubElement(l_cell, "mxGeometry", x=str(l_def["x"]), y="40", width=str(l_def["w"]), height=str(pool_h), as_="geometry")

        node_map = {}
        for n in diag["nodes"]:
            n_id = f"node_{diag['id']}_{n['id']}"
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
            e_id = f"edge_{diag['id']}_{e_idx}"
            src = node_map[e["src"]]
            tgt = node_map[e["tgt"]]
            lbl = e.get("label", "")
            
            # Custom entry/exit geometry styling
            edge_style = style_edge
            if "exit" in e:
                edge_style += e["exit"]
            if "entry" in e:
                edge_style += e["entry"]

            e_cell = ET.SubElement(root, "mxCell", id=e_id, value=lbl, style=edge_style, edge="1", source=src, target=tgt, parent="1")
            ET.SubElement(e_cell, "mxGeometry", relative="1", as_="geometry")

        # Export individual Draw.io XML with clean naming
        xml_str = ET.tostring(mxGraphModel, encoding='unicode')
        with open(f"docs/drawio_xml/So_do_{diag['id']}.xml", "w", encoding="utf-8") as f:
            f.write(xml_str)

        # Generate corresponding PlantUML code with PERFECT 2-BRANCH SYNTAX & DETACH
        lanes = diag["lanes"]
        puml_lines = [
            f"@startuml {diag['id']}",
            f"title {diag['title']}",
            "skinparam defaultFontName Helvetica",
            "skinparam ActivityFontSize 11",
            "skinparam ArrowFontSize 10",
            "skinparam ActivityBackgroundColor #FEFECE",
            "skinparam ActivityBorderColor #A80036",
            "skinparam ActivityBorderThickness 1.2",
            "skinparam ArrowColor #A80036",
            "skinparam ArrowThickness 1.2",
            "skinparam ActivityDiamondBackgroundColor #FEFECE",
            "skinparam ActivityDiamondBorderColor #A80036",
            "skinparam ActivityStartColor #000000",
            "skinparam ActivityEndColor #000000",
            ""
        ]

        if "custom_puml" in diag:
            puml_lines.append(diag["custom_puml"])
        elif "puml_spec" in diag:
            spec = diag["puml_spec"]
            # Start in lane 0
            puml_lines.append(f"|{lanes[0]}|")
            puml_lines.append("start")
            
            # Pre actions
            for l_idx, txt in spec["pre"]:
                puml_lines.append(f"|{lanes[l_idx]}|")
                clean_txt = txt.replace("\n", "\\n")
                puml_lines.append(f":{clean_txt};")
            
            if spec.get("decision"):
                dec_lane, dec_txt, err_lbl, ok_lbl = spec["decision"]
                puml_lines.append(f"|{lanes[dec_lane]}|")
                clean_dec = dec_txt.replace("\n", "\\n")
                
                # Error branch
                puml_lines.append(f"if ({clean_dec}) then ({err_lbl})")
                for l_idx, txt in spec["err_branch"]:
                    puml_lines.append(f"  |{lanes[l_idx]}|")
                    clean_txt = txt.replace("\n", "\\n")
                    puml_lines.append(f"  :{clean_txt};")
                puml_lines.append("  stop")
                puml_lines.append("  detach")
                
                # Success branch
                puml_lines.append(f"else ({ok_lbl})")
                for l_idx, txt in spec["ok_branch"]:
                    puml_lines.append(f"  |{lanes[l_idx]}|")
                    clean_txt = txt.replace("\n", "\\n")
                    puml_lines.append(f"  :{clean_txt};")
                puml_lines.append("  stop")
                puml_lines.append("  detach")
                puml_lines.append("endif")
            else:
                puml_lines.append(f"|{lanes[0]}|")
                puml_lines.append("stop")
        
        puml_lines.append("@enduml")

        with open(f"docs/plantuml/{diag['id']}.puml", "w", encoding="utf-8") as f:
            f.write("\n".join(puml_lines))

    # Write Master Draw.io file
    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write("docs/striker_activity_diagrams.drawio", encoding="utf-8", xml_declaration=True)
    print(f"SUCCESS: Generated {len(diagrams)} Diagrams with Clean Single-Index Naming!")

if __name__ == "__main__":
    build_perfect_diagrams()
