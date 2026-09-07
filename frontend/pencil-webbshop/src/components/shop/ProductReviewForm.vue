<template>
  <v-card border class="mt-3 pa-3">
    <v-alert
      v-if="!auth.user"
      class="mb-3"
      color="secondary"
      density="compact"
      variant="tonal"
    >
      Logga in för att lägga kommentar
    </v-alert>

    <v-rating v-model="rating" density="compact" :disabled="!auth.user" size="20" />

    <v-text-field
      v-model="title"
      class="mt-2"
      :disabled="!auth.user"
      hide-details
      label="Titel på omdömet"
    />

    <v-textarea
      v-model="comment"
      :disabled="!auth.user"
      hide-details
      label="Text"
      rows="2"
    />

    <v-btn
      class="mt-3"
      :disabled="!canSubmit || submitting"
      :loading="submitting"
      size="small"
      @click="submit"
    >
      Skicka kommentar
    </v-btn>
  </v-card>
</template>
<script setup lang="ts">
  import type { Review } from '@/api/reviews.service'
  import { computed, ref } from 'vue'
  import { useAuthStore } from '@/stores/auth'
  import { useReviewStore } from '@/stores/reviews'

  const props = defineProps<{ productId: number }>()
  const emit = defineEmits<{
    created: [review: Review]
    confirmed: [temporaryId: number, review: Review]
    failed: [temporaryId: number]
  }>()
  const auth = useAuthStore()
  const reviews = useReviewStore()
  const rating = ref(5)
  const title = ref('')
  const comment = ref('')
  const submitting = ref(false)
  const canSubmit = computed(() => Boolean(auth.user && title.value.trim() && comment.value.trim()))

  async function submit () {
    if (!canSubmit.value || !auth.user) return

    const temporaryId = -Date.now()
    const optimisticReview: Review = {
      id: temporaryId,
      product_id: props.productId,
      user_id: auth.user.id,
      rating: rating.value,
      comment: comment.value.trim(),
      author_name: auth.user.name,
      review_title: title.value.trim(),
      created_at: new Date().toISOString(),
    }
    emit('created', optimisticReview)
    title.value = ''
    comment.value = ''
    submitting.value = true
    try {
      const review = await reviews.create(
        props.productId,
        optimisticReview.rating,
        optimisticReview.review_title,
        optimisticReview.comment,
      )
      emit('confirmed', temporaryId, review)
    } catch {
      emit('failed', temporaryId)
    } finally {
      submitting.value = false
    }
  }
</script>
