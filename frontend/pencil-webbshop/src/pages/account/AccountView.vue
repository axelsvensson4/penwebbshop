<template>
  <PageHeader :subtitle="t('account.intro')" :title="t('account.title')" />
  <h2 class="text-h5 mb-5">{{ t('account.welcome') }}</h2>

  <v-row>
    <v-col v-for="item in items" :key="item.route" cols="12" md="4">
      <v-card
        border
        class="pa-5"
        height="100%"
        link
        :to="{ name: item.route }"
      >
        <h3 class="text-h6">{{ t(item.title) }}</h3>
        <p class="text-body-2 text-medium-emphasis mt-2">{{ t(item.text) }}</p>
      </v-card>
    </v-col>
  </v-row>

</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'

  const { t } = useI18n()
  const items = [
    { route: 'account-profile', title: 'account.profile', text: 'account.profileText' },
    { route: 'account-orders', title: 'account.orders', text: 'account.ordersText' },
    { route: 'account-comments', title: 'Mina kommentarer', text: 'Se dina publicerade produktomdömen.' },
  ]
</script>
