import React, { useState, useEffect, useMemo } from 'react';
import { 
  DollarSign, 
  CreditCard, 
  TrendingUp, 
  Filter, 
  Search, 
  Wallet, 
  RefreshCw, 
  CheckCircle2,
  Truck,
  Clock,
  XCircle,
  PhoneCall,
  Package
} from 'lucide-react';
import { toast } from 'sonner';
import { fetchAdminOrders } from '../../services/orders';

// 2 Phương thức thanh toán chính thức
const METHODS: Record<'cod' | 'momo', { label: string; badgeBg: string }> = {
  cod: { label: 'COD Tiền mặt', badgeBg: 'bg-amber-500/10 border-amber-500/30 text-amber-400' },
  momo: { label: 'MoMo AIO', badgeBg: 'bg-pink-500/10 border-pink-500/30 text-pink-400' },
};

interface RawOrder {
  id: number;
  order_code?: string;
  order_number?: string;
  shipping_name?: string;
  shipping_phone?: string;
  shipping_address?: string;
  phone?: string;
  user?: { name?: string };
  total_amount?: number;
  total_price?: number;
  subtotal?: number;
  discount_amount?: number;
  shipping_fee?: number;
  payment_method?: string;
  payment_status?: string;
  order_status?: string;
  status?: string;
  created_at?: string;
  note?: string;
  calculated_gateway: 'cod' | 'momo';
  calculated_status: string;
  is_paid: boolean;
}

