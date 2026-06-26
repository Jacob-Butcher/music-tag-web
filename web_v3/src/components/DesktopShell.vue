<template>
  <n-layout has-sider style="height: 100vh;">
    <n-layout-sider bordered collapse-mode="width" :collapsed-width="64" :width="200" style="background: #f5f5f7;">
      <div style="padding: 16px; display: flex; align-items: center; gap: 8px;">
        <n-avatar :size="32" src="/assets/favicon_64.ico" />
        <span v-if="true" style="font-weight: 600; font-size: 15px;">Music Tag</span>
      </div>
      <n-menu :value="activeMenu" :options="menuOptions" @update:value="handleMenu" />
    </n-layout-sider>
    <n-layout>
      <n-layout-header bordered style="height: 52px; padding: 0 16px; display: flex; align-items: center; justify-content: space-between;">
        <span style="font-weight: 500;">{{ $route.meta.title }}</span>
        <n-space align="center">
          <n-dropdown trigger="click" :options="userOptions" @select="handleUserAction">
            <n-button text>{{ userData.username || 'admin' }}</n-button>
          </n-dropdown>
        </n-space>
      </n-layout-header>
      <n-layout-content style="padding: 16px; overflow: auto;">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup>
import { ref, computed, h, onMounted } from 'vue'
import { useCommonStore } from '@/stores/common'
import { NIcon } from 'naive-ui'
import { HomeOutline, PeopleOutline } from '@vicons/ionicons5'
import api from '@/api'

const store = useCommonStore()
const userData = ref({})
const activeMenu = ref('home')

const menuOptions = computed(() => {
  const opts = [{ label: '首页', key: 'home', icon: () => h(NIcon, null, () => h(HomeOutline)) }]
  if (store.userRole === 'admin') {
    opts.push({ label: '用户管理', key: 'user', icon: () => h(NIcon, null, () => h(PeopleOutline)) })
  }
  return opts
})

const userOptions = [
  { label: '后台管理', key: 'admin' },
  { label: '使用手册', key: 'manual' },
  { label: '关于作者', key: 'about' },
]

onMounted(async () => {
  try {
    const res = await api.loginInfo()
    if (res.data) { userData.value = res.data; store.setUserRole(res.data.role) }
  } catch { /* */ }
})

function handleMenu(key) { activeMenu.value = key; if (key === 'home') window.location.hash = '#/'; else window.location.hash = '#/' + key }
function handleUserAction(key) {
  if (key === 'admin') window.open('/admin/')
  if (key === 'manual') window.open('https://xiers-organization.gitbook.io/music-tag-web/')
  if (key === 'about') window.open('https://github.com/xhongc/music-tag-web')
}
</script>
