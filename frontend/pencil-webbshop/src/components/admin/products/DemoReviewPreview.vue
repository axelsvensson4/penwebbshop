<template>
  <v-card border class="pa-5">
    <div class="d-flex align-center justify-space-between mb-4">
      <h2 class="text-h6">{{ t('admin.demo.title') }}</h2>
      <v-btn size="small" variant="tonal" @click="generate">{{ t('admin.actions.generatePreview') }}</v-btn>
    </div>

    <v-rating
      v-model="rating"
      :aria-label="t('admin.demo.rating')"
      color="amber"
      density="compact"
      readonly
      size="22"
    />

    <v-list v-if="reviews.length > 0" class="mt-2" density="compact">
      <v-list-item v-for="review in reviews" :key="review" prepend-icon="mdi-comment-outline" :title="review" />
    </v-list>

    <p v-else class="text-body-2 text-medium-emphasis">{{ t('admin.demo.empty') }}</p>
    <p class="text-caption text-warning mt-3">{{ t('admin.demo.notice') }}</p>
  </v-card>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useI18n } from 'vue-i18n'

  const { t } = useI18n()
  const rating = ref(0)
  const reviews = ref<string[]>([])
  const templates = ['Bra kvalitet och snabb leverans.', 'Produkten motsvarade mina förväntningar.', 'Enkel att använda och bra kvalitet.', 'Mycket nöjd med produkten.', 'Bra produkt till rimligt pris.']

  function generate () {
    rating.value = Math.floor(Math.random() * 5) + 1
    const selectedReviews = new Set<string>()
    const count = 3 + Math.floor(Math.random() * 3)
    while (selectedReviews.size < count) {
      selectedReviews.add(templates[Math.floor(Math.random() * templates.length)])
    }
    reviews.value = [...selectedReviews]
  }
</script>
