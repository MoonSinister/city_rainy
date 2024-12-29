
<template>
  <div>
    <h1>实时数据更新</h1>
    <p>当前时间：{{ currentTime }}</p>
  </div>
</template>

<script>
export default {
  name: 'RealTimeUpdate', // 组件名称
  data() {
    return {
      currentTime: '',
    };
  },
  mounted() {
    // 定时器：每秒请求一次后端接口
    this.fetchData();
    setInterval(this.fetchData, 1000); // 每 1 秒轮询一次
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('http://127.0.0.1:5000/get_data');
        const data = await response.json();
        this.currentTime = data.time;
      } catch (error) {
        console.error('获取数据失败:', error);
      }
    },
  },
};
</script>
