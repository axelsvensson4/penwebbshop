<template>
  <div class="d-flex align-center justify-space-between mb-6">
    <PageHeader title="Produkter" />
    <v-btn color="primary" :to="{ name: 'admin-product-create' }">Lägg till produkt</v-btn>
  </div>

  <v-list border>
    <v-list-item v-for="product in products" :key="product.id" :subtitle="formatPrice(product.price_ore, product.currency)" :title="product.name">
      <template #append>
        <v-menu>
          <template #activator="{ props }"><v-btn v-bind="props" icon="mdi-dots-vertical" variant="text" /></template>
          <v-list><v-list-item title="Redigera" :to="{ name: 'admin-product-edit', params: { id: product.id } }" /><v-list-item title="Radera" @click="remove(product.id)" /></v-list>
        </v-menu>
      </template>
    </v-list-item>

    <v-list-item v-if="products.length === 0" title="Inga produkter ännu." />
  </v-list>
</template>

<script setup lang="ts">
  import type { AdminProduct } from '@/types/admin-product'
  import { onMounted, ref } from 'vue'
  import { adminProductsService } from '@/api/admin-products.service'
  import PageHeader from '@/components/common/PageHeader.vue'

  const products = ref<AdminProduct[]>([])
  function formatPrice (price: number, currency: string) {
    return new Intl.NumberFormat('sv-SE', { style: 'currency', currency }).format(price / 100)
  }
  async function load () {
    products.value = await adminProductsService.list()
  }
  async function remove (id: number) {
    await adminProductsService.delete(id)
    await load()
  }
  onMounted(() => {
    load()
  })
</script>
