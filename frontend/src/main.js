import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { fetchCurrentUser } from './utils/auth.js'

// Classic styling
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'

fetchCurrentUser()
createApp(App).use(router).mount('#app')
