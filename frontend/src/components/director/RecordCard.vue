<template>
  <div class="bg-white rounded-xl shadow overflow-hidden">
    <div class="relative aspect-square bg-gray-100 flex items-center justify-center">
      <img v-if="record.type === 'photo' && record.file_path" :src="`/uploads/${record.file_path}`" class="w-full h-full object-cover" />
      <div v-else-if="record.type === 'video'" class="flex flex-col items-center text-gray-500">
        <span class="text-4xl">🎥</span>
        <span class="text-xs mt-1">Видео</span>
      </div>
      <div v-else class="flex flex-col items-center text-red-400">
        <span class="text-4xl">❌</span>
        <span class="text-xs mt-1">Без сумки</span>
      </div>
      <div v-if="record.checked_at" class="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded-full">✓</div>
    </div>
    <div class="p-2">
      <p class="text-xs font-medium text-gray-900 truncate">{{ record.employee_name }}</p>
      <p class="text-xs text-gray-500">{{ formatTime(record.created_at) }}</p>
      <div class="flex gap-1 mt-2">
        <button v-if="!record.checked_at" @click="$emit('check', record)" class="flex-1 bg-primary-500 text-white text-xs py-1 rounded-lg">Проверено</button>
        <a v-if="record.file_path" :href="`/uploads/${record.file_path}`" download class="flex-1 bg-gray-100 text-gray-700 text-xs py-1 rounded-lg text-center">Скачать</a>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({ record: Object })
defineEmits(['check'])
function formatTime(dt) {
  return new Date(dt).toLocaleString('ru-RU', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })
}
</script>
