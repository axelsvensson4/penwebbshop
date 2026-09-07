import { defineStore } from 'pinia'
import { ref } from 'vue'
import { type Order, type Review, reviewsService } from '@/api/reviews.service'

export const useReviewStore = defineStore('reviews', () => {
  const reviews = ref<Review[]>([])
  const orders = ref<Order[]>([])
  async function loadMine () {
    reviews.value = await reviewsService.mine()
    orders.value = await reviewsService.orders()
  }
  async function create (productId: number, rating: number, title: string, comment: string) {
    const review = await reviewsService.create(productId, rating, title, comment)
    reviews.value.unshift(review)
    return review
  }
  async function remove (productId: number, reviewId: number) {
    await reviewsService.delete(productId, reviewId)
    reviews.value = reviews.value.filter(review => review.id !== reviewId)
  }
  return { reviews, orders, loadMine, create, remove }
})
