<template>
  <v-btn
    :aria-label="isDark ? 'Aktivera ljust läge' : 'Aktivera mörkt läge'"
    :icon="isDark ? 'mdi-weather-sunny' : 'mdi-weather-night'"
    variant="text"
    @click="toggleTheme"
  />
</template>

<script setup lang="ts">
  import { computed } from 'vue'
  import { useTheme } from 'vuetify'

  const theme = useTheme()
  const isDark = computed(() => theme.global.current.value.dark)

  function toggleTheme () {
    const nextTheme = isDark.value ? 'light' : 'dark'
    theme.global.name.value = nextTheme
    localStorage.setItem('theme', nextTheme)
  }
</script>
