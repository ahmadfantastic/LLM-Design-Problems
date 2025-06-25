<template>
  <div v-if="stats" class="card shadow-sm p-4 mb-4">
    <h3 class="h6 mb-3">My Evaluation</h3>
    <div v-if="stats.user_model_avg" class="table-responsive mb-3">
      <table class="table table-sm">
        <thead>
          <tr>
            <th rowspan="2">Metric</th>
            <template v-for="m in userModelKeys" :key="m">
              <th class="text-center" colspan="4">{{ m }}</th>
            </template>
            <th class="text-center" colspan="4">All Models</th>
          </tr>
          <tr>
            <template v-for="m in userModelKeys">
              <th>Yes</th>
              <th>Maybe</th>
              <th>No</th>
              <th>Score</th>
            </template>
            <th>Yes</th>
            <th>Maybe</th>
            <th>No</th>
            <th>Score</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="c in evaluationCriteria" :key="c.key">
            <th>{{ c.name }}</th>
            <template v-for="m in userModelKeys">
              <td>{{ percent(stats.user_model_avg[m][c.key], 'yes') }}</td>
              <td>{{ percent(stats.user_model_avg[m][c.key], 'maybe') }}</td>
              <td>{{ percent(stats.user_model_avg[m][c.key], 'no') }}</td>
              <td>{{ formatScore(stats.user_model_avg[m][c.key]) }}</td>
            </template>
            <td>{{ percent(stats.user_avg[c.key], 'yes') }}</td>
            <td>{{ percent(stats.user_avg[c.key], 'maybe') }}</td>
            <td>{{ percent(stats.user_avg[c.key], 'no') }}</td>
            <td>{{ formatScore(stats.user_avg[c.key]) }}</td>
          </tr>
          <tr>
            <th>Weighted Score</th>
            <template v-for="m in userModelKeys">
              <td colspan="3"></td>
              <td>{{ formatScore(weightedScore(stats.user_model_avg[m])) }}</td>
            </template>
            <td colspan="3"></td>
            <td>{{ formatScore(weightedScore(stats.user_avg)) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <ul v-else class="list-group mb-3">
      <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ c.name }}</span>
        <span>{{ percent(stats.user_avg[c.key], 'yes') }} / {{ percent(stats.user_avg[c.key], 'maybe') }} / {{ percent(stats.user_avg[c.key], 'no') }} ({{ formatScore(stats.user_avg[c.key]) }})</span>
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
              <th rowspan="2">Metric</th>
              <template v-for="m in modelKeys" :key="m">
                <th class="text-center" colspan="4">{{ m }}</th>
              </template>
              <th class="text-center" colspan="4">All Models</th>
            </tr>
            <tr>
              <template v-for="m in modelKeys">
                <th>Yes</th>
                <th>Maybe</th>
                <th>No</th>
                <th>Score</th>
              </template>
              <th>Yes</th>
              <th>Maybe</th>
              <th>No</th>
              <th>Score</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in evaluationCriteria" :key="c.key">
              <th>{{ c.name }}</th>
              <template v-for="m in modelKeys">
                <td>{{ percent(stats.model_avg[m][c.key], 'yes') }}</td>
                <td>{{ percent(stats.model_avg[m][c.key], 'maybe') }}</td>
                <td>{{ percent(stats.model_avg[m][c.key], 'no') }}</td>
                <td>{{ formatScore(stats.model_avg[m][c.key]) }}</td>
              </template>
              <td>{{ percent(stats.overall_avg[c.key], 'yes') }}</td>
              <td>{{ percent(stats.overall_avg[c.key], 'maybe') }}</td>
              <td>{{ percent(stats.overall_avg[c.key], 'no') }}</td>
              <td>{{ formatScore(stats.overall_avg[c.key]) }}</td>
            </tr>
            <tr>
              <th>Weighted Score</th>
              <template v-for="m in modelKeys">
                <td colspan="3"></td>
                <td>{{ formatScore(weightedScore(stats.model_avg[m])) }}</td>
              </template>
              <td colspan="3"></td>
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
          <span>{{ percent(stats.overall_avg[c.key], 'yes') }} / {{ percent(stats.overall_avg[c.key], 'maybe') }} / {{ percent(stats.overall_avg[c.key], 'no') }} ({{ formatScore(stats.overall_avg[c.key]) }})</span>
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
import { onMounted, ref, watch, computed } from 'vue'
import axios from 'axios'
import { evaluationCriteria } from '../utils/constants.js'

const props = defineProps({ projectId: Number, problems: Array })
const stats = ref(null)

const modelKeys = computed(() => {
  return stats.value && stats.value.model_avg ? Object.keys(stats.value.model_avg) : []
})

const userModelKeys = computed(() => {
  return stats.value && stats.value.user_model_avg ? Object.keys(stats.value.user_model_avg) : []
})

const fetchStats = async () => {
  if (!props.projectId) return
  const { data } = await axios.get(`/api/projects/${props.projectId}/stats`)
  stats.value = data
}

const percent = (obj, key) => {
  if (!obj || obj[key] === null || obj[key] === undefined) return 'N/A'
  return obj[key]
}

const formatScore = (obj) => {
  if (!obj || obj.score === null || obj.score === undefined) return 'N/A'
  return obj.score.toFixed(2)
}

const weightedScore = (group) => {
  if (!group) return null
  let sum = 0
  let total = 0
  evaluationCriteria.forEach(c => {
    const item = group[c.key]
    if (item && item.score !== null && item.score !== undefined) {
      sum += item.score * c.weight
      total += c.weight
    }
  })
  if (total === 0) return null
  return sum / total
}

const formatKappa = (val) => {
  if (val === null || val === undefined) return 'N/A'
  return val.toFixed(2)
}

onMounted(fetchStats)
watch(() => props.problems, fetchStats)
</script>
