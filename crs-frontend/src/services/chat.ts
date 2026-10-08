import api from './api';

/**
 * Helper format URL ảnh/tệp đính kèm trong chat
 */
export function formatChatAttachmentUrl(url?: string | null): string {
  if (!url || typeof url !== 'string' || url.trim() === '') return '';
  if (url.startsWith('data:') || url.startsWith('blob:') || url.startsWith('http://') || url.startsWith('https://')) {
    return url;
  }
  const cleanPath = url.startsWith('/') ? url : `/${url}`;
  const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api';
  const origin = apiBase.replace(/\/api\/?$/, '');
  return `${origin}${cleanPath}`;
}

/**
 * Kiểm tra nội dung text có phải là placeholder mặc định khi gửi ảnh/file không
 */
export function isPlaceholderContent(content?: string | null, hasAttachment?: boolean): boolean {
  if (!content) return true;
  const trimmed = content.trim();
  if (hasAttachment) {
    if (
      trimmed === '[Hình ảnh]' ||
      trimmed === '[Tệp đính kèm]' ||
      trimmed === '[Đã gửi một tệp đính kèm]' ||
      trimmed.startsWith('[Đã gửi một tệp đính kèm') ||
      trimmed.startsWith('[Đã gửi ảnh') ||
      trimmed.startsWith('Screenshot')
    ) {
      return true;
    }
  }
  return false;
}

/**
 * Rút gọn tin nhắn cuối cùng hiển thị trên danh sách hội thoại
 */
export function renderLastMessageSnippet(lastMsg?: string | null): string {
  if (!lastMsg) return 'Bấm để mở cuộc trò chuyện';
  const trimmed = lastMsg.trim();
  if (
    trimmed.startsWith('[Đã gửi một tệp đính kèm') ||
    trimmed.includes('Screenshot') ||
    trimmed === '[Hình ảnh]' ||
    trimmed.startsWith('[Đã gửi ảnh')
  ) {
    return '📷 [Hình ảnh]';
  }
  if (trimmed === '[Tệp đính kèm]') {
    return '📎 [Tệp đính kèm]';
  }
  return lastMsg;
}


export interface ChatUser {

  id: number;
  name: string;
  email?: string;
  phone_number?: string;
  avatar?: string;
  role?: string;
}

export interface ChatSuggestedProduct {
  id: number;
  name: string;
  brand?: string;
  tag?: string;
  price: number;
  old_price?: number | null;
  image?: string;
  slug?: string;
}

export interface ChatOrderTrackingStep {
  key: string;
  title: string;
  description?: string;
  completed: boolean;
  active?: boolean;
  is_error?: boolean;
  time?: string | null;
}

export interface ChatOrderItem {
  id?: number;
  product_id?: number;
  name: string;
  image?: string;
  price: number;
  quantity: number;
  size?: string | number | null;
}

export interface ChatOrderTracking {
  order_id: number;
  order_number: string;
  status: string;
  status_label: string;
  total_amount: number;
  shipping_fee?: number;
  created_at: string;
  tracking_code: string;
  shipping_carrier: string;
  payment_method?: string;
  is_paid?: boolean;
  steps: ChatOrderTrackingStep[];
  items: ChatOrderItem[];
}

export interface ChatMessage {
  id: number;
  sender_id: number;
  receiver_id: number;
  content: string;
  sender_type?: 'CUSTOMER' | 'ADMIN' | 'AI' | 'user' | 'admin' | 'ai' | string;
  attachment_url?: string | null;
  attachment_type?: string | null;
  attachment_name?: string | null;
  metadata?: {
    suggested_products?: ChatSuggestedProduct[];
    order_tracking?: ChatOrderTracking | null;
    [key: string]: any;
  } | null;
  is_read: boolean;
  created_at: string;
  updated_at?: string;
  sender?: ChatUser;
  receiver?: ChatUser;
  ai_response?: {
    id?: number;
    sender_id?: number;
    receiver_id?: number;
    content: string;
    sender_type: 'AI' | string;
    metadata?: {
      suggested_products?: ChatSuggestedProduct[];
      order_tracking?: ChatOrderTracking | null;
      [key: string]: any;
    } | null;
    created_at?: string;
  };
}

export interface AdminChatUser {
  id: number;
  name: string;
  email?: string;
  phone_number?: string;
  avatar?: string;
  role?: string;
  last_message: string;
  last_message_time: string | null;
  unread_count: number;
}

export interface AdminUnreadCountResponse {
  unread_count: number;
  recent_messages: ChatMessage[];
}

export interface ChatFeedbackItem {
  id: number;
  user_id: number;
  message_id?: number;
  rating: number;
  feedback_type: string;
  comment?: string;
  tags?: string[];
  created_at: string;
}

export interface ChatFeedbackStats {
  total: number;
  average_rating: number;
  rating_counts: Record<number, number>;
}

/**
 * 1. User: Lấy toàn bộ lịch sử tin nhắn với Admin/AI (Lưu trữ vĩnh viễn trên Server)
 */
export async function fetchUserMessages(userId?: number): Promise<ChatMessage[]> {
  try {
    const params = userId ? { user_id: userId } : undefined;
    const res = await api.get('/user/chat/messages', { params });
    const payload = res.data;
    if (Array.isArray(payload?.data)) return payload.data;
    if (Array.isArray(payload)) return payload;
    return [];
  } catch (error) {
    console.error('Lỗi tải tin nhắn User:', error);
    return [];
  }
}

/**
 * 2. User: Gửi tin nhắn tới Admin / Gemini AI (kèm text, file, ảnh, icon, vision)
 */
