<template>
  <v-container max-width="480">
    <v-btn class="mb-4" prepend-icon="mdi-arrow-left" :to="{ name: 'home' }" variant="text">
      Tillbaka till startsidan
    </v-btn>

    <v-card border class="pa-6">
      <h1 class="text-h5 mb-5">{{ registerMode ? 'Skapa användare' : 'Logga in' }}</h1>

      <v-form @submit.prevent="submit">
        <v-text-field v-if="registerMode" v-model="name" label="Namn" required />
        <v-text-field v-model="username" label="Användarnamn" required />
        <v-text-field v-model="password" label="Lösenord" required type="password" />
        <v-alert v-if="auth.error" class="mb-3" type="error">{{ auth.error }}</v-alert>
        <v-btn block color="primary" :loading="auth.isLoading" type="submit">{{ registerMode ? 'Skapa konto' : 'Logga in' }}</v-btn>
      </v-form>

      <v-btn block class="mt-3" variant="text" @click="registerMode = !registerMode">{{ registerMode ? 'Har du konto? Logga in' : 'Skapa användare' }}</v-btn>
    </v-card>

    <v-dialog v-model="captchaOpen" max-width="800" persistent>
      <v-card class="pa-6">
        <h2 class="text-h4 text-center mb-2">CAPTCHA</h2>
        <p class="text-h6 text-center mb-5">Hitta waldo</p>

        <v-img
          alt="Hitta Waldo"
          class="waldo-image"
          cover
          :src="'/bilder/wldo.png'"
          @click="findWaldo"
        />

        <v-alert v-if="captchaMessage" class="mt-5" :type="captchaMessageType" variant="tonal">
          {{ captchaMessage }}
        </v-alert>

        <v-btn
          v-if="captchaAttempt >= 3"
          block
          class="mt-5"
          color="primary"
          :loading="auth.isLoading"
          @click="completeRegistration"
        >
          Nästa
        </v-btn>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'

  const auth = useAuthStore()
  const route = useRoute()
  const router = useRouter()
  const registerMode = ref(route.query.mode === 'register')
  const name = ref('')
  const username = ref('')
  const password = ref('')
  const captchaOpen = ref(false)
  const captchaAttempt = ref(0)
  const captchaMessage = ref('')
  const captchaMessageType = ref<'error' | 'success'>('error')

  async function submit () {
    if (registerMode.value) {
      captchaAttempt.value = 0
      captchaMessage.value = ''
      captchaOpen.value = true
      return
    }
    if (await auth.authenticate('login', name.value, username.value, password.value)) {
      await router.push(String(route.query.redirect ?? '/account'))
    }
  }

  function findWaldo () {
    captchaAttempt.value += 1
    if (captchaAttempt.value === 1) {
      captchaMessageType.value = 'error'
      captchaMessage.value = 'Du hittade någon. Tyvärr inte rätt någon.'
      return
    }
    if (captchaAttempt.value === 2) {
      captchaMessageType.value = 'success'
      captchaMessage.value = 'Grattis! Du hittade… någon helt annan.'
      window.setTimeout(() => {
        if (captchaAttempt.value === 2) captchaMessageType.value = 'error'
      }, 1000)
      return
    }
    captchaMessageType.value = 'success'
    captchaMessage.value = 'Du hittade Waldo! 🎉 Han var tydligen där hela tiden.'
  }

  async function completeRegistration () {
    const claimOrderId = Number(route.query.claimOrder)
    const canClaimOrder = Number.isInteger(claimOrderId) && claimOrderId > 0
    if (await auth.authenticate('register', name.value, username.value, password.value, canClaimOrder ? claimOrderId : undefined)) {
      captchaOpen.value = false
      await router.push(String(route.query.redirect ?? '/account'))
    }
  }
</script>

<style scoped>
  .waldo-image {
    cursor: crosshair;
    max-height: 440px;
  }
</style>
