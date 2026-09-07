import { defineStore } from 'pinia'
import { ref } from 'vue'
import { authService, type AuthUser } from '@/api/auth.service'
import { ApiError, setAuthToken } from '@/api/client'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<AuthUser | null>(null)
  const error = ref<string | null>(null)
  const isLoading = ref(false)
  const restored = ref(false)

  async function authenticate (mode: 'login' | 'register', name: string, username: string, password: string, claimOrderId?: number) {
    isLoading.value = true
    error.value = null
    try {
      const result = mode === 'login'
        ? await authService.login(username, password)
        : await authService.register(name, username, password, claimOrderId)
      setAuthToken(result.token)
      user.value = result.user
      return true
    } catch (caughtError) {
      error.value = caughtError instanceof ApiError ? caughtError.message : 'Inloggningen misslyckades.'
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function updateProfile (profile: Pick<AuthUser, 'name' | 'email' | 'address' | 'postal_code' | 'city'>) {
    user.value = await authService.updateProfile(profile)
  }

  async function logout () {
    await authService.logout()
    setAuthToken(null)
    user.value = null
  }

  async function restore () {
    if (restored.value) {
      return
    }

    try {
      user.value = await authService.me()
    } catch {
      user.value = null
    } finally {
      restored.value = true
    }
  }

  return { user, error, isLoading, restored, authenticate, updateProfile, logout, restore }
})
