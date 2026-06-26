<template>
  <div class="mobile-shell">
    <div class="mobile-content">
      <router-view />
    </div>
    <!-- Bottom Tab Bar -->
    <div class="bottom-nav">
      <div class="nav-item" :class="{ active: $route.name === 'home' }" @click="$router.push('/')">
        <n-icon size="22"><MusicalNotesOutline /></n-icon>
        <span>首页</span>
      </div>
      <div class="nav-item" v-if="store.userRole === 'admin'" :class="{ active: $route.name === 'user' }" @click="$router.push('/user')">
        <n-icon size="22"><PeopleOutline /></n-icon>
        <span>用户</span>
      </div>
      <div class="nav-item" @click="showDrawer = true">
        <n-icon size="22"><MenuOutline /></n-icon>
        <span>菜单</span>
      </div>
    </div>
    <!-- Bottom Sheet -->
    <n-drawer v-model:show="showDrawer" placement="bottom" :height="280">
      <n-drawer-content title="" :native-scrollbar="false">
        <div class="drawer-user">
          <n-avatar round :size="40" style="background: #0071e3">{{ userData.username?.[0] || 'U' }}</n-avatar>
          <span style="margin-left: 12px; font-size: 16px; font-weight: 600;">{{ userData.username || '用户' }}</span>
        </div>
        <n-divider />
        <n-space vertical :size="4">
          <n-button text @click="goAdmin">后台管理</n-button>
          <n-button text @click="goManual">使用手册</n-button>
          <n-button text @click="goAbout">关于作者</n-button>
        </n-space>
      </n-drawer-content>
    </n-drawer>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useCommonStore } from '@/stores/common'
import { MusicalNotesOutline, PeopleOutline, MenuOutline } from '@vicons/ionicons5'
import api from '@/api'

const store = useCommonStore()
const showDrawer = ref(false)
const userData = ref({})

onMounted(async () => {
  try {
    const res = await api.loginInfo()
    if (res.data) {
      userData.value = res.data
      store.setUserRole(res.data.role)
    } else {
      // not logged in
    }
  } catch { /* silent */ }
})

function goAdmin() { showDrawer.value = false; window.open('/admin/') }
function goManual() { showDrawer.value = false; window.open('https://xiers-organization.gitbook.io/music-tag-web/') }
function goAbout() { showDrawer.value = false; window.open('https://github.com/xhongc/music-tag-web') }
</script>

<style scoped>
.mobile-shell {
  height: 100%; display: flex; flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif;
}
.mobile-content { flex: 1; overflow-y: auto; padding-bottom: calc(56px + env(safe-area-inset-bottom, 0)); }
.bottom-nav {
  position: fixed; bottom: 0; left: 0; width: 100%;
  height: 56px; padding-bottom: env(safe-area-inset-bottom, 0);
  display: flex; background: rgba(255,255,255,0.92);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  border-top: 0.5px solid rgba(60,60,67,0.08); z-index: 100;
}
.nav-item {
  flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
  font-size: 10px; color: #86868b; cursor: pointer; transition: color 0.15s;
}
.nav-item.active { color: #0071e3; }
.drawer-user { display: flex; align-items: center; padding: 8px 0; }
</style>
