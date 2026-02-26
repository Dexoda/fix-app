<template>
  <div class="min-h-screen bg-primary-500 flex flex-col items-center justify-center px-6">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-white rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <span class="text-4xl">🛍️</span>
        </div>
        <h1 class="text-3xl font-bold text-white">Fix App</h1>
        <p class="text-primary-100 mt-1">Контроль сотрудников</p>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-xl">
        <h2 class="text-xl font-bold text-gray-900 mb-6">Вход в систему</h2>
        <form @submit.prevent="handleLogin" class="flex flex-col gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="email" type="email" required autocomplete="email"
              class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500 text-base"
              placeholder="admin@fixapp.local" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
            <input v-model="password" type="password" required autocomplete="current-password"
              class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500 text-base"
              placeholder="••••••••" />
          </div>
          <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
          <button type="submit" :disabled="loading"
            class="w-full bg-primary-500 text-white py-4 rounded-xl font-bold text-lg transition-all active:scale-95 disabled:opacity-50">
            {{ loading ? 'Вход...' : 'Войти' }}
          </button>
        </form>
        <p class="text-center text-sm text-gray-500 mt-4">
          Нет аккаунта?
          <router-link to="/register" class="text-primary-500 font-medium">Зарегистрироваться</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    const role = auth.user?.role
    if (role === 'super_admin') router.push('/superadmin')
    else if (role === 'director') router.push('/director')
    else router.push('/admin')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка входа'
  } finally {
    loading.value = false
  }
}
</script>
