<template>
  <div class="precipitation-container">
    <!-- 左侧导航菜单边框容器 -->
    <div class="button-border" v-show="!isExpanded">
      <div class="top-image-container">
        <img src="../../assets/images/rain-bus.png" alt="Top Image" class="top-image" />
      </div>
      <h2 class="simulation-title">城市交通系统仿真</h2>
      <ul class="nav-menu">
        <li class="nav-item" @click="showDialog = true">
          <el-icon>
            <Setting />
          </el-icon> 初始化
        </li>
        <li class="nav-item" @click="handleRun">
          <el-icon>
            <CaretRight />
          </el-icon> 系统运行
        </li>
        <li class="nav-item" @click="handlePause">
          <el-icon>
            <VideoPause />
          </el-icon> 暂停系统
        </li>
      </ul>
      <div class="image-container">
        <img src="../../assets/images/runbus.gif" alt="Placeholder" class="bottom-image" />
      </div>
    </div>

    <!-- 初始化设置弹窗 -->
    <el-dialog title="实验设置" v-model="showDialog" width="50%" :close-on-click-modal="false">
      <div class="settings-table-container">
        <div class="text-center text-xl font-bold mb-4" style="color: white;">
          实验设置
        </div>
        <table class="settings-table">
          <thead>
            <tr>
              <th>参数名称</th>
              <th>参数值</th>
              <th>说明</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>agent总数</td>
              <td>190</td>
              <td>模拟的agent数量</td>
            </tr>
            <tr>
              <td>积水点数量</td>
              <td>5782</td>
              <td>积水点数据量</td>
            </tr>
            <tr>
              <td>积水等级</td>
              <td>0-3级</td>
              <td>0级为无风险积水，3级为严重积水</td>
            </tr>
            <tr>
              <td>延误时间阈值</td>
              <td>60分钟</td>
              <td>超过该阈值则公交停运</td>
            </tr>
            <tr>
              <td>不调控agent数量</td>
              <td>50</td>
              <td>始终按照原始路线行进</td>
            </tr>
            <tr>
              <td>规则调控agent数量</td>
              <td>70</td>
              <td>基于实时积水数据生成最优路径或基于阈值停运</td>
            </tr>
            <tr>
              <td>LLM调控agent数量</td>
              <td>70</td>
              <td>基于知识库与llm动态调整</td>
            </tr>
            <tr>
              <td>模拟时长</td>
              <td>16h</td>
              <td>降水发生后模拟的时间范围</td>
            </tr>
          </tbody>
        </table>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="showDialog = false">关闭</el-button>
          <el-button type="primary" @click="handleInit">确认初始化</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 3D效果弹窗 -->
    <el-dialog
      :title="selectedIntersection?.name || '3D视图'"
      v-model="show3DWindow"
      width="50%"
      :before-close="close3DWindow"
      :close-on-click-modal="false"
      class="three-d-dialog"
    >
      <div :id="`three-d-map-${selectedIntersection?.name}`" class="three-d-map"></div>
    </el-dialog>

    <div class="center-box" :class="{ 'expanded-map': isExpanded }">
      <div class="map-outer-border">
        <div ref="mapRef" class="map-container" id="map-container"></div>
        <!-- 地图控制按钮（仅在扩展时显示） -->
        <div class="map-controls" v-if="isExpanded">
          <!-- 暂停/开始按钮 -->
          <el-button style="height: 46px; width: 46px" v-if="isPaused" type="success" @click="togglePause" circle>
            <VideoPlay style="width: 18px; height: 18px;" />
          </el-button>
          <el-button style="height: 46px; width: 46px" v-else type="warning" @click="togglePause" circle plain>
            <VideoPause style="width: 18px; height: 18px;" />
          </el-button>
          <!-- 关闭按钮 -->
          <el-button style="height: 46px; width: 46px" type="danger" @click="closeExpanded" circle>
            <Close style="width: 18px; height: 18px;" />
          </el-button>
          <!-- 热力图选项下拉菜单 -->
          <el-dropdown trigger="click" @command="handleHeatmapOption">
            <el-button type="primary" style="height: 46px; padding: 0 15px;">
              热力图选项
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="population">只显示人流热力图</el-dropdown-item>
                <el-dropdown-item command="flood">只显示积水热力图</el-dropdown-item>
                <el-dropdown-item command="hide">隐藏热力图</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
          <!-- 早晚高峰选项下拉菜单 -->
          <el-dropdown trigger="click" @command="handlePeakOption">
            <el-button type="primary" style="height: 46px; padding: 0 15px;">
              高峰时段
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="morning">早高峰</el-dropdown-item>
                <el-dropdown-item command="evening">晚高峰</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>

    <!-- 底部左侧边框 -->
    <div class="bottom-left-box" v-show="!isExpanded">
      <div class="bottom-left-border">
        <h2 class="delay-title">各Agent调控策略</h2>
        <div class="agent-sections">
          <div class="agent-section">
            <div class="agent-header">
              <img src="../../assets/images/people/policyagent.png" alt="Policy Agent" class="agent-image" />
              <h3 class="agent-subtitle">PolicyAgent</h3>
            </div>
            <div class="agent-content">
              <!-- PolicyAgent content placeholder -->
            </div>
          </div>
          <div class="agent-section">
            <div class="agent-header">
              <img src="../../assets/images/people/busdispatching.png" alt="Bus Dispatch Agent" class="agent-image" />
              <h3 class="agent-subtitle">公交调度Agent</h3>
            </div>
            <div class="agent-content">
              <!-- Bus Dispatch Agent content placeholder -->
            </div>
          </div>
          <div class="agent-section">
            <div class="agent-header">
              <img src="../../assets/images/people/informationrelease.png" alt="Policy Release Agent" class="agent-image" />
              <h3 class="agent-subtitle">政策发布Agent</h3>
            </div>
            <div class="agent-content">
              <!-- Policy Release Agent content placeholder -->
            </div>
          </div>
          <div class="agent-section">
            <div class="agent-header">
              <img src="../../assets/images/people/trafficcontrol.png" alt="Traffic Control Agent" class="agent-image" />
              <h3 class="agent-subtitle">交通管制Agent</h3>
            </div>
            <div class="agent-content">
              <!-- Traffic Control Agent content placeholder -->
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="right-panel" v-show="!isExpanded">
      <div class="r-charts-wrapper">
        <div class="r-chart-section">
          <div ref="ringChartRef" class="ring-chart-container"></div>
        </div>
        <div class="r-bottom-section">
          <div ref="combinedChartRef" class="combined-chart-container"></div>
        </div>
      </div>
      <div class="bottom-right-box">
        <div class="bottom-right-border">
          <h2 class="control-title">系统控制</h2>
          <div class="control-container">
            <div class="button-wrapper">
              <el-button type="success" @click="handlePreviousPeriod">上一时段</el-button>
              <el-button type="success" @click="handleNextPeriod">下一时段</el-button>
            </div>
            <div class="slider-wrapper">
              <span class="slider-label">调整系统运行速度</span>
              <el-slider v-model="systemSpeed" :min="1" :max="10" :step="1" show-stops />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, computed, nextTick } from 'vue';
