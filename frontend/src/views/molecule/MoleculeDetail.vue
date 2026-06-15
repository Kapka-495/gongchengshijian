<template>
  <div class="detail-page">
    <AppPageHeader />
    <el-card v-loading="loading">
      <template v-if="molecule">
        <el-row :gutter="20">
          <!-- Left: Structure Viewer -->
          <el-col :span="10">
            <div class="structure-viewer">
              <div ref="viewer" style="width:100%;height:350px;"></div>
              <div style="text-align:center;margin-top:8px">
                <el-button size="small" @click="downloadStructure">{{ $t('btn.download') }} {{ $t('molecule.formula') }}</el-button>
                <el-button size="small" type="primary" @click="copySMILES">Copy SMILES</el-button>
              </div>
            </div>
          </el-col>
          <!-- Right: Properties -->
          <el-col :span="14">
            <el-tabs v-model="activeTab">
              <el-tab-pane :label="$t('molecule.detail')" name="info">
                <el-descriptions :column="2" border size="small">
                  <el-descriptions-item :label="$t('molecule.id')">{{ molecule.id }}</el-descriptions-item>
                  <el-descriptions-item :label="$t('molecule.formula')"><strong>{{ molecule.formula }}</strong></el-descriptions-item>
                  <el-descriptions-item :label="$t('molecule.mass')">{{ molecule.mass }} g/mol</el-descriptions-item>
                  <el-descriptions-item :label="$t('molecule.volumeUnit')">{{ molecule.volume }}</el-descriptions-item>
                  <el-descriptions-item :label="$t('molecule.type')"><el-tag size="small">{{ molecule.type }}</el-tag></el-descriptions-item>
                  <el-descriptions-item label="Charge"> {{ molecule.charge || 0 }}</el-descriptions-item>
                  <el-descriptions-item label="Spin">{{ molecule.spin || 1 }}</el-descriptions-item>
                  <el-descriptions-item :label="$t('molecule.tags')">
                    <el-tag
                      v-for="tag in molecule.tags"
                      :key="tag"
                      size="mini"
                      style="margin-right:4px;cursor:pointer"
                      @click="$router.push({ path: '/molecule', query: { keyword: tag } })"
                    >{{ tag }}</el-tag>
                  </el-descriptions-item>
                  <el-descriptions-item label="SMILES" :span="2">{{ molecule.smiles }}</el-descriptions-item>
                  <el-descriptions-item label="InChI" :span="2"><span style="font-size:11px;word-break:break-all">{{ molecule.inchi }}</span></el-descriptions-item>
                </el-descriptions>
              </el-tab-pane>
              <el-tab-pane label="Metadata" name="metadata">
                <el-empty description="元数据加载中..." v-if="!metadataLoaded"></el-empty>
                <el-form v-else label-width="120px" size="small">
                  <el-form-item label="计算方法">DFT-PBE</el-form-item>
                  <el-form-item label="基组">6-31G(d,p)</el-form-item>
                  <el-form-item label="温度">298.15 K</el-form-item>
                  <el-form-item label="压力">101325 Pa</el-form-item>
                </el-form>
              </el-tab-pane>
              <el-tab-pane label="Related" name="related">
                <el-empty description="暂无相关分子数据"></el-empty>
              </el-tab-pane>
              <el-tab-pane :label="$t('spectrum.spectroscopyData')" name="spectrum">
                <div v-loading="spectrumLoading">
                  <template v-if="spectrumData.length">
                    <el-form :inline="true" size="small" style="margin-bottom:12px">
                      <el-form-item :label="$t('spectrum.selectSpectrum')">
                        <el-select v-model="activeSpectrumId" @change="initSpectrumChart" style="width:260px">
                          <el-option v-for="s in spectrumData" :key="s.id" :label="s.name + ' (' + s.type + ')'" :value="s.id"></el-option>
                        </el-select>
                      </el-form-item>
                    </el-form>
                    <div ref="spectrumChart" style="width:100%;height:300px"></div>
                    <el-descriptions v-if="activeSpectrum" :column="2" border size="small" style="margin-top:16px">
                      <el-descriptions-item :label="$t('spectrum.instrument')">{{ activeSpectrum.instrument }}</el-descriptions-item>
                      <el-descriptions-item :label="$t('spectrum.spectrumType')">{{ activeSpectrum.type }}</el-descriptions-item>
                      <el-descriptions-item :label="$t('spectrum.conditions')" :span="2">{{ activeSpectrum.conditions }}</el-descriptions-item>
                    </el-descriptions>
                    <el-table v-if="activeSpectrum && activeSpectrum.peaks && activeSpectrum.peaks.length" :data="activeSpectrum.peaks" size="small" style="margin-top:12px">
                      <el-table-column prop="label" :label="$t('spectrum.peakPosition')" width="200"></el-table-column>
                      <el-table-column prop="x" :label="activeSpectrum.xLabel || 'Position'" width="180"></el-table-column>
                      <el-table-column prop="y" :label="$t('spectrum.peakIntensity')"></el-table-column>
                    </el-table>
                  </template>
                  <el-empty v-else :description="$t('spectrum.noSpectrumData')"></el-empty>
                </div>
              </el-tab-pane>
            </el-tabs>
          </el-col>
        </el-row>
      </template>
      <el-empty v-else :description="$t('common.noData')"></el-empty>
      <div style="margin-top:20px">
        <el-button @click="$router.push('/molecule')">{{ $t('btn.backToList') }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getMoleculeDetail, getSpectrum } from '@/api'

