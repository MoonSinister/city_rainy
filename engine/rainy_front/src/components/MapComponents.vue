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
      heatmap: null, // 热力图实例
      isHeatmapReady: false, // 热力图是否初始化完成
      infoWindow: null, // 信息框实例
    };
  },
  methods: {
    // 初始化高德地图
    initMap() {
      if (typeof AMap === "undefined") {
        console.error("高德地图 API 加载失败，请检查 index.html 配置的 script 标签。");
        return;
      }

      // 初始化 3D 地图实例
      this.map = new AMap.Map("container", {
        viewMode: "3D", // 切换为 3D 模式
        zoom: 12,
        center: [117.190182, 39.11],
        pitch: 60,
        rotation: 0,
      });

      this.map.setFeatures(["bg", "road", "building", "land"]); // 显示建筑物、道路、地形等底图

      // 加载建筑物和热力图插件
      this.map.plugin(["AMap.Buildings", "AMap.HeatMap"], () => {
        const buildings = new AMap.Buildings({
          zooms: [15, 20],
          zIndex: 10,
          heightFactor: 2,
        });
        this.map.add(buildings);

        this.heatmap = new AMap.HeatMap(this.map, {
          radius: 5,
          opacity: [0.1, 0.8],
          gradient: {
            0.1: "blue",
            0.5: "green",
            0.9: "red",
          },
        });

        this.isHeatmapReady = true;
        this.startAutoUpdate();
      });

      // 初始化信息框
      this.infoWindow = new AMap.InfoWindow({
        offset: new AMap.Pixel(0, -30), // 信息框的偏移
      });
    },

    // 定时更新地图数据
    startAutoUpdate() {
      this.updateMap();
      setInterval(() => {
        this.updateMap();
      }, 1000);
    },

    // 获取数据并更新地图
    async updateMap() {
      try {
        const response = await axios.get("http://127.0.0.1:5000/get_data");
        const { data, flood_points } = response.data;

        this.updateMarkers(data); // 更新散点标记

        if (this.isHeatmapReady) {
          this.updateHeatmap(flood_points);
        } else {
          console.warn("热力图尚未初始化，稍后再尝试更新。");
        }
      } catch (error) {
        console.error("获取数据失败：", error);
      }
    },

    // 平滑移动标记点
    moveMarker(marker, targetPosition) {
      const start = marker.getCenter(); // 获取当前点的位置
      const end = targetPosition; // 目标位置
      const steps = 120; // 动画帧数，越大越平滑
      let currentStep = 0;

      // 每一步的经度和纬度变化量
      const deltaLng = (end[0] - start.getLng()) / steps;
      const deltaLat = (end[1] - start.getLat()) / steps;

      const animate = () => {
        if (currentStep < steps) {
          currentStep++;
          const nextLng = start.getLng() + deltaLng * currentStep;
          const nextLat = start.getLat() + deltaLat * currentStep;

          marker.setCenter([nextLng, nextLat]); // 更新位置
          requestAnimationFrame(animate); // 继续下一帧
        }
      };

      animate();
    },

    // 更新地图上的标记点
    updateMarkers(newData) {
      newData.forEach((newCoordinate, index) => {
        // 如果点已存在，则平滑移动
        if (this.markers[index]) {
          this.moveMarker(this.markers[index], newCoordinate);
        } else {
          // 如果点不存在，则直接添加新点
          const circleMarker = new AMap.CircleMarker({
            center: newCoordinate, // 初始位置
            radius: 6, // 圆点半径
            strokeColor: "#fff", // 描边颜色
            strokeWeight: 2, // 描边宽度
            strokeOpacity: 1, // 描边透明度
            fillColor: "#007BFF", // 填充颜色
            fillOpacity: 0.8, // 填充透明度
            zIndex: 10, // 层级
          });

          circleMarker.setMap(this.map); // 添加到地图上
          this.addInfoWindow(circleMarker, newCoordinate); // 为新点添加信息框功能
          this.markers.push(circleMarker); // 保存到 markers 数组中
        }
      });

      // 如果新点数量小于现有点数量，移除多余的点
      if (newData.length < this.markers.length) {
        const excessMarkers = this.markers.splice(newData.length);
        excessMarkers.forEach((marker) => marker.setMap(null));
      }
    },

    // 添加信息框功能
    addInfoWindow(marker, coordinate) {
      marker.on("click", () => {
        const content = `
          <div style="padding: 5px;">
            <p><strong>经度：</strong>${coordinate[0]}</p>
            <p><strong>纬度：</strong>${coordinate[1]}</p>
          </div>
        `;

        this.infoWindow.setContent(content); // 设置信息框内容
        this.infoWindow.open(this.map, marker.getCenter()); // 在标记点的位置打开信息框
      });
    },

    // 更新热力图
    updateHeatmap(flood_points) {
      if (!this.map || !this.heatmap) {
        console.error("热力图尚未初始化！");
        return;
      }

      const heatData = flood_points.map((point) => ({
        lng: point.longitude,
        lat: point.latitude,
        count: point.depth,
      }));

      this.heatmap.setDataSet({
        data: heatData,
        max: 1,
      });
    },

    // 清除地图上的标记点
    clearMarkers() {
      this.markers.forEach((marker) => {
        marker.setMap(null);
      });
      this.markers = [];
    },
  },
  mounted() {
    this.initMap();
  },
};
</script>

<style scoped>
#container {
  width: 100%;
  height: 500px;
}
</style>
