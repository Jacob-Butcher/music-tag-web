<template>
  <div :style="layoutStyle">
    <!-- File Browser -->
    <div v-show="!isMobile || mobileView === 'file'" :style="panelStyle('1')">
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
        @search="onSearch"
      />
    </div>

    <!-- Tag Editor: always visible on desktop, push nav on mobile -->
    <div v-show="!isMobile || mobileView === 'edit'" :style="panelStyle('420px')">
      <TagEditor
        :is-mobile="isMobile"
        :checked-keys="checkedKeys"
        :editing="editing"
        :manual-edit="manualEdit"
        :saving="saving"
        :task-info="taskModal"
        @save-tag="saveTag"
        @batch-save="batchSave"
        @show-batch-auto="showBatchAuto = true"
        @show-progress="taskModal.show = true"
        @apply-meta="applyOnlineMeta"
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

    <!-- Task progress modal (keeps polling even when closed) -->
    <n-modal :show="taskModal.show" :on-update:show="(v) => taskModal.show = v" title="刮削进度" preset="card" style="width: 480px; max-height: 70vh;">
      <n-space v-if="taskModal.total" vertical :size="12">
        <div style="display:flex;gap:24px;font-size:13px;">
          <span>总数: <b>{{ taskModal.total }}</b></span>
          <span style="color:#18a058;">成功: <b>{{ taskModal.success }}</b></span>
          <span style="color:#d03050;">失败: <b>{{ taskModal.failed }}</b></span>
          <span v-if="taskModal.pending" style="color:#999;">处理中: {{ taskModal.pending }}</span>
        </div>
        <n-progress
          type="line"
          :percentage="taskModal.total ? Math.round((taskModal.success + taskModal.failed) / taskModal.total * 100) : 0"
          :color="taskModal.failed ? '#f0a020' : '#18a058'"
        />
        <n-data-table
          :columns="taskColumns"
          :data="taskModal.items"
          size="small"
          :row-key="(r) => r.full_path"
          max-height="300"
          virtual-scroll
        />
      </n-space>
      <div v-else style="text-align:center;padding:20px;color:#999;">等待任务开始...</div>
    </n-modal>
  </div>
</template>

<script setup>
import { h, ref, computed, onBeforeUnmount } from 'vue'
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
const taskModal = ref({ show: false, total: 0, success: 0, failed: 0, pending: 0, items: [] })
let taskPollTimer = null
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
  if (flexVal === '1') return { flex: 1, minWidth: '300px', overflow: 'auto' }
  return { width: flexVal, flexShrink: 0, overflow: 'auto' }
}

const BATCH_SIZE = 30
let batchTimer = null

// -- Fast file list first, then batch-load ID3 --
async function loadFiles() {
  try {
    const res = await api.fileList({ file_path: filePath.value, sorted_fields: [] })
    if (res.data) {
      const files = flattenTree(res.data)
      musicList.value = files
      // Start batch-loading metadata in background
      startBatchLoad(files.map((f) => f.name))
    }
  } catch { message.error('加载文件失败') }
}

