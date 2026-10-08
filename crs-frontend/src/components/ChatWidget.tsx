import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useApp } from '../context/AppContext';
import { 
  fetchUserMessages, 
  sendUserMessage, 
  submitChatFeedback,
  formatChatAttachmentUrl,
  isPlaceholderContent,
  type ChatMessage, 
  type ChatSuggestedProduct,
  type ChatOrderTracking 
} from '../services/chat';
import { 
  MessageSquare, X, Send, Headphones, Sparkles, Loader2, ShieldCheck, 
  Zap, ArrowRight, Maximize2, Minimize2, Smile, Paperclip, FileText, 
  Bot, ShoppingCart, Check, ExternalLink, Tag, Package, Truck, Copy, Camera
} from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'sonner';
import type { Product } from '../types';

// Danh mục Emoji & Gợi ý nhanh
const EMOJI_CATEGORIES = [
  { name: 'Bóng đá & Thể thao', emojis: ['⚽', '👟', '🥅', '🏆', '🥇', '⚡', '🔥', '💪', '🎯', '🏃'] },
  { name: 'Cảm xúc & Biểu tượng', emojis: ['😊', '😎', '😂', '👍', '❤️', '👏', '🎉', '⭐', '✨', '❓'] },
  { name: 'Mua sắm & Đơn hàng', emojis: ['📦', '🛍️', '💳', '🚚', '🏷️', '🔖', '💯', '🚀', '💬', '📞'] }
];

const QUICK_SUGGESTIONS = [
  '⚽ Tư vấn chọn size giày bóng đá chuẩn?',
  '👟 Gợi ý các mẫu giày Nike & Adidas hot nhất?',
  '📦 Kiểm tra tiến trình đơn hàng của tôi?',
  '⚡ Shop có voucher giảm giá nào hôm nay?',
  '🔄 Hướng dẫn đổi trả nếu không vừa size?'
];

const HOME_QUICK_CHIPS = [
  { icon: '🔥', label: 'Top giày bán chạy', prompt: 'Gợi ý cho mình top mẫu giày đá bóng bán chạy nhất trang chủ kèm size và giá nhé!' },
  { icon: '🎁', label: 'Voucher ưu đãi', prompt: 'Shop hiện có những mã giảm giá voucher nào hot nhất hôm nay?' },
  { icon: '⚽', label: 'Giày cỏ nhân tạo TF', prompt: 'Tư vấn cho mình các mẫu giày đá bóng sân cỏ nhân tạo (đinh TF) hot nhất!' },
  { icon: '📏', label: 'Tư vấn chọn size', prompt: 'Hướng dẫn mình cách đo chiều dài chân và chọn size giày bóng đá chuẩn phom nhé!' },
  { icon: '🚚', label: 'Tra cứu đơn hàng', prompt: 'Kiểm tra tình trạng đơn hàng mới nhất của mình với shop!' },
];

/**
 * Thẻ tra cứu đơn hàng trực quan (Order Tracking Card)
 */
