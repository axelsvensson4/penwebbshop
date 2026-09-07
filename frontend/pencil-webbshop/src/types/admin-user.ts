export interface AdminUser {
  id: number
  name: string
  username: string
  role: 'USER' | 'ADMIN'
  active: boolean
}
