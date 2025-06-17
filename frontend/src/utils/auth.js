import { ref } from 'vue'
import axios from 'axios'

export const currentUser = ref(null)

export async function fetchCurrentUser() {
  const { data } = await axios.get('/api/current_user')
  currentUser.value = data
}

export async function login(username, password) {
  const res = await axios.post('/api/login', { username, password })
  await fetchCurrentUser()
  return res
}

export async function logout() {
  await axios.post('/api/logout')
  currentUser.value = null
}
