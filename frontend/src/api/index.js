// ============================================================
// API Layer
// - USE_MOCK=false → 走真实后端，失败则弹窗提示并降级到 mock
// - USE_MOCK=true  → 直接走 mock，不发起网络请求
// - 登录 / 用户信息始终走 mock
// - XRD 始终走 Python 后端
// ============================================================

import { Message } from 'element-ui'
import request from '@/utils/request'
import {
  mockUsers, mockNews, mockAnnouncements,
  mockMolecules, mockMaterials, mockLiterature,
  mockMoleculeTags, mockMaterialTags,
  mockApiServices, mockAuditLogs, mockMetadata,
  mockSpectrum, mockCategorySummary, mockMoleculeSummary,
  mockObsFiles, generateAiResponse
} from '@/mock/data'

// ★ 后端就绪后改为 false
const USE_MOCK = false

// --- helpers ---
const delay = (ms = 300) => new Promise(resolve => setTimeout(resolve, ms))

function paginate(array, page = 1, size = 10) {
  const total = array.length
  const start = (page - 1) * size
  return { result: array.slice(start, start + size), page: { size, current: page, total } }
}

function ok(data) {
  return { code: 200, msg: null, data }
}

// 核心封装：真实调用失败 → 弹窗 + 降级到 mock
async function call(realFn, mockFn) {
  if (USE_MOCK) return mockFn()
  try {
    return await realFn()
  } catch (_e) {
    Message.error('该接口后端还未实现')
    return mockFn()
  }
}

// ==================== Auth (always mock) ====================

export async function login({ username, password }) {
  await delay()
  const user = mockUsers.find(u =>
    (u.username === username || u.email === username) && u.password === password
  )
  if (!user) throw new Error('用户名或密码错误')
  const { password: _, ...userInfo } = user
  return ok({ token: 'mock-token-' + user.id, userInfo })
}

export async function getUserInfo() {
  await delay()
  const raw = localStorage.getItem('userInfo')
  return ok(raw ? JSON.parse(raw) : null)
}

// ==================== Auth (real with fallback) ====================

export async function register(data) {
  return call(
    () => request.post('/auth/register', data),
    async () => { await delay(); return ok({ success: true }) }
  )
}

export async function logout() {
  return call(
    () => request.post('/auth/logout'),
    async () => { await delay(); return ok(null) }
  )
}

export async function getVisitorCount() {
  return call(
    () => request.get('/visitor-count'),
    async () => { await delay(100); return ok(23748) }
  )
}

export async function changePassword(data) {
  return call(
    () => request.post('/auth/change-password', data),
    async () => { await delay(); return ok({ success: true }) }
  )
}

// ==================== News ====================

export async function getNewsList({ page = 1, size = 10, keyword = '' } = {}) {
  return call(
    () => request.get('/news', { params: { page, size, keyword } }),
    async () => {
      await delay()
      let list = mockNews
      if (keyword) list = list.filter(n => n.title.includes(keyword) || n.summary.includes(keyword))
      return ok(paginate(list, page, size))
    }
  )
}

export async function getNewsDetail(id) {
  return call(
    () => request.get(`/news/${id}`),
    async () => { await delay(); return ok(mockNews.find(n => n.id === Number(id)) || null) }
  )
}

// ==================== Announcements ====================

export async function getAnnouncementList({ page = 1, size = 10 } = {}) {
  return call(
    () => request.get('/announcements', { params: { page, size } }),
    async () => { await delay(); return ok(paginate(mockAnnouncements, page, size)) }
  )
}

export async function getAnnouncementDetail(id) {
  return call(
    () => request.get(`/announcements/${id}`),
    async () => { await delay(); return ok(mockAnnouncements.find(n => n.id === Number(id)) || null) }
  )
}

// ==================== Molecule (basic) ====================

export async function getMoleculeList({ page = 1, size = 10, keyword = '', type = '' } = {}) {
  return call(
    () => request.get('/molecule/list', { params: { page, size, keyword, type } }),
    async () => {
      await delay()
      let list = mockMolecules
      if (keyword) list = list.filter(m => m.formula.includes(keyword) || m.smiles.includes(keyword) || m.tags.some(t => t.includes(keyword)))
      if (type) list = list.filter(m => m.type === type)
      return ok(paginate(list, page, size))
    }
  )
}

export async function getMoleculeDetail(id) {
  return call(
    () => request.get(`/molecule/detail/${id}`),
    async () => { await delay(); return ok(mockMolecules.find(m => m.id === Number(id)) || null) }
  )
}

export async function getMoleculeTags() {
  return call(
    () => request.get('/molecule/tags'),
    async () => { await delay(); return ok(mockMoleculeTags) }
  )
}

export async function searchSimilarMolecules({ smiles, type = '2d', threshold = 0.7 } = {}) {
  return call(
    () => request.post('/molecule/similarity', { smiles, type, threshold }),
    async () => {
      await delay(500)
      const results = mockMolecules.slice(0, 5).map((m, i) => ({ ...m, similarity: (0.95 - i * 0.08).toFixed(4) }))
      return ok({ result: results })
    }
  )
}

