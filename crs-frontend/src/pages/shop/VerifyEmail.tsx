import { motion } from 'framer-motion'
import { Mail, RotateCw, ShieldAlert } from 'lucide-react'
import confetti from 'canvas-confetti'
import { useEffect, useState, useRef } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { AuthLayout } from '../../layouts/AuthLayout'
import { resendOtp, verifyEmail } from '../../services/auth'
import { useApp } from '../../context/AppContext'
import { toast } from 'sonner'

export function VerifyEmail() {
  const [params] = useState(() => new URLSearchParams(window.location.search))
  const email = (params.get('email') ?? '').trim().toLowerCase()
  const [otp, setOtp] = useState<string[]>(['', '', '', '', '', ''])
  const [cooldown, setCooldown] = useState(60)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const otpInputsRef = useRef<(HTMLInputElement | null)[]>([])
  const { login } = useApp()
  const navigate = useNavigate()
  const value = otp.join('')

  // Tự động focus vào ô đầu tiên khi mở trang
  useEffect(() => {
    const timer = setTimeout(() => {
      otpInputsRef.current[0]?.focus()
    }, 100)
    return () => clearTimeout(timer)
  }, [])

  // Bộ đếm ngược thời gian gửi lại mã
  useEffect(() => {
    if (cooldown <= 0) return
    const timer = window.setInterval(() => setCooldown((current) => current - 1), 1000)
    return () => window.clearInterval(timer)
  }, [cooldown])

  // Xử lý khi người dùng gõ phím vào từng ô
  const handleChange = (index: number, e: React.ChangeEvent<HTMLInputElement>) => {
    const rawVal = e.target.value
    const digitsOnly = rawVal.replace(/\D/g, '')

    if (!digitsOnly) {
      const copy = [...otp]
      copy[index] = ''
      setOtp(copy)
      setError('')
      return
    }

    if (digitsOnly.length > 1) {
      // Người dùng paste hoặc trình duyệt tự động điền nhiều số
      const copy = [...otp]
      for (let i = 0; i < digitsOnly.length && index + i < 6; i++) {
        copy[index + i] = digitsOnly[i]
      }
      setOtp(copy)
      setError('')
      const nextFocus = Math.min(index + digitsOnly.length, 5)
      otpInputsRef.current[nextFocus]?.focus()
      return
    }

    // Nhập 1 chữ số bình thường
    const copy = [...otp]
    copy[index] = digitsOnly[0]
    setOtp(copy)
    setError('')

    // Nhảy sang ô tiếp theo
    if (index < 5) {
      otpInputsRef.current[index + 1]?.focus()
    }
  }

  // Xử lý phím điều hướng & Backspace
  const handleKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace') {
      if (!otp[index] && index > 0) {
        // Ô hiện tại rỗng -> nhảy về ô trước và xóa ô đó
        e.preventDefault()
        const copy = [...otp]
        copy[index - 1] = ''
        setOtp(copy)
        otpInputsRef.current[index - 1]?.focus()
      } else if (otp[index]) {
        const copy = [...otp]
        copy[index] = ''
        setOtp(copy)
      }
    } else if (e.key === 'ArrowLeft' && index > 0) {
      e.preventDefault()
      otpInputsRef.current[index - 1]?.focus()
    } else if (e.key === 'ArrowRight' && index < 5) {
      e.preventDefault()
      otpInputsRef.current[index + 1]?.focus()
    }
  }

  // Xử lý Paste trực tiếp
  const handlePaste = (e: React.ClipboardEvent) => {
    e.preventDefault()
    const pasted = e.clipboardData.getData('text').replace(/\D/g, '').slice(0, 6)
    if (!pasted) return

    const copy = Array.from({ length: 6 }, (_, idx) => pasted[idx] ?? '')
    setOtp(copy)
    setError('')

    const nextFocus = Math.min(pasted.length, 5)
    otpInputsRef.current[nextFocus]?.focus()
  }

  const verify = async (e?: React.FormEvent) => {
    if (e) e.preventDefault()
    if (value.length !== 6) {
      setError('Vui lòng nhập đủ 6 chữ số mã OTP')
      return
    }
    if (!email) {
      setError('Không tìm thấy thông tin email. Vui lòng đăng nhập lại.')
      return
    }

    setLoading(true)
    setError('')
    try {
      const response = await verifyEmail(email, value)
      const user = response.user || response.data?.user
      const token = response.token || response.data?.token || 'demo-token'
      if (user) {
        login(user, token)
      }
      confetti({
        particleCount: 140,
        spread: 90,
        origin: { y: 0.65 },
        colors: ['#84cc16', '#10b981', '#38bdf8', '#ffffff'],
      })
      toast.success('🎉 Email đã được xác minh thành công! Đã đăng nhập vào hệ thống.')
      navigate('/')
    } catch (err: any) {
      const errMsg = err?.response?.data?.message || err?.response?.data?.errors?.otp_code?.[0] || 'Mã OTP không đúng hoặc đã hết hạn.'
      setError(errMsg)
    } finally {
      setLoading(false)
    }
  }

  const resend = async () => {
    if (cooldown > 0 || !email) return
    try {
      setLoading(true)
      await resendOtp(email)
      setCooldown(60)
      setOtp(['', '', '', '', '', ''])
      setError('')
      toast.success('Mã OTP mới đã được gửi về email của bạn. Vui lòng kiểm tra email mới nhất.')
      otpInputsRef.current[0]?.focus()
    } catch (err: any) {
      const errMsg = err?.response?.data?.message || 'Không thể gửi lại mã OTP. Vui lòng thử lại sau.'
      toast.error(errMsg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <AuthLayout>
      <div className="space-y-6 text-center">
        {/* Header & Logo */}
        <div className="space-y-2">
          <Link to="/" className="inline-flex items-center gap-2 text-2xl font-black italic tracking-tighter text-white hover:opacity-90 transition">
            <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-lime-400 text-slate-950 not-italic font-black text-lg shadow-md shadow-lime-400/30">
              S
            </span>
            STRIKER.
          </Link>

          <div className="flex items-center justify-center gap-1.5 font-mono text-[10px] font-black uppercase tracking-[0.3em] text-lime-400">
            <Mail size={13} className="animate-pulse" /> EMAIL VERIFICATION
          </div>

          <h2 className="text-2xl sm:text-3xl font-black italic tracking-tighter uppercase text-white leading-tight">
            XÁC MINH <span className="text-lime-400">TÀI KHOẢN.</span>
          </h2>
          <p className="text-xs text-slate-400 leading-relaxed max-w-xs mx-auto">
            Nhập mã OTP 6 chữ số đã được gửi tới
            <br />
            <b className="text-lime-400 font-mono text-xs">{email || 'email của bạn'}</b>
          </p>
        </div>

        {error && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex items-center justify-center gap-2 rounded-xl border border-rose-500/30 bg-rose-500/20 p-3 text-xs font-semibold text-rose-300 text-left"
          >
            <ShieldAlert size={16} className="shrink-0" />
            <span>{error}</span>
          </motion.div>
        )}

        {/* 6 OTP Inputs */}
        <form onSubmit={verify} className="space-y-4">
          <div className="flex justify-center gap-2 sm:gap-3 py-2">
            {otp.map((digit, index) => (
              <input
                id={`otp-${index}`}
                key={index}
                ref={(el) => {
                  otpInputsRef.current[index] = el
                }}
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
                autoComplete="one-time-code"
                value={digit}
                onChange={(e) => handleChange(index, e)}
                onKeyDown={(e) => handleKeyDown(index, e)}
                onPaste={handlePaste}
                className="h-12 w-10 sm:h-14 sm:w-12 rounded-xl border border-white/15 bg-slate-900/90 text-center font-mono text-2xl font-black text-lime-400 outline-none transition focus:border-lime-400 focus:ring-2 focus:ring-lime-400/30 select-all"
              />
            ))}
          </div>

          <button
            type="submit"
            disabled={loading || value.length !== 6}
            className="w-full flex items-center justify-center gap-2 rounded-xl bg-lime-400 py-3.5 text-xs sm:text-sm font-black uppercase tracking-wider text-slate-950 transition hover:bg-lime-300 shadow-lg shadow-lime-400/25 disabled:opacity-40 cursor-pointer disabled:cursor-not-allowed"
          >
            {loading ? (
              <span className="h-4 w-4 animate-spin rounded-full border-2 border-slate-950 border-t-transparent" />
            ) : (
              'XÁC MINH NGAY →'
            )}
          </button>
        </form>

        <div className="text-xs text-slate-400">
          {cooldown > 0 ? (
            <span>
              Gửi lại mã sau <b className="text-lime-400 font-mono">{cooldown}s</b>
            </span>
          ) : (
            <button
              type="button"
              onClick={resend}
              className="inline-flex items-center gap-1 font-bold text-lime-400 hover:underline cursor-pointer"
            >
              <RotateCw size={12} /> Gửi lại mã OTP
            </button>
          )}
        </div>

        <div className="border-t border-white/10 pt-4">
          <Link to="/login" className="text-xs font-semibold text-slate-400 hover:text-white transition">
            ← Quay lại đăng nhập
          </Link>
        </div>
      </div>
    </AuthLayout>
  )
}