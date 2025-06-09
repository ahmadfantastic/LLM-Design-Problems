<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary mb-4">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">LLM Exam Design Problem App</a>
      <ul class="navbar-nav ms-auto" v-if="user">
        <li class="nav-item" v-if="user.is_admin">
          <RouterLink class="nav-link" to="/register">Add User</RouterLink>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="#" @click.prevent="doLogout">Logout ({{ user.username }})</a>
        </li>
      </ul>
      <ul class="navbar-nav ms-auto" v-else>
        <li class="nav-item">
          <RouterLink class="nav-link" to="/login">Login</RouterLink>
        </li>
      </ul>
    </div>
  </nav>

  <div class="container py-4">
    <RouterView />
  </div>
</template>

<script setup>
import { currentUser, logout } from './utils/auth.js'
import { computed } from 'vue'

const user = computed(() => currentUser.value)
const doLogout = async () => {
  await logout()
}
</script>

<style lang="css">
p {
  white-space: pre-line;
}
</style>

