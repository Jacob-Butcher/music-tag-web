<template>
  <div class="mobile-shell">
    <div class="mobile-header">
      <span class="mobile-title">Music Tag</span>
    </div>
    <div class="mobile-content">
      <router-view />
    </div>
  </div>
</template>

<style scoped>
.mobile-shell {
  height: 100%; display: flex; flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif;
}
.mobile-header {
  height: 48px; padding: 0 16px; display: flex; align-items: center;
  border-bottom: 1px solid #f0f0f0; background: #fff; flex-shrink: 0;
  padding-top: env(safe-area-inset-top, 0);
}
.mobile-title { font-weight: 600; font-size: 15px; }
.mobile-content { flex: 1; overflow-y: auto; }
</style>
