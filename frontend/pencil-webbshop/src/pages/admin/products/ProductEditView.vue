<template>
  <PageHeader title="Redigera produkt" />

  <v-progress-linear v-if="!store.selectedProduct && !store.error" color="primary" indeterminate />
  <ProductForm v-else-if="store.selectedProduct" :product="store.selectedProduct" />
  <v-alert v-else type="error" variant="tonal">{{ store.error }}</v-alert>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import { useRoute } from 'vue-router'
  import ProductForm from '@/components/admin/products/ProductForm.vue'
  import PageHeader from '@/components/common/PageHeader.vue'
  import { useAdminProductsStore } from '@/stores/admin-products'

  const route = useRoute()
  const store = useAdminProductsStore()

  onMounted(() => {
    store.fetchProduct(Number(route.params.id))
  })
</script>
