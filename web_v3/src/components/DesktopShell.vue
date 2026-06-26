<template>
  <n-layout has-sider style="height: 100vh;">
    <n-layout-sider bordered collapse-mode="width" :collapsed-width="64" :width="200" style="background: #f5f5f7;">
      <div style="padding: 16px; display: flex; align-items: center; gap: 8px;">
        <n-avatar :size="32" src="/assets/favicon_64.ico" />
        <span style="font-weight: 600; font-size: 15px;">Music Tag</span>
      </div>
      <n-menu :value="activeMenu" :options="menuOptions" @update:value="handleMenu" />
    </n-layout-sider>
    <n-layout>
      <n-layout-header bordered style="height: 52px; padding: 0 16px; display: flex; align-items: center; justify-content: space-between;">
        <span style="font-weight: 500;">{{ $route.meta.title }}</span>
        <n-space align="center">
          <n-button text size="small" @click="window.open('https://xiers-organization.gitbook.io/music-tag-web/')">使用手册</n-button>
          <n-button text size="small" @click="window.open('https://github.com/xhongc/music-tag-web')">关于作者</n-button>
        </n-space>
      </n-layout-header>
      <n-layout-content style="padding: 16px; overflow: auto;">
        <router-view />
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script setup>
import { ref, h } from 'vue'
import { NIcon } from 'naive-ui'
import { HomeOutline } from '@vicons/ionicons5'

const activeMenu = ref('home')

const menuOptions = [
  { label: '首页', key: 'home', icon: () => h(NIcon, null, () => h(HomeOutline)) },
]

function handleMenu() {
  // single page, no navigation needed
}
</script>