// ==================== Materials ====================

export async function getMaterialsList({ page = 1, size = 10, keyword = '', type = '' } = {}) {
  return call(
    () => request.get('/materials', { params: { page, size, keyword, type } }),
    async () => {
      await delay()
      let list = mockMaterials
      if (keyword) list = list.filter(m => m.name.includes(keyword) || m.formula.includes(keyword) || m.tags.some(t => t.includes(keyword)))
      if (type) list = list.filter(m => m.type === type)
      return ok(paginate(list, page, size))
    }
  )
}

export async function getMaterialsDetail(id) {
  return call(
    () => request.get(`/materials/${id}`),
    async () => { await delay(); return ok(mockMaterials.find(m => m.id === Number(id)) || null) }
  )
}

export async function getMaterialTags() {
  return call(
    () => request.get('/materials/tags'),
    async () => { await delay(); return ok(mockMaterialTags) }
  )
}

// ==================== Literature ====================

export async function getLiteratureList({ page = 1, size = 10, keyword = '' } = {}) {
  return call(
    () => request.get('/literature', { params: { page, size, keyword } }),
    async () => {
      await delay()
      let list = mockLiterature
      if (keyword) list = list.filter(l => l.title.includes(keyword) || l.authors.includes(keyword) || l.doi.includes(keyword))
      return ok(paginate(list, page, size))
    }
  )
}

export async function getLiteratureDetail(id) {
  return call(
    () => request.get(`/literature/${id}`),
    async () => { await delay(); return ok(mockLiterature.find(l => l.id === Number(id)) || null) }
  )
}

// ==================== API Info ====================

export async function getApiServices() {
  return call(
    () => request.get('/api-services'),
    async () => { await delay(); return ok(mockApiServices) }
  )
}

// ==================== Admin ====================

export async function getAuditLogs({ page = 1, size = 10 } = {}) {
  return call(
    () => request.get('/admin/audit-logs', { params: { page, size } }),
    async () => { await delay(); return ok(paginate(mockAuditLogs, page, size)) }
  )
}

export async function getMetadata({ page = 1, size = 10 } = {}) {
  return call(
    () => request.get('/admin/metadata', { params: { page, size } }),
    async () => { await delay(); return ok(paginate(mockMetadata, page, size)) }
  )
}

export async function saveMetadata(data) {
  return call(
    () => request.post('/admin/metadata', data),
    async () => { await delay(); return ok({ success: true, id: Date.now() }) }
  )
}

export async function deleteMetadata(id) {
  return call(
    () => request.delete(`/admin/metadata/${id}`),
    async () => { await delay(); return ok({ success: true }) }
  )
}

// ==================== Upload ====================

