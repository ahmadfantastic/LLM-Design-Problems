import { createRouter, createWebHistory } from 'vue-router'
import ProjectList from './components/ProjectList.vue'
import ProjectDetail from './components/ProjectDetail.vue'
import ProblemDetail from './components/ProblemDetail.vue'
import LoginView from './components/LoginView.vue'
import RegisterUser from './components/RegisterUser.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: ProjectList },
    { path: '/login', component: LoginView },
    { path: '/register', component: RegisterUser },
    { path: '/projects/:id', component: ProjectDetail, props: true },
    { path: '/problems/:id', component: ProblemDetail, props: true },
  ]
})

