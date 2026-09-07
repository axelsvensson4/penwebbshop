<template>
  <v-snackbar
    class="cart-added-toast"
    location="top"
    :model-value="cart.addedDialogOpen"
    timeout="3500"
    @update:model-value="cart.setAddedDialogOpen"
  >
    <div class="d-flex align-center ga-3 text-white font-weight-bold">
      <v-icon icon="mdi-cart-check" size="24" />
      Produkten är tillagd i varukorgen.
    </div>
  </v-snackbar>
</template>

<script setup lang="ts">
  import { useCartStore } from '@/stores/cart'

  const cart = useCartStore()
</script>

<style scoped>
  .cart-added-toast :deep(.v-snackbar__wrapper) {
    background: #3f3f3f;
    color: #fff;
  }
</style>
