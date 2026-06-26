import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/home/Index.vue'),
    meta: { title: '音乐标签Web版' }
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('@/views/user/Index.vue'),
    meta: { title: '用户信息' }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/user/Login.vue'),
    meta: { title: '登录' }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
