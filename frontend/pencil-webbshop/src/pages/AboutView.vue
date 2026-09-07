<template>
  <div class="about-content">
    <PageHeader :subtitle="t('about.subtitle')" :title="t('about.title')" />

    <section class="about-intro mb-12">
      <p class="text-overline text-primary mb-3">{{ t('about.eyebrow') }}</p>
      <h2>{{ t('about.question') }}</h2>
      <p class="text-h6 font-italic mt-4">{{ t('about.answer') }}</p>
    </section>

    <v-sheet class="about-copy pa-6 pa-md-10 mb-12" color="surface">
      <p>
        {{ t('about.introOne') }}
      </p>

      <p>{{ t('about.introTwo') }}</p>

      <p>
        {{ t('about.introThree') }}
      </p>
    </v-sheet>

    <v-row class="mb-12">
      <v-col cols="12" md="6">
        <v-sheet class="about-copy pa-6 pa-md-8 h-100" color="primary">
          <p class="text-overline mb-3">{{ t('about.visionLabel') }}</p>
          <h2>{{ t('about.visionTitle') }}</h2>

          <p>
            {{ t('about.visionOne') }}
          </p>

          <p>
            {{ t('about.visionTwo') }}
          </p>
        </v-sheet>
      </v-col>

      <v-col cols="12" md="6">
        <v-sheet class="about-copy pa-6 pa-md-8 h-100" color="surface">
          <p class="text-overline text-primary mb-3">{{ t('about.teamLabel') }}</p>
          <h2>{{ t('about.teamTitle') }}</h2>
          <p>{{ t('about.teamIntro') }}</p>

          <ul>
            <li v-for="item in teamItems" :key="item">{{ t(item) }}</li>
          </ul>
        </v-sheet>
      </v-col>
    </v-row>

    <v-sheet class="about-copy about-closing pa-6 pa-md-10 text-center" color="surface">
      <p>
        {{ t('about.closingOne') }}
      </p>

      <p>{{ t('about.closingTwo') }}</p>
      <h2>{{ t('about.closingTitle') }}</h2>
      <p class="mb-0">{{ t('about.closingThree') }}</p>
    </v-sheet>
  </div>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'

  const { t } = useI18n()
  const teamItems = ['about.teamOne', 'about.teamTwo', 'about.teamThree', 'about.teamFour']
</script>

<style scoped>
  .about-content {
    max-width: 1000px;
    margin: 0 auto;
  }

  .about-intro {
    max-width: 720px;
    margin: 0 auto;
    text-align: center;
  }

  .about-intro h2,
  .about-copy h2 {
    color: var(--app-primary);
  }

  .about-copy {
    border: 1px solid var(--app-border);
    line-height: 1.8;
  }

  .about-copy p + p {
    margin-top: 1.25rem;
  }

  .about-copy ul {
    padding-left: 1.25rem;
  }

  .about-copy li + li {
    margin-top: 0.75rem;
  }

  .about-copy.bg-primary {
    color: rgb(var(--v-theme-on-primary));
  }

  .about-copy.bg-primary h2 {
    color: inherit;
  }

  .about-closing h2 {
    margin-top: 2rem;
  }
</style>
