<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <!-- Input Section -->
      <el-tabs v-model="activeTab" type="card" class="xrd-tabs">
        <el-tab-pane label="粘贴数据" name="paste">
          <el-input
            v-model="textData"
            type="textarea"
            :rows="8"
            placeholder="每行格式：角度 强度（空格或制表符分隔）&#10;示例：&#10;25.5 100&#10;26.2 85&#10;38.1 120"
          ></el-input>
        </el-tab-pane>
        <el-tab-pane label="上传 NPY 文件" name="npy">
          <p style="color:#909399;font-size:13px;margin-bottom:12px">
            上传 NumPy 保存的 .npy 文件，数组形状需为 [N, 2]：第 0 列为 2θ 角度(度)，第 1 列为强度。支持 CoreMOF 格式。
          </p>
          <el-upload
            ref="npyUpload"
            :auto-upload="false"
            :limit="1"
            accept=".npy"
            :on-change="handleNpyChange"
            :on-remove="handleNpyRemove"
            :file-list="npyFileList"
            action="#"
          >
            <el-button size="small" type="primary">
              <i class="el-icon-folder-opened"></i> 选择 .npy 文件
            </el-button>
          </el-upload>
        </el-tab-pane>
        <el-tab-pane label="示例数据" name="sample">
          <p style="color:#909399;font-size:13px;margin-bottom:12px">点击下方按钮加载示例 XRD 衍射峰数据</p>
          <el-button size="small" type="success" @click="loadSample">加载示例数据</el-button>
        </el-tab-pane>
      </el-tabs>

      <!-- Parameters -->
      <el-divider content-position="left">处理参数</el-divider>
      <el-form :inline="true" size="small">
        <el-form-item label="最小角度 (°)">
          <el-input-number v-model="minAngle" :min="0" :max="90" :step="0.1" :precision="1" size="small"></el-input-number>
        </el-form-item>
        <el-form-item label="最大角度 (°)">
          <el-input-number v-model="maxAngle" :min="5" :max="180" :step="0.1" :precision="1" size="small"></el-input-number>
        </el-form-item>
        <el-form-item label="步长 (°)">
          <el-input-number v-model="step" :min="0.001" :step="0.001" :precision="3" size="small"></el-input-number>
        </el-form-item>
        <el-form-item label="Sigma (高斯展宽)">
          <el-input-number v-model="sigma" :min="0.01" :step="0.01" :precision="2" size="small"></el-input-number>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="processing" @click="handleProcess">{{ processing ? '处理中...' : '处理并可视化' }}</el-button>
        </el-form-item>
      </el-form>

      <!-- Y-axis Toggle -->
      <el-form v-if="chartResult" :inline="true" size="small" style="margin-top:8px">
        <el-form-item label="Y 轴显示">
          <el-radio-group v-model="yAxisMode" @change="renderChart" size="small">
            <el-radio-button label="real">真实强度</el-radio-button>
            <el-radio-button label="normalized">归一化 (0–1)</el-radio-button>
          </el-radio-group>
        </el-form-item>
      </el-form>

      <!-- Chart -->
      <el-divider v-if="chartResult" content-position="left">XRD 图谱</el-divider>
      <div v-if="chartResult" ref="chartContainer" style="width:100%;height:420px;margin-top:8px"></div>
      <div v-if="chartResult" class="chart-legend">
        <span><span class="legend-dot" style="background:#409EFF"></span> 高斯展宽后</span>
        <span><span class="legend-dot" style="background:#E6A23C"></span> 原始峰</span>
        <span><span class="legend-dot" style="background:#67C23A"></span> 最大值</span>
        <span><span class="legend-dot" style="background:#F56C6C"></span> 最小值</span>
      </div>

      <!-- Stats -->
      <template v-if="chartResult">
        <el-divider content-position="left">数据统计</el-divider>
        <p style="color:#909399;font-size:13px;margin-bottom:12px">处理完成后将显示强度分布统计（最大值、最小值、四分位数）</p>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-card shadow="never" class="stats-card">
              <div slot="header"><span style="font-weight:600;color:#1a4a80">原始数据（强度）</span></div>
              <el-descriptions :column="1" size="small" border>
                <el-descriptions-item label="最大值">{{ formatNum(stats.original.max) }}</el-descriptions-item>
                <el-descriptions-item label="最小值">{{ formatNum(stats.original.min) }}</el-descriptions-item>
                <el-descriptions-item label="Q1 (25%)">{{ formatNum(stats.original.q1) }}</el-descriptions-item>
                <el-descriptions-item label="中位数 Q2 (50%)">{{ formatNum(stats.original.q2) }}</el-descriptions-item>
                <el-descriptions-item label="Q3 (75%)">{{ formatNum(stats.original.q3) }}</el-descriptions-item>
              </el-descriptions>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card shadow="never" class="stats-card">
              <div slot="header"><span style="font-weight:600;color:#67C23A">展宽后数据（归一化强度）</span></div>
              <el-descriptions :column="1" size="small" border>
                <el-descriptions-item label="最大值">{{ formatNum(stats.processed.max) }}</el-descriptions-item>
                <el-descriptions-item label="最小值">{{ formatNum(stats.processed.min) }}</el-descriptions-item>
                <el-descriptions-item label="Q1 (25%)">{{ formatNum(stats.processed.q1) }}</el-descriptions-item>
                <el-descriptions-item label="中位数 Q2 (50%)">{{ formatNum(stats.processed.q2) }}</el-descriptions-item>
                <el-descriptions-item label="Q3 (75%)">{{ formatNum(stats.processed.q3) }}</el-descriptions-item>
              </el-descriptions>
            </el-card>
          </el-col>
        </el-row>
      </template>

      <el-empty v-if="!chartResult && !processing" description="请粘贴 XRD 数据或上传 .npy 文件，点击「处理并可视化」查看图谱"></el-empty>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import AppPageHeader from '@/components/AppPageHeader.vue'
