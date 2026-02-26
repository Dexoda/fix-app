<template>
  <div>
    <input
      ref="fileInput"
      type="file"
      :accept="accept"
      :capture="capture"
      class="hidden"
      @change="handleFile"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  accept: { type: String, default: 'image/*' },
  capture: { type: String, default: 'environment' },
})
const emit = defineEmits(['file-selected'])
const fileInput = ref(null)

function open() {
  fileInput.value.click()
}

function handleFile(event) {
  const file = event.target.files[0]
  if (file) {
    emit('file-selected', file)
    event.target.value = ''
  }
}

defineExpose({ open })
</script>
