<template>
  <v-card
    class="product-card"
    flat
    height="100%"
    :link="!preview"
    @click="openProduct"
  >
    <div class="product-media">
      <v-img
        v-if="image"
        :alt="name"
        :aspect-ratio="compact ? 1 : undefined"
        class="product-image"
        cover
        :height="compact ? undefined : 180"
        :src="imageSource"
      />

      <v-sheet
        v-else
        class="product-image d-flex align-center justify-center"
        color="surface-variant"
        :height="compact ? undefined : 180"
        :style="compact ? 'aspect-ratio: 1' : undefined"
      >
        <v-icon color="medium-emphasis" icon="mdi-image-outline" size="48" />
      </v-sheet>
    </div>

    <v-card-item class="product-copy text-center px-2">
      <v-card-title class="text-body-1">{{ name }}</v-card-title>

      <template v-if="!compact"><v-rating
                                  color="amber"
                                  density="compact"
                                  :model-value="rating"
                                  readonly
                                  size="18"
                                />

        <p v-if="summary" class="text-body-2 text-medium-emphasis mt-2">{{ summary }}</p><v-card-subtitle v-if="!availability">{{ t('products.unavailable') }}</v-card-subtitle></template>
    </v-card-item>

    <v-card-text class="product-price pt-0 text-center">
      <span v-if="compareAtPrice" class="text-decoration-line-through text-medium-emphasis mr-2">{{ formatPrice(compareAtPrice) }}</span>
      <span class="font-weight-bold">{{ formatPrice(price) }}</span>
    </v-card-text>

    <v-card-actions class="cart-actions justify-space-between" @click.stop>
      <div class="card-stock">
        <v-icon :color="stockInfo.color" :icon="stockInfo.icon" size="18" />
        <span :class="`text-${stockInfo.color}`">{{ stockInfo.label }}</span>
      </div>

      <v-menu v-model="cartMenuOpen" :disabled="preview">
        <template #activator="{ props: menuProps }"><v-btn v-bind="menuProps" icon="mdi-cart-plus" variant="text" @click.stop /></template>

        <v-list min-width="220" @click.stop>
          <v-list-subheader>Välj skick</v-list-subheader>
          <v-list-item title="Ny" @click="addToCart('NEW')" />
          <v-list-item title="Begagnad" @click="addToCart('USED')" />
          <v-list-item title="Sliten" @click="addToCart('WORN')" />
        </v-list>
      </v-menu>
    </v-card-actions>
  </v-card>
</template>

<script setup lang="ts">
  import { computed, ref } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useRouter } from 'vue-router'
  import { useCartStore } from '@/stores/cart'

  const props = withDefaults(defineProps<{
    id: number
    name: string
    price: number
    currency?: string
    image?: string | null
    availability?: boolean
    compareAtPrice?: number | null
    summary?: string | null
    rating?: number
    compact?: boolean
    preview?: boolean
    stockQuantity?: number
    stockStatus?: 'IN_STOCK' | 'LOW_STOCK' | 'OUT_OF_STOCK'
  }>(), {
    availability: true,
    compareAtPrice: null,
    currency: 'SEK',
    image: null,
    rating: 0,
    summary: null,
    compact: false,
    preview: false,
    stockQuantity: 0,
    stockStatus: 'IN_STOCK',
  })

  const { locale, t } = useI18n()
  const router = useRouter()
  const cart = useCartStore()
  const cartMenuOpen = ref(false)
  async function addToCart (condition: 'NEW' | 'USED' | 'WORN') {
    const added = await cart.add(props.id, condition)
    if (added) {
      cartMenuOpen.value = false
    }
  }
  async function openProduct (event: MouseEvent) {
    if (props.preview) return
    if ((event.target as HTMLElement).closest('.cart-actions')) return
    await router.push({ name: 'product-detail', params: { id: props.id } })
  }
  const imageSource = computed(() => {
    if (!props.image?.startsWith('/')) return props.image ?? undefined
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'
    return `${new URL(apiBaseUrl).origin}${props.image}`
  })
  const localeTag = computed(() => ({ sv: 'sv-SE', en: 'en-GB', ja: 'ja-JP' }[locale.value] ?? 'sv-SE'))
  const stockInfo = computed(() => {
    if (props.stockStatus === 'OUT_OF_STOCK') {
      return { color: 'secondary', icon: 'mdi-clock-outline', label: 'Slut i lager' }
    }
    if (props.stockStatus === 'LOW_STOCK') {
      return { color: 'secondary', icon: 'mdi-package-variant-closed-alert', label: 'Få kvar' }
    }
    return {
      color: 'success',
      icon: 'mdi-package-variant-closed-check',
      label: props.stockQuantity > 0 ? `${props.stockQuantity} i lager` : 'I lager',
    }
  })
  function formatPrice (price: number) {
    return new Intl.NumberFormat(localeTag.value, {
      style: 'currency', currency: props.currency, minimumFractionDigits: 2,
    }).format(price / 100)
  }
</script>

<style scoped>
  .product-card {
    background: transparent;
    border: 1px solid #d4af37;
    box-shadow: none;
  }

  .product-media {
    padding: 6px;
    background: var(--app-primary);
    box-shadow: var(--app-shadow-sm);
  }

  .product-image {
    border: 1px solid var(--app-border);
  }

  .product-copy :deep(.v-card-title) {
    color: var(--app-primary);
    font-family: var(--app-font-display);
    font-size: 1.3rem;
  }

  .product-price {
    color: var(--app-primary);
  }

  .cart-actions :deep(.v-btn) {
    color: var(--app-secondary);
  }

  .card-stock {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    font-size: 0.75rem;
    font-weight: 600;
  }
</style>
