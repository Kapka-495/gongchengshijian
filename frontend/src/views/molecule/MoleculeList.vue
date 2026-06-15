<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <!-- Search Mode Tabs -->
      <el-tabs v-model="searchTab" @tab-click="onTabChange" class="search-tabs">
        <el-tab-pane :label="$t('spectrum.keywordSearch')" name="keyword"></el-tab-pane>
        <el-tab-pane :label="$t('spectrum.spectraTypeSearch')" name="spectra"></el-tab-pane>
      </el-tabs>

      <!-- Keyword Search Form -->
      <el-form v-show="searchTab === 'keyword'" :inline="true" size="small" class="search-form">
        <el-form-item :label="$t('common.keyword')">
          <el-input v-model="keyword" :placeholder="$t('common.pleaseInput') + $t('molecule.formula')" clearable @keyup.enter.native="fetchData"></el-input>
        </el-form-item>
        <el-form-item :label="$t('molecule.type')">
          <el-select v-model="filterType" clearable :placeholder="$t('common.pleaseSelect')" @change="fetchData">
            <el-option label="无机小分子" value="无机小分子"></el-option>
            <el-option label="有机小分子" value="有机小分子"></el-option>
            <el-option label="芳香族化合物" value="芳香族化合物"></el-option>
            <el-option label="无机盐" value="无机盐"></el-option>
            <el-option label="烯烃" value="烯烃"></el-option>
            <el-option label="无机酸" value="无机酸"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">{{ $t('btn.search') }}</el-button>
          <el-button @click="resetSearch">{{ $t('btn.reset') }}</el-button>
          <el-button type="success" @click="$router.push('/molecule-similarity')">{{ $t('molecule.similarity') }}</el-button>
          <el-button type="text" @click="showAdvanced = !showAdvanced">
            {{ $t('molecule.advancedSearch') }} <i :class="showAdvanced ? 'el-icon-arrow-up' : 'el-icon-arrow-down'"></i>
          </el-button>
        </el-form-item>
      </el-form>

      <!-- Advanced Search Panel -->
      <el-card v-show="searchTab === 'keyword' && showAdvanced" shadow="never" class="advanced-panel">
        <el-form :inline="true" size="small">
          <el-form-item :label="$t('molecule.formulaFilter')">
            <el-input v-model="searchFormula" placeholder="e.g. H2O" clearable style="width:130px"></el-input>
          </el-form-item>
          <el-form-item :label="$t('molecule.smilesFilter')">
            <el-input v-model="searchSmiles" placeholder="e.g. O" clearable style="width:150px"></el-input>
          </el-form-item>
          <el-form-item :label="$t('molecule.massRange')">
            <el-input-number v-model="massMin" :min="0" :precision="1" size="small" style="width:100px" :placeholder="$t('molecule.from')"></el-input-number>
            <span style="margin:0 4px;color:#909399">-</span>
            <el-input-number v-model="massMax" :min="0" :precision="1" size="small" style="width:100px" :placeholder="$t('molecule.to')"></el-input-number>
          </el-form-item>
          <el-form-item :label="$t('molecule.chargeFilter')">
            <el-input-number v-model="charge" :min="-10" :max="10" size="small" style="width:100px"></el-input-number>
          </el-form-item>
          <el-form-item :label="$t('molecule.spinFilter')">
            <el-input-number v-model="spin" :min="0" :max="10" size="small" style="width:100px"></el-input-number>
          </el-form-item>
        </el-form>
        <el-form :inline="true" size="small" style="margin-top:4px">
          <el-form-item :label="$t('molecule.tags')">
            <el-select v-model="selectedTags" multiple clearable filterable :placeholder="$t('common.pleaseSelect')" style="width:280px">
              <el-option v-for="t in tagOptions" :key="t.name" :label="t.name + ' (' + t.count + ')'" :value="t.name"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item :label="$t('molecule.sortBy')">
            <el-select v-model="sortField" clearable style="width:110px">
              <el-option label="ID" value="id"></el-option>
              <el-option :label="$t('molecule.mass')" value="mass"></el-option>
              <el-option :label="$t('molecule.formula')" value="formula"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-radio-group v-model="sortOrder" size="small">
              <el-radio-button label="asc">{{ $t('molecule.sortAsc') }}</el-radio-button>
              <el-radio-button label="desc">{{ $t('molecule.sortDesc') }}</el-radio-button>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" size="small" @click="fetchData">{{ $t('btn.search') }}</el-button>
            <el-button size="small" @click="clearAdvanced">{{ $t('btn.reset') }}</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- Spectrum Type Search Form -->
      <el-form v-show="searchTab === 'spectra'" :inline="true" size="small" class="search-form">
        <el-form-item :label="$t('spectrum.spectrumType')">
          <el-select v-model="spectraType" :placeholder="$t('common.pleaseSelect')" @change="fetchData">
            <el-option v-for="st in spectraTypeOptions" :key="st.type" :label="st.label + ' (' + st.count + ')'" :value="st.type"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="fetchData">{{ $t('btn.search') }}</el-button>
          <el-button @click="spectraType = ''; currentPage = 1; fetchData()">{{ $t('btn.reset') }}</el-button>
        </el-form-item>
      </el-form>

      <!-- Table -->
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column prop="id" :label="$t('molecule.id')" width="80"></el-table-column>
        <el-table-column prop="formula" :label="$t('molecule.formula')" width="150">
          <template slot-scope="scope">
            <router-link :to="'/molecule-detail/' + scope.row.id" style="color:#1a4a80;font-weight:bold">{{ scope.row.formula }}</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="smiles" label="SMILES" width="180"></el-table-column>
        <el-table-column prop="mass" :label="$t('molecule.mass')" width="100"></el-table-column>
        <el-table-column prop="type" :label="$t('molecule.type')" width="140">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.type }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="tags" :label="$t('molecule.tags')" min-width="200">
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
            <el-button type="text" @click="$router.push('/molecule-detail/' + scope.row.id)">{{ $t('molecule.detail') }}</el-button>
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
import { searchMoleculeCore, searchBySpectraType, getMoleculeTags } from '@/api'
import { mockSpectrumTypes } from '@/mock/data'

