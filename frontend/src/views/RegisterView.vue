<template>
  <div class="min-h-screen bg-primary-500 flex flex-col items-center justify-center px-6">
    <div class="w-full max-w-sm">
      <div class="text-center mb-8">
        <div class="w-20 h-20 bg-white rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <span class="text-4xl">🛍️</span>
        </div>
        <h1 class="text-3xl font-bold text-white">Fix App</h1>
      </div>
      <div class="bg-white rounded-2xl p-6 shadow-xl">
        <h2 class="text-xl font-bold text-gray-900 mb-6">Регистрация</h2>
        <form @submit.prevent="handleRegister" class="flex flex-col gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Полное имя</label>
            <input v-model="full_name" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500 text-base" placeholder="Иван Иванов" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="email" type="email" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500 text-base" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Пароль</label>
            <input v-model="password" type="password" required minlength="6" class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500 text-base" />
          </div>
          <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
          <p v-if="success" class="text-green-600 text-sm text-center">✓ Аккаунт создан! Войдите в систему.</p>
          <button type="submit" :disabled="loading" class="w-full bg-primary-500 text-white py-4 rounded-xl font-bold text-lg">
            {{ loading ? 'Создание...' : 'Создать аккаунт' }}
          </button>
        </form>
        <p class="text-center text-sm text-gray-500 mt-4">
          Уже есть аккаунт?
          <router-link to="/login" class="text-primary-500 font-medium">Войти</router-link>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const full_name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const success = ref(false)
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  success.value = false
  loading.value = true
  try {
    await auth.register(email.value, password.value, full_name.value)
    success.value = true
    full_name.value = ''
    email.value = ''
    password.value = ''
  } catch (e) {
    error.value = e.response?.data?.detail || 'Ошибка регистрации'
  } finally {
    loading.value = false
  }
}
</script>
