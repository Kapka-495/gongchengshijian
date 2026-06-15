import Vue from 'vue'
import Vuex from 'vuex'
import user from './modules/user'
import molecule from './modules/molecule'
import materials from './modules/materials'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: {
    user,
    molecule,
    materials
  }
})
