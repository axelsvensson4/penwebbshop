<template>
  <PageHeader :subtitle="t('products.intro')" :title="t('products.title')" />

  <v-sheet class="catalog-tools pa-4 mb-8" color="surface">
    <v-form class="d-flex flex-wrap align-center ga-3" @submit.prevent="applyFilters">
      <v-text-field
        v-model="search"
        bg-color="surface"
        class="catalog-search"
        hide-details
        label="Sök efter en penna"
        prepend-inner-icon="mdi-magnify"
        variant="outlined"
        @update:model-value="handleSearchInput"
      />

      <v-select
        v-model="category"
        class="catalog-category"
        clearable
        hide-details
        :items="categories"
        label="Kategori"
        variant="outlined"
        @update:model-value="applyFilters"
      />

      <v-btn color="primary" type="submit" variant="flat">Sök</v-btn>
    </v-form>
  </v-sheet>

  <v-alert v-if="productStore.error" class="mb-6" type="error" variant="tonal">{{ productStore.error }}</v-alert>
  <v-progress-linear v-else-if="productStore.isLoading" color="primary" indeterminate />

  <v-row v-else-if="productStore.products.length > 0" class="product-grid">
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

  <v-alert v-else type="info" variant="tonal">{{ t('products.empty') }}</v-alert>
</template>

<script setup lang="ts">
  import { onMounted, ref } from 'vue'
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'
  import ProductCard from '@/components/shop/ProductCard.vue'
  import { useProductStore } from '@/stores/products'

  const { t } = useI18n()
  const productStore = useProductStore()
  const search = ref('')
  const category = ref<string | null>(null)
  const categories = [
    { title: 'Lyxiga', value: 'lyxiga' },
    { title: 'Traditionella', value: 'traditionella' },
    { title: 'Fjäderpenna', value: 'fjäderpenna' },
    { title: 'För astronauter', value: 'för-astronauter' },
    { title: 'Limited Edition', value: 'limited-edition' },
  ]

  function applyFilters () {
    productStore.fetchProducts({ available_only: false, category: category.value, outlet: false, search: search.value })
  }

  function handleSearchInput (value: string) {
    if (!value.trim()) {
      applyFilters()
    }
  }

  onMounted(applyFilters)
</script>

<style scoped>
  .product-grid { row-gap: 24px; }

  .catalog-tools {
    border: 1px solid var(--app-border);
  }

  .catalog-search {
    min-width: min(100%, 280px);
    flex: 1 1 280px;
  }

  .catalog-category {
    min-width: min(100%, 220px);
    flex: 0 1 240px;
  }
</style>