import * as echarts from 'echarts';
import axios from 'axios';
import output from '../../assets/output.json';
import { ElButton, ElDialog, ElSlider, ElDropdown, ElDropdownMenu, ElDropdownItem, ElNotification } from 'element-plus';
import { VideoPlay, VideoPause, Close, Setting, CaretRight } from '@element-plus/icons-vue';

const chartData = ref(null);
const ringChartData = ref(null);
const horizontalBarChartData = ref(null);
const busChartData = ref(null);
const mapData = ref(null);
const areaMatrix = ref(null);
const currentIndex = ref(0);
const timer = ref(null);
const heatmapTimer = ref(null);
const ringChartRef = ref(null);
const horizontalBarChartRef = ref(null);
const combinedChartRef = ref(null);
const mapRef = ref(null);
let ringChartInstance = null;
let horizontalBarChartInstance = null;
let combinedChartInstance = null;
let mapInstance = null;
let markers = [];
let intersectionMarkers = [];
let heatmap = null;
let areaHeatmap = ref(null);
let isHeatmapReady = ref(false);
let infoWindow = null;
const proximityRadius = 50;
const showDialog = ref(false);
const systemSpeed = ref(5);
const isExpanded = ref(false);
const isPaused = ref(false);
const currentPeak = ref('morning');
const isAreaHeatmapInitialized = ref(false);
// 3D窗口相关状态
const show3DWindow = ref(false);
const selectedIntersection = ref(null);
let threeDMapInstance = null;
let threeDMarkers = [];
let threeDHeatmap = null;

const keyIntersections = [
  { name: '下瓦房地铁站路口', lng: 117.222893, lat: 39.1052 },
  { name: '天津大礼堂交叉路口', lng: 117.204362, lat: 39.088580 },
  { name: '天津日报交叉路口', lng: 117.224102, lat: 39.093011 },
  { name: '友谊南路地铁站交叉路口', lng: 117.217662, lat: 39.063736 },
  { name: '第四医院交叉路口', lng: 117.262956, lat: 39.063092 },
  { name: '人民公园交叉路口', lng: 117.215402, lat: 39.103334 },
  { name: '和悦汇商场交叉路口', lng: 117.245566, lat: 39.081352 },
  { name: '陈塘地铁站交叉路口', lng: 117.250551, lat: 39.070809 },
  { name: '河西区中心小学交叉路口', lng: 117.213233, lat: 39.067846 },
  { name: '瑞江花园小区交叉路口', lng: 117.232093, lat: 39.063590 },
  { name: '天津医科大学第二医院交叉路口', lng: 117.218625, lat: 39.084100 },
];

const allDelaysZero = computed(() => {
  if (!horizontalBarChartData.value || !horizontalBarChartData.value.regions) return true;
  return horizontalBarChartData.value.regions.every(item => item.value === 0);
});

const loadAreaMatrix = async () => {
  try {
    const response = await axios.get('./area_matrix.json');
    areaMatrix.value = response.data;
    console.log('area_matrix 加载完成:', areaMatrix.value);
    if (areaMatrix.value.length !== 64) {
      console.warn(`area_matrix.json 包含 ${areaMatrix.value.length} 个块，期望 64 个`);
    }
    if (isHeatmapReady.value) {
      initAreaHeatmap();
    }
  } catch (error) {
    console.error('加载 area_matrix 失败:', error);
    areaMatrix.value = Array(64).fill().map((_, i) => ({
      type: 'commercial',
      lon: [117.17 + (i % 8) * 0.014625, 117.184625 + (i % 8) * 0.014625],
      lat: [39.03 + Math.floor(i / 8) * 0.010875, 39.040875 + Math.floor(i / 8) * 0.010875],
      id: i + 1,
    }));
    console.log('使用模拟数据:', areaMatrix.value);
    if (isHeatmapReady.value) {
      initAreaHeatmap();
    }
  }
};

