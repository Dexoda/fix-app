<template>
  <div class="bg-white rounded-2xl shadow p-4 flex flex-col gap-3">
    <div class="flex items-center gap-3">
      <div class="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center text-primary-600 font-bold text-lg">
        {{ initials }}
      </div>
      <div>
        <p class="font-semibold text-gray-900">{{ employee.full_name }}</p>
        <p v-if="employee.position" class="text-sm text-gray-500">{{ employee.position }}</p>
      </div>
    </div>
    <div class="grid grid-cols-3 gap-2">
      <button @click="$emit('photo', employee)" class="flex flex-col items-center gap-1 bg-blue-50 hover:bg-blue-100 text-blue-600 rounded-xl py-3 active:scale-95 transition-all">
        <span class="text-2xl">📷</span>
        <span class="text-xs font-medium">Фото</span>
      </button>
      <button @click="$emit('video', employee)" class="flex flex-col items-center gap-1 bg-purple-50 hover:bg-purple-100 text-purple-600 rounded-xl py-3 active:scale-95 transition-all">
        <span class="text-2xl">🎥</span>
        <span class="text-xs font-medium">Видео</span>
      </button>
      <button @click="$emit('no-bag', employee)" class="flex flex-col items-center gap-1 bg-red-50 hover:bg-red-100 text-red-600 rounded-xl py-3 active:scale-95 transition-all">
        <span class="text-2xl">❌</span>
        <span class="text-xs font-medium">Без сумки</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({ employee: Object })
defineEmits(['photo', 'video', 'no-bag'])
const initials = computed(() => {
  const parts = props.employee.full_name.split(' ')
  return parts.map(p => p[0]).slice(0, 2).join('').toUpperCase()
})
</script>
