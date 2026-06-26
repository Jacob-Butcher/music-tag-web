<template>
  <n-card :bordered="false" size="small" style="border-radius: 12px;">
    <!-- Mobile header with back + search -->
    <div v-if="isMobile" style="display: flex; align-items: center; padding: 4px 0 12px;">
      <n-button text @click="$emit('back')">
        <n-icon size="22"><ChevronBack /></n-icon>
      </n-button>
      <span style="flex:1; text-align:center; font-weight:600;">{{ editing.title || editing.filename || '编辑' }}</span>
      <n-button text @click="$emit('search-resource')">
        <n-icon size="22"><Search /></n-icon>
      </n-button>
    </div>

    <!-- Single file editing -->
    <template v-if="checkedKeys.length === 0">
      <n-space vertical :size="12">
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
      </n-space>
    </template>
  </n-card>
</template>

<script setup>
import { ChevronBack, Search } from '@vicons/ionicons5'

defineProps({
  isMobile: { type: Boolean, default: false },
  checkedKeys: { type: Array, default: () => [] },
  editing: { type: Object, default: () => ({}) },
  manualEdit: { type: Object, default: () => ({}) },
  saving: { type: Boolean, default: false },
})

defineEmits(['save-tag', 'batch-save', 'show-batch-auto', 'search-resource', 'back'])
</script>
