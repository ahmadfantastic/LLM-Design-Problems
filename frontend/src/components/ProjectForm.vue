<template>
  <form @submit.prevent="submit" class="row g-4">
    <div class="col-12">
      <input v-model="name" class="form-control" placeholder="Project name" required />
    </div>

    <div class="col-12">
      <textarea v-model="objectives" class="form-control" rows="3" placeholder="Learning objectives" required></textarea>
    </div>

    <div class="col-12">
      <textarea v-model="task" class="form-control" rows="3" placeholder="Task description" required></textarea>
    </div>

    <div class="col-12">
      <input v-model="technologies" class="form-control" placeholder="Key technologies" required />
    </div>

    <div class="col-12 text-end">
      <button class="btn btn-success">
        <i class="bi bi-plus-circle me-1"></i>Create Project
      </button>
    </div>
  </form>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const emit = defineEmits(['created'])

const name = ref('')
const objectives = ref('')
const task = ref('')
const technologies = ref('')

const submit = async () => {
  await axios.post('/api/projects', {
    name: name.value,
    learning_objectives: objectives.value,
    task_description: task.value,
    technologies: technologies.value
  })
  name.value = objectives.value = task.value = technologies.value = ''
  emit('created')
}
</script>
