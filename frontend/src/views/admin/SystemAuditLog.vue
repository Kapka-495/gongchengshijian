<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="username" label="用户名" width="120"></el-table-column>
        <el-table-column prop="action" label="操作" width="100">
          <template slot-scope="scope">
            <el-tag :type="getTagType(scope.row.action)" size="small">{{ scope.row.action }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="resource" label="资源" width="120"></el-table-column>
        <el-table-column prop="detail" label="详情" min-width="200"></el-table-column>
        <el-table-column prop="ip" label="IP" width="140"></el-table-column>
        <el-table-column prop="time" label="时间" width="170"></el-table-column>
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
import { getAuditLogs } from '@/api'

export default {
  name: 'SystemAuditLog',
  components: { AppPageHeader },
  data() {
    return { list: [], total: 0, currentPage: 1, pageSize: 10, loading: false }
  },
  created() { this.fetchData() },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await getAuditLogs({ page: this.currentPage, size: this.pageSize })
        this.list = res.data.result; this.total = res.data.page.total
      } catch (_) {}
      this.loading = false
    },
    handlePageChange(page) { this.currentPage = page; this.fetchData() },
    getTagType(action) {
      const map = { '登录': 'success', '查询': 'info', '创建': 'primary', '上传': 'warning', '下载': 'info', '删除': 'danger', '修改': 'warning' }
      return map[action] || 'info'
    }
  }
}
</script>
