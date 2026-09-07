/**
 * plugins/vuetify.ts
 *
 * Framework documentation: https://vuetifyjs.com`
 */

// Composables
import { createVuetify } from 'vuetify'
// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const storedTheme = localStorage.getItem('theme')
const defaultTheme = storedTheme === 'dark' ? 'dark' : 'light'

// https://vuetifyjs.com/en/introduction/why-vuetify/#feature-guides
export default createVuetify({
  theme: {
    defaultTheme,
    themes: {
      light: {
        dark: false,
        colors: {
          'primary': '#001F16',
          'secondary': '#D4AF37',
          'background': '#F5F1E7',
          'surface': '#F5F1E7',
          'surface-variant': '#ECE6D9',
          'success': '#2E7D32',
          'warning': '#B9770E',
          'error': '#B3261E',
          'info': '#2563A8',
        },
      },
      dark: {
        dark: true,
        colors: {
          'primary': '#A9CFBE',
          'secondary': '#D4AF37',
          'background': '#0C1110',
          'surface': '#16201C',
          'surface-variant': '#29322E',
          'success': '#81C784',
          'warning': '#F6C667',
          'error': '#F28B82',
          'info': '#8AB4F8',
        },
      },
    },
  },
})
