<template>
  <div>
    <RouterLink
      :to="`/projects/${problem.project_id}`"
      class="text-decoration-none"
    >
      <i class="bi bi-arrow-left me-1"></i>Back to project
    </RouterLink>

    <h1 class="h4 my-3">
      <i :class="typeIcon[problem.type] || 'bi bi-question-circle'"></i>
      Generated Design Problem #{{ problem.id }}
    </h1>

    <!-- Navigation between problems -->
    <div class="d-flex justify-content-between mb-3">
      <RouterLink
        v-if="prevId"
        :to="`/problems/${prevId}`"
        class="btn btn-outline-secondary btn-sm"
      >
        <i class="bi bi-chevron-left me-1"></i>Previous
      </RouterLink>
      <RouterLink
        v-if="nextId"
        :to="`/problems/${nextId}`"
        class="btn btn-outline-secondary btn-sm ms-auto"
      >
        Next<i class="bi bi-chevron-right ms-1"></i>
      </RouterLink>
    </div>

    <!-- Generated Problem -->
    <div class="mb-4">
      <div v-html="renderedProblem" class="border rounded p-3 bg-light"></div>
    </div>
    
    <div class="mb-4">
      
    </div>

    <!-- Target Objectives -->
    <h2 class="h6 mb-3">Target Learning Objective</h2>
    <div class="border rounded p-3 bg-light mb-3">{{ problem.target_objectives }}</div>
    

    <!-- Evaluation -->
    <div v-if="!isEvaluated" class="card p-3 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2 class="h6 mb-0">Evaluate this design problem</h2>
        <button
          v-if="!loadingAutoEval"
          class="btn btn-outline-secondary btn-sm"
          @click="autoEvaluate"
        >
          <i class="bi bi-robot me-1"></i>Evaluate with LLM
        </button>
        <div v-if="loadingAutoEval" class="spinner-border spinner-border-sm text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>
      <EvaluationForm :problem="problem" @submitted="fetchProblem" />
    </div>

    <div v-else class="card p-3 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2 class="h6 mb-0">Evaluation</h2>
        <div class="d-flex gap-2">
          <button
            v-if="!loadingAutoEval"
            class="btn btn-outline-secondary btn-sm"
            @click="autoEvaluate"
          >
            <i class="bi bi-robot me-1"></i>Evaluate with LLM
          </button>
          <div v-if="loadingAutoEval" class="spinner-border spinner-border-sm text-primary" role="status">
            <span class="visually-hidden">Loading...</span>
          </div>
          <button
            class="btn btn-outline-primary btn-sm"
            @click="editingEvaluation = true"
          >
            <i class="bi bi-pencil-square me-1"></i>Edit Evaluation
          </button>
        </div>
      </div>

      <div v-if="editingEvaluation">
        <EvaluationForm
          :problem="problem"
          :initial-evaluation="{
            scenario: problem.scenario,
            alignment: problem.alignment,
            complexity: problem.complexity,
            clarity: problem.clarity,
            feasibility: problem.feasibility,
            evaluation_note: problem.evaluation_note
          }"
          @submitted="handleEvaluationUpdate"
        />
      </div>

      <div v-else class="row">
        <div v-for="criteria in evaluationCriteria" :key="criteria.key" class="col-6 col-md-3 col-lg-2 mb-2">
          <div class="fw-bold fs-4" :title="criteria['score_'+problem[criteria.key]]">{{ answerMap[problem[criteria.key]] }}</div>
          <small class="text-muted text-capitalize">{{ criteria.name }}</small>
        </div>
        <div class="col-12 mt-3">
          <h6>Evaluation Notes</h6>
          <div
            class="border rounded p-3 bg-light"
            style="white-space: pre-wrap; overflow-wrap: break-word;"
          >
            {{ problem.evaluation_note }}
          </div>
        </div>
      </div>
    </div>

    <!-- Generated Answer -->
    <div class="card p-3 mb-4">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h2 class="h6 mb-0">Generated Answer</h2>
        <button
          v-if="!loadingAnswer"
          class="btn btn-outline-primary btn-sm"
          @click="generateAnswer"
        >
          <i class="bi bi-lightbulb me-1"></i>
          {{ problem.sample_answer ? 'Regenerate Answer' : 'Generate Answer' }}
        </button>
        <div v-if="loadingAnswer" class="spinner-border text-primary spinner-border-sm" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
      </div>

      <div v-if="problem.sample_answer" class="border rounded p-3 bg-light" v-html="renderedAnswer"></div>
    </div>

    <!-- Prompt -->
    <div class="mb-4">
      <h2 class="h6">Prompt</h2>
      <div
        class="border rounded p-3 bg-light"
        style="white-space: pre-wrap; overflow-wrap: break-word;"
      >
        {{ problem.prompt }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import EvaluationForm from './EvaluationForm.vue'
import MarkdownIt from 'markdown-it'
import { evaluationCriteria } from '../utils/constants.js'

const md = new MarkdownIt()
const route = useRoute()
const problem = ref({})
const renderedProblem = ref('')
const renderedAnswer = ref('')

const editingEvaluation = ref(false)
const loadingAnswer = ref(false)
const loadingAutoEval = ref(false)

const projectProblems = ref([])


const isEvaluated = computed(() =>
  evaluationCriteria.every(
    criteria => problem.value[criteria.key] !== null 
    && problem.value[criteria.key] !== undefined
  )
)

const fetchProblem = async () => {
  const { data } = await axios.get(`/api/problems/${route.params.id}`)
  problem.value = data
  renderedProblem.value = md.render(problem.value.generated_problem || '')
  renderedAnswer.value = md.render(problem.value.sample_answer || '')
  editingEvaluation.value = false // exit edit mode when refreshing
  await fetchProjectProblems()
}

const handleEvaluationUpdate = () => {
  fetchProblem()
  editingEvaluation.value = false
}


const fetchProjectProblems = async () => {
  if (!problem.value.project_id) return
  const { data } = await axios.get(`/api/projects/${problem.value.project_id}`)
  projectProblems.value = [...data.problems].sort((a, b) => a.id - b.id)
}

const prevId = computed(() => {
  const idx = projectProblems.value.findIndex(p => p.id === problem.value.id)
  return idx > 0 ? projectProblems.value[idx - 1].id : null
})

const nextId = computed(() => {
  const idx = projectProblems.value.findIndex(p => p.id === problem.value.id)
  return idx >= 0 && idx < projectProblems.value.length - 1
    ? projectProblems.value[idx + 1].id
    : null
})


const generateAnswer = async () => {
  loadingAnswer.value = true
  try {
    await axios.post(`/api/problems/${route.params.id}/answer`)
    await fetchProblem()
  } finally {
    loadingAnswer.value = false
  }
}

const autoEvaluate = async () => {
  loadingAutoEval.value = true
  try {
    await axios.post(`/api/problems/${route.params.id}/auto_evaluate`)
    await fetchProblem()
  } finally {
    loadingAutoEval.value = false
  }
}

const typeIcon = {
  open: 'bi bi-chat-text',
  multiple_choice: 'bi bi-list-ul',
  true_false: 'bi bi-check2-square',
}

const answerMap = ['No', 'Maybe', 'Yes']

onMounted(fetchProblem)
watch(() => route.params.id, fetchProblem)
</script>
