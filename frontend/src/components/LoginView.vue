<template>
  <div class="row justify-content-center">
    <div class="col-md-4">
      <form @submit.prevent="submit">
        <h1 class="h5 mb-3">Login</h1>
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input v-model="username" class="form-control" required />
        </div>
        <div class="mb-3" v-if="showPassword || settingPassword">
          <label class="form-label">Password</label>
          <input
            v-model="password"
            type="password"
            class="form-control"
            required
          />
        </div>
        <div class="mb-3" v-if="settingPassword">
          <label class="form-label">Confirm Password</label>
          <input
            v-model="confirmPassword"
            type="password"
            class="form-control"
            required
          />
        </div>
        <button class="btn btn-primary">
          {{ settingPassword ? 'Set Password' : 'Login' }}
        </button>
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
const confirmPassword = ref('')
const showPassword = ref(false)
const settingPassword = ref(false)

const submit = async () => {
  if (settingPassword.value && password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return
  }

  try {
    await login(
      username.value,
      showPassword.value || settingPassword.value ? password.value : undefined
    )
    router.push('/')
  } catch (e) {
    if (e.response && e.response.data && e.response.data.set_password_required) {
      settingPassword.value = true
      showPassword.value = true
    } else if (!showPassword.value) {
      showPassword.value = true
    } else {
      alert('Login failed')
    }
  }
}
</script>