export default {
  name: 'MoleculeList',
  components: { AppPageHeader },
  data() {
    return {
      list: [], total: 0, currentPage: 1, pageSize: 10,
      keyword: '', filterType: '', loading: false,
      // Search mode
      searchTab: 'keyword',
      // Advanced search
      showAdvanced: false,
      searchFormula: '', searchSmiles: '',
      massMin: null, massMax: null,
      charge: null, spin: null,
      selectedTags: [], tagOptions: [],
      sortField: '', sortOrder: 'asc',
      // Spectrum type search
      spectraType: '',
      spectraTypeOptions: mockSpectrumTypes
    }
  },
  created() {
    // 从 URL query 中读取初始搜索关键词（支持从标签云页面跳转）
    if (this.$route.query.keyword) {
      this.keyword = this.$route.query.keyword
    }
    this.fetchTagOptions()
    this.fetchData()
  },
  methods: {
    handleTagClick(tag) {
      this.keyword = tag
      this.currentPage = 1
      this.fetchData()
    },
    async fetchTagOptions() {
      try {
        const res = await getMoleculeTags()
        this.tagOptions = res.data || []
      } catch (_) { this.tagOptions = [] }
    },
    async fetchData() {
      this.loading = true
      try {
        let res
        if (this.searchTab === 'spectra') {
          res = await searchBySpectraType({
            spectraType: this.spectraType,
            page: this.currentPage,
            size: this.pageSize
          })
        } else {
          res = await searchMoleculeCore({
            page: this.currentPage,
            size: this.pageSize,
            keyword: this.keyword,
            type: this.filterType,
            formula: this.searchFormula,
            smiles: this.searchSmiles,
            massMin: this.massMin,
            massMax: this.massMax,
            charge: this.charge,
            spin: this.spin,
            tags: this.selectedTags,
            sortField: this.sortField,
            sortOrder: this.sortOrder
          })
        }
        this.list = res.data.result
        this.total = res.data.page.total
      } catch (_) {}
      this.loading = false
    },
    handlePageChange(page) { this.currentPage = page; this.fetchData() },
    resetSearch() {
      this.keyword = ''; this.filterType = ''
      this.searchFormula = ''; this.searchSmiles = ''
      this.massMin = null; this.massMax = null
      this.charge = null; this.spin = null
      this.selectedTags = []; this.sortField = ''; this.sortOrder = 'asc'
      this.currentPage = 1
      this.fetchData()
    },
    clearAdvanced() {
      this.searchFormula = ''; this.searchSmiles = ''
      this.massMin = null; this.massMax = null
      this.charge = null; this.spin = null
      this.selectedTags = []; this.sortField = ''; this.sortOrder = 'asc'
      this.currentPage = 1
      this.fetchData()
    },
    onTabChange() {
      this.currentPage = 1
      this.spectraType = ''
      this.fetchData()
    }
  }
}
</script>

<style scoped>
.search-form { margin-bottom: 16px; }
.search-tabs { margin-top: -8px; }
.search-tabs >>> .el-tabs__header { margin-bottom: 12px; }
.advanced-panel {
  background: #fafbfc;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  margin-bottom: 16px;
  padding: 8px 16px 0 16px;
}
</style>
