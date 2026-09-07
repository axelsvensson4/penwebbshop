<template>
  <PageHeader :title="t('faq.title')" />

  <v-expansion-panels variant="accordion">
    <v-expansion-panel v-for="item in items" :key="item.question" :text="t(item.answer)" :title="t(item.question)" />
  </v-expansion-panels>
</template>

<script setup lang="ts">
  import { useI18n } from 'vue-i18n'
  import PageHeader from '@/components/common/PageHeader.vue'

  const { t } = useI18n()
  const items = [
    { question: 'faq.q1', answer: 'faq.a1' },
    { question: 'faq.q2', answer: 'faq.a2' },
    { question: 'faq.q3', answer: 'faq.a3' },
    { question: 'faq.q4', answer: 'faq.a4' },
    { question: 'faq.q5', answer: 'faq.a5' },
    { question: 'faq.q6', answer: 'faq.a6' },
    { question: 'faq.q7', answer: 'faq.a7' },
    { question: 'faq.q8', answer: 'faq.a8' },
    { question: 'faq.q9', answer: 'faq.a9' },
    { question: 'faq.q10', answer: 'faq.a10' },
  ]
</script>
