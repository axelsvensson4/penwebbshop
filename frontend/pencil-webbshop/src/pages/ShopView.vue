<template>
  <PageHeader :subtitle="t('shop.intro')" :title="t('shop.title')" />

  <v-row>
    <v-col cols="12" md="6">
      <v-card
        border
        class="pa-6"
        height="100%"
        link
        :to="{ name: 'products' }"
      >
        <v-icon icon="mdi-view-grid-outline" size="36" />
        <h2 class="text-h5 mt-4">{{ t('navigation.products') }}</h2>
        <p class="text-body-1 text-medium-emphasis mt-2">{{ t('shop.productsText') }}</p>
      </v-card>
    </v-col>

    <v-col cols="12" md="6">
      <v-card
        border
        class="pa-6"
        height="100%"
        link
        :to="{ name: 'outlet' }"
      >
        <v-icon icon="mdi-tag-outline" size="36" />
        <h2 class="text-h5 mt-4">{{ t('navigation.outlet') }}</h2>
        <p class="text-body-1 text-medium-emphasis mt-2">{{ t('shop.outletText') }}</p>
      </v-card>
    </v-col>
  </v-row>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'

  const { t } = useI18n()
</script>
