<template>
  <div class="login-wrap">
    <n-card class="login-card" :bordered="false">
      <template #header>
        <div style="text-align: center; font-size: 20px; font-weight: 600;">登录</div>
      </template>
      <n-form ref="formRef" :model="form" :rules="rules" size="large">
        <n-form-item path="username" label="用户名">
          <n-input v-model:value="form.username" placeholder="请输入用户名" clearable />
        </n-form-item>
        <n-form-item path="password" label="密码">
          <n-input v-model:value="form.password" type="password" placeholder="请输入密码" show-password-on="click" @keyup.enter="submit" />
        </n-form-item>
      </n-form>
      <n-button type="primary" block round size="large" :loading="loading" @click="submit" style="height: 48px;">
        登录
      </n-button>
    </n-card>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import api from '@/api'

const router = useRouter()
const message = useMessage()
const loading = ref(false)
const form = reactive({ username: 'admin', password: 'admin' })
const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  password: [{ required: true, message: '请输入密码' }],
}

async function submit() {
  loading.value = true
  try {
    const res = await api.login(form)
    const token = res.access || res.token || (res.data && res.data.access)
    if (token) {
      // set cookie
      const curDate = new Date()
      const curTamp = curDate.getTime()
      const curWeeHours = new Date(curDate.toLocaleDateString()).getTime() - 1
      const passedTamp = curTamp - curWeeHours
      const leftTamp = 7 * 24 * 60 * 60 * 1000 - passedTamp
      const leftTime = new Date()
      leftTime.setTime(leftTamp + curTamp)
      document.cookie = 'AUTHORIZATION=' + escape('JWT ' + token) + ';expires=' + leftTime.toGMTString()
      router.push('/')
    } else {
      message.error('登录失败：未获取到认证令牌')
    }
  } catch (e) {
    message.error('登录请求失败：' + e)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  height: 100vh; display: flex; align-items: center; justify-content: center;
  background: linear-gradient(135deg, #f5f5f7 0%, #e8e8ed 100%);
}
.login-card {
  width: 360px; max-width: 90vw;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.06);
}
</style>
