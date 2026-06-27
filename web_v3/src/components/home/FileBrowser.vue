<template>
  <n-card :bordered="false" size="small" style="border-radius: 12px; height: 100%;">
    <n-space vertical :size="8">
      <n-space :size="4" align="center">
        <n-button text @click="$emit('go-up')" :disabled="filePath === '/'">
          <n-icon size="20"><ArrowUndo /></n-icon>
        </n-button>
        <n-input
          :value="searchText"
          size="small"
          placeholder="搜索歌曲"
          clearable
          @update:value="onInput"
          @keyup.enter="doSearch"
          @clear="doClear"
        />
        <n-button text @click="doSearch">
          <n-icon size="20"><Search /></n-icon>
        </n-button>
      </n-space>
      <div v-if="searchMode" style="font-size:12px;color:#999;">搜索结果: "{{ lastQuery }}" · {{ musicList.length }} 首</div>
      <div v-else style="font-size:12px;color:#999;">{{ filePath }}</div>

      <n-data-table
        v-if="musicList.length"
        :columns="columns"
        :data="musicList"
        :row-key="(row) => row.name"
        :row-props="rowProps"
        size="small"
        max-height="calc(100vh - 200px)"
        virtual-scroll
        @update:checked-row-keys="(v) => $emit('update:checkedKeys', v)"
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
import { h, ref } from 'vue'
import { NImage } from 'naive-ui'
import { ArrowUndo, Search, FolderOpenOutline } from '@vicons/ionicons5'

defineProps({
  filePath: { type: String, required: true },
  musicList: { type: Array, default: () => [] },
  checkedKeys: { type: Array, default: () => [] },
})

const emit = defineEmits(['update:filePath', 'load-files', 'go-up', 'update:checkedKeys', 'row-click', 'search'])

const searchText = ref('')
const searchMode = ref(false)
const lastQuery = ref('')

function onInput(val) {
  searchText.value = val
  if (!val) { searchMode.value = false; emit('load-files'); return }
  emit('update:filePath', val)
}

function doSearch() {
  if (searchText.value) {
    searchMode.value = true
    lastQuery.value = searchText.value
    emit('search', searchText.value)
  } else {
    searchMode.value = false
    emit('load-files')
  }
}

function doClear() {
  searchText.value = ''
  searchMode.value = false
  emit('load-files')
}

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
  return { style: 'cursor: pointer;', onClick: () => emit('row-click', row) }
}

const columns = [
  { type: 'selection', width: 40 },
  {
    title: '', key: 'artwork', width: 44,
    render(row) {
      if (!row._loaded) return h('div', { style: 'width:32px;height:32px;border-radius:4px;background:#f0f0f0;' })
      if (!row.artwork) return h('div', { style: 'width:32px;height:32px;border-radius:4px;background:#f5f5f7;font-size:18px;text-align:center;line-height:32px;' }, '🎵')
      return h(NImage, { src: row.artwork, width: 32, height: 32, style: 'border-radius:4px;object-fit:cover;', previewDisabled: true })
    },
  },
  {
    title: '标题', key: 'title', ellipsis: { tooltip: true }, width: 160,
    render(row) {
      if (row._loaded) return row.title || row.name
      return row.name.split('.').slice(0, -1).join('.') || row.name
    },
  },
  {
    title: '艺术家', key: 'artist', ellipsis: { tooltip: true }, width: 120,
    render(row) {
      if (!row._loaded) return h('span', { style: 'color:#ccc;' }, '...')
      return row.artist || '-'
    },
  },
  {
    title: '专辑', key: 'album', ellipsis: { tooltip: true }, width: 140,
    render(row) {
      if (!row._loaded) return h('span', { style: 'color:#ccc;' }, '...')
      return row.album || '-'
    },
  },
  {
    title: '年份', key: 'year', width: 56,
    render(row) {
      if (!row._loaded) return ''
      return row.year || ''
    },
  },
  {
    title: '歌词', key: 'lyrics', width: 48, align: 'center',
    render(row) {
      if (!row._loaded) return ''
      return row.lyrics ? '✓' : ''
    },
  },
  {
    title: '时长', key: 'duration', width: 56,
    render(row) {
      if (!row._loaded) return ''
      return formatDuration(row.duration)
    },
  },
  {
    title: '大小', key: 'size', width: 72,
    render: (row) => formatSize(row.size),
  },
]
</script>
