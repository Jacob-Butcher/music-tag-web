import axios from 'axios'

const http = axios.create({
  baseURL: window.siteUrl || '/',
  withCredentials: true,
  timeout: 200000,
})

http.interceptors.request.use((config) => {
  config.headers['X-Requested-With'] = 'XMLHttpRequest'
  return config
})

http.interceptors.response.use(
  (response) => response.data,
  (error) => ({ code: 500, message: String(error), result: false })
)

const POST = (url, params) => http.post(url, params)
const GET = (url, params) => http.get(url, { params })

export default {
  fileList: (params) => POST('/api/file_list/', params),
  batchMusicId3: (params) => POST('/api/batch_music_id3/', params),
  musicId3: (params) => POST('/api/music_id3/', params),
  updateId3: (params) => POST('/api/update_id3/', params),
  batchUpdateId3: (params) => POST('/api/batch_update_id3/', params),
  batchAutoUpdateId3: (params) => POST('/api/batch_auto_update_id3/', params),
  tidyFolder: (params) => POST('/api/tidy_folder/', params),
  fetchId3Title: (params) => POST('/api/fetch_id3_by_title/', params),
  fetchLyric: (params) => POST('/api/fetch_lyric/', params),
  translationLyc: (params) => POST('/api/translation_lyc/', params),
  uploadImage: (params) => POST('/api/upload_image/', params),
  getRecord: (params) => GET('/api/record/', params),
}
