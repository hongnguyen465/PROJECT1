import html
import xml.etree.ElementTree as ET

def create_drawio_xml():
    diagrams_data = [
        {
            "name": "1. Quản lý khách hàng",
            "swimlanes": ["Admin", "Frontend", "Auth Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Đăng nhập và mở Quản lý khách hàng"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu lấy danh sách khách hàng"},
                {"lane": 2, "type": "action", "label": "Truy vấn danh sách tài khoản"},
                {"lane": 1, "type": "action", "label": "Hiển thị danh sách khách hàng"},
                {"lane": 0, "type": "decision", "label": "Chọn thao tác?"},
                # Branch 1: Khóa
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu khóa tài khoản", "branch": "[Khóa tài khoản]"},
                {"lane": 2, "type": "decision", "label": "Đang hoạt động?"},
                {"lane": 2, "type": "action", "label": "Cập nhật trạng thái locked", "branch": "[Hợp lệ]"},
                {"lane": 1, "type": "action", "label": "Thông báo khóa thành công & làm mới"},
                # Branch 2: Mở khóa
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu mở khóa", "branch": "[Mở khóa]"},
                {"lane": 2, "type": "decision", "label": "Đang bị khóa?"},
                {"lane": 2, "type": "action", "label": "Cập nhật trạng thái active", "branch": "[Hợp lệ]"},
                {"lane": 1, "type": "action", "label": "Thông báo mở khóa thành công & làm mới"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "2. Duyệt, tìm kiếm & xem sản phẩm",
            "swimlanes": ["Khách hàng", "Frontend", "Catalog Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Truy cập website cửa hàng"},
                {"lane": 1, "type": "action", "label": "Tải Hero Banner & sản phẩm nổi bật"},
                {"lane": 2, "type": "action", "label": "Truy vấn Banner và sản phẩm"},
                {"lane": 1, "type": "action", "label": "Hiển thị trang chủ"},
                {"lane": 0, "type": "decision", "label": "Chọn phương thức?"},
                {"lane": 1, "type": "action", "label": "Gửi từ khóa tìm kiếm / bộ lọc / danh mục", "branch": "[Tìm kiếm/Lọc/Danh mục]"},
                {"lane": 2, "type": "action", "label": "Lọc và tìm kiếm sản phẩm theo điều kiện"},
                {"lane": 1, "type": "action", "label": "Hiển thị kết quả danh sách sản phẩm"},
                {"lane": 0, "type": "action", "label": "Chọn xem chi tiết sản phẩm"},
                {"lane": 1, "type": "action", "label": "Tải chi tiết sản phẩm & biến thể SKU"},
                {"lane": 2, "type": "action", "label": "Truy vấn thông tin sản phẩm và SKU tồn kho"},
                {"lane": 1, "type": "action", "label": "Hiển thị trang chi tiết sản phẩm"},
                {"lane": 0, "type": "action", "label": "Chọn Màu / Size (SKU)"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra tồn kho SKU?"},
                {"lane": 1, "type": "action", "label": "Hiển thị Còn hàng & Mở nút Mua", "branch": "[Còn hàng]"},
                {"lane": 1, "type": "action", "label": "Hiển thị Hết hàng & Khóa nút Mua", "branch": "[Hết hàng]"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "3. Quản trị Catalog sản phẩm",
            "swimlanes": ["Admin", "Frontend", "Catalog Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Đăng nhập và mở Quản trị Catalog"},
                {"lane": 1, "type": "action", "label": "Tải dữ liệu danh mục, thương hiệu, banner, sản phẩm"},
                {"lane": 2, "type": "action", "label": "Truy vấn CSDL Catalog"},
                {"lane": 1, "type": "action", "label": "Hiển thị trang Quản trị Catalog"},
                {"lane": 0, "type": "decision", "label": "Chọn phân hệ quản lý?"},
                {"lane": 0, "type": "action", "label": "Thêm / Sửa / Xóa sản phẩm & SKU", "branch": "[Sản phẩm & SKU]"},
                {"lane": 1, "type": "decision", "label": "Kiểm tra dữ liệu nhập?"},
                {"lane": 2, "type": "action", "label": "Lưu sản phẩm/SKU hoặc Xóa mềm", "branch": "[Hợp lệ]"},
                {"lane": 1, "type": "action", "label": "Thông báo cập nhật Catalog thành công"},
                {"lane": 2, "type": "action", "label": "Tự động cộng lại số lượng tồn kho SKU", "branch": "[Hoàn tồn đơn hủy]"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "4. Quản lý giỏ hàng",
            "swimlanes": ["Customer", "Frontend", "Catalog Service", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Chọn biến thể SKU & số lượng -> Thêm giỏ"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu kiểm tra tồn kho"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra số lượng tồn?"},
                {"lane": 3, "type": "action", "label": "Thêm vào giỏ & tính lại tổng tiền", "branch": "[Đủ hàng]"},
                {"lane": 1, "type": "action", "label": "Thông báo thêm thành công & cập nhật badge"},
                {"lane": 0, "type": "action", "label": "Mở Drawer Giỏ hàng"},
                {"lane": 3, "type": "action", "label": "Truy vấn danh sách mặt hàng trong giỏ"},
                {"lane": 1, "type": "action", "label": "Hiển thị danh sách giỏ hàng"},
                {"lane": 0, "type": "decision", "label": "Thao tác trên giỏ?"},
                {"lane": 3, "type": "action", "label": "Cập nhật số lượng mới trong giỏ", "branch": "[Cập nhật SL]"},
                {"lane": 3, "type": "action", "label": "Xóa sản phẩm khỏi giỏ hàng", "branch": "[Xóa món]"},
                {"lane": 1, "type": "action", "label": "Chuyển hướng sang Checkout", "branch": "[Thanh toán]"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "5. Checkout và tạo đơn hàng",
            "swimlanes": ["Customer", "Frontend", "Catalog Service", "GHN API", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Thanh toán (Checkout)"},
                {"lane": 0, "type": "action", "label": "Chọn địa chỉ nhận hàng (Tỉnh/Huyện/Xã)"},
                {"lane": 4, "type": "action", "label": "Gửi thông tin địa chỉ sang GHN"},
                {"lane": 3, "type": "action", "label": "Tính phí vận chuyển theo khoảng cách/khối lượng"},
                {"lane": 1, "type": "action", "label": "Hiển thị phí ship & gửi kiểm tra kho"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra tồn kho giỏ hàng?"},
                {"lane": 0, "type": "action", "label": "Nhập mã Voucher giảm giá (nếu có)", "branch": "[Còn hàng]"},
                {"lane": 4, "type": "decision", "label": "Kiểm tra hạn & giá trị đơn tối thiểu?"},
                {"lane": 1, "type": "action", "label": "Áp dụng giảm giá & tính Tổng thanh toán", "branch": "[Hợp lệ]"},
                {"lane": 0, "type": "action", "label": "Xác nhận Đặt hàng ngay"},
                {"lane": 4, "type": "action", "label": "Tạo đơn hàng (pending) & xóa giỏ hàng"},
                {"lane": 1, "type": "action", "label": "Chuyển sang chọn phương thức thanh toán"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "6. Thanh toán COD",
            "swimlanes": ["Customer", "Frontend", "Order Service", "Admin"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Chọn phương thức COD & Xác nhận"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu thanh toán COD"},
                {"lane": 2, "type": "action", "label": "Ghi nhận đơn COD (payment_status = pending)"},
                {"lane": 1, "type": "action", "label": "Hiển thị màn hình Đặt hàng thành công"},
                {"lane": 3, "type": "action", "label": "Đóng gói & Bàn giao bưu tá giao hàng"},
                {"lane": 0, "type": "action", "label": "Nhận hàng & trả tiền mặt cho shipper"},
                {"lane": 3, "type": "decision", "label": "Giao hàng & thu tiền thành công?"},
                {"lane": 2, "type": "action", "label": "Cập nhật payment_status = paid & order = delivered", "branch": "[Thành công]"},
                {"lane": 3, "type": "action", "label": "Hoàn tất đối soát đơn COD"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "7. Thanh toán MoMo Sandbox",
            "swimlanes": ["Customer", "Frontend", "Payment Service", "MoMo Gateway", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Chọn thanh toán Ví MoMo & Xác nhận"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu tạo giao dịch MoMo"},
                {"lane": 2, "type": "action", "label": "Tạo chữ ký số HMAC-SHA256 gửi MoMo"},
                {"lane": 3, "type": "action", "label": "Khởi tạo giao dịch & trả PayUrl / QRCode"},
                {"lane": 1, "type": "action", "label": "Hiển thị mã QR MoMo và chuyển hướng"},
                {"lane": 0, "type": "action", "label": "Quét mã QR và xác nhận thanh toán trên App MoMo"},
                {"lane": 3, "type": "decision", "label": "Xử lý giao dịch MoMo?"},
                {"lane": 3, "type": "action", "label": "Gửi Webhook IPN & Redirect Callback", "branch": "[Thành công]"},
                {"lane": 2, "type": "decision", "label": "Xác thực chữ ký số IPN?"},
                {"lane": 2, "type": "action", "label": "Cập nhật payment_status = paid", "branch": "[Hợp lệ]"},
                {"lane": 4, "type": "action", "label": "Cập nhật trạng thái đơn hàng đã thanh toán"},
                {"lane": 1, "type": "action", "label": "Hiển thị màn hình Thanh toán Thành công!"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "8. Theo dõi & Hủy đơn hàng",
            "swimlanes": ["Customer", "Frontend", "Order Service", "Catalog Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Đơn hàng của tôi"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu lấy lịch sử đơn hàng"},
                {"lane": 2, "type": "action", "label": "Truy vấn danh sách đơn hàng"},
                {"lane": 1, "type": "action", "label": "Hiển thị danh sách đơn hàng"},
                {"lane": 0, "type": "action", "label": "Chọn một đơn hàng để xem chi tiết"},
                {"lane": 2, "type": "decision", "label": "Trạng thái đơn hàng?"},
                {"lane": 1, "type": "action", "label": "Hiển thị mã vận đơn & nút tra cứu GHN", "branch": "[shipping]"},
                {"lane": 1, "type": "action", "label": "Hiển thị nút Hủy đơn hàng", "branch": "[pending]"},
                {"lane": 0, "type": "action", "label": "Xác nhận yêu cầu Hủy đơn"},
                {"lane": 2, "type": "action", "label": "Cập nhật order_status = cancelled"},
                {"lane": 3, "type": "action", "label": "Cộng bù lại số lượng tồn kho SKU"},
                {"lane": 1, "type": "action", "label": "Hiển thị thông báo hủy đơn thành công"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "9. Đánh giá sản phẩm",
            "swimlanes": ["Customer", "Frontend", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở chi tiết đơn hàng đã mua -> Chọn đánh giá"},
                {"lane": 2, "type": "decision", "label": "Đơn hàng đã delivered?"},
                {"lane": 2, "type": "decision", "label": "Đã đánh giá chưa?", "branch": "[Đã giao hàng]"},
                {"lane": 1, "type": "action", "label": "Hiển thị form Đánh giá (Số sao & Nhận xét)", "branch": "[Chưa đánh giá]"},
                {"lane": 0, "type": "action", "label": "Chọn số sao (1-5), nhập nhận xét & Gửi"},
                {"lane": 1, "type": "decision", "label": "Kiểm tra dữ liệu nhập?"},
                {"lane": 2, "type": "action", "label": "Lưu đánh giá & Tính lại điểm sao trung bình", "branch": "[Hợp lệ]"},
                {"lane": 1, "type": "action", "label": "Hiển thị thông báo đánh giá thành công & cập nhật UI"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "10. Quản trị đơn hàng & GHN Logistics",
            "swimlanes": ["Admin", "Frontend", "Order Service", "GHN API"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Quản lý đơn hàng"},
                {"lane": 2, "type": "action", "label": "Truy vấn danh sách đơn & thống kê KPI"},
                {"lane": 1, "type": "action", "label": "Hiển thị danh sách đơn & bộ lọc"},
                {"lane": 0, "type": "action", "label": "Chọn xem chi tiết một đơn hàng"},
                {"lane": 0, "type": "decision", "label": "Chọn thao tác quản trị?"},
                {"lane": 2, "type": "action", "label": "Cập nhật trạng thái thủ công (processing/delivered)", "branch": "[Chuyển trạng thái]"},
                {"lane": 2, "type": "action", "label": "Gửi thông tin kiện hàng sang GHN", "branch": "[Tạo đơn GHN 1-Click]"},
                {"lane": 3, "type": "action", "label": "Cấp mã vận đơn (Tracking Code)"},
                {"lane": 2, "type": "action", "label": "Lưu mã GHN & chuyển đơn sang shipping"},
                {"lane": 2, "type": "action", "label": "Xác nhận thu tiền COD -> payment_status = paid", "branch": "[Xác nhận COD]"},
                {"lane": 2, "type": "action", "label": "Cập nhật hoàn tiền (refund_pending/refunded)", "branch": "[Hoàn tiền]"},
                {"lane": 1, "type": "action", "label": "Làm mới chi tiết đơn hàng"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "11. Đăng ký, Đăng nhập & Xác thực OTP",
            "swimlanes": ["User", "Frontend", "Auth Service", "Mail Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "decision", "label": "Chọn chức năng?"},
                {"lane": 0, "type": "action", "label": "Nhập thông tin Đăng ký tài khoản", "branch": "[Đăng ký]"},
                {"lane": 2, "type": "action", "label": "Tạo mã OTP xác thực email/sđt"},
                {"lane": 3, "type": "action", "label": "Gửi email chứa mã OTP xác thực"},
                {"lane": 0, "type": "action", "label": "Nhập mã OTP xác thực"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra mã OTP?"},
                {"lane": 2, "type": "action", "label": "Kích hoạt tài khoản & cấp JWT Token", "branch": "[Chính xác]"},
                {"lane": 0, "type": "action", "label": "Nhập Email/SĐT & Mật khẩu", "branch": "[Đăng nhập]"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra thông tin & trạng thái?"},
                {"lane": 2, "type": "action", "label": "Cấp Bearer JWT Token & thông tin người dùng", "branch": "[Hợp lệ & Active]"},
                {"lane": 1, "type": "action", "label": "Lưu Token vào LocalStorage & chuyển trang chủ"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "12. Tư vấn trực tuyến LiveChat CSKH (Lab 7)",
            "swimlanes": ["Customer", "Frontend", "Auth Service", "Admin CSKH"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở ChatWidget tại trang mua sắm"},
                {"lane": 0, "type": "action", "label": "Nhập nội dung cần tư vấn sản phẩm & Gửi"},
                {"lane": 1, "type": "action", "label": "Gửi tin nhắn qua API Chat"},
                {"lane": 2, "type": "action", "label": "Lưu tin nhắn vào CSDL (is_read = false)"},
                {"lane": 3, "type": "action", "label": "Nhận thông báo cuộc hội thoại mới & mở AdminChat"},
                {"lane": 3, "type": "action", "label": "Nhập nội dung phản hồi giải đáp khách hàng & Gửi"},
                {"lane": 2, "type": "action", "label": "Lưu phản hồi & cập nhật trạng thái đã đọc"},
                {"lane": 1, "type": "action", "label": "Cập nhật tin nhắn phản hồi ngay tức thì"},
                {"lane": 0, "type": "action", "label": "Khách hàng nhận được tư vấn giải đáp"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        },
        {
            "name": "13. Quản trị Báo cáo Tài chính & Đối soát (Lab 9)",
            "swimlanes": ["Admin", "Frontend", "Payment Service", "Order Service"],
            "steps": [
                {"lane": 0, "type": "start", "label": ""},
                {"lane": 0, "type": "action", "label": "Mở trang Quản trị Tài chính (Finance)"},
                {"lane": 1, "type": "action", "label": "Gửi yêu cầu lấy thống kê tài chính & đối soát"},
                {"lane": 2, "type": "action", "label": "Tổng hợp doanh thu theo các đơn paid / delivered"},
                {"lane": 3, "type": "action", "label": "Truy vấn danh sách giao dịch COD & MoMo"},
                {"lane": 1, "type": "action", "label": "Hiển thị 4 KPI, Biểu đồ Spline & Bảng đối soát"},
                {"lane": 0, "type": "decision", "label": "Thao tác trên giao dịch?"},
                {"lane": 2, "type": "decision", "label": "Kiểm tra ràng buộc State Machine?", "branch": "[Duyệt hoàn tiền]"},
                {"lane": 2, "type": "action", "label": "Chuyển trạng thái refund_pending -> refunded", "branch": "[Hợp lệ]"},
                {"lane": 3, "type": "action", "label": "Ghi nhận lịch sử giao dịch và thời gian hoàn tiền"},
                {"lane": 1, "type": "action", "label": "Cập nhật lại số liệu báo cáo tài chính"},
                {"lane": 0, "type": "end", "label": ""}
            ]
        }
    ]

    mxfile = ET.Element("mxfile", host="app.diagrams.net", modified="2026-10-04T20:00:00.000Z", agent="Striker UML Generator", version="21.0.0", type="device")

    for diag_idx, diag in enumerate(diagrams_data):
        diagram = ET.SubElement(mxfile, "diagram", name=diag["name"], id=f"diag_{diag_idx+1}")
        
        num_lanes = len(diag["swimlanes"])
        lane_width = 240
        page_width = max(1169, num_lanes * lane_width + 100)
        
        mxGraphModel = ET.SubElement(diagram, "mxGraphModel", dx="1200", dy="800", grid="1", gridSize="10", guides="1", tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1", pageWidth=str(page_width), pageHeight="1400", math="0", shadow="0")
        root = ET.SubElement(mxGraphModel, "root")
        
        ET.SubElement(root, "mxCell", id="0")
        ET.SubElement(root, "mxCell", id="1", parent="0")

        # Create Pool / Swimlanes
        pool_id = f"pool_{diag_idx+1}"
        pool_height = 80 + len(diag["steps"]) * 75 + 100
        pool_cell = ET.SubElement(root, "mxCell", id=pool_id, value=diag["name"], style="swimlane;html=1;childLayout=stackLayout;resizeParent=1;resizeParentMax=0;startSize=30;horizontal=1;containerType=tree;horizontalStack=1;whiteSpace=wrap;fillColor=#1e293b;strokeColor=#0f172a;fontColor=#ffffff;fontStyle=1;fontSize=14;", vertex="1", parent="1")
        pool_geom = ET.SubElement(pool_cell, "mxGeometry", x="40", y="40", width=str(num_lanes * lane_width), height=str(pool_height), as_="geometry")

        lane_ids = []
        for lane_idx, lane_name in enumerate(diag["swimlanes"]):
            lane_id = f"lane_{diag_idx+1}_{lane_idx}"
            lane_ids.append(lane_id)
            lane_cell = ET.SubElement(root, "mxCell", id=lane_id, value=lane_name, style="swimlane;html=1;startSize=26;horizontal=0;fillColor=#f8fafc;strokeColor=#cbd5e1;fontColor=#1e293b;fontStyle=1;fontSize=12;", vertex="1", parent=pool_id)
            ET.SubElement(lane_cell, "mxGeometry", x=str(lane_idx * lane_width), y="30", width=str(lane_width), height=str(pool_height - 30), as_="geometry")

        # Create Nodes
        node_ids = []
        y_cursor = 60
        for step_idx, step in enumerate(diag["steps"]):
            node_id = f"node_{diag_idx+1}_{step_idx}"
            node_ids.append(node_id)
            lane_idx = step["lane"]
            lane_id = lane_ids[lane_idx]
            step_type = step["type"]
            label = step["label"]
            
            x_pos = (lane_width - 180) / 2
            
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
            else: # action
                style = "rounded=1;whiteSpace=wrap;html=1;arcSize=18;fillColor=#ffffff;strokeColor=#64748b;fontColor=#0f172a;fontSize=11;shadow=1;"
                w, h = 180, 42
                x_pos = (lane_width - 180) / 2

            node_cell = ET.SubElement(root, "mxCell", id=node_id, value=label, style=style, vertex="1", parent=lane_id)
            ET.SubElement(node_cell, "mxGeometry", x=str(int(x_pos)), y=str(int(y_cursor)), width=str(w), height=str(h), as_="geometry")
            
            y_cursor += 75

        # Create Edges
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
    print("File docs/striker_activity_diagrams.drawio created successfully!")

create_drawio_xml()
