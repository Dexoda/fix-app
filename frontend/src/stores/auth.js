import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'shop_admin')
  const isDirector = computed(() => user.value?.role === 'director')
  const isSuperAdmin = computed(() => user.value?.role === 'super_admin')

  async function login(email, password) {
    loading.value = true
    try {
      const { data } = await api.post('/auth/login', { email, password })
      localStorage.setItem('access_token', data.access_token)
      localStorage.setItem('refresh_token', data.refresh_token)
      await fetchMe()
      return true
    } finally {
      loading.value = false
    }
  }

  async function register(email, password, full_name) {
    loading.value = true
    try {
      await api.post('/auth/register', { email, password, full_name })
      return true
    } finally {
      loading.value = false
    }
  }

  async function fetchMe() {
    try {
      const { data } = await api.get('/auth/me')
      user.value = data
    } catch {
      user.value = null
    }
  }

  function logout() {
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  return { user, loading, isAuthenticated, isAdmin, isDirector, isSuperAdmin, login, register, fetchMe, logout }
})
