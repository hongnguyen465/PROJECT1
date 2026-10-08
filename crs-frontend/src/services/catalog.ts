import api from './api.js'
import type { Product } from '../types'

let categoriesCache: any = null
let categoriesCacheTime = 0

let brandsCache: any = null
let brandsCacheTime = 0

export async function fetchProducts(params: Record<string, string | number> = {}) {
  const response = await api.get('/products', { params })
  return response.data?.data ?? response.data
}

export async function fetchCategories(forceRefresh = false) {
  const now = Date.now()
  if (!forceRefresh && categoriesCache && now - categoriesCacheTime < 60000) {
    return categoriesCache
  }
  const response = await api.get('/categories')
  const data = response.data?.data ?? response.data
  categoriesCache = data
  categoriesCacheTime = now
  return data
}

export async function fetchBrands(forceRefresh = false) {
  const now = Date.now()
  if (!forceRefresh && brandsCache && now - brandsCacheTime < 60000) {
    return brandsCache
  }
  const response = await api.get('/brands')
  const data = response.data?.data ?? response.data
  brandsCache = data
  brandsCacheTime = now
  return data
}

export async function checkStock(items: Array<{ product_id: number; quantity: number }>) {
  const response = await api.post('/products/check-stock', { items })
  return response.data?.data ?? response.data
}

export async function createProduct(payload: Partial<Product>) {
  categoriesCache = null
  brandsCache = null
  const response = await api.post('/products', payload)
  return response.data?.data ?? response.data
}

export async function updateProduct(id: number, payload: Partial<Product>) {
  categoriesCache = null
  brandsCache = null
  const response = await api.patch(`/products/${id}`, payload)
  return response.data?.data ?? response.data
}

export async function deleteProduct(id: number) {
  categoriesCache = null
  brandsCache = null
  const response = await api.delete(`/products/${id}`)
  return response.data?.data ?? response.data
}
