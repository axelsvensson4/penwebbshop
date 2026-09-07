/**
 * router/index.ts
 *
 * Manual routes for ./src/pages/*.vue
 */

// Composables
import { createRouter, createWebHistory } from 'vue-router'
import AdminLayout from '@/layouts/AdminLayout.vue'
import ShopLayout from '@/layouts/ShopLayout.vue'
import AboutView from '@/pages/AboutView.vue'
import AccountView from '@/pages/account/AccountView.vue'
import AddressesView from '@/pages/account/AddressesView.vue'
import CommentsView from '@/pages/account/CommentsView.vue'
import OrdersView from '@/pages/account/OrdersView.vue'
import ProfileView from '@/pages/account/ProfileView.vue'
import SettingsView from '@/pages/account/SettingsView.vue'
import AdminDashboardView from '@/pages/admin/AdminDashboardView.vue'
import AdminUsersView from '@/pages/admin/AdminUsersView.vue'
import ProductCreateView from '@/pages/admin/products/ProductCreateView.vue'
import ProductEditView from '@/pages/admin/products/ProductEditView.vue'
import ProductsAdminView from '@/pages/admin/products/ProductsAdminView.vue'
import CartView from '@/pages/CartView.vue'
import CheckoutView from '@/pages/CheckoutView.vue'
import FaqView from '@/pages/FaqView.vue'
import HomeView from '@/pages/HomeView.vue'
import LoginView from '@/pages/LoginView.vue'
import OrderConfirmationView from '@/pages/OrderConfirmationView.vue'
import OutletView from '@/pages/OutletView.vue'
import ProductDetailView from '@/pages/ProductDetailView.vue'
import ProductsView from '@/pages/ProductsView.vue'
import ShopView from '@/pages/ShopView.vue'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: ShopLayout,
      children: [
        { path: '', name: 'home', component: HomeView },
        { path: 'shop', name: 'shop', component: ShopView },
        { path: 'shop/products', name: 'products', component: ProductsView },
        { path: 'shop/products/:id', name: 'product-detail', component: ProductDetailView },
        { path: 'shop/outlet', name: 'outlet', component: OutletView },
        { path: 'cart', name: 'cart', component: CartView },
        { path: 'checkout', name: 'checkout', component: CheckoutView },
        { path: 'order-confirmation', name: 'order-confirmation', component: OrderConfirmationView },
        { path: 'faq', name: 'faq', component: FaqView },
        { path: 'about', name: 'about', component: AboutView },
        {
          path: 'account',
          meta: { requiresAuth: true },
          children: [
            { path: '', name: 'account', component: AccountView, meta: { requiresAuth: true } },
            { path: 'orders', name: 'account-orders', component: OrdersView, meta: { requiresAuth: true } },
            { path: 'comments', name: 'account-comments', component: CommentsView, meta: { requiresAuth: true } },
            { path: 'profile', name: 'account-profile', component: ProfileView, meta: { requiresAuth: true } },
            { path: 'addresses', name: 'account-addresses', component: AddressesView, meta: { requiresAuth: true } },
            { path: 'settings', name: 'account-settings', component: SettingsView, meta: { requiresAuth: true } },
          ],
        },
      ],
    },
    {
      path: '/admin',
      meta: { requiresAuth: true, roles: ['ADMIN'] },
      component: AdminLayout,
      children: [
        { path: '', redirect: { name: 'admin-dashboard' } },
        { path: 'dashboard', name: 'admin-dashboard', component: AdminDashboardView, meta: { requiresAuth: true, roles: ['ADMIN'] } },
        { path: 'users', name: 'admin-users', component: AdminUsersView, meta: { requiresAuth: true, roles: ['ADMIN'] } },
        { path: 'products', name: 'admin-products', component: ProductsAdminView, meta: { requiresAuth: true, roles: ['ADMIN'] } },
        { path: 'products/new', name: 'admin-product-create', component: ProductCreateView, meta: { requiresAuth: true, roles: ['ADMIN'] } },
        { path: 'products/:id', name: 'admin-product-edit', component: ProductEditView, meta: { requiresAuth: true, roles: ['ADMIN'] } },
      ],
    },
    { path: '/login', name: 'login', component: LoginView },
  ],
})

router.beforeEach(async to => {
  const auth = useAuthStore()
  await auth.restore()
  const roles = to.meta.roles as string[] | undefined
  if (to.meta.requiresAuth && !auth.user) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (roles?.includes('ADMIN') && auth.user?.role !== 'ADMIN') {
    return { name: 'account' }
  }
})

export default router