import { xrdProcess, xrdProcessNpy } from '@/api'

const SAMPLE_DATA = `25.5 100
26.2 85
38.1 120
44.2 95
51.8 110
64.2 78
77.4 65`

export default {
  name: 'XrdTool',
  components: { AppPageHeader },
  data() {
    return {
      activeTab: 'paste',
      textData: '',
      npyFileList: [],
      npyFile: null,
      minAngle: 5,
      maxAngle: 90,
      step: 0.01,
      sigma: 0.1,
      yAxisMode: 'real',
      processing: false,
      chartResult: null,
      chart: null,
      stats: {
        original: { min: null, max: null, q1: null, q2: null, q3: null },
        processed: { min: null, max: null, q1: null, q2: null, q3: null }
      }
    }
  },
  methods: {
    loadSample() {
      this.textData = SAMPLE_DATA
      this.activeTab = 'paste'
    },
    handleNpyChange(file, fileList) {
      this.npyFile = file.raw
      this.npyFileList = fileList
    },
    handleNpyRemove() {
      this.npyFile = null
      this.npyFileList = []
    },
    parseTextData(text) {
      const lines = text.trim().split(/\r?\n/).filter(Boolean)
      const data = []
      for (const line of lines) {
        const parts = line.trim().split(/[\s\t,;]+/)
        if (parts.length >= 2) {
          const angle = parseFloat(parts[0])
          const intensity = parseFloat(parts[1])
          if (!isNaN(angle) && !isNaN(intensity)) {
            data.push({ angle, intensity })
          }
        }
      }
      return data
    },
    computeStats(arr) {
      if (!arr || arr.length === 0) {
        return { min: null, max: null, q1: null, q2: null, q3: null }
      }
      const sorted = [...arr].sort((a, b) => a - b)
      const n = sorted.length
      const percentile = (p) => {
        const idx = p * (n - 1)
        const lo = Math.floor(idx)
        const hi = Math.ceil(idx)
        if (lo === hi) return sorted[lo]
        return sorted[lo] + (idx - lo) * (sorted[hi] - sorted[lo])
      }
      return {
        min: sorted[0],
        max: sorted[n - 1],
        q1: percentile(0.25),
        q2: percentile(0.5),
        q3: percentile(0.75)
      }
    },
    formatNum(v) {
      if (v == null) return '—'
      if (Math.abs(v) < 1e-4 || Math.abs(v) >= 1e4) return v.toExponential(4)
      return v.toFixed(4)
    },
    async handleProcess() {
      if (this.activeTab === 'npy') {
        if (!this.npyFile) {
          this.$message.warning('请先选择要上传的 .npy 文件')
          return
        }
        return this.processNpy()
      }

      const text = this.textData.trim()
      if (!text) {
        this.$message.warning('请输入 XRD 数据，或切换到「上传 NPY 文件」或「示例数据」Tab')
        return
      }

      const data = this.parseTextData(text)
      if (!data.length) {
        this.$message.error('无法解析有效数据，请检查格式（每行：角度 强度，空格或制表符分隔）')
        return
      }

      this.processing = true
      try {
        const result = await xrdProcess({
          data,
          min_angle: this.minAngle,
          max_angle: this.maxAngle,
          step: this.step,
          sigma: this.sigma
        })
        this.chartResult = result.data
        this.updateStats(result.data)
        this.$nextTick(() => this.renderChart())
      } catch (e) {
        this.$message.error('处理失败：' + (e.message || '请确保 XRD 后端服务已启动'))
      }
      this.processing = false
    },
    async processNpy() {
      const formData = new FormData()
      formData.append('file', this.npyFile)
      formData.append('min_angle', String(this.minAngle))
      formData.append('max_angle', String(this.maxAngle))
      formData.append('step', String(this.step))
      formData.append('sigma', String(this.sigma))

      this.processing = true
      try {
        const result = await xrdProcessNpy(formData)
        this.chartResult = result.data
        this.updateStats(result.data)
        this.$nextTick(() => this.renderChart())
      } catch (e) {
        this.$message.error('处理失败：' + (e.message || '请确保 XRD 后端服务已启动'))
      }
      this.processing = false
    },
    updateStats(result) {
      this.stats.original = this.computeStats(result.original.intensities)
      this.stats.processed = this.computeStats(result.processed.intensities)
    },
    renderChart() {
      if (!this.$refs.chartContainer || !this.chartResult) return
      if (this.chart) { this.chart.dispose(); this.chart = null }

      const result = this.chartResult
      const original = result.original
      const processed = result.processed
      const useNormalized = this.yAxisMode === 'normalized'

      let processedY, originalY
      if (useNormalized) {
        const maxOrig = Math.max(...original.intensities, 1)
        originalY = original.intensities.map(v => v / maxOrig)
        processedY = [...processed.intensities]
      } else {
        const maxOrig = Math.max(...original.intensities, 1)
        originalY = [...original.intensities]
        processedY = processed.intensities.map(v => v * maxOrig)
      }

      // Find max/min across all data for annotation points
      const combined = []
      processed.angles.forEach((a, i) => combined.push({ x: a, y: processedY[i], type: 'processed' }))
      original.angles.forEach((a, i) => combined.push({ x: a, y: originalY[i], type: 'original' }))
      const maxPt = combined.reduce((a, b) => (a.y >= b.y ? a : b))
      const minPt = combined.reduce((a, b) => (a.y <= b.y ? a : b))

      this.chart = echarts.init(this.$refs.chartContainer)
      this.chart.setOption({
        tooltip: {
          trigger: 'axis',
          formatter: (params) => {
            let html = ''
            params.forEach(p => {
              html += `<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${p.color};margin-right:5px"></span>`
              html += `${p.seriesName}: ${Number(p.value[1]).toFixed(4)}<br/>`
            })
            return html
          }
        },
        legend: { show: false },
        grid: { top: 20, bottom: 50, left: 60, right: 30 },
        xAxis: {
          type: 'value',
          name: '2θ (度)',
          nameLocation: 'center',
          nameGap: 30,
          min: 'dataMin',
          max: 'dataMax',
          minorTick: { show: true },
          minorSplitLine: { show: true, lineStyle: { color: '#f0f0f0' } }
        },
        yAxis: {
          type: 'value',
          name: useNormalized ? '强度 (归一化)' : '强度',
          nameLocation: 'center',
          nameGap: 45,
          min: 'dataMin',
          max: 'dataMax'
        },
        series: [
          {
            name: '高斯展宽后',
            type: 'line',
            data: processed.angles.map((a, i) => [a, processedY[i]]),
            smooth: true,
            showSymbol: false,
            lineStyle: { color: '#409EFF', width: 1.5 },
            areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: 'rgba(64,158,255,0.15)' },
              { offset: 1, color: 'rgba(64,158,255,0.02)' }
            ])}
          },
          {
            name: '原始峰',
            type: 'scatter',
            data: original.angles.map((a, i) => [a, originalY[i]]),
            symbolSize: 8,
            itemStyle: { color: '#E6A23C', borderColor: '#fff', borderWidth: 1 },
            emphasis: { scale: 1.5 }
          },
          {
            name: '最大值',
            type: 'scatter',
            data: [[maxPt.x, maxPt.y]],
            symbol: 'triangle',
            symbolSize: 16,
            itemStyle: { color: '#67C23A' },
            label: {
              show: true,
              position: 'top',
              distance: 8,
              formatter: `最大值 ${maxPt.y.toFixed(2)} @ ${maxPt.x.toFixed(2)}°`,
              fontSize: 11
            }
          },
          {
            name: '最小值',
            type: 'scatter',
            data: [[minPt.x, minPt.y]],
            symbol: 'triangle',
            symbolSize: 16,
            symbolRotate: 180,
            itemStyle: { color: '#F56C6C' },
            label: {
              show: true,
              position: 'bottom',
              distance: 8,
              formatter: `最小值 ${minPt.y.toFixed(2)} @ ${minPt.x.toFixed(2)}°`,
              fontSize: 11
            }
          }
        ]
      })
    }
  },
  beforeDestroy() {
    if (this.chart) { this.chart.dispose(); this.chart = null }
  }
}
</script>

<style scoped>
.xrd-tabs { margin-bottom: 8px; }
.chart-legend {
  display: flex;
  gap: 20px;
  justify-content: center;
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}
.legend-dot {
  display: inline-block;
  width: 12px;
  height: 4px;
  border-radius: 2px;
  margin-right: 6px;
  vertical-align: middle;
}
.stats-card {
  border: 1px solid #ebeef5;
}
</style>
