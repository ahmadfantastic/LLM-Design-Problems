<template>
  <div class="row">
    <div class="col-md-5">
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
          <div
            class="border rounded p-3 bg-light position-relative"
            :class="{ 'collapsed-text': !showFullObjectives }"
            style="white-space: pre-wrap; overflow-wrap: break-word;"
          >
            {{ project.learning_objectives }}
          </div>
          <button class="btn btn-link px-0" @click="showFullObjectives = !showFullObjectives">
            {{ showFullObjectives ? 'Show less' : 'Show more' }}
          </button>
        </div>

        <div class="mb-4">
          <h5 class="text-primary">Task Description</h5>
          <div
            class="border rounded p-3 bg-light position-relative"
            :class="{ 'collapsed-text': !showFullTask }"
            style="white-space: pre-wrap; overflow-wrap: break-word;"
          >
            {{ project.task_description }}
          </div>
          <button class="btn btn-link px-0" @click="showFullTask = !showFullTask">
            {{ showFullTask ? 'Show less' : 'Show more' }}
          </button>
        </div>

        <div class="mb-4">
          <h5 class="text-primary">Project Technologies</h5>
          <div class="border rounded p-3 bg-light" style="white-space: pre-wrap; overflow-wrap: break-word;">
            {{ project.technologies }}
          </div>
        </div>
      </template>
      
      <!-- Stats panel -->
      <StatsPanel :project-id="project.id" :problems="project.problems" />
    </div>

    <div class="col-md-7">
      <!-- Create Problem -->
      <h2 class="h5 mt-4">Generate Design Problem</h2>
      <ProblemForm :project="project" @created="fetchProject" />

      <!-- Problem list -->
      <div class="d-flex justify-content-between align-items-center mt-4">
        <h2 class="h5 mb-0">Design Problems</h2>
        <button class="btn btn-outline-secondary btn-sm" @click="exportCsv">
          <i class="bi bi-download me-1"></i> Export CSV
        </button>
      </div>
      <div v-if="project.problems.length === 0" class="text-muted fst-italic mb-3">
        No design problems generated yet.
      </div>
      <ProblemList
        v-else
        :problems="project.problems"
        @deleted="fetchProject"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'
import ProblemForm from './ProblemForm.vue'
import StatsPanel from './StatsPanel.vue'
import ProblemList from './ProblemList.vue'

const route = useRoute()
const showFullObjectives = ref(false)
const showFullTask = ref(false)
const project = ref({ problems: [] })
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

const exportCsv = async () => {
  const { data } = await axios.get(
    `/api/projects/${project.value.id}/problems.csv`,
    { responseType: 'blob' }
  )
  const url = window.URL.createObjectURL(new Blob([data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', `project_${project.value.id}_problems.csv`)
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

onMounted(fetchProject)
</script>

<style scoped>
.collapsed-text {
  max-height: 5rem;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
