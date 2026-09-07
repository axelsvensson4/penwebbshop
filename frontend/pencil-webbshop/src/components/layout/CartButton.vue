<template>
  <v-badge color="surface" :content="itemCount" :model-value="itemCount > 0"><v-btn :aria-label="t('navigation.cart')" icon="mdi-cart-outline" :to="{ name: 'cart' }" variant="text" /></v-badge>
</template>

<script setup lang="ts">
  import { computed, onMounted } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useCartStore } from '@/stores/cart'

  const { t } = useI18n()
  const cart = useCartStore()
  const itemCount = computed(() => cart.items.reduce((total, item) => total + item.quantity, 0))
  onMounted(() => {
    cart.load()
  })
</script>
