<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-button type="primary" size="small" @click="handleAdd" style="margin-bottom:16px">{{ $t('btn.add') }}</el-button>
      <el-table :data="list" v-loading="loading" stripe>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="fieldEn" label="英文字段名"></el-table-column>
        <el-table-column prop="fieldZh" label="中文字段名"></el-table-column>
        <el-table-column prop="type" label="类型" width="100"></el-table-column>
        <el-table-column prop="required" label="必填" width="80">
          <template slot-scope="scope">
            <el-tag :type="scope.row.required ? 'danger' : 'info'" size="small">{{ scope.row.required ? '是' : '否' }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200"></el-table-column>
        <el-table-column :label="$t('common.operation')" width="150">
          <template slot-scope="scope">
            <el-button type="text" @click="handleEdit(scope.row)">{{ $t('btn.edit') }}</el-button>
            <el-button type="text" style="color:#F56C6C" @click="handleDelete(scope.row)">{{ $t('btn.delete') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <!-- Add/Edit Dialog -->
    <el-dialog :visible.sync="dialogVisible" :title="editForm.id ? $t('btn.edit') : $t('btn.add')" width="500px">
      <el-form :model="editForm" label-width="100px" size="small">
        <el-form-item label="英文名"><el-input v-model="editForm.fieldEn"></el-input></el-form-item>
        <el-form-item label="中文名"><el-input v-model="editForm.fieldZh"></el-input></el-form-item>
        <el-form-item label="类型"><el-select v-model="editForm.type"><el-option label="string" value="string"></el-option><el-option label="float" value="float"></el-option><el-option label="int" value="int"></el-option></el-select></el-form-item>
        <el-form-item label="必填"><el-switch v-model="editForm.required"></el-switch></el-form-item>
        <el-form-item label="描述"><el-input v-model="editForm.description" type="textarea"></el-input></el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">{{ $t('btn.cancel') }}</el-button>
        <el-button type="primary" @click="handleSave">{{ $t('btn.save') }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getMetadata, saveMetadata, deleteMetadata } from '@/api'

export default {
  name: 'MetadataManage',
  components: { AppPageHeader },
  data() {
    return {
      list: [], loading: false, dialogVisible: false,
      editForm: { fieldEn: '', fieldZh: '', type: 'string', required: false, description: '' }
    }
  },
  created() { this.fetchData() },
  methods: {
    async fetchData() {
      this.loading = true
      try {
        const res = await getMetadata()
        this.list = res.data.result || []
      } catch (_) {}
      this.loading = false
    },
    handleAdd() {
      this.editForm = { fieldEn: '', fieldZh: '', type: 'string', required: false, description: '' }
      this.dialogVisible = true
    },
    handleEdit(row) {
      this.editForm = { ...row }
      this.dialogVisible = true
    },
    async handleSave() {
      try {
        await saveMetadata(this.editForm)
        this.$message.success(this.$t('common.saveSuccess'))
        this.dialogVisible = false
        this.fetchData()
      } catch (_) {}
    },
    async handleDelete(row) {
      try {
        await this.$confirm(this.$t('common.confirmDelete'), '', { type: 'warning' })
        await deleteMetadata(row.id)
        this.$message.success(this.$t('common.deleteSuccess'))
        this.fetchData()
      } catch (_) {}
    }
  }
}
</script>
