<template>
  <ShopNavbar />
  <CartAddedDialog />

  <v-main>
    <ShopBreadcrumbs v-if="$route.name !== 'home'" />

    <v-container class="shop-content pt-8 pb-16" max-width="1440">
      <router-view />
    </v-container>
  </v-main>

  <ShopFooter />
</template>

<script setup lang="ts">
  import CartAddedDialog from '@/components/layout/CartAddedDialog.vue'
  import ShopBreadcrumbs from '@/components/layout/ShopBreadcrumbs.vue'
  import ShopFooter from '@/components/layout/ShopFooter.vue'
  import ShopNavbar from '@/components/layout/ShopNavbar.vue'
</script>
