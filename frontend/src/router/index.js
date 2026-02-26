import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: () => import('../views/LoginView.vue'), meta: { guest: true } },
  { path: '/register', component: () => import('../views/RegisterView.vue'), meta: { guest: true } },
  { path: '/admin', component: () => import('../views/AdminDashboard.vue'), meta: { auth: true, roles: ['shop_admin'] } },
  { path: '/director', component: () => import('../views/DirectorDashboard.vue'), meta: { auth: true, roles: ['director', 'super_admin'] } },
  { path: '/superadmin', component: () => import('../views/SuperAdminDashboard.vue'), meta: { auth: true, roles: ['super_admin'] } },
  { path: '/superadmin/shops', component: () => import('../views/ShopsManagement.vue'), meta: { auth: true, roles: ['super_admin'] } },
  { path: '/superadmin/employees', component: () => import('../views/EmployeesManagement.vue'), meta: { auth: true, roles: ['super_admin'] } },
  { path: '/superadmin/users', component: () => import('../views/UsersManagement.vue'), meta: { auth: true, roles: ['super_admin'] } },
  { path: '/superadmin/logs', component: () => import('../views/LogsView.vue'), meta: { auth: true, roles: ['super_admin'] } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (!auth.user && localStorage.getItem('access_token')) {
    await auth.fetchMe()
  }

  if (to.meta.auth && !auth.isAuthenticated) {
    return next('/login')
  }
  if (to.meta.guest && auth.isAuthenticated) {
    return redirectByRole(auth.user.role, next)
  }
  if (to.meta.roles && !to.meta.roles.includes(auth.user?.role)) {
    return redirectByRole(auth.user?.role, next)
  }
  next()
})

function redirectByRole(role, next) {
  if (role === 'super_admin') return next('/superadmin')
  if (role === 'director') return next('/director')
  if (role === 'shop_admin') return next('/admin')
  next('/login')
}

export default router
