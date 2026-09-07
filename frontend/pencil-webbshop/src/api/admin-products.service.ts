import type { AdminProduct, ProductCreateInput } from '@/types/admin-product'
import { apiClient } from './client'

export const adminProductsService = {
  list () {
    return apiClient.get<AdminProduct[]>('/admin/products')
  },
  get (productId: number) {
    return apiClient.get<AdminProduct>(`/admin/products/${productId}`)
  },
  delete (productId: number) {
    return apiClient.delete<void>(`/admin/products/${productId}`)
  },
  create (product: ProductCreateInput) {
    return apiClient.post<AdminProduct>('/admin/products', product)
  },
  update (productId: number, product: ProductCreateInput) {
    return apiClient.put<AdminProduct>(`/admin/products/${productId}`, product)
  },
  uploadImage (productId: number, image: File, altText: string) {
    const path = `/admin/products/${productId}/image?alt_text=${encodeURIComponent(altText)}`
    return apiClient.file<AdminProduct>(path, image)
  },
}
