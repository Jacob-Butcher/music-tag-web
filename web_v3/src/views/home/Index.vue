<template>
  <div :style="layoutStyle">
    <!-- File Browser -->
    <div v-show="!isMobile || mobileView === 'file'" :style="panelStyle('480px')">
      <FileBrowser
        :file-path="filePath"
        :music-list="musicList"
        :checked-keys="checkedKeys"
        :selected-key="selectedKey"
        :loading-meta="loadingMeta"
        @update:file-path="(v) => filePath = v"
        @load-files="loadFiles"
        @go-up="goUpDir"
        @update:checked-keys="(v) => checkedKeys = v"
        @row-click="onRowClick"
      />
    </div>

    <!-- Tag Editor -->
    <div v-show="!isMobile || mobileView === 'edit'" :style="panelStyle('1')">
      <TagEditor
        :is-mobile="isMobile"
        :checked-keys="checkedKeys"
        :editing="editing"
        :manual-edit="manualEdit"
        :saving="saving"
        @save-tag="saveTag"
        @batch-save="batchSave"
        @show-batch-auto="showBatchAuto = true"
        @back="mobileView = 'file'"
      />
    </div>

    <!-- Auto-batch modal -->
    <n-modal v-model:show="showBatchAuto" title="批量自动刮削" preset="card" style="width: 400px;">
      <n-space vertical>
        <n-radio-group v-model:value="batchMode">
          <n-radio value="hard">严格模式</n-radio>
          <n-radio value="simple">宽松模式</n-radio>
        </n-radio-group>
        <n-select v-model:value="batchSources" multiple placeholder="音乐源" :options="sourceOptions" />
      </n-space>
      <template #footer>
        <n-button type="primary" round block @click="doBatchAuto">开始刮削</n-button>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useMessage } from 'naive-ui'
import api from '@/api'
import { useMobile } from '@/composables/useMobile'
import FileBrowser from '@/components/home/FileBrowser.vue'
import TagEditor from '@/components/home/TagEditor.vue'

const message = useMessage()
const { isMobile } = useMobile()

const mobileView = ref('file')
const filePath = ref('/app/media/')
const musicList = ref([])
const checkedKeys = ref([])
const selectedKey = ref('')
const editing = ref({})
const manualEdit = ref({})
const saving = ref(false)
const loadingMeta = ref(false)
const showBatchAuto = ref(false)
const batchMode = ref('hard')
const batchSources = ref([])
let currentFileName = ''

const sourceOptions = [
  { label: '网易云', value: 'netease' },
  { label: '咪咕', value: 'migu' },
  { label: 'QQ音乐', value: 'qmusic' },
  { label: '酷狗', value: 'kugou' },
]

const layoutStyle = computed(() =>
  isMobile.value
    ? { display: 'flex', flexDirection: 'column', height: '100%' }
    : { display: 'flex', gap: '12px', height: '100%' }
)

function panelStyle(flexVal) {
  if (isMobile.value) return { flex: 1, overflow: 'auto' }
  return { width: flexVal, minWidth: '300px', overflow: 'auto' }
}

// -- Fast file list (no ID3 read) --
async function loadFiles() {
  try {
    const res = await api.fileList({ file_path: filePath.value, sorted_fields: [] })
    if (res.data) {
      musicList.value = flattenTree(res.data)
    }
  } catch { message.error('加载文件失败') }
}

function flattenTree(nodes) {
  const files = []
  nodes.forEach((node) => {
    if (node.children) {
      node.children.forEach((child) => {
        if (child.icon !== 'icon-folder') {
          files.push({ name: child.name, size: child.size, update_time: child.update_time })
        }
      })
    }
  })
  return files
}

function goUpDir() {
  const parts = filePath.value.replace(/\/$/, '').split('/')
  parts.pop()
  filePath.value = parts.join('/') || '/'
  loadFiles()
}

// -- Click file → load ID3 for single file --
async function onRowClick(row) {
  selectedKey.value = row.name
  loadingMeta.value = true
  try {
    const res = await api.musicId3({ file_path: filePath.value, file_name: row.name })
    if (res.data) {
      editing.value = { ...res.data, is_save_lyrics_file: false, is_save_album_cover: false }
      currentFileName = row.name
      if (isMobile.value) mobileView.value = 'edit'
    }
  } catch { message.error('读取标签失败') }
  loadingMeta.value = false
}

async function saveTag() {
  saving.value = true
  try {
    await api.updateId3({
      music_id3_info: [{ file_full_path: filePath.value.replace(/\/$/, '') + '/' + currentFileName, ...editing.value }],
    })
    message.success('修改成功')
    if (isMobile.value) mobileView.value = 'file'
  } catch { message.error('保存失败') }
  saving.value = false
}

async function batchSave() {
  try {
    const selectData = musicList.value
      .filter((m) => checkedKeys.value.includes(m.name))
      .map((m) => ({ name: m.name, icon: 'icon-script-file' }))
    await api.batchUpdateId3({ file_full_path: filePath.value, select_data: selectData, music_info: manualEdit.value })
    message.success('批量修改成功')
  } catch { message.error('修改失败') }
}

function doBatchAuto() {
  const selectData = musicList.value
    .filter((m) => checkedKeys.value.includes(m.name))
    .map((m) => ({ name: m.name, icon: 'icon-script-file' }))
  api.batchAutoUpdateId3({ file_full_path: filePath.value, select_data: selectData, music_info: { select_mode: batchMode.value, source_list: batchSources.value } })
  message.success('任务已创建')
  showBatchAuto.value = false
}

loadFiles()
</script>
