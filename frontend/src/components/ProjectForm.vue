<template>
  <form @submit.prevent="submit" class="mb-6 grid gap-4 lg:grid-cols-3">
    <input v-model="name" placeholder="Project name" class="input" required />
    <textarea v-model="objectives" placeholder="Learning objectives (one per line)" class="textarea" required></textarea>
    <textarea v-model="task" placeholder="Task description" class="textarea" required></textarea>
    <button class="btn col-span-full w-max">Create</button>
  </form>
</template>
<script setup>
import { ref } from 'vue'
import axios from 'axios'
const emit = defineEmits(['created'])
const name = ref(''), objectives = ref(''), task = ref('')
const submit = async () => {
  await axios.post('/api/projects', {
    name: name.value,
    learning_objectives: objectives.value,
    task_description: task.value
  })
  name.value = objectives.value = task.value = ''
  emit('created')
}
</script>