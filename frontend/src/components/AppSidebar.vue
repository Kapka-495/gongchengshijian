<template>
  <div class="app-sidebar">
    <div class="sidebar-toggle" @click="$emit('toggle')">
      <i :class="collapsed ? 'el-icon-s-unfold' : 'el-icon-s-fold'"></i>
    </div>
    <el-menu
      :default-active="activeMenu"
      :collapse="collapsed"
      :unique-opened="true"
      background-color="#fff"
      text-color="#333133"
      active-text-color="#1a4a80"
      router
      class="sidebar-menu"
    >
      <el-menu-item index="/home">
        <i class="el-icon-s-home"></i>
        <span slot="title">{{ $t('title.home') }}</span>
      </el-menu-item>

      <el-submenu index="molecule-group">
        <template slot="title">
          <i class="el-icon-s-data"></i>
          <span>{{ $t('title.molecule') }}</span>
        </template>
        <el-menu-item index="/molecule">{{ $t('molecule.dataList') }}</el-menu-item>
        <el-menu-item index="/molecule-tags">{{ $t('molecule.tags') }}</el-menu-item>
        <el-menu-item index="/molecule-similarity">{{ $t('molecule.similarity') }}</el-menu-item>
        <el-menu-item index="/molecule-detail-coalesce">{{ $t('title.moleculeDetailCoalesce') }}</el-menu-item>
      </el-submenu>

      <el-submenu index="materials-group">
        <template slot="title">
          <i class="el-icon-s-grid"></i>
          <span>{{ $t('title.materials') }}</span>
        </template>
        <el-menu-item index="/materials">{{ $t('material.list') }}</el-menu-item>
        <el-menu-item index="/material-tags">{{ $t('material.tags') }}</el-menu-item>
        <el-menu-item index="/integration-materials">{{ $t('material.integration') }}</el-menu-item>
      </el-submenu>

      <el-menu-item index="/literature">
        <i class="el-icon-document"></i>
        <span slot="title">{{ $t('title.literature') }}</span>
      </el-menu-item>

      <el-menu-item index="/xrd-tool">
        <i class="el-icon-data-line"></i>
        <span slot="title">{{ $t('title.xrdTool') }}</span>
      </el-menu-item>

      <el-menu-item index="/api-info">
        <i class="el-icon-connection"></i>
        <span slot="title">{{ $t('title.apiInfo') }}</span>
      </el-menu-item>

      <el-submenu index="news-group">
        <template slot="title">
          <i class="el-icon-bell"></i>
          <span>{{ $t('nav.news') }} & {{ $t('nav.announcement') }}</span>
        </template>
        <el-menu-item index="/newsList">{{ $t('news.newsCenter') }}</el-menu-item>
        <el-menu-item index="/announcementList">{{ $t('news.announcementCenter') }}</el-menu-item>
      </el-submenu>

      <el-menu-item index="/community">
        <i class="el-icon-share"></i>
        <span slot="title">{{ $t('title.community') }}</span>
      </el-menu-item>

      <el-menu-item index="/upload_data">
        <i class="el-icon-upload2"></i>
        <span slot="title">{{ $t('title.uploadData') }}</span>
      </el-menu-item>

      <el-submenu index="admin-group" v-if="userInfo && userInfo.role === 'admin'">
        <template slot="title">
          <i class="el-icon-setting"></i>
          <span>{{ $t('nav.admin') }}</span>
        </template>
        <el-menu-item index="/controlConsole">{{ $t('admin.controlConsole') }}</el-menu-item>
        <el-menu-item index="/metadata-manage">{{ $t('admin.metadataManage') }}</el-menu-item>
        <el-menu-item index="/tag-definition-manage">{{ $t('admin.tagDefinitionManage') }}</el-menu-item>
        <el-menu-item index="/permission-tag-definition-manage">{{ $t('admin.permissionTagManage') }}</el-menu-item>
        <el-menu-item index="/system-audit-log">{{ $t('admin.auditLog') }}</el-menu-item>
      </el-submenu>
    </el-menu>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'AppSidebar',
  props: {
    collapsed: { type: Boolean, default: false }
  },
  computed: {
    ...mapState('user', ['userInfo']),
    activeMenu() {
      return this.$route.path
    }
  }
}
</script>

<style scoped>
.app-sidebar {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.sidebar-toggle {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-bottom: 1px solid #ebeef5;
  color: #606266;
  font-size: 18px;
  transition: background 0.3s;
}
.sidebar-toggle:hover {
  background: #f5f7fa;
}
.sidebar-menu {
  flex: 1;
  border-right: none;
  overflow-y: auto;
}
.sidebar-menu:not(.el-menu--collapse) {
  width: 220px;
}
</style>
