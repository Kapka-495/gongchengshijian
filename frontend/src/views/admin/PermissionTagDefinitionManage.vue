<template>
  <div class="list-page">
    <AppPageHeader />
    <el-card>
      <p style="color:#909399">权限标签定义管理 - 管理数据的访问权限标签（公开、专项内公开、保密、保护期）</p>
      <el-table :data="permissions" stripe>
        <el-table-column type="index" width="60"></el-table-column>
        <el-table-column prop="name" label="权限名称"></el-table-column>
        <el-table-column prop="level" label="级别" width="80"></el-table-column>
        <el-table-column prop="description" label="描述"></el-table-column>
        <el-table-column label="状态" width="100">
          <template><el-tag type="success" size="small">激活</el-tag></template>
        </el-table-column>
        <el-table-column :label="$t('common.operation')" width="150">
          <template>
            <el-button type="text">{{ $t('btn.edit') }}</el-button>
            <el-button type="text">{{ $t('admin.resetPermission') }}</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'

export default {
  name: 'PermissionTagDefinitionManage',
  components: { AppPageHeader },
  data() {
    return {
      permissions: [
        { name: '公开', level: 1, description: '所有用户可见' },
        { name: '专项内公开', level: 2, description: '专项认证用户可见' },
        { name: '保密', level: 3, description: '仅数据拥有者和授权用户可见' },
        { name: '保护期', level: 4, description: '≤12个月保护期后转为公开' }
      ]
    }
  }
}
</script>