const generatePopulationHeatData = (peak) => {
  if (!areaMatrix.value || areaMatrix.value.length !== 64) {
    console.warn('areaMatrix 数据无效或块数不为 64，使用默认数据');
    return Array(64).fill().map((_, i) => ({
      lng: 117.17 + (i % 8) * 0.014625,
      lat: 39.03 + Math.floor(i / 8) * 0.010875,
      count: Math.random(),
    }));
  }
  return areaMatrix.value.map(block => {
    const lng = (block.lon[0] + block.lon[1]) / 2;
    const lat = (block.lat[0] + block.lat[1]) / 2;
    let population;
    if (peak === 'morning') {
      const rand = Math.random();
      if (rand < 0.2) {
        population = Math.random() * 0.3;
      } else if (rand < 0.5) {
        population = 0.3 + Math.random() * 0.4;
      } else {
        population = 0.7 + Math.random() * 0.3;
      }
    } else {
      const rand = Math.random();
      if (rand < 0.4) {
        population = Math.random() * 0.3;
      } else if (rand < 0.8) {
        population = 0.3 + Math.random() * 0.4;
      } else {
        population = 0.7 + Math.random() * 0.3;
      }
    }
    return { lng, lat, count: population };
  });
};

const initAreaHeatmap = () => {
  if (!mapInstance || !isHeatmapReady.value || !areaMatrix.value) {
    console.warn('地图、热力图插件或地块数据未初始化，延迟尝试初始化人流热力图');
    setTimeout(initAreaHeatmap, 1000);
    return;
  }
  if (areaHeatmap.value) {
    console.log('人流热力图已存在，更新数据');
    updateAreaHeatmap();
    return;
  }
  console.log('初始化人流热力图');
  areaHeatmap.value = new AMap.HeatMap(mapInstance, {
    radius: 150,
    opacity: [0, 0.8],
    gradient: { 0.1: 'green', 0.5: 'yellow', 0.9: 'orange', 1.0: 'red' },
    zIndex: 20,
  });
  isAreaHeatmapInitialized.value = true;
  areaHeatmap.value.hide();
};

const updateAreaHeatmap = () => {
  if (!areaHeatmap.value || !isAreaHeatmapInitialized.value) {
    console.warn('人流热力图未初始化，尝试重新初始化');
    initAreaHeatmap();
    return;
  }
  const heatData = generatePopulationHeatData(currentPeak.value);
  if (heatData.length !== 64) {
    console.warn(`人流热力图数据包含 ${heatData.length} 个点，期望 64 个`);
  }
  console.log('更新人流热力图数据:', heatData);
  areaHeatmap.value.setDataSet({ data: heatData, max: 1.0 });
};

const handleHeatmapOption = (command) => {
  console.log('热力图切换命令:', command);
  if (!mapInstance) {
    ElNotification({
      title: '错误',
      message: '地图未初始化，请稍后重试',
      type: 'error',
    });
    return;
  }

  if (!isHeatmapReady.value || !heatmap) {
    console.warn('积水热力图未初始化，尝试加载');
    mapInstance.plugin(['AMap.HeatMap'], () => {
      heatmap = new AMap.HeatMap(mapInstance, {
        radius: 25,
        opacity: [0, 0.8],
        gradient: { 0.1: 'green', 0.5: 'yellow', 0.9: 'orange', 1.0: 'red' },
        zIndex: 10,
      });
      isHeatmapReady.value = true;
      console.log('积水热力图插件加载完成');
      heatmap.hide();
      proceedWithHeatmapSwitch(command);
    });
    return;
  }

  if (!areaHeatmap.value || !isAreaHeatmapInitialized.value) {
    console.warn('人流热力图未初始化，尝试初始化');
    initAreaHeatmap();
    setTimeout(() => proceedWithHeatmapSwitch(command), 1000);
    return;
  }

  proceedWithHeatmapSwitch(command);
};

const proceedWithHeatmapSwitch = (command) => {
  if (!heatmap || !areaHeatmap.value) {
    ElNotification({
      title: '错误',
      message: '热力图实例未准备好，请稍后重试',
      type: 'error',
    });
    return;
  }

  switch (command) {
    case 'population':
      areaHeatmap.value.show();
      heatmap.hide();
      if (threeDHeatmap) threeDHeatmap.hide();
      ElNotification({
        title: '成功',
        message: '已显示人流热力图',
        type: 'success',
      });
      break;
    case 'flood':
      heatmap.show();
      areaHeatmap.value.hide();
      if (threeDHeatmap) threeDHeatmap.show();
      ElNotification({
        title: '成功',
        message: '已显示积水热力图',
        type: 'success',
      });
      break;
    case 'hide':
      heatmap.hide();
      areaHeatmap.value.hide();
      if (threeDHeatmap) threeDHeatmap.hide();
      ElNotification({
        title: '成功',
        message: '已隐藏所有热力图',
        type: 'success',
      });
      break;
    default:
      console.warn('未知的热力图命令:', command);
      ElNotification({
        title: '错误',
        message: '无效的热力图选项',
        type: 'error',
      });
  }
};

const handlePeakOption = (command) => {
  currentPeak.value = command;
  updateAreaHeatmap();
  ElNotification({
    title: '成功',
    message: `已切换至${command === 'morning' ? '早高峰' : '晚高峰'}人流热力图`,
    type: 'success',
  });
};

const fetchChartData = async () => {
  try {
    const response = await fetch('http://localhost:5000/data-list');
    const data = await response.json();
    if (data.success && data.data) {
      ringChartData.value = {
        abnormals: data.data.abnormalData.abnormals.map(item => ({ name: item.name, value: item.value })),
      };
      horizontalBarChartData.value = {
        regions: data.data.regionData.regions.slice(0, 8).map(item => ({ name: item.name, value: item.value })),
      };
      busChartData.value = {
        abnormals: data.data.columnData.abnormals.map(item => ({ name: String(item.name), value: item.value })),
      };
      mapData.value = (await axios.get('http://127.0.0.1:5000/get_data_map')).data.data || [];
    } else {
      throw new Error('Invalid data format');
    }
  } catch (error) {
    console.error('获取数据失败:', error);
    ringChartData.value = { abnormals: [{ name: '交通顺畅', value: 0 }, { name: '交通阻塞', value: 0 }] };
    horizontalBarChartData.value = { regions: Array(8).fill(0).map((_, index) => ({ name: `区域${index + 1}`, value: 0 })) };
    busChartData.value = { abnormals: Array(15).fill(0).map((_, index) => ({ name: `${index + 1}`, value: 0 })) };
    await updateMap();
  }
};

