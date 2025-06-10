<template>
  <div class="row justify-content-center">
    <div class="col-md-4">
      <form @submit.prevent="submit">
        <h1 class="h5 mb-3">Login</h1>
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input v-model="username" class="form-control" required />
        </div>
        <div class="mb-3">
          <label class="form-label">Password</label>
          <input v-model="password" type="password" class="form-control" required />
        </div>
        <button class="btn btn-primary">Login</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../utils/auth.js'

const router = useRouter()
const username = ref('')
const password = ref('')

const submit = async () => {
  try {
    await login(username.value, password.value)
    router.push('/')
  } catch (e) {
    alert('Login failed')
  }
}
</script>
