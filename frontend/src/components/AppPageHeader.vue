<template>
  <div class="app-page-header">
    <el-page-header :content="$t(metaTitle)" @back="handleBack">
      <template slot="content">
        <span>{{ $t(metaTitle) }}</span>
      </template>
    </el-page-header>
  </div>
</template>

<script>
export default {
  name: 'AppPageHeader',
  computed: {
    metaTitle() {
      return this.$route.meta && this.$route.meta.title ? this.$route.meta.title : 'title.home'
    }
  },
  methods: {
    handleBack() {
      this.$router.back()
    }
  }
}
</script>

<style scoped>
.app-page-header {
  margin-bottom: 16px;
}
</style>
