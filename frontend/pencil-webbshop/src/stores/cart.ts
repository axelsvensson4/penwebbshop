import { defineStore } from 'pinia'
import { ref } from 'vue'
import { type CartItem, cartService } from '@/api/cart.service'

export const useCartStore = defineStore('cart', () => {
  const error = ref<string | null>(null)
  const items = ref<CartItem[]>([])
  const subtotalOre = ref(0)
  const shippingOre = ref(4900)
  const totalOre = ref(4900)
  const addedDialogOpen = ref(false)
  async function load () {
    try {
      const cart = await cartService.get()
      items.value = cart.items
      subtotalOre.value = cart.subtotal_ore
      shippingOre.value = cart.shipping_ore
      totalOre.value = cart.total_ore
    } catch {
      items.value = []
      subtotalOre.value = 0
      shippingOre.value = 4900
      totalOre.value = 4900
    }
  }
  async function add (productId: number, condition: 'NEW' | 'USED' | 'WORN', quantity = 1) {
    try {
      error.value = null
      await cartService.add(productId, condition, quantity)
      await load()
      addedDialogOpen.value = true
      return true
    } catch {
      error.value = 'Kunde inte lägga produkten i kundvagnen.'
      return false
    }
  }
  async function updateQuantity (item: CartItem, quantity: number) {
    if (quantity < 1) {
      return
    }
    try {
      error.value = null
      await cartService.update(item, quantity)
      await load()
    } catch {
      error.value = 'Kunde inte uppdatera antalet i kundvagnen.'
    }
  }
  async function removeItem (itemId: number) {
    try {
      error.value = null
      await cartService.remove(itemId)
      await load()
    } catch {
      error.value = 'Kunde inte ta bort produkten från kundvagnen.'
    }
  }
  async function clear () {
    await cartService.clear()
    items.value = []
    subtotalOre.value = 0
    shippingOre.value = 4900
    totalOre.value = 4900
  }
  async function completeCheckout () {
    const result = await cartService.checkout()
    items.value = []
    subtotalOre.value = 0
    shippingOre.value = 4900
    totalOre.value = 4900
    return result
  }
  async function cancelOrderClaim (orderId: number) {
    await cartService.cancelOrderClaim(orderId)
  }
  function setAddedDialogOpen (isOpen: boolean) {
    addedDialogOpen.value = isOpen
  }
  return { error, items, subtotalOre, shippingOre, totalOre, addedDialogOpen, load, add, updateQuantity, removeItem, clear, completeCheckout, cancelOrderClaim, setAddedDialogOpen }
})
