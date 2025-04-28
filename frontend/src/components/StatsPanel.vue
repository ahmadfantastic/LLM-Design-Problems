<template>
  <div v-if="questions.length" class="border rounded-xl p-6">
    <h3 class="text-lg font-semibold mb-4">Project Statistics</h3>
    <canvas ref="chart"></canvas>
  </div>
</template>
<script setup>
import { onMounted, ref, watch } from 'vue'
import Chart from 'chart.js/auto'
const props = defineProps({ questions: Array })
const chart = ref(null)
const render = () => {
  if (!props.questions.length) return
  const labels = ['alignment', 'complexity', 'clarity', 'feasibility']
  const avgs = labels.map(l => {
    const vals = props.questions.map(q => q.evaluation?.[l] || 0)
    return vals.reduce((a, b) => a + b, 0) / vals.length
  })
  new Chart(chart.value, {
    type: 'bar',
    data: { labels, datasets: [{ data: avgs }] },
  })
}
onMounted(render)
watch(() => props.questions, render)
</script>