const OrderTrackingCard: React.FC<{ tracking: ChatOrderTracking; onClose: () => void }> = ({ tracking, onClose }) => {
  const navigate = useNavigate();
  const [copied, setCopied] = useState(false);
  const isCompleted = tracking.status === 'completed';
  const isCancelled = tracking.status === 'cancelled';
  const isShipping = tracking.status === 'shipping';

  const copyCode = (code: string) => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    toast.success(`Đã sao chép mã GHN: ${code}`);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="mt-3 bg-zinc-950/90 border border-zinc-700/80 rounded-2xl p-3.5 shadow-xl space-y-3">
      <div className="flex items-center justify-between border-b border-white/10 pb-2.5">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-xl bg-lime-400/10 border border-lime-400/30 flex items-center justify-center text-lime-400">
            <Package className="w-4 h-4" />
          </div>
          <div>
            <div className="text-[10px] font-mono text-zinc-400">Mã đơn hàng</div>
            <div className="text-xs font-black text-white tracking-wider">{tracking.order_number}</div>
          </div>
        </div>
        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold font-mono ${
          isCompleted ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' :
          isCancelled ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' :
          isShipping ? 'bg-sky-500/20 text-sky-400 border border-sky-500/30 animate-pulse' :
          'bg-amber-500/20 text-amber-400 border border-amber-500/30'
        }`}>
          {tracking.status_label}
        </span>
      </div>

      <div className="space-y-2 py-1">
        <div className="text-[10px] font-mono font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1">
          <Truck className="w-3 h-3 text-lime-400" />
          <span>Vận chuyển ({tracking.shipping_carrier}):</span>
        </div>
        <div className="relative pl-4 space-y-2.5 before:absolute before:left-1.5 before:top-2 before:bottom-2 before:w-0.5 before:bg-zinc-800">
          {tracking.steps.map((step, idx) => (
            <div key={idx} className="relative flex items-start justify-between gap-2 text-[11px]">
              <span className={`absolute -left-4 top-1 w-2.5 h-2.5 rounded-full ring-2 ring-zinc-950 ${
                step.is_error ? 'bg-rose-500' : step.completed ? 'bg-emerald-400' : step.active ? 'bg-sky-400 animate-ping' : 'bg-zinc-700'
              }`} />
              <div>
                <span className={`font-semibold ${step.completed ? 'text-white' : step.active ? 'text-sky-400 font-bold' : 'text-zinc-500'}`}>
                  {step.title}
                </span>
                {step.description && <div className="text-[9px] text-zinc-500">{step.description}</div>}
              </div>
              {step.time && <span className="text-[9px] font-mono text-zinc-500 shrink-0">{step.time}</span>}
            </div>
          ))}
        </div>
      </div>

      {tracking.tracking_code && (
        <div className="flex items-center justify-between bg-zinc-900/90 px-2.5 py-1.5 rounded-xl border border-white/5 text-[10px] font-mono">
          <span className="text-zinc-400">Mã GHN: <strong className="text-lime-400">{tracking.tracking_code}</strong></span>
          <button
            type="button"
            onClick={() => copyCode(tracking.tracking_code!)}
            className="text-zinc-400 hover:text-white flex items-center gap-1 transition"
          >
            {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
            <span>{copied ? 'Đã chép' : 'Sao chép'}</span>
          </button>
        </div>
      )}

      {tracking.items && tracking.items.length > 0 && (
        <div className="space-y-1.5 border-t border-white/5 pt-2">
          <div className="text-[10px] font-mono text-zinc-400">Sản phẩm:</div>
          {tracking.items.slice(0, 2).map((it, idx) => (
            <div key={idx} className="flex items-center justify-between text-xs py-0.5">
              <span className="text-zinc-300 truncate max-w-[190px]">{it.name} {it.size ? `(Size ${it.size})` : ''}</span>
              <span className="text-zinc-400 font-mono text-[11px]">x{it.quantity}</span>
            </div>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between border-t border-white/10 pt-2 text-xs">
        <div>
          <div className="text-[9px] font-mono text-zinc-500 uppercase">Tổng tiền</div>
          <div className="text-xs font-black text-lime-400 font-mono">{Number(tracking.total_amount).toLocaleString('vi-VN')}đ</div>
        </div>
        <button
          type="button"
          onClick={() => { onClose(); navigate('/orders'); }}
          className="px-3 py-1.5 bg-zinc-800 hover:bg-zinc-700 text-white rounded-xl text-[10px] font-bold flex items-center gap-1 transition"
        >
          <span>Xem chi tiết</span>
          <ArrowRight className="w-3 h-3" />
        </button>
      </div>
    </div>
  );
};

/**
 * Component chính ChatWidget
 */
export const ChatWidget: React.FC = () => {
  const { user, cartDrawerOpen, addToCart } = useApp();
  const navigate = useNavigate();

  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [unreadCount, setUnreadCount] = useState(0);
  const [isExpanded, setIsExpanded] = useState(false);
  const [showEmojiPicker, setShowEmojiPicker] = useState(false);
  const [selectedFile, setSelectedFile] = useState<{ url: string; type: string; name: string } | null>(null);
  const [addedCartIds, setAddedCartIds] = useState<number[]>([]);
  const [ratedMessages, setRatedMessages] = useState<Record<number, number>>({});

  const fileInputRef = useRef<HTMLInputElement>(null);
  const imageInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const lastMessageCountRef = useRef(0);

  const scrollToBottom = useCallback((smooth = true) => {
    messagesEndRef.current?.scrollIntoView({ behavior: smooth ? 'smooth' : 'auto' });
  }, []);

  // Tải danh sách tin nhắn
  const loadMessages = useCallback(async (isInitial = false) => {
    if (!user) return;
    if (isInitial) setLoading(true);

    try {
      const data = await fetchUserMessages(Number(user.id));
      if (Array.isArray(data) && data.length > 0) {
        setMessages(data);
        if (!isOpen && data.length > lastMessageCountRef.current) {
          const newIncoming = data.slice(lastMessageCountRef.current).filter(m => {
            const type = m.sender_type?.toUpperCase();
            return type === 'AI' || type === 'ADMIN' || m.sender_id !== Number(user.id);
          });
          if (newIncoming.length > 0) setUnreadCount(prev => prev + newIncoming.length);
        }
        lastMessageCountRef.current = data.length;
      }
    } catch (err) {
      console.error('Lỗi tải tin nhắn:', err);
    } finally {
      if (isInitial) {
        setLoading(false);
        setTimeout(() => scrollToBottom(false), 80);
      }
    }
  }, [user, isOpen, scrollToBottom]);

  // Polling tự động mỗi 3.5s khi mở khung chat
  useEffect(() => {
    if (!user) return;
    if (isOpen) {
      setUnreadCount(0);
      void loadMessages(messages.length === 0);
      const interval = setInterval(() => void loadMessages(false), 3500);
      return () => clearInterval(interval);
    }
  }, [user, isOpen, loadMessages, messages.length]);

  useEffect(() => {
    if (isOpen && messages.length > 0) scrollToBottom();
  }, [messages.length, isOpen, scrollToBottom]);

  // Chọn file / ảnh đính kèm
  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>, forceImage = false) => {
    const file = e.target.files?.[0];
    if (!file) return;
    if (file.size > 8 * 1024 * 1024) {
      toast.error('Tệp đính kèm không được vượt quá 8MB.');
      return;
    }

    const isImg = forceImage || file.type.startsWith('image/');
    const reader = new FileReader();
    reader.onload = (event) => {
      setSelectedFile({
        url: event.target?.result as string,
        type: isImg ? 'image' : 'file',
        name: file.name
      });
      if (isImg) toast.info('Đã đính kèm ảnh giày! AI Gemini Vision sẽ phân tích mẫu giày này.', { duration: 3000 });
    };
    reader.readAsDataURL(file);
    e.target.value = '';
  };

  // Đánh giá CSAT
  const handleRateMessage = async (msgId: number, rating: number) => {
    setRatedMessages(prev => ({ ...prev, [msgId]: rating }));
    try {
      const success = await submitChatFeedback(rating, undefined, msgId, 'ai');
      if (success) toast.success(`Cảm ơn bạn đã đánh giá ${rating} ⭐!`);
    } catch (e) {
      console.error(e);
    }
  };

  // Thêm nhanh vào giỏ hàng
  const handleQuickAddToCart = (prod: ChatSuggestedProduct) => {
    const productObj: Product = {
      id: Number(prod.id),
      name: prod.name,
      price: Number(prod.price),
      oldPrice: prod.old_price ? Number(prod.old_price) : undefined,
      image: prod.image || '',
      images: prod.image ? [prod.image] : [],
      category: 'Giày bóng đá',
      brand: prod.brand || 'STRIKER',
      description: '',
      stock: 10,
      sizes: ['39', '40', '41', '42', '43'],
      colors: ['Standard'],
      rating: 5,
      reviewsCount: 1,
      soldCount: 10,
      tag: prod.tag || undefined,
    };

    addToCart(productObj, 1);
    toast.success(`Đã thêm "${prod.name}" vào giỏ hàng! 🛒`);
    setAddedCartIds(prev => [...prev, prod.id]);
    setTimeout(() => setAddedCartIds(prev => prev.filter(id => id !== prod.id)), 2500);
  };

  // Gửi tin nhắn
  const handleSendMessage = async (customText?: string) => {
    const textToSend = (customText || inputMessage).trim();
    if ((!textToSend && !selectedFile) || sending || !user) return;

    setSending(true);
    setShowEmojiPicker(false);
    if (!customText) setInputMessage('');

    const currentFile = selectedFile;
    setSelectedFile(null);

    const optimisticMsgId = Date.now();
    const optimisticMsg: ChatMessage = {
      id: optimisticMsgId,
      sender_id: Number(user.id),
      receiver_id: 1,
      content: textToSend || (currentFile?.type === 'image' ? '[Hình ảnh]' : '[Tệp đính kèm]'),
      sender_type: 'CUSTOMER',
      attachment_url: currentFile?.url,
      attachment_type: currentFile?.type,
      attachment_name: currentFile?.name,
      is_read: false,
      created_at: new Date().toISOString(),
    };

    setMessages(prev => [...prev, optimisticMsg]);
    setTimeout(() => scrollToBottom(), 50);

    try {
      const res = await sendUserMessage(textToSend, currentFile || undefined, Number(user.id));
      if (res?.ai_response) {
        const aiMsg: ChatMessage = {
          id: res.ai_response.id || (Date.now() + 1),
          sender_id: res.ai_response.sender_id || 1,
          receiver_id: Number(user.id),
          content: res.ai_response.content,
          sender_type: 'AI',
          metadata: res.ai_response.metadata,
          is_read: false,
          created_at: res.ai_response.created_at || new Date().toISOString(),
        };

        setMessages(prev => {
          const updated = prev.map(m => m.id === optimisticMsgId ? { ...m, id: res.id || m.id } : m);
          return updated.some(m => m.id === aiMsg.id) ? updated : [...updated, aiMsg];
        });
      } else {
        void loadMessages(false);
      }
    } catch (error) {
      console.error('Lỗi khi gửi tin nhắn:', error);
    } finally {
      setSending(false);
      setTimeout(() => scrollToBottom(), 100);
    }
  };

  if (cartDrawerOpen || user?.role === 'admin') return null;

  return (
    <div className="fixed bottom-6 right-6 z-40 flex flex-col items-end font-sans transition-all duration-200">
      {isOpen && (
        <div className={`bg-[#0F141E]/95 backdrop-blur-2xl border border-white/10 rounded-3xl shadow-2xl flex flex-col overflow-hidden mb-4 transition-all duration-300 animate-in fade-in slide-in-from-bottom-5 ${isExpanded ? 'w-[94vw] sm:w-[540px] h-[720px]' : 'w-[90vw] sm:w-[420px] h-[600px]'}`}>
          
          {/* Header */}
          <div className="bg-gradient-to-r from-zinc-900 via-zinc-900/90 to-[#121927] p-4 border-b border-white/10 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-lime-400 to-emerald-500 p-[2px] shadow-lg shadow-lime-400/20">
                <div className="w-full h-full bg-zinc-950 rounded-[14px] flex items-center justify-center">
                  <Headphones className="w-5 h-5 text-lime-400" />
                </div>
              </div>
              <div>
                <div className="flex items-center gap-1.5">
                  <h3 className="font-black text-sm text-white tracking-wide">STRIKER LIVE-SUPPORT</h3>
                  <ShieldCheck className="w-3.5 h-3.5 text-lime-400" />
                </div>
                <p className="text-[11px] font-mono text-emerald-400 flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                  Gemini Vision & Tư vấn viên 24/7
                </p>
              </div>
            </div>

            <div className="flex items-center gap-1">
              <button onClick={() => setIsExpanded(!isExpanded)} className="p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800/80" title={isExpanded ? 'Thu nhỏ' : 'Mở rộng'}>
                {isExpanded ? <Minimize2 className="w-4 h-4" /> : <Maximize2 className="w-4 h-4" />}
              </button>
              <button onClick={() => setIsOpen(false)} className="p-1.5 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800/80" title="Đóng">
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Content Area */}
          {!user ? (
            <div className="flex-1 flex flex-col items-center justify-center p-6 text-center">
              <div className="w-14 h-14 rounded-2xl bg-lime-400/10 border border-lime-400/20 flex items-center justify-center text-lime-400 mb-4 shadow-lg">
                <Zap className="w-7 h-7" />
              </div>
              <h4 className="text-base font-bold text-white mb-2">Trò chuyện cùng STRIKER</h4>
              <p className="text-xs text-zinc-400 mb-6 leading-relaxed">
                Đăng nhập tài khoản để nhận diện giày qua ảnh, tra cứu đơn hàng và lưu lịch sử trò chuyện.
              </p>
              <Link to="/login" onClick={() => setIsOpen(false)} className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-lime-400 to-emerald-400 text-zinc-950 font-black text-xs uppercase tracking-wider hover:brightness-110 flex items-center justify-center gap-2 shadow-lg transition">
                <span>Đăng nhập ngay</span>
                <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          ) : (
            <>
              {/* Message List */}
              <div className="flex-1 p-4 overflow-y-auto custom-scrollbar space-y-3 bg-[#0A0D14]/60">
                <div className="bg-zinc-900/70 border border-zinc-800/90 rounded-2xl p-3.5 text-xs text-zinc-300 leading-relaxed shadow-sm">
                  <div className="flex items-center gap-1.5 font-bold text-lime-400 mb-1 text-[11px] uppercase tracking-wider font-mono">
                    <Sparkles className="w-3.5 h-3.5" />
                    Trợ lý AI STRIKER
                  </div>
                  Chào mừng <span className="font-semibold text-white">{user.name}</span>! Bạn có thể gửi ảnh giày để AI nhận diện, tra cứu đơn hàng hoặc hỏi tư vấn size bất cứ lúc nào.
                </div>

                {messages.length < 3 && (
                  <div className="space-y-1.5 pt-1 pb-2">
                    <div className="text-[10px] uppercase font-mono font-bold text-zinc-500 tracking-wider">Gợi ý nhanh:</div>
                    <div className="flex flex-col gap-1.5">
                      {QUICK_SUGGESTIONS.map((sug, idx) => (
                        <button key={idx} onClick={() => void handleSendMessage(sug)} className="text-left text-xs text-zinc-300 hover:text-lime-400 bg-zinc-900/80 hover:bg-zinc-800/90 border border-zinc-800 rounded-xl px-3 py-2 transition flex items-center justify-between group">
                          <span className="truncate">{sug}</span>
                          <Send className="w-3 h-3 text-zinc-600 group-hover:text-lime-400 shrink-0 ml-2" />
                        </button>
                      ))}
                    </div>
                  </div>
                )}

                {loading && (
                  <div className="flex items-center justify-center py-6 text-zinc-500 text-xs gap-2 font-mono">
                    <Loader2 className="w-4 h-4 animate-spin text-lime-400" />
                    Đang tải tin nhắn...
                  </div>
                )}

                {messages.map((msg, index) => {
                  const isAi = msg.sender_type?.toUpperCase() === 'AI';
                  const isCustomer = msg.sender_type?.toUpperCase() === 'CUSTOMER' || (msg.sender_id === Number(user.id) && !isAi && msg.sender_type?.toUpperCase() !== 'ADMIN');
                  const isMe = isCustomer;
                  const timeStr = msg.created_at ? new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';

                  return (
                    <div key={msg.id || index} className={`flex flex-col ${isMe ? 'items-end' : 'items-start'}`}>
                      <div className="flex items-end gap-2 max-w-[90%]">
                        {!isMe && (
                          <div className={`w-7 h-7 rounded-xl flex items-center justify-center shrink-0 text-xs font-bold ${isAi ? 'bg-gradient-to-tr from-lime-400/20 to-emerald-400/20 border border-lime-400/40 text-lime-400' : 'bg-zinc-800 border border-zinc-700 text-lime-400'}`}>
                            {isAi ? <Bot className="w-4 h-4 text-lime-400" /> : 'S'}
                          </div>
                        )}
                        <div className={`px-4 py-2.5 rounded-2xl text-xs leading-relaxed break-words shadow-md w-full ${isMe ? 'bg-gradient-to-r from-lime-400 to-lime-500 text-zinc-950 font-medium rounded-br-none' : 'bg-zinc-800/90 text-zinc-100 border border-zinc-700/80 rounded-bl-none'}`}>
                          {!isMe && (
                            <div className="text-[10px] font-bold text-lime-400 mb-1 font-mono flex items-center gap-1">
                              {isAi ? <><Sparkles className="w-3 h-3" /><span>Trợ lý AI STRIKER</span></> : <span>Quản trị viên STRIKER</span>}
                            </div>
                          )}

                          {msg.attachment_url && (
                            <div className="mb-2">
                              {msg.attachment_type === 'image' || msg.attachment_url.startsWith('data:image') || msg.attachment_url.match(/\.(jpeg|jpg|gif|png|webp)$/i) ? (
                                <div className="relative group">
                                  <img
                                    src={formatChatAttachmentUrl(msg.attachment_url)}
                                    alt={msg.attachment_name || 'Đính kèm'}
                                    className="max-h-52 rounded-xl object-cover border border-white/10 hover:opacity-95 cursor-pointer"
                                    onClick={() => window.open(formatChatAttachmentUrl(msg.attachment_url)!, '_blank')}
                                  />
                                  {isMe && (
                                    <div className="absolute bottom-1.5 left-1.5 bg-zinc-950/80 backdrop-blur-md px-2 py-0.5 rounded-lg text-[9px] font-mono text-lime-400 flex items-center gap-1">
                                      <Camera className="w-2.5 h-2.5" />
                                      <span>Gemini Vision</span>
                                    </div>
                                  )}
                                </div>
                              ) : (
                                <a href={formatChatAttachmentUrl(msg.attachment_url)} target="_blank" rel="noreferrer" className="flex items-center gap-2 p-2 rounded-xl bg-zinc-900/80 border border-white/10 text-lime-400 text-xs font-mono">
                                  <FileText className="w-4 h-4 shrink-0" />
                                  <span className="truncate">{msg.attachment_name || 'Tải tệp đính kèm'}</span>
                                </a>
                              )}
                            </div>
                          )}

                          {!isPlaceholderContent(msg.content, Boolean(msg.attachment_url)) && (
                            <p className="whitespace-pre-wrap">{msg.content}</p>
                          )}

                          {msg.metadata?.order_tracking && (
                            <OrderTrackingCard tracking={msg.metadata.order_tracking} onClose={() => setIsOpen(false)} />
                          )}

                          {msg.metadata?.suggested_products && msg.metadata.suggested_products.length > 0 && (
                            <div className="mt-3 pt-2.5 border-t border-white/10 space-y-2">
                              <div className="text-[10px] font-mono font-bold uppercase tracking-wider text-lime-400 flex items-center gap-1">
                                <Tag className="w-3 h-3" />
                                <span>Sản phẩm gợi ý:</span>
                              </div>
                              <div className="grid grid-cols-1 gap-2">
                                {msg.metadata.suggested_products.map((prod) => {
                                  const isAdded = addedCartIds.includes(prod.id);
                                  return (
                                    <div key={prod.id} className="flex items-center gap-2.5 p-2 bg-zinc-950/70 hover:bg-zinc-950 border border-white/10 hover:border-lime-500/40 rounded-xl transition group">
                                      {prod.image ? (
                                        <img src={prod.image} alt={prod.name} className="w-12 h-12 rounded-lg object-cover bg-zinc-900 border border-white/5 shrink-0" />
                                      ) : (
                                        <div className="w-12 h-12 rounded-lg bg-zinc-900 border border-white/5 flex items-center justify-center text-sm shrink-0">👟</div>
                                      )}
                                      <div className="flex-1 min-w-0">
                                        <div className="flex items-center gap-1">
                                          {prod.brand && <span className="text-[9px] font-mono text-lime-400 font-bold uppercase">{prod.brand}</span>}
                                          {prod.tag && <span className="text-[8px] font-mono px-1 py-0.2 bg-red-500/20 text-red-400 rounded font-bold">{prod.tag}</span>}
                                        </div>
                                        <h5 className="text-[11px] font-bold text-white truncate group-hover:text-lime-400 transition">{prod.name}</h5>
                                        <div className="flex items-baseline gap-1.5 mt-0.5">
                                          <span className="text-xs font-black text-lime-400 font-mono">{Number(prod.price).toLocaleString('vi-VN')}đ</span>
                                          {prod.old_price && <span className="text-[10px] text-zinc-500 line-through font-mono">{Number(prod.old_price).toLocaleString('vi-VN')}đ</span>}
                                        </div>
                                      </div>
                                      <div className="flex flex-col gap-1 shrink-0">
                                        <button type="button" onClick={() => { setIsOpen(false); navigate(`/product/${prod.id}`); }} className="px-2 py-1 bg-zinc-800 hover:bg-zinc-700 text-white rounded-lg text-[10px] font-bold flex items-center gap-1 transition" title="Xem chi tiết">
                                          <ExternalLink className="w-2.5 h-2.5" />
                                          <span>Xem</span>
                                        </button>
                                        <button type="button" onClick={() => handleQuickAddToCart(prod)} className={`px-2 py-1 rounded-lg text-[10px] font-bold flex items-center gap-1 transition ${isAdded ? 'bg-emerald-500 text-zinc-950' : 'bg-gradient-to-r from-lime-400 to-emerald-400 text-zinc-950 hover:brightness-110'}`} title="Thêm vào giỏ hàng">
                                          {isAdded ? <Check className="w-2.5 h-2.5" /> : <ShoppingCart className="w-2.5 h-2.5" />}
                                          <span>{isAdded ? 'Đã thêm' : 'Mua'}</span>
                                        </button>
                                      </div>
                                    </div>
                                  );
                                })}
                              </div>
                            </div>
                          )}

                          {isAi && (
                            <div className="flex items-center justify-between mt-2.5 pt-2 border-t border-white/10 text-[10px] font-mono">
                              <span className="text-zinc-400">Đánh giá câu trả lời:</span>
                              {ratedMessages[msg.id] ? (
                                <span className="text-amber-400 font-bold">{'★'.repeat(ratedMessages[msg.id])} Cảm ơn bạn! ❤️</span>
                              ) : (
                                <div className="flex items-center gap-1">
                                  {[1, 2, 3, 4, 5].map((star) => (
                                    <button key={star} type="button" onClick={() => handleRateMessage(msg.id, star)} className="text-zinc-500 hover:text-amber-400 text-xs transition hover:scale-125" title={`Chấm ${star} sao`}>
                                      ★
                                    </button>
                                  ))}
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                      <span className="text-[9px] font-mono text-zinc-500 mt-1 px-1">{timeStr}</span>
                    </div>
                  );
                })}

                {sending && (
                  <div className="flex items-start gap-2 max-w-[85%] animate-in fade-in">
                    <div className="w-7 h-7 rounded-xl flex items-center justify-center shrink-0 bg-lime-400/20 border border-lime-400/40 text-lime-400">
                      <Bot className="w-4 h-4 text-lime-400 animate-pulse" />
                    </div>
                    <div className="px-4 py-2.5 rounded-2xl rounded-bl-none bg-zinc-800/90 border border-zinc-700/80 text-xs text-zinc-300 flex items-center gap-2">
                      <span className="text-[11px] text-lime-400 font-mono flex items-center gap-1">
                        <Sparkles className="w-3 h-3 animate-spin" />
                        AI đang phân tích & soạn câu trả lời
                      </span>
                    </div>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </div>

              {/* Tệp đính kèm chờ gửi */}
              {selectedFile && (
                <div className="px-3 py-2 bg-zinc-900 border-t border-white/10 flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2 min-w-0">
                    {selectedFile.type === 'image' ? (
                      <div className="relative">
                        <img src={selectedFile.url} alt="preview" className="w-9 h-9 rounded-lg object-cover border border-lime-400/50" />
                        <span className="absolute -top-1 -right-1 w-3 h-3 rounded-full bg-lime-400 flex items-center justify-center text-[7px] font-black text-zinc-950">AI</span>
                      </div>
                    ) : (
                      <FileText className="w-5 h-5 text-lime-400 shrink-0" />
                    )}
                    <div className="min-w-0">
                      <div className="text-xs text-zinc-200 font-medium truncate max-w-[200px]">{selectedFile.name}</div>
                      {selectedFile.type === 'image' && <div className="text-[10px] text-lime-400 font-mono">✨ Gemini Vision sẵn sàng nhận diện</div>}
                    </div>
                  </div>
                  <button onClick={() => setSelectedFile(null)} className="p-1 text-zinc-400 hover:text-white rounded-lg hover:bg-zinc-800" title="Hủy">
                    <X className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}

              {/* Emoji Picker */}
              {showEmojiPicker && (
                <div className="p-3 bg-zinc-900 border-t border-white/10 max-h-48 overflow-y-auto custom-scrollbar space-y-2">
                  {EMOJI_CATEGORIES.map((cat, idx) => (
                    <div key={idx} className="space-y-1">
                      <div className="text-[10px] font-mono font-bold text-zinc-400 uppercase tracking-wider">{cat.name}</div>
                      <div className="flex flex-wrap gap-1.5">
                        {cat.emojis.map((emoji, eIdx) => (
                          <button key={eIdx} onClick={() => setInputMessage(prev => prev + emoji)} className="p-1.5 text-base hover:bg-zinc-800 rounded-lg transition hover:scale-125">
                            {emoji}
                          </button>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              )}

              {/* Input Form Footer */}
              <div className="p-3 bg-zinc-900/95 border-t border-white/10">
                {/* Home Quick Chips */}
                <div className="flex items-center gap-1.5 overflow-x-auto custom-scrollbar pb-2 mb-1 pt-0.5">
                  {HOME_QUICK_CHIPS.map((chip, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => void handleSendMessage(chip.prompt)}
                      disabled={sending}
                      className="shrink-0 text-[10px] font-mono text-zinc-300 hover:text-lime-300 bg-zinc-950/80 hover:bg-zinc-800 border border-white/10 hover:border-lime-400/40 rounded-full px-2.5 py-1 transition flex items-center gap-1 disabled:opacity-50 cursor-pointer shadow-sm"
                      title={chip.prompt}
                    >
                      <span>{chip.icon}</span>
                      <span>{chip.label}</span>
                    </button>
                  ))}
                </div>

                <input type="file" ref={fileInputRef} onChange={(e) => handleFileSelect(e, false)} className="hidden" accept="image/*,.pdf,.doc,.docx,.txt" />
                <input type="file" ref={imageInputRef} onChange={(e) => handleFileSelect(e, true)} className="hidden" accept="image/*" />

                <div className="flex items-center gap-1.5 bg-zinc-950/80 border border-zinc-800 rounded-2xl p-1.5 focus-within:border-lime-500/60 transition-all">
                  <button type="button" onClick={() => imageInputRef.current?.click()} className="p-1.5 text-zinc-400 hover:text-lime-400 hover:bg-zinc-800/80 rounded-xl transition" title="Tải ảnh giày để AI Gemini Vision nhận diện">
                    <Camera className="w-4 h-4" />
                  </button>
                  <button type="button" onClick={() => fileInputRef.current?.click()} className="p-1.5 text-zinc-400 hover:text-lime-400 hover:bg-zinc-800/80 rounded-xl transition" title="Đính kèm tệp tin">
                    <Paperclip className="w-4 h-4" />
                  </button>
                  <button type="button" onClick={() => setShowEmojiPicker(!showEmojiPicker)} className={`p-1.5 rounded-xl transition ${showEmojiPicker ? 'text-lime-400 bg-zinc-800' : 'text-zinc-400 hover:text-lime-400 hover:bg-zinc-800/80'}`} title="Biểu tượng cảm xúc">
                    <Smile className="w-4 h-4" />
                  </button>

                  <input
                    type="text"
                    value={inputMessage}
                    onChange={(e) => setInputMessage(e.target.value)}
                    onKeyDown={(e) => {
                      if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        void handleSendMessage();
                      }
                    }}
                    placeholder={selectedFile ? "Nhập câu hỏi kèm ảnh..." : "Hỏi AI hoặc CSKH STRIKER..."}
                    className="flex-1 bg-transparent text-xs text-white placeholder-zinc-500 focus:outline-none px-2 py-1"
                    disabled={sending}
                  />

                  <button
                    type="button"
                    onClick={() => void handleSendMessage()}
                    disabled={(!inputMessage.trim() && !selectedFile) || sending}
                    className="p-2 bg-gradient-to-r from-lime-400 to-emerald-400 hover:brightness-110 disabled:opacity-40 disabled:hover:brightness-100 text-zinc-950 rounded-xl font-bold transition flex items-center justify-center shrink-0 shadow-sm"
                  >
                    {sending ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            </>
          )}
        </div>
      )}

      {/* Floating Trigger Button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="group relative flex items-center gap-2.5 px-4 py-3 bg-gradient-to-r from-lime-400 to-emerald-400 text-zinc-950 font-black rounded-2xl shadow-xl shadow-lime-400/20 hover:shadow-lime-400/40 hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer"
      >
        <div className="relative">
          <MessageSquare className="w-5 h-5 text-zinc-950" />
          {unreadCount > 0 && !isOpen && (
            <span className="absolute -top-2 -right-2 min-w-[18px] h-[18px] px-1 bg-red-500 text-white rounded-full text-[10px] font-black flex items-center justify-center border-2 border-zinc-950 animate-bounce">
              {unreadCount}
            </span>
          )}
        </div>
        <span className="text-xs tracking-wider uppercase font-black">
          {isOpen ? 'Đóng chat' : 'Tư vấn AI'}
        </span>
        {!isOpen && (
          <span className="relative flex h-2.5 w-2.5">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-zinc-950 opacity-75" />
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-zinc-950" />
          </span>
        )}
      </button>
    </div>
  );
};
