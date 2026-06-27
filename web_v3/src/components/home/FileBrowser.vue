<template>
  <n-card :bordered="false" size="small" style="border-radius: 12px; height: 100%;">
    <n-space vertical :size="8">
      <n-space :size="4" align="center">
        <n-input
          v-model:value="searchText"
          size="small"
          placeholder="搜索歌曲"
          clearable
          @keyup.enter="doSearch"
          @clear="doClear"
        />
        <n-button text @click="doSearch">
          <n-icon size="20"><Search /></n-icon>
        </n-button>
      </n-space>
      <div v-if="searchMode" style="font-size:12px;color:#999;">"{{ lastQuery }}" · {{ filteredList.length }} 首</div>

      <!-- Filters -->
      <n-space :size="4" align="center" v-if="musicList.some(r => r._loaded)">
        <span style="font-size:11px;color:#999;">筛选缺失:</span>
        <n-checkbox v-for="f in filterOptions" :key="f.key" size="small" :checked="filters[f.key]" @update:checked="(v) => filters[f.key] = v">{{ f.label }}</n-checkbox>
        <span style="font-size:11px;color:#999;">{{ filteredList.length }}/{{ musicList.length }}</span>
      </n-space>

      <n-data-table
        v-if="filteredList.length"
        :columns="columns"
        :data="filteredList"
        :row-key="(row) => row.name"
        :row-props="rowProps"
        size="small"
        max-height="calc(100vh - 200px)"
        virtual-scroll
        @update:checked-row-keys="(v) => $emit('update:checkedKeys', v)"
        :checked-row-keys="checkedKeys"
      />

      <div v-else-if="!musicList.length" style="padding: 40px; text-align: center; color: #999;">
        <n-icon size="40"><FolderOpenOutline /></n-icon>
        <p>搜索歌曲查看标签信息</p>
      </div>
      <div v-else style="padding: 20px; text-align: center; color: #999;font-size:13px;">当前筛选条件无匹配结果</div>
    </n-space>
  </n-card>
</template>

<script setup>
import { h, ref, reactive, computed } from 'vue'
import { NImage } from 'naive-ui'
import { Search, FolderOpenOutline } from '@vicons/ionicons5'

const props = defineProps({
  musicList: { type: Array, default: () => [] },
  checkedKeys: { type: Array, default: () => [] },
})

const emit = defineEmits(['update:checkedKeys', 'row-click', 'search', 'clear-search'])

const searchText = ref('')
const searchMode = ref(false)
const lastQuery = ref('')

const filters = reactive({ noArtwork: false, noLyrics: false, noArtist: false, noAlbum: false, noYear: false })
const filterOptions = [
  { key: 'noArtwork', label: '封面' },
  { key: 'noLyrics', label: '歌词' },
  { key: 'noArtist', label: '艺术家' },
  { key: 'noAlbum', label: '专辑' },
  { key: 'noYear', label: '年份' },
]

const filteredList = computed(() => {
  const active = Object.entries(filters).filter(([, v]) => v).map(([k]) => k)
  if (!active.length) return props.musicList
  return props.musicList.filter((row) => {
    if (!row._loaded) return true
    if (active.includes('noArtwork') && !row.artwork) return true
    if (active.includes('noLyrics') && !row.lyrics) return true
    if (active.includes('noArtist') && !row.artist) return true
    if (active.includes('noAlbum') && !row.album) return true
    if (active.includes('noYear') && !row.year) return true
    return false
  })
})

function doSearch() {
  if (searchText.value) {
    searchMode.value = true
    lastQuery.value = searchText.value
    emit('search', searchText.value)
  }
}

function doClear() {
  searchText.value = ''
  searchMode.value = false
  emit('clear-search')
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
