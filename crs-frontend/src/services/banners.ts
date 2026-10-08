import api from './api.js'
import type { BannerSlide } from '../types'

let bannersCache: BannerSlide[] | null = null
let bannersCacheTime = 0

export async function fetchBanners(params: Record<string, string | number | boolean> = {}, forceRefresh = false): Promise<BannerSlide[]> {
  const now = Date.now()
  if (!forceRefresh && Object.keys(params).length === 0 && bannersCache && now - bannersCacheTime < 60000) {
    return bannersCache
  }
  const response = await api.get('/banners', { params })
  const list = response.data?.data ?? response.data ?? []
  const data = Array.isArray(list) ? list.map(mapDbBanner) : []
  if (Object.keys(params).length === 0) {
    bannersCache = data
    bannersCacheTime = now
  }
  return data
}

export async function createBanner(payload: Partial<BannerSlide>): Promise<BannerSlide> {
  bannersCache = null
  const response = await api.post('/banners', payload)
  return mapDbBanner(response.data?.data ?? response.data)
}

export async function updateBanner(id: string | number, payload: Partial<BannerSlide>): Promise<BannerSlide> {
  bannersCache = null
  const response = await api.patch(`/banners/${id}`, payload)
  return mapDbBanner(response.data?.data ?? response.data)
}

export async function deleteBanner(id: string | number): Promise<void> {
  bannersCache = null
  await api.delete(`/banners/${id}`)
}

export function mapDbBanner(raw: Record<string, any>): BannerSlide {
  return {
    id: raw.id,
    title: raw.title ?? '',
    subtitle: raw.subtitle ?? '',
    tag: raw.tag ?? '',
    image: raw.image ?? '',
    link: raw.link ?? '',
    order: raw.order ? Number(raw.order) : 1,
    isActive: Boolean(raw.is_active ?? raw.isActive ?? true),
  }
}
