<template>
  <form @submit.prevent="submit" class="d-flex gap-2 align-items-end mb-3">
    <textarea
      v-model="subset"
      placeholder="Target objectives (comma separated)"
      class="form-control"
    ></textarea>
    <button class="btn btn-success">
      <i class="bi bi-lightning-charge-fill me-1"></i>Generate
    </button>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const props = defineProps({ project: Object })
const emit = defineEmits(['created'])
const subset = ref('')

const submit = async () => {
  await axios.post(
    `/api/projects/${props.project.id}/questions`,
    { selected_objectives: subset.value }
  )
  subset.value = ''
  emit('created')
}
</script>
