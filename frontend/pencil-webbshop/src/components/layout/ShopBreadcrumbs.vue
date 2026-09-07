<template>
  <v-container class="py-3" max-width="1440">
    <v-breadcrumbs class="px-0" density="compact" :items="items" />
  </v-container>
</template>

<script setup lang="ts">
  import { computed } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useRoute } from 'vue-router'
  import { useProductStore } from '@/stores/products'

  const route = useRoute()
  const { t } = useI18n()
  const productStore = useProductStore()
  const items = computed(() => {
    const breadcrumbs: { title: string, to?: { name: string }, disabled?: boolean }[] = [{ title: 'Hem', to: { name: 'home' } }]
    if (route.name === 'home') return breadcrumbs
    if (route.name === 'product-detail') {
      breadcrumbs.push({ title: t('navigation.shop'), to: { name: 'shop' } }, { title: t('navigation.products'), to: { name: 'products' } })
    }
    if (String(route.name).startsWith('account-')) {
      breadcrumbs.push({ title: t('navigation.account'), to: { name: 'account' } })
    }
    const labels: Record<string, string> = {
      'shop': 'navigation.shop', 'products': 'navigation.products', 'outlet': 'navigation.outlet', 'product-detail': 'navigation.products', 'cart': 'navigation.cart', 'faq': 'navigation.faq', 'about': 'navigation.about', 'account': 'navigation.account',
      'account-profile': 'account.profile', 'account-orders': 'account.orders', 'account-comments': 'Mina kommentarer',
    }
    const productName = route.name === 'product-detail' ? productStore.selectedProduct?.name : undefined
    const label = productName ?? (route.meta.breadcrumb as string | undefined) ?? labels[String(route.name)]
    if (label) breadcrumbs.push({ title: t(label), disabled: true })
    return breadcrumbs
  })
</script>
