import { apiClient } from './client'

export interface Review {
  id: number
  product_id: number
  user_id: number | null
  rating: number
  comment: string
  author_name: string
  review_title: string
  product_name?: string | null
  created_at: string
}

export interface OrderItem {
  id: number
  product_id: number
  product_name: string
  price_ore: number
  quantity: number
  condition: 'NEW' | 'USED' | 'WORN'
}

export interface Order {
  id: number
  status: string
  created_at: string
  items: OrderItem[]
}
export const reviewsService = {
  create (productId: number, rating: number, title: string, comment: string) {
    return apiClient.post<Review>(`/products/${productId}/reviews`, { rating, title, comment })
  },
  delete (productId: number, reviewId: number) {
    return apiClient.delete<void>(`/products/${productId}/reviews/${reviewId}`)
  },
  mine () {
    return apiClient.get<Review[]>('/reviews/me')
  },
  forProduct (productId: number) {
    return apiClient.get<Review[]>(`/products/${productId}/reviews`)
  },
  orders () {
    return apiClient.get<Order[]>('/orders/me')
  },
}
