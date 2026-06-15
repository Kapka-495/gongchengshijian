<template>
  <div class="detail-page">
    <AppPageHeader />
    <el-card v-loading="loading">
      <template v-if="item">
        <h2 style="margin-top:0;color:#1a4a80">{{ item.title }}</h2>
        <div style="color:#909399;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #ebeef5">
          <p>{{ $t('literature.authorList') }}: {{ item.authors }}</p>
          <p>{{ $t('literature.journal') }}: {{ item.journal }}, {{ item.volume }}({{ item.issue }}), {{ item.pages }} ({{ item.year }})</p>
          <p>DOI: <a :href="'https://doi.org/' + item.doi" target="_blank">{{ item.doi }}</a></p>
        </div>
        <el-divider>{{ $t('literature.abstract') }}</el-divider>
        <div style="line-height:1.8;font-size:15px;color:#333">{{ item.abstract }}</div>
        <el-divider>{{ $t('literature.keywords') }}</el-divider>
        <div>
          <el-tag v-for="kw in item.keywords" :key="kw" style="margin:4px">{{ kw }}</el-tag>
        </div>
        <el-divider>关联标签</el-divider>
        <div>
          <el-tag v-for="tag in item.tags" :key="tag" style="margin:4px" type="success">{{ tag }}</el-tag>
        </div>
      </template>
      <el-empty v-else :description="$t('common.noData')"></el-empty>
      <div style="margin-top:20px">
        <el-button @click="$router.push('/literature')">{{ $t('btn.backToList') }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getLiteratureDetail } from '@/api'

export default {
  name: 'LiteratureDetail',
  components: { AppPageHeader },
  data() { return { item: null, loading: false } },
  created() { this.fetchDetail() },
  methods: {
    async fetchDetail() {
      this.loading = true
      try {
        const res = await getLiteratureDetail(this.$route.params.id)
        this.item = res.data
      } catch (_) {}
      this.loading = false
    }
  }
}
</script>
