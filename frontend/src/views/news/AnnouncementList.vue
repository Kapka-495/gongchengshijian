<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column type="index" width="60" :label="$t('common.id')"></el-table-column>
        <el-table-column :label="$t('common.title')" min-width="400">
          <template slot-scope="scope">
            <span class="importance-tag" :class="'importance-' + scope.row.importance"></span>
            <a @click="$router.push('/announcementDetails/' + scope.row.id)" style="color:#1a4a80;cursor:pointer">{{ scope.row.title }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="author" :label="$t('common.author')" width="120"></el-table-column>
        <el-table-column prop="createTime" :label="$t('common.createTime')" width="140"></el-table-column>
      </el-table>
      <el-pagination
        v-if="total > 0"
        style="margin-top:16px;text-align:right"
        :current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      ></el-pagination>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getAnnouncementList } from '@/api'

export default {
  name: 'AnnouncementList',
  components: { AppPageHeader },
  data() {
    return { list: [], total: 0, currentPage: 1, pageSize: 10, loading: false }
  },
  created() { this.fetchData() },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await getAnnouncementList({ page: this.currentPage, size: this.pageSize })
        this.list = res.data.result
        this.total = res.data.page.total
      } catch (_) {}
      this.loading = false
    },
    handlePageChange(page) { this.currentPage = page; this.fetchData() }
  }
}
</script>

<style scoped>
.importance-tag { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; vertical-align: middle; }
.importance-high { background: #F56C6C; }
.importance-medium { background: #E6A23C; }
.importance-low { background: #67C23A; }
</style>
