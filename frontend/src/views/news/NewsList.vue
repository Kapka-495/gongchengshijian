<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-row :gutter="20" style="margin-bottom:16px">
        <el-col :span="8">
          <el-input v-model="keyword" :placeholder="$t('common.keyword')" clearable @clear="fetchData" @keyup.enter.native="fetchData">
            <el-button slot="append" icon="el-icon-search" @click="fetchData"></el-button>
          </el-input>
        </el-col>
      </el-row>
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column type="index" width="60" :label="$t('common.id')"></el-table-column>
        <el-table-column prop="title" :label="$t('common.title')" min-width="300">
          <template slot-scope="scope">
            <a @click="$router.push('/newsDetails/' + scope.row.id)" style="color:#1a4a80;cursor:pointer">{{ scope.row.title }}</a>
          </template>
        </el-table-column>
        <el-table-column prop="author" :label="$t('common.author')" width="120"></el-table-column>
        <el-table-column prop="createTime" :label="$t('common.createTime')" width="180"></el-table-column>
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
import { getNewsList } from '@/api'

export default {
  name: 'NewsList',
  components: { AppPageHeader },
  data() {
    return {
      list: [], total: 0, currentPage: 1, pageSize: 10,
      keyword: '', loading: false
    }
  },
  created() { this.fetchData() },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await getNewsList({ page: this.currentPage, size: this.pageSize, keyword: this.keyword })
        this.list = res.data.result
        this.total = res.data.page.total
      } catch (_) {}
      this.loading = false
    },
    handlePageChange(page) {
      this.currentPage = page
      this.fetchData()
    }
  }
}
</script>