const initRingChart = () => {
  if (!ringChartRef.value || !ringChartData.value) return;
  ringChartInstance = echarts.init(ringChartRef.value);
  renderRingChart();
};

const initHorizontalBarChart = () => {
  if (!horizontalBarChartRef.value || !horizontalBarChartData.value) return;
  horizontalBarChartInstance = echarts.init(horizontalBarChartRef.value);
  renderHorizontalBarChart();
};

const initCombinedChart = () => {
  if (!combinedChartRef.value || !busChartData.value) {
    console.warn('combinedChartRef 或 busChartData 未准备好，无法初始化公交线路图表');
    return;
  }
  combinedChartInstance = echarts.init(combinedChartRef.value);
  renderCombinedChart();
};

const renderRingChart = () => {
  if (!ringChartInstance || !ringChartData.value) return;
  const option = {
    title: { text: '内涝风险占比图', textStyle: { color: '#000000', fontSize: 14 }, left: 'center', top: '5%' },
    tooltip: { trigger: 'item' },
    series: [{
      name: '内涝风险',
      type: 'pie',
      radius: ['30%', '65%'],
      center: ['50%', '55%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 1 },
      label: { show: true, position: 'outside', formatter: '{b}: {d}%', color: '#000000', fontSize: 10 },
      emphasis: { label: { show: true, fontSize: 12, fontWeight: 'bold' } },
      data: ringChartData.value.abnormals.map(item => ({ name: item.name, value: item.value })),
      color: ['#40c4ff', '#ff6384'],
    }],
  };
  ringChartInstance.setOption(option);
};

const renderHorizontalBarChart = () => {
  if (!horizontalBarChartInstance || !horizontalBarChartData.value) return;
  const option = {
    title: { text: '延误时间统计', textStyle: { color: '#000000', fontSize: 14 }, left: 'center', top: 10 },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '30%', right: '5%', top: '20%', bottom: '5%', containLabel: false },
    xAxis: { type: 'value', show: false },
    yAxis: {
      type: 'category',
      data: horizontalBarChartData.value.regions.map(item => item.name),
      axisLine: { lineStyle: { color: '#000000' } },
      axisLabel: { color: '#000000', fontSize: 10 },
    },
    series: [
      {
        type: 'bar',
        data: horizontalBarChartData.value.regions.map(item => item.value),
        itemStyle: { color: '#40c4ff' },
        barWidth: '50%',
      },
    ],
  };
  horizontalBarChartInstance.setOption(option);
};

const renderCombinedChart = () => {
  if (!combinedChartInstance || !busChartData.value) {
    console.warn('combinedChartInstance 或 busChartData 未准备好，无法渲染公交线路图表');
    return;
  }
  const names = busChartData.value.abnormals.map(item => item.name);
  const values = busChartData.value.abnormals.map(item => item.value);
  const option = {
    title: { text: '公交线路运行情况', textStyle: { color: '#000000', fontSize: 14 }, left: 'center', top: 5 },
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { data: ['公交线路运行情况'], top: 25, textStyle: { color: '#000000' } },
    grid: { left: '10%', right: '10%', bottom: '15%', top: '15%', containLabel: true },
    xAxis: [
      {
        type: 'category',
        data: names,
        axisLine: { lineStyle: { color: '#000000' } },
        axisLabel: { color: '#000000', fontSize: 10, rotate: 45 },
      },
    ],
    yAxis: [
      {
        type: 'value',
        name: '数量',
        nameTextStyle: { color: '#000000' },
        axisLine: { lineStyle: { color: '#000000' } },
        axisLabel: { color: '#000000' },
        splitLine: { lineStyle: { color: '#d9d9d9' } },
      },
    ],
    series: [
      {
        name: '公交线路运行情况',
        type: 'bar',
        emphasis: { focus: 'series' },
        data: values,
        itemStyle: { color: '#4b5cc4' },
      },
    ],
  };
  combinedChartInstance.setOption(option);
};

const initMap = () => {
  if (!mapRef.value || typeof AMap === 'undefined') {
    console.error('高德地图API加载失败，尝试延迟重试');
    setTimeout(initMap, 1000);
    return;
  }
  console.log('初始化地图');
  mapInstance = new AMap.Map('map-container', {
    viewMode: '2D',
    zoom: 14,
    center: [117.2285, 39.0735],
    pitch: 0,
    rotation: 0,
  });
  mapInstance.setFeatures(['bg', 'road', 'land']);
  mapInstance.plugin(['AMap.HeatMap'], () => {
    console.log('高德地图热力图插件加载完成');
    heatmap = new AMap.HeatMap(mapInstance, {
      radius: 25,
      opacity: [0, 0.8],
      gradient: { 0.1: 'green', 0.5: 'yellow', 0.9: 'orange', 1.0: 'red' },
      zIndex: 10,
    });
    isHeatmapReady.value = true;
    heatmap.hide();
    if (areaMatrix.value) {
      initAreaHeatmap();
    }
  });
  infoWindow = new AMap.InfoWindow({ offset: new AMap.Pixel(0, -30) });
  loadAreaMatrix();
};

