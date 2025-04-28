<template>
  <form class="row g-3 my-4" @submit.prevent="submit">
    <div
      v-for="criteria in evaluationCriteria"
      :key="criteria.key"
      class="col-6 col-md-3 col-lg-2"
    >
      <label :for="criteria.key" class="form-label text-capitalize">
        {{ criteria.name }}
      </label>
      <select
        :id="criteria.key"
        v-model="scores[criteria.key]"
        class="form-select"
        required
      >
        <option disabled value="">—</option>
        <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
      </select>
    </div>
    <div class="col-12">
      <button class="btn btn-primary">
        <i class="bi bi-save me-1"></i>Save Evaluation
      </button>
    </div>
  </form>
</template>

<script setup>
import { reactive, watchEffect } from 'vue'
import axios from 'axios'
import { evaluationCriteria } from '../utils/constants.js'

const props = defineProps({
  question: Object,
  initialScores: {
    type: Object,
    default: () => ({
      scenario: '',
      alignment: '',
      complexity: '',
      clarity: '',
      feasibility: ''
    })
  }
})

const emit = defineEmits(['submitted'])


const scores = reactive({ ...props.initialScores })

watchEffect(() => {
  if (props.initialScores) {
    evaluationCriteria.forEach(criteria => {
      scores[criteria.key] = props.initialScores[criteria.key] ?? ''
    })
  }
})

const submit = async () => {
  await axios.post(`/api/questions/${props.question.id}/evaluate`, scores)
  emit('submitted')
}
</script>
