import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/home/Index.vue'),
    meta: { title: '音乐标签Web版' }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
