<template>
  <PageHeader :title="t('account.orders')" />

  <v-card border class="pa-5">
    <p v-if="store.orders.length === 0" class="mb-0">Inga beställningar ännu.</p>

    <v-list v-else>
      <v-list-group
        v-for="order in store.orders"
        :key="order.id"
      >
        <template #activator="{ props }">
          <v-list-item
            v-bind="props"
            :subtitle="`${formatDate(order.created_at)} · ${statusLabel(order.status)}`"
            :title="`Beställning #${order.id}`"
          />
        </template>

        <v-list-item
          v-for="item in order.items"
          :key="item.id"
          class="pl-10"
          :subtitle="`${conditionLabel(item.condition)} · ${item.quantity} st`"
          :title="`${item.product_name} · ${formatPrice(item.price_ore * item.quantity)}`"
        />

        <v-list-item
          class="pl-10 font-weight-bold"
          :title="`Totalt: ${formatPrice(orderTotal(order))}`"
        />
      </v-list-group>
    </v-list>
  </v-card>
</template>

<script setup lang="ts">
  import type { Order } from '@/api/reviews.service'
  import { onMounted } from 'vue'
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'
  import { useReviewStore } from '@/stores/reviews'

  const { t } = useI18n()
  const store = useReviewStore()
  function formatDate (value: string) {
    return new Intl.DateTimeFormat('sv-SE', { dateStyle: 'long', timeStyle: 'short' }).format(new Date(value))
  }
  function formatPrice (priceOre: number) {
    return new Intl.NumberFormat('sv-SE', { style: 'currency', currency: 'SEK' }).format(priceOre / 100)
  }
  function conditionLabel (condition: 'NEW' | 'USED' | 'WORN') {
    return { NEW: 'Ny', USED: 'Begagnad', WORN: 'Sliten' }[condition]
  }
  function statusLabel (status: string) {
    return { PENDING: 'Mottagen' }[status] ?? status
  }
  function orderTotal (order: Order) {
    return order.items.reduce((total, item) => total + item.price_ore * item.quantity, 0) + 4900
  }
  onMounted(() => store.loadMine())
</script>
