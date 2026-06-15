<template>
  <div class="list-page">
    <AppPageHeader />
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6" v-for="stat in stats" :key="stat.label">
        <el-card shadow="hover">
          <div style="text-align:center">
            <div style="font-size:32px;font-weight:bold;color:#1a4a80">{{ stat.value }}</div>
            <div style="color:#999;font-size:13px;margin-top:8px">{{ stat.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row :gutter="20" style="margin-top:20px">
      <el-col :span="14">
        <el-card>
          <div slot="header">系统概览</div>
          <div ref="overviewChart" style="height:300px"></div>
        </el-card>
      </el-col>
      <el-col :span="10">
        <el-card>
          <div slot="header">快速管理入口</div>
          <div class="admin-links">
            <el-button type="primary" plain style="width:100%;margin-bottom:12px" @click="$router.push('/metadata-manage')">{{ $t('admin.metadataManage') }}</el-button>
            <el-button type="success" plain style="width:100%;margin-bottom:12px" @click="$router.push('/tag-definition-manage')">{{ $t('admin.tagDefinitionManage') }}</el-button>
            <el-button type="warning" plain style="width:100%;margin-bottom:12px" @click="$router.push('/permission-tag-definition-manage')">{{ $t('admin.permissionTagManage') }}</el-button>
            <el-button type="info" plain style="width:100%" @click="$router.push('/system-audit-log')">{{ $t('admin.auditLog') }}</el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import * as echarts from 'echarts'

export default {
  name: 'ControlConsole',
  components: { AppPageHeader },
  data() {
    return {
      stats: [
        { label: '注册用户', value: '1,245' },
        { label: '分子数据', value: '12,456' },
        { label: '材料数据', value: '5,832' },
        { label: 'API调用(今日)', value: '8,523' }
      ]
    }
  },
  mounted() {
    this.$nextTick(() => {
      if (this.$refs.overviewChart) {
        const chart = echarts.init(this.$refs.overviewChart)
        chart.setOption({
          tooltip: { trigger: 'axis' },
          legend: { data: ['分子上传', '材料上传', '用户注册'] },
          xAxis: { type: 'category', data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'] },
          yAxis: { type: 'value' },
          series: [
            { name: '分子上传', type: 'bar', data: [120, 180, 250, 310, 280, 350], itemStyle: { color: '#409EFF' } },
            { name: '材料上传', type: 'bar', data: [80, 100, 150, 180, 200, 230], itemStyle: { color: '#67C23A' } },
            { name: '用户注册', type: 'line', data: [30, 45, 60, 85, 100, 130], itemStyle: { color: '#E6A23C' } }
          ]
        })
      }
    })
  }
}
</script>
