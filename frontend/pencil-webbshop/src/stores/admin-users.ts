import type { AdminUser } from '@/types/admin-user'
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { adminUsersService } from '@/api/admin-users.service'
import { ApiError } from '@/api/client'

export const useAdminUsersStore = defineStore('admin-users', () => {
  const users = ref<AdminUser[]>([])
  const error = ref<string | null>(null)

  async function load () {
    try {
      error.value = null
      users.value = await adminUsersService.list()
    } catch (caughtError) {
      error.value = caughtError instanceof ApiError ? caughtError.message : 'Kunde inte hämta användare.'
    }
  }
  async function toggleBan (userId: number) {
    const updatedUser = await adminUsersService.toggleBan(userId)
    const index = users.value.findIndex(user => user.id === userId)
    if (index !== -1) {
      users.value[index] = updatedUser
    }
  }
  async function remove (userId: number) {
    await adminUsersService.delete(userId)
    users.value = users.value.filter(user => user.id !== userId)
  }

  return { users, error, load, toggleBan, remove }
})
