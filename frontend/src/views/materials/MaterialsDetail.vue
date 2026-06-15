<template>
  <div class="detail-page">
    <AppPageHeader />
    <el-card v-loading="loading">
      <template v-if="material">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-descriptions :column="2" border size="small">
              <el-descriptions-item :label="$t('material.id')">{{ material.id }}</el-descriptions-item>
              <el-descriptions-item :label="$t('material.name')"><strong>{{ material.name }}</strong></el-descriptions-item>
              <el-descriptions-item :label="$t('molecule.formula')">{{ material.formula }}</el-descriptions-item>
              <el-descriptions-item :label="$t('material.type')"><el-tag size="small">{{ material.type }}</el-tag></el-descriptions-item>
              <el-descriptions-item label="晶系">{{ material.crystalSystem }}</el-descriptions-item>
              <el-descriptions-item label="空间群">{{ material.spaceGroup }}</el-descriptions-item>
              <el-descriptions-item label="晶格常数">{{ material.latticeConstant }} Å</el-descriptions-item>
              <el-descriptions-item label="带隙">{{ material.bandGap ? material.bandGap + ' eV' : '-' }}</el-descriptions-item>
              <el-descriptions-item :label="$t('material.tags')" :span="2">
                <el-tag
                  v-for="tag in material.tags"
                  :key="tag"
                  size="mini"
                  style="margin-right:4px;cursor:pointer"
                  @click="$router.push({ path: '/materials', query: { keyword: tag } })"
                >{{ tag }}</el-tag>
              </el-descriptions-item>
            </el-descriptions>
          </el-col>
          <el-col :span="12">
            <div ref="structureViewer" style="height:300px;background:#f8f9fa;border:1px solid #ebeef5;border-radius:4px;display:flex;align-items:center;justify-content:center;color:#999;">
              材料结构可视化区域
            </div>
            <el-divider>关联分子</el-divider>
            <div>
              <el-tag v-for="mol in relatedMolecules" :key="mol.id" style="margin:4px;cursor:pointer" @click="$router.push('/molecule-detail/' + mol.id)">
                {{ mol.formula }}
              </el-tag>
              <el-empty v-if="!relatedMolecules.length" description="暂无关联分子"></el-empty>
            </div>
          </el-col>
        </el-row>
      </template>
      <el-empty v-else :description="$t('common.noData')"></el-empty>
      <div style="margin-top:20px">
        <el-button @click="$router.push('/materials')">{{ $t('btn.backToList') }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getMaterialsDetail } from '@/api'

export default {
  name: 'MaterialsDetail',
  components: { AppPageHeader },
  data() { return { material: null, relatedMolecules: [], loading: false } },
  created() { this.fetchDetail() },
  methods: {
    async fetchDetail() {
      this.loading = true
      try {
        const res = await getMaterialsDetail(this.$route.params.id)
        this.material = res.data
        // Mock related molecules
        this.relatedMolecules = [
          { id: 1, formula: 'H2O' },
          { id: 2, formula: 'CO2' },
          { id: 5, formula: 'CO2' }
        ]
      } catch (_) {}
      this.loading = false
    }
  }
}
</script>
