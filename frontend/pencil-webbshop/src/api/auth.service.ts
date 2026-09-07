import { apiClient } from './client'

export interface AuthUser {
  id: number
  name: string
  username: string
  role: 'USER' | 'ADMIN'
  email: string
  address: string
  postal_code: string
  city: string
}

interface LoginResponse {
  token: string
  user: AuthUser
}

export const authService = {
  login (username: string, password: string) {
    return apiClient.post<LoginResponse>('/auth/login', { username, password })
  },
  register (name: string, username: string, password: string, claimOrderId?: number) {
    return apiClient.post<LoginResponse>('/auth/register', { name, username, password, claim_order_id: claimOrderId })
  },
  logout () {
    return apiClient.post<void>('/auth/logout', {})
  },
  me () {
    return apiClient.get<AuthUser>('/auth/me')
  },
  updateProfile (profile: Pick<AuthUser, 'name' | 'email' | 'address' | 'postal_code' | 'city'>) {
    return apiClient.patch<AuthUser>('/auth/me', profile)
  },
}
