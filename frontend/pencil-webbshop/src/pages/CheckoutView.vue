<template>
  <section v-if="paymentState !== 'form'" class="payment-state">
    <v-card class="payment-card pa-8 text-center" max-width="440">
      <template v-if="paymentState === 'bankid'">
        <v-img alt="QR-kod för BankID" class="qr-code mx-auto mb-6" :src="'/bilder/qr.png'" />
        <h1 class="text-h5 mb-3">Öppna BankID för att slutföra köpet</h1>
        <p class="text-medium-emphasis mb-0">Skanna QR-koden i BankID-appen.</p>
      </template>

      <template v-else>
        <v-progress-circular color="secondary" indeterminate size="60" width="5" />
        <h1 class="text-h5 mt-6 mb-2">Bearbetar betalning</h1>
        <p class="text-medium-emphasis mb-0">Ett ögonblick...</p>
      </template>
    </v-card>
  </section>

  <template v-else>
    <PageHeader :title="t('checkout.title')" />

    <v-form ref="form" @submit.prevent="submitOrder">
      <v-row>
        <v-col cols="12" md="7">
          <v-card border class="pa-5">
            <v-alert
              v-if="!auth.user"
              class="mb-5"
              color="secondary"
              icon="mdi-account-outline"
              variant="tonal"
            >
              Du kan fortsätta som gäst och fylla i dina uppgifter här, eller logga in för att använda ditt konto.

              <template #append>
                <v-btn color="primary" size="small" variant="flat" @click="goToLogin">Logga in</v-btn>
              </template>
            </v-alert>

            <h2 class="text-h6">{{ t('checkout.contact') }}</h2>

            <v-text-field
              v-model="customer.name"
              class="mt-4"
              label="Namn"
              required
              :rules="requiredRules"
            />

            <v-text-field
              v-model="customer.email"
              label="E-post"
              required
              :rules="emailRules"
              type="email"
            />

            <v-divider class="my-5" />
            <h2 class="text-h6">{{ t('checkout.address') }}</h2>

            <v-text-field
              v-model="customer.address"
              class="mt-4"
              label="Gatuadress"
              required
              :rules="requiredRules"
            />

            <v-row>
              <v-col cols="12" sm="4"><v-text-field v-model="customer.postalCode" label="Postnummer" required :rules="requiredRules" /></v-col>
              <v-col cols="12" sm="8"><v-text-field v-model="customer.city" label="Ort" required :rules="requiredRules" /></v-col>
            </v-row>
          </v-card>
        </v-col>

        <v-col cols="12" md="5">
          <v-card border class="pa-5">
            <h2 class="text-h6 mb-4">{{ t('cart.summary') }}</h2>
            <div class="d-flex justify-space-between mb-2"><span>{{ t('cart.subtotal') }}</span><span>{{ formatPrice(cart.subtotalOre) }}</span></div>
            <div class="d-flex justify-space-between mb-4"><span>{{ t('cart.shipping') }}</span><span>{{ formatPrice(cart.shippingOre) }}</span></div>
            <v-divider class="mb-4" />
            <div class="d-flex justify-space-between font-weight-bold"><span>{{ t('common.total') }}</span><span>{{ formatPrice(cart.totalOre) }}</span></div>

            <v-divider class="my-5" />
            <h2 class="text-h6">{{ t('checkout.payment') }}</h2>

            <v-radio-group v-model="paymentMethod" class="mt-3" hide-details>
              <v-radio label="Kort" value="CARD">
                <template #label><v-icon class="mr-2" icon="mdi-credit-card-outline" />Kort</template>
              </v-radio>

              <v-radio label="Swish" value="SWISH">
                <template #label><v-icon class="mr-2" icon="mdi-cellphone" />Swish</template>
              </v-radio>
            </v-radio-group>

            <div v-if="paymentMethod === 'CARD'" class="mt-4">
              <v-text-field
                v-model="card.number"
                label="Kortnummer"
                placeholder="1234 5678 9012 3456"
                required
                :rules="cardRules"
              />

              <v-row>
                <v-col cols="6"><v-text-field
                  v-model="card.expiry"
                  label="Giltigt till"
                  placeholder="MM/ÅÅ"
                  required
                  :rules="expiryRules"
                /></v-col>

                <v-col cols="6"><v-text-field v-model="card.cvc" label="CVC" required :rules="cvcRules" /></v-col>
              </v-row>
            </div>

            <v-text-field
              v-else
              v-model="swishNumber"
              class="mt-4"
              label="Swish-nummer"
              placeholder="07X-XXX XX XX"
              required
              :rules="swishRules"
            />

            <v-btn
              block
              class="mt-6"
              color="primary"
              :disabled="!canSubmit"
              type="submit"
            >{{ t('checkout.submit') }}</v-btn>
          </v-card>
        </v-col>
      </v-row>
    </v-form>
  </template>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useRouter } from 'vue-router'
  import PageHeader from '@/components/common/PageHeader.vue'
  import { useAuthStore } from '@/stores/auth'
  import { useCartStore } from '@/stores/cart'

  const { t } = useI18n()
  const router = useRouter()
  const cart = useCartStore()
  const auth = useAuthStore()
  const form = ref()
  const paymentState = ref<'form' | 'bankid' | 'processing'>('form')
  const paymentMethod = ref<'CARD' | 'SWISH'>('CARD')
  const customer = ref({ name: '', email: '', address: '', postalCode: '', city: '' })
  const card = ref({ number: '', expiry: '', cvc: '' })
  const swishNumber = ref('')
  const requiredRules = [(value: string) => Boolean(value?.trim()) || 'Fältet är obligatoriskt.']
  const emailRules = [...requiredRules, (value: string) => (value.includes('@') && value.includes('.')) || 'Ange en giltig e-postadress.']
  const cardRules = [...requiredRules, (value: string) => value.replaceAll(' ', '').length >= 12 || 'Ange ett giltigt kortnummer.']
  const expiryRules = [...requiredRules, (value: string) => /^\d{2}\/\d{2}$/.test(value) || 'Ange MM/ÅÅ.']
  const cvcRules = [...requiredRules, (value: string) => /^\d{3,4}$/.test(value) || 'Ange en giltig CVC.']
  const swishRules = [...requiredRules, (value: string) => /^07\d{7,8}$/.test(value.replaceAll(/[-\s]/g, '')) || 'Ange ett giltigt Swish-nummer.']
  const hasValidCustomer = computed(() => {
    const { name, email, address, postalCode, city } = customer.value
    return Boolean(name.trim() && email.includes('@') && email.includes('.') && address.trim() && postalCode.trim() && city.trim())
  })
  const hasValidPayment = computed(() => paymentMethod.value === 'CARD'
    ? card.value.number.replaceAll(' ', '').length >= 12 && /^\d{2}\/\d{2}$/.test(card.value.expiry) && /^\d{3,4}$/.test(card.value.cvc)
    : /^07\d{7,8}$/.test(swishNumber.value.replaceAll(/[-\s]/g, '')))
  const canSubmit = computed(() => cart.items.length > 0 && hasValidCustomer.value && hasValidPayment.value)

  function formatPrice (priceOre: number) {
    return new Intl.NumberFormat('sv-SE', { style: 'currency', currency: 'SEK' }).format(priceOre / 100)
  }

  async function goToLogin () {
    await router.push({ name: 'login', query: { redirect: '/checkout' } })
  }

  async function submitOrder () {
    if (!canSubmit.value) return
    const validation = await form.value?.validate()
    if (!validation?.valid) return
    paymentState.value = 'bankid'
    window.setTimeout(() => {
      paymentState.value = 'processing'
      window.setTimeout(finishCheckout, 2000)
    }, 5000)
  }

  async function finishCheckout () {
    try {
      const { order_id: orderId } = await cart.completeCheckout()
      await router.push({ name: 'order-confirmation', query: { order: orderId } })
    } catch {
      paymentState.value = 'form'
    }
  }

  onMounted(async () => {
    await cart.load()
    await auth.restore()
    if (auth.user) {
      customer.value = {
        name: auth.user.name,
        email: auth.user.email,
        address: auth.user.address,
        postalCode: auth.user.postal_code,
        city: auth.user.city,
      }
    }
  })
</script>

<style scoped>
  .payment-state { display: grid; min-height: 55vh; place-items: center; }
  .payment-card { width: min(100%, 440px); }
  .qr-code {
    width: 220px;
    aspect-ratio: 1;
  }
</style>
