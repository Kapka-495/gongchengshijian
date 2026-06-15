<template>
  <el-container class="default-layout">
    <!-- Header -->
    <el-header class="app-header" height="60px">
      <AppHeader />
    </el-header>
    <el-container class="main-container">
      <!-- Sidebar -->
      <el-aside :width="sidebarCollapsed ? '64px' : '220px'" class="app-sidebar-wrapper">
        <AppSidebar :collapsed="sidebarCollapsed" @toggle="toggleSidebar" />
      </el-aside>
      <!-- Main Content -->
      <el-main class="app-main">
        <AppBreadcrumb />
        <div class="app-content">
          <router-view />
        </div>
        <AppFooter />
      </el-main>
    </el-container>
    <!-- Intelligent Search Float -->
    <IntelligentSearch />
  </el-container>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'
import AppSidebar from '@/components/AppSidebar.vue'
import AppFooter from '@/components/AppFooter.vue'
import AppBreadcrumb from '@/components/AppBreadcrumb.vue'
import IntelligentSearch from '@/components/IntelligentSearch.vue'

export default {
  name: 'DefaultLayout',
  components: { AppHeader, AppSidebar, AppFooter, AppBreadcrumb, IntelligentSearch },
  data() {
    return { sidebarCollapsed: false }
  },
  methods: {
    toggleSidebar() {
      this.sidebarCollapsed = !this.sidebarCollapsed
    }
  }
}
</script>

<style scoped>
.default-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
}
.app-header {
  background: #1a4a80;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 100;
}
.main-container {
  flex: 1;
  overflow: hidden;
}
.app-sidebar-wrapper {
  background: #fff;
  border-right: 1px solid #e9ecef;
  transition: width 0.3s;
  overflow-x: hidden;
}
.app-main {
  background: #f8f9fa;
  padding: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}
.app-content {
  flex: 1;
  padding: 20px;
}
</style>
