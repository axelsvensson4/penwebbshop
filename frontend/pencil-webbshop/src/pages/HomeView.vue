<template>
  <div class="home-content">
    <section class="home-section mb-12">
      <v-sheet class="home-hero pa-8 pa-md-12" color="secondary" rounded="lg">
        <div class="hero-content">
          <div class="hero-copy">
            <h1 class="text-h3 text-md-h2 font-weight-bold mb-4">{{ t('hero.title') }}</h1>
            <p class="text-body-1 mb-6">{{ t('hero.text') }}</p>
            <v-btn class="home-cta" :to="{ name: 'products' }" variant="flat">{{ t('common.viewProducts') }}</v-btn>
          </div>

          <v-img alt="NORTHPOINT" class="hero-logo" src="/bilder/loggaa.png" />
        </div>
      </v-sheet>
    </section>

    <section class="home-section mb-12">
      <h2 class="text-h4 mb-5">{{ t('home.featured') }}</h2>

      <v-row>
        <v-col
          v-for="product in productStore.products"
          :key="product.id"
          cols="12"
          md="3"
          sm="6"
        >
          <ProductCard
            :id="product.id"
            :availability="product.is_available"
            compact
            :compare-at-price="product.compare_at_price_ore"
            :currency="product.currency"
            :image="product.image_url"
            :name="product.name"
            :price="product.price_ore"
            :rating="product.average_rating"
            :stock-quantity="product.stock_quantity"
            :stock-status="product.availability"
            :summary="product.summary"
          />
        </v-col>
      </v-row>
    </section>

    <section class="home-section mb-12">
      <h2 class="text-h4 mb-5">{{ t('home.benefits') }}</h2>

      <v-row>
        <v-col v-for="benefit in benefits" :key="benefit.icon" cols="12" md="4">
          <v-card border class="pa-5" color="surface" height="100%">
            <v-avatar color="white" size="48">
              <v-icon color="surface" :icon="benefit.icon" size="26" />
            </v-avatar>

            <p class="text-h6 mt-4">{{ t(benefit.text) }}</p>
          </v-card>
        </v-col>
      </v-row>
    </section>

    <Recensioner class="home-section" />
  </div>
</template>

<script setup lang="ts">
  import { onMounted } from 'vue'
  import { useI18n } from 'vue-i18n'
  import ProductCard from '@/components/shop/ProductCard.vue'
  import Recensioner from '@/components/shop/Recensioner.vue'
  import { useProductStore } from '@/stores/products'

  const { t } = useI18n()
  const productStore = useProductStore()
  const benefits = [
    { icon: 'mdi-check-decagram-outline', text: 'home.benefitOne' },
    { icon: 'mdi-shield-check-outline', text: 'home.benefitTwo' },
    { icon: 'mdi-chat-question-outline', text: 'home.benefitThree' },
  ]

  onMounted(() => {
    productStore.fetchProducts({ available_only: false, featured: true, limit: 4 })
  })

</script>

<style scoped>
  .home-hero {
    color: #001f16;
    box-shadow: var(--app-shadow-sm);
  }

  .hero-content {
    display: grid;
    align-items: center;
    gap: 2rem;
    grid-template-columns: minmax(0, 1fr) minmax(160px, 0.45fr);
  }

  .hero-copy { max-width: 650px; }
  .hero-logo {
    justify-self: center;
    max-width: 190px;
    width: 100%;
    border: 1px solid #000;
  }

  .home-cta {
    background-color: #000 !important;
    color: #fff !important;
  }

  .home-content {
    max-width: 1120px;
    margin: 0 auto;
  }

  .home-section :deep(.v-card) {
    background-color: rgb(var(--v-theme-surface));
  }

  @media (max-width: 600px) {
    .hero-content { display: flex; flex-direction: column; align-items: flex-start; }
    .hero-logo { align-self: center; width: 150px; }
  }
</style>
