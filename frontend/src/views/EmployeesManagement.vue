<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader title="Сотрудники" :show-back="true" />
    <div class="flex-1 overflow-y-auto p-4">
      <LoadingSpinner v-if="loading" />
      <div v-else>
        <div class="flex flex-col gap-3 mb-4">
          <div v-for="emp in employees" :key="emp.id" class="bg-white rounded-xl shadow p-4 flex items-center justify-between">
            <div>
              <p class="font-semibold text-gray-900">{{ emp.full_name }}</p>
              <p class="text-sm text-gray-500">{{ emp.position || 'Без должности' }} · {{ shopName(emp.shop_id) }}</p>
            </div>
            <div class="flex gap-2">
              <button @click="editEmp(emp)" class="bg-gray-100 text-gray-700 px-3 py-2 rounded-lg text-sm">✏️</button>
              <button @click="deleteEmp(emp.id)" class="bg-red-50 text-red-500 px-3 py-2 rounded-lg text-sm">🗑️</button>
            </div>
          </div>
        </div>
        <button @click="showForm = true; editTarget = null" class="w-full bg-primary-500 text-white py-3 rounded-xl font-medium">+ Добавить сотрудника</button>
      </div>
    </div>
    <EmployeeForm v-if="showForm" :employee="editTarget" :shops="shops" @close="showForm = false" @save="saveEmp" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAppStore } from '../stores/app'
import AppHeader from '../components/common/AppHeader.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import EmployeeForm from '../components/superadmin/EmployeeForm.vue'

const appStore = useAppStore()
const employees = ref([])
const shops = ref([])
const loading = ref(true)
const showForm = ref(false)
const editTarget = ref(null)

onMounted(load)

async function load() {
  loading.value = true
  try {
    const [emps, shs] = await Promise.all([api.get('/employees'), api.get('/shops')])
    employees.value = emps.data
    shops.value = shs.data
  } finally { loading.value = false }
}

function shopName(id) { return shops.value.find(s => s.id === id)?.name || id }
function editEmp(emp) { editTarget.value = emp; showForm.value = true }

async function saveEmp(data) {
  try {
    if (editTarget.value) await api.put(`/employees/${editTarget.value.id}`, data)
    else await api.post('/employees', data)
    showForm.value = false
    appStore.showToast('Сохранено')
    await load()
  } catch (e) { appStore.showToast('Ошибка', 'error') }
}

async function deleteEmp(id) {
  if (!confirm('Удалить сотрудника?')) return
  try { await api.delete(`/employees/${id}`); await load(); appStore.showToast('Удалено') }
  catch (e) { appStore.showToast('Ошибка', 'error') }
}
</script>
