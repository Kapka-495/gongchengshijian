<template>
  <div class="list-page">
    <AppPageHeader />
    <el-row :gutter="20">
      <el-col :span="16">
        <el-card>
          <div slot="header">{{ $t('community.community') }}</div>
          <p style="color:#909399">社区主页 - 讨论区、用户贡献、数据集分享</p>
          <el-tabs v-model="activeTab">
            <el-tab-pane label="热门讨论" name="discussions">
              <div v-for="d in discussions" :key="d.id" class="discussion-item">
                <h4 style="margin:0;color:#1a4a80;cursor:pointer">{{ d.title }}</h4>
                <div style="font-size:12px;color:#999;margin-top:4px">{{ d.author }} · {{ d.time }} · {{ d.replies }} 回复</div>
                <p style="font-size:13px;color:#606266;margin:8px 0">{{ d.content }}</p>
              </div>
              <el-empty v-if="!discussions.length" description="暂无讨论"></el-empty>
            </el-tab-pane>
            <el-tab-pane label="数据集分享" name="datasets">
              <div v-for="ds in datasets" :key="ds.id" class="discussion-item">
                <h4 style="margin:0;color:#1a4a80;cursor:pointer">{{ ds.title }}</h4>
                <div style="font-size:12px;color:#999;margin-top:4px">{{ ds.author }} · {{ ds.time }} · {{ ds.downloads }} 下载</div>
              </div>
              <el-empty v-if="!datasets.length" description="暂无数据集分享"></el-empty>
            </el-tab-pane>
          </el-tabs>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <div slot="header">快捷入口</div>
          <el-menu>
            <el-menu-item @click="$router.push('/community/TagsCommunity')">
              <i class="el-icon-collection-tag"></i>
              <span>{{ $t('community.tagsCommunity') }}</span>
            </el-menu-item>
            <el-menu-item @click="$router.push('/upload_data')">
              <i class="el-icon-upload2"></i>
              <span>{{ $t('community.contributeData') }}</span>
            </el-menu-item>
            <el-menu-item>
              <i class="el-icon-reading"></i>
              <span>{{ $t('community.domainKnowledgeBase') }}</span>
            </el-menu-item>
          </el-menu>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import AppPageHeader from '@/components/AppPageHeader.vue'

export default {
  name: 'Community',
  components: { AppPageHeader },
  data() {
    return {
      activeTab: 'discussions',
      discussions: [
        { id: 1, title: '关于DFT计算中泛函选择的讨论', author: 'ZhangLab', time: '2026-01-12', replies: 23, content: '在进行过渡金属催化剂的DFT计算时，大家通常使用什么泛函？PBE还是RPBE？对于吸附能计算，哪种更准确？...' },
        { id: 2, title: '分享：分子动力学模拟初始结构准备经验', author: 'ChemSim', time: '2026-01-08', replies: 15, content: '在使用LAMMPS进行分子动力学模拟时，初始结构的准备非常重要。这里分享一些我的经验和注意事项...' },
        { id: 3, title: '求助：如何评估机器学习势函数的精度？', author: 'ML_newbie', time: '2026-01-05', replies: 8, content: '我训练了一个NNP势函数，但是不知道如何系统评估其精度。除了RMSE，还需要看哪些指标？...' }
      ],
      datasets: [
        { id: 1, title: 'Cu(111)表面CO2还原DFT数据集', author: 'ZhangLab', time: '2026-01-10', downloads: 156 },
        { id: 2, title: '钙钛矿带隙高通量计算数据集', author: 'PerovGroup', time: '2026-01-06', downloads: 89 }
      ]
    }
  }
}
</script>

<style scoped>
.discussion-item { padding: 12px 0; border-bottom: 1px solid #f0f0f0; }
.discussion-item:last-child { border-bottom: none; }
</style>
