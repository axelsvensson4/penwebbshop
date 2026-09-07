<template>
  <PageHeader title="Mina kommentarer" />

  <v-card border class="pa-5">
    <p v-if="store.reviews.length === 0" class="mb-0">Inga kommentarer ännu.</p>

    <div v-else>
      <template v-for="(review, index) in store.reviews" :key="review.id">
        <article class="py-4">
          <div class="d-flex flex-wrap align-center ga-3 mb-2">
            <v-rating
              color="secondary"
              density="compact"
              :model-value="review.rating"
              readonly
              size="18"
            />

            <span class="text-medium-emphasis">{{ formatDate(review.created_at) }}</span>
          </div>

          <p class="text-body-2 text-medium-emphasis mb-1">Penna: {{ review.product_name || 'Okänd produkt' }}</p>
          <h2 class="text-subtitle-1 font-weight-bold mb-1">{{ review.review_title }}</h2>
          <p class="mb-0">{{ review.comment }}</p>
        </article>

        <v-divider v-if="index < store.reviews.length - 1" />
      </template>
    </div>
  </v-card>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import PageHeader from '@/components/common/PageHeader.vue'
  import { useReviewStore } from '@/stores/reviews'

  const store = useReviewStore()
  function formatDate (value: string) {
    return new Intl.DateTimeFormat('sv-SE', { dateStyle: 'long' }).format(new Date(value))
  }
  onMounted(() => store.loadMine())
</script>
