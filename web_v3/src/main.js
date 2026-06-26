import { createApp } from 'vue'
import { createPinia } from 'pinia'
import naive from 'naive-ui'
import router from './router'
import App from './App.vue'
import api from './api'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(naive)
app.config.globalProperties.$api = api

// cookie helpers
app.config.globalProperties.$getCookie = (name) => {
  const reg = new RegExp('(^| )' + name + '=([^;]*)(;|$)')
  const arr = document.cookie.match(reg)
  return arr ? unescape(arr[2]) : null
}
app.config.globalProperties.$setCookie = (name, value, day) => {
  if (day > 0) {
    const curDate = new Date()
    const curTamp = curDate.getTime()
    const curWeeHours = new Date(curDate.toLocaleDateString()).getTime() - 1
    const passedTamp = curTamp - curWeeHours
    const leftTamp = 7 * 24 * 60 * 60 * 1000 - passedTamp
    const leftTime = new Date()
    leftTime.setTime(leftTamp + curTamp)
    document.cookie = name + '=' + escape(value) + ';expires=' + leftTime.toGMTString()
  } else {
    document.cookie = name + '=' + escape(value)
  }
}

app.mount('#app')
