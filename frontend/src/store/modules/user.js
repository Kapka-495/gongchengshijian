import { login, register, getUserInfo, logout } from '@/api'

const state = {
  token: localStorage.getItem('token') || '',
  userInfo: JSON.parse(localStorage.getItem('userInfo') || 'null'),
  visitorCount: 0
}

const mutations = {
  SET_TOKEN(state, token) {
    state.token = token
    localStorage.setItem('token', token)
  },
  SET_USER_INFO(state, info) {
    state.userInfo = info
    localStorage.setItem('userInfo', JSON.stringify(info))
  },
  SET_VISITOR_COUNT(state, count) {
    state.visitorCount = count
  },
  CLEAR_AUTH(state) {
    state.token = ''
    state.userInfo = null
    localStorage.removeItem('token')
    localStorage.removeItem('userInfo')
  }
}

const actions = {
  async login({ commit }, credentials) {
    const res = await login(credentials)
    commit('SET_TOKEN', res.data.token)
    commit('SET_USER_INFO', res.data.userInfo)
    return res
  },
  async register({ commit }, data) {
    const res = await register(data)
    return res
  },
  async getUserInfo({ commit }) {
    const res = await getUserInfo()
    commit('SET_USER_INFO', res.data)
    return res
  },
  async logout({ commit }) {
    try { await logout() } catch (_) { /* ignore */ }
    commit('CLEAR_AUTH')
  },
  setVisitorCount({ commit }, count) {
    commit('SET_VISITOR_COUNT', count)
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
