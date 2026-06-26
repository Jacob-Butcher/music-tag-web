<template>
  <n-card :bordered="false" size="small" style="border-radius: 12px;">
    <!-- Mobile header -->
    <div v-if="isMobile" style="display: flex; align-items: center; padding: 4px 0 12px;">
      <n-button text @click="$emit('back')">
        <n-icon size="22"><ChevronBack /></n-icon>
      </n-button>
      <span style="flex:1; text-align:center; font-weight:600;">搜索结果</span>
    </div>

    <!-- Result list -->
    <div v-if="results.length > 0">
      <div
        v-for="(item, i) in results"
        :key="i"
        style="display: flex; align-items: center; padding: 8px; border-bottom: 1px solid #f0f0f0; cursor: pointer;"
        @click="$emit('apply', item)"
      >
        <n-image
          v-if="item.album_img"
          :src="item.album_img"
          width="48"
          height="48"
          style="border-radius: 6px; margin-right: 10px;"
          preview-disabled
        />
        <div style="flex: 1; overflow: hidden;">
          <div style="font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            {{ item.name }}
          </div>
          <div style="font-size: 12px; color: #999;">{{ item.artist }} · {{ item.album }}</div>
        </div>
        <n-tag size="small" v-if="item.year">{{ item.year }}</n-tag>
      </div>
    </div>

    <!-- Empty state -->
    <div v-else style="padding: 40px; text-align: center; color: #999;">
      <n-icon size="40"><Search /></n-icon>
      <p>点击标签页的 🔍 搜索资源</p>
    </div>
  </n-card>
</template>

<script setup>
import { ChevronBack, Search } from '@vicons/ionicons5'

defineProps({
  isMobile: { type: Boolean, default: false },
  results: { type: Array, default: () => [] },
})

defineEmits(['apply', 'back'])
</script>
