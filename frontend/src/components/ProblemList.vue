<template>
  <ul class="list-group mb-4">
    <li
      v-for="(q, idx) in problems"
      :key="q.id"
      class="list-group-item"
    >
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <i :class="typeIcon[q.type] || 'bi bi-question-circle'"></i>
          <RouterLink
            :to="`/problems/${q.id}`"
            class="text-decoration-none me-2">
            Design Problem #{{ idx + 1 }}
          </RouterLink>

          <span
            class="badge"
            :class="isEvaluated(q) ? 'bg-success' : 'bg-warning text-dark'">
            {{ isEvaluated(q) ? 'Evaluated' : 'Pending Evaluation' }}
          </span>
          <span
            class="badge ms-2"
            :class="modelBadgeClass(q.model)">
            {{ q.model }}
          </span>
        </div>

        <div class="d-flex align-items-center gap-2">
          <small class="text-muted">
            {{ new Date(q.created_at).toLocaleString() }}
          </small>

          <button
            class="btn btn-sm btn-outline-secondary"
            @click="toggleExpand(q.id)"
          >
            <i
              :class="expandedIds.includes(q.id)
                ? 'bi bi-chevron-up'
                : 'bi bi-chevron-down'"
            ></i>
          </button>

          <button
            class="btn btn-sm btn-outline-danger"
            @click="confirmDelete(q.id)"
          >
            <i class="bi bi-trash"></i>
          </button>
        </div>
      </div>

      <!-- Expanded problem display -->
      <div v-if="expandedIds.includes(q.id)" class="mt-2">
        <div class="mb-0" v-html="renderMarkdown(q.generated_problem)"></div>
      </div>
    </li>
  </ul>
</template>


<script setup>
import { ref } from 'vue'
import axios from 'axios'
import MarkdownIt from 'markdown-it'

const props = defineProps({ problems: Array })
const emit = defineEmits(['deleted'])
const md = new MarkdownIt()

const expandedIds = ref([])

const toggleExpand = (id) => {
  if (expandedIds.value.includes(id)) {
    expandedIds.value = expandedIds.value.filter(qid => qid !== id)
  } else {
    expandedIds.value.push(id)
  }
}

// Markdown rendering
const renderMarkdown = (text) => md.render(text || '')

const confirmDelete = async (qid) => {
  if (confirm('Are you sure you want to delete this problem?')) {
    await axios.delete(`/api/problems/${qid}`)
    emit('deleted')
  }
}

const isEvaluated = (q) => {
  return q.alignment != null && q.complexity != null && q.clarity != null && q.feasibility != null
}

const typeIcon = {
  open: 'bi bi-chat-text',
  multiple_choice: 'bi bi-list-ul',
  true_false: 'bi bi-check2-square',
}

const modelBadgeClass = (model) => {
  if (!model) return 'bg-info text-dark'
  const m = model.toLowerCase()
  if (m.includes('gemini')) return 'gemini-badge'
  if (m.includes('gpt') || m.startsWith('o1') || m.startsWith('o3')) return 'openai-badge'
  return 'bg-info text-dark'
}
</script>

<style scoped>
.openai-badge {
  background-color: #10a37f;
  color: white;
}
.gemini-badge {
  background-color: #4285F4;
  color: white;
}
</style>