const checkWebGLSupport = () => {
  const canvas = document.createElement('canvas');
  const supportsWebGL = !!(canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
  if (!supportsWebGL) {
    console.error('浏览器不支持WebGL，无法显示3D效果');
    ElNotification({
      title: '错误',
      message: '当前浏览器不支持3D效果，请使用支持WebGL的浏览器',
      type: 'error',
    });
  }
  return supportsWebGL;
};

const init3DMap = (intersection) => {
  if (typeof AMap === 'undefined') {
    console.error('高德地图API未加载，无法初始化3D地图');
    ElNotification({
      title: '错误',
      message: '高德地图API加载失败，请检查网络',
      type: 'error',
    });
    return;
  }
  if (!checkWebGLSupport()) return;
  const containerId = `three-d-map-${intersection.name}`;
  nextTick(() => {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`3D地图容器 ${containerId} 未找到`);
      return;
    }
    threeDMapInstance = new AMap.Map(containerId, {
      viewMode: '3D',
      zoom: 17,
      center: [intersection.lng, intersection.lat],
      pitch: 60,
      rotation: 0,
      features: ['bg', 'road', 'building'],
    });
    threeDMapInstance.plugin(['AMap.Buildings', 'AMap.HeatMap'], () => {
      const buildings = new AMap.Buildings({ zooms: [15, 20], zIndex: 10, heightFactor: 3 });
      threeDMapInstance.add(buildings);
      threeDHeatmap = new AMap.HeatMap(threeDMapInstance, {
        radius: 25,
        opacity: [0, 0.8],
        gradient: { 0.1: 'green', 0.5: 'yellow', 0.9: 'orange', 1.0: 'red' },
        zIndex: 10,
      });
      threeDHeatmap.hide(); // 默认隐藏积水热力图
      console.log(`3D地图已为 ${intersection.name} 初始化`);
      addBusMarkersTo3DMap(intersection);
      update3DHeatmap(intersection, lastFloodPoints.value);
    });
  });
};

const addBusMarkersTo3DMap = (intersection) => {
  clear3DMarkers();
  const radiusInDegrees = 0.0018; // 约200米
  markers.forEach(marker => {
    const position = marker.getCenter();
    const lng = position.getLng();
    const lat = position.getLat();
    if (
      lng >= intersection.lng - radiusInDegrees &&
      lng <= intersection.lng + radiusInDegrees &&
      lat >= intersection.lat - radiusInDegrees &&
      lat <= intersection.lat + radiusInDegrees
    ) {
      const threeDMarker = new AMap.CircleMarker({
        center: [lng, lat],
        radius: 6,
        strokeColor: '#fff',
        strokeWeight: 2,
        strokeOpacity: 1,
        fillColor: marker.getOptions().fillColor,
        fillOpacity: 0.8,
        zIndex: 10,
      });
      threeDMarker.setMap(threeDMapInstance);
      threeDMarkers.push(threeDMarker);
    }
  });
  console.log(`在 ${intersection.name} 的3D地图中添加了 ${threeDMarkers.length} 个公交车标记`);
};

const clear3DMarkers = () => {
  threeDMarkers.forEach(marker => marker.setMap(null));
  threeDMarkers = [];
  console.log('已清除3D地图中的公交车标记');
};

const lastFloodPoints = ref([]); // 存储最新的积水点数据

const update3DHeatmap = (intersection, flood_points) => {
  if (!threeDMapInstance || !threeDHeatmap) {
    console.warn('3D地图或热力图未初始化，无法更新3D积水热力图');
    return;
  }
  if (!flood_points || flood_points.length === 0) {
    console.warn('3D积水数据为空，使用默认数据');
    flood_points = [{ longitude: intersection.lng, latitude: intersection.lat, depth: 0.5 }];
  }
  const radiusInDegrees = 0.0018; // 约200米
  const filteredFloodPoints = flood_points.filter(point =>
    point.longitude >= intersection.lng - radiusInDegrees &&
    point.longitude <= intersection.lng + radiusInDegrees &&
    point.latitude >= intersection.lat - radiusInDegrees &&
    point.latitude <= intersection.lat + radiusInDegrees
  );
  const depths = filteredFloodPoints.map(point => point.depth);
  const minDepth = depths.length > 0 ? Math.min(...depths) : 0;
  const maxDepth = depths.length > 0 ? Math.max(...depths) : 1;
  const sigmoidNormalization = (value, min, max, k = 10) =>
    0.1 / (1 + Math.exp(-k * ((value - min) / (max - min) - 0.5)));
  const heatData = filteredFloodPoints.map(point => ({
    lng: point.longitude,
    lat: point.latitude,
    count: sigmoidNormalization(point.depth, minDepth, maxDepth),
  }));
  threeDHeatmap.setDataSet({ data: heatData, max: 0.1 });
  console.log(`3D积水热力图更新，数据点数: ${heatData.length}`);
};

import trafficControlIcon from '@/assets/images/坐标.png';

const addIntersectionMarkers = () => {
  if (!mapInstance) {
    console.warn('地图未初始化，无法添加交叉口标记');
    return;
  }
  clearIntersectionMarkers();
  keyIntersections.forEach(intersection => {
    const marker = new AMap.Marker({
      position: [intersection.lng, intersection.lat],
      icon: new AMap.Icon({
        size: new AMap.Size(50, 50),
        image: trafficControlIcon,
        imageSize: new AMap.Size(50, 50),
      }),
      offset: new AMap.Pixel(-20, -20),
      zIndex: 100,
      title: intersection.name,
    });
    marker.setMap(mapInstance);
    marker.on('error', () => {
      console.error(`交叉口标记图片加载失败: ${intersection.name}`);
      ElNotification({
        title: '错误',
        message: `交叉口 ${intersection.name} 的标记图片加载失败`,
        type: 'error',
      });
    });
    marker.on('click', () => {
      const content = `<div style="padding: 5px;color:black"><p><strong>交叉口:</strong> ${intersection.name}</p></div>`;
      infoWindow.setContent(content);
      infoWindow.open(mapInstance, marker.getPosition());
      selectedIntersection.value = intersection;
      show3DWindow.value = true;
      nextTick(() => {
        init3DMap(intersection);
      });
      ElNotification({
        title: '3D视图',
        message: `显示 ${intersection.name} 的3D效果图`,
        type: 'success',
      });
    });
    intersectionMarkers.push(marker);
  });
  console.log('已添加交叉口标记:', intersectionMarkers.length);
};

