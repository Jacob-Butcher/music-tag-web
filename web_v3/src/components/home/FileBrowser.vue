<template>
  <n-card :bordered="false" size="small" style="border-radius: 12px; height: 100%;">
    <n-space vertical :size="8">
      <!-- Path input bar -->
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

      <!-- Music table -->
      <n-data-table
        v-if="musicList.length"
        :columns="columns"
        :data="musicList"
        :row-key="(row) => row.file_name"
        :row-props="rowProps"
        :single-line="false"
        :bordered="false"
        size="small"
        max-height="calc(100vh - 200px)"
        virtual-scroll
        @update:checked-row-keys="$emit('update:checkedKeys', $event)"
        :checked-row-keys="checkedKeys"
      />

      <!-- Empty state -->
      <div v-else style="padding: 40px; text-align: center; color: #999;">
        <n-icon size="40"><FolderOpenOutline /></n-icon>
        <p>点击上方输入文件夹路径</p>
      </div>
    </n-space>
  </n-card>
</template>

<script setup>
import { h } from 'vue'
import { NButton } from 'naive-ui'
import { ArrowUndo, ArrowDown, FolderOpenOutline } from '@vicons/ionicons5'

const props = defineProps({
  filePath: { type: String, required: true },
  musicList: { type: Array, default: () => [] },
  checkedKeys: { type: Array, default: () => [] },
  selectedKey: { type: String, default: '' },
})

const emit = defineEmits(['update:filePath', 'load-files', 'go-up', 'update:checkedKeys', 'row-click'])

function formatDuration(sec) {
  if (!sec) return ''
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${m}:${String(s).padStart(2, '0')}`
}

function formatSize(bytes) {
  if (!bytes) return ''
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1048576).toFixed(1) + ' MB'
}

function rowProps(row) {
  return {
    style: 'cursor: pointer;',
    onClick: () => emit('row-click', row),
  }
}

const columns = [
  {
    type: 'selection',
    width: 40,
  },
  {
    title: '标题',
    key: 'title',
    ellipsis: { tooltip: true },
    width: 180,
    render(row) {
      return row.title || row.file_name
    },
  },
  {
    title: '艺术家',
    key: 'artist',
    ellipsis: { tooltip: true },
    width: 130,
    render(row) {
      return row.artist || '-'
    },
  },
  {
    title: '专辑',
    key: 'album',
    ellipsis: { tooltip: true },
    width: 150,
    render(row) {
      return row.album || '-'
    },
  },
  {
    title: '年份',
    key: 'year',
    width: 60,
    render(row) {
      return row.year || ''
    },
  },
  {
    title: '时长',
    key: 'duration',
    width: 60,
    render(row) {
      return formatDuration(row.duration)
    },
  },
  {
    title: '大小',
    key: 'file_size',
    width: 70,
    render(row) {
      return formatSize(row.file_size)
    },
  },
]
</script>
