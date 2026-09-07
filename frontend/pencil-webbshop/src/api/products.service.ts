import { apiClient } from './client'

export type ProductListParams = {
  available_only?: boolean
  category?: string | null
  featured?: boolean
  limit?: number
  outlet?: boolean
  search?: string | null
}

export interface Product {
  id: number
  name: string
  slug: string | null
  summary: string | null
  price_ore: number
  compare_at_price_ore: number | null
  currency: string
  description: string | null
  image_url: string | null
  is_available: boolean
  is_outlet: boolean
  availability: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK'
  stock_quantity: number
  condition: 'NEW' | 'USED' | 'WORN'
  featured: boolean
  category: string | null
  average_rating: number
  review_count: number
}

export const productsService = {
  list (params?: ProductListParams) {
    return apiClient.get<Product[]>('/products', params)
  },
  get (productId: number) {
    return apiClient.get<Product>(`/products/${productId}`)
  },
}
