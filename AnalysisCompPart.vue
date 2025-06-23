<template>
    <div class="direct-part">
      <!-- 简略模式：只显示提示文字 -->

  
      <!-- 详细模式：展示整个组件结构 -->
      
            <CompPartFull />
      
    </div>
  </template>
  
  <script setup>
  import { defineAsyncComponent, nextTick, watch } from 'vue'
  
  // 引入完整内容组件（从原始代码中抽离）
  const CompPartFull = defineAsyncComponent(() => import('./CompPartFull.vue'))
  
  const props = defineProps({
    collapsed: Boolean
  })
  
  // 监听展开后自动触发图表重绘逻辑（延迟让 DOM 完全展开）
  watch(() => props.collapsed, (newVal) => {
    if (!newVal) {
      nextTick(() => {
        setTimeout(() => {
          // CompPartFull 会在 mounted 中自行触发绘图
          const evt = new Event('comp-resize')
          window.dispatchEvent(evt)
        }, 400)
      })
    }
  })
  </script>
  
  <style scoped>
  .direct-part {
    width: 100%;
    height: 100%;
    padding: 10px;
    box-sizing: border-box;
  }
  
  .summary-text {
    font-size: 16px;
    color: #666;
    font-style: italic;
    text-align: center;
    background-color: #f4f4f4;
    border: 1px dashed #ccc;
    padding: 30px;
    border-radius: 6px;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  </style>
  