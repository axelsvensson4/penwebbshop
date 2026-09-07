<template>
  <PageHeader :subtitle="t('outlet.intro')" :title="t('outlet.title')" />

  <v-row class="product-grid">
    <v-col
      v-for="product in productStore.products"
      :key="product.id"
      cols="12"
      md="3"
      sm="6"
    >
      <ProductCard
        :id="product.id"
        :availability="product.is_available"
        compact
        :compare-at-price="product.compare_at_price_ore"
        :currency="product.currency"
        :image="product.image_url"
        :name="product.name"
        :price="product.price_ore"
        :rating="product.average_rating"
        :stock-quantity="product.stock_quantity"
        :stock-status="product.availability"
        :summary="product.summary"
      />
    </v-col>
  </v-row>

  <v-alert v-if="productStore.products.length === 0 && !productStore.isLoading" type="info" variant="tonal">Inga outletprodukter just nu.</v-alert>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'
  import ProductCard from '@/components/shop/ProductCard.vue'
  import { useProductStore } from '@/stores/products'

  const { t } = useI18n()
  const productStore = useProductStore()

  onMounted(() => {
    productStore.fetchProducts({ available_only: false, outlet: true })
  })
</script>

<style scoped>
  .product-grid { row-gap: 24px; }
</style>
