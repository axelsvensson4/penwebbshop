<template>
  <v-layout class="admin-layout">
    <v-navigation-drawer class="admin-drawer" permanent width="260">
      <div class="admin-brand pa-5">
        <img alt="NORTHPOINT" class="admin-logo" src="/logga.webp">
        <span>NORTHPOINT</span>
      </div>

      <v-divider />

      <v-list class="pt-4" nav>
        <v-list-item
          prepend-icon="mdi-view-dashboard-outline"
          title="Dashboard"
          :to="{ name: 'admin-dashboard' }"
        />

        <v-list-item
          prepend-icon="mdi-account-group-outline"
          title="Användare"
          :to="{ name: 'admin-users' }"
        />

        <v-list-item
          prepend-icon="mdi-package-variant-closed"
          title="Produkter"
          :to="{ name: 'admin-products' }"
        />
      </v-list>
    </v-navigation-drawer>

    <v-main class="admin-main">
      <v-app-bar class="admin-topbar" elevation="0">
        <v-spacer />
        <v-btn prepend-icon="mdi-open-in-new" :to="{ name: 'home' }" variant="text">Till webshopen</v-btn>
        <v-divider class="mx-2" vertical />

        <v-btn prepend-icon="mdi-account-circle-outline" :to="{ name: 'account' }" variant="text">
          {{ auth.user?.name || 'Konto' }}
        </v-btn>
      </v-app-bar>

      <v-container class="admin-content py-8 px-6" max-width="1400">
        <router-view />
      </v-container>
    </v-main>
  </v-layout>
</template>

<script setup lang="ts">
  import { useAuthStore } from '@/stores/auth'

  const auth = useAuthStore()
</script>

<style scoped>
  .admin-layout { min-height: 100vh; background: rgb(var(--v-theme-background)); }
  .admin-drawer { background: #001f16 !important; color: #fff; }
  .admin-brand { display: flex; align-items: center; gap: 0.75rem; font-family: var(--app-font-display); font-size: 1.25rem; font-weight: 700; letter-spacing: 0.05em; }
  .admin-logo { width: 40px; height: 40px; object-fit: contain; }
  .admin-drawer :deep(.v-list-item) { color: #fff; }
  .admin-drawer :deep(.v-list-item--active) { background: rgb(212 175 55 / 22%); color: #d4af37; }
  .admin-main { min-height: 100vh; }
  .admin-topbar { background: rgb(var(--v-theme-surface)) !important; border-bottom: 1px solid var(--app-border); }
  .admin-content { padding-top: 96px !important; }
</style>
