<template>
  <div class="container">
    

    <div class="content">
      <DirectPart v-if="active === 'direct'" />
      <CompPart v-if="active === 'comp'" />
      <!-- 添加调试信息 -->
      <p>Current active: {{ active }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import DirectPart from './AnalysisDirectPart.vue'
import CompPart from './AnalysisCompPart.vue'

// 确保 active 是响应式的
const active = ref('direct')

// 添加日志验证点击是否触发
const setActive = (part) => {
  console.log('Button clicked, switching to:', part)
  active.value = part
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.button-group {
  padding: 10px;
  background-color: #f4f4f4;
  border-bottom: 1px solid #ddd;
}

button {
  padding: 8px 16px;
  margin-right: 10px;
  border: 1px solid #ddd;
  background-color: white;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.2s ease;
  position: relative; /* 确保按钮可点击 */
  z-index: 1; /* 提升层级，避免被覆盖 */
  font-weight: bold
}

button.active {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

button:hover:not(.active) {
  background-color: #f0f0f0;
}

.content {
  flex: 1;
  overflow: auto;
}
</style>