<template>
  <div class="detail-page">
    <AppPageHeader />
    <el-card v-loading="loading">
      <div v-if="item">
        <h2 style="margin-top:0;color:#1a4a80">{{ item.title }}</h2>
        <div style="color:#999;font-size:13px;margin-bottom:20px;padding-bottom:16px;border-bottom:1px solid #ebeef5">
          {{ item.author }} · {{ item.createTime }}
        </div>
        <div class="content-body" v-html="item.content"></div>
      </div>
      <el-empty v-else :description="$t('common.noData')"></el-empty>
      <div style="margin-top:20px">
        <el-button @click="$router.push('/announcementList')">{{ $t('btn.backToList') }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getAnnouncementDetail } from '@/api'

export default {
  name: 'AnnouncementDetails',
  components: { AppPageHeader },
  data() { return { item: null, loading: false } },
  created() { this.fetchDetail() },
  methods: {
    async fetchDetail() {
      this.loading = true
      try {
        const res = await getAnnouncementDetail(this.$route.params.id)
        this.item = res.data
      } catch (_) {}
      this.loading = false
    }
  }
}
</script>
<style scoped>
.content-body { line-height: 1.8; font-size: 15px; color: #333; }
.content-body >>> p { margin: 12px 0; }
</style>
