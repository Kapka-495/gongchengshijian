<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-steps :active="activeStep" align-center style="margin-bottom:30px">
        <el-step title="选择模板" />
        <el-step title="上传文件" />
        <el-step title="填写元数据" />
        <el-step title="提交审核" />
      </el-steps>

      <!-- Step 0: Select Template -->
      <div v-if="activeStep === 0">
        <h3>{{ $t('upload.selectTemplate') }} ({{ $t('upload.templateCount') }})</h3>
        <el-row :gutter="16">
          <el-col :span="8" v-for="tpl in templates" :key="tpl.id" style="margin-bottom:16px">
            <el-card shadow="hover" :class="['template-card', { selected: selectedTemplate === tpl.id }]" @click.native="selectedTemplate = tpl.id">
              <div style="text-align:center">
                <i class="el-icon-document" style="font-size:40px;color:#1a4a80"></i>
                <div style="margin-top:8px;font-weight:bold">{{ tpl.name }}</div>
                <div style="font-size:12px;color:#999;margin-top:4px">{{ tpl.desc }}</div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- Step 1: Upload File -->
      <div v-if="activeStep === 1">
        <h3>{{ $t('upload.uploadFile') }}</h3>
        <p style="color:#909399;font-size:13px">{{ $t('upload.toolHint') }}</p>
        <el-upload
          class="upload-area"
          drag
          action="#"
          :on-change="handleFileChange"
          :auto-upload="false"
          multiple
        >
          <i class="el-icon-upload" style="font-size:48px;color:#c0c4cc"></i>
          <div class="el-upload__text">拖拽文件到此处或 <em>点击选择</em></div>
          <div class="el-upload__tip" slot="tip">支持 .json, .csv, .xyz, .cif, POSCAR, OUTCAR 等格式</div>
        </el-upload>
        <div v-if="uploadFiles.length" style="margin-top:16px">
          <el-tag v-for="f in uploadFiles" :key="f.name" closable @close="removeFile(f)" style="margin-right:8px;margin-bottom:4px">
            {{ f.name }} ({{ formatFileSize(f.size) }})
          </el-tag>
        </div>
        <el-form size="small" style="margin-top:16px">
          <el-form-item label="处理工具">
            <el-select v-model="selectedTool">
              <el-option label="VASP" value="vasp"></el-option>
              <el-option label="ASE" value="ase"></el-option>
              <el-option label="LAMMPS" value="lammps"></el-option>
              <el-option label="Gaussian" value="gaussian"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>

      <!-- Step 2: Metadata -->
      <div v-if="activeStep === 2">
        <h3>{{ $t('admin.metadataManage') }}</h3>
        <el-form label-width="120px" size="small">
          <el-form-item label="计算方法"><el-input v-model="metadata.calculationMethod"></el-input></el-form-item>
          <el-form-item label="基组"><el-input v-model="metadata.basisSet"></el-input></el-form-item>
          <el-form-item label="温度(K)"><el-input-number v-model="metadata.temperature"></el-input-number></el-form-item>
          <el-form-item label="压力(Pa)"><el-input-number v-model="metadata.pressure"></el-input-number></el-form-item>
          <el-form-item label="描述">
            <el-input v-model="metadata.description" type="textarea" rows="4" :placeholder="$t('common.pleaseInput') + $t('common.description')"></el-input>
          </el-form-item>
          <el-form-item :label="$t('permission.publicLabel')">
            <el-select v-model="metadata.accessLevel">
              <el-option label="公开" value="public"></el-option>
              <el-option label="专项内公开" value="internal"></el-option>
              <el-option label="保密" value="confidential"></el-option>
              <el-option label="保护期" value="embargoed"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item v-if="metadata.accessLevel === 'embargoed'" label="保护期">
            <el-select v-model="metadata.embargoPeriod">
              <el-option label="6个月" value="6"></el-option>
              <el-option label="12个月" value="12"></el-option>
            </el-select>
          </el-form-item>
        </el-form>
      </div>

      <!-- Step 3: Review & Submit -->
      <div v-if="activeStep === 3">
        <h3>确认提交</h3>
        <el-descriptions :column="2" border>
          <el-descriptions-item label="模板">{{ selectedTemplate ? templates.find(t => t.id === selectedTemplate).name : '-' }}</el-descriptions-item>
          <el-descriptions-item label="文件数">{{ uploadFiles.length }}</el-descriptions-item>
          <el-descriptions-item label="处理工具">{{ selectedTool }}</el-descriptions-item>
          <el-descriptions-item label="权限">{{ metadata.accessLevel }}</el-descriptions-item>
          <el-descriptions-item label="计算方法">{{ metadata.calculationMethod }}</el-descriptions-item>
          <el-descriptions-item label="基组">{{ metadata.basisSet }}</el-descriptions-item>
        </el-descriptions>
        <div style="text-align:center;margin-top:20px">
          <el-button type="primary" size="large" :loading="submitting" :disabled="submitting" @click="handleSubmit">{{ submitting ? $t('common.loading') : $t('btn.upload') }}</el-button>
        </div>
      </div>

      <!-- Navigation -->
      <div style="text-align:center;margin-top:30px">
        <el-button v-if="activeStep > 0" @click="activeStep--">{{ $t('btn.previous') }}</el-button>
        <el-button v-if="activeStep < 3" type="primary" @click="goNext">{{ $t('btn.next') }}</el-button>
      </div>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { uploadMoleculeFile } from '@/api'

