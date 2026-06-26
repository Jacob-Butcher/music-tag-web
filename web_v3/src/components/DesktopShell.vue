<template>
  <div style="height: 100vh; display: flex; flex-direction: column;">
    <div style="height: 48px; padding: 0 16px; display: flex; align-items: center; border-bottom: 1px solid #f0f0f0; background: #fff; flex-shrink: 0;">
      <span style="font-weight: 600; font-size: 15px;">Music Tag</span>
    </div>
    <div style="flex: 1; overflow: auto; padding: 16px;">
      <router-view />
    </div>
  </div>
</template>
