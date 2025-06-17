<template>
  <div class="row justify-content-center">
    <div class="col-md-4">
      <form @submit.prevent="submit">
        <h1 class="h5 mb-3">Register User</h1>
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input v-model="username" class="form-control" required />
        </div>
        <div class="form-check mb-3">
          <input class="form-check-input" type="checkbox" id="admin" v-model="isAdmin" />
          <label class="form-check-label" for="admin">Admin</label>
        </div>
        <button class="btn btn-primary">Create</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()
const username = ref('')
const isAdmin = ref(false)

const submit = async () => {
  await axios.post('/api/register', { username: username.value, is_admin: isAdmin.value })
  router.push('/')
}
</script>