export async function uploadData(formData) {
  return call(
    () => request.post('/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
    async () => { await delay(1000); return ok({ success: true, fileId: Date.now() }) }
  )
}

// ==================== Molecule Open APIs ====================

export async function searchMoleculeCore(params = {}) {
  return call(
    () => request.post('/molecule/open/search/core', params),
    async () => {
      const {
        page = 1, size = 10, keyword = '', type = '', category = '',
        formula = '', smiles = '', inchi = '',
        massMin = null, massMax = null, charge = null, spin = null,
        tags = [], sortField = '', sortOrder = 'asc'
      } = params
      await delay()
      let list = [...mockMolecules]
      if (keyword) {
        const kw = keyword.toLowerCase()
        list = list.filter(m =>
          m.formula.toLowerCase().includes(kw) || m.smiles.toLowerCase().includes(kw) ||
          (m.inchi && m.inchi.toLowerCase().includes(kw)) || m.tags.some(t => t.toLowerCase().includes(kw))
        )
      }
      if (type) list = list.filter(m => m.type === type)
      if (category) list = list.filter(m => m.tags.some(t => t.includes(category)))
      if (formula) list = list.filter(m => m.formula.toLowerCase() === formula.toLowerCase())
      if (smiles) list = list.filter(m => m.smiles.toLowerCase() === smiles.toLowerCase())
      if (inchi) list = list.filter(m => m.inchi && m.inchi.toLowerCase().includes(inchi.toLowerCase()))
      if (massMin !== null && massMin !== '') list = list.filter(m => m.mass >= Number(massMin))
      if (massMax !== null && massMax !== '') list = list.filter(m => m.mass <= Number(massMax))
      if (charge !== null && charge !== '') list = list.filter(m => m.charge === Number(charge))
      if (spin !== null && spin !== '') list = list.filter(m => m.spin === Number(spin))
      if (tags && tags.length) list = list.filter(m => tags.some(t => m.tags.includes(t)))
      if (sortField) {
        list.sort((a, b) => {
          const va = a[sortField] ?? '', vb = b[sortField] ?? ''
          if (typeof va === 'number') return sortOrder === 'asc' ? va - vb : vb - va
          return sortOrder === 'asc' ? String(va).localeCompare(String(vb)) : String(vb).localeCompare(String(va))
        })
      }
      return ok(paginate(list, page, size))
    }
  )
}

export async function getMoleculeByPicId(picId) {
  return call(
    () => request.get(`/molecule/open/${picId}`),
    async () => { await delay(); return ok(mockMolecules.find(m => m.id === Number(picId)) || null) }
  )
}

export async function getSummaryByCategory() {
  return call(
    () => request.get('/molecule/open/summary/groupbycategory'),
    async () => { await delay(200); return ok(mockCategorySummary) }
  )
}

export async function getMoleculeSummary() {
  return call(
    () => request.get('/molecule/open/summary'),
    async () => { await delay(); return ok(mockMoleculeSummary) }
  )
}

export async function uploadMoleculeFile(formData) {
  return call(
    () => request.post('/molecule/open/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
    async () => {
      await delay(1200)
      const cnt = formData.getAll ? formData.getAll('files').length : (formData.get('files') ? 1 : 0)
      return ok({ success: true, uploadId: Date.now(), fileCount: cnt })
    }
  )
}

export async function getSpectrum(picId) {
  return call(
    () => request.get(`/molecule/open/spectrum/${picId}`),
    async () => {
      await delay(400)
      const entry = mockSpectrum.find(s => s.picId === Number(picId))
      return ok(entry ? entry.spectra : [])
    }
  )
}

export async function searchBySpectraType({ spectraType = '', page = 1, size = 10 } = {}) {
  return call(
    () => request.post('/molecule/open/search/by-spectra-type', { spectraType, page, size }),
    async () => {
      await delay(400)
      let results = []
      if (spectraType) {
        const picIds = mockSpectrum
          .filter(s => s.spectra.some(sp => sp.type === spectraType))
          .map(s => s.picId)
        results = mockMolecules.filter(m => picIds.includes(m.id))
      } else {
        results = [...mockMolecules]
      }
      return ok(paginate(results, page, size))
    }
  )
}

export async function uploadObsFile(formData) {
  return call(
    () => request.post('/molecule/open/obs-files', formData, { headers: { 'Content-Type': 'multipart/form-data' } }),
    async () => { await delay(1000); return ok({ success: true, fileId: 'obs-' + Date.now() }) }
  )
}

export async function downloadObsFile({ fileId } = {}) {
  return call(
    () => request.get('/molecule/open/obs-files/download', { params: { fileId } }),
    async () => {
      await delay(300)
      const file = mockObsFiles.find(f => f.id === fileId)
      if (!file) throw new Error('文件未找到')
      return ok({ ...file, downloadUrl: '#mock-download-' + fileId })
    }
  )
}

export async function streamObsFile({ fileId } = {}) {
  return call(
    () => request.get('/molecule/open/obs-files/stream', { params: { fileId } }),
    async () => {
      await delay(200)
      const file = mockObsFiles.find(f => f.id === fileId)
      if (!file) throw new Error('文件未找到')
      return ok({ ...file, previewContent: '[Binary content preview — mock mode]', previewType: 'text' })
    }
  )
}

// ==================== AI Chat ====================

export async function sendAiMessage({ message, history = [] } = {}) {
  return call(
    () => request.post('/ai/chat', { message, history }),
    async () => {
      await delay(600)
      if (!message || !message.trim()) throw new Error('消息不能为空')
      const response = generateAiResponse(message, mockCategorySummary)
      return ok({ reply: response.reply, actions: response.actions || [], timestamp: new Date().toISOString() })
    }
  )
}

// ==================== Community ====================

export async function getCommunityList({ page = 1, size = 10 } = {}) {
  return call(
    () => request.get('/community', { params: { page, size } }),
    async () => { await delay(); return ok(paginate(mockMoleculeTags, page, size)) }
  )
}

// ==================== XRD (always real) ====================

export async function xrdProcess({ data, min_angle = 5, max_angle = 90, step = 0.01, sigma = 0.1 } = {}) {
  try {
    const response = await fetch('/xrd-api/process', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ data, min_angle, max_angle, step, sigma })
    })
    if (!response.ok) {
      const err = await response.json().catch(() => ({}))
      throw new Error(err.detail || `XRD 处理失败: ${response.status}`)
    }
    return ok(await response.json())
  } catch (_e) {
    Message.error('该接口后端还未实现')
    return ok({ original: { angles: [], intensities: [] }, processed: { angles: [], intensities: [] } })
  }
}

export async function xrdProcessNpy(formData) {
  try {
    const response = await fetch('/xrd-api/process-npy', { method: 'POST', body: formData })
    if (!response.ok) {
      const err = await response.json().catch(() => ({}))
      throw new Error(err.detail || `XRD NPY 处理失败: ${response.status}`)
    }
    return ok(await response.json())
  } catch (_e) {
    Message.error('该接口后端还未实现')
    return ok({ original: { angles: [], intensities: [] }, processed: { angles: [], intensities: [] } })
  }
}
