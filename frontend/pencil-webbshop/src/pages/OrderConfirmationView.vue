<template>
  <section class="confirmation-page">
    <v-card class="pa-8 text-center" max-width="520">
      <v-icon color="success" icon="mdi-check-circle-outline" size="72" />
      <h1 class="text-h4 mt-5">Tack för din beställning!</h1>

      <p class="text-body-1 text-medium-emphasis mt-3">
        Din beställning är mottagen och vi börjar förbereda dina pennor.
      </p>

      <v-btn
        v-if="!auth.user && orderId"
        class="mt-2"
        color="secondary"
        @click="createAccount"
      >
        Skapa ett konto
      </v-btn>

      <v-btn class="mt-5" color="primary" @click="goHome">Till startsidan</v-btn>
    </v-card>
  </section>
</template>

<script setup lang="ts">
  import { computed, onMounted } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import { useCartStore } from '@/stores/cart'

  const route = useRoute()
  const router = useRouter()
  const auth = useAuthStore()
  const cart = useCartStore()
  const orderId = computed(() => {
    const value = Number(route.query.order)
    return Number.isInteger(value) && value > 0 ? value : null
  })

  onMounted(() => auth.restore())

  async function createAccount () {
    if (!orderId.value) return
    await router.push({ name: 'login', query: { mode: 'register', claimOrder: orderId.value } })
  }

  async function goHome () {
    if (!auth.user && orderId.value) {
      await cart.cancelOrderClaim(orderId.value)
    }
    await router.push({ name: 'home' })
  }
</script>

<style scoped>
  .confirmation-page { display: grid; min-height: 55vh; place-items: center; }
</style>
