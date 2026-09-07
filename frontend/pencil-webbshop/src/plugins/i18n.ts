import { createI18n } from 'vue-i18n'
import en from '@/i18n/locales/en'
import ja from '@/i18n/locales/ja'
import sv from '@/i18n/locales/sv'

export const supportedLocales = ['sv', 'en', 'ja'] as const
export type SupportedLocale = typeof supportedLocales[number]

const storedLocale = localStorage.getItem('locale')
const initialLocale = supportedLocales.includes(storedLocale as SupportedLocale)
  ? storedLocale as SupportedLocale
  : 'sv'

const i18n = createI18n({
  legacy: false,
  locale: initialLocale,
  fallbackLocale: 'sv',
  messages: { sv, en, ja },
})

export function setLocale (locale: SupportedLocale) {
  i18n.global.locale.value = locale
  localStorage.setItem('locale', locale)
}

export default i18n
