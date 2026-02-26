<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader title="Пользователи" :show-back="true" />
    <div class="flex-1 overflow-y-auto p-4">
      <LoadingSpinner v-if="loading" />
      <div v-else>
        <div class="flex flex-col gap-3 mb-4">
          <div v-for="u in users" :key="u.id" class="bg-white rounded-xl shadow p-4 flex items-center justify-between">
            <div>
              <p class="font-semibold text-gray-900">{{ u.full_name }}</p>
              <p class="text-sm text-gray-500">{{ u.email }} · {{ roleLabel(u.role) }}</p>
            </div>
            <div class="flex gap-2">
              <button @click="editUser(u)" class="bg-gray-100 text-gray-700 px-3 py-2 rounded-lg text-sm">✏️</button>
              <button @click="deleteUser(u.id)" class="bg-red-50 text-red-500 px-3 py-2 rounded-lg text-sm">🗑️</button>
            </div>
          </div>
        </div>
        <button @click="showForm = true; editTarget = null" class="w-full bg-primary-500 text-white py-3 rounded-xl font-medium">+ Добавить пользователя</button>
      </div>
    </div>
    <UserForm v-if="showForm" :user="editTarget" :shops="shops" @close="showForm = false" @save="saveUser" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAppStore } from '../stores/app'
import AppHeader from '../components/common/AppHeader.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import UserForm from '../components/superadmin/UserForm.vue'

const appStore = useAppStore()
const users = ref([])
const shops = ref([])
const loading = ref(true)
const showForm = ref(false)
const editTarget = ref(null)

const roleLabels = { super_admin: 'Супер-админ', shop_admin: 'Администратор', director: 'Директор' }
function roleLabel(r) { return roleLabels[r] || r }

onMounted(load)

async function load() {
  loading.value = true
  try {
    const [usrs, shs] = await Promise.all([api.get('/users'), api.get('/shops')])
    users.value = usrs.data
    shops.value = shs.data
  } finally { loading.value = false }
}

function editUser(u) { editTarget.value = u; showForm.value = true }

async function saveUser(data) {
  try {
    if (editTarget.value) await api.put(`/users/${editTarget.value.id}`, data)
    else await api.post('/users', data)
    showForm.value = false
    appStore.showToast('Сохранено')
    await load()
  } catch (e) { appStore.showToast(e.response?.data?.detail || 'Ошибка', 'error') }
}

async function deleteUser(id) {
  if (!confirm('Удалить пользователя?')) return
  try { await api.delete(`/users/${id}`); await load(); appStore.showToast('Удалено') }
  catch (e) { appStore.showToast('Ошибка', 'error') }
}
</script>
