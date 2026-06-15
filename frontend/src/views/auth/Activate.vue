<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>{{ $t('title.activate') }}</h2>
        <p>{{ $t('title.platform') }}</p>
      </div>
      <el-form size="medium">
        <el-form-item>
          <el-input v-model="email" :placeholder="$t('common.email')" prefix-icon="el-icon-message"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input v-model="code" :placeholder="$t('auth.emailCode')" prefix-icon="el-icon-tickets"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleActivate" style="width:100%">{{ $t('auth.activateAccount') }}</el-button>
        </el-form-item>
        <el-form-item style="text-align:center;margin-bottom:0">
          <router-link to="/login">{{ $t('btn.back') }} {{ $t('title.login') }}</router-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Activate',
  data() {
    return { email: '', code: '' }
  },
  methods: {
    handleActivate() {
      if (!this.email || !this.code) {
        this.$message.warning('请填写邮箱和激活码')
        return
      }
      this.$message.success('激活成功！')
      setTimeout(() => this.$router.push('/login'), 2000)
    }
  }
}
</script>

<style scoped>
.auth-page { display:flex;justify-content:center;align-items:center;min-height:100vh;background:linear-gradient(135deg,#1a4a80 0%,#2d5d9d 50%,#437fa1 100%); }
.auth-card { width:400px;background:#fff;border-radius:8px;padding:40px;box-shadow:0 8px 32px rgba(0,0,0,0.2); }
.auth-header { text-align:center;margin-bottom:30px; }
.auth-header h2 { margin:0;color:#1a4a80;font-size:22px; }
.auth-header p { margin:8px 0 0;color:#999;font-size:13px; }
</style>
