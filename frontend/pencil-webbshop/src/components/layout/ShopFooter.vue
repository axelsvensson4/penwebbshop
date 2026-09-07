<template>
  <v-footer class="shop-footer mt-16" color="primary">
    <v-container class="d-flex flex-column align-center text-center ga-6 py-16" max-width="1440">
      <div>
        <p class="footer-brand mb-3">NORTHPOINT</p>
        <div class="footer-line mx-auto" />
      </div>

      <div class="footer-languages">
        <div class="text-body-2 font-weight-bold mb-1">{{ t('common.language') }}</div>

        <div class="d-flex flex-wrap ga-1">
          <v-btn
            v-for="language in languages"
            :key="language.code"
            :active="locale === language.code"
            size="small"
            variant="text"
            @click="changeLocale(language.code)"
          >
            {{ language.label }}
          </v-btn>
        </div>
      </div>

      <div class="d-flex flex-wrap justify-center ga-3">
        <v-btn size="small" :to="{ name: 'faq' }" variant="text">{{ t('navigation.faq') }}</v-btn>
        <v-btn size="small" :to="{ name: 'about' }" variant="text">{{ t('navigation.about') }}</v-btn>
      </div>

      <span class="text-body-2 footer-copyright">© {{ new Date().getFullYear() }} NORTHPOINT</span>
    </v-container>
  </v-footer>
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

  function changeLocale (language: SupportedLocale) {
    setLocale(language)
  }
</script>

<style scoped>
  .shop-footer {
    color: var(--app-secondary);
  }

  .footer-brand {
    font-family: var(--app-font-display);
    font-size: 2rem;
    font-weight: 700;
  }

  .footer-line {
    width: 48px;
    height: 1px;
    background: var(--app-secondary);
  }

  .footer-languages :deep(.v-btn),
  :deep(.v-btn) {
    color: var(--app-secondary);
  }

  .footer-copyright {
    color: rgb(var(--v-theme-secondary) / 70%);
  }
</style>
