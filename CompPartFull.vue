<template>
  <div style="width: 99%; min-width:1200px; display: flex;height: 102%;">
    <el-card style="width: 100%; height: 98%">
      <div style="display: flex; flex-direction: column; width: 100%; height: 100%; font-size: 20px; margin-top: 1rem">
        <div style="display: flex; width: 100%; justify-content: space-between">
          <div style="display: flex; font-family: 'Microsoft YaHei',serif; font-weight: bold;font-size: 22px">
            观察分析界面
          </div>
          <div>
            <el-tooltip content="刷新数据" placement="bottom" effect="light">
              <el-button type="warning" @click="updateCharts()">
                <el-icon size="20"><Refresh/></el-icon>
              </el-button>
            </el-tooltip>
          </div>
        </div>
        <!-- 分割线 -->
        <el-divider></el-divider>
        
        <!-- 分类视图 - 当未选择具体分类时显示 -->
        <div v-if="!selectedCategory" style="display: flex; flex-direction: column; width: 100%;">
          <div style="display: flex; width: 100%; justify-content: space-between; margin-bottom: 1rem;">
            <h3 style="margin: 0;">实验结果分类概览</h3>
            <el-button type="primary" size="small" @click="resetView">返回分类视图</el-button>
          </div>
          
          <!-- 分类统计信息 -->
          <div style="display: flex; width: 100%;">
            <el-descriptions title="" :column="3" border style="width: 98%">
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><DataLine /></el-icon>
                    实验总数
                  </div>
                </template>
                <span style="color: #409EFF">{{totalExperiments}}个</span>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><DataLine /></el-icon>
                    分类数量
                  </div>
                </template>
                {{categories.length}}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><Timer /></el-icon>
                    平均城市运行效率
                  </div>
                </template>
                {{avgSystemEfficiency}}
              </el-descriptions-item>
            </el-descriptions>
          </div>
          
          <!-- 分类扇形图和列表 -->
          <div style="display: flex; width: 100%; margin-top: 1rem;">
            <!-- 左侧扇形图 -->
            <el-card style="width: 50%; margin-right: 1rem;">
              <template #header>
                <div class="card-header">
                  <span>实验结果分类分布</span>
                </div>
              </template>
              <div id="categoryPieChart" style="width: 100%; height: 400px;"></div>
            </el-card>
            
            <!-- 右侧分类列表 -->
            <el-card style="width: 50%;">
              <template #header>
                <div class="card-header">
                  <span>分类列表</span>
                </div>
              </template>
              <el-table :data="categories" style="width: 100%" @row-click="handleCategoryClick">
                <el-table-column prop="name" label="分类名称" width="180" />
                <el-table-column prop="count" label="实验数量" width="120" />
                <el-table-column prop="avgEfficiency" label="平均效率" width="120" />
                <el-table-column prop="description" label="描述" />
              </el-table>
            </el-card>
          </div>
        </div>
        
        <!-- 分类内实验列表 - 当选择了分类但未选择具体实验时显示 -->
        <div v-else-if="selectedCategory && !selectedExperiment" style="display: flex; flex-direction: column; width: 100%;">
          <div style="display: flex; width: 100%; justify-content: space-between; margin-bottom: 1rem;">
            <h3 style="margin: 0;">分类：{{ selectedCategory.name }}</h3>
            <el-button type="primary" size="small" @click="resetView">返回分类视图</el-button>
          </div>
          
          <!-- 分类详细信息 -->
          <div style="display: flex; width: 100%;">
            <el-descriptions title="" :column="3" border style="width: 98%">
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><DataLine /></el-icon>
                    实验数量
                  </div>
                </template>
                <span style="color: #409EFF">{{selectedCategory.count}}个</span>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><DataLine /></el-icon>
                    平均城市运行效率
                  </div>
                </template>
                {{selectedCategory.avgEfficiency}}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><Timer /></el-icon>
                    描述
                  </div>
                </template>
                {{selectedCategory.description}}
              </el-descriptions-item>
            </el-descriptions>
          </div>
          
          <!-- 实验列表 -->
          <el-card style="width: 100%; margin-top: 1rem;">
            <template #header>
              <div class="card-header">
                <span>实验列表</span>
              </div>
            </template>
            <el-table :data="experimentsInCategory" style="width: 100%" @row-click="handleExperimentClick">
              <el-table-column prop="id" label="实验ID" width="120" />
              <el-table-column prop="name" label="实验名称" width="180" />
              <el-table-column prop="efficiency" label="城市运行效率" width="120" />
              <el-table-column prop="riderCount" label="积水消退时间" width="120" />
              <el-table-column prop="orderCount" label="交通恢复率" width="120" />
              <el-table-column prop="runTime" label="决策类型" width="120" />
            </el-table>
          </el-card>
        </div>
        
        <!-- 具体实验数据展示 - 当选择了具体实验时显示 -->
        <div v-else style="display: flex; flex-direction: column; width: 100%;">
          <div style="display: flex; width: 100%; justify-content: space-between; margin-bottom: 1rem;">
            <h3 style="margin: 0;">实验：{{ selectedExperiment.name }}</h3>
            <div>
              <el-button type="primary" size="small" style="margin-right: 10px;" @click="backToCategory">返回分类</el-button>
              <el-button type="warning" size="small" @click="resetView">返回分类视图</el-button>
            </div>
          </div>
          
          <!-- 上方描述框 -->
          <div style="display: flex; width: 100%;">
            <el-descriptions title="" :column="3" border style="width: 98%">
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><DataLine /></el-icon>
                    实验个体数量
                  </div>
                </template>
                <span style="color: #409EFF">190</span>
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><DataLine /></el-icon>
                    交通恢复率
                  </div>
                </template>
                85
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><Timer /></el-icon>
                    系统运行时长
                  </div>
                </template>
                360s
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><Coin/></el-icon>
                    城市运行效率
                  </div>
                </template>
                {{systemEfficiency}}
              </el-descriptions-item>
              <el-descriptions-item>
                <template #label>
                  <div class="cell-item">
                    <el-icon class="iconStyle"><Money/></el-icon>
                    平均效率
                  </div>
                </template>
                {{averageEfficiency}}
              </el-descriptions-item>
            </el-descriptions>
          </div>
          
          <!-- 中间图表区域 -->
          <div style="display: inline; width: 100%; height: calc(100vh - 380px); overflow-y: auto; font-size: 20px">
            <!-- 第一行图表 -->
            <div style="width: 100%; display: flex; margin-top: 2rem; min-width: 1200px">
              <el-card class="chartCard" style="min-width: 650px">
                <template #header>
                  <div class="card-header">
                    <span>交通运行趋势图</span>
                  </div>
                </template>
                <div id="riderChart" class="chartDiv" />
              </el-card>
              <el-card class="chartCard">
                <template #header>
                  <div class="card-header">
                    <span>积水分布热力图</span>
                    <el-select v-model="currentHeatmapState" size="small" @change="updateHeatmapChart" style="margin-left: 10px;">
                      <el-option label="调控前" value="before"></el-option>
                      <el-option label="调控后" value="after"></el-option>
                    </el-select>
                  </div>
                </template>
                <div id="heatmapChart" class="chartDiv" />
              </el-card>
            </div>

            <!-- 第二行图表 -->
            <div style="display: flex; width: 100%; height: 100%; font-size: 20px; margin-top: 1rem; min-width: 1200px;">
              <el-card class="chartCard" style="min-width: 650px">
                <template #header>
                  <div class="card-header">
                    <span>调控方案执行效果图</span>
                  </div>
                </template>
                <div id="systemEfficiencyChart" class="chartDiv"/>
              </el-card>
              <el-card class="chartCard">
                <template #header>
                  <div class="card-header">
                    <span>Agent决策贡献雷达图</span>
                  </div>
                </template>
                <div id="radarChart" class="chartDiv"/>
              </el-card>
            </div>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Coin, DataLine, Money, Refresh, Timer } from "@element-plus/icons";
