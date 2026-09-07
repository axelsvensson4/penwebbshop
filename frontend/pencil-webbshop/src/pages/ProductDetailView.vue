<template>
  <v-progress-linear v-if="loading" indeterminate />
  <v-alert v-else-if="error" type="error">{{ error }}</v-alert>

  <v-row v-else-if="product">
    <v-col cols="12" md="6">
      <v-img
        v-if="imageUrl"
        :alt="product.name"
        aspect-ratio="1"
        class="product-image"
        cover
        :src="imageUrl"
      />

      <v-sheet v-else class="product-image" color="surface-variant" height="200" />
    </v-col>

    <v-col cols="12" md="6">
      <h1 class="text-h3">{{ product.name }}</h1>
      <v-rating color="amber" :model-value="product.average_rating" readonly />
      <p>{{ product.review_count }} recensioner</p><p>{{ product.summary }}</p>
      <p class="text-h5">{{ price }}</p>

      <div class="stock-status mb-5">
        <v-icon :color="stockStatus.color" :icon="stockStatus.icon" />
        <span>{{ stockStatus.message }}</span>
      </div>

      <v-menu v-model="cartMenuOpen">
        <template #activator="{ props: menuProps }">
          <v-btn v-bind="menuProps" color="primary" prepend-icon="mdi-cart-plus">
            Lägg i kundvagn
          </v-btn>
        </template>

        <v-list min-width="220">
          <v-list-subheader>Välj skick</v-list-subheader>
          <v-list-item title="Ny" @click="addToCart('NEW')" />
          <v-list-item title="Begagnad" @click="addToCart('USED')" />
          <v-list-item title="Sliten" @click="addToCart('WORN')" />
        </v-list>
      </v-menu>

    </v-col>

    <v-col cols="12">
      <h2 class="text-h5">Kommentarer</h2>

      <ProductReviewForm
        :product-id="product.id"
        @confirmed="confirmReview"
        @created="handleReviewCreated"
        @failed="removeReview"
      />

      <div class="mt-4 review-list">
        <template v-for="(review, index) in reviews" :key="review.id">
          <article class="review-item">
            <div class="d-flex flex-wrap align-center ga-3 mb-2">
              <strong>{{ review.author_name }}</strong>

              <v-rating
                color="secondary"
                density="compact"
                :model-value="review.rating"
                readonly
                size="18"
              />

              <span class="text-medium-emphasis">{{ formatReviewDate(review.created_at) }}</span>

              <v-btn
                v-if="review.user_id === auth.user?.id"
                color="error"
                icon="mdi-delete-outline"
                size="small"
                variant="text"
                @click="deleteReview(review.id)"
              />
            </div>

            <h3 class="text-subtitle-1 font-weight-bold mb-1">{{ review.review_title }}</h3>
            <p class="review-text mb-0">{{ review.comment }}</p>
          </article>

          <v-divider v-if="index < reviews.length - 1" />
        </template>
      </div>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
  import type { Product } from '@/api/products.service'
  import { computed, onMounted, ref } from 'vue'
  import { useRoute } from 'vue-router'
  import { type Review, reviewsService } from '@/api/reviews.service'
  import ProductReviewForm from '@/components/shop/ProductReviewForm.vue'
  import { useAuthStore } from '@/stores/auth'
  import { useCartStore } from '@/stores/cart'
  import { useProductStore } from '@/stores/products'
  import { useReviewStore } from '@/stores/reviews'

  const route = useRoute()
  const product = ref<Product | null>(null)
  const reviews = ref<Review[]>([])
  const error = ref<string | null>(null)
  const loading = ref(true)
  const productStore = useProductStore()
  const cart = useCartStore()
  const cartMenuOpen = ref(false)
  const auth = useAuthStore()
  const reviewStore = useReviewStore()
  const imageUrl = computed(() => product.value?.image_url
    ? `${new URL(import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api').origin}${product.value.image_url}`
    : undefined)
  const price = computed(() => product.value
    ? new Intl.NumberFormat('sv-SE', { style: 'currency', currency: product.value.currency }).format(product.value.price_ore / 100)
    : '')
  function formatReviewDate (value: string) {
    return new Intl.DateTimeFormat('sv-SE', { dateStyle: 'long' }).format(new Date(value))
  }
  const stockStatus = computed(() => {
    switch (product.value?.availability) {
      case 'LOW_STOCK': {
        return {
          color: 'secondary',
          icon: 'mdi-package-variant-closed-alert',
          message: product.value.stock_quantity > 0
            ? `Få kvar – bara ${product.value.stock_quantity} kvar i lager.`
            : 'Få kvar i lager – passa på innan de är slut.',
        }
      }
      case 'OUT_OF_STOCK': {
        return {
          color: 'secondary',
          icon: 'mdi-clock-outline',
          message: 'Slut i lager – snart redo för fler skriväventyr.',
        }
      }
      default: {
        return {
          color: 'success',
          icon: 'mdi-package-variant-closed-check',
          message: product.value?.stock_quantity && product.value.stock_quantity > 0
            ? `${product.value.stock_quantity} i lager – redo att skriva vidare med ✍️`
            : 'I lager – redo att skriva vidare med ✍️',
        }
      }
    }
  })

  async function addToCart (selectedCondition: 'NEW' | 'USED' | 'WORN') {
    if (!product.value) return
    const added = await cart.add(product.value.id, selectedCondition)
    if (added) cartMenuOpen.value = false
  }

  function handleReviewCreated (review: Review) {
    reviews.value.unshift(review)
  }

  function confirmReview (temporaryId: number, review: Review) {
    const index = reviews.value.findIndex(item => item.id === temporaryId)
    if (index !== -1) reviews.value[index] = review
  }

  function removeReview (temporaryId: number) {
    reviews.value = reviews.value.filter(review => review.id !== temporaryId)
  }

  async function deleteReview (reviewId: number) {
    if (!product.value) return
    await reviewStore.remove(product.value.id, reviewId)
    reviews.value = reviews.value.filter(review => review.id !== reviewId)
  }

  onMounted(async () => {
    try {
      const id = Number(route.params.id)
      product.value = await productStore.fetchProduct(id)
      reviews.value = await reviewsService.forProduct(id)
    } catch {
      error.value = 'Produkten kunde inte hämtas.'
    } finally {
      loading.value = false
    }
  })
</script>

<style scoped>
  .stock-status {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    color: rgb(var(--v-theme-success));
    font-weight: 600;
  }

  .product-image {
    width: 65%;
    margin: 0 auto;
  }

  .review-list {
    background: transparent;
  }

  .review-item {
    padding: 1rem 0;
  }

  .review-text {
    overflow-wrap: anywhere;
    white-space: normal;
  }

</style>
