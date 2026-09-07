import type { AdminProduct, ProductCreateInput } from '@/types/admin-product'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { adminProductsService } from '@/api/admin-products.service'
import { ApiError } from '@/api/client'

export const useAdminProductsStore = defineStore('admin-products', () => {
  const isSaving = ref(false)
  const error = ref<string | null>(null)
  const selectedProduct = ref<AdminProduct | null>(null)

  async function createProduct (input: ProductCreateInput, image?: File, altText = ''): Promise<AdminProduct | null> {
    isSaving.value = true
    error.value = null
    try {
      const product = await adminProductsService.create(input)
      return image ? await adminProductsService.uploadImage(product.id, image, altText) : product
    } catch (caughtError) {
      error.value = caughtError instanceof ApiError ? caughtError.message : 'Produkten kunde inte sparas.'
      return null
    } finally {
      isSaving.value = false
    }
  }

  async function fetchProduct (productId: number) {
    error.value = null
    try {
      selectedProduct.value = await adminProductsService.get(productId)
    } catch (caughtError) {
      error.value = caughtError instanceof ApiError ? caughtError.message : 'Produkten kunde inte hämtas.'
    }
  }

  async function updateProduct (productId: number, input: ProductCreateInput, image?: File, altText = ''): Promise<AdminProduct | null> {
    isSaving.value = true
    error.value = null
    try {
      const product = await adminProductsService.update(productId, input)
      selectedProduct.value = image ? await adminProductsService.uploadImage(product.id, image, altText) : product
      return selectedProduct.value
    } catch (caughtError) {
      error.value = caughtError instanceof ApiError ? caughtError.message : 'Produkten kunde inte uppdateras.'
      return null
    } finally {
      isSaving.value = false
    }
  }

  return { isSaving, error, selectedProduct, createProduct, fetchProduct, updateProduct }
})
