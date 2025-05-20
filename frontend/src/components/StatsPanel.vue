<template>
  <div v-if="problems.length" class="card shadow-sm p-4 mb-4">
    <h3 class="h6 mb-3">Project Statistics</h3>
    <canvas ref="chart"></canvas>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import { evaluationCriteria } from '../utils/constants.js'

const props = defineProps({ problems: Array })
const chart = ref(null)

const render = async () => {
  if (!props.problems.length) return
  await nextTick() // wait for <canvas> to exist

  const avgs = evaluationCriteria.map(criteria => {
    const validVals = props.problems
      .map(q => q[criteria.key])
      .filter(v => v !== null && v !== undefined)

    if (!validVals.length) return 0  // no evaluated problems yet for this field

    const total = validVals.reduce((a, b) => a + b, 0)
    return total / validVals.length
  })

  new Chart(chart.value, {
    type: 'bar',
    data: {
      labels: evaluationCriteria.map(c => c.name),
      datasets: [{
        data: avgs,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        title: {
          display: true,
          text: 'Average Evaluation Scores',
          font: { size: 16 }
        },
        tooltip: {
          callbacks: {
            label: function(context) {
              const idx = context.dataIndex
              const criteria = evaluationCriteria[idx]
              const value = context.dataset.data[idx]
              return [
                `${criteria.name}: ${value.toFixed(2)}`,
                criteria.description  // show the long description!
              ]
            }
          }
        }
      },
      scales: {
        y: {
          suggestedMin: 0,
          suggestedMax: 2 ,
          ticks: { stepSize: 1 }
        }
      }
    }
  })

}

onMounted(render)
watch(() => props.problems, render)
</script>
