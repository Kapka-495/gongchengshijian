<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <p style="color:#909399">分子聚合详情页面 - 显示分子数据的聚合统计信息</p>
      <el-row :gutter="20">
        <el-col :span="12">
          <div ref="typeChart" style="height:300px"></div>
        </el-col>
        <el-col :span="12">
          <div ref="massChart" style="height:300px"></div>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import * as echarts from 'echarts'

export default {
  name: 'MoleculeDetailCoalesce',
  components: { AppPageHeader },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.typeChart) {
        const c1 = echarts.init(this.$refs.typeChart)
        c1.setOption({
          title: { text: '分子类型分布', left: 'center' },
          series: [{
            type: 'pie', radius: ['40%', '70%'],
            data: [
              { value: 4500, name: '有机小分子' },
              { value: 3200, name: '无机小分子' },
              { value: 1800, name: '芳香族化合物' },
              { value: 1200, name: '无机盐' },
              { value: 800, name: '烯烃' },
              { value: 956, name: '其他' }
            ]
          }]
        })
      }
      if (this.$refs.massChart) {
        const c2 = echarts.init(this.$refs.massChart)
        c2.setOption({
          title: { text: '分子质量分布', left: 'center' },
          xAxis: { type: 'category', data: ['<50', '50-100', '100-200', '200-500', '500+'] },
          yAxis: { type: 'value' },
          series: [{ type: 'bar', data: [3200, 4100, 2800, 1500, 856], itemStyle: { color: '#2d5d9d' } }]
        })
      }
    })
  }
}
</script>
