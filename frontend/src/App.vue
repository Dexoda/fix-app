<template>
  <div class="min-h-screen">
    <Toast />
    <router-view />
  </div>
</template>

<script setup>
import Toast from './components/common/Toast.vue'
</script>
