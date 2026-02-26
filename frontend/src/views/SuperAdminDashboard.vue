<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <AppHeader title="Супер-Админ" />
    <div class="flex-1 overflow-y-auto p-4">
      <div class="grid grid-cols-2 gap-4">
        <router-link to="/superadmin/shops" class="bg-white rounded-2xl p-6 shadow flex flex-col items-center gap-3 active:scale-95 transition-all">
          <span class="text-4xl">🏪</span>
          <span class="font-semibold text-gray-800">Магазины</span>
        </router-link>
        <router-link to="/superadmin/employees" class="bg-white rounded-2xl p-6 shadow flex flex-col items-center gap-3 active:scale-95 transition-all">
          <span class="text-4xl">👤</span>
          <span class="font-semibold text-gray-800">Сотрудники</span>
        </router-link>
        <router-link to="/superadmin/users" class="bg-white rounded-2xl p-6 shadow flex flex-col items-center gap-3 active:scale-95 transition-all">
          <span class="text-4xl">👥</span>
          <span class="font-semibold text-gray-800">Пользователи</span>
        </router-link>
        <router-link to="/superadmin/logs" class="bg-white rounded-2xl p-6 shadow flex flex-col items-center gap-3 active:scale-95 transition-all">
          <span class="text-4xl">📋</span>
          <span class="font-semibold text-gray-800">Логи</span>
        </router-link>
        <router-link to="/director" class="bg-primary-50 rounded-2xl p-6 shadow flex flex-col items-center gap-3 col-span-2 active:scale-95 transition-all border border-primary-200">
          <span class="text-4xl">📸</span>
          <span class="font-semibold text-primary-700">Просмотр записей</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import AppHeader from '../components/common/AppHeader.vue'
</script>
