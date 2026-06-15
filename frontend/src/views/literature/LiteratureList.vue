<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-form :inline="true" size="small" style="margin-bottom:16px">
        <el-form-item :label="$t('common.keyword')">
          <el-input v-model="keyword" :placeholder="$t('literature.doi') + ' / ' + $t('common.title')" clearable @keyup.enter.native="fetchData" style="width:300px"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">{{ $t('btn.search') }}</el-button>
          <el-button @click="keyword = ''; fetchData()">{{ $t('btn.reset') }}</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="title" :label="$t('literature.title')" min-width="300">
          <template slot-scope="scope">
            <router-link :to="'/literature-detail/' + scope.row.id" style="color:#1a4a80">{{ scope.row.title }}</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="authors" :label="$t('literature.authorList')" width="180"></el-table-column>
        <el-table-column prop="journal" :label="$t('literature.journal')" min-width="200"></el-table-column>
        <el-table-column prop="year" :label="$t('literature.year')" width="80"></el-table-column>
        <el-table-column label="DOI" width="180">
          <template slot-scope="scope">
            <a :href="'https://doi.org/' + scope.row.doi" target="_blank" style="font-size:12px;color:#409EFF">{{ scope.row.doi }}</a>
          </template>
        </el-table-column>
        <el-table-column :label="$t('common.operation')" width="100">
          <template slot-scope="scope">
            <el-button type="text" @click="$router.push('/literature-detail/' + scope.row.id)">{{ $t('literature.detail') }}</el-button>
          </template>
        </el-table-column>
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
import { getLiteratureList } from '@/api'

export default {
  name: 'LiteratureList',
  components: { AppPageHeader },
  data() {
    return { list: [], total: 0, currentPage: 1, pageSize: 10, keyword: '', loading: false }
  },
  created() { this.fetchData() },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await getLiteratureList({ page: this.currentPage, size: this.pageSize, keyword: this.keyword })
        this.list = res.data.result; this.total = res.data.page.total
      } catch (_) {}
      this.loading = false
    },
    handlePageChange(page) { this.currentPage = page; this.fetchData() }
  }
}
</script>
