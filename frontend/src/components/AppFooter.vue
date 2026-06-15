<template>
  <div class="app-footer">
    <div class="footer-content">
      <span>© 2025 {{ $t('title.platform') }} | USTC</span>
      <span class="footer-sep">|</span>
      <span>{{ $t('nav.about') }}</span>
      <span class="footer-sep">|</span>
      <span>访客量: {{ visitorCount }}</span>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  name: 'AppFooter',
  computed: {
    ...mapState('user', ['visitorCount'])
  },
  mounted() {
    this.fetchVisitorCount()
  },
  methods: {
    async fetchVisitorCount() {
      try {
        const { getVisitorCount } = await import('@/api')
        const res = await getVisitorCount()
        this.$store.commit('user/SET_VISITOR_COUNT', res.data)
      } catch (_) { /* ignore */ }
    }
  }
}
</script>

<style scoped>
.app-footer {
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-top: 1px solid #ebeef5;
  background: #fff;
  font-size: 12px;
  color: #999;
  margin-top: auto;
}
.footer-sep {
  margin: 0 12px;
}
</style>
