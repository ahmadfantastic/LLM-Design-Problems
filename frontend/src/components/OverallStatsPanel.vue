<template>
  <div v-if="stats" class="card shadow-sm p-4 mb-4">
    <h3 class="h6 mb-3">My Evaluation</h3>
    <div v-if="stats.user_model_avg" class="table-responsive mb-3">
      <table class="table table-sm">
        <thead>
          <tr>
            <th>Metric</th>
            <th v-for="m in userModelKeys" :key="m">{{ m }}</th>
            <th>All Models</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in evaluationCriteria" :key="c.key">
            <th>{{ c.name }}</th>
            <td v-for="m in userModelKeys" :key="m">
              {{ formatScore(stats.user_model_avg[m][c.key]) }}
            </td>
            <td>{{ formatScore(stats.user_avg[c.key]) }}</td>
          </tr>
          <tr>
            <th>Weighted Score</th>
            <td v-for="m in userModelKeys" :key="m">
              {{ formatScore(weightedScore(stats.user_model_avg[m])) }}
            </td>
            <td>{{ formatScore(weightedScore(stats.user_avg)) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <ul v-else class="list-group mb-3">
      <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ c.name }}</span>
        <span>{{ formatScore(stats.user_avg[c.key]) }}</span>
      </li>
      <li class="list-group-item d-flex justify-content-between align-items-center">
        <strong>Weighted Score</strong>
        <span>{{ formatScore(weightedScore(stats.user_avg)) }}</span>
      </li>
    </ul>
    <div v-if="stats.model_avg">
      <h6>Overall Evaluation</h6>
      <div class="table-responsive">
        <table class="table table-sm">
          <thead>
            <tr>
              <th>Metric</th>
              <th v-for="m in modelKeys" :key="m">{{ m }}</th>
              <th>All Models</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in evaluationCriteria" :key="c.key">
              <th>{{ c.name }}</th>
              <td v-for="m in modelKeys" :key="m">
                {{ formatScore(stats.model_avg[m][c.key]) }}
              </td>
              <td>{{ formatScore(stats.overall_avg && stats.overall_avg[c.key]) }}</td>
            </tr>
            <tr>
              <th>Weighted Score</th>
              <td v-for="m in modelKeys" :key="m">
                {{ formatScore(weightedScore(stats.model_avg[m])) }}
              </td>
              <td>{{ formatScore(weightedScore(stats.overall_avg)) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
  </div>
  <div v-else-if="stats.overall_avg">
      <h6>Overall Evaluation</h6>
      <ul class="list-group mb-3">
        <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
          <span>{{ c.name }}</span>
          <span>{{ formatScore(stats.overall_avg[c.key]) }}</span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <strong>Weighted Score</strong>
          <span>{{ formatScore(weightedScore(stats.overall_avg)) }}</span>
        </li>
      </ul>
    </div>
    <div v-if="stats.interrater">
      <h6>Interrater Agreement (Weighted Kappa)</h6>
      <ul class="list-group mb-3">
        <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
          <span>{{ c.name }}</span>
          <span>{{ formatKappa(stats.interrater[c.key]) }}</span>
        </li>
        <li class="list-group-item d-flex justify-content-between align-items-center">
          <strong>Overall</strong>
          <span>{{ formatKappa(stats.interrater.overall) }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, computed } from 'vue'
import axios from 'axios'
import { evaluationCriteria } from '../utils/constants.js'

const stats = ref(null)

const modelKeys = computed(() => {
  return stats.value && stats.value.model_avg ? Object.keys(stats.value.model_avg) : []
})

const userModelKeys = computed(() => {
  return stats.value && stats.value.user_model_avg ? Object.keys(stats.value.user_model_avg) : []
})

const fetchStats = async () => {
  const { data } = await axios.get('/api/stats')
  stats.value = data
}

const formatKappa = (val) => {
  if (val === null || val === undefined) return 'N/A'
  return val.toFixed(2)
}

const formatScore = (val) => {
  if (val === null || val === undefined) return 'N/A'
  return val.toFixed(2)
}

const weightedScore = (obj) => {
  if (!obj) return null
  let sum = 0
  let total = 0
  for (const c of evaluationCriteria) {
    const v = obj[c.key]
    if (v !== null && v !== undefined) {
      sum += v * c.weight
      total += c.weight
    }
  }
  return total > 0 ? sum / total : null
}

onMounted(fetchStats)
</script>

