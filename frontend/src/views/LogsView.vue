<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader title="Журнал действий" :show-back="true" />
    <div class="flex-1 overflow-y-auto p-4">
      <LoadingSpinner v-if="loading" />
      <div v-else>
        <div v-if="logs.length === 0" class="text-center py-8 text-gray-400">Нет записей</div>
        <div class="flex flex-col gap-2">
          <div v-for="log in logs" :key="log.id" class="bg-white rounded-xl p-4 shadow-sm">
            <div class="flex items-start justify-between">
              <div>
                <p class="font-medium text-gray-900">{{ actionLabel(log.action) }}</p>
                <p class="text-sm text-gray-500">{{ log.user_name }}</p>
              </div>
              <span class="text-xs text-gray-400">{{ formatTime(log.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'
import AppHeader from '../components/common/AppHeader.vue'
import LoadingSpinner from '../components/common/LoadingSpinner.vue'

const logs = ref([])
const loading = ref(true)

onMounted(async () => {
  try { logs.value = (await api.get('/logs')).data } finally { loading.value = false }
})

const actionMap = { upload: 'Загрузка файла', no_bag: 'Без сумки', check: 'Проверено' }
function actionLabel(a) { return actionMap[a] || a }
function formatTime(dt) {
  return new Date(dt).toLocaleString('ru-RU')
}
</script>
