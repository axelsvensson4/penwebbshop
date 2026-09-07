import type { AdminUser } from '@/types/admin-user'
import { apiClient } from './client'

export const adminUsersService = {
  list () {
    return apiClient.get<AdminUser[]>('/admin/users')
  },
  toggleBan (userId: number) {
    return apiClient.patch<AdminUser>(`/admin/users/${userId}/ban`, {})
  },
  delete (userId: number) {
    return apiClient.delete<void>(`/admin/users/${userId}`)
  },
}
