<template>
  <div class="list-page">
    <AppPageHeader />
    <!-- API Overview -->
    <el-card style="margin-bottom:20px">
      <div slot="header">PIC-DB API</div>
      <p>{{ $t('api.apiDesc1') }}</p>
      <el-alert
        :title="$t('api.apiKeyDesc')"
        type="info"
        :closable="false"
        show-icon
        style="margin-top:12px"
      >
        <template slot="default">
          {{ $t('api.apiKeyDesc') }}
          <a href="javascript:void(0)" style="color:#409EFF">{{ $t('api.apiKeyView') }}</a>
        </template>
      </el-alert>
    </el-card>

    <!-- API Key Management -->
    <el-card style="margin-bottom:20px">
      <div slot="header">API Key</div>
      <el-descriptions :column="2" border>
        <el-descriptions-item label="API Key">pic_db_xxxxxxxxxxxxxxxxxxxxxxxx</el-descriptions-item>
        <el-descriptions-item label="Status"><el-tag type="success">Active</el-tag></el-descriptions-item>
        <el-descriptions-item label="Rate Limit">1000 requests/hour</el-descriptions-item>
        <el-descriptions-item label="Created">2025-12-01</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <!-- API Services -->
    <el-card v-for="svc in services" :key="svc.name" style="margin-bottom:20px">
      <div slot="header">
        <strong>{{ svc.label }}</strong>
        <span style="color:#909399;font-size:13px;margin-left:8px">{{ svc.description }}</span>
      </div>
      <el-collapse accordion>
        <el-collapse-item v-for="api in svc.apis" :key="api.name">
          <template slot="title">
            <el-tag :type="api.method === 'GET' ? 'success' : 'warning'" size="small" style="margin-right:8px">{{ api.method }}</el-tag>
            <strong>{{ api.path }}</strong>
            <span style="color:#909399;margin-left:12px;font-size:13px">{{ api.desc }}</span>
          </template>
          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="Path">{{ api.path }}</el-descriptions-item>
            <el-descriptions-item label="Method">{{ api.method }}</el-descriptions-item>
            <el-descriptions-item label="Parameters">{{ api.params }}</el-descriptions-item>
            <el-descriptions-item label="Response">
              <pre style="background:#f5f7fa;padding:8px;border-radius:4px;font-size:12px;overflow-x:auto">{{ api.response }}</pre>
            </el-descriptions-item>
          </el-descriptions>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'
import { getApiServices } from '@/api'

export default {
  name: 'ApiInfo',
  components: { AppPageHeader },
  data() { return { services: [] } },
  created() { this.fetchServices() },
  methods: {
    async fetchServices() {
      try {
        const res = await getApiServices()
        this.services = res.data || []
      } catch (_) {}
    }
  }
}
</script>
