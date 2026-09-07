<template>
  <v-form ref="form" @submit.prevent="save">
    <v-row>
      <v-col cols="12" md="7">
        <v-card border class="pa-5 mb-5">
          <h2 class="text-h6 mb-4">{{ t('admin.sections.information') }}</h2>

          <v-text-field
            v-model="input.name"
            counter="120"
            :label="t('admin.fields.name')"
            required
            :rules="nameRules"
          />

          <v-text-field
            v-model="input.short_description"
            counter="240"
            :label="t('admin.fields.shortDescription')"
            required
            :rules="shortDescriptionRules"
          />

          <v-text-field
            v-model.number="input.price"
            :label="t('admin.fields.price')"
            min="0"
            prefix="SEK"
            required
            :rules="priceRules"
            step="0.01"
            type="number"
          />

          <v-text-field
            v-model.number="input.stock_quantity"
            label="Lagersaldo"
            min="0"
            prepend-inner-icon="mdi-package-variant-closed-check"
            required
            type="number"
          />
        </v-card>

        <v-card border class="pa-5 mb-5">
          <h2 class="text-h6 mb-4">{{ t('admin.sections.classification') }}</h2>

          <v-select
            v-model="input.category"
            :items="categories"
            :label="t('admin.fields.category')"
            required
            :rules="requiredRules"
          />

          <v-select v-model="input.product_type" :items="productTypes" :label="t('admin.fields.productType')" />
          <v-switch v-model="input.active" color="primary" inset :label="t('admin.fields.active')" />
          <v-switch v-model="input.featured" color="primary" inset label="Utvald på startsidan" />
        </v-card>
      </v-col>

      <v-col cols="12" md="5">
        <v-card border class="pa-5 mb-5">
          <h2 class="text-h6 mb-4">{{ t('admin.fields.image') }}</h2>

          <v-file-input
            v-model="image"
            accept="image/jpeg,image/png,image/webp"
            :label="t('admin.fields.image')"
            prepend-icon="mdi-camera"
            :rules="imageRules"
            show-size
          />

          <v-text-field v-model="altText" :label="t('admin.fields.altText')" />

          <v-img
            v-if="imagePreview"
            :alt="altText || input.name"
            class="mt-2"
            cover
            height="220"
            :src="imagePreview"
          />
        </v-card>

        <v-card border class="pa-5 mb-5">
          <h2 class="text-h6 mb-4">{{ t('admin.sections.preview') }}</h2>

          <ProductCard
            :id="0"
            :availability="input.availability !== 'OUT_OF_STOCK'"
            compact
            :image="imagePreview"
            :name="input.name || t('admin.preview.productName')"
            preview
            :price="priceInOre"
            :stock-quantity="input.stock_quantity"
            :stock-status="input.availability"
            :summary="input.short_description"
          />
        </v-card>
      </v-col>
    </v-row>

    <v-alert v-if="store.error" class="mt-5" type="error" variant="tonal">{{ store.error }}</v-alert>
    <div class="d-flex justify-end ga-3 mt-6"><v-btn :to="{ name: 'admin-products' }" variant="text">{{ t('admin.actions.cancel') }}</v-btn><v-btn color="primary" :disabled="store.isSaving" :loading="store.isSaving" type="submit">{{ t('admin.actions.save') }}</v-btn></div>
  </v-form>
</template>

<script setup lang="ts">
  import type { AdminProduct, ProductCreateInput } from '@/types/admin-product'
  import { computed, onBeforeUnmount, ref, watch } from 'vue'
  import { useI18n } from 'vue-i18n'
  import { useRouter } from 'vue-router'
  import ProductCard from '@/components/shop/ProductCard.vue'
  import { useAdminProductsStore } from '@/stores/admin-products'

  const { t } = useI18n()
  const router = useRouter()
  const store = useAdminProductsStore()
  const props = defineProps<{ product?: AdminProduct }>()
  const form = ref()
  const image = ref<File | File[] | null>(null)
  const altText = ref('')
  const imagePreview = ref<string | null>(null)
  const input = ref<ProductCreateInput>({ name: '', short_description: '', description: '-', price: 0, currency: 'SEK', category: 'Lyxiga', product_type: 'STANDARD', availability: 'IN_STOCK', condition: 'NEW', active: true, featured: false, stock_quantity: 10 })
  const requiredRules = [(value: string) => Boolean(value) || t('admin.validation.required')]
  const nameRules = [(value: string) => Boolean(value) || t('admin.validation.required'), (value: string) => value.length <= 120 || t('admin.validation.nameLength')]
  const shortDescriptionRules = [(value: string) => Boolean(value) || t('admin.validation.required'), (value: string) => value.length <= 240 || t('admin.validation.shortDescriptionLength')]
  const priceRules = [(value: number) => value >= 0 || t('admin.validation.price')]
  const imageRules = [(value: File | File[] | null) => !value || (Array.isArray(value) ? value[0] : value).size <= 5 * 1024 * 1024 || t('admin.validation.imageSize')]
  const categories = computed(() => ['Lyxiga', 'Traditionella', 'Fjäderpenna', 'För astronauter', 'Limited Edition'])
  const productTypes = computed(() => [{ title: t('admin.productTypes.standard'), value: 'STANDARD' }, { title: t('admin.productTypes.outlet'), value: 'OUTLET' }])
  const priceInOre = computed(() => Math.round((input.value.price || 0) * 100))

  watch(image, value => {
    if (imagePreview.value) URL.revokeObjectURL(imagePreview.value)
    const file = Array.isArray(value) ? value[0] : value
    imagePreview.value = file ? URL.createObjectURL(file) : null
  })
  watch(() => props.product, product => {
    if (!product) return
    input.value = {
      name: product.name,
      short_description: product.short_description,
      description: product.description,
      price: product.price_ore / 100,
      currency: 'SEK',
      category: product.category,
      product_type: product.product_type,
      availability: product.availability,
      condition: product.condition,
      active: product.active,
      featured: product.featured,
      stock_quantity: product.stock_quantity,
    }
    altText.value = product.name
    imagePreview.value = product.image_url ? getImageUrl(product.image_url) : null
  }, { immediate: true })
  onBeforeUnmount(() => {
    if (imagePreview.value) URL.revokeObjectURL(imagePreview.value)
  })

  async function save () {
    const validation = await form.value?.validate()
    if (!validation?.valid) return
    const selectedImage = Array.isArray(image.value) ? image.value[0] : image.value
    const productInput = props.product
      ? input.value
      : { ...input.value, description: '-', condition: 'NEW' as const, availability: 'IN_STOCK' as const }
    const product = props.product
      ? await store.updateProduct(props.product.id, productInput, selectedImage ?? undefined, altText.value || input.value.name)
      : await store.createProduct(productInput, selectedImage ?? undefined, altText.value || input.value.name)
    if (product) await router.push({ name: 'admin-products' })
  }

  function getImageUrl (imageUrl: string) {
    if (!imageUrl.startsWith('/')) return imageUrl
    const apiBaseUrl = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000/api'
    return `${new URL(apiBaseUrl).origin}${imageUrl}`
  }
</script>
