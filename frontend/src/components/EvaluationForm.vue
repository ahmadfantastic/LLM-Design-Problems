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
        v-model="evaluation_data[criteria.key]"
        class="form-select"
        required
      >
        <option disabled value="">—</option>
        <option :key="2" :value="2" :title="criteria['score_2']">Yes</option>
        <option :key="1" :value="1" :title="criteria['score_1']">May be</option>
        <option :key="0" :value="0" :title="criteria['score_0']">No</option>
      </select>
    </div>
    <div class="col-12">
      <label for="evaluation_note" class="form-label">Evaluation Notes</label>
      <textarea
        id="evaluation_note"
        v-model="evaluation_data.evaluation_note"
        class="form-control"
        rows="3"
        placeholder="Add your evaluation notes here..."
      ></textarea>
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
  initialEvaluation: {
    type: Object,
    default: () => ({
      scenario: '',
      alignment: '',
      complexity: '',
      clarity: '',
      feasibility: '',
      evaluation_note: ''
    })
  }
})

const emit = defineEmits(['submitted'])


const evaluation_data = reactive({ ...props.initialEvaluation})

watchEffect(() => {
  if (props.initialEvaluation) {
    evaluationCriteria.forEach(criteria => {
      evaluation_data[criteria.key] = props.initialEvaluation[criteria.key] ?? ''
    })
    evaluation_data['evaluation_note'] = props.initialEvaluation['evaluation_note'] ?? ''
  }
})

const submit = async () => {
  await axios.post(`/api/questions/${props.question.id}/evaluate`, evaluation_data)
  emit('submitted')
}
</script>
