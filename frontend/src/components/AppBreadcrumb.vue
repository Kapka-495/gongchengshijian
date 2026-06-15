<template>
  <div class="app-breadcrumb">
    <el-breadcrumb separator="/">
      <el-breadcrumb-item v-if="fromRoute && fromRoute.meta && fromRoute.meta.title">
        {{ $t('title.currentPosition') }}：
        <a href="javascript:void(0)" @click="goBack">{{ $t(fromRoute.meta.title) }}</a>
      </el-breadcrumb-item>
      <el-breadcrumb-item v-for="(route, index) in matchedRoutes" :key="index">
        <router-link v-if="route.path && route.meta.title" :to="route.path">
          {{ $t(route.meta.title) }}
        </router-link>
        <span v-else>{{ $t(route.meta.title || 'title.home') }}</span>
      </el-breadcrumb-item>
    </el-breadcrumb>
  </div>
</template>

<script>
export default {
  name: 'AppBreadcrumb',
  data() {
    return {
      matchedRoutes: [],
      fromRoute: null
    }
  },
  created() { this.updateBreadcrumbs() },
  watch: {
    $route: { deep: true, handler: 'updateBreadcrumbs' }
  },
  methods: {
    updateBreadcrumbs() {
      const { matched, meta } = this.$route
      this.matchedRoutes = matched.filter(r => r.meta && r.meta.title)
      this.fromRoute = meta.fromRoute || null
    },
    goBack() {
      if (this.fromRoute && this.fromRoute.path) {
        this.$router.push(this.fromRoute.path)
      } else {
        this.$router.back()
      }
    }
  }
}
</script>

<style scoped>
.app-breadcrumb {
  padding: 12px 20px;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
}
</style>
