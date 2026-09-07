<template>
  <v-menu>
    <template #activator="{ props }">
      <v-btn v-bind="props" :aria-label="t('common.language')" icon="mdi-web" variant="text" />
    </template>

    <v-list density="compact">
      <v-list-item v-for="language in languages" :key="language.code" :active="locale === language.code" @click="changeLocale(language.code)">
        <v-list-item-title>{{ language.label }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import { setLocale, type SupportedLocale } from '@/plugins/i18n'

  const { locale, t } = useI18n()
  const languages: { code: SupportedLocale, label: string }[] = [
    { code: 'sv', label: 'Svenska' },
    { code: 'en', label: 'English' },
    { code: 'ja', label: '日本語' },
  ]
  const changeLocale = (language: SupportedLocale) => setLocale(language)
</script>