export const Finance: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'summary' | 'transactions'>('summary');
  const [orders, setOrders] = useState<RawOrder[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  // Bộ lọc tài chính thực tế
  const [filters, setFilters] = useState({
    search: '',
    date_from: '',
    date_to: '',
    min_amount: '',
    max_amount: '',
    gateway: '',
    status: '',
    sort: 'newest',
  });

  // Tải dữ liệu đơn hàng
  const loadOrders = async () => {
    try {
      setLoading(true);
      const res = await fetchAdminOrders({ per_page: 100 });
      const rawList = Array.isArray(res) 
        ? res 
        : (res?.data && Array.isArray(res.data) ? res.data : (res?.orders && Array.isArray(res.orders) ? res.orders : []));
      setOrders(rawList);
    } catch {
      toast.error('Không thể tải dữ liệu báo cáo tài chính');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadOrders();
  }, []);

  // Chuẩn hóa trạng thái đơn hàng & thanh toán thực tế
  const normalizedOrders = useMemo<RawOrder[]>(() => {
    return orders.map(order => {
      const pm = (order.payment_method || '').toLowerCase();
      const gateway: 'cod' | 'momo' = pm.includes('momo') ? 'momo' : 'cod';

      const rawPay = (order.payment_status || '').toLowerCase();
      const rawOrd = (order.order_status || order.status || '').toLowerCase();

      let ordStatus = 'pending';
      let isPaid = false;

      // 1. Nếu đơn bị hủy
      if (rawOrd === 'cancelled' || rawOrd === 'cancel') {
        ordStatus = 'cancelled';
        isPaid = false;
      } 
      // 2. Đã giao hàng thành công (Thực thu)
      else if (rawOrd === 'delivered') {
        ordStatus = 'delivered';
        isPaid = true;
      } 
      // 3. Đang giao hàng
      else if (rawOrd === 'shipping') {
        ordStatus = 'shipping';
        isPaid = (gateway === 'momo' && rawPay === 'paid');
      } 
      // 4. Đang đóng gói / lấy hàng
      else if (rawOrd === 'processing') {
        ordStatus = 'processing';
        isPaid = (gateway === 'momo' && rawPay === 'paid');
      } 
      // 5. Chờ xử lý
      else {
        ordStatus = 'pending';
        isPaid = (gateway === 'momo' && rawPay === 'paid');
      }

      return {
        ...order,
        calculated_gateway: gateway,
        calculated_status: ordStatus,
        is_paid: isPaid,
      };
    });
  }, [orders]);

  // Áp dụng bộ lọc
  const filteredOrders = useMemo(() => {
    return normalizedOrders.filter(order => {
      // 1. Search (Mã đơn, tên, sđt)
      if (filters.search) {
        const s = filters.search.toLowerCase().trim();
        const code = (order.order_code || order.order_number || `#${order.id}`).toLowerCase();
        const name = (order.shipping_name || order.user?.name || '').toLowerCase();
        const phone = (order.shipping_phone || order.phone || '').toLowerCase();
        if (!code.includes(s) && !name.includes(s) && !phone.includes(s)) {
          return false;
        }
      }

      // 2. Date From
      if (filters.date_from) {
        const orderDate = new Date(order.created_at || '').getTime();
        const fromDate = new Date(`${filters.date_from}T00:00:00`).getTime();
        if (orderDate < fromDate) return false;
      }

      // 3. Date To
      if (filters.date_to) {
        const orderDate = new Date(order.created_at || '').getTime();
        const toDate = new Date(`${filters.date_to}T23:59:59`).getTime();
        if (orderDate > toDate) return false;
      }

      // 4. Min Amount
      const amount = Number(order.total_amount ?? order.total_price ?? 0);
      if (filters.min_amount && amount < Number(filters.min_amount)) {
        return false;
      }

      // 5. Max Amount
      if (filters.max_amount && amount > Number(filters.max_amount)) {
        return false;
      }

      // 6. Gateway (COD / MoMo)
      if (filters.gateway && order.calculated_gateway !== filters.gateway) {
        return false;
      }

      // 7. Status
      if (filters.status && order.calculated_status !== filters.status) {
        return false;
      }

      return true;
    }).sort((a, b) => {
      const amountA = Number(a.total_amount ?? a.total_price ?? 0);
      const amountB = Number(b.total_amount ?? b.total_price ?? 0);
      const dateA = new Date(a.created_at || 0).getTime();
      const dateB = new Date(b.created_at || 0).getTime();

      if (filters.sort === 'oldest') return dateA - dateB;
      if (filters.sort === 'amount_asc') return amountA - amountB;
      if (filters.sort === 'amount_desc') return amountB - amountA;
      return dateB - dateA; // newest
    });
  }, [normalizedOrders, filters]);

  // Tổng hợp các chỉ số tài chính (Summary Statistics)
  const summaryStats = useMemo(() => {
    const totalCount = filteredOrders.length;
    const totalGrossAmount = filteredOrders.reduce((sum, o) => sum + Number(o.total_amount ?? o.total_price ?? 0), 0);

    let grossDeliveredRevenue = 0;
    let deliveredCount = 0;
    let totalDeliveredSubtotal = 0;
    let totalVoucherDiscounts = 0;
    let totalShippingFees = 0;

    let shippingRevenue = 0;
    let shippingCount = 0;

    let pendingRevenue = 0;
    let pendingCount = 0;

    let cancelledRevenue = 0;
    let cancelledCount = 0;

    const methodBreakdown = {
      cod: { totalCount: 0, totalGross: 0, deliveredCount: 0, deliveredAmount: 0, shippingCount: 0, shippingAmount: 0, cancelledCount: 0, cancelledAmount: 0 },
      momo: { totalCount: 0, totalGross: 0, deliveredCount: 0, deliveredAmount: 0, pendingCount: 0, pendingAmount: 0, cancelledCount: 0, cancelledAmount: 0 },
    };

    filteredOrders.forEach(o => {
      const amt = Number(o.total_amount ?? o.total_price ?? 0);
      const sub = Number(o.subtotal ?? amt);
      const disc = Number(o.discount_amount ?? 0);
      const ship = Number(o.shipping_fee ?? 0);
      const gw = o.calculated_gateway;
      const st = o.calculated_status;

      methodBreakdown[gw].totalCount += 1;
      methodBreakdown[gw].totalGross += amt;

      if (st === 'delivered') {
        grossDeliveredRevenue += amt;
        deliveredCount += 1;
        totalDeliveredSubtotal += sub;
        totalVoucherDiscounts += disc;
        totalShippingFees += ship;
        methodBreakdown[gw].deliveredCount += 1;
        methodBreakdown[gw].deliveredAmount += amt;
      } else if (st === 'shipping') {
        shippingRevenue += amt;
        shippingCount += 1;
        if (gw === 'cod') {
          methodBreakdown.cod.shippingCount += 1;
          methodBreakdown.cod.shippingAmount += amt;
        }
      } else if (st === 'cancelled') {
        cancelledRevenue += amt;
        cancelledCount += 1;
        methodBreakdown[gw].cancelledCount += 1;
        methodBreakdown[gw].cancelledAmount += amt;
      } else {
        pendingRevenue += amt;
        pendingCount += 1;
        if (gw === 'momo') {
          methodBreakdown.momo.pendingCount += 1;
          methodBreakdown.momo.pendingAmount += amt;
        }
      }
    });

    const netRevenue = grossDeliveredRevenue;

    return {
      totalCount,
      totalGrossAmount,
      grossDeliveredRevenue,
      deliveredCount,
      totalDeliveredSubtotal,
      totalVoucherDiscounts,
      totalShippingFees,
      netRevenue,
      shippingRevenue,
      shippingCount,
      pendingRevenue,
      pendingCount,
      cancelledRevenue,
      cancelledCount,
      methodBreakdown,
    };
  }, [filteredOrders]);

  // Reset bộ lọc
  const handleResetFilters = () => {
    setFilters({
      search: '',
      date_from: '',
      date_to: '',
      min_amount: '',
      max_amount: '',
      gateway: '',
      status: '',
      sort: 'newest',
    });
    toast.info('Đã xóa bộ lọc');
  };

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      {/* Header Tinh Gọn */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-5">
        <div>
          <div className="flex items-center gap-2.5 mb-1">
            <div className="p-2 rounded-xl bg-gradient-to-br from-lime-400/20 to-emerald-400/10 border border-lime-400/30 text-lime-400">
              <DollarSign className="w-5 h-5" />
            </div>
            <div className="flex items-center gap-2">
              <h1 className="text-xl sm:text-2xl font-black italic tracking-wider text-white">
                BÁO CÁO TÀI CHÍNH & DOANH THU
              </h1>
              <span className="px-2 py-0.5 rounded-full text-[11px] font-bold bg-lime-400/20 text-lime-400 border border-lime-400/30">
                FINANCE
              </span>
            </div>
          </div>
          <p className="text-xs text-slate-400">
            Quản lý doanh thu thực nhận, theo dõi dòng tiền COD và trạng thái thanh toán MoMo
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center p-1 bg-slate-900 border border-slate-800 rounded-xl shadow-inner self-start sm:self-auto">
          <button
            onClick={() => setActiveTab('summary')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition ${
              activeTab === 'summary'
                ? 'bg-lime-400 text-slate-950 shadow-md font-black'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <TrendingUp className="w-3.5 h-3.5" />
            Thống kê chỉ số
          </button>
          <button
            onClick={() => setActiveTab('transactions')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs font-bold transition ${
              activeTab === 'transactions'
                ? 'bg-lime-400 text-slate-950 shadow-md font-black'
                : 'text-slate-400 hover:text-white'
            }`}
          >
            <CreditCard className="w-3.5 h-3.5" />
            Lịch sử giao dịch ({filteredOrders.length})
          </button>
        </div>
      </div>

      {/* FORM BỘ LỌC TINH GỌN */}
      <div className="p-4 sm:p-5 rounded-2xl bg-slate-900/90 border border-slate-800 shadow-xl space-y-3 backdrop-blur-md">
        <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-lime-400">
          <Filter className="w-3.5 h-3.5" /> Bộ lọc báo cáo doanh thu
        </div>

        {/* Row 1: Search & Dates */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 mb-1">Tìm đơn hàng</label>
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
              <input
                type="text"
                placeholder="Mã đơn (#ORD-...), tên, SĐT..."
                value={filters.search}
                onChange={e => setFilters(prev => ({ ...prev, search: e.target.value }))}
                className="w-full pl-8 pr-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs placeholder:text-slate-600 focus:border-lime-400 outline-none transition"
              />
            </div>
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 mb-1">Từ ngày</label>
            <input
              type="date"
              value={filters.date_from}
              onChange={e => setFilters(prev => ({ ...prev, date_from: e.target.value }))}
              className="w-full px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs focus:border-lime-400 outline-none transition"
            />
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 mb-1">Đến ngày</label>
            <input
              type="date"
              value={filters.date_to}
              onChange={e => setFilters(prev => ({ ...prev, date_to: e.target.value }))}
              className="w-full px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs focus:border-lime-400 outline-none transition"
            />
          </div>
        </div>

        {/* Row 2: Method & Status & Actions */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-1">
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 mb-1">Phương thức</label>
            <select
              value={filters.gateway}
              onChange={e => setFilters(prev => ({ ...prev, gateway: e.target.value }))}
              className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs focus:border-lime-400 outline-none transition"
            >
              <option value="">Tất cả phương thức</option>
              <option value="cod">COD (Tiền mặt khi nhận)</option>
              <option value="momo">MoMo QR / ATM</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 mb-1">Trạng thái</label>
            <select
              value={filters.status}
              onChange={e => setFilters(prev => ({ ...prev, status: e.target.value }))}
              className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs focus:border-lime-400 outline-none transition"
            >
              <option value="">Tất cả trạng thái</option>
              <option value="delivered">Đã giao (Thực thu)</option>
              <option value="shipping">Đang giao (GHN)</option>
              <option value="processing">Chờ lấy hàng</option>
              <option value="pending">Chờ xử lý</option>
              <option value="cancelled">Đã hủy đơn</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] font-semibold text-slate-400 mb-1">Sắp xếp</label>
            <select
              value={filters.sort}
              onChange={e => setFilters(prev => ({ ...prev, sort: e.target.value }))}
              className="w-full px-2.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 text-white text-xs focus:border-lime-400 outline-none transition"
            >
              <option value="newest">Mới nhất trước</option>
              <option value="oldest">Cũ nhất trước</option>
              <option value="amount_desc">Số tiền cao ➔ thấp</option>
              <option value="amount_asc">Số tiền thấp ➔ cao</option>
            </select>
          </div>
          <div className="flex items-end gap-2">
            <button
              onClick={handleResetFilters}
              className="flex-1 px-2.5 py-1.5 rounded-xl border border-slate-700 text-slate-400 hover:text-white hover:bg-slate-800 text-xs font-semibold transition text-center"
            >
              Xóa lọc
            </button>
            <button
              onClick={loadOrders}
              className="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition flex items-center justify-center"
              title="Làm mới dữ liệu"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            </button>
          </div>
        </div>
      </div>

      {/* NỘI DUNG TAB 1: THỐNG KÊ CHỈ SỐ TÀI CHÍNH */}
      {activeTab === 'summary' && (
        <div className="space-y-6">
          {/* Card Highlight: DOANH THU THỰC NHẬN */}
          <div className="p-5 sm:p-6 rounded-2xl bg-gradient-to-br from-lime-950/40 via-slate-900 to-slate-950 border border-lime-400/40 shadow-xl relative overflow-hidden group">
            <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-5 relative z-10">
              <div className="space-y-1.5">
                <div className="flex items-center gap-2">
                  <span className="px-2.5 py-0.5 rounded-full text-[11px] font-black bg-lime-400 text-slate-950 uppercase tracking-wider">
                    DOANH THU THỰC NHẬN
                  </span>
                  <span className="text-[11px] text-slate-400">Tổng tiền các đơn giao thành công</span>
                </div>
                <div className="text-3xl sm:text-4xl font-black text-lime-400 tracking-tight">
                  {summaryStats.grossDeliveredRevenue.toLocaleString('vi-VN')} đ
                </div>
                <p className="text-xs text-slate-300">
                  Số tiền thực tế cửa hàng đã thu từ các đơn hàng giao thành công
                </p>
              </div>

              {/* Khối Đối Chiếu Trực Quan */}
              <div className="flex items-center gap-4 bg-slate-950/80 p-3 sm:p-4 rounded-xl border border-slate-800/80 shadow-inner">
                <div className="px-3 text-left">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Đơn hàng hoàn tất</div>
                  <div className="text-base sm:text-lg font-black text-white mt-0.5">
                    {summaryStats.deliveredCount} đơn
                  </div>
                  <div className="text-[10px] text-lime-400 font-semibold mt-0.5 flex items-center gap-1">
                    <CheckCircle2 className="w-3 h-3 inline" /> Tỷ lệ hoàn thành: {summaryStats.totalCount > 0 ? Math.round((summaryStats.deliveredCount / summaryStats.totalCount) * 100) : 0}%
                  </div>
                </div>

                <div className="px-3 border-l border-slate-800/80 text-left">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Tổng giá trị đơn tạo</div>
                  <div className="text-base sm:text-lg font-black text-slate-300 mt-0.5">
                    {summaryStats.totalGrossAmount.toLocaleString('vi-VN')} đ
                  </div>
                  <div className="text-[10px] text-slate-500 font-medium mt-0.5">
                    {summaryStats.totalCount} đơn trong bộ lọc
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* 3 Thẻ Dòng Tiền Tồn Đọng & Đang Xử Lý */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Card 1: Tiền hàng đã giao thành công */}
            <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-emerald-950/30 via-slate-900 to-slate-900 border border-emerald-500/30 shadow-md">
              <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-emerald-400 mb-1.5">
                <CheckCircle2 className="w-4 h-4" /> Đã giao (Thực thu)
              </div>
              <div className="text-xl sm:text-2xl font-black text-emerald-400 tracking-tight">
                {summaryStats.grossDeliveredRevenue.toLocaleString('vi-VN')} đ
              </div>
              <p className="text-xs text-slate-400 mt-1">
                {summaryStats.deliveredCount} đơn hàng giao thành công
              </p>
            </div>

            {/* Card 2: Tiền hàng đang giao (GHN) */}
            <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-sky-950/30 via-slate-900 to-slate-900 border border-sky-500/30 shadow-md">
              <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-sky-400 mb-1.5">
                <Truck className="w-4 h-4" /> Tiền đơn đang giao
              </div>
              <div className="text-xl sm:text-2xl font-black text-sky-400 tracking-tight">
                {summaryStats.shippingRevenue.toLocaleString('vi-VN')} đ
              </div>
              <p className="text-xs text-slate-400 mt-1">
                {summaryStats.shippingCount} đơn hàng đang trên đường giao
              </p>
            </div>

            {/* Card 3: Tiền hàng chờ xử lý */}
            <div className="p-4 sm:p-5 rounded-2xl bg-gradient-to-br from-amber-950/30 via-slate-900 to-slate-900 border border-amber-500/30 shadow-md">
              <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-amber-400 mb-1.5">
                <Clock className="w-4 h-4" /> Tiền đơn chờ xử lý
              </div>
              <div className="text-xl sm:text-2xl font-black text-amber-400 tracking-tight">
                {summaryStats.pendingRevenue.toLocaleString('vi-VN')} đ
              </div>
              <p className="text-xs text-slate-400 mt-1">
                {summaryStats.pendingCount} đơn hàng mới đặt chờ đóng gói
              </p>
            </div>
          </div>

          {/* Bảng Thống kê Kênh thanh toán Tinh Gọn */}
          <div className="rounded-2xl bg-slate-900 border border-slate-800 overflow-hidden shadow-xl">
            <div className="px-5 py-3.5 border-b border-slate-800 font-bold text-xs sm:text-sm text-white flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Wallet className="w-4 h-4 text-lime-400" /> Báo cáo doanh thu & dòng tiền theo kênh
              </div>
              <span className="text-[11px] text-slate-400 font-normal">Hạch toán thực thu theo từng phương thức</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-slate-950/70 uppercase tracking-wider text-slate-400 border-b border-slate-800">
                  <tr>
                    <th className="px-4 py-3">Kênh thanh toán</th>
                    <th className="px-4 py-3 text-right">Tổng đơn</th>
                    <th className="px-4 py-3 text-right">Tổng giá trị</th>
                    <th className="px-4 py-3 text-right">Đã hoàn tất</th>
                    <th className="px-4 py-3 text-right">Đã hủy</th>
                    <th className="px-4 py-3 text-right">Doanh thu Thực nhận</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 text-slate-300">
                  {/* COD Row */}
                  <tr className="hover:bg-slate-800/40 transition">
                    <td className="px-4 py-3 font-bold text-white flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-amber-400 shadow-sm" />
                      COD (Tiền mặt khi nhận)
                    </td>
                    <td className="px-4 py-3 text-right font-medium">{summaryStats.methodBreakdown.cod.totalCount}</td>
                    <td className="px-4 py-3 text-right font-semibold text-slate-300">
                      {summaryStats.methodBreakdown.cod.totalGross.toLocaleString('vi-VN')} đ
                    </td>
                    <td className="px-4 py-3 text-right font-bold text-emerald-400">
                      {summaryStats.methodBreakdown.cod.deliveredCount} đơn
                    </td>
                    <td className="px-4 py-3 text-right font-medium text-slate-500">
                      {summaryStats.methodBreakdown.cod.cancelledCount} đơn
                    </td>
                    <td className="px-4 py-3 text-right font-black text-lime-400">
                      {summaryStats.methodBreakdown.cod.deliveredAmount.toLocaleString('vi-VN')} đ
                    </td>
                  </tr>

                  {/* MoMo Row */}
                  <tr className="hover:bg-slate-800/40 transition">
                    <td className="px-4 py-3 font-bold text-white flex items-center gap-2">
                      <span className="w-2 h-2 rounded-full bg-pink-400 shadow-sm" />
                      MoMo QR / ATM
                    </td>
                    <td className="px-4 py-3 text-right font-medium">{summaryStats.methodBreakdown.momo.totalCount}</td>
                    <td className="px-4 py-3 text-right font-semibold text-slate-300">
                      {summaryStats.methodBreakdown.momo.totalGross.toLocaleString('vi-VN')} đ
                    </td>
                    <td className="px-4 py-3 text-right font-bold text-emerald-400">
                      {summaryStats.methodBreakdown.momo.deliveredCount} đơn
                    </td>
                    <td className="px-4 py-3 text-right font-medium text-slate-500">
                      {summaryStats.methodBreakdown.momo.cancelledCount} đơn
                    </td>
                    <td className="px-4 py-3 text-right font-black text-lime-400">
                      {summaryStats.methodBreakdown.momo.deliveredAmount.toLocaleString('vi-VN')} đ
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* NỘI DUNG TAB 2: DANH SÁCH GIAO DỊCH */}
      {activeTab === 'transactions' && (
        <div className="rounded-2xl bg-slate-900 border border-slate-800 overflow-hidden shadow-xl space-y-3">
          <div className="px-5 py-3.5 border-b border-slate-800 font-bold text-xs sm:text-sm text-white flex items-center justify-between">
            <div className="flex items-center gap-2">
              <CreditCard className="w-4 h-4 text-lime-400" /> Danh sách giao dịch chi tiết ({filteredOrders.length} đơn)
            </div>
            <span className="text-[11px] text-slate-400 font-normal hidden md:inline">
              Theo dõi dòng tiền và trạng thái thanh toán
            </span>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-950/70 uppercase tracking-wider text-slate-400 border-b border-slate-800">
                <tr>
                  <th className="px-4 py-3 w-[25%]">Mã Đơn hàng</th>
                  <th className="px-4 py-3 w-[25%]">Khách hàng</th>
                  <th className="px-4 py-3 w-[25%]">Tổng tiền & Kênh</th>
                  <th className="px-4 py-3 w-[25%] text-right">Trạng thái & Thanh toán</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60 text-slate-300">
                {filteredOrders.length === 0 ? (
                  <tr>
                    <td colSpan={4} className="px-4 py-10 text-center text-slate-500">
                      Không có đơn hàng nào phù hợp với bộ lọc hiện tại.
                    </td>
                  </tr>
                ) : (
                  filteredOrders.map(order => {
                    return (
                      <tr key={order.id} className="hover:bg-slate-800/40 transition">
                        {/* 1. Mã đơn & Thời gian */}
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div className="flex items-center gap-1.5">
                            <span className="font-black text-white text-xs">#{order.id}</span>
                            <span className="text-[11px] text-lime-400 font-semibold truncate max-w-[120px]">
                              {order.order_code || order.order_number || '—'}
                            </span>
                          </div>
                          <div className="text-[10px] text-slate-500 mt-0.5">
                            {order.created_at ? new Date(order.created_at).toLocaleString('vi-VN') : '—'}
                          </div>
                        </td>

                        {/* 2. Khách hàng & SĐT */}
                        <td className="px-4 py-3">
                          <div className="font-bold text-white text-xs truncate max-w-[140px]">
                            {order.shipping_name || order.user?.name || 'Khách vãng lai'}
                          </div>
                          <div className="text-[11px] text-slate-400 mt-0.5 flex items-center gap-1">
                            <PhoneCall className="w-3 h-3 text-slate-500 shrink-0" />
                            <span>{order.shipping_phone || order.phone || '—'}</span>
                          </div>
                        </td>

                        {/* 3. Tổng tiền & Kênh thanh toán */}
                        <td className="px-4 py-3 whitespace-nowrap">
                          <div className="font-black text-white text-xs sm:text-sm">
                            {Number(order.total_amount ?? order.total_price ?? 0).toLocaleString('vi-VN')} đ
                          </div>
                          <div className="mt-1">
                            <span className={`inline-block px-2 py-0.5 rounded text-[10px] font-bold border ${METHODS[order.calculated_gateway]?.badgeBg}`}>
                              {order.calculated_gateway === 'momo' ? 'MoMo AIO' : 'COD Tiền mặt'}
                            </span>
                          </div>
                        </td>

                        {/* 4. Trạng thái & Dòng tiền */}
                        <td className="px-4 py-3 text-right">
                          <div>
                            {order.calculated_status === 'delivered' ? (
                              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
                                <CheckCircle2 className="w-3 h-3" /> Đã thanh toán (Thực thu)
                              </span>
                            ) : order.calculated_status === 'cancelled' ? (
                              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-medium bg-slate-800 text-slate-400 border border-slate-700">
                                <XCircle className="w-3 h-3" /> Đã hủy đơn
                              </span>
                            ) : order.is_paid ? (
                              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-bold bg-pink-500/15 text-pink-400 border border-pink-500/30">
                                <CheckCircle2 className="w-3 h-3" /> MoMo • Đã thanh toán
                              </span>
                            ) : order.calculated_status === 'shipping' ? (
                              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-sky-500/10 text-sky-400 border border-sky-500/30">
                                <Truck className="w-3 h-3" /> COD • Chờ thu khi giao
                              </span>
                            ) : order.calculated_status === 'processing' ? (
                              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-indigo-500/10 text-indigo-400 border border-indigo-500/30">
                                <Package className="w-3 h-3" /> {order.calculated_gateway === 'momo' ? 'MoMo • Chờ thanh toán' : 'COD • Chờ lấy hàng'}
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                                <Clock className="w-3 h-3" /> {order.calculated_gateway === 'momo' ? 'MoMo • Chờ thanh toán' : 'COD • Chờ xử lý'}
                              </span>
                            )}
                          </div>
                        </td>
                      </tr>
                    );
                  })
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};
