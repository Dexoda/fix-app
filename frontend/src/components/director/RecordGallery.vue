<template>
  <div v-if="records.length === 0" class="text-center py-12 text-gray-400">
    <p class="text-4xl mb-2">📂</p>
    <p>Записей не найдено</p>
  </div>
  <div v-else class="grid grid-cols-2 gap-3 p-4">
    <RecordCard v-for="record in records" :key="record.id" :record="record" @check="$emit('check', record)" />
  </div>
</template>

<script setup>
import RecordCard from './RecordCard.vue'
defineProps({ records: Array })
defineEmits(['check'])
</script>
