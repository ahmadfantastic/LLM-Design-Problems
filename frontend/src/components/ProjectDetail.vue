<template>
  <div>
    <div class="mb-3">
      <RouterLink :to="`/`" class="text-decoration-none">
        <i class="bi bi-arrow-left me-1"></i>Back to projects
      </RouterLink>
    </div>

    <div class="d-flex justify-content-between align-items-center">
      <h1 class="h3 mb-3">{{ project.name }}</h1>
      <button class="btn btn-outline-primary btn-sm" @click="editing = !editing">
        <i class="bi bi-pencil-square me-1"></i>Edit
      </button>
    </div>

    <div v-if="editing" class="card card-body mb-4">
      <form @submit.prevent="saveEdit" class="row g-3">
        <div class="col-12 col-md-6">
          <input v-model="editForm.name" class="form-control" placeholder="Project name" required />
        </div>
        <div class="col-12">
          <textarea v-model="editForm.learning_objectives" class="form-control" rows="3" placeholder="Learning objectives" required />
        </div>
        <div class="col-12">
          <textarea v-model="editForm.task_description" class="form-control" rows="3" placeholder="Task description" required />
        </div>
        
        <div class="col-12">
          <textarea v-model="editForm.technologies" class="form-control" rows="3" placeholder="Technologies" required />
        </div>
        <div class="col-12">
          <button class="btn btn-success me-2">
            <i class="bi bi-save me-1"></i>Save
          </button>
          <button class="btn btn-secondary" @click.prevent="editing = false">
            Cancel
          </button>
        </div>
      </form>
    </div>

    <template v-else>
      <div class="mb-4">
        <h5 class="text-primary">Learning Objectives</h5>
        <div class="border rounded p-3 bg-light" style="white-space: pre-wrap; overflow-wrap: break-word;">
          {{ project.learning_objectives }}
        </div>
      </div>

      <div class="mb-4">
        <h5 class="text-primary">Task Description</h5>
        <div class="border rounded p-3 bg-light" style="white-space: pre-wrap; overflow-wrap: break-word;">
          {{ project.task_description }}
        </div>
      </div>

      <div class="mb-4">
        <h5 class="text-primary">Project Technologies</h5>
        <div class="border rounded p-3 bg-light" style="white-space: pre-wrap; overflow-wrap: break-word;">
          {{ project.technologies }}
        </div>
      </div>
    </template>

    <!-- Create Question -->
    <h2 class="h5 mt-4">Generate Question</h2>
    <QuestionForm :project="project" @created="fetchProject" />

    <!-- Question list -->
    <h2 class="h5 mt-4">Questions</h2>
    <ul class="list-group mb-4">
      <li
        v-for="q in project.questions"
        :key="q.id"
        class="list-group-item d-flex justify-content-between align-items-center"
      >
        <div>
          <RouterLink
            :to="`/questions/${q.id}`"
            class="text-decoration-none me-2"
          >
            Question #{{ q.id }}
          </RouterLink>

          <span
            class="badge"
            :class="isEvaluated(q) ? 'bg-success' : 'bg-warning text-dark'"
          >
            {{ isEvaluated(q) ? 'Evaluated' : 'Pending Evaluation' }}
          </span>
        </div>

        <div class="d-flex align-items-center gap-2">
          <small class="text-muted">
            {{ new Date(q.created_at).toLocaleString() }}
          </small>

          <!-- NEW: Delete button -->
          <button
            class="btn btn-sm btn-outline-danger"
            @click="confirmDelete(q.id)"
          >
            <i class="bi bi-trash"></i>
          </button>
        </div>
      </li>
    </ul>

    <!-- Stats panel -->
    <StatsPanel :questions="project.questions" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import QuestionForm from './QuestionForm.vue'
import StatsPanel from './StatsPanel.vue'

const route = useRoute()
const project = ref({ questions: [] })
const editing = ref(false)
const editForm = ref({
  name: '',
  learning_objectives: '',
  task_description: ''
})

const fetchProject = async () => {
  const { data } = await axios.get(`/api/projects/${route.params.id}`)
  project.value = data
  editForm.value.name = data.name
  editForm.value.learning_objectives = data.learning_objectives
  editForm.value.task_description = data.task_description
  editForm.value.technologies = data.technologies
}

const saveEdit = async () => {
  await axios.patch(`/api/projects/${project.value.id}`, editForm.value)
  editing.value = false
  fetchProject()
}

const confirmDelete = async (qid) => {
  if (confirm('Are you sure you want to delete this question?')) {
    await axios.delete(`/api/questions/${qid}`)
    await fetchProject()
  }
}

const isEvaluated = (q) => {
  return q.alignment != null && q.complexity != null && q.clarity != null && q.feasibility != null
}

onMounted(fetchProject)
</script>
