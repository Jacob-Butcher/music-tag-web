import { createRouter, createWebHashHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/home/Index.vue'),
    meta: { title: '音乐标签Web版', requiresAuth: true }
  },
  {
    path: '/user',
    name: 'user',
    component: () => import('@/views/user/Index.vue'),
    meta: { title: '用户信息', requiresAuth: true }
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/user/Login.vue'),
    meta: { title: '登录', requiresAuth: false }
  }
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

function getAuthCookie() {
  const name = 'AUTHORIZATION'
  if (!document.cookie) return null
  const cookies = document.cookie.split(';')
  for (let i = 0; i < cookies.length; i++) {
    const cookie = cookies[i].trim()
    if (cookie.substring(0, name.length + 1) === (name + '=')) {
      return decodeURIComponent(cookie.substring(name.length + 1))
    }
  }
  return null
}

router.beforeEach((to, from, next) => {
  const token = getAuthCookie()
  if (to.meta.requiresAuth !== false && !token) {
    next('/login')
  } else if (to.name === 'login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
