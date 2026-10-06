import xml.etree.ElementTree as ET

def update_drawio_file():
    diagrams = [
        {
            "name": "1. Đăng ký tài khoản & Xác thực OTP",
            "swimlanes": ["User", "Frontend", "Auth Service", "Mail Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Nhập Họ tên, Email, SĐT và Mật khẩu"},
                {"lane": 1, "type": "decision", "label": "Dữ liệu hợp lệ?"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra trùng lặp Email/SĐT?", "branch": "[Hợp lệ]"},
                {"lane": 2, "type": "action", "label": "Tạo tài khoản pending & mã OTP", "branch": "[Chưa tồn tại]"},
                {"lane": 3, "type": "action", "label": "Gửi email chứa mã OTP xác thực"},
                {"lane": 1, "type": "action", "label": "Hiển thị màn hình nhập mã OTP"},
                {"lane": 0, "type": "action", "label": "Nhập mã OTP nhận từ email"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra mã OTP?"},
                {"lane": 2, "type": "action", "label": "Kích hoạt active & cấp JWT Token", "branch": "[Chính xác & Còn hạn]"},
                {"lane": 1, "type": "action", "label": "Lưu Token & đăng nhập thành công"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "2. Đăng nhập hệ thống",
            "swimlanes": ["User", "Frontend", "Auth Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Nhập Email/SĐT và Mật khẩu"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu đăng nhập"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra thông tin đăng nhập?"},
                {"lane": 2, "type": "decision", "label": "Trạng thái tài khoản?", "branch": "[Đúng mật khẩu]"},
                {"lane": 2, "type": "action", "label": "Cấp Bearer JWT Token kèm Role", "branch": "[Active]"},
                {"lane": 1, "type": "action", "label": "Lưu Token vào LocalStorage & chuyển trang chủ"},
                {"lane": 1, "type": "action", "label": "Thông báo tài khoản bị khóa", "branch": "[Locked]"},
                {"lane": 1, "type": "action", "label": "Thông báo sai tài khoản hoặc mật khẩu", "branch": "[Sai mật khẩu]"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "3. Quản lý khách hàng",
            "swimlanes": ["Admin", "Frontend", "Auth Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở chức năng Quản lý khách hàng"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu lấy danh sách khách hàng"},
                {"lane": 2, "type": "action", "label": "Truy vấn danh sách tài khoản"},
                {"lane": 1, "type": "action", "label": "Hiển thị danh sách khách hàng"},
                {"lane": 0, "type": "decision", "label": "Chọn thao tác?"},
                {"lane": 2, "type": "action", "label": "Cập nhật trạng thái thành locked", "branch": "[Khóa tài khoản]"},
                {"lane": 2, "type": "action", "label": "Cập nhật trạng thái thành active", "branch": "[Mở khóa tài khoản]"},
                {"lane": 1, "type": "action", "label": "Thông báo thành công & làm mới danh sách"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "4. Duyệt và Tìm kiếm sản phẩm",
            "swimlanes": ["Khách hàng", "Frontend", "Catalog Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Truy cập trang Cửa hàng (Shop)"},
                {"lane": 1, "type": "action", "label": "Tải Banner và danh mục sản phẩm"},
                {"lane": 2, "type": "action", "label": "Truy vấn dữ liệu sản phẩm & banner"},
                {"lane": 1, "type": "action", "label": "Hiển thị danh sách sản phẩm"},
                {"lane": 0, "type": "decision", "label": "Chọn thao tác duyệt?"},
                {"lane": 2, "type": "action", "label": "Tìm kiếm theo từ khóa tên/SKU", "branch": "[Tìm kiếm]"},
                {"lane": 2, "type": "action", "label": "Lọc theo giá, thương hiệu, HOT/NEW", "branch": "[Bộ lọc]"},
                {"lane": 2, "type": "action", "label": "Lấy sản phẩm theo danh mục", "branch": "[Danh mục]"},
                {"lane": 1, "type": "action", "label": "Hiển thị kết quả danh sách sản phẩm"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "5. Xem chi tiết & Kiểm tra tồn kho",
            "swimlanes": ["Khách hàng", "Frontend", "Catalog Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Chọn một sản phẩm để xem chi tiết"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu lấy chi tiết sản phẩm & SKU"},
                {"lane": 2, "type": "action", "label": "Truy vấn thông tin sản phẩm và các biến thể"},
                {"lane": 1, "type": "action", "label": "Hiển thị trang chi tiết sản phẩm"},
                {"lane": 0, "type": "action", "label": "Chọn Màu sắc và Kích thước (SKU)"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra số lượng tồn kho biến thể?"},
                {"lane": 1, "type": "action", "label": "Hiển thị Còn hàng & Mở nút Mua", "branch": "[Còn hàng]"},
                {"lane": 1, "type": "action", "label": "Hiển thị Hết hàng & Khóa nút Mua", "branch": "[Hết hàng]"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "6. Quản trị Catalog sản phẩm",
            "swimlanes": ["Admin", "Frontend", "Catalog Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Quản trị Catalog"},
                {"lane": 1, "type": "action", "label": "Tải dữ liệu quản trị sản phẩm, danh mục, banner"},
                {"lane": 0, "type": "decision", "label": "Chọn phân hệ quản lý?"},
                {"lane": 2, "type": "action", "label": "Thêm/Sửa/Xóa mềm sản phẩm và biến thể SKU", "branch": "[Sản phẩm & SKU]"},
                {"lane": 2, "type": "action", "label": "Thêm/Sửa/Xóa danh mục sản phẩm", "branch": "[Danh mục]"},
                {"lane": 2, "type": "action", "label": "Thêm/Sửa/Xóa Banner quảng cáo", "branch": "[Banner]"},
                {"lane": 2, "type": "action", "label": "Tự động hoàn trả tồn kho SKU do đơn hủy", "branch": "[Hoàn tồn kho]"},
                {"lane": 1, "type": "action", "label": "Thông báo cập nhật Catalog thành công"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "7. Quản lý giỏ hàng",
            "swimlanes": ["Customer", "Frontend", "Catalog Service", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Chọn SKU & Số lượng -> Thêm vào giỏ"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra tồn kho SKU?"},
                {"lane": 3, "type": "action", "label": "Thêm sản phẩm vào giỏ & tính lại tổng", "branch": "[Đủ hàng]"},
                {"lane": 1, "type": "action", "label": "Thông báo thêm thành công & mở Giỏ hàng"},
                {"lane": 0, "type": "decision", "label": "Chọn thao tác trên giỏ?"},
                {"lane": 3, "type": "action", "label": "Cập nhật số lượng mới & tính lại tiền", "branch": "[Cập nhật SL]"},
                {"lane": 3, "type": "action", "label": "Xóa sản phẩm khỏi giỏ hàng", "branch": "[Xóa món]"},
                {"lane": 1, "type": "action", "label": "Chuyển sang trang Checkout", "branch": "[Thanh toán]"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "8. Checkout và Tạo đơn hàng",
            "swimlanes": ["Customer", "Frontend", "Catalog Service", "GHN API", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở Checkout & Chọn địa chỉ nhận hàng"},
                {"lane": 3, "type": "action", "label": "Tính phí vận chuyển theo Tỉnh/Huyện/Xã"},
                {"lane": 1, "type": "action", "label": "Hiển thị phí ship & kiểm tra tồn kho"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra tồn kho giỏ hàng?"},
                {"lane": 0, "type": "action", "label": "Nhập mã Voucher giảm giá", "branch": "[Còn hàng]"},
                {"lane": 4, "type": "decision", "label": "Kiểm tra hạn & điều kiện đơn tối thiểu?"},
                {"lane": 1, "type": "action", "label": "Áp dụng giảm giá & tính Tổng thanh toán", "branch": "[Hợp lệ]"},
                {"lane": 0, "type": "action", "label": "Nhấn nút Xác nhận Đặt hàng ngay"},
                {"lane": 4, "type": "action", "label": "Tạo đơn hàng (pending) & xóa giỏ hàng"},
                {"lane": 1, "type": "action", "label": "Chuyển sang bước chọn phương thức thanh toán"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "9. Thanh toán COD",
            "swimlanes": ["Customer", "Frontend", "Order Service", "Admin"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Chọn phương thức COD & Xác nhận"},
                {"lane": 2, "type": "action", "label": "Ghi nhận đơn COD (payment_status = pending)"},
                {"lane": 1, "type": "action", "label": "Hiển thị màn hình Đặt hàng thành công"},
                {"lane": 3, "type": "action", "label": "Đóng gói & Bàn giao đơn vị vận chuyển"},
                {"lane": 0, "type": "action", "label": "Nhận hàng & Thanh toán tiền mặt cho shipper"},
                {"lane": 3, "type": "decision", "label": "Giao hàng & thu tiền thành công?"},
                {"lane": 2, "type": "action", "label": "Cập nhật payment_status = paid & order = delivered", "branch": "[Thành công]"},
                {"lane": 3, "type": "action", "label": "Hoàn tất đối soát tiền COD"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "10. Thanh toán MoMo Sandbox",
            "swimlanes": ["Customer", "Frontend", "Payment Service", "MoMo Gateway", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Chọn thanh toán Ví MoMo & Xác nhận"},
                {"lane": 2, "type": "action", "label": "Tạo chữ ký số HMAC-SHA256 gửi sang MoMo"},
                {"lane": 3, "type": "action", "label": "Khởi tạo giao dịch & trả về QR Code / PayUrl"},
                {"lane": 1, "type": "action", "label": "Hiển thị mã QR MoMo và chuyển hướng"},
                {"lane": 0, "type": "action", "label": "Quét mã QR và xác nhận thanh toán trên App MoMo"},
                {"lane": 3, "type": "decision", "label": "Kết quả thanh toán MoMo?"},
                {"lane": 2, "type": "action", "label": "Xác thực chữ ký số IPN Webhook", "branch": "[Thành công]"},
                {"lane": 2, "type": "action", "label": "Cập nhật payment_status = paid"},
                {"lane": 4, "type": "action", "label": "Cập nhật trạng thái đơn hàng đã thanh toán"},
                {"lane": 1, "type": "action", "label": "Hiển thị màn hình Thanh toán Thành công!"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "11. Theo dõi & Hủy đơn hàng",
            "swimlanes": ["Customer", "Frontend", "Order Service", "Catalog Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Đơn hàng của tôi & Xem chi tiết"},
                {"lane": 2, "type": "decision", "label": "Trạng thái đơn hàng hiện tại?"},
                {"lane": 1, "type": "action", "label": "Hiển thị mã vận đơn & Tra cứu lộ trình GHN", "branch": "[shipping]"},
                {"lane": 1, "type": "action", "label": "Hiển thị nút Hủy đơn hàng", "branch": "[pending]"},
                {"lane": 0, "type": "action", "label": "Xác nhận yêu cầu Hủy đơn"},
                {"lane": 2, "type": "action", "label": "Cập nhật order_status = cancelled"},
                {"lane": 3, "type": "action", "label": "Cộng bù lại số lượng tồn kho cho các SKU"},
                {"lane": 1, "type": "action", "label": "Hiển thị thông báo hủy đơn thành công"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "12. Đánh giá sản phẩm",
            "swimlanes": ["Customer", "Frontend", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở chi tiết đơn hàng đã mua -> Chọn đánh giá"},
                {"lane": 2, "type": "decision", "label": "Đơn hàng đã delivered?"},
                {"lane": 2, "type": "decision", "label": "Sản phẩm đã được đánh giá chưa?", "branch": "[Đã giao hàng]"},
                {"lane": 1, "type": "action", "label": "Hiển thị biểu mẫu Đánh giá (Số sao & Nhận xét)", "branch": "[Chưa đánh giá]"},
                {"lane": 0, "type": "action", "label": "Chọn số sao (1-5), nhập nhận xét & Gửi"},
                {"lane": 2, "type": "action", "label": "Lưu đánh giá & Tính lại điểm sao trung bình"},
                {"lane": 1, "type": "action", "label": "Hiển thị thông báo đánh giá thành công & cập nhật UI"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "13. Quản trị đơn hàng & GHN",
            "swimlanes": ["Admin", "Frontend", "Order Service", "GHN API"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Quản lý đơn hàng & Lọc đơn"},
                {"lane": 0, "type": "decision", "label": "Chọn thao tác quản trị?"},
                {"lane": 2, "type": "action", "label": "Cập nhật trạng thái thủ công (processing/delivered)", "branch": "[Chuyển trạng thái]"},
                {"lane": 2, "type": "action", "label": "Gửi thông tin kiện hàng sang GHN Logistics", "branch": "[Tạo đơn GHN 1-Click]"},
                {"lane": 3, "type": "action", "label": "Cấp mã vận đơn (Tracking Code)"},
                {"lane": 2, "type": "action", "label": "Lưu mã GHN & chuyển đơn sang shipping"},
                {"lane": 2, "type": "action", "label": "Xác nhận thu tiền COD -> payment_status = paid", "branch": "[Xác nhận COD]"},
                {"lane": 1, "type": "action", "label": "Làm mới chi tiết đơn hàng & thông báo thành công"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "14. Tư vấn trực tuyến LiveChat (Lab 7)",
            "swimlanes": ["Customer", "Frontend", "Auth Service", "Admin CSKH"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở ChatWidget tại cửa hàng & Nhập câu hỏi"},
                {"lane": 1, "type": "action", "label": "Gửi tin nhắn qua API Chat"},
                {"lane": 2, "type": "action", "label": "Lưu tin nhắn vào CSDL (is_read = false)"},
                {"lane": 3, "type": "action", "label": "Mở bàn trực CSKH (AdminChatModal) & Trả lời"},
                {"lane": 2, "type": "action", "label": "Lưu phản hồi & Cập nhật trạng thái đã đọc"},
                {"lane": 1, "type": "action", "label": "Hiển thị phản hồi CSKH trên khung chat khách"},
                {"lane": 0, "type": "action", "label": "Khách hàng nhận được tư vấn giải đáp"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "15. Báo cáo Tài chính & Hoàn tiền (Lab 9)",
            "swimlanes": ["Admin", "Frontend", "Payment Service", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Quản trị Tài chính (Finance)"},
                {"lane": 2, "type": "action", "label": "Tổng hợp doanh thu từ các đơn delivered / paid"},
                {"lane": 3, "type": "action", "label": "Truy vấn danh sách giao dịch COD & MoMo"},
                {"lane": 1, "type": "action", "label": "Hiển thị 4 KPI, Biểu đồ Spline & Bảng đối soát"},
                {"lane": 0, "type": "action", "label": "Chọn đơn hàng hoàn tiền & Chuyển trạng thái refunded"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra ràng buộc State Machine tài chính?"},
                {"lane": 2, "type": "action", "label": "Cập nhật trạng thái refunded & Ghi log", "branch": "[Hợp lệ]"},
                {"lane": 3, "type": "action", "label": "Đồng bộ trạng thái thanh toán đơn hàng"},
                {"lane": 1, "type": "action", "label": "Thông báo hoàn tiền thành công & Cập nhật doanh thu"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        }
    ]

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T20:55:00.000Z", agent="Striker UML Generator V2", version="21.0.0", type="device")

    for diag_idx, diag in enumerate(diagrams):
        diagram = ET.SubElement(mxfile, "diagram", name=diag["name"], id=f"diag_{diag_idx+1}")
        num_lanes = len(diag["swimlanes"])
        lane_width = 240
        page_width = max(1169, num_lanes * lane_width + 100)
        
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1200", dy="800", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(page_width), pageHeight="1400", math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        pool_id = f"pool_{diag_idx+1}"
        pool_height = 80 + len(diag["steps"]) * 75 + 100
        pool_cell = ET.SubElement(root, "mxCell", id=pool_id, value=diag["name"], style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=30;horizontal=1;containerType=tree;horizontalStack=1;whiteSpace=wrap;fillColor=#1e293b;strokeColor=#0f172a;fontColor=#ffffff;fontStyle=1;fontSize=14;", vertex="1", parent="1")
        ET.SubElement(pool_cell, "mxGeometry", x="40", y="40", width=str(num_lanes * lane_width), height=str(pool_height), as_="geometry")

        lane_ids = []
        for lane_idx, lane_name in enumerate(diag["swimlanes"]):
            lane_id = f"lane_{diag_idx+1}_{lane_idx}"
            lane_ids.append(lane_id)
            lane_cell = ET.SubElement(root, "mxCell", id=lane_id, value=lane_name, style="swimlane;html=1;startSize=26;horizontal=0;fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#1e293b;fontStyle=1;fontSize=12;", vertex="1", parent=pool_id)
            ET.SubElement(lane_cell, "mxGeometry", x=str(lane_idx * lane_width), y="30", width=str(lane_width), height=str(pool_height - 30), as_="geometry")

        node_ids = []
        y_cursor = 60
        for step_idx, step in enumerate(diag["steps"]):
            node_id = f"node_{diag_idx+1}_{step_idx}"
            node_ids.append(node_id)
            lane_idx = step["lane"]
            lane_id = lane_ids[lane_idx]
            step_type = step["type"]
            label = step["label"]
            
            if step_type == "start":
                style = "ellipse;fillColor=#10b981;strokeColor=#059669;html=1;shape=startState;"
                w, h = 32, 32
                x_pos = (lane_width - 32) / 2
            elif step_type == "end":
                style = "ellipse;html=1;shape=endState;fillColor=#ef4444;strokeColor=#b91c1c;"
                w, h = 32, 32
                x_pos = (lane_width - 32) / 2
            elif step_type == "decision":
                style = "rhombus;whiteSpace=wrap;html=1;fillColor=#fef3c7;strokeColor=#d97706;fontColor=#78350f;fontSize=11;fontStyle=1;"
                w, h = 170, 50
                x_pos = (lane_width - 170) / 2
            else:
                style = "rounded=1;whiteSpace=wrap;html=1;arcSize=18;fillColor=#ffffff;strokeColor=#64748b;fontColor=#0f172a;fontSize=11;shadow=1;"
                w, h = 180, 42
                x_pos = (lane_width - 180) / 2

            node_cell = ET.SubElement(root, "mxCell", id=node_id, value=label, style=style, vertex="1", parent=lane_id)
            ET.SubElement(node_cell, "mxGeometry", x=str(int(x_pos)), y=str(int(y_cursor)), width=str(w), height=str(h), as_="geometry")
            y_cursor += 75

        for step_idx in range(len(diag["steps"]) - 1):
            edge_id = f"edge_{diag_idx+1}_{step_idx}"
            src_id = node_ids[step_idx]
            tgt_id = node_ids[step_idx+1]
            branch_label = diag["steps"][step_idx+1].get("branch", "")
            edge_style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#334155;strokeWidth=1.5;endArrow=classic;endFill=1;fontSize=10;fontColor=#2563eb;"
            edge_cell = ET.SubElement(root, "mxCell", id=edge_id, value=branch_label, style=edge_style, edge="1", source=src_id, target=tgt_id, parent="1")
            ET.SubElement(edge_cell, "mxGeometry", relative="1", as_="geometry")

    tree = ET.ElementTree(mxfile)
    ET.indent(tree, space="  ", level=0)
    tree.write("c:/xampp/htdocs/PROJECT-main/PROJECT-main/docs/striker_activity_diagrams.drawio", encoding="utf-8", xml_declaration=True)
    print("Updated docs/striker_activity_diagrams.drawio with 15 diagrams!")

update_drawio_file()
