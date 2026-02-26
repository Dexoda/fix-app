<template>
  <div class="fixed inset-0 bg-black/50 flex items-end z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-t-2xl w-full p-6 pb-safe">
      <h2 class="text-lg font-bold mb-4">{{ shop ? 'Редактировать магазин' : 'Новый магазин' }}</h2>
      <form @submit.prevent="submit" class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Название *</label>
          <input v-model="form.name" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500" placeholder="Название магазина" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Адрес</label>
          <input v-model="form.address" class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500" placeholder="Адрес" />
        </div>
        <div class="flex gap-3">
          <button type="button" @click="$emit('close')" class="flex-1 bg-gray-100 text-gray-700 py-3 rounded-xl font-medium">Отмена</button>
          <button type="submit" :disabled="loading" class="flex-1 bg-primary-500 text-white py-3 rounded-xl font-medium">Сохранить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
const props = defineProps({ shop: Object })
const emit = defineEmits(['close', 'save'])
const loading = ref(false)
const form = reactive({ name: props.shop?.name || '', address: props.shop?.address || '' })
async function submit() {
  loading.value = true
  try {
    emit('save', { ...form })
  } finally {
    loading.value = false
  }
}
</script>
