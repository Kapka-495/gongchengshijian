<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-row :gutter="16">
        <el-col :span="6" v-for="tag in tags" :key="tag.id" style="margin-bottom:16px">
          <el-card shadow="hover" class="tag-card" @click.native="handleTagClick(tag)">
            <div class="tag-name">{{ tag.name }}</div>
            <div class="tag-count">{{ tag.count }} 个材料</div>
            <div class="tag-category">{{ tag.category }}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-if="!loading && !tags.length" :description="$t('common.noData')"></el-empty>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getMaterialTags } from '@/api'

export default {
  name: 'MaterialTags',
  components: { AppPageHeader },
  data() { return { tags: [], loading: false } },
  created() { this.fetchTags() },
  methods: {
    async fetchTags() {
      this.loading = true
      try {
        const res = await getMaterialTags()
        this.tags = res.data || []
      } catch (_) {}
      this.loading = false
    },
    handleTagClick(tag) {
      this.$router.push({ path: '/materials', query: { keyword: tag.name } })
    }
  }
}
</script>

<style scoped>
.tag-card { cursor: pointer; text-align: center; transition: transform 0.2s; }
.tag-card:hover { transform: translateY(-2px); }
.tag-name { font-size: 18px; font-weight: bold; color: #1a4a80; }
.tag-count { font-size: 24px; color: #67C23A; margin: 8px 0; }
.tag-category { font-size: 12px; color: #999; }
</style>
