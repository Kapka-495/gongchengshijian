<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <div slot="header">{{ $t('community.tagsCommunity') }}</div>
      <p style="color:#909399">标签社区 - 用户共建的分类标签体系</p>
      <el-row :gutter="16">
        <el-col :span="12">
          <h4>分子标签</h4>
          <div ref="molTagCloud" style="height:300px"></div>
        </el-col>
        <el-col :span="12">
          <h4>材料标签</h4>
          <div ref="matTagCloud" style="height:300px"></div>
        </el-col>
      </el-row>
      <el-divider>标签建议</el-divider>
      <el-form :inline="true" size="small">
        <el-form-item label="建议新标签">
          <el-input v-model="newTag" placeholder="输入标签名"></el-input>
        </el-form-item>
        <el-form-item label="分类">
          <el-select v-model="newTagCategory">
            <el-option label="分子" value="molecule"></el-option>
            <el-option label="材料" value="material"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="suggestTag">{{ $t('btn.submit') }}</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import * as echarts from 'echarts'
import { getMoleculeTags, getMaterialTags } from '@/api'

export default {
  name: 'TagsCommunity',
  components: { AppPageHeader },
  data() {
    return { newTag: '', newTagCategory: 'molecule' }
  },
  mounted() { this.initCharts() },
  methods: {
    async initCharts() {
      try {
        const [molRes, matRes] = await Promise.all([getMoleculeTags(), getMaterialTags()])
        if (this.$refs.molTagCloud) {
          const c1 = echarts.init(this.$refs.molTagCloud)
          c1.setOption({
            series: [{
              type: 'wordCloud', shape: 'circle',
              sizeRange: [14, 40], rotationRange: [-30, 30], gridSize: 8,
              textStyle: { fontFamily: 'sans-serif', fontWeight: 'bold',
                color: () => '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0').replace(/^[0-9a-f]{2}/, '2d5d') },
              data: (molRes.data || []).map(t => ({ name: t.name, value: t.count }))
            }]
          })
        }
        if (this.$refs.matTagCloud) {
          const c2 = echarts.init(this.$refs.matTagCloud)
          c2.setOption({
            series: [{
              type: 'wordCloud', shape: 'circle',
              sizeRange: [14, 40], rotationRange: [-30, 30], gridSize: 8,
              textStyle: { fontFamily: 'sans-serif', fontWeight: 'bold',
                color: () => '#' + Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0').replace(/^[0-9a-f]{2}/, '1a4a') },
              data: (matRes.data || []).map(t => ({ name: t.name, value: t.count }))
            }]
          })
        }
      } catch (_) {}
    },
    suggestTag() {
      if (!this.newTag.trim()) { this.$message.warning('请输入标签名'); return }
      this.$message.success('标签建议已提交！')
      this.newTag = ''
    }
  }
}
</script>
