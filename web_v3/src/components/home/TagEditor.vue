<template>
  <n-card :bordered="false" size="small" style="border-radius: 12px;">
    <!-- Mobile header with back -->
    <div v-if="isMobile" style="display: flex; align-items: center; padding: 4px 0 12px;">
      <n-button text @click="$emit('back')">
        <n-icon size="22"><ChevronBack /></n-icon>
      </n-button>
      <span style="flex:1; text-align:center; font-weight:600;">{{ editing.title || editing.filename || '编辑' }}</span>
      <span style="width: 22px;" />
    </div>

    <!-- Single file editing -->
    <template v-if="checkedKeys.length === 0">
      <n-space vertical :size="10">
        <!-- File info bar -->
        <div style="display:flex;flex-wrap:wrap;gap:4px 16px;padding:8px 12px;background:#f5f5f7;border-radius:8px;font-size:12px;color:#666;">
          <span>📄 {{ editing.filename }}</span>
          <span v-if="editing.duration">⏱ {{ fmtDuration(editing.duration) }}</span>
          <span v-if="editing.bit_rate">📊 {{ formatBitrate(editing.bit_rate) }}</span>
          <span v-if="editing.size">💾 {{ formatSize(editing.size) }}</span>
          <span v-if="editing.tracknumber">🔢 #{{ editing.tracknumber }}</span>
        </div>
        <n-input v-model:value="editing.title" placeholder="标题" />
        <n-input v-model:value="editing.artist" placeholder="艺术家" />
        <n-input v-model:value="editing.album" placeholder="专辑" />
        <n-input v-model:value="editing.albumartist" placeholder="专辑艺术家" />
        <n-input v-model:value="editing.genre" placeholder="风格" />
        <n-input-number v-model:value="editing.year" placeholder="年份" :min="1900" :max="2099" />
        <n-input v-model:value="editing.lyrics" type="textarea" :rows="8" placeholder="歌词" />
        <n-input v-model:value="editing.comment" type="textarea" placeholder="描述" />
        <template v-if="editing.artwork">
          <n-image :src="editing.artwork" width="200" style="border-radius: 8px;" />
        </template>
        <!-- Online search -->
        <div style="display:flex;gap:8px;">
          <n-select v-model:value="searchSource" size="small" style="width:110px;" :options="sourceOpts" placeholder="数据源" />
          <n-button size="small" :loading="searching" @click="doOnlineSearch" style="flex:1;">在线搜索资源</n-button>
        </div>
        <div v-if="searchResults.length" style="max-height:180px;overflow:auto;border:1px solid #eee;border-radius:8px;">
          <div v-for="(item, i) in searchResults" :key="i"
            style="display:flex;align-items:center;padding:6px 8px;cursor:pointer;border-bottom:1px solid #f5f5f5;"
            :style="{ background: hoverIdx === i ? '#f5f5f7' : '' }"
            @mouseenter="hoverIdx = i" @mouseleave="hoverIdx = -1"
            @click="!item._err && $emit('apply-meta', item); !item._err && (searchResults = [])">
            <n-image v-if="item.album_img" :src="item.album_img" width="36" height="36" style="border-radius:4px;margin-right:8px;" preview-disabled />
            <div style="flex:1;overflow:hidden;">
              <div style="font-size:12px;font-weight:500;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ item.name }}</div>
              <div style="font-size:11px;color:#999;">{{ item.artist }} · {{ item.album }}<span v-if="item.year"> · {{ item.year }}</span></div>
            </div>
          </div>
        </div>
        <n-button type="primary" block round :loading="saving" @click="$emit('save-tag')" style="height: 48px;">
          保存信息
        </n-button>
      </n-space>
    </template>

    <!-- Batch editing -->
    <template v-else>
      <n-space vertical :size="12">
        <n-alert type="info">已选择 {{ checkedKeys.length }} 个文件</n-alert>
        <n-input v-model:value="manualEdit.title" placeholder="批量设置标题 (支持变量 ${title}, ${album})" />
        <n-input v-model:value="manualEdit.artist" placeholder="批量设置艺术家" />
        <n-input v-model:value="manualEdit.album" placeholder="批量设置专辑" />
        <n-button type="primary" block round @click="$emit('batch-save')" style="height: 48px;">手动修改</n-button>
        <n-button type="warning" block round @click="$emit('show-batch-auto')" style="height: 48px;">自动刮削</n-button>
        <!-- Task progress indicator -->
        <div v-if="taskInfo.items && taskInfo.items.length" style="padding:8px 12px;background:#f5f5f7;border-radius:8px;font-size:12px;">
          <div style="display:flex;justify-content:space-between;align-items:center;">
            <span>刮削: <b style="color:#18a058">{{ taskInfo.success }}</b> / <b>{{ taskInfo.total }}</b><span v-if="taskInfo.failed" style="color:#d03050"> ({{ taskInfo.failed }} 失败)</span></span>
            <n-button text size="tiny" type="primary" @click="$emit('show-progress')">查看进度</n-button>
          </div>
        </div>
      </n-space>
    </template>
  </n-card>
</template>

<script setup>
import { ref } from 'vue'
import { ChevronBack } from '@vicons/ionicons5'
import api from '@/api'

const props = defineProps({
  isMobile: { type: Boolean, default: false },
  checkedKeys: { type: Array, default: () => [] },
  editing: { type: Object, default: () => ({}) },
  manualEdit: { type: Object, default: () => ({}) },
  saving: { type: Boolean, default: false },
  taskInfo: { type: Object, default: () => ({}) },
})

defineEmits(['save-tag', 'batch-save', 'show-batch-auto', 'show-progress', 'back', 'apply-meta'])

const searchSource = ref('netease')
const searching = ref(false)
const searchResults = ref([])
const hoverIdx = ref(-1)

const sourceOpts = [
  { label: '网易云', value: 'netease' },
  { label: 'QQ音乐', value: 'qmusic' },
  { label: '酷狗', value: 'kugou' },
  { label: '酷我', value: 'kuwo' },
  { label: '咪咕', value: 'migu' },
]

async function doOnlineSearch() {
  const title = props.editing.title
  if (!title) return
  searching.value = true
  searchResults.value = []
  try {
    const res = await api.fetchId3Title({ title, resource: searchSource.value })
    if (res.data && res.data.length) {
      searchResults.value = res.data
    } else if (res.result === false || res.code) {
      searchResults.value = [{ name: '搜索失败: ' + (res.message || res.msg || '无结果'), artist: '', album: '', _err: true }]
    }
  } catch { searchResults.value = [{ name: '网络请求失败，请检查网络连接', artist: '', album: '', _err: true }] }
  searching.value = false
}

function fmtDuration(sec) {
  if (!sec) return ''
  const m = Math.floor(sec / 60)
  const s = Math.floor(sec % 60)
  return `${m}:${String(s).padStart(2, '0')}`
}

function formatBitrate(bps) {
  if (!bps) return ''
  return Math.round(bps / 1000) + ' kbps'
}

function formatSize(bytes) {
  if (!bytes) return ''
  if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1048576).toFixed(1) + ' MB'
}
</script>
