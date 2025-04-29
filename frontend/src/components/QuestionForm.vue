<template>
  <form @submit.prevent="submit" class="d-flex gap-2 align-items-end mb-3">
    <textarea
      v-model="target"
      placeholder="Target objectives (comma separated)"
      class="form-control"></textarea>
    <input
      v-model="count"
      type="number"
      max="50"
      min="1"
      default="1"
      placeholder="Count"
      class="form-control"
      style="width: 100px"/>
    <!-- <button class="btn btn-success">
      <i class="bi bi-lightning-charge-fill me-1"></i>Generate
    </button> -->
    <button class="btn btn-success" :disabled="loading">
      <span v-if="loading" class="spinner-border spinner-border-sm me-1" role="status" aria-hidden="true"></span>
      <i v-else class="bi bi-lightning-charge-fill me-1"></i>
      {{ loading ? 'Generating...' : 'Generate' }}
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({ project: Object })
const emit = defineEmits(['created'])
const target = ref('')
const count = ref('')

const loading = ref(false)

const submit = async () => {
  loading.value = true
  try {
    await axios.post(
      `/api/projects/${props.project.id}/questions`,
      { 
        selected_objectives: target.value,
        count: count.value
      }
    )
    emit('created')
  } finally {
    loading.value = false
  }
}
</script>
