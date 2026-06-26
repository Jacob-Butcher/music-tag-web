<template>
  <n-card title="用户管理" :bordered="false" style="border-radius: 12px;">
    <template #header-extra>
      <n-button type="primary" round size="small" @click="showAdd = true">新增用户</n-button>
    </template>
    <n-data-table :columns="columns" :data="data" :pagination="{ pageSize: 15 }" :bordered="false" size="small" />
  </n-card>
  <n-modal v-model:show="showAdd" title="新增用户" preset="card" style="width: 400px;">
    <n-form :model="form" label-width="80">
      <n-form-item label="手机号"><n-input v-model:value="form.username" /></n-form-item>
      <n-form-item label="密码"><n-input v-model:value="form.pwd" type="password" /></n-form-item>
      <n-form-item label="角色">
        <n-select v-model:value="form.role" :options="[{label:'管理员',value:1},{label:'普通用户',value:2}]" />
      </n-form-item>
    </n-form>
    <template #footer>
      <n-button type="primary" round @click="showAdd = false" style="height: 40px;">确定</n-button>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, h, reactive } from 'vue'
import { NButton } from 'naive-ui'

const showAdd = ref(false)
const form = reactive({ username: '', pwd: '', role: 1 })
const data = ref([])

const columns = [
  { title: '序号', key: 'ip', width: 150 },
  { title: '来源', key: 'source', width: 100 },
  { title: '状态', key: 'status', width: 100 },
  { title: '创建时间', key: 'create_time', width: 180 },
  {
    title: '操作', key: 'actions', width: 160,
    render() {
      return h('div', { style: 'display: flex; gap: 8px' }, [
        h(NButton, { text: true, type: 'primary', size: 'small' }, () => '编辑'),
        h(NButton, { text: true, type: 'error', size: 'small' }, () => '删除'),
      ])
    }
  },
]
</script>
