<template>
  <div v-if="show" :class="['toast', type]">
    <i v-if="type === 'success'" class="fas fa-check-circle"></i>
    <i v-else-if="type === 'error'" class="fas fa-exclamation-circle"></i>
    {{ message }}
  </div>
</template>

<script setup>
const props = defineProps({ message: String, type: String, show: Boolean })
</script>

<style scoped>
.toast {
  position: fixed;
  top: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  z-index: 9999;
  padding: 1rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 1rem;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
  animation: fadeInOut 3s forwards;
  display: flex;
  align-items: center;
  gap: 10px;
}
.toast.success {
  background: #e6fbe6;
  color: #2e7d32;
  border: 2px solid #2e7d32;
}
.toast.error {
  background: #fff0f0;
  color: #d32f2f;
  border: 2px solid #d32f2f;
}
@keyframes fadeInOut {
  0% { opacity: 0; top: -50px; }
  10% { opacity: 1; top: 1.5rem; }
  90% { opacity: 1; top: 1.5rem; }
  100% { opacity: 0; top: -50px; }
}
</style>