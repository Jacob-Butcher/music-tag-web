<template>
  <div :style="isMobile ? { display: 'flex', flexDirection: 'column', height: '100%' } : { display: 'flex', gap: '12px', height: '100%' }">
    <!-- File Browser -->
    <div v-show="!isMobile || mobileView === 'file'" :style="isMobile ? { flex: 1, overflow: 'auto' } : { width: '380px', minWidth: '300px', overflow: 'auto' }">
      <n-card :bordered="false" size="small" style="border-radius: 12px; height: 100%;">
        <n-space vertical :size="8">
          <!-- Path input -->
          <n-space :size="4" align="center">
            <n-button text @click="goUpDir" :disabled="filePath === '/'"><n-icon size="20"><ArrowUndo /></n-icon></n-button>
            <n-input v-model:value="filePath" size="small" placeholder="输入文件夹路径" @keyup.enter="loadFiles" />
            <n-button text @click="loadFiles"><n-icon size="20"><ArrowDown /></n-icon></n-button>
          </n-space>
          <!-- File tree -->
          <n-tree v-if="treeData.length"
            :data="treeData" :node-key="(node) => node.key"
            :virtual-scroll="false"
            block-line
            @update:selected-keys="onNodeSelect"
            @update:checked-keys="onNodeCheck"
            checkable
            :checked-keys="checkedKeys"
          />
          <div v-else style="padding: 40px; text-align: center; color: #999;">
            <n-icon size="40"><FolderOpenOutline /></n-icon>
            <p>点击上方输入文件夹路径</p>
          </div>
        </n-space>
      </n-card>
    </div>

    <!-- Edit Panel -->
    <div v-show="!isMobile || mobileView === 'edit'" :style="isMobile ? { flex: 1, overflow: 'auto', padding: '12px' } : { flex: 1, overflow: 'auto' }">
      <!-- Mobile header -->
      <div v-if="isMobile" style="display: flex; align-items: center; padding: 4px 0 12px;">
        <n-button text @click="mobileView = 'file'"><n-icon size="22"><ChevronBack /></n-icon></n-button>
        <span style="flex:1; text-align:center; font-weight:600;">{{ editing.title || editing.filename || '编辑' }}</span>
        <n-button text @click="searchResource"><n-icon size="22"><Search /></n-icon></n-button>
      </div>

      <n-card :bordered="false" size="small" style="border-radius: 12px;">
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
            <n-button type="primary" block round :loading="saving" @click="saveTag" style="height: 48px;">
              保存信息
            </n-button>
          </n-space>
        </template>
        <template v-else>
          <n-space vertical :size="12">
            <n-alert type="info">已选择 {{ checkedKeys.length }} 个文件</n-alert>
            <n-input v-model:value="manualEdit.title" placeholder="批量设置标题 (支持变量 ${title}, ${album})" />
            <n-input v-model:value="manualEdit.artist" placeholder="批量设置艺术家" />
            <n-input v-model:value="manualEdit.album" placeholder="批量设置专辑" />
            <n-button type="primary" block round @click="batchSave" style="height: 48px;">手动修改</n-button>
            <n-button type="warning" block round @click="showBatchAuto = true" style="height: 48px;">自动刮削</n-button>
          </n-space>
        </template>
      </n-card>
    </div>

    <!-- Resource Panel -->
    <div v-show="!isMobile || mobileView === 'resource'" :style="isMobile ? { flex: 1, overflow: 'auto', padding: '12px' } : { width: '450px', overflow: 'auto' }">
      <div v-if="isMobile" style="display: flex; align-items: center; padding: 4px 0 12px;">
        <n-button text @click="mobileView = 'edit'"><n-icon size="22"><ChevronBack /></n-icon></n-button>
        <span style="flex:1; text-align:center; font-weight:600;">搜索结果</span>
      </div>
      <n-card :bordered="false" size="small" style="border-radius: 12px;">
        <div v-if="searchResults.length > 0">
          <div v-for="(item, i) in searchResults" :key="i"
            style="display: flex; align-items: center; padding: 8px; border-bottom: 1px solid #f0f0f0; cursor: pointer;"
            @click="applyResult(item)">
            <n-image v-if="item.album_img" :src="item.album_img" width="48" height="48" style="border-radius: 6px; margin-right: 10px;" preview-disabled />
            <div style="flex: 1; overflow: hidden;">
              <div style="font-size: 13px; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{{ item.name }}</div>
              <div style="font-size: 12px; color: #999;">{{ item.artist }} · {{ item.album }}</div>
            </div>
            <n-tag size="small" v-if="item.year">{{ item.year }}</n-tag>
          </div>
        </div>
        <div v-else style="padding: 40px; text-align: center; color: #999;">
          <n-icon size="40"><Search /></n-icon>
          <p>点击标签页的 🔍 搜索资源</p>
        </div>
      </n-card>
    </div>

    <!-- Auto-batch dialog -->
    <n-modal v-model:show="showBatchAuto" title="批量自动刮削" preset="card" style="width: 400px;">
      <n-space vertical>
        <n-radio-group v-model:value="batchMode">
          <n-radio value="hard">严格模式</n-radio>
          <n-radio value="simple">宽松模式</n-radio>
        </n-radio-group>
        <n-select v-model:value="batchSources" multiple placeholder="音乐源" :options="[
          {label:'网易云',value:'netease'},{label:'咪咕',value:'migu'},{label:'QQ音乐',value:'qmusic'},{label:'酷狗',value:'kugou'}
        ]" />
      </n-space>
      <template #footer><n-button type="primary" round block @click="doBatchAuto">开始刮削</n-button></template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useMessage } from 'naive-ui'
