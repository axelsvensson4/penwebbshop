<template>
  <v-menu>
    <template #activator="{ props }">
      <v-btn v-bind="props" :aria-label="t('navigation.account')" icon="mdi-account-circle-outline" variant="text" />
    </template>

    <v-list density="compact" min-width="190">
      <template v-if="!auth.user">
        <v-list-item :title="t('account.login')" :to="{ name: 'login' }" />
        <v-list-item :title="t('account.register')" :to="{ name: 'login', query: { mode: 'register' } }" />
      </template>

      <template v-else>
        <v-list-item :title="t('navigation.account')" :to="{ name: 'account' }" />

        <v-list-item
          v-if="auth.user.role === 'ADMIN'"
          title="Administration"
          :to="{ name: 'admin-dashboard' }"
        />

        <v-list-item :title="t('account.logout')" @click="logout" />
      </template>
    </v-list>
  </v-menu>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import { useAuthStore } from '@/stores/auth'

  const { t } = useI18n()
  const auth = useAuthStore()

  async function logout () {
    await auth.logout()
    window.location.assign(import.meta.env.BASE_URL)
  }
</script>
