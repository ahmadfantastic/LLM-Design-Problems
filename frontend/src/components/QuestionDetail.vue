<template>
  <div>
    <RouterLink
      :to="`/projects/${question.project_id}`"
      class="text-decoration-none"
    >
      <i class="bi bi-arrow-left me-1"></i>Back to project
    </RouterLink>

    <h1 class="h4 my-3">
      <i :class="typeIcon[question.type] || 'bi bi-question-circle'"></i>
      Generated Design Problem #{{ question.id }}
    </h1>

    <!-- Generated Question -->
    <div class="mb-4">
      <div v-html="renderedQuestion" class="border rounded p-3 bg-light"></div>
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
          class="btn btn-outline-primary btn-sm"
          @click="editingEvaluation = true"
        >
          <i class="bi bi-pencil-square me-1"></i>Edit Evaluation
        </button>
      </div>

      <div v-if="editingEvaluation">
        <EvaluationForm
          :question="question"
          :initial-evaluation="{
            scenario: question.scenario,
            alignment: question.alignment,
            complexity: question.complexity,
            clarity: question.clarity,
            feasibility: question.feasibility,
            evaluation_note: question.evaluation_note
          }"
          @submitted="handleEvaluationUpdate"
        />
      </div>

      <div v-else class="row">
        <div v-for="criteria in evaluationCriteria" :key="criteria.key" class="col-6 col-md-3 col-lg-2 mb-2">
          <div class="fw-bold fs-4" :title="criteria['score_'+question[criteria.key]]">{{ answerMap[question[criteria.key]] }}</div>
          <small class="text-muted text-capitalize">{{ criteria.name }}</small>
        </div>
        <div class="col-12 mt-3">
          <h6>Evaluation Notes</h6>
          <div
            class="border rounded p-3 bg-light"
            style="white-space: pre-wrap; overflow-wrap: break-word;"
          >
            {{ question.evaluation_note }}
          </div>
        </div>
      </div>
    </div>

    <!-- Generated Answer -->
    <div class="card p-3 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2 class="h6 mb-0">Generated Answer</h2>
        <button
          v-if="!question.sample_answer && !loadingAnswer"
          class="btn btn-outline-primary btn-sm"
          @click="generateAnswer"
        >
          <i class="bi bi-lightbulb me-1"></i>Generate Answer
        </button>
        <div v-if="loadingAnswer" class="spinner-border text-primary spinner-border-sm" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-if="question.sample_answer" class="border rounded p-3 bg-light" v-html="renderedAnswer"></div>
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
const renderedQuestion = ref('')
const renderedAnswer = ref('')

const editingEvaluation = ref(false)
const loadingAnswer = ref(false)


const isEvaluated = computed(() =>
  evaluationCriteria.every(
    criteria => question.value[criteria.key] !== null 
    && question.value[criteria.key] !== undefined
  )
)

const fetchQuestion = async () => {
  const { data } = await axios.get(`/api/questions/${route.params.id}`)
  question.value = data
  renderedQuestion.value = md.render(question.value.generated_question || '')
  renderedAnswer.value = md.render(question.value.sample_answer || '')
  editingEvaluation.value = false // exit edit mode when refreshing
}

const handleEvaluationUpdate = () => {
  fetchQuestion()
  editingEvaluation.value = false
}


const generateAnswer = async () => {
  loadingAnswer.value = true
  try {
    await axios.post(`/api/questions/${route.params.id}/answer`)
    await fetchQuestion()
  } finally {
    loadingAnswer.value = false
  }
}

const typeIcon = {
  open: 'bi bi-chat-text',
  multiple_choice: 'bi bi-list-ul',
  true_false: 'bi bi-check2-square',
}

const answerMap = ['No', 'Maybe', 'Yes', 'Definitely', 'Not sure']


onMounted(fetchQuestion)
</script>
