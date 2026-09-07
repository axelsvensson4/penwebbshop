import { apiClient } from './client'

export const cartService = {
  get () {
    return apiClient.get<CartResponse>('/cart')
  },
  add (productId: number, condition: 'NEW' | 'USED' | 'WORN', quantity = 1) {
    return apiClient.post('/cart/items', { product_id: productId, condition, quantity })
  },
  update (item: CartItem, quantity: number) {
    return apiClient.patch<void>(`/cart/items/${item.id}`, {
      product_id: item.product_id,
      condition: item.condition,
      quantity,
    })
  },
  remove (itemId: number) {
    return apiClient.delete<void>(`/cart/items/${itemId}`)
  },
  clear () {
    return apiClient.delete('/cart')
  },
  checkout () {
    return apiClient.post<{ order_id: number }>('/cart/checkout', {})
  },
  cancelOrderClaim (orderId: number) {
    return apiClient.delete<void>(`/cart/checkout/${orderId}/claim`)
  },
}

export interface CartItem {
  id: number
  product_id: number
  quantity: number
  condition: 'NEW' | 'USED' | 'WORN'
  name: string
  price_ore: number
  image_url: string | null
}

export interface CartResponse {
  items: CartItem[]
  subtotal_ore: number
  shipping_ore: number
  total_ore: number
}