export default {
  name: 'MoleculeDetail',
  components: { AppPageHeader },
  data() {
    return {
      molecule: null, loading: false, activeTab: 'info', metadataLoaded: false,
      // Spectrum data
      spectrumData: [], spectrumLoading: false,
      activeSpectrumId: '', spectrumChart: null
    }
  },
  computed: {
    activeSpectrum() {
      if (!this.activeSpectrumId || !this.spectrumData.length) return null
      return this.spectrumData.find(s => s.id === this.activeSpectrumId) || this.spectrumData[0]
    }
  },
  watch: {
    activeTab(val) {
      if (val === 'spectrum' && !this.spectrumData.length) {
        this.fetchSpectrumData()
      }
    }
  },
  mounted() { this.fetchDetail() },
  methods: {
    async fetchDetail() {
      this.loading = true
      try {
        const res = await getMoleculeDetail(this.$route.params.id)
        this.molecule = res.data
        this.$nextTick(() => {
          this.initViewer()
          setTimeout(() => { this.metadataLoaded = true }, 500)
        })
      } catch (_) {}
      this.loading = false
    },
    async fetchSpectrumData() {
      if (!this.molecule) return
      this.spectrumLoading = true
      try {
        const res = await getSpectrum(this.molecule.id)
        this.spectrumData = res.data || []
        if (this.spectrumData.length) {
          this.activeSpectrumId = this.spectrumData[0].id
          this.$nextTick(() => this.initSpectrumChart())
        }
      } catch (_) { this.spectrumData = [] }
      this.spectrumLoading = false
    },
    initSpectrumChart() {
      if (!this.$refs.spectrumChart) return
      if (this.spectrumChart) { this.spectrumChart.dispose(); this.spectrumChart = null }
      const spec = this.activeSpectrum
      if (!spec || !spec.dataPoints) return
      this.spectrumChart = echarts.init(this.$refs.spectrumChart)
      this.spectrumChart.setOption({
        title: { text: spec.name, left: 'center', top: 5, textStyle: { fontSize: 13, color: '#303133' } },
        tooltip: { trigger: 'axis' },
        grid: { top: 40, bottom: 40, left: 55, right: 15 },
        xAxis: {
          type: 'value',
          name: spec.xLabel || '',
          nameLocation: 'center',
          nameGap: 25,
          inverse: spec.type === 'NMR'
        },
        yAxis: {
          type: 'value',
          name: spec.yLabel || '',
          nameLocation: 'center',
          nameGap: 40
        },
        series: [{
          type: 'line',
          data: spec.dataPoints,
          smooth: true,
          showSymbol: false,
          lineStyle: { color: '#1a4a80', width: 1.5 },
          areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(26,74,128,0.15)' },
            { offset: 1, color: 'rgba(26,74,128,0.02)' }
          ])},
          markPoint: {
            data: (spec.peaks || []).map(p => ({
              name: p.label,
              coord: [p.x, p.y],
              value: p.label
            })),
            symbol: 'pin',
            symbolSize: 28,
            label: { fontSize: 10 }
          }
        }]
      })
    },
    initViewer() {
      if (!this.$refs.viewer || !this.molecule || !window.ChemDoodle) return
      try {
        const mol = this.molecule
        let canvas = document.createElement('canvas')
        canvas.width = this.$refs.viewer.clientWidth
        canvas.height = 350
        this.$refs.viewer.innerHTML = ''
        this.$refs.viewer.appendChild(canvas)

        // Build molecule from atoms/bonds or use SMILES
        let molData
        if (mol.atoms && mol.bonds) {
          const cdmMol = new ChemDoodle.structures.Molecule()
          const scale = 30
          // Simple layout - arrange atoms in a row
          const n = mol.atoms.length
          for (let i = 0; i < n; i++) {
            const angle = (2 * Math.PI * i) / n
            const x = 175 + 80 * Math.cos(angle)
            const y = 175 + 80 * Math.sin(angle)
            cdmMol.atoms.push(new ChemDoodle.structures.Atom(mol.atoms[i], new ChemDoodle.structures.Point(x, y)))
          }
          if (mol.bonds) {
            mol.bonds.forEach(b => {
              if (b[0] < n && b[1] < n) {
                cdmMol.bonds.push(new ChemDoodle.structures.Bond(cdmMol.atoms[b[0]], cdmMol.atoms[b[1]], b[2] || 1))
              }
            })
          }
          molData = cdmMol
        } else {
          molData = ChemDoodle.readMOL(ChemDoodle.structures.Molecule.fromSMILES(mol.smiles))
        }
        const viewer = new ChemDoodle.ViewerCanvas(canvas, this.$refs.viewer.clientWidth, 350)
        viewer.specs.shapesColor = '#1a4a80'
        viewer.specs.backgroundColor = '#fff'
        viewer.specs.atoms_display = true
        viewer.specs.bonds_width_2D = 0.8
        viewer.loadMolecule(molData)
      } catch (e) {
        console.warn('ChemDoodle init failed:', e)
        if (this.$refs.viewer) {
          this.$refs.viewer.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:350px;background:#f8f9fa;border:1px solid #ebeef5;border-radius:4px;color:#999;">Structure: ' + this.molecule.smiles + '</div>'
        }
      }
    },
    downloadStructure() {
      if (this.molecule) {
        this.$message.success('Structure download triggered (mock)')
      }
    },
    copySMILES() {
      if (this.molecule && this.molecule.smiles) {
        navigator.clipboard.writeText(this.molecule.smiles).then(() => {
          this.$message.success(this.$t('common.copySuccess'))
        }).catch(() => {})
      }
    }
  },
  beforeDestroy() {
    if (this.spectrumChart) { this.spectrumChart.dispose(); this.spectrumChart = null }
  }
}
</script>

<style scoped>
.structure-viewer {
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 12px;
  background: #fff;
}
</style>
