<template>
  <h1 class="text-h4 mb-2">Dashboard</h1>
  <p class="text-medium-emphasis mb-8">Översikt över din webbshop.</p>

  <v-card border class="sales-card pa-5 mb-6">
    <div class="d-flex flex-wrap align-center justify-space-between ga-4 mb-5">
      <div>
        <p class="text-h6 mb-1">Försäljning</p>
        <p class="text-body-2 text-medium-emphasis mb-0">Utveckling mellan 0 och 100 000 000 SEK</p>
      </div>

      <v-btn-toggle
        v-model="period"
        color="primary"
        density="compact"
        mandatory
        rounded="lg"
      >
        <v-btn value="week">Vecka</v-btn>
        <v-btn value="month">Månad</v-btn>
        <v-btn value="year">År</v-btn>
      </v-btn-toggle>
    </div>

    <svg
      aria-label="Försäljningskurva"
      class="sales-chart"
      preserveAspectRatio="none"
      role="img"
      viewBox="0 0 660 180"
    >
      <text v-for="axis in yAxis" :key="axis.value" x="0" :y="axis.y">{{ axis.value }}</text>

      <line
        v-for="line in gridLines"
        :key="line"
        x1="55"
        x2="660"
        :y1="line"
        :y2="line"
      />

      <path :d="chartPath" />
    </svg>

    <div class="d-flex justify-space-between text-caption text-medium-emphasis mt-2">
      <span>{{ labels.start }}</span>
      <span>{{ labels.end }}</span>
    </div>
  </v-card>

</template>

<script setup lang="ts">
  import { computed, ref } from 'vue'

  const period = ref<'week' | 'month' | 'year'>('week')
  const series = {
    week: [18, 42, 30, 66, 49, 75, 61, 38, 54, 47, 72, 64, 83, 59, 41, 68, 52, 79, 63, 45, 70, 57, 88, 69, 76],
    month: [12, 26, 21, 45, 39, 58, 52, 73, 62, 84, 71, 90, 68, 54, 77, 61, 83, 74, 92, 70, 86, 63, 81, 75, 95],
    year: [8, 19, 15, 37, 32, 55, 48, 67, 58, 81, 72, 94, 76, 62, 85, 71, 89, 65, 78, 56, 82, 69, 91, 74, 97],
  }
  const labelsByPeriod = {
    week: { start: 'Måndag', end: 'Söndag' },
    month: { start: 'Dag 1', end: 'Dag 30' },
    year: { start: 'Januari', end: 'December' },
  }
  const gridLines = [20, 60, 100, 140, 180]
  const yAxis = [
    { value: '100 000 000', y: 20 },
    { value: '75 000 000', y: 60 },
    { value: '50 000 000', y: 100 },
    { value: '25 000 000', y: 140 },
    { value: '0', y: 180 },
  ]
  const chartPath = computed(() => {
    const values = series[period.value]
    const points = values.map((value, index) => {
      const x = 55 + (index / (values.length - 1)) * 605
      const y = 180 - (value / 100) * 160 - 10
      return { x, y }
    })
    return points.slice(0, -1).reduce((path, point, index) => {
      const previous = points[index - 1] ?? point
      const next = points[index + 1]
      const afterNext = points[index + 2] ?? next
      const controlOneX = point.x + (next.x - previous.x) / 6
      const controlOneY = point.y + (next.y - previous.y) / 6
      const controlTwoX = next.x - (afterNext.x - point.x) / 6
      const controlTwoY = next.y - (afterNext.y - point.y) / 6
      return `${path} C ${controlOneX},${controlOneY} ${controlTwoX},${controlTwoY} ${next.x},${next.y}`
    }, `M ${points[0].x},${points[0].y}`)
  })
  const labels = computed(() => labelsByPeriod[period.value])
</script>

<style scoped>
  .sales-card { background: rgb(var(--v-theme-surface)); }
  .sales-chart { display: block; width: 100%; height: 220px; overflow: visible; }
  .sales-chart line { stroke: rgb(var(--v-theme-on-surface) / 12%); stroke-width: 1; }
  .sales-chart text { fill: #fff; font-size: 8px; }
  .sales-chart path { fill: none; stroke: #d4af37; stroke-linecap: round; stroke-linejoin: round; stroke-width: 4; }
</style>
