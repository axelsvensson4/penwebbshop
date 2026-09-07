<template>
  <PageHeader :title="t('cart.title')" />

  <v-row>
    <v-col cols="12" :md="cart.items.length > 0 ? 7 : 12">
      <v-alert
        v-if="cart.items.length > 0"
        class="mb-4"
        color="secondary"
        icon="mdi-lightbulb-outline"
        variant="tonal"
      >
        <strong>TIPS!</strong> Priset är samma oberoende av skick, välj en Ny.
      </v-alert>

      <v-list v-if="cart.items.length > 0">
        <template v-for="(item, index) in cart.items" :key="item.id">
          <v-list-item class="cart-item py-3">
            <template #prepend>
              <v-avatar class="mr-4" rounded size="72">
                <v-img v-if="item.image_url" :alt="item.name" cover :src="getImageUrl(item.image_url)" />
                <v-icon v-else icon="mdi-image-outline" />
              </v-avatar>
            </template>

            <v-list-item-title class="font-weight-bold">{{ item.name }}</v-list-item-title>
            <v-list-item-subtitle>Skick: {{ conditionLabel(item.condition) }}</v-list-item-subtitle>

            <template #append>
              <div class="d-flex align-center ga-2">
                <v-btn
                  aria-label="Minska antal"
                  density="compact"
                  icon="mdi-minus"
                  variant="text"
                  @click="cart.updateQuantity(item, item.quantity - 1)"
                />

                <span class="quantity-value">{{ item.quantity }}</span>

                <v-btn
                  aria-label="Öka antal"
                  density="compact"
                  icon="mdi-plus"
                  variant="text"
                  @click="cart.updateQuantity(item, item.quantity + 1)"
                />

                <span class="item-total">{{ formatPrice(item.price_ore * item.quantity) }}</span>

                <v-btn
                  aria-label="Ta bort från kundvagnen"
                  color="secondary"
                  density="compact"
                  icon="mdi-trash-can-outline"
                  variant="text"
                  @click="cart.removeItem(item.id)"
                />
              </div>
            </template>
          </v-list-item>

          <v-divider v-if="index < cart.items.length - 1" />
        </template>
      </v-list>

      <template v-else>
        <div class="empty-cart">
          <v-alert color="secondary" icon="mdi-cart-outline" variant="tonal">{{ t('cart.empty') }}</v-alert>
          <v-btn class="mt-4" color="primary" :to="{ name: 'products' }">Kolla in våra produkter</v-btn>
        </div>
      </template>
    </v-col>

    <v-col v-if="cart.items.length > 0" cols="12" md="5">
      <v-card border class="pa-5">
        <h2 class="text-h6 mb-4">{{ t('cart.summary') }}</h2>
        <div class="d-flex justify-space-between mb-2"><span>{{ t('cart.subtotal') }}</span><span>{{ formatPrice(cart.subtotalOre) }}</span></div>
        <div class="d-flex justify-space-between mb-4"><span>{{ t('cart.shipping') }}</span><span>{{ formatPrice(cart.shippingOre) }}</span></div>
        <v-divider class="mb-4" />
        <div class="d-flex justify-space-between font-weight-bold"><span>{{ t('common.total') }}</span><span>{{ formatPrice(cart.totalOre) }}</span></div>
        <v-btn block class="mt-6" color="primary" :to="{ name: 'checkout' }">{{ t('cart.checkout') }}</v-btn>
        <v-btn block class="mt-2" variant="text" @click="cart.clear">Töm kundvagn</v-btn>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'
  import { useCartStore } from '@/stores/cart'

  const { t } = useI18n()
  const cart = useCartStore()
  function conditionLabel (condition: 'NEW' | 'USED' | 'WORN') {
    return { NEW: 'Ny', USED: 'Begagnad', WORN: 'Sliten' }[condition]
  }

  function formatPrice (priceOre: number) {
    return new Intl.NumberFormat('sv-SE', { style: 'currency', currency: 'SEK' }).format(priceOre / 100)
  }

  function getImageUrl (imageUrl: string) {
    if (!imageUrl.startsWith('/')) return imageUrl
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'
    return `${new URL(apiBaseUrl).origin}${imageUrl}`
  }
  onMounted(() => {
    cart.load()
  })
</script>

<style scoped>
  .quantity-value {
    min-width: 1.5rem;
    text-align: center;
  }

  .item-total {
    min-width: 92px;
    text-align: right;
  }

  .empty-cart {
    display: flex;
    flex-direction: column;
    align-items: center;
    max-width: 440px;
    margin: 3rem auto;
    text-align: center;
  }

  .empty-cart :deep(.v-alert) {
    width: 100%;
  }
</style>
