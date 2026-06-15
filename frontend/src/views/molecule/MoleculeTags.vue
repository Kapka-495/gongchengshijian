<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-row :gutter="16">
        <el-col :span="6" v-for="tag in tags" :key="tag.id" style="margin-bottom:16px">
          <el-card shadow="hover" class="tag-card" @click.native="handleTagClick(tag)">
            <div class="tag-name">{{ tag.name }}</div>
            <div class="tag-count">{{ tag.count }} 个分子</div>
            <div class="tag-category">{{ tag.category }}</div>
          </el-card>
        </el-col>
      </el-row>
      <el-empty v-if="!loading && !tags.length" :description="$t('molecule.tagsLoadFail')"></el-empty>
    </el-card>
    <!-- Tag cloud visualization -->
    <el-card style="margin-top:20px">
      <div slot="header">标签云</div>
      <div ref="tagCloud" style="height:400px"></div>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import * as echarts from 'echarts'
import { getMoleculeTags } from '@/api'

export default {
  name: 'MoleculeTags',
  components: { AppPageHeader },
  data() {
    return { tags: [], loading: false }
  },
  created() { this.fetchTags() },
  methods: {
    async fetchTags() {
      this.loading = true
      try {
        const res = await getMoleculeTags()
        this.tags = res.data || []
        this.$nextTick(() => this.initTagCloud())
      } catch (_) {}
      this.loading = false
    },
    initTagCloud() {
      if (!this.$refs.tagCloud) return
      const chart = echarts.init(this.$refs.tagCloud)
      chart.setOption({
        series: [{
          type: 'wordCloud',
          shape: 'circle',
          sizeRange: [16, 48],
          rotationRange: [-45, 45],
          gridSize: 8,
          drawOutOfBound: false,
          textStyle: { fontFamily: 'sans-serif', fontWeight: 'bold', color: () => '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0').replace(/^[0-9a-f]{2}/, '2d5d') },
          data: this.tags.map(t => ({ name: t.name, value: t.count }))
        }]
      })
    },
    handleTagClick(tag) {
      this.$router.push({ path: '/molecule', query: { keyword: tag.name } })
    }
  }
}
</script>

<style scoped>
.tag-card { cursor: pointer; text-align: center; transition: transform 0.2s; }
.tag-card:hover { transform: translateY(-2px); }
.tag-name { font-size: 18px; font-weight: bold; color: #1a4a80; }
.tag-count { font-size: 24px; color: #409EFF; margin: 8px 0; }
.tag-category { font-size: 12px; color: #999; }
</style>
