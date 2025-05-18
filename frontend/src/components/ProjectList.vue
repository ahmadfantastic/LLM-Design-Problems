<template>
  <div class="container py-4">
    <div class="row g-4">
      
      <!-- LEFT COLUMN: Project Form -->
      <div class="col-12 col-md-5">
        <div class="card shadow-sm">
          <div class="card-header bg-primary text-white">
            <h5 class="mb-0">Create New Project</h5>
          </div>
          <div class="card-body">
            <ProjectForm @created="fetchProjects" />
          </div>
        </div>
      </div>

      <!-- RIGHT COLUMN: Project List -->
      <div class="col-12 col-md-7">
        <h2 class="h5 mb-3">Existing Projects</h2>

        <div v-if="projects.length === 0" class="text-center py-5">
          <p class="h5 mb-4">No projects created yet.</p>
          <p class="text-muted">Start by creating your first project!</p>
        </div>

        <div v-else class="row row-cols-1 row-cols-md-2 g-4">
          <div v-for="p in projects" :key="p.id" class="col">
            <div class="card h-100 shadow-sm">
              <div class="card-body">
                <RouterLink :to="`/projects/${p.id}`" class="h5 card-title text-decoration-none">
                  {{ p.name }}
                </RouterLink>
                <p class="card-text small text-muted">
                  Created {{ new Date(p.created_at).toLocaleDateString() }}
                </p>
                <p class="card-text small">
                  <i class="bi bi-question-circle me-1"></i>
                  {{ p.question_count }} question{{ p.question_count !== 1 ? 's' : '' }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import ProjectForm from './ProjectForm.vue'

const projects = ref([])
const fetchProjects = async () => {
  const { data } = await axios.get('/api/projects')
  projects.value = data
}
onMounted(fetchProjects)
</script>