const close3DWindow = () => {
  show3DWindow.value = false;
  selectedIntersection.value = null;
  if (threeDMapInstance) {
    clear3DMarkers();
    if (threeDHeatmap) {
      threeDHeatmap.setMap(null);
      threeDHeatmap = null;
    }
    threeDMapInstance.destroy();
    threeDMapInstance = null;
  }
};

const clearIntersectionMarkers = () => {
  intersectionMarkers.forEach(marker => marker.setMap(null));
  intersectionMarkers = [];
  console.log('已清除交叉口标记');
};

const updateMap = async () => {
  if (isPaused.value) {
    console.log('地图更新暂停');
    return;
  }
  try {
    const response = await axios.get('http://127.0.0.1:5000/get_data_map');
    const { data, flood_points } = response.data;
    lastFloodPoints.value = flood_points; // 保存最新的积水点数据
    updateMarkers(data);
    if (isHeatmapReady.value && heatmap) {
      updateHeatmap(flood_points);
    } else {
      console.warn('热力图尚未初始化，稍后再尝试更新。');
    }
    if (isExpanded.value && intersectionMarkers.length === 0) {
      addIntersectionMarkers();
    }
    if (show3DWindow.value && threeDMapInstance && selectedIntersection.value) {
      addBusMarkersTo3DMap(selectedIntersection.value);
      update3DHeatmap(selectedIntersection.value, flood_points);
    }
  } catch (error) {
    console.error('获取地图数据失败：', error);
  }
};

const updateMarkers = (newData) => {
  newData.forEach((newCoordinate, index) => {
    if (markers[index]) {
      moveMarker(markers[index], newCoordinate);
    } else {
      const circleMarker = new AMap.CircleMarker({
        center: newCoordinate,
        radius: 6,
        strokeColor: '#fff',
        strokeWeight: 2,
        strokeOpacity: 1,
        fillColor: '#FF0000',
        fillOpacity: 0.8,
        zIndex: 10,
      });
      circleMarker.setMap(mapInstance);
      addInfoWindow(circleMarker, newCoordinate[3]);
      markers.push(circleMarker);
    }
    const isInProximity = output.some(point => newCoordinate[2] !== 0);
    let fillColor = newCoordinate[2] === -1 ? '#FF0000' : (isInProximity ? '#FFFF00' : '#00FF00');
    markers[index].setOptions({ fillColor });
  });
  if (newData.length < markers.length) {
    const excessMarkers = markers.splice(newData.length);
    excessMarkers.forEach(marker => marker.setMap(null));
  }
};

const moveMarker = (marker, targetPosition) => {
  const start = marker.getCenter();
  const end = targetPosition;
  const steps = 60;
  let currentStep = 0;
  const deltaLng = (end[0] - start.getLng()) / steps;
  const deltaLat = (end[1] - start.getLat()) / steps;
  const animate = () => {
    if (currentStep < steps) {
      currentStep++;
      const nextLng = start.getLng() + deltaLng * currentStep;
      const nextLat = start.getLat() + deltaLat * currentStep;
      marker.setCenter([nextLng, nextLat]);
      requestAnimationFrame(animate);
    }
  };
  animate();
};

const addInfoWindow = (marker, coordinate) => {
  marker.on('click', () => {
    const content = `<div style="padding: 5px;color:black"><p><strong></strong>${coordinate}</p></div>`;
    infoWindow.setContent(content);
    infoWindow.open(mapInstance, marker.getCenter());
  });
};

const updateHeatmap = (flood_points) => {
  if (!mapInstance || !heatmap) {
    console.error('热力图尚未初始化！');
    return;
  }
  if (!flood_points || flood_points.length === 0) {
    console.warn('积水数据为空，使用默认数据');
    flood_points = [
      { longitude: 117.2285, latitude: 39.0735, depth: 0.5 },
    ];
  }
  const depths = flood_points.map(point => point.depth);
  const minDepth = Math.min(...depths);
  const maxDepth = Math.max(...depths);
  const sigmoidNormalization = (value, min, max, k = 10) =>
    0.1 / (1 + Math.exp(-k * ((value - min) / (max - min) - 0.5)));
  const heatData = flood_points.map(point => ({
    lng: point.longitude,
    lat: point.latitude,
    count: sigmoidNormalization(point.depth, minDepth, maxDepth),
  }));
  heatmap.setDataSet({ data: heatData, max: 0.1 });
  console.log('积水数据更新:', heatData.length);
};

const resizeChart = () => {
  if (ringChartInstance) ringChartInstance.resize();
  if (combinedChartInstance) combinedChartInstance.resize();
  if (mapInstance) mapInstance.setFitView();
};

const updateSystem = async () => {
  if (isPaused.value && isExpanded.value) {
    console.log('系统暂停');
    return;
  }
  await fetchChartData();
  if (!ringChartData.value || !horizontalBarChartData.value || !busChartData.value) return;
  const maxLength = busChartData.value.abnormals.length;
  if (currentIndex.value < maxLength - 1) {
    currentIndex.value += 1;
    console.log(currentIndex.value);
  } else {
    currentIndex.value = 0;
  }
  renderRingChart();
  renderHorizontalBarChart();
  renderCombinedChart();
  await updateMap();
};

