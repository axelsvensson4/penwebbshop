<template>
  <PageHeader :title="t('account.addresses')" />
  <v-alert type="info" variant="tonal">{{ t('common.comingSoon') }}</v-alert>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'

  const { t } = useI18n()
</script>