import { ArrowUndo, ArrowDown, ChevronBack, Search, FolderOpenOutline } from '@vicons/ionicons5'
import api from '@/api'

const router = useRouter()
const message = useMessage()
const isMobile = ref(window.innerWidth < 768)
const mobileView = ref('file')
const filePath = ref('/app/media/')
const treeData = ref([])
const checkedKeys = ref([])
const checkedData = ref([])
const editing = ref({})
const manualEdit = ref({})
const saving = ref(false)
const searchResults = ref([])
const showBatchAuto = ref(false)
const batchMode = ref('hard')
const batchSources = ref([])
let currentFileName = ''

onMounted(() => {
  isMobile.value = window.innerWidth < 768
  loadFiles()
})

async function loadFiles() {
  try {
    const res = await api.fileList({ file_path: filePath.value, sorted_fields: [] })
    if (res.data) {
      treeData.value = res.data.map((node, i) => formatNode(node, `${i}-`))
    }
  } catch (e) {
    message.error('加载文件失败')
  }
}

function formatNode(node, prefix) {
  const key = prefix + (node.name || '')
  return {
    key,
    label: node.title || node.name,
    isLeaf: node.icon !== 'icon-folder',
    ...(node.children ? { children: node.children.map((c, i) => formatNode(c, key + '-' + i)) } : {}),
  }
}

function goUpDir() {
  const parts = filePath.value.replace(/\/$/, '').split('/')
  parts.pop()
  filePath.value = parts.join('/') || '/'
  loadFiles()
}

function onNodeSelect(keys) {
  const key = keys[0]
  if (key) {
    // extract file name from key and load ID3
    const path = filePath.value.replace(/\/$/, '') + '/' + key.split('-').pop()
    loadMusicInfo(path, key.split('-').pop())
  }
}

async function loadMusicInfo(fullPath, fileName) {
  try {
    const res = await api.musicId3({ file_path: filePath.value, file_name: fileName })
    if (res.data) {
      editing.value = { ...res.data, is_save_lyrics_file: false, is_save_album_cover: false }
      currentFileName = fileName
      if (isMobile.value) mobileView.value = 'edit'
    }
  } catch (e) { message.error('读取标签失败') }
}

function onNodeCheck(keys) {
  checkedKeys.value = keys
  if (isMobile.value && keys.length > 0) mobileView.value = 'edit'
}

async function saveTag() {
  saving.value = true
  try {
    await api.updateId3({ music_id3_info: [{ file_full_path: filePath.value + '/' + currentFileName, ...editing.value }] })
    message.success('修改成功')
    if (isMobile.value) mobileView.value = 'file'
  } catch (e) { message.error('保存失败') }
  saving.value = false
}

async function batchSave() {
  try {
    await api.batchUpdateId3({ file_full_path: filePath.value, select_data: checkedData.value, music_info: manualEdit.value })
    message.success('批量修改成功')
  } catch (e) { message.error('修改失败') }
}

function searchResource() {
  if (!editing.value.title) { message.warning('请输入标题'); return }
  api.fetchId3Title({ title: editing.value.title, resource: 'netease' }).then(res => {
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
  api.batchAutoUpdateId3({ file_full_path: filePath.value, select_data: checkedData.value, music_info: { select_mode: batchMode.value, source_list: batchSources.value } })
  message.success('任务已创建')
  showBatchAuto.value = false
}
</script>
