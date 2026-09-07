<template>
  <div class="page-header mb-12 text-center">
    <p v-if="eyebrow" class="text-overline text-primary">{{ eyebrow }}</p>
    <h1 class="text-h3 font-weight-bold mb-2">{{ title }}</h1>
    <p v-if="subtitle" class="text-body-1 text-medium-emphasis">{{ subtitle }}</p>
  </div>
</template>

<script setup lang="ts">
  defineProps<{ title: string, subtitle?: string, eyebrow?: string }>()
</script>

<style scoped>
  .page-header::after {
    display: block;
    width: min(100%, 320px);
    height: 1px;
    margin: 2rem auto 0;
    background: var(--app-secondary);
    content: '';
  }

  .page-header h1 {
    color: var(--app-primary);
  }
</style>
