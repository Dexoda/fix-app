<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader title="Директор: Записи" />
    <FilterBar :shops="shops" :employees="employees" @apply="applyFilters" />
    <div class="flex-1 overflow-y-auto">
      <LoadingSpinner v-if="loading" />
      <RecordGallery v-else :records="records" @check="checkRecord" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAppStore } from '../stores/app'
import AppHeader from '../components/common/AppHeader.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import FilterBar from '../components/director/FilterBar.vue'
import RecordGallery from '../components/director/RecordGallery.vue'

const appStore = useAppStore()
const records = ref([])
const shops = ref([])
const employees = ref([])
const loading = ref(true)
const currentFilters = ref({})

onMounted(async () => {
  try {
    const [shopsRes, empsRes] = await Promise.all([api.get('/shops'), api.get('/employees')])
    shops.value = shopsRes.data
    employees.value = empsRes.data
    await loadRecords()
  } catch (e) {
    appStore.showToast('Ошибка загрузки', 'error')
    loading.value = false
  }
})

async function loadRecords(filters = {}) {
  loading.value = true
  try {
    const params = {}
    if (filters.shop_id) params.shop_id = filters.shop_id
    if (filters.date) params.date_filter = filters.date
    if (filters.employee_id) params.employee_id = filters.employee_id
    if (filters.type) params.type = filters.type
    const { data } = await api.get('/records', { params })
    records.value = data
  } catch (e) {
    appStore.showToast('Ошибка загрузки записей', 'error')
  } finally {
    loading.value = false
  }
}

function applyFilters(filters) {
  currentFilters.value = filters
  loadRecords(filters)
}

async function checkRecord(record) {
  try {
    const { data } = await api.post(`/records/${record.id}/check`)
    const idx = records.value.findIndex(r => r.id === record.id)
    if (idx !== -1) records.value[idx] = data
    appStore.showToast('✓ Запись отмечена как проверенная')
  } catch (e) {
    appStore.showToast('Ошибка', 'error')
  }
}
</script>
