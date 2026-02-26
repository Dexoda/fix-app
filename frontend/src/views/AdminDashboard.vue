<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader :title="shopName" />
    <div class="flex-1 overflow-y-auto p-4">
      <LoadingSpinner v-if="loading" />
      <div v-else-if="employees.length === 0" class="text-center py-12 text-gray-400">
        <p class="text-4xl mb-2">👤</p>
        <p>Нет сотрудников</p>
      </div>
      <div v-else class="flex flex-col gap-4">
        <EmployeeCard
          v-for="emp in employees"
          :key="emp.id"
          :employee="emp"
          @photo="handlePhoto"
          @video="handleVideo"
          @no-bag="handleNoBag"
        />
      </div>
    </div>
    <CameraCapture ref="photoCapture" accept="image/*" capture="environment" @file-selected="uploadPhoto" />
    <CameraCapture ref="videoCapture" accept="video/*" capture="environment" @file-selected="uploadVideo" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import { useAuthStore } from '../stores/auth'
import { useAppStore } from '../stores/app'
import AppHeader from '../components/common/AppHeader.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import EmployeeCard from '../components/admin/EmployeeCard.vue'
import CameraCapture from '../components/admin/CameraCapture.vue'

const auth = useAuthStore()
const appStore = useAppStore()
const employees = ref([])
const loading = ref(true)
const photoCapture = ref(null)
const videoCapture = ref(null)
const selectedEmployee = ref(null)

const shopName = computed(() => auth.user?.shop_id ? 'Мой магазин' : 'Fix App')

onMounted(async () => {
  try {
    const { data } = await api.get('/employees')
    employees.value = data.filter(e => e.is_active)
  } catch (e) {
    appStore.showToast('Ошибка загрузки сотрудников', 'error')
  } finally {
    loading.value = false
  }
})

function handlePhoto(emp) {
  selectedEmployee.value = emp
  photoCapture.value.open()
}

function handleVideo(emp) {
  selectedEmployee.value = emp
  videoCapture.value.open()
}

async function handleNoBag(emp) {
  try {
    await api.post('/records/no-bag', { employee_id: emp.id, shop_id: emp.shop_id })
    appStore.showToast('✓ Отмечено: без сумки')
  } catch (e) {
    appStore.showToast('Ошибка', 'error')
  }
}

async function uploadPhoto(file) {
  await uploadFile(file, selectedEmployee.value)
}

async function uploadVideo(file) {
  await uploadFile(file, selectedEmployee.value)
}

async function uploadFile(file, emp) {
  if (!emp) return
  const formData = new FormData()
  formData.append('file', file)
  formData.append('employee_id', emp.id)
  formData.append('shop_id', emp.shop_id)
  try {
    await api.post('/records/upload', formData, { headers: { 'Content-Type': 'multipart/form-data' } })
    appStore.showToast('✓ Успешно загружено')
  } catch (e) {
    appStore.showToast(e.response?.data?.detail || 'Ошибка загрузки', 'error')
  }
}
</script>
