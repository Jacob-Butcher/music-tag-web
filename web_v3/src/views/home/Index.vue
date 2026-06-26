<template>
  <div :style="layoutStyle">
    <!-- File Browser -->
    <div v-show="!isMobile || mobileView === 'file'" :style="panelStyle('480px')">
      <FileBrowser
        :file-path="filePath"
        :music-list="musicList"
        :checked-keys="checkedKeys"
        :selected-key="selectedKey"
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
        @search-resource="searchResource"
        @back="mobileView = 'file'"
      />
    </div>

    <!-- Resource Search -->
    <div v-show="!isMobile || mobileView === 'resource'" :style="panelStyle('450px')">
      <ResourcePanel
        :is-mobile="isMobile"
        :results="searchResults"
        @apply="applyResult"
        @back="mobileView = 'edit'"
      />
    </div>

    <!-- Auto-batch modal -->
    <n-modal v-model:show="showBatchAuto" title="批量自动刮削" preset="card" style="width: 400px;">
      <n-space vertical>
        <n-radio-group v-model:value="batchMode">
          <n-radio value="hard">严格模式</n-radio>
          <n-radio value="simple">宽松模式</n-radio>
        </n-radio-group>
        <n-select
          v-model:value="batchSources"
          multiple
          placeholder="音乐源"
          :options="sourceOptions"
        />
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
import ResourcePanel from '@/components/home/ResourcePanel.vue'

const message = useMessage()
const { isMobile } = useMobile()

// --- State ---
const mobileView = ref('file')
const filePath = ref('/app/media/')
const musicList = ref([])
const checkedKeys = ref([])
const selectedKey = ref('')
const editing = ref({})
const manualEdit = ref({})
const saving = ref(false)
const searchResults = ref([])
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

// --- Layout ---
const layoutStyle = computed(() =>
  isMobile.value
    ? { display: 'flex', flexDirection: 'column', height: '100%' }
    : { display: 'flex', gap: '12px', height: '100%' }
)

function panelStyle(flexVal) {
  if (isMobile.value) return { flex: 1, overflow: 'auto' }
  return {
    width: flexVal === '1' ? undefined : flexVal,
    minWidth: flexVal === '1' ? undefined : '300px',
    flex: flexVal === '1' ? 1 : undefined,
    overflow: 'auto',
  }
}

// --- File operations ---
async function loadFiles() {
  try {
    const res = await api.batchMusicList({ file_path: filePath.value, sorted_fields: [] })
    if (res.data) {
      musicList.value = res.data
    }
  } catch {
    message.error('加载文件失败')
  }
}

function goUpDir() {
  const parts = filePath.value.replace(/\/$/, '').split('/')
  parts.pop()
  filePath.value = parts.join('/') || '/'
  loadFiles()
}

function onRowClick(row) {
  selectedKey.value = row.file_name
  editing.value = { ...row, is_save_lyrics_file: false, is_save_album_cover: false }
  currentFileName = row.file_name
  if (isMobile.value) mobileView.value = 'edit'
}

// --- Tag operations ---
async function saveTag() {
  saving.value = true
  try {
    await api.updateId3({
      music_id3_info: [{ file_full_path: filePath.value.replace(/\/$/, '') + '/' + currentFileName, ...editing.value }],
    })
    message.success('修改成功')
    if (isMobile.value) mobileView.value = 'file'
  } catch {
    message.error('保存失败')
  }
  saving.value = false
}

async function batchSave() {
  try {
    const selectData = musicList.value
      .filter((m) => checkedKeys.value.includes(m.file_name))
      .map((m) => ({ name: m.file_name, icon: 'icon-script-file' }))
    await api.batchUpdateId3({
      file_full_path: filePath.value,
      select_data: selectData,
      music_info: manualEdit.value,
    })
    message.success('批量修改成功')
  } catch {
    message.error('修改失败')
  }
}

// --- Resource search ---
function searchResource() {
  if (!editing.value.title) {
    message.warning('请输入标题')
    return
  }
  api.fetchId3Title({ title: editing.value.title, resource: 'netease' }).then((res) => {
    searchResults.value = res.data || []
    if (isMobile.value) mobileView.value = 'resource'
  })
}

function applyResult(item) {
  editing.value.title = item.name
  editing.value.artist = item.artist
  editing.value.album = item.album
  editing.value.year = item.year
  editing.value.artwork = item.album_img
  if (isMobile.value) mobileView.value = 'edit'
}

function doBatchAuto() {
  const selectData = musicList.value
    .filter((m) => checkedKeys.value.includes(m.file_name))
    .map((m) => ({ name: m.file_name, icon: 'icon-script-file' }))
  api.batchAutoUpdateId3({
    file_full_path: filePath.value,
    select_data: selectData,
    music_info: { select_mode: batchMode.value, source_list: batchSources.value },
  })
  message.success('任务已创建')
  showBatchAuto.value = false
}

// Bootstrap
loadFiles()
</script>
