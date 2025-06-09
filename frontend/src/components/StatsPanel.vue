<template>
  <div v-if="stats" class="card shadow-sm p-4 mb-4">
    <h3 class="h6 mb-3">Project Statistics</h3>
    <ul class="list-group mb-3">
      <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
        <span>{{ c.name }}</span>
        <span>{{ stats.user_avg[c.key] !== null && stats.user_avg[c.key] !== undefined ? stats.user_avg[c.key].toFixed(2) : 'N/A' }}</span>
      </li>
    </ul>
    <div v-if="stats.overall_avg">
      <h6>Overall Averages</h6>
      <ul class="list-group mb-3">
        <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
          <span>{{ c.name }}</span>
          <span>{{ stats.overall_avg[c.key] !== null && stats.overall_avg[c.key] !== undefined ? stats.overall_avg[c.key].toFixed(2) : 'N/A' }}</span>
        </li>
      </ul>
      <h6>Interrater Agreement (Kappa)</h6>
      <ul class="list-group">
        <li v-for="c in evaluationCriteria" :key="c.key" class="list-group-item d-flex justify-content-between align-items-center">
          <span>{{ c.name }}</span>
          <span>{{ stats.kappa[c.key] !== null && stats.kappa[c.key] !== undefined ? stats.kappa[c.key].toFixed(2) : 'N/A' }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue'
import axios from 'axios'
import { evaluationCriteria } from '../utils/constants.js'

const props = defineProps({ projectId: Number, problems: Array })
const stats = ref(null)

const fetchStats = async () => {
  if (!props.projectId) return
  const { data } = await axios.get(`/api/projects/${props.projectId}/stats`)
  stats.value = data
}

onMounted(fetchStats)
watch(() => props.problems, fetchStats)
</script>

