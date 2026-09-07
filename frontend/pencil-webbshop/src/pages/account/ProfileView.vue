<template>
  <PageHeader :title="t('account.profile')" />

  <v-form @submit.prevent="save">
    <v-text-field v-model="profile.name" label="Namn" />

    <v-text-field v-model="profile.email" label="E-post" type="email" />

    <v-text-field v-model="profile.address" label="Gatuadress" />

    <v-row>
      <v-col cols="12" sm="4"><v-text-field v-model="profile.postal_code" label="Postnummer" /></v-col>
      <v-col cols="12" sm="8"><v-text-field v-model="profile.city" label="Ort" /></v-col>
    </v-row>

    <v-btn color="primary" type="submit">Spara</v-btn>
  </v-form>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'
  import { useAuthStore } from '@/stores/auth'

  const { t } = useI18n()
  const auth = useAuthStore()
  const profile = ref({
    name: auth.user?.name ?? '',
    email: auth.user?.email ?? '',
    address: auth.user?.address ?? '',
    postal_code: auth.user?.postal_code ?? '',
    city: auth.user?.city ?? '',
  })

  async function save () {
    await auth.updateProfile(profile.value)
  }
</script>
