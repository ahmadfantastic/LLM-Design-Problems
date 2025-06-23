<template>
  <div v-if="stats" class="card shadow-sm p-4 mb-4">
    <h3 class="h6 mb-3">My Evaluation</h3>
    <ul class="list-group mb-3">
      <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ c.name }}</span>
        <span>{{ stats.user_avg[c.key] !== null && stats.user_avg[c.key] !== undefined ? stats.user_avg[c.key] : 'N/A' }}</span>
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
                {{ stats.model_avg[m][c.key] !== null && stats.model_avg[m][c.key] !== undefined ? stats.model_avg[m][c.key] : 'N/A' }}
              </td>
              <td>{{ stats.overall_avg && stats.overall_avg[c.key] !== undefined && stats.overall_avg[c.key] !== null ? stats.overall_avg[c.key] : 'N/A' }}</td>
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
          <span>{{ stats.overall_avg[c.key] !== null && stats.overall_avg[c.key] !== undefined ? stats.overall_avg[c.key]: 'N/A' }}</span>
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

const fetchStats = async () => {
  if (!props.projectId) return
  const { data } = await axios.get(`/api/projects/${props.projectId}/stats`)
  stats.value = data
}

onMounted(fetchStats)
watch(() => props.problems, fetchStats)
</script>

