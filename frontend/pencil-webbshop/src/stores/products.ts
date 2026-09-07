import { defineStore } from 'pinia'
import { ref } from 'vue'
import { ApiError } from '@/api/client'
import { type Product, type ProductListParams, productsService } from '@/api/products.service'

export const useProductStore = defineStore('products', () => {
  const products = ref<Product[]>([])
  const allProducts = ref<Product[]>([])
  const selectedProduct = ref<Product | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const hasLoaded = ref(false)
  let loadPromise: Promise<void> | null = null

  async function loadAllProducts () {
    if (hasLoaded.value) {
      return
    }
    if (loadPromise) {
      return loadPromise
    }

    loadPromise = (async () => {
      isLoading.value = true
      error.value = null
      try {
        allProducts.value = await productsService.list({ available_only: false, limit: 100 })
        hasLoaded.value = true
      } catch (caughtError) {
        error.value = caughtError instanceof ApiError
          ? caughtError.message
          : 'Kunde inte hämta produkter.'
      } finally {
        isLoading.value = false
        loadPromise = null
      }
    })()
    return loadPromise
  }

  function filterProducts (params?: ProductListParams) {
    let filtered = [...allProducts.value]
    if (params?.available_only) {
      filtered = filtered.filter(product => product.is_available && product.availability !== 'OUT_OF_STOCK')
    }
    if (params?.outlet !== undefined) {
      filtered = filtered.filter(product => product.is_outlet === params.outlet)
    }
    if (params?.featured !== undefined) {
      filtered = filtered.filter(product => product.featured === params.featured)
    }
    if (params?.category) {
      filtered = filtered.filter(product => product.category === params.category)
    }
    if (params?.search?.trim()) {
      const searchTerm = params.search.trim().toLocaleLowerCase('sv-SE')
      filtered = filtered.filter(product => [product.name, product.summary, product.description]
        .some(value => value?.toLocaleLowerCase('sv-SE').includes(searchTerm)))
    }
    return params?.limit ? filtered.slice(0, params.limit) : filtered
  }

  async function fetchProducts (params?: ProductListParams) {
    await loadAllProducts()
    products.value = filterProducts(params)
  }

  async function fetchProduct (productId: number) {
    await loadAllProducts()
    selectedProduct.value = allProducts.value.find(product => product.id === productId) ?? null
    if (!selectedProduct.value) {
      throw new Error('Produkten hittades inte.')
    }
    return selectedProduct.value
  }

  return { products, allProducts, selectedProduct, isLoading, error, fetchProducts, fetchProduct }
})