const handleInit = () => {
  console.log('初始化');
  currentIndex.value = 0;
  fetchChartData().then(() => {
    renderRingChart();
    renderHorizontalBarChart();
    renderCombinedChart();
    updateMap();
  });
  showDialog.value = false;
};

const handleRun = () => {
  console.log('系统运行');
  if (!isExpanded.value) {
    isExpanded.value = true;
    isPaused.value = false;
    if (timer.value) clearInterval(timer.value);
    const intervalTime = 5000 / systemSpeed.value;
    timer.value = setInterval(() => {
      console.log('调用 updateSystem');
      updateSystem();
    }, intervalTime);
    if (heatmapTimer.value) clearInterval(heatmapTimer.value);
    heatmapTimer.value = setInterval(() => {
      updateAreaHeatmap();
    }, 5000);
    addIntersectionMarkers();
  }
};

const handlePause = () => {
  console.log('暂停系统');
  if (!isExpanded.value && timer.value) {
    clearInterval(timer.value);
    timer.value = null;
  }
  if (!isExpanded.value && heatmapTimer.value) {
    clearInterval(heatmapTimer.value);
    heatmapTimer.value = null;
  }
  if (!isExpanded.value) {
    clearIntersectionMarkers();
    close3DWindow();
  }
};

const togglePause = () => {
  console.log('暂停/开始切换');
  isPaused.value = !isPaused.value;
  if (!isPaused.value && isExpanded.value && !timer.value) {
    const intervalTime = 5000 / systemSpeed.value;
    timer.value = setInterval(() => {
      console.log('调用 updateSystem');
      updateSystem();
    }, intervalTime);
    if (!heatmapTimer.value) {
      heatmapTimer.value = setInterval(() => {
        updateAreaHeatmap();
      }, 5000);
    }
    if (intersectionMarkers.length === 0) {
      addIntersectionMarkers();
    }
  } else if (isPaused.value && timer.value) {
    clearInterval(timer.value);
    timer.value = null;
    if (heatmapTimer.value) {
      clearInterval(heatmapTimer.value);
      heatmapTimer.value = null;
    }
  }
};

const closeExpanded = () => {
  console.log('关闭扩展模式');
  isExpanded.value = false;
  isPaused.value = false;
  if (timer.value) {
    clearInterval(timer.value);
    timer.value = null;
  }
  if (heatmapTimer.value) {
    clearInterval(heatmapTimer.value);
    heatmapTimer.value = null;
  }
  clearIntersectionMarkers();
  close3DWindow();
  nextTick(() => {
    resizeChart();
    renderRingChart();
    renderCombinedChart();
    if (mapInstance) {
      mapInstance.setZoomAndCenter(14, [117.2285, 39.0735]);
      mapInstance.setPitch(0);
      mapInstance.setRotation(0);
      mapInstance.setFeatures(['bg', 'road', 'land']);
    }
  });
};

const handlePreviousPeriod = () => {
  console.log('上一时段');
  if (currentIndex.value > 0) {
    currentIndex.value -= 1;
    updateSystem();
  }
};

const handleNextPeriod = () => {
  console.log('下一时段');
  const maxLength = busChartData.value.abnormals.length;
  if (currentIndex.value < maxLength - 1) {
    currentIndex.value += 1;
    updateSystem();
  }
};

watch(systemSpeed, (newSpeed) => {
  if (timer.value) {
    clearInterval(timer.value);
    const intervalTime = 5000 / newSpeed;
    timer.value = setInterval(() => {
      updateSystem();
    }, intervalTime);
  }
});

watch(isExpanded, (newVal, oldVal) => {
  if (!newVal && oldVal) {
    console.log('扩展状态关闭，重新绘制右侧图表');
    renderRingChart();
    renderCombinedChart();
    resizeChart();
    clearIntersectionMarkers();
    close3DWindow();
    if (mapInstance) {
      mapInstance.setZoomAndCenter(14, [117.2285, 39.0735]);
      mapInstance.setPitch(0);
      mapInstance.setRotation(0);
      mapInstance.setFeatures(['bg', 'road', 'land']);
    }
  }
});

onMounted(() => {
  fetchChartData().then(() => {
    initRingChart();
    initHorizontalBarChart();
    initCombinedChart();
    initMap();
    renderCombinedChart();
  }).catch(error => {
    console.error('初始化数据获取失败:', error);
    initRingChart();
    initHorizontalBarChart();
    initCombinedChart();
    initMap();
    renderCombinedChart();
  });
  window.addEventListener('resize', resizeChart);
  loadAreaMatrix();
});

onUnmounted(() => {
  if (ringChartInstance) ringChartInstance.dispose();
  if (horizontalBarChartInstance) horizontalBarChartInstance.dispose();
  if (combinedChartInstance) combinedChartInstance.dispose();
  if (mapInstance) mapInstance.destroy();
  if (areaHeatmap.value) areaHeatmap.value.setMap(null);
  if (threeDMapInstance) {
    clear3DMarkers();
    if (threeDHeatmap) {
      threeDHeatmap.setMap(null);
      threeDHeatmap = null;
    }
    threeDMapInstance.destroy();
  }
  if (timer.value) clearInterval(timer.value);
  if (heatmapTimer.value) clearInterval(heatmapTimer.value);
  clearIntersectionMarkers();
  close3DWindow();
  window.removeEventListener('resize', resizeChart);
});

