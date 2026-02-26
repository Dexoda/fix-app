<template>
  <div class="fixed top-4 right-4 z-50 flex flex-col gap-2">
    <transition-group name="toast">
      <div
        v-for="toast in appStore.toasts"
        :key="toast.id"
        class="px-4 py-3 rounded-lg shadow-lg text-white text-sm font-medium max-w-xs"
        :class="toast.type === 'error' ? 'bg-red-500' : 'bg-primary-500'"
      >
        {{ toast.message }}
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { useAppStore } from '../../stores/app'
const appStore = useAppStore()
</script>

<style scoped>
.toast-enter-active, .toast-leave-active { transition: all 0.3s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(100%); }
</style>
