<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-form :inline="true" size="small" class="search-form">
        <el-form-item :label="$t('common.keyword')">
          <el-input v-model="keyword" :placeholder="$t('common.pleaseInput')" clearable @keyup.enter.native="fetchData"></el-input>
        </el-form-item>
        <el-form-item :label="$t('material.type')">
          <el-select v-model="filterType" clearable :placeholder="$t('common.pleaseSelect')" @change="fetchData">
            <el-option label="金属表面" value="金属表面"></el-option>
            <el-option label="金属氧化物" value="金属氧化物"></el-option>
            <el-option label="二维材料" value="二维材料"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">{{ $t('btn.search') }}</el-button>
          <el-button @click="resetSearch">{{ $t('btn.reset') }}</el-button>
        </el-form-item>
      </el-form>
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" :label="$t('material.id')" width="80"></el-table-column>
        <el-table-column prop="name" :label="$t('material.name')" min-width="160">
          <template slot-scope="scope">
            <router-link :to="'/materials-detail/' + scope.row.id" style="color:#1a4a80;font-weight:bold">{{ scope.row.name }}</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="formula" :label="$t('molecule.formula')" width="120"></el-table-column>
        <el-table-column prop="type" :label="$t('material.type')" width="130">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="crystalSystem" label="晶系" width="100"></el-table-column>
        <el-table-column prop="spaceGroup" label="空间群" width="120"></el-table-column>
        <el-table-column prop="bandGap" label="带隙(eV)" width="100">
          <template slot-scope="scope">{{ scope.row.bandGap || '-' }}</template>
        </el-table-column>
        <el-table-column prop="tags" :label="$t('material.tags')" min-width="200">
          <template slot-scope="scope">
            <el-tag
              v-for="tag in scope.row.tags"
              :key="tag"
              size="mini"
              style="margin-right:4px;cursor:pointer"
              @click="handleTagClick(tag)"
            >{{ tag }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column :label="$t('common.operation')" width="100">
          <template slot-scope="scope">
            <el-button type="text" @click="$router.push('/materials-detail/' + scope.row.id)">{{ $t('material.detail') }}</el-button>
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
import { getMaterialsList } from '@/api'

export default {
  name: 'MaterialsList',
  components: { AppPageHeader },
  data() {
    return { list: [], total: 0, currentPage: 1, pageSize: 10, keyword: '', filterType: '', loading: false }
  },
  created() {
    if (this.$route.query.keyword) {
      this.keyword = this.$route.query.keyword
    }
    this.fetchData()
  },
  methods: {
    handleTagClick(tag) {
      this.keyword = tag
      this.currentPage = 1
      this.fetchData()
    },
    async fetchData() {
      this.loading = true
      try {
        const res = await getMaterialsList({ page: this.currentPage, size: this.pageSize, keyword: this.keyword, type: this.filterType })
        this.list = res.data.result; this.total = res.data.page.total
      } catch (_) {}
      this.loading = false
    },
    handlePageChange(page) { this.currentPage = page; this.fetchData() },
    resetSearch() { this.keyword = ''; this.filterType = ''; this.currentPage = 1; this.fetchData() }
  }
}
</script>
