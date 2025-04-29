<template>
  <div>
    <RouterLink
      :to="`/projects/${question.project_id}`"
      class="text-decoration-none"
    >
      <i class="bi bi-arrow-left me-1"></i>Back to project
    </RouterLink>

    <h1 class="h4 my-3">Generated Design Problem #{{ question.id }}</h1>

    <!-- Generated Question -->
    <div class="mb-4">
      <h2 class="h6">Generated Design Problem</h2>
      <div v-html="renderedOutput" class="border rounded p-3 bg-light"></div>
    </div>

    <!-- Evaluation -->
    <div v-if="!isEvaluated" class="card p-3 mb-4">
      <h2 class="h6 mb-3">Evaluate this design problem</h2>
      <EvaluationForm :question="question" @submitted="fetchQuestion" />
    </div>

    <div v-else class="card p-3 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2 class="h6 mb-0">Evaluation</h2>
        <button
          class="btn btn-outline-secondary btn-sm"
          @click="editingEvaluation = true"
        >
          <i class="bi bi-pencil-square me-1"></i>Edit Evaluation
        </button>
      </div>

      <div v-if="editingEvaluation">
        <EvaluationForm
          :question="question"
          :initial-scores="{
            scenario: question.scenario,
            alignment: question.alignment,
            complexity: question.complexity,
            clarity: question.clarity,
            feasibility: question.feasibility
          }"
          @submitted="handleEvaluationUpdate"
        />
      </div>

      <div v-else class="row text-center">
        <div v-for="criteria in evaluationCriteria" :key="criteria.key" class="col-6 col-md-3 col-lg-2 mb-2">
          <div class="fw-bold fs-4">{{ question[criteria.key] }}</div>
          <small class="text-muted text-capitalize">{{ criteria.name }}</small>
        </div>
      </div>
    </div>

    <!-- Prompt -->
    <div class="mb-4">
      <h2 class="h6">Prompt</h2>
      <div
        class="border rounded p-3 bg-light"
        style="white-space: pre-wrap; overflow-wrap: break-word;"
      >
        {{ question.prompt }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import EvaluationForm from './EvaluationForm.vue'
import MarkdownIt from 'markdown-it'
import { evaluationCriteria } from '../utils/constants.js'

const md = new MarkdownIt()
const route = useRoute()
const question = ref({})
const renderedOutput = ref('')
const editingEvaluation = ref(false)


const isEvaluated = computed(() =>
  evaluationCriteria.every(
    criteria => question.value[criteria.key] !== null 
    && question.value[criteria.key] !== undefined
  )
)

const fetchQuestion = async () => {
  const { data } = await axios.get(`/api/questions/${route.params.id}`)
  question.value = data
  renderedOutput.value = md.render(question.value.generated_question || '')
  editingEvaluation.value = false // exit edit mode when refreshing
}

const handleEvaluationUpdate = () => {
  fetchQuestion()
  editingEvaluation.value = false
}

onMounted(fetchQuestion)
</script>