export async function sendUserMessage(
  message: string, 
  attachment?: { url: string; type: string; name?: string },
  userId?: number
): Promise<ChatMessage> {
  const payload: Record<string, any> = { message };
  if (userId) {
    payload.user_id = userId;
    payload.sender_id = userId;
  }
  if (attachment) {
    payload.attachment_url = attachment.url;
    payload.attachment_type = attachment.type;
    payload.attachment_name = attachment.name;
  }
  const res = await api.post('/user/chat/send', payload);
  const data = res.data?.data || res.data || {};
  if (res.data?.ai_response && !data.ai_response) {
    data.ai_response = res.data.ai_response;
  }
  return data;
}

/**
 * 3. User: Gửi đánh giá hài lòng cuộc hội thoại (CSAT ⭐)
 */
export async function submitChatFeedback(
  rating: number,
  comment?: string,
  messageId?: number,
  feedbackType: 'ai' | 'admin' = 'ai',
  tags?: string[]
): Promise<boolean> {
  try {
    const res = await api.post('/user/chat/feedback', {
      rating,
      comment,
      message_id: messageId,
      feedback_type: feedbackType,
      tags,
    });
    return res.data?.success === true;
  } catch (error) {
    console.error('Lỗi gửi đánh giá CSAT:', error);
    return false;
  }
}

/**
 * 4. Admin: Lấy danh sách khách hàng đã nhắn tin
 */
export async function fetchAdminChatUsers(): Promise<AdminChatUser[]> {
  try {
    const res = await api.get('/admin/chat/users');
    return Array.isArray(res.data?.data) ? res.data.data : (Array.isArray(res.data) ? res.data : []);
  } catch (error) {
    console.error('Lỗi tải danh sách chat Admin:', error);
    return [];
  }
}

/**
 * 5. Admin: Lấy chi tiết lịch sử tin nhắn của 1 User
 */
export async function fetchAdminMessages(userId: number): Promise<ChatMessage[]> {
  try {
    const res = await api.get(`/admin/chat/messages/${userId}`);
    return Array.isArray(res.data?.data) ? res.data.data : (Array.isArray(res.data) ? res.data : []);
  } catch (error) {
    console.error(`Lỗi tải tin nhắn Admin với user ${userId}:`, error);
    return [];
  }
}

/**
 * 6. Admin: Gửi tin nhắn phản hồi cho User
 */
export async function sendAdminMessage(
  userId: number, 
  message: string,
  attachment?: { url: string; type: string; name?: string }
): Promise<ChatMessage> {
  const payload: Record<string, any> = { user_id: userId, message };
  if (attachment) {
    payload.attachment_url = attachment.url;
    payload.attachment_type = attachment.type;
    payload.attachment_name = attachment.name;
  }
  const res = await api.post('/admin/chat/send', payload);
  return res.data?.data || res.data;
}

/**
 * 7. Admin: Lấy tổng số tin nhắn chưa đọc & tin nhắn gần nhất (cho badge chuông)
 */
export async function fetchAdminUnreadCount(): Promise<AdminUnreadCountResponse> {
  try {
    const res = await api.get('/admin/chat/unread-count');
    const data = res.data?.data || res.data;
    return {
      unread_count: data?.unread_count ?? data?.count ?? 0,
      recent_messages: Array.isArray(data?.recent_messages) ? data.recent_messages : [],
    };
  } catch (error) {
    console.error('Lỗi lấy số tin nhắn chưa đọc:', error);
    return { unread_count: 0, recent_messages: [] };
  }
}

/**
 * 8. Admin: Đánh dấu tin nhắn của 1 User là đã đọc
 */
export async function markAdminMessagesAsRead(userId: number): Promise<void> {
  try {
    await api.patch(`/admin/chat/messages/${userId}/read`);
  } catch (error) {
    console.error('Lỗi đánh dấu tin nhắn đã đọc:', error);
  }
}

/**
 * 9. Admin: Tìm kiếm khách hàng trong hệ thống
 */
export async function searchAdminCustomers(query: string): Promise<AdminChatUser[]> {
  try {
    const res = await api.get('/admin/chat/search', { params: { query } });
    return Array.isArray(res.data?.data) ? res.data.data : (Array.isArray(res.data) ? res.data : []);
  } catch (error) {
    console.error('Lỗi tìm kiếm khách hàng:', error);
    return [];
  }
}

/**
 * 10. Admin: Lấy thông tin 1 User để mở chat trực tiếp
 */
export async function fetchChatUserDetail(userId: number): Promise<AdminChatUser | null> {
  try {
    const res = await api.get(`/admin/chat/user-detail/${userId}`);
    return res.data?.data || res.data || null;
  } catch (error) {
    console.error(`Lỗi lấy thông tin user ${userId}:`, error);
    return null;
  }
}

/**
 * 11. Admin: Lấy thống kê đánh giá hài lòng CSAT
 */
export async function fetchAdminFeedbacks(): Promise<{ feedbacks: ChatFeedbackItem[]; stats: ChatFeedbackStats }> {
  try {
    const res = await api.get('/admin/chat/feedbacks');
    const data = res.data?.data || {};
    return {
      feedbacks: Array.isArray(data.feedbacks) ? data.feedbacks : [],
      stats: data.stats || { total: 0, average_rating: 5, rating_counts: {} },
    };
  } catch (error) {
    console.error('Lỗi lấy danh sách feedback CSAT:', error);
    return {
      feedbacks: [],
      stats: { total: 0, average_rating: 5, rating_counts: {} },
    };
  }
}
