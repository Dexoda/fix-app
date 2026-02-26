<template>
  <div class="fixed inset-0 bg-black/50 flex items-end z-50" @click.self="$emit('close')">
    <div class="bg-white rounded-t-2xl w-full p-6 pb-safe">
      <h2 class="text-lg font-bold mb-4">{{ employee ? 'Редактировать сотрудника' : 'Новый сотрудник' }}</h2>
      <form @submit.prevent="submit" class="flex flex-col gap-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">ФИО *</label>
          <input v-model="form.full_name" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500" />
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Магазин *</label>
          <select v-model="form.shop_id" required class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500 bg-white">
            <option value="">Выберите магазин</option>
            <option v-for="shop in shops" :key="shop.id" :value="shop.id">{{ shop.name }}</option>
          </select>
        </div>
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Должность</label>
          <input v-model="form.position" class="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:border-primary-500" />
        </div>
        <div class="flex gap-3">
          <button type="button" @click="$emit('close')" class="flex-1 bg-gray-100 text-gray-700 py-3 rounded-xl font-medium">Отмена</button>
          <button type="submit" class="flex-1 bg-primary-500 text-white py-3 rounded-xl font-medium">Сохранить</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
const props = defineProps({ employee: Object, shops: Array })
const emit = defineEmits(['close', 'save'])
const form = reactive({
  full_name: props.employee?.full_name || '',
  shop_id: props.employee?.shop_id || '',
  position: props.employee?.position || '',
})
function submit() { emit('save', { ...form }) }
</script>
