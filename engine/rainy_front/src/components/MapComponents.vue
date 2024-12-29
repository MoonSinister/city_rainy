<template>
  <div>
    <div id="container" style="width: 100%; height: 500px;"></div>
  </div>
</template>

<script>
import axios from "axios";
/* global AMap */
export default {
  name: "App",
  data() {
    return {
      map: null, // 高德地图实例
      markers: [], // 存储地图上的标记点
    };
  },
  methods: {
    // 初始化高德地图
    initMap() {
      // 检测 AMap 对象是否已加载成功
      if (typeof AMap === "undefined") {
        console.error("高德地图 API 加载失败，请检查 index.html 配置的 script 标签。");
        return;
      }

      // 初始化地图实例
      this.map = new AMap.Map("container", {
        zoom: 10, // 地图缩放级别
        center: [117.190182, 39.125596], // 地图初始中心点
      });

      // 开始定时更新地图上的数据
      this.startAutoUpdate();
    },

    // 定时获取数据并更新地图
    startAutoUpdate() {
      this.updateMap(); // 初始化时立即获取一次数据
      setInterval(() => {
        this.updateMap(); // 每隔5秒获取数据
      }, 1000);
    },

    // 从后端获取数据并更新地图
    async updateMap() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_data"); // 调用后端 Flask API
        const data = response.data.data;

        // 清除现有标记点
        this.clearMarkers();

        // 遍历后端返回的坐标数据并添加点
        data.forEach((coordinate) => {
          const marker = new AMap.Marker({
            position: coordinate, // 点的经纬度
            map: this.map, // 将点添加至地图
          });
          this.markers.push(marker);
        });
      } catch (error) {
        console.error("获取数据失败：", error);
      }
    },

    // 清除地图上的所有标记
    clearMarkers() {
      this.markers.forEach((marker) => {
        marker.setMap(null); // 从地图中移除
      });
      this.markers = [];
    },
  },
  mounted() {
    this.initMap(); // 直接初始化地图
  },
};
</script>

<style scoped>
#container {
  width: 100%;
  height: 500px;
}
</style>
