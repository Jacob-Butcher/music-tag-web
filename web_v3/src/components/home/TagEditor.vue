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
import { ChevronBack } from '@vicons/ionicons5'

defineProps({
  isMobile: { type: Boolean, default: false },
  checkedKeys: { type: Array, default: () => [] },
  editing: { type: Object, default: () => ({}) },
  manualEdit: { type: Object, default: () => ({}) },
  saving: { type: Boolean, default: false },
  taskInfo: { type: Object, default: () => ({}) },
})

defineEmits(['save-tag', 'batch-save', 'show-batch-auto', 'show-progress', 'back'])

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
