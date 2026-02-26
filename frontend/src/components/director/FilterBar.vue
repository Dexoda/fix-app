<template>
  <div class="bg-white border-b px-4 py-3 flex flex-col gap-3">
    <div class="grid grid-cols-2 gap-2">
      <select v-model="filters.shop_id" class="input-field text-sm">
        <option value="">Все магазины</option>
        <option v-for="shop in shops" :key="shop.id" :value="shop.id">{{ shop.name }}</option>
      </select>
      <input type="date" v-model="filters.date" class="input-field text-sm" />
    </div>
    <div class="grid grid-cols-2 gap-2">
      <select v-model="filters.employee_id" class="input-field text-sm">
        <option value="">Все сотрудники</option>
        <option v-for="emp in employees" :key="emp.id" :value="emp.id">{{ emp.full_name }}</option>
      </select>
      <select v-model="filters.type" class="input-field text-sm">
        <option value="">Все типы</option>
        <option value="photo">📷 Фото</option>
        <option value="video">🎥 Видео</option>
        <option value="no_bag">❌ Без сумки</option>
      </select>
    </div>
    <button @click="$emit('apply', filters)" class="w-full bg-primary-500 text-white py-2 rounded-xl font-medium text-sm">
      Применить фильтры
    </button>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
const props = defineProps({ shops: Array, employees: Array })
defineEmits(['apply'])
const filters = reactive({ shop_id: '', date: '', employee_id: '', type: '' })
</script>

<style scoped>
.input-field {
  @apply border border-gray-300 rounded-lg px-3 py-2 w-full bg-white focus:outline-none focus:border-primary-500;
}
</style>