export default {
  name: 'UploadData',
  components: { AppPageHeader },
  data() {
    return {
      activeStep: 0,
      templates: [
        { id: 1, name: '分子结构模板', desc: '用于上传分子结构数据' },
        { id: 2, name: '材料性质模板', desc: '用于上传材料性质数据' },
        { id: 3, name: '催化数据模板', desc: '用于上传催化反应数据' }
      ],
      selectedTemplate: null,
      uploadFiles: [],
      selectedTool: 'vasp',
      submitting: false,
      metadata: {
        calculationMethod: 'DFT-PBE',
        basisSet: '6-31G(d,p)',
        temperature: 298,
        pressure: 101325,
        description: '',
        accessLevel: 'public',
        embargoPeriod: '12'
      }
    }
  },
  methods: {
    handleFileChange(file) {
      this.uploadFiles.push(file)
    },
    removeFile(file) {
      this.uploadFiles = this.uploadFiles.filter(f => f.name !== file.name)
    },
    formatFileSize(bytes) {
      if (!bytes) return '0 B'
      const units = ['B', 'KB', 'MB', 'GB']
      let i = 0
      let size = bytes
      while (size >= 1024 && i < units.length - 1) { size /= 1024; i++ }
      return size.toFixed(1) + ' ' + units[i]
    },
    goNext() {
      if (this.activeStep === 0 && !this.selectedTemplate) {
        this.$message.warning(this.$t('upload.selectTemplateFirst'))
        return
      }
      if (this.activeStep === 1 && !this.uploadFiles.length) {
        this.$message.warning(this.$t('upload.selectFileFirst'))
        return
      }
      this.activeStep++
    },
    async handleSubmit() {
      if (!this.selectedTemplate) {
        this.$message.warning(this.$t('upload.selectTemplateFirst'))
        return
      }
      if (!this.uploadFiles.length) {
        this.$message.warning(this.$t('upload.selectFileFirst'))
        return
      }

      const formData = new FormData()
      formData.append('templateId', this.selectedTemplate)
      formData.append('tool', this.selectedTool)
      formData.append('metadata', JSON.stringify(this.metadata))
      this.uploadFiles.forEach(f => {
        formData.append('files', f.raw || f)
      })

      this.submitting = true
      try {
        const res = await uploadMoleculeFile(formData)
        if (res.data && res.data.success) {
          this.$message.success(this.$t('upload.uploadSuccess'))
          this.activeStep = 0
          this.selectedTemplate = null
          this.uploadFiles = []
        } else {
          this.$message.error(this.$t('upload.uploadFailed'))
        }
      } catch (e) {
        this.$message.error(this.$t('upload.uploadFailed'))
      }
      this.submitting = false
    }
  }
}
</script>

<style scoped>
.template-card { cursor: pointer; border: 2px solid transparent; transition: all 0.2s; }
.template-card.selected { border-color: #1a4a80; background: #f0f5ff; }
.template-card:hover { border-color: #409EFF; }
.upload-area { width: 100%; }
.upload-area >>> .el-upload-dragger { width: 100%; }
</style>
