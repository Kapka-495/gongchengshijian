<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <p style="color:#606266">输入分子SMILES进行相似性搜索，查找结构相似的分子。</p>
      <el-form :inline="true" size="small">
        <el-form-item label="SMILES">
          <el-input v-model="smiles" placeholder="e.g. c1ccccc1" style="width:300px"></el-input>
        </el-form-item>
        <el-form-item :label="$t('molecule.type')">
          <el-select v-model="searchType" style="width:120px">
            <el-option label="2D 相似性" value="2d"></el-option>
            <el-option label="3D 相似性" value="3d"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="Threshold">
          <el-input-number v-model="threshold" :min="0" :max="1" :step="0.1" :precision="1"></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="doSearch">{{ $t('btn.search') }}</el-button>
        </el-form-item>
      </el-form>
      <!-- Results -->
      <el-table v-if="results.length" :data="results" stripe style="margin-top:16px">
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="formula" :label="$t('molecule.formula')" width="150">
          <template slot-scope="scope">
            <router-link :to="'/molecule-detail/' + scope.row.id" style="color:#1a4a80;font-weight:bold">{{ scope.row.formula }}</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="smiles" label="SMILES" width="200"></el-table-column>
        <el-table-column prop="mass" :label="$t('molecule.mass')" width="100"></el-table-column>
        <el-table-column prop="type" :label="$t('molecule.type')" width="140"></el-table-column>
        <el-table-column prop="similarity" label="Similarity" width="120">
          <template slot-scope="scope">
            <el-progress :percentage="Math.round(scope.row.similarity * 100)" :color="getColor(scope.row.similarity)"></el-progress>
          </template>
        </el-table-column>
        <el-table-column :label="$t('common.operation')" width="100">
          <template slot-scope="scope">
            <el-button type="text" @click="$router.push('/molecule-detail/' + scope.row.id)">{{ $t('molecule.detail') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-if="searched && !results.length" description="No similar molecules found"></el-empty>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { searchSimilarMolecules } from '@/api'

export default {
  name: 'MoleculeSimilarity',
  components: { AppPageHeader },
  data() {
    return {
      smiles: '', searchType: '2d', threshold: 0.7,
      results: [], loading: false, searched: false
    }
  },
  methods: {
    async doSearch() {
      if (!this.smiles.trim()) { this.$message.warning('请输入SMILES'); return }
      this.loading = true; this.searched = true
      try {
        const res = await searchSimilarMolecules({ smiles: this.smiles, type: this.searchType, threshold: this.threshold })
        this.results = res.data.result || []
      } catch (_) {}
      this.loading = false
    },
    getColor(val) {
      if (val >= 0.9) return '#67C23A'
      if (val >= 0.8) return '#409EFF'
      return '#E6A23C'
    }
  }
}
</script>
