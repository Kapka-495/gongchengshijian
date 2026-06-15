import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store'

Vue.use(VueRouter)

const routes = [
  // Auth routes (public)
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/auth/Login.vue'),
    meta: { title: 'router.login', noAuth: true }
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/auth/Register.vue'),
    meta: { title: 'router.register', noAuth: true }
  },
  {
    path: '/forgetPassword',
    name: 'forgetPassword',
    component: () => import('@/views/auth/ForgetPassword.vue'),
    meta: { title: 'router.forgetPassword', noAuth: true }
  },
  {
    path: '/activate',
    name: 'activate',
    component: () => import('@/views/auth/Activate.vue'),
    meta: { title: 'router.activate', noAuth: true }
  },
  // Main routes (require auth)
  {
    path: '/',
    component: () => import('@/layouts/DefaultLayout.vue'),
    redirect: '/home',
    children: [
      {
        path: 'home',
        name: 'home',
        component: () => import('@/views/home/Home.vue'),
        meta: { title: 'router.home' }
      },
      // News
      {
        path: 'newsList',
        name: 'newsList',
        component: () => import('@/views/news/NewsList.vue'),
        meta: { title: 'router.newsList' }
      },
      {
        path: 'newsDetails/:id',
        name: 'newsDetails',
        component: () => import('@/views/news/NewsDetails.vue'),
        meta: { title: 'router.newsDetail' }
      },
      {
        path: 'announcementList',
        name: 'announcementList',
        component: () => import('@/views/news/AnnouncementList.vue'),
        meta: { title: 'router.announcementList' }
      },
      {
        path: 'announcementDetails/:id',
        name: 'announcementDetails',
        component: () => import('@/views/news/AnnouncementDetails.vue'),
        meta: { title: 'router.announcementDetail' }
      },
      // Molecule
      {
        path: 'molecule',
        name: 'molecule',
        component: () => import('@/views/molecule/MoleculeList.vue'),
        meta: { title: 'router.molecule' }
      },
      {
        path: 'molecule-detail/:id',
        name: 'molecule-detail',
        component: () => import('@/views/molecule/MoleculeDetail.vue'),
        meta: { title: 'router.molecule_detail' }
      },
      {
        path: 'molecule-detail-coalesce',
        name: 'molecule-detail-coalesce',
        component: () => import('@/views/molecule/MoleculeDetailCoalesce.vue'),
        meta: { title: 'router.molecule_detail' }
      },
      {
        path: 'molecule-tags',
        name: 'molecule-tags',
        component: () => import('@/views/molecule/MoleculeTags.vue'),
        meta: { title: 'router.molecule_tags' }
      },
      {
        path: 'molecule-similarity',
        name: 'molecule-similarity',
        component: () => import('@/views/molecule/MoleculeSimilarity.vue'),
        meta: { title: 'router.molecule_similarity' }
      },
      // Materials
      {
        path: 'materials',
        name: 'materials',
        component: () => import('@/views/materials/MaterialsList.vue'),
        meta: { title: 'router.materials' }
      },
      {
        path: 'materials-detail/:id',
        name: 'materials-detail',
        component: () => import('@/views/materials/MaterialsDetail.vue'),
        meta: { title: 'router.materials_detail' }
      },
      {
        path: 'catalytic-detail/:id',
        name: 'catalytic-detail',
        component: () => import('@/views/materials/CatalyticDetail.vue'),
        meta: { title: 'router.CatalyzeDetail' }
      },
      {
        path: 'integration-materials',
        name: 'integration-materials',
        component: () => import('@/views/materials/IntegrationMaterials.vue'),
        meta: { title: 'router.integration_materials' }
      },
      {
        path: 'material-tags',
        name: 'material-tags',
        component: () => import('@/views/materials/MaterialTags.vue'),
        meta: { title: 'router.material_tags' }
      },
      // Literature
      {
        path: 'literature',
        name: 'literature',
        component: () => import('@/views/literature/LiteratureList.vue'),
        meta: { title: 'router.literature' }
      },
      {
        path: 'literature-detail/:id',
        name: 'literature-detail',
        component: () => import('@/views/literature/LiteratureDetail.vue'),
        meta: { title: 'router.literature_detail' }
      },
      // API Info
      {
        path: 'api-info',
        name: 'api-info',
        component: () => import('@/views/api-info/ApiInfo.vue'),
        meta: { title: 'router.api_info' }
      },
      // Admin
      {
        path: 'controlConsole',
        name: 'controlConsole',
        component: () => import('@/views/admin/ControlConsole.vue'),
        meta: { title: 'router.controlConsole', requireAdmin: true }
      },
      {
        path: 'metadata-manage',
        name: 'metadata-manage',
        component: () => import('@/views/admin/MetadataManage.vue'),
        meta: { title: 'router.metadata_management', requireAdmin: true }
      },
      {
        path: 'tag-definition-manage',
        name: 'tag-definition-manage',
        component: () => import('@/views/admin/TagDefinitionManage.vue'),
        meta: { title: 'router.tag_definition_management', requireAdmin: true }
      },
      {
        path: 'permission-tag-definition-manage',
        name: 'permission-tag-definition-manage',
        component: () => import('@/views/admin/PermissionTagDefinitionManage.vue'),
        meta: { title: 'router.tag_audit_management', requireAdmin: true }
      },
      {
        path: 'system-audit-log',
        name: 'system-audit-log',
        component: () => import('@/views/admin/SystemAuditLog.vue'),
        meta: { title: 'router.audit_log_management', requireAdmin: true }
      },
      // XRD
      {
        path: 'xrd-tool',
        name: 'xrd-tool',
        component: () => import('@/views/xrd/XrdTool.vue'),
        meta: { title: 'router.xrdTool' }
      },
      // Upload
      {
        path: 'upload_data',
        name: 'upload_data',
        component: () => import('@/views/upload/UploadData.vue'),
        meta: { title: 'router.uploadData' }
      },
      // Community
      {
        path: 'community',
        name: 'community',
        component: () => import('@/views/community/Community.vue'),
        meta: { title: 'router.community' }
      },
      {
        path: 'community/TagsCommunity',
        name: 'TagsCommunity',
        component: () => import('@/views/community/TagsCommunity.vue'),
        meta: { title: 'router.TagsCommunity' }
      },
      // Other
      {
        path: 'other',
        name: 'other',
        component: () => import('@/views/other/Other.vue'),
        meta: { title: 'router.other' }
      }
    ]
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: '/pichemdata/',
  routes
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.noAuth) {
    // Public routes - redirect to home if already logged in
    if (token && to.path === '/login') {
      next('/home')
    } else {
      next()
    }
  } else {
    // Protected routes
    if (!token) {
      next({ path: '/login', query: { redirect: to.fullPath } })
    } else if (to.meta.requireAdmin) {
      const userInfo = store.state.user.userInfo
      if (userInfo && userInfo.role === 'admin') {
        next()
      } else {
        next('/home')
      }
    } else {
      next()
    }
  }
})

export default router
