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

      <!-- File tree -->
      <n-tree
        v-if="treeData.length"
        :data="treeData"
        :node-key="(node) => node.key"
        :virtual-scroll="false"
        block-line
        @update:selected-keys="(keys) => $emit('node-select', keys)"
        @update:checked-keys="(keys) => $emit('node-check', keys)"
        checkable
        :checked-keys="checkedKeys"
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
import { ArrowUndo, ArrowDown, FolderOpenOutline } from '@vicons/ionicons5'

defineProps({
  filePath: { type: String, required: true },
  treeData: { type: Array, default: () => [] },
  checkedKeys: { type: Array, default: () => [] },
})

defineEmits(['update:filePath', 'load-files', 'go-up', 'node-select', 'node-check'])
</script>
