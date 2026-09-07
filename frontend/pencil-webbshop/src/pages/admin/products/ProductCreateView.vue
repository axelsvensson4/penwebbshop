<template>
  <v-btn class="mb-4" prepend-icon="mdi-arrow-left" :to="{ name: 'admin-products' }" variant="text">Tillbaka till produktlistan</v-btn>

  <PageHeader :title="t('admin.products.create.title')" />

  <ProductForm />
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import ProductForm from '@/components/admin/products/ProductForm.vue'
  import PageHeader from '@/components/common/PageHeader.vue'

  const { t } = useI18n()
</script>
