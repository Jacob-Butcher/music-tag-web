<template>
  <n-config-provider :theme-overrides="themeOverrides" :locale="zhCN" :date-locale="dateZhCN">
    <n-message-provider>
      <div style="height: 100vh; width: 100vw; overflow: hidden; background: #f5f5f7;">
        <MobileShell v-if="isMobile" />
        <DesktopShell v-else />
      </div>
    </n-message-provider>
  </n-config-provider>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { zhCN, dateZhCN } from 'naive-ui'
import DesktopShell from '@/components/DesktopShell.vue'
import MobileShell from '@/components/MobileShell.vue'

const isMobile = ref(window.innerWidth < 768)

const themeOverrides = {
  common: {
    primaryColor: '#0071e3',
    primaryColorHover: '#0077ed',
    primaryColorPressed: '#0060c9',
    borderRadius: '12px',
    fontFamily: "-apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif",
  }
}

function handleResize() {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => window.addEventListener('resize', handleResize))
onBeforeUnmount(() => window.removeEventListener('resize', handleResize))
</script>

<style>
* { -webkit-tap-highlight-color: transparent; }
html { touch-action: manipulation; }
body { margin: 0; -webkit-text-size-adjust: 100%; }
</style>
