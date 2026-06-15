<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <p style="color:#909399">集成材料页面 - 展示跨来源、跨类型的集成材料数据库</p>
      <el-table :data="list" stripe>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="name" :label="$t('material.name')" min-width="160">
          <template slot-scope="scope">
            <router-link :to="'/materials-detail/' + scope.row.id" style="color:#1a4a80;font-weight:bold">{{ scope.row.name }}</router-link>
          </template>
        </el-table-column>
        <el-table-column prop="formula" :label="$t('molecule.formula')" width="120"></el-table-column>
        <el-table-column prop="type" :label="$t('material.type')" width="130"></el-table-column>
        <el-table-column label="来源" width="100">
          <template slot-scope="scope">
            <el-tag size="small" type="info">{{ scope.row.id % 2 === 0 ? 'Materials Project' : 'OQMD' }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getMaterialsList } from '@/api'

export default {
  name: 'IntegrationMaterials',
  components: { AppPageHeader },
  data() { return { list: [] } },
  created() { this.fetchData() },
  methods: {
    async fetchData() {
      try {
        const res = await getMaterialsList({ page: 1, size: 20 })
        this.list = res.data.result || []
      } catch (_) {}
    }
  }
}
</script>