watch(() => ringChartData.value, () => { if (ringChartData.value) renderRingChart(); });
watch(() => horizontalBarChartData.value, () => { if (horizontalBarChartData.value) renderHorizontalBarChart(); });
watch(() => busChartData.value, () => { if (busChartData.value) renderCombinedChart(); }, { deep: true });
watch(() => mapData.value, () => { if (mapData.value) updateMap(); });
watch(() => areaMatrix.value, (newVal) => {
  console.log('areaMatrix 更新:', newVal);
  if (newVal && isHeatmapReady.value) initAreaHeatmap();
});
</script>

<style scoped>
.precipitation-container {
  width: 99%;
  height: 93vh;
  display: flex;
  background-color: #ffffff;
  position: relative;
  overflow: hidden;
}

.center-box {
  position: absolute;
  top: 5mm;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 55vh;
  z-index: 10;
}

.center-box.expanded-map {
  top: 0;
  left: 0;
  transform: none;
  width: 100%;
  height: 100%;
  z-index: 1000;
}

.map-outer-border {
  width: 100%;
  height: 100%;
  border: 1px solid #d3d3d3;
  box-shadow: 0 0 2mm rgba(128, 128, 128, 0.5);
  padding: 3mm;
  background-color: #ffffff;
  box-sizing: border-box;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
}

.map-controls {
  position: absolute;
  top: 20px;
  right: 20px;
  display: flex;
  gap: 15px;
  z-index: 1010;
  align-items: center;
}

:deep(.el-dropdown .el-button) {
  height: 46px;
  font-size: 14px;
  padding: 0 15px;
  border-radius: 4px;
}

.button-border {
  position: absolute;
  top: 5mm;
  left: 5mm;
  width: 18%;
  height: 55vh;
  border: none;
  background: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 20px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.top-image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 300px;
  margin-bottom: 20px;
}

.top-image {
  width: 98%;
  height: 70%;
  object-fit: cover;
}

.nav-menu {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  font-size: 18px;
  font-family: SimSun, serif;
  font-weight: bold;
  color: #606266;
  border-radius: 6px;
  cursor: pointer;
  background-color: #f5f5f5;
  transition: all 0.3s ease;
}

.simulation-title {
  font-size: 23px;
  font-weight: bold;
  color: #000000;
  text-align: center;
  margin-bottom: 30px;
}

.nav-item:hover {
  background-color: #c0c0c0;
  color: #ffffff;
}

.nav-item:active {
  background-color: #c0c0c0;
}

.nav-item .el-icon {
  margin-right: 12px;
  font-size: 24px;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: flex-end;
  height: 70px;
}

.bottom-image {
  width: 100px;
  height: 60px;
  object-fit: cover;
}

.bottom-left-box {
  position: absolute;
  top: calc(55vh + 10mm);
  left: 5mm;
  right: 25%;
  width: 79%;
  height: 33vh;
  z-index: 5;
}

.bottom-left-border {
  width: 100%;
  height: 100%;
  border: 1px solid #d3d3d3;
  box-shadow: 0 0 2mm rgba(128, 128, 128, 0.5);
  padding: 3mm;
  background-color: #ffffff;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.delay-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  text-align: center;
  margin-top: 10px;
  margin-bottom: 10px;
}

.agent-sections {
  width: 100%;
  height: 100%;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 0;
}

.agent-section {
  border: 1px dashed #d3d3d3;
  padding: 10px;
  display: flex;
  flex-direction: column;
}

.agent-header {
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}

.agent-image {
  width: 40px;
  height: 40px;
  margin-right: 10px;
  border-radius: 4px;
  object-fit: cover;
}

.agent-subtitle {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.agent-content {
  flex-grow: 1;
  font-size: 14px;
  color: #666;
}

.right-panel {
  width: 20%;
  height: 93vh;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  background-color: #ffffff;
  position: absolute;
  right: 0;
  z-index: 5;
}

.r-charts-wrapper {
  width: 90%;
  height: 55vh;
  border: 1px solid #d3d3d3;
  box-shadow: 0 0 2mm rgba(128, 128, 128, 0.5);
  background-color: #ffffff;
  padding: 3mm;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-top: 5mm;
  margin-right: 5%;
}

.r-chart-section {
  width: 100%;
  height: 40%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
}

.r-bottom-section {
  width: 100%;
  height: 60%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #ffffff;
}

.ring-chart-container,
.combined-chart-container {
  width: 100%;
  height: 100%;
}

.bottom-right-box {
  width: 90%;
  height: 33vh;
  z-index: 5;
  margin-right: 5%;
  margin-top: 5mm;
}

.bottom-right-border {
  width: 100%;
  height: 100%;
  border: 1px solid #d3d3d3;
  box-shadow: 0 0 2mm rgba(128, 128, 128, 0.5);
  padding: 3mm;
  background-color: #ffffff;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.control-title {
  font-size: 23px;
  font-weight: bold;
  color: #000000;
  text-align: center;
  margin-bottom: 10px;
}

.control-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-evenly;
  height: 100%;
  width: 100%;
}

.button-wrapper {
  display: flex;
  gap: 20px;
}

.slider-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.slider-label {
  font-size: 16px;
  color: #333333;
  margin-bottom: 10px;
}

:deep(.el-slider) {
  width: 80%;
}

.settings-table-container {
  background-color: rgba(30, 41, 59, 0.5);
  padding: 24px;
  border-radius: 8px;
}

.settings-table {
  width: 100%;
  color: white;
  border-collapse: collapse;
  border-spacing: 0;
}

.settings-table th,
.settings-table td {
  padding: 10px;
  text-align: left;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.settings-table th {
  font-weight: bold;
  background-color: rgba(255, 255, 255, 0.1);
}

.settings-table tr:last-child td {
  border-bottom: none;
}

.three-d-map {
  width: 100%;
  height: 500px; /* 固定高度以确保弹窗内地图显示正常 */
}

:deep(.three-d-dialog .el-dialog__body) {
  padding: 0;
}
</style>