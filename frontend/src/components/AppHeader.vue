<template>
  <div class="app-header-inner">
    <!-- Logo -->
    <div class="header-left">
      <div class="logo" @click="$router.push('/home')">
        <i class="el-icon-s-data" style="font-size:24px;margin-right:8px;color:#66b1ff"></i>
        <span class="logo-text">{{ $t('title.platform') }}</span>
      </div>
    </div>
    <!-- Nav Menu -->
    <div class="header-center">
      <el-menu
        mode="horizontal"
        :default-active="activeMenu"
        background-color="#1a4a80"
        text-color="#fff"
        active-text-color="#66b1ff"
        class="header-menu"
        @select="handleMenuSelect"
      >
        <el-menu-item index="/home">{{ $t('nav.home') }}</el-menu-item>
        <el-submenu index="data">
          <template slot="title">{{ $t('nav.molecule') }}/{{ $t('nav.materials') }}</template>
          <el-menu-item index="/molecule">{{ $t('molecule.list') }}</el-menu-item>
          <el-menu-item index="/materials">{{ $t('material.list') }}</el-menu-item>
          <el-menu-item index="/molecule-tags">{{ $t('molecule.tags') }}</el-menu-item>
          <el-menu-item index="/molecule-similarity">{{ $t('molecule.similarity') }}</el-menu-item>
          <el-menu-item index="/integration-materials">{{ $t('material.integration') }}</el-menu-item>
        </el-submenu>
        <el-menu-item index="/literature">{{ $t('nav.literature') }}</el-menu-item>
        <el-menu-item index="/api-info">{{ $t('nav.api') }}</el-menu-item>
        <el-submenu index="news">
          <template slot="title">{{ $t('nav.news') }}</template>
          <el-menu-item index="/newsList">{{ $t('news.newsCenter') }}</el-menu-item>
          <el-menu-item index="/announcementList">{{ $t('news.announcementCenter') }}</el-menu-item>
        </el-submenu>
        <el-menu-item index="/community">{{ $t('nav.community') }}</el-menu-item>
        <el-submenu index="admin" v-if="userInfo && userInfo.role === 'admin'">
          <template slot="title">{{ $t('nav.admin') }}</template>
          <el-menu-item index="/controlConsole">{{ $t('admin.controlConsole') }}</el-menu-item>
          <el-menu-item index="/metadata-manage">{{ $t('admin.metadataManage') }}</el-menu-item>
          <el-menu-item index="/tag-definition-manage">{{ $t('admin.tagDefinitionManage') }}</el-menu-item>
          <el-menu-item index="/permission-tag-definition-manage">{{ $t('admin.permissionTagManage') }}</el-menu-item>
          <el-menu-item index="/system-audit-log">{{ $t('admin.auditLog') }}</el-menu-item>
        </el-submenu>
      </el-menu>
    </div>
    <!-- Right -->
    <div class="header-right">
      <el-dropdown trigger="click" @command="handleLangChange">
        <span class="lang-switch">
          {{ lang === 'zh' ? '中文' : 'English' }} <i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="zh">中文</el-dropdown-item>
          <el-dropdown-item command="en">English</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
      <el-dropdown trigger="click" @command="handleUserCommand">
        <span class="user-info">
          <i class="el-icon-user-solid"></i>
          {{ userInfo ? userInfo.nickname || userInfo.username : 'User' }}
          <i class="el-icon-arrow-down el-icon--right"></i>
        </span>
        <el-dropdown-menu slot="dropdown">
          <el-dropdown-item command="profile">{{ $t('common.nickname') }}</el-dropdown-item>
          <el-dropdown-item command="password">{{ $t('auth.changePassword') }}</el-dropdown-item>
          <el-dropdown-item command="logout" divided>{{ $t('auth.logout') }}</el-dropdown-item>
        </el-dropdown-menu>
      </el-dropdown>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'AppHeader',
  data() {
    return {
      lang: localStorage.getItem('lang') || 'zh'
    }
  },
  computed: {
    ...mapState('user', ['userInfo']),
    activeMenu() {
      const path = this.$route.path
      if (path.includes('molecule')) return '/molecule'
      if (path.includes('materials') || path.includes('material') || path.includes('catalytic') || path.includes('integration')) return '/materials'
      if (path.includes('literature')) return '/literature'
      if (path.includes('api')) return '/api-info'
      if (path.includes('news')) return '/newsList'
      if (path.includes('announcement')) return '/announcementList'
      if (path.includes('community')) return '/community'
      if (path.includes('control') || path.includes('metadata') || path.includes('tag') || path.includes('audit') || path.includes('permission')) return 'admin'
      return '/home'
    }
  },
  methods: {
    handleMenuSelect(index) {
      this.$router.push(index)
    },
    handleLangChange(lang) {
      this.lang = lang
      this.$i18n.locale = lang
      localStorage.setItem('lang', lang)
    },
    handleUserCommand(command) {
      if (command === 'logout') {
        this.$store.dispatch('user/logout').then(() => {
          this.$message.success(this.$t('auth.logoutSuccess'))
          this.$router.push('/login')
        })
      } else if (command === 'password') {
        this.showChangePasswordDialog()
      } else if (command === 'profile') {
        this.showChangeNicknameDialog()
      }
    },
    showChangePasswordDialog() {
      this.$prompt(this.$t('auth.changePassword'), this.$t('auth.changePassword'), {
        confirmButtonText: this.$t('btn.confirm'),
        cancelButtonText: this.$t('btn.cancel'),
        inputType: 'password'
      }).then(({ value }) => {
        this.$message.success(this.$t('auth.changePasswordSuccess'))
      }).catch(() => {})
    },
    showChangeNicknameDialog() {
      this.$prompt(this.$t('common.nickname'), this.$t('Confirm change nickname'), {
        confirmButtonText: this.$t('btn.confirm'),
        cancelButtonText: this.$t('btn.cancel'),
        inputValue: this.userInfo ? this.userInfo.nickname : ''
      }).then(({ value }) => {
        if (this.userInfo) {
          this.userInfo.nickname = value
          this.$store.commit('user/SET_USER_INFO', { ...this.userInfo })
        }
        this.$message.success(this.$t('common.saveSuccess'))
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.app-header-inner {
  display: flex;
  align-items: center;
  height: 60px;
  padding: 0 20px;
}
.header-left {
  flex-shrink: 0;
}
.logo {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  white-space: nowrap;
}
.header-center {
  flex: 1;
  display: flex;
  justify-content: center;
}
.header-menu {
  border-bottom: none !important;
}
.header-menu .el-menu-item,
.header-menu .el-submenu .el-submenu__title {
  border-bottom: none !important;
}
.header-right {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  gap: 16px;
}
.lang-switch, .user-info {
  color: #fff;
  cursor: pointer;
  font-size: 14px;
}
.lang-switch:hover, .user-info:hover {
  color: #66b1ff;
}
</style>
