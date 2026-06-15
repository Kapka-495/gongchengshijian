<template>
  <div class="detail-page">
    <AppPageHeader />
    <el-card>
      <p style="color:#909399">催化详情页面 - 显示催化反应机理、活性位点、反应能垒等信息</p>
      <el-row :gutter="20">
        <el-col :span="12">
          <div ref="energyChart" style="height:350px"></div>
        </el-col>
        <el-col :span="12">
          <el-descriptions border size="small" title="催化体系信息">
            <el-descriptions-item label="催化类型">多相催化</el-descriptions-item>
            <el-descriptions-item label="活性位点">Metal site</el-descriptions-item>
            <el-descriptions-item label="反应类型">CO₂ 还原</el-descriptions-item>
            <el-descriptions-item label="能垒">0.85 eV</el-descriptions-item>
            <el-descriptions-item label="计算方法">DFT-PBE</el-descriptions-item>
            <el-descriptions-item label="温度">298 K</el-descriptions-item>
          </el-descriptions>
        </el-col>
      </el-row>
      <div style="margin-top:20px">
        <el-button @click="$router.push('/materials')">{{ $t('btn.backToList') }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import * as echarts from 'echarts'

export default {
  name: 'CatalyticDetail',
  components: { AppPageHeader },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.energyChart) {
        const chart = echarts.init(this.$refs.energyChart)
        chart.setOption({
          title: { text: '反应路径能垒图', left: 'center' },
          xAxis: { type: 'category', data: ['IS', 'TS1', 'IM', 'TS2', 'FS'] },
          yAxis: { type: 'value', name: 'Energy (eV)' },
          series: [{
            type: 'line', smooth: true,
            data: [0, 0.85, 0.32, 0.65, -0.45],
            markPoint: { data: [{ type: 'max', name: 'Max' }] },
            itemStyle: { color: '#409EFF' },
            areaStyle: { opacity: 0.15 }
          }]
        })
      }
    })
  }
}
</script>
