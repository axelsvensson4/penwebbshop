<template>
  <v-app-bar class="shop-navbar" elevation="0">
    <v-container class="d-flex align-center h-100 px-4 px-md-10 position-relative" fluid>

      <v-btn aria-label="NORTHPOINT startsida" class="brand-mark" :to="{ name: 'home' }" variant="text">
        <img alt="NORTHPOINT" class="brand-image" src="/logga.webp">
      </v-btn>

      <nav aria-label="Huvudnavigation" class="main-nav d-none d-md-flex ga-1">
        <v-menu open-on-hover>
          <template #activator="{ props }">
            <v-btn v-bind="props" :to="{ name: 'shop' }" variant="text">{{ t('navigation.shop') }}</v-btn>
          </template>

          <v-list density="compact">
            <v-list-item :title="t('navigation.products')" :to="{ name: 'products' }" />
            <v-list-item :title="t('navigation.outlet')" :to="{ name: 'outlet' }" />
          </v-list>
        </v-menu>

        <v-btn :to="{ name: 'faq' }" variant="text">{{ t('navigation.faq') }}</v-btn>
        <v-btn :to="{ name: 'about' }" variant="text">{{ t('navigation.about') }}</v-btn>
      </nav>

      <div class="ml-auto d-flex align-center ga-1">
        <ThemeToggle />
        <CartButton />
        <ProfileMenu />

        <v-btn
          aria-label="Öppna meny"
          class="d-md-none"
          icon="mdi-menu"
          variant="text"
          @click="drawerOpen = true"
        />
      </div>
    </v-container>
  </v-app-bar>

  <v-navigation-drawer v-model="drawerOpen" location="right" temporary>
    <v-list nav>
      <v-list-item :title="t('navigation.shop')" :to="{ name: 'shop' }" @click="drawerOpen = false" />
      <v-list-item class="pl-8" :title="t('navigation.products')" :to="{ name: 'products' }" @click="drawerOpen = false" />
      <v-list-item class="pl-8" :title="t('navigation.outlet')" :to="{ name: 'outlet' }" @click="drawerOpen = false" />
      <v-list-item :title="t('navigation.faq')" :to="{ name: 'faq' }" @click="drawerOpen = false" />
      <v-list-item :title="t('navigation.about')" :to="{ name: 'about' }" @click="drawerOpen = false" />
    </v-list>
  </v-navigation-drawer>
</template>

<script setup lang="ts">
  import { ref } from 'vue'
  import { useI18n } from 'vue-i18n'
  import CartButton from './CartButton.vue'
  import ProfileMenu from './ProfileMenu.vue'
  import ThemeToggle from './ThemeToggle.vue'

  const { t } = useI18n()
  const drawerOpen = ref(false)
</script>

<style scoped>
  .shop-navbar {
    background-color: #d4af37 !important;
    color: #001f16 !important;
    border-bottom: 1px solid rgb(0 31 22 / 25%);
  }

  .brand-mark {
    background: transparent !important;
    color: var(--app-primary);
    min-width: 64px;
    height: 64px;
    padding: 0;
    box-shadow: none;
  }

  .brand-mark :deep(.v-btn__overlay),
  .brand-mark :deep(.v-btn__underlay) {
    opacity: 0;
  }

  .brand-image {
    display: block;
    width: 56px;
    height: 56px;
    object-fit: contain;
  }

  .main-nav {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }

  :deep(nav .v-btn) {
    color: #414845;
  }

  :deep(nav .v-btn:hover),
  :deep(nav .v-btn.router-link-active) {
    color: #001f16;
  }

  .shop-navbar :deep(.v-btn) {
    color: #001f16;
  }

  @media (max-width: 959px) {
    .brand-mark {
      min-width: 52px;
      height: 52px;
    }

    .brand-image {
      width: 46px;
      height: 46px;
    }
  }
</style>
