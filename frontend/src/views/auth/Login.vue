<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <h2>{{ $t('title.platform') }}</h2>
        <p>Precision Chemistry Data Platform</p>
      </div>
      <el-form ref="form" :model="form" :rules="rules" size="medium">
        <el-form-item prop="username">
          <el-input v-model="form.username" :placeholder="$t('common.username')" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" :placeholder="$t('common.password')" prefix-icon="el-icon-lock" @keyup.enter.native="handleLogin"></el-input>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="rememberMe">{{ $t('auth.rememberMe') }}</el-checkbox>
          <router-link to="/forgetPassword" class="forgot-link">{{ $t('auth.forgotPassword') }}</router-link>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="loading" @click="handleLogin" style="width:100%">{{ $t('btn.login') }}</el-button>
        </el-form-item>
        <el-form-item style="text-align:center;margin-bottom:0">
          <span>{{ $t('auth.noAccount') }}</span>
          <router-link to="/register">{{ $t('auth.goRegister') }}</router-link>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return {
      form: { username: 'admin', password: 'admin123' },
      rememberMe: false,
      loading: false,
      rules: {
        username: [{ required: true, message: this.$t('common.pleaseInput') + this.$t('common.username'), trigger: 'blur' }],
        password: [{ required: true, message: this.$t('common.pleaseInput') + this.$t('common.password'), trigger: 'blur' }]
      }
    }
  },
  created() {
    if (this.$route.query.registered) {
      this.$message.success('注册成功，请登录')
    }
  },
  methods: {
    handleLogin() {
      this.$refs.form.validate(valid => {
        if (!valid) return
        this.loading = true
        this.$store.dispatch('user/login', this.form).then(() => {
          this.$message.success('登录成功')
          const redirect = this.$route.query.redirect || '/home'
          this.$router.push(redirect)
        }).catch(err => {
          this.$message.error(err.message || '登录失败')
        }).finally(() => {
          this.loading = false
        })
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
  width: 400px;
  background: #fff;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
}
.auth-header {
  text-align: center;
  margin-bottom: 30px;
}
.auth-header h2 {
  margin: 0;
  color: #1a4a80;
  font-size: 24px;
}
.auth-header p {
  margin: 8px 0 0;
  color: #999;
  font-size: 13px;
}
.forgot-link {
  float: right;
  font-size: 13px;
}
</style>
