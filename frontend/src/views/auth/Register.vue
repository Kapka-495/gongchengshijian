<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>{{ $t('title.register') }}</h2>
        <p>{{ $t('title.platform') }}</p>
      </div>
      <el-form ref="form" :model="form" :rules="rules" size="medium">
        <el-form-item prop="username">
          <el-input v-model="form.username" :placeholder="$t('common.username')" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" :placeholder="$t('common.email')" prefix-icon="el-icon-message"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" :placeholder="$t('common.password')" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" :placeholder="$t('common.confirmPassword')" prefix-icon="el-icon-lock"></el-input>
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model="form.phone" :placeholder="$t('common.phone')" prefix-icon="el-icon-mobile-phone"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleRegister" style="width:100%">{{ $t('btn.register') }}</el-button>
        </el-form-item>
        <el-form-item style="text-align:center;margin-bottom:0">
          <span>{{ $t('auth.hasAccount') }}</span>
          <router-link to="/login">{{ $t('auth.goLogin') }}</router-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Register',
  data() {
    const validateConfirmPass = (rule, value, callback) => {
      if (value !== this.form.password) {
        callback(new Error('两次输入密码不一致'))
      } else { callback() }
    }
    return {
      form: { username: '', email: '', password: '', confirmPassword: '', phone: '' },
      loading: false,
      rules: {
        username: [{ required: true, message: this.$t('common.pleaseInput') + this.$t('common.username'), trigger: 'blur' }],
        email: [{ required: true, type: 'email', message: '请输入有效邮箱', trigger: 'blur' }],
        password: [{ required: true, min: 6, message: '密码至少6位', trigger: 'blur' }],
        confirmPassword: [{ required: true, validator: validateConfirmPass, trigger: 'blur' }],
        phone: [{ required: true, message: this.$t('common.pleaseInput') + this.$t('common.phone'), trigger: 'blur' }]
      }
    }
  },
  methods: {
    handleRegister() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.loading = true
        this.$store.dispatch('user/register', this.form).then(() => {
          this.$router.push({ path: '/login', query: { registered: '1' } })
        }).catch(() => {
          this.$message.error('注册失败')
        }).finally(() => { this.loading = false })
      })
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #1a4a80 0%, #2d5d9d 50%, #437fa1 100%);
}
.auth-card {
  width: 420px;
  background: #fff;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
.auth-header {
  text-align: center;
  margin-bottom: 30px;
}
.auth-header h2 { margin: 0; color: #1a4a80; font-size: 22px; }
.auth-header p { margin: 8px 0 0; color: #999; font-size: 13px; }
</style>
