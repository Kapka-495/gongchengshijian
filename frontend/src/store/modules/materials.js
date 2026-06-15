const state = {
  list: [],
  total: 0,
  currentPage: 1,
  pageSize: 10,
  searchKeyword: ''
}

const mutations = {
  SET_LIST(state, { list, total }) {
    state.list = list
    state.total = total
  },
  SET_PAGE(state, page) {
    state.currentPage = page
  },
  SET_PAGE_SIZE(state, size) {
    state.pageSize = size
  },
  SET_SEARCH_KEYWORD(state, keyword) {
    state.searchKeyword = keyword
  },
  RESET_FILTERS(state) {
    state.searchKeyword = ''
    state.currentPage = 1
  }
}

const actions = {
  updateList({ commit }, { list, total }) {
    commit('SET_LIST', { list, total })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}
