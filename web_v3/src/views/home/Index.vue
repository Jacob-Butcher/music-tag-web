<template>
  <div :style="layoutStyle">
    <!-- File Browser -->
    <div v-show="!isMobile || mobileView === 'file'" :style="panelStyle('1')">
      <FileBrowser
        :music-list="musicList"
        :checked-keys="checkedKeys"
        @update:checked-keys="(v) => checkedKeys = v"
        @row-click="onRowClick"
        @search="onSearch"
        @clear-search="loadFiles"
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
        @show-progress="showTaskPanel = true"
        @apply-meta="(item, source) => applyOnlineMeta(item, source)"
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

    <!-- Task history button + panel (top-right) -->
    <n-button v-if="taskModal.items.length || taskPollTimer" size="small" round style="position:fixed;top:8px;right:8px;z-index:200;" @click="showTaskPanel = !showTaskPanel">
      <template #icon><n-icon size="16"><TimeOutline /></n-icon></template>
      刮削 {{ taskModal.success }}/{{ taskModal.total }}
      <span v-if="taskModal.pending"> ({{ taskModal.pending }})</span>
    </n-button>
    <div v-if="showTaskPanel && taskModal.items.length" class="task-panel">
      <div class="task-panel-header">
        <span>刮削记录</span>
        <n-button text size="tiny" @click="showTaskPanel = false">✕</n-button>
      </div>
      <div style="max-height:280px;overflow:auto;">
        <div v-for="t in taskModal.items" :key="t.full_path" style="display:flex;align-items:center;padding:3px 10px;font-size:11px;border-bottom:1px solid #f5f5f5;">
          <span :style="{color: t.state==='success'?'#18a058':t.state==='failed'?'#d03050':'#999',width:'16px',flexShrink:0}">{{ t.state==='success'?'✓':t.state==='failed'?'✗':'·' }}</span>
          <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ t.song_name || t.filename || '' }}</span>
          <span v-if="t.message" style="color:#d03050;font-size:10px;margin-left:4px;">{{ t.message }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.task-panel {
  position: fixed; top: 40px; right: 8px; width: 280px; z-index: 200;
  background: rgba(255,255,255,0.96); backdrop-filter: blur(10px);
  border-radius: 10px; box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  font-size: 12px; border: 1px solid #e8e8ed;
}
.task-panel-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 10px; font-weight: 500;
}
</style>

<script setup>
import { h, ref, computed, onBeforeUnmount } from 'vue'
import { useMessage } from 'naive-ui'
import { TimeOutline } from '@vicons/ionicons5'
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
const taskPaths = ref([])
const showTaskPanel = ref(false)
let taskPollTimer = null
let taskPollStart = 0
let pollErrors = 0
let currentFileName = ''
let currentFileFullPath = ''

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
  } catch (e) { message.error('读取标签失败: ' + (e.message || e)) }
  loadingMeta.value = false
}

async function saveTag() {
  saving.value = true
  try {
    const savePath = currentFileFullPath || (filePath.value.replace(/\/$/, '') + '/' + currentFileName)
    const payload = { file_full_path: savePath, ...editing.value }
    // Map artwork → album_img for backend
    if (payload.artwork && !payload.album_img) { payload.album_img = payload.artwork; delete payload.artwork }
    const res = await api.updateId3({
      music_id3_info: [payload],
    })
    const errCode = String(res.code || '')
    if (res.result === false || errCode.startsWith('4') || errCode.startsWith('5')) {
      message.error('保存失败: ' + (res.message || JSON.stringify(res)))
    } else {
      message.success('修改成功')
      // Update table row with saved metadata
      const idx = musicList.value.findIndex((m) => (m.full_path || (filePath.value.replace(/\/$/, '') + '/' + m.name)) === savePath)
      if (idx >= 0) {
        const saved = { ...editing.value, _loaded: true }
        musicList.value[idx] = { ...musicList.value[idx], title: saved.title, artist: saved.artist, album: saved.album, year: saved.year, artwork: saved.artwork, lyrics: saved.lyrics, _loaded: true }
      }
      if (isMobile.value) mobileView.value = 'file'
    }
  } catch (e) { message.error('保存失败: ' + (e.message || e)) }
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

async function applyOnlineMeta(item, source) {
  editing.value.title = item.name || editing.value.title
  editing.value.artist = item.artist || editing.value.artist
  editing.value.album = item.album || editing.value.album
  editing.value.year = item.year || editing.value.year
  editing.value.artwork = item.album_img || editing.value.artwork
  editing.value.album_img = item.album_img || editing.value.album_img
  // Fetch lyrics from the same source
  const songId = item.id || item.rid
  if (songId && source) {
    try {
      const lrcRes = await api.fetchLyric({ resource: source, song_id: String(songId) })
      if (lrcRes.data) editing.value.lyrics = lrcRes.data
    } catch { /* ignore */ }
  }
  message.success('已应用在线元数据')
}

function doBatchAuto() {
  const selectData = musicList.value
    .filter((m) => checkedKeys.value.includes(m.name))
    .map((m) => ({ name: m.name, icon: 'icon-script-file' }))
  api.batchAutoUpdateId3({ file_full_path: filePath.value, select_data: selectData, music_info: { select_mode: batchMode.value, source_list: batchSources.value } })
  showBatchAuto.value = false
  // Store selected paths and start polling
  taskPaths.value = musicList.value
    .filter((m) => checkedKeys.value.includes(m.name))
    .map((m) => filePath.value.replace(/\/$/, '') + '/' + m.name)
  taskModal.value = { show: true, total: selectData.length, success: 0, failed: 0, pending: selectData.length, items: [] }
  showTaskPanel.value = true
  taskPollStart = Date.now()
  startTaskPoll()
}

function startTaskPoll() {
  if (taskPollTimer) clearInterval(taskPollTimer)
  taskPollTimer = setInterval(async () => {
    try {
      const res = await api.getRecord({ full_path: filePath.value.replace(/\/$/, '') })
      if (res.data) {
        pollErrors = 0
        let items = Array.isArray(res.data) ? res.data : (res.data.results || [])
        // Filter to only selected files
        const pathSet = new Set(taskPaths.value)
        items = items.filter((t) => pathSet.has(t.full_path))
        const success = items.filter((t) => t.state === 'success').length
        const failed = items.filter((t) => t.state === 'failed' || t.state === 'error').length
        const total = taskPaths.value.length
        const pending = total - success - failed
        taskModal.value = { ...taskModal.value, items, total, success, failed, pending }
        if (pending === 0 && total > 0) {
          clearInterval(taskPollTimer)
          taskPollTimer = null
          message.success(`刮削完成: ${success} 成功, ${failed} 失败`)
        }
        // Timeout after 5 minutes
        if (Date.now() - taskPollStart > 300000) {
          clearInterval(taskPollTimer)
          taskPollTimer = null
          if (pending > 0) message.warning('刮削超时，部分文件未处理')
        }
      }
    } catch {
      pollErrors++
      if (pollErrors > 5) { clearInterval(taskPollTimer); taskPollTimer = null; message.error('刮削进度查询失败') }
    }
  }, 2000)
}

onBeforeUnmount(() => {
  if (taskPollTimer) clearInterval(taskPollTimer)
})

loadFiles()
</script>
