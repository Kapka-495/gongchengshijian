<template>
  <div class="home-page">
    <!-- Stats Cards -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="stat in stats" :key="stat.label">
        <el-card shadow="hover" class="stat-card" @click.native="$router.push(stat.link)">
          <div class="stat-content">
            <div class="stat-icon" :style="{background: stat.color}">
              <i :class="stat.icon"></i>
            </div>
            <div class="stat-info">
              <div class="stat-number">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Charts Row -->
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="14">
        <el-card shadow="hover">
          <div slot="header">
            <span>{{ $t('molecule.dataTrend') }}</span>
          </div>
          <div ref="moleculeChart" style="height:320px"></div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover" class="announcement-panel">
          <div slot="header">
            <span>{{ $t('news.announcementCenter') }}</span>
            <el-button type="text" style="float:right;padding:3px 0" @click="$router.push('/announcementList')">{{ $t('btn.more') }} <i class="el-icon-arrow-right"></i></el-button>
          </div>
          <div class="announcement-list">
            <div v-for="item in announcements" :key="item.id" class="announcement-item" @click="$router.push('/announcementDetails/' + item.id)">
              <span class="ann-dot" :class="'importance-' + item.importance"></span>
              <span class="ann-title">{{ item.title }}</span>
              <span class="ann-date">{{ item.createTime }}</span>
            </div>
            <el-empty v-if="!announcements.length" :description="$t('common.noData')"></el-empty>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- Quick Links & News -->
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="14">
        <el-card shadow="hover">
          <div slot="header">
            <span>{{ $t('news.latestNews') }}</span>
            <el-button type="text" style="float:right;padding:3px 0" @click="$router.push('/newsList')">{{ $t('btn.more') }} <i class="el-icon-arrow-right"></i></el-button>
          </div>
          <div class="news-list">
            <div v-for="item in news" :key="item.id" class="news-item" @click="$router.push('/newsDetails/' + item.id)">
              <div class="news-title">{{ item.title }}</div>
              <div class="news-meta">{{ item.author }} · {{ item.createTime }}</div>
              <div class="news-summary">{{ item.summary }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card shadow="hover">
          <div slot="header"><span>快速入口</span></div>
          <div class="quick-links">
            <div class="quick-link" @click="$router.push('/molecule')">
              <i class="el-icon-search"></i>
              <span>{{ $t('molecule.dataList') }}</span>
            </div>
            <div class="quick-link" @click="$router.push('/molecule-similarity')">
              <i class="el-icon-connection"></i>
              <span>{{ $t('molecule.similarity') }}</span>
            </div>
            <div class="quick-link" @click="$router.push('/upload_data')">
              <i class="el-icon-upload2"></i>
              <span>{{ $t('upload.uploadData') }}</span>
            </div>
            <div class="quick-link" @click="$router.push('/api-info')">
              <i class="el-icon-document"></i>
              <span>{{ $t('title.apiInfo') }}</span>
            </div>
            <div class="quick-link" @click="$router.push('/literature')">
              <i class="el-icon-reading"></i>
              <span>{{ $t('title.literature') }}</span>
            </div>
            <div class="quick-link" @click="$router.push('/community')">
              <i class="el-icon-share"></i>
              <span>{{ $t('title.community') }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getNewsList, getAnnouncementList, getSummaryByCategory, getMaterialsList, getLiteratureList, getVisitorCount } from '@/api'

export default {
  name: 'Home',
  data() {
    return {
      stats: [
        { label: '分子数量', value: 0, icon: 'el-icon-s-data', color: '#409EFF', link: '/molecule' },
        { label: '材料数量', value: 0, icon: 'el-icon-s-grid', color: '#67C23A', link: '/materials' },
        { label: '文献数量', value: 0, icon: 'el-icon-document', color: '#E6A23C', link: '/literature' },
        { label: 'API调用次数', value: 0, icon: 'el-icon-connection', color: '#F56C6C', link: '/api-info' }
      ],
      statsLoading: false,
      news: [],
      announcements: [],
      chart: null
    }
  },
  mounted() {
    this.fetchStats()
    this.fetchNews()
    this.fetchAnnouncements()
  },
  methods: {
    async fetchStats() {
      this.statsLoading = true
      try {
        const [catRes, matRes, litRes, visitorRes] = await Promise.all([
          getSummaryByCategory(),
          getMaterialsList({ page: 1, size: 1 }),
          getLiteratureList({ page: 1, size: 1 }),
          getVisitorCount()
        ])
        // Total molecules from category summary
        const totalMolecules = catRes.data.reduce((sum, c) => sum + c.count, 0)
        const totalMaterials = matRes.data.page?.total || 0
        const totalLiterature = litRes.data.page?.total || 0
        const visitorCount = visitorRes.data || 0

        this.stats[0].value = totalMolecules
        this.stats[1].value = totalMaterials
        this.stats[2].value = totalLiterature
        this.stats[3].value = visitorCount

        // Init chart with category data
        this.$nextTick(() => this.initChart(catRes.data))
      } catch (_) {
        // Fallback to defaults
        this.stats[0].value = 12456
        this.stats[1].value = 5832
        this.stats[2].value = 3201
        this.stats[3].value = '1.2M+'
      }
      this.statsLoading = false
    },
    async fetchNews() {
      try {
        const res = await getNewsList({ page: 1, size: 4 })
        this.news = res.data.result || []
      } catch (_) { /* mock error handling */ }
    },
    async fetchAnnouncements() {
      try {
        const res = await getAnnouncementList({ page: 1, size: 5 })
        this.announcements = res.data.result || []
      } catch (_) { /* mock error handling */ }
    },
    initChart(categoryData) {
      if (!this.$refs.moleculeChart) return
      if (this.chart) { this.chart.dispose(); this.chart = null }
      this.chart = echarts.init(this.$refs.moleculeChart)
      const cats = categoryData ? categoryData.map(c => c.category) : ['无机小分子', '有机小分子', '芳香族化合物', '无机盐', '烯烃', '无机酸', '过渡金属配合物', '其他']
      const counts = categoryData ? categoryData.map(c => c.count) : [2341, 4521, 1876, 1203, 892, 523, 678, 422]
      this.chart.setOption({
        title: { text: this.$t('molecule.categoryDistribution'), left: 'center', top: 10, textStyle: { fontSize: 14, color: '#606266' } },
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { top: 50, bottom: 60, left: 60, right: 20 },
        xAxis: {
          type: 'category',
          data: cats,
          axisLabel: { rotate: 30, fontSize: 11 }
        },
        yAxis: { type: 'value', name: '数量' },
        series: [
          {
            name: '分子数量',
            type: 'bar',
            data: counts,
            itemStyle: { color: '#409EFF', borderRadius: [4, 4, 0, 0] },
            label: { show: true, position: 'top', fontSize: 10 }
          }
        ]
      })
      window.addEventListener('resize', () => this.chart && this.chart.resize())
    }
  },
  beforeDestroy() {
    if (this.chart) { this.chart.dispose(); this.chart = null }
  }
}
</script>

<style scoped>
.stats-row { margin-bottom: 0; }
.stat-card { cursor: pointer; transition: transform 0.2s; }
.stat-card:hover { transform: translateY(-2px); }
.stat-content { display: flex; align-items: center; gap: 16px; }
.stat-icon { width: 56px; height: 56px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 28px; color: #fff; }
.stat-number { font-size: 28px; font-weight: bold; color: #303133; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
.announcement-list { max-height: 320px; overflow-y: auto; }
.announcement-item { display: flex; align-items: center; padding: 10px 0; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
.announcement-item:hover { background: #f5f7fa; margin: 0 -20px; padding: 10px 20px; }
.ann-dot { width: 8px; height: 8px; border-radius: 50%; margin-right: 10px; flex-shrink: 0; }
.importance-high { background: #F56C6C; }
.importance-medium { background: #E6A23C; }
.importance-low { background: #67C23A; }
.ann-title { flex: 1; font-size: 14px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.ann-date { font-size: 12px; color: #999; margin-left: 12px; }
.news-list {}
.news-item { padding: 12px 0; border-bottom: 1px solid #f0f0f0; cursor: pointer; }
.news-item:last-child { border-bottom: none; }
.news-item:hover { background: #f5f7fa; margin: 0 -20px; padding: 12px 20px; }
.news-title { font-size: 15px; font-weight: 600; color: #303133; }
.news-meta { font-size: 12px; color: #999; margin: 4px 0; }
.news-summary { font-size: 13px; color: #606266; line-height: 1.5; }
.quick-links { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
.quick-link { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 12px; border: 1px solid #ebeef5; border-radius: 8px; cursor: pointer; transition: all 0.2s; color: #606266; }
.quick-link:hover { border-color: #1a4a80; color: #1a4a80; background: #f0f5ff; }
.quick-link i { font-size: 28px; margin-bottom: 8px; }
.quick-link span { font-size: 13px; }
</style>
