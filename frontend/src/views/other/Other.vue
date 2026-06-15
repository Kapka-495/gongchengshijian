<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <p style="color:#909399">其他功能和页面</p>
      <el-row :gutter="16">
        <el-col :span="8">
          <el-card shadow="hover">
            <div slot="header">{{ $t('filter.period') }}</div>
            <el-radio-group v-model="timeFilter" size="small">
              <el-radio-button label="thisYear">{{ $t('filter.thisYear') }}</el-radio-button>
              <el-radio-button label="threeYears">{{ $t('filter.threeYears') }}</el-radio-button>
              <el-radio-button label="fiveYears">{{ $t('filter.fiveYears') }}</el-radio-button>
              <el-radio-button label="tenYears">{{ $t('filter.tenYears') }}</el-radio-button>
              <el-radio-button label="all">{{ $t('filter.all') }}</el-radio-button>
            </el-radio-group>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover">
            <div slot="header">元素搜索</div>
            <el-checkbox-group v-model="selectedElements" size="small">
              <el-checkbox label="H">H</el-checkbox>
              <el-checkbox label="C">C</el-checkbox>
              <el-checkbox label="O">O</el-checkbox>
              <el-checkbox label="N">N</el-checkbox>
              <el-checkbox label="Fe">Fe</el-checkbox>
              <el-checkbox label="Cu">Cu</el-checkbox>
              <el-checkbox label="Pt">Pt</el-checkbox>
              <el-checkbox label="Au">Au</el-checkbox>
            </el-checkbox-group>
            <el-checkbox style="margin-top:12px" v-model="includeExtra">{{ $t('filter.includeExtraElements') }}</el-checkbox>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover">
            <div slot="header">搜索类型</div>
            <el-radio-group v-model="searchMode" size="small">
              <el-radio label="onlyElements">{{ $t('filter.onlySpecifiedElements') }}</el-radio>
              <el-radio label="onlyRelated">{{ $t('filter.onlyRelatedElements') }}</el-radio>
              <el-radio label="anySmiles">{{ $t('filter.anySmilesSearch') }}</el-radio>
            </el-radio-group>
            <el-divider></el-divider>
            <el-radio-group v-model="similarityMode" size="small">
              <el-radio label="high3d">{{ $t('filter.high3DLowSim') }}</el-radio>
              <el-radio label="highSim">{{ $t('filter.highSimLow3D') }}</el-radio>
            </el-radio-group>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'

export default {
  name: 'Other',
  components: { AppPageHeader },
  data() {
    return {
      timeFilter: 'all',
      selectedElements: ['H', 'C', 'O'],
      includeExtra: false,
      searchMode: 'onlyElements',
      similarityMode: 'high3d'
    }
  }
}
</script>
