<template>
  <form @submit.prevent="submit" class="d-flex gap-2 align-items-end mb-3 align-items-center">
    <textarea
      v-model="target"
      placeholder="Target objectives"
      class="form-control">
    </textarea>

     <!-- Wrap dropdown and count input together -->
     <div class="d-flex flex-column">
      <select v-model="type" class="form-select" required style="width: 120px">
        <option disabled value="">Type</option>
        <option value="open">Open</option>
        <option value="multiple_choice">Multi Choice</option>
        <option value="true_false">True/False</option>
      </select>

      <input
        v-model="count"
        type="number"
        max="10"
        min="1"
        placeholder="Count"
        class="form-control"
        style="width: 120px"
        required/>
    </div>

    <select v-model="model" class="form-select" required style="width: 120px">
      <option disabled value="">Model</option>
      <option value="gpt-4o">GPT-4o</option>
      <option value="gpt-3.5-turbo">gpt-3.5-turbo</option>
      <option value="o1">o1</option>
      <option value="o3">o3</option>
      <option value="o3-mini">o3-mini</option>
      <option value="gemini-2.5-flash">Gemini Flash</option>
      <option value="gemini-2.5-pro">Gemini Pro</option>
    </select>

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
const type = ref('open')
const count = ref(1)
const model = ref('gpt-4o')

const loading = ref(false)

const submit = async () => {
  loading.value = true
  try {
    await axios.post(
      `/api/projects/${props.project.id}/problems`,
      { 
        target_objectives: target.value,
        type: type.value,
        count: count.value,
        model: model.value
      }
    )
    emit('created')
  } finally {
    loading.value = false
  }
}
</script>
