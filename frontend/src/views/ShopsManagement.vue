<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader title="Магазины" :show-back="true" />
    <div class="flex-1 overflow-y-auto p-4">
      <LoadingSpinner v-if="loading" />
      <div v-else>
        <div v-if="shops.length === 0" class="text-center py-8 text-gray-400">Нет магазинов</div>
        <div class="flex flex-col gap-3 mb-4">
          <div v-for="shop in shops" :key="shop.id" class="bg-white rounded-xl shadow p-4 flex items-center justify-between">
            <div>
              <p class="font-semibold text-gray-900">{{ shop.name }}</p>
              <p v-if="shop.address" class="text-sm text-gray-500">{{ shop.address }}</p>
            </div>
            <div class="flex gap-2">
              <button @click="editShop(shop)" class="bg-gray-100 text-gray-700 px-3 py-2 rounded-lg text-sm">✏️</button>
              <button @click="deleteShop(shop.id)" class="bg-red-50 text-red-500 px-3 py-2 rounded-lg text-sm">🗑️</button>
            </div>
          </div>
        </div>
        <button @click="showForm = true; editTarget = null" class="w-full bg-primary-500 text-white py-3 rounded-xl font-medium">+ Добавить магазин</button>
      </div>
    </div>
    <ShopForm v-if="showForm" :shop="editTarget" @close="showForm = false" @save="saveShop" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import { useAppStore } from '../stores/app'
import AppHeader from '../components/common/AppHeader.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'
import ShopForm from '../components/superadmin/ShopForm.vue'

const appStore = useAppStore()
const shops = ref([])
const loading = ref(true)
const showForm = ref(false)
const editTarget = ref(null)

onMounted(load)

async function load() {
  loading.value = true
  try { shops.value = (await api.get('/shops')).data } finally { loading.value = false }
}

function editShop(shop) { editTarget.value = shop; showForm.value = true }

async function saveShop(data) {
  try {
    if (editTarget.value) await api.put(`/shops/${editTarget.value.id}`, data)
    else await api.post('/shops', data)
    showForm.value = false
    appStore.showToast('Сохранено')
    await load()
  } catch (e) { appStore.showToast('Ошибка', 'error') }
}

async function deleteShop(id) {
  if (!confirm('Удалить магазин?')) return
  try { await api.delete(`/shops/${id}`); await load(); appStore.showToast('Удалено') }
  catch (e) { appStore.showToast('Ошибка', 'error') }
}
</script>
