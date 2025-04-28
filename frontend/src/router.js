import { createRouter, createWebHistory } from 'vue-router'
import ProjectList from './components/ProjectList.vue'
import ProjectDetail from './components/ProjectDetail.vue'
import QuestionDetail from './components/QuestionDetail.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: ProjectList },
    { path: '/projects/:id', component: ProjectDetail, props: true },
    { path: '/questions/:id', component: QuestionDetail, props: true },
  ]
})