<template>
  <n-card :bordered="false" size="small" style="border-radius: 12px; height: 100%;">
    <n-space vertical :size="8">
      <n-space :size="4" align="center">
        <n-button text @click="$emit('go-up')" :disabled="filePath === '/'">
          <n-icon size="20"><ArrowUndo /></n-icon>
        </n-button>
        <n-input
          :value="filePath"
          size="small"
          placeholder="输入文件夹路径"
          @update:value="(val) => $emit('update:filePath', val)"
          @keyup.enter="$emit('load-files')"
        />
        <n-button text @click="$emit('load-files')">
          <n-icon size="20"><ArrowDown /></n-icon>
        </n-button>
      </n-space>

      <n-data-table
        v-if="musicList.length"
        :columns="columns"
        :data="musicList"
        :row-key="(row) => row.name"
        :row-props="rowProps"
        size="small"
        max-height="calc(100vh - 200px)"
        virtual-scroll
        @update:checked-row-keys="$emit('update:checkedKeys', $event)"
        :checked-row-keys="checkedKeys"
      />

      <div v-else style="padding: 40px; text-align: center; color: #999;">
        <n-icon size="40"><FolderOpenOutline /></n-icon>
        <p>点击上方输入文件夹路径</p>
      </div>
    </n-space>
  </n-card>
</template>

<script setup>
import { ArrowUndo, ArrowDown, FolderOpenOutline } from '@vicons/ionicons5'

defineProps({
  filePath: { type: String, required: true },
  musicList: { type: Array, default: () => [] },
  checkedKeys: { type: Array, default: () => [] },
})

const emit = defineEmits(['update:filePath', 'load-files', 'go-up', 'update:checkedKeys', 'row-click'])

function formatSize(bytes) {
  if (!bytes) return ''
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1048576).toFixed(1) + ' MB'
}

function rowProps(row) {
  return { style: 'cursor: pointer;', onClick: () => emit('row-click', row) }
}

const columns = [
  { type: 'selection', width: 40 },
  { title: '文件名', key: 'name', ellipsis: { tooltip: true } },
  { title: '大小', key: 'size', width: 80, render: (row) => formatSize(row.size) },
  { title: '修改时间', key: 'update_time', width: 160 },
]
</script>
