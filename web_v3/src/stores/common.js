import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useCommonStore = defineStore('common', () => {
  const userRole = ref('')
  const fullPath = ref('')
  const hasMsg = ref(false)

  function setUserRole(role) { userRole.value = role }
  function setFullPath(path) { fullPath.value = path }
  function setHasMsg(val) { hasMsg.value = val }

  return { userRole, fullPath, hasMsg, setUserRole, setFullPath, setHasMsg }
})
