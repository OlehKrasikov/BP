import { createRouter, createWebHistory } from 'vue-router'

import UploadView from '../views/UploadView.vue'
import SettingsView from '../views/SettingsView.vue'
import ResultView from '../views/ResultView.vue'

const routes = [
  { path: '/', component: UploadView },
  { path: '/settings', name: 'settings', component: SettingsView },
  { path: '/result', name: 'result', component: ResultView }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 