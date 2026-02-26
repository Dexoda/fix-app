<template>
  <button
    v-bind="$attrs"
    :disabled="disabled || loading"
    class="flex items-center justify-center gap-2 rounded-xl font-semibold transition-all active:scale-95"
    :class="[sizeClass, variantClass, { 'opacity-50 cursor-not-allowed': disabled || loading }]"
  >
    <svg v-if="loading" class="animate-spin w-5 h-5" fill="none" viewBox="0 0 24 24">
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
    </svg>
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  variant: { type: String, default: 'primary' },
  size: { type: String, default: 'md' },
  loading: Boolean,
  disabled: Boolean,
})
const variantClass = computed(() => ({
  primary: 'bg-primary-500 hover:bg-primary-600 text-white',
  secondary: 'bg-gray-200 hover:bg-gray-300 text-gray-800',
  danger: 'bg-red-500 hover:bg-red-600 text-white',
  outline: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50',
}[props.variant]))
const sizeClass = computed(() => ({
  sm: 'px-3 py-2 text-sm',
  md: 'px-4 py-3 text-base',
  lg: 'px-6 py-4 text-lg',
  xl: 'px-8 py-5 text-xl w-full',
}[props.size]))
</script>
