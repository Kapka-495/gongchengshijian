<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <el-button type="primary" size="small" @click="handleAdd" style="margin-bottom:16px">{{ $t('btn.add') }}</el-button>
      <el-table :data="tags" stripe>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="name" label="标签名"></el-table-column>
        <el-table-column prop="category" label="分类"></el-table-column>
        <el-table-column prop="count" label="关联数量" width="120"></el-table-column>
        <el-table-column label="状态" width="100"><template><el-tag type="success" size="small">激活</el-tag></template></el-table-column>
        <el-table-column :label="$t('common.operation')" width="150">
          <template slot-scope="scope">
            <el-button type="text" @click="handleEdit(scope.row)">{{ $t('btn.edit') }}</el-button>
            <el-button type="text" style="color:#F56C6C" @click="handleDelete(scope.row)">{{ $t('btn.delete') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog :visible.sync="dialogVisible" :title="$t('btn.add')" width="400px">
      <el-form :model="editForm" label-width="80px" size="small">
        <el-form-item label="名称"><el-input v-model="editForm.name"></el-input></el-form-item>
        <el-form-item label="分类"><el-input v-model="editForm.category"></el-input></el-form-item>
      </el-form>
      <span slot="footer">
        <el-button @click="dialogVisible = false">{{ $t('btn.cancel') }}</el-button>
        <el-button type="primary" @click="dialogVisible = false; $message.success($t('common.saveSuccess'))">{{ $t('btn.save') }}</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getMoleculeTags, getMaterialTags } from '@/api'

export default {
  name: 'TagDefinitionManage',
  components: { AppPageHeader },
  data() { return { tags: [], dialogVisible: false, editForm: { name: '', category: '' } } },
  created() { this.fetchData() },
  methods: {
    async fetchData() {
      try {
        const [mol, mat] = await Promise.all([getMoleculeTags(), getMaterialTags()])
        this.tags = [...(mol.data || []), ...(mat.data || [])]
      } catch (_) {}
    },
    handleAdd() { this.editForm = { name: '', category: '' }; this.dialogVisible = true },
    handleEdit(row) { this.editForm = { ...row }; this.dialogVisible = true },
    async handleDelete() {
      try {
        await this.$confirm(this.$t('common.confirmDelete'), '', { type: 'warning' })
        this.$message.success(this.$t('common.deleteSuccess'))
        this.fetchData()
      } catch (_) {}
    }
  }
}
</script>
