import axios from 'axios'
import { getToken, clearAuth } from './auth'
import { Message } from 'element-ui'
import router from '@/router'

const service = axios.create({
  baseURL: '/pichemdata/api/v1',
  timeout: 15000
})

// Request interceptor
service.interceptors.request.use(
  config => {
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Response interceptor
service.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code === 403 || res.code === 401) {
      // 开发阶段仅拒绝请求，不清除登录态（避免 mock 登录被踢）
      return Promise.reject(new Error(res.msg || 'Auth failed'))
    }
    if (res.code !== 200) {
      Message.error(res.msg || 'Request failed')
      return Promise.reject(new Error(res.msg || 'Error'))
    }
    return res
  },
  error => {
    Message.error(error.message || 'Network error')
    return Promise.reject(error)
  }
)

export default service
