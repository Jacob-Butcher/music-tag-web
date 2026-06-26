<template>
  <n-card title="用户信息" :bordered="false" style="border-radius: 12px; max-width: 480px;">
    <template #header-extra>
      <n-button type="primary" round size="small" @click="window.open('/admin/')">后台管理</n-button>
    </template>
    <n-space v-if="user" vertical :size="12">
      <n-descriptions label-placement="left" :column="1" bordered>
        <n-descriptions-item label="用户名">{{ user.username }}</n-descriptions-item>
        <n-descriptions-item label="角色">
          <n-tag :type="user.role === 'admin' ? 'info' : 'default'">
            {{ user.role === 'admin' ? '管理员' : '普通用户' }}
          </n-tag>
        </n-descriptions-item>
      </n-descriptions>
      <n-divider>操作</n-divider>
      <n-button text @click="window.open('/admin/auth/user/')">管理用户</n-button>
      <n-button text @click="window.open('/admin/auth/group/')">管理权限组</n-button>
    </n-space>
    <n-skeleton v-else text :repeat="3" />
  </n-card>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/api'

const user = ref(null)

onMounted(async () => {
  try {
    const res = await api.loginInfo()
    if (res.data) user.value = res.data
  } catch { /* ignore */ }
})
</script>
