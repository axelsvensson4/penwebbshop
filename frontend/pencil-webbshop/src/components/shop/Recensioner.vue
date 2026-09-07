<template>
  <section aria-labelledby="customer-reviews-title">
    <h2 id="customer-reviews-title" class="text-h4 mb-5">{{ t('reviews.title') }}</h2>

    <div v-if="reviewPages.length > 0" class="reviews-carousel">
      <v-btn
        :aria-label="t('reviews.previous')"
        :disabled="page === 0"
        icon="mdi-chevron-left"
        variant="text"
        @click="page -= 1"
      />

      <v-window v-model="page" class="flex-grow-1">
        <v-window-item v-for="(reviewPage, pageIndex) in reviewPages" :key="pageIndex" :value="pageIndex">
          <v-row>
            <v-col v-for="review in reviewPage" :key="`${review.name}-${review.review_title}`" cols="12" md="3">
              <v-card class="review-card pa-5" flat height="400">
                <v-rating
                  color="secondary"
                  density="compact"
                  :length="5"
                  :model-value="ratingFor(review.rating)"
                  readonly
                  size="18"
                />

                <h3 class="text-h6 mt-3 mb-2">”{{ review.review_title }}”</h3>
                <p class="text-body-2 mb-4">{{ review.review_text }}</p>
                <p class="text-body-2 font-weight-bold mb-0">{{ review.name }}, {{ review.age }}</p>
              </v-card>
            </v-col>
          </v-row>
        </v-window-item>
      </v-window>

      <v-btn
        :aria-label="t('reviews.next')"
        :disabled="page === reviewPages.length - 1"
        icon="mdi-chevron-right"
        variant="text"
        @click="page += 1"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
  import { computed, onMounted, ref } from 'vue'
  import { useI18n } from 'vue-i18n'

  type Review = {
    rating: number
    name: string
    age: number
    review_title: string
    review_text: string
  }

  const reviews = ref<Review[]>([])
  const { t } = useI18n()
  const page = ref(0)
  const reviewPages = computed(() => {
    const pageSize = 4
    return Array.from({ length: Math.ceil(reviews.value.length / pageSize) }, (_, index) => {
      const start = index * pageSize
      return reviews.value.slice(start, start + pageSize)
    })
  })

  function ratingFor (rating: number) {
    return Math.min(5, Math.max(1, rating))
  }

  onMounted(async () => {
    const response = await fetch('/recensions.json')

    if (response.ok) {
      reviews.value = await response.json() as Review[]
    }
  })
</script>

<style scoped>
  .review-card {
    background-color: transparent !important;
    box-shadow: none !important;
  }

  .reviews-carousel {
    display: flex;
    align-items: center;
    gap: 8px;
  }
</style>
