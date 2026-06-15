<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>{{ $t('title.forgetPassword') }}</h2>
      </div>
      <el-form ref="form" :model="form" :rules="rules" size="medium">
        <el-form-item prop="email">
          <el-input v-model="form.email" :placeholder="$t('common.email')" prefix-icon="el-icon-message"></el-input>
        </el-form-item>
        <el-form-item prop="code">
          <el-row :gutter="12" style="width:100%">
            <el-col :span="14">
              <el-input v-model="form.code" :placeholder="$t('auth.emailCode')"></el-input>
            </el-col>
            <el-col :span="10">
              <el-button :disabled="countdown > 0" @click="sendCode" style="width:100%">
                {{ countdown > 0 ? countdown + 's' : $t('auth.sendCode') }}
              </el-button>
            </el-col>
          </el-row>
        </el-form-item>
        <el-form-item prop="newPassword">
          <el-input v-model="form.newPassword" type="password" :placeholder="$t('common.newPassword')" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleReset" style="width:100%">{{ $t('auth.resetPassword') }}</el-button>
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
  name: 'ForgetPassword',
  data() {
    return {
      form: { email: '', code: '', newPassword: '' },
      countdown: 0,
      timer: null,
      rules: {
        email: [{ required: true, type: 'email', message: '请输入有效邮箱', trigger: 'blur' }],
        code: [{ required: true, message: '请输入验证码', trigger: 'blur' }],
        newPassword: [{ required: true, min: 6, message: '密码至少6位', trigger: 'blur' }]
      }
    }
  },
  methods: {
    sendCode() {
      if (!this.form.email) { this.$message.warning('请先输入邮箱'); return }
      this.countdown = 60
      this.timer = setInterval(() => {
        this.countdown--
        if (this.countdown <= 0) clearInterval(this.timer)
      }, 1000)
      this.$message.success('验证码已发送')
    },
    handleReset() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.$message.success(this.$t('auth.resetSuccess'))
        setTimeout(() => this.$router.push('/login'), 3000)
      })
    }
  },
  beforeDestroy() {
    if (this.timer) clearInterval(this.timer)
  }
}
</script>

<style scoped>
.auth-page { display:flex;justify-content:center;align-items:center;min-height:100vh;background:linear-gradient(135deg,#1a4a80 0%,#2d5d9d 50%,#437fa1 100%); }
.auth-card { width:400px;background:#fff;border-radius:8px;padding:40px;box-shadow:0 8px 32px rgba(0,0,0,0.2); }
.auth-header { text-align:center;margin-bottom:30px; }
.auth-header h2 { margin:0;color:#1a4a80;font-size:22px; }
</style>