import * as echarts from "echarts";

export default {
  name: "newAnalysisObservation",
  components: { Refresh, DataLine, Timer, Money, Coin },
  data() {
    return {
      // 基础数据
      riderCount: 100,
      orderCount: 500,
      systemRunTime: 3600,
      systemEfficiency: 85.7,
      averageEfficiency: 76.2,
      
      // 图表实例
      riderChart: null,
      heatmapChart: null,
      systemEfficiencyChart: null,
      radarChart: null,
      categoryPieChart: null,
      
      // 定时器
      timer: null,
      
      // 分类视图数据
      selectedCategory: null,
      selectedExperiment: null,
      totalExperiments: 45,
      avgSystemEfficiency: 78.5,
      
      // 分类数据
      categories: [
        { name: '高效缓解', count: 15, avgEfficiency: 92.3, description: '平均城市运行效率超过90%的实验集合' },
        { name: '中等缓解', count: 20, avgEfficiency: 75.8, description: '平均城市运行效率在70%-90%之间的实验集合' },
        { name: '低效缓解', count: 10, avgEfficiency: 62.4, description: '平均城市运行效率低于70%的实验集合' }
      ],
      
      // 实验数据（按分类）
      experimentsData: {
        '高效缓解': [
          { id: 'HE001', name: '道路拥堵程度低', efficiency: 94.2, riderCount: 120, orderCount: 80, runTime: '快速响应' },
          { id: 'HE002', name: '政策Agent大规模介入', efficiency: 91.5, riderCount: 100, orderCount: 85, runTime: '详细决策' },
          { id: 'HE003', name: '人力资源充足', efficiency: 93.8, riderCount: 110, orderCount: 79, runTime: '反馈决策' }
        ],
        '中等缓解': [
          { id: 'ME001', name: '道路拥堵程度中等', efficiency: 78.5, riderCount: 90, orderCount: 73, runTime: '快速响应' },
          { id: 'ME002', name: '政策Agent中等规模介入', efficiency: 75.2, riderCount: 85, orderCount: 72, runTime: '详细决策' },
          { id: 'ME003', name: '人力资源偏少', efficiency: 76.8, riderCount: 95, orderCount: 69, runTime: '反馈决策' }
        ],
        '低效缓解': [
          { id: 'LE001', name: '道路拥堵程度高', efficiency: 65.3, riderCount: 80, orderCount: 60, runTime: '快速响应' },
          { id: 'LE002', name: '政策Agent少规模介入', efficiency: 62.1, riderCount: 75, orderCount: 59, runTime: '详细决策' },
          { id: 'LE003', name: '人力资源很少', efficiency: 68.7, riderCount: 70, orderCount: 62, runTime: '反馈决策'}
        ]
      },
      
      // 当前分类下的实验列表
      experimentsInCategory: [],
      
      // 城市积水分布图（交通运行趋势）数据
      trafficData: {
        beforeControl: [30, 30, 28, 27, 25, 24, 23, 22, 23, 25, 27, 28, 29, 30, 30, 30], // 调控前车辆平均速度（km/h）
        afterControl: [30, 30, 32, 35, 38, 42, 45, 48, 50, 52, 53, 54, 55, 55, 55, 55] // 调控后车辆平均速度（km/h）
      },
      
      // Agent决策贡献数据
      agentContributions: [
        {
          name: '实验1',
          data: {
            'Policy Agent': 75,
            '公交调控Agent': 60,
            '政策发布Agent': 85,
            '交通管控Agent': 70
          }
        },
        {
          name: '实验2',
          data: {
            'Policy Agent': 65,
            '公交调控Agent': 80,
            '政策发布Agent': 70,
            '交通管控Agent': 75
          }
        }
      ],
      
      // 调控方案执行效果图数据
      efficiencyData: {
        baseline: Array(16).fill(60), // 调控前基线，默认60分
        postIntervention: [60, 60, 62, 65, 70, 75, 80, 85, 88, 90, 92, 93, 94, 95, 95, 95] // 调控后效率
      },
      
      // 积水分布热力图数据
      waterData: {
        beforeControl: this.generateHeatmapData(10, 10, 0.5, 1.0), // 调控前积水深度（0.5-1.0米）
        afterControl: null // 调控后积水深度，初始化时基于beforeControl生成
      },
      currentHeatmapState: 'before' // 当前显示状态：before 或 after
    };
  },
  mounted() {
    // 初始化调控后积水数据，确保数值小于调控前
    this.waterData.afterControl = this.waterData.beforeControl.map(([x, y, val]) => [x, y, val * (0.2 + Math.random() * 0.3)]);
    // 初始化分类视图
    this.resetView();
    this.initCategoryPieChart();
    
    // 模拟数据更新
    this.timer = setInterval(() => {
      this.updateData();
      this.updateCharts();
    }, 5000);
  },
  beforeUnmount() {
    // 清除定时器
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
    
    // 销毁图表实例
    this.riderChart && this.riderChart.dispose();
    this.heatmapChart && this.heatmapChart.dispose();
    this.systemEfficiencyChart && this.systemEfficiencyChart.dispose();
    this.radarChart && this.radarChart.dispose();
    this.categoryPieChart && this.categoryPieChart.dispose();
  },
  methods: {
    // 初始化所有图表
    initCharts() {
      this.initRiderChart(); // 城市积水分布图
      this.initHeatmapChart(); // 积水分布热力图
      this.initSystemEfficiencyChart(); // 调控方案执行效果图
      this.initRadarChart(); // Agent决策贡献雷达图
    },
    
    // 初始化分类扇形图
    initCategoryPieChart() {
      if (this.categoryPieChart) {
        this.categoryPieChart.dispose();
      }
      
      this.categoryPieChart = echarts.init(document.getElementById('categoryPieChart'));
      
      // 准备数据
      const pieData = this.categories.map(category => ({
        name: category.name,
        value: category.count
      }));
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 10,
          data: this.categories.map(category => category.name)
        },
        series: [
          {
            name: '实验分类',
            type: 'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '18',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: pieData
          }
        ]
      };
      
      this.categoryPieChart.setOption(option);
    },
    
    // 处理分类点击
    handleCategoryClick(row) {
      this.selectedCategory = row;
      this.experimentsInCategory = this.experimentsData[row.name] || [];
    },
    
    // 处理实验点击
    handleExperimentClick(row) {
      this.selectedExperiment = row;
      
      // 更新实验数据
      this.riderCount = row.riderCount;
      this.orderCount = row.orderCount;
      this.systemRunTime = row.runTime;
      this.systemEfficiency = row.efficiency;
      this.averageEfficiency = (row.efficiency * 0.9).toFixed(1); // 模拟平均效能
      
      // 初始化图表
      this.$nextTick(() => {
        this.initCharts();
      });
    },
    
    // 返回分类视图
    resetView() {
      this.selectedCategory = null;
      this.selectedExperiment = null;
      this.experimentsInCategory = [];
      
      // 如果在分类视图，初始化扇形图
      this.$nextTick(() => {
        if (document.getElementById('categoryPieChart')) {
          this.initCategoryPieChart();
        }
      });
    },
    
    // 返回分类
    backToCategory() {
      this.selectedExperiment = null;
    },
    
    // 初始化城市积水分布图（原骑手个体图表）
    initRiderChart() {
      this.riderChart = echarts.init(document.getElementById('riderChart'));
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'cross', label: { backgroundColor: '#6a7985' } }
        },
        legend: { data: ['调控前', '调控后'], top: '5%' },
        grid: { left: '10%', right: '10%', top: '15%', bottom: '15%', containLabel: true },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: Array.from({length: 16}, (_, i) => `${i + 1}h`),
          name: '时间'
        },
        yAxis: {
          type: 'value',
          min: 20,
          max: 60,
          name: '车辆平均速度 (km/h)'
        },
        series: [
          {
            name: '调控前',
            type: 'line',
            data: this.trafficData.beforeControl,
            showSymbol: true,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: { width: 1, color: '#999' }
          },
          {
            name: '调控后',
            type: 'line',
            data: this.trafficData.afterControl,
            showSymbol: true,
            symbol: 'circle',
            symbolSize: 6,
            lineStyle: { width: 2, color: '#409EFF' },
            
          }
        ]
      };
      this.riderChart.setOption(option);
    },
    
    // 初始化积水分布热力图（原城市热力图）
    initHeatmapChart() {
      this.heatmapChart = echarts.init(document.getElementById('heatmapChart'));
      const option = {
        tooltip: {
          position: 'top',
          formatter: params => `区域: (${params.data[0] + 1}, ${params.data[1] + 1})<br>积水深度: ${params.data[2].toFixed(2)}米`
        },
        grid: { top: '20%', left: '10%', right: '15%', bottom: '15%' },
        xAxis: {
          type: 'category',
          data: Array.from({length: 10}, (_, i) => `区域${i + 1}`),
          name: '城市区域',
          splitArea: { show: true }
        },
        yAxis: {
          type: 'category',
          data: Array.from({length: 10}, (_, i) => `${i + 1}h`),
          name: '时间',
          splitArea: { show: true }
        },
        visualMap: {
          min: 0,
          max: 1,
          calculable: true,
          orient: 'vertical',
          right: '1%',
          top: 'center',
          inRange: {
            color: ['#e0f7fa', '#b3e5fc', '#81d4fa', '#4fc3f7', '#29b6f6', '#0288d1', '#01579b']
          }
        },
        series: [{
          name: this.currentHeatmapState === 'before' ? '调控前积水深度' : '调控后积水深度',
          type: 'heatmap',
          data: this.waterData[this.currentHeatmapState + 'Control'],
          label: { show: false },
          emphasis: { itemStyle: { borderColor: '#333', borderWidth: 1 } }
        }]
      };
      this.heatmapChart.setOption(option);
    },
    
    // 初始化调控方案执行效果图（原城市运行效率图表）
    initSystemEfficiencyChart() {
      this.systemEfficiencyChart = echarts.init(document.getElementById('systemEfficiencyChart'));
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: { type: 'cross', label: { backgroundColor: '#6a7985' } }
        },
        legend: { data: ['调控前基线', '调控后效率'], top: '5%' },
        grid: { left: '10%', right: '10%', top: '15%', bottom: '15%', containLabel: true },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: Array.from({length: 16}, (_, i) => `${i + 1}h`),
          name: '时间'
        },
        yAxis: {
          type: 'value',
          min: 0,
          max: 100,
          name: '城市运行效率（分）'
        },
        series: [
          {
            name: '调控前基线',
            type: 'line',
            data: this.efficiencyData.baseline,
            showSymbol: false,
            lineStyle: { width: 1, color: '#999' },
            areaStyle: { color: 'rgba(153, 153, 153, 0.2)' }
          },
          {
            name: '调控后效率',
            type: 'line',
            data: this.efficiencyData.postIntervention,
            showSymbol: false,
            lineStyle: { width: 2, color: '#409EFF' },
            areaStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: 'rgba(64, 158, 255, 0.7)' },
                { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
              ])
            },
 
          }
        ]
      };
      this.systemEfficiencyChart.setOption(option);
    },
    
    // 初始化Agent决策贡献雷达图（原效能分布图表）
    initRadarChart() {
      this.radarChart = echarts.init(document.getElementById('radarChart'));
      const indicators = [
        { name: 'Policy Agent', max: 100 },
        { name: '公交调控Agent', max: 100 },
        { name: '政策发布Agent', max: 100 },
        { name: '交通管控Agent', max: 100 }
      ];
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: function(params) {
            let result = `${params.name}<br/>`;
            params.value.forEach((val, idx) => {
              result += `${indicators[idx].name}: ${val}<br/>`;
            });
            return result;
          }
        },
        legend: { data: this.agentContributions.map(exp => exp.name), bottom: '5%' },
        radar: {
          indicator: indicators,
          radius: '60%',
          center: ['50%', '50%'],
          name: { textStyle: { color: '#333', fontSize: 12 } },
          splitArea: { areaStyle: { color: ['rgba(64, 158, 255, 0.1)', 'rgba(64, 158, 255, 0.2)'] } },
          splitLine: { lineStyle: { color: 'rgba(64, 158, 255, 0.3)' } }
        },
        series: [{
          type: 'radar',
          data: this.agentContributions.map(exp => ({
            value: [
              exp.data['Policy Agent'],
              exp.data['公交调控Agent'],
              exp.data['政策发布Agent'],
              exp.data['交通管控Agent']
            ],
            name: exp.name,
            areaStyle: { opacity: 0.2 }
          })),
          lineStyle: { width: 2 },
          itemStyle: { color: '#409EFF' },
          emphasis: { lineStyle: { width: 4 } }
        }]
      };
      this.radarChart.setOption(option);
    },
    
    // 生成热力图数据
    generateHeatmapData(width, height, minValue, maxValue) {
      const data = [];
      for (let i = 0; i < width; i++) {
        for (let j = 0; j < height; j++) {
          const value = minValue + Math.random() * (maxValue - minValue);
          data.push([i, j, value]);
        }
      }
      return data;
    },
    
    // 生成Agent贡献数据
    generateAgentContribution() {
      return {
        'Policy Agent': Math.floor(50 + Math.random() * 50),
        '公交调控Agent': Math.floor(50 + Math.random() * 50),
        '政策发布Agent': Math.floor(50 + Math.random() * 50),
        '交通管控Agent': Math.floor(50 + Math.random() * 50)
      };
    },
    
    // 更新热力图
    updateHeatmapChart() {
      if (this.heatmapChart) {
        const option = this.heatmapChart.getOption();
        option.series[0].data = this.waterData[this.currentHeatmapState + 'Control'];
        option.series[0].name = this.currentHeatmapState === 'before' ? '调控前积水深度' : '调控后积水深度';
        this.heatmapChart.setOption(option);
      }
    },
    
    // 更新数据
    updateData() {
      // 更新基础数据
      this.systemRunTime += 5;
      this.riderCount = Math.floor(Math.random() * 50) + 80; // 80-130之间随机
      this.orderCount = Math.floor(Math.random() * 200) + 400; // 400-600之间随机
      this.systemEfficiency = (Math.random() * 10 + 80).toFixed(1); // 80-90之间随机
      this.averageEfficiency = (Math.random() * 15 + 70).toFixed(1); // 70-85之间随机
      
      // 更新交通运行趋势数据
      this.trafficData.beforeControl = this.trafficData.beforeControl.map(val => Math.max(20, Math.min(35, val + (Math.random() - 0.5) * 2)));
      this.trafficData.afterControl = this.trafficData.afterControl.map((val, idx) => {
        if (idx < 2) return 30;
        return Math.max(30, Math.min(55, val + (Math.random() - 0.5) * 3));
      });
      
      // 更新Agent贡献数据
      this.agentContributions = [
        { name: '实验1', data: this.generateAgentContribution() },
        { name: '实验2', data: this.generateAgentContribution() }
      ];
      
      // 更新调控方案执行效果图数据
      this.efficiencyData.postIntervention = this.efficiencyData.postIntervention.map((val, idx) => {
        if (idx < 2) return 60;
        return Math.min(95, val + (Math.random() - 0.5) * 5);
      });
      
      // 更新积水分布热力图数据
      this.waterData.beforeControl = this.waterData.beforeControl.map(([x, y, val]) => [x, y, Math.min(1.0, Math.max(0.5, val + (Math.random() - 0.5) * 0.1))]);
      this.waterData.afterControl = this.waterData.beforeControl.map(([x, y, val]) => [x, y, val * (0.2 + Math.random() * 0.3)]);
    },
    
    // 更新图表
    updateCharts() {
      // 如果在分类视图，更新扇形图
      if (!this.selectedCategory && this.categoryPieChart) {
        this.initCategoryPieChart();
      }
      
      // 如果未选择具体实验，不更新其他图表
      if (!this.selectedExperiment) {
        return;
      }
      
      // 更新城市积水分布图
      if (this.riderChart) {
        const option = this.riderChart.getOption();
        option.series[0].data = this.trafficData.beforeControl;
        option.series[1].data = this.trafficData.afterControl;
        this.riderChart.setOption(option);
      }
      
      // 更新积水分布热力图
      this.updateHeatmapChart();
      
      // 更新调控方案执行效果图
      if (this.systemEfficiencyChart) {
        const option = this.systemEfficiencyChart.getOption();
        option.series[0].data = this.efficiencyData.baseline;
        option.series[1].data = this.efficiencyData.postIntervention;
        this.systemEfficiencyChart.setOption(option);
      }
      
      // 更新Agent决策贡献雷达图
      if (this.radarChart) {
        const option = this.radarChart.getOption();
        option.series[0].data = this.agentContributions.map(exp => ({
          value: [
            exp.data['Policy Agent'],
            exp.data['公交调控Agent'],
            exp.data['政策发布Agent'],
            exp.data['交通管控Agent']
          ],
          name: exp.name
        }));
        this.radarChart.setOption(option);
      }
    }
  }
};
</script>

<style scoped>
.chartCard {
  width: 48%;
  margin: 0 1%;
  height: 400px; /* 增加高度以容纳图表内容 */
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chartDiv {
  width: 100%;
  height: 340px; /* 增加图表容器高度，留出标题和图例空间 */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.iconStyle {
  margin-right: 6px;
  color: #409EFF;
}

.cell-item {
  display: flex;
  align-items: center;
  font-size: 14px;
}
</style>