<template>
    <div id="jiemian" class="app-container">
      <!-- 边栏 -->
      <div class="sidebar">
        <button @click="currentComponent = 'ComponentA'">显示组件A</button>
        <button @click="currentComponent = 'ComponentB'">显示组件B</button>
        <button @click="currentComponent = 'ComponentC'">显示组件C</button>
      </div>
      
      <!-- 主内容区域 -->
      <div class="content">
        <component :is="currentComponent"></component>
      </div>
    </div>
  </template>
  
  <script>
  // 创建组件A
  const ComponentA = {
    template: `<div><h2>这是组件 A</h2><p>这里是组件A的内容</p></div>`,
  };
  
  // 创建组件B
  const ComponentB = {
    template: `<div><h2>这是组件 B</h2><p>这里是组件B的内容</p></div>`,
  };
  
  // 创建组件C
  const ComponentC = {
    template: `<div><h2>这是组件 C</h2><p>这里是组件C的内容</p></div>`,
  };
  
  export default {
    name: 'JiemianComponent',
    components: {
      ComponentA,
      ComponentB,
      ComponentC,
    },
    data() {
      return {
        currentComponent: 'ComponentA', // 默认显示组件A
      };
    },
  };
  </script>
  
  <style>
  /* 基本样式 */
  .app-container {
    display: flex;
    height: 100vh;
    font-family: Arial, sans-serif;
  }
  
  .sidebar {
    width: 200px;
    background-color: #f4f4f4;
    padding: 10px;
    border-right: 1px solid #ccc;
  }
  
  .sidebar button {
    display: block;
    width: 100%;
    margin-bottom: 10px;
    padding: 10px;
    background-color: #007bff;
    color: white;
    border: none;
    cursor: pointer;
  }
  
  .sidebar button:hover {
    background-color: #0056b3;
  }
  
  .content {
    flex: 1;
    padding: 20px;
  }
  </style>
  