async function onSearch(query) {
  try {
    const res = await api.searchMusic({ query })
    if (res.data) {
      musicList.value = res.data.map((f) => ({
        name: f.name,
        size: f.size,
        update_time: '',
        file_path: f.file_path,
        full_path: f.full_path,
      }))
      startBatchLoad(res.data.map((f) => f.name))
    }
  } catch { message.error('搜索失败') }
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

async function startBatchLoad(fileNames) {
  if (batchTimer) clearTimeout(batchTimer)
  let offset = 0
  async function loadNextBatch() {
    const batch = fileNames.slice(offset, offset + BATCH_SIZE)
    if (!batch.length) return
    try {
      const res = await api.batchMusicId3({ file_path: filePath.value, file_names: batch })
      if (res.data) {
        // Merge metadata into musicList
        const metaMap = {}
        res.data.forEach((m) => { metaMap[m.file_name] = m })
        musicList.value = musicList.value.map((row) => {
          const meta = metaMap[row.name]
          return meta ? { ...row, ...meta, _loaded: true } : row
        })
      }
    } catch { /* retry later? skip for now */ }
    offset += BATCH_SIZE
    if (offset < fileNames.length) {
      batchTimer = setTimeout(loadNextBatch, 50)
    }
  }
  loadNextBatch()
}

function goUpDir() {
  const parts = filePath.value.replace(/\/$/, '').split('/')
  parts.pop()
  filePath.value = parts.join('/') || '/'
  if (batchTimer) clearTimeout(batchTimer)
  loadFiles()
}

// -- Click file → load ID3 for single file --
async function onRowClick(row) {
  selectedKey.value = row.name
  loadingMeta.value = true
  const dirPath = row.file_path || filePath.value
  try {
    const res = await api.musicId3({ file_path: dirPath, file_name: row.name })
    if (res.data) {
      editing.value = { ...res.data, is_save_lyrics_file: false, is_save_album_cover: false }
      currentFileName = row.name
      currentFileFullPath = row.full_path || (dirPath.replace(/\/$/, '') + '/' + row.name)
      if (isMobile.value) mobileView.value = 'edit'
    }
  } catch { message.error('读取标签失败') }
  loadingMeta.value = false
}

async function saveTag() {
  saving.value = true
  try {
    const savePath = currentFileFullPath || (filePath.value.replace(/\/$/, '') + '/' + currentFileName)
    const res = await api.updateId3({
      music_id3_info: [{ file_full_path: savePath, ...editing.value }],
    })
    if (res.result === false || res.code) {
      message.error('保存失败: ' + (res.message || JSON.stringify(res)))
    } else {
      message.success('修改成功')
      if (isMobile.value) mobileView.value = 'file'
    }
  } catch { message.error('保存失败，网络错误') }
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

function applyOnlineMeta(item) {
  editing.value.title = item.name || editing.value.title
  editing.value.artist = item.artist || editing.value.artist
  editing.value.album = item.album || editing.value.album
  editing.value.year = item.year || editing.value.year
  editing.value.artwork = item.album_img || editing.value.artwork
  message.success('已应用在线元数据')
}

function doBatchAuto() {
  const selectData = musicList.value
    .filter((m) => checkedKeys.value.includes(m.name))
    .map((m) => ({ name: m.name, icon: 'icon-script-file' }))
  api.batchAutoUpdateId3({ file_full_path: filePath.value, select_data: selectData, music_info: { select_mode: batchMode.value, source_list: batchSources.value } })
  showBatchAuto.value = false
  // Open progress modal and start polling
  taskModal.value = { show: true, total: selectData.length, success: 0, failed: 0, pending: selectData.length, items: [] }
  startTaskPoll()
}

function startTaskPoll() {
  if (taskPollTimer) clearInterval(taskPollTimer)
  taskPollTimer = setInterval(async () => {
    try {
      const res = await api.getRecord({ parent_path: filePath.value.replace(/\/$/, '') })
      if (res.data) {
        const items = Array.isArray(res.data) ? res.data : (res.data.results || [])
        const success = items.filter((t) => t.state === 'success').length
        const failed = items.filter((t) => t.state === 'failed' || t.state === 'error').length
        const total = items.length || taskModal.value.total
        const pending = total - success - failed
        taskModal.value = { ...taskModal.value, items, total, success, failed, pending }
        // Stop polling when all done
        if (pending === 0 && total > 0) {
          clearInterval(taskPollTimer)
          taskPollTimer = null
          message.success('刮削完成')
        }
      }
    } catch { /* ignore poll errors */ }
  }, 2000)
}

const taskColumns = [
  { title: '歌曲', key: 'song_name', ellipsis: { tooltip: true }, width: 150 },
  {
    title: '状态', key: 'state', width: 70,
    render(row) {
      const map = { success: '✓', failed: '✗' }
      return h('span', { style: { color: row.state === 'success' ? '#18a058' : row.state === 'failed' ? '#d03050' : '#999' } }, map[row.state] || '...')
    },
  },
  { title: '信息', key: 'message', ellipsis: { tooltip: true }, width: 200 },
]

onBeforeUnmount(() => {
  if (taskPollTimer) clearInterval(taskPollTimer)
})

loadFiles()
</script>
