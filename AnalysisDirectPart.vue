<template>
    <div class="direct-part">
      <!-- 简略模式：只显示提示文字 -->
      <template v-if="collapsed">
        <div class="summary-text">
          当前界面展示整体分析与实验数据
          <br>
          <br>
          👉 点击查看不同实验组的对比情况
        </div>
      </template>
  
      <!-- 详细模式：展示图表和分析内容 -->
      <template v-else>
        
        <el-card class="main-card" v-loading="isLoading">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <div style="font-size: 22px; font-family: 'Microsoft YaHei', serif; font-weight: bold;">
                    实验对比界面
                </div>
                    <br><br><br>
                </div>

            <!-- 分割线 -->
            <el-divider></el-divider>
          <div class="content-wrapper">
            <!-- 控制面板 -->
            <div class="control-panel">
              <el-descriptions :column="3" border>
                <el-descriptions-item label="对比模式">
                  <el-select v-model="comparisonMode" placeholder="选择对比模式" @change="onModeChange">
                    <el-option label="按策略对比" value="byEnvironment" />
                    <el-option label="按环境对比" value="byStrategy" />
                  </el-select>
                </el-descriptions-item>
                <el-descriptions-item :label="comparisonMode === 'byEnvironment' ? '环境' : '策略'">
                  <el-select
                    v-model="selectedOption"
                    :placeholder="comparisonMode === 'byEnvironment' ? '选择环境' : '选择策略'"
                    @change="refreshChart"
                  >
                    <el-option
                      v-for="option in comparisonMode === 'byEnvironment' ? environmentOptions : strategyOptions"
                      :key="option"
                      :label="option"
                      :value="option"
                    />
                  </el-select>
                </el-descriptions-item>
                <el-descriptions-item label="实验组">
                  <el-select v-model="selectedExperiment" placeholder="选择实验组" @change="refreshChart">
                    <el-option
                      v-for="group in experimentGroups"
                      :key="group.id"
                      :label="group.name"
                      :value="group.id"
                    />
                  </el-select>
                </el-descriptions-item>
              </el-descriptions>
            </div>
  
            <!-- 图表区域 -->
            <div class="chart-container">
              <el-card class="chart-wrapper">
                <h3 class="chart-title">{{ chartTitle }}</h3>
                <div class="chart-content">
                  <!-- 雷达图 -->
                  <div class="radar-chart">
                    <div class="chart-section">
                      <h4>综合影响对比</h4>
                      <svg ref="radarChart"></svg>
                    </div>
                  </div>
                  <!-- 左侧柱状图 -->
                  <div class="left-charts">
                    <div class="chart-section">
                      <h4>积水导致道路通行功能下降百分比</h4>
                      <svg ref="floodChart"></svg>
                    </div>
                    <div class="chart-section">
                      <h4>公交准点率</h4>
                      <svg ref="punctualityChart"></svg>
                    </div>
                  </div>
                  <!-- 右侧柱状图 -->
                  <div class="right-chart">
                    <div class="chart-section">
                      <h4>公交线路停运次数</h4>
                      <svg ref="disruptionChart"></svg>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </el-card>
      </template>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, nextTick } from 'vue';
  import * as d3 from 'd3';
  import { watch } from 'vue'

  // 状态定义
  const isLoading = ref(false);
  const strategyOptions = ref(['固定路线', '保守型', '激进型']);
  const environmentOptions = ref(['晴天', '雨天', '高峰', '雨天高峰']);
  const comparisonMode = ref('byEnvironment');
  const selectedOption = ref('晴天');
  const chartTitle = ref('晴天环境下的公交指标对比');
  const floodChart = ref(null);
  const punctualityChart = ref(null);
  const disruptionChart = ref(null);
  const radarChart = ref(null);
  const props = defineProps({
  collapsed: Boolean
});
  // 实验组定义
  const experimentGroups = ref([
    { id: 'group1', name: '实验组 1', data: null },
    { id: 'group2', name: '实验组 2', data: null },
    { id: 'group3', name: '实验组 3', data: null },
  ]);
  const selectedExperiment = ref('group1');
  
  // 图表配置
  const chartHeightLeft = 250;
  const chartHeightRight = 540;
  const margin = { top: 30, right: 40, bottom: 60, left: 60 };
  
  // 生成单个实验组的数据
  const generateUnifiedData = () => {
    const data = {};
    environmentOptions.value.forEach((env) => {
      data[env] = {};
      strategyOptions.value.forEach((strat) => {
        let floodImpact = Math.random() * 50;
        if (env === '雨天') floodImpact += 30;
        if (env === '雨天高峰') floodImpact += 50;
        if (strat === '保守型') floodImpact -= 10;
        if (strat === '激进型') floodImpact -= 20;
  
        let punctuality = Math.random() * 80 + 20;
        if (env === '高峰') punctuality -= 20;
        if (env === '雨天高峰') punctuality -= 40;
        if (strat === '保守型') punctuality += 10;
        if (strat === '激进型') punctuality += 15;
  
        let disruptions = Math.round(Math.random() * 5);
        if (env === '雨天') disruptions += 2;
        if (env === '高峰') disruptions += 1;
        if (env === '雨天高峰') disruptions += 4;
        if (strat === '激进型') disruptions -= 2;
  
        data[env][strat] = {
          floodImpact: Math.max(0, Math.min(floodImpact, 100)),
          punctuality: Math.max(0, Math.min(punctuality, 100)),
          disruptions: Math.max(0, Math.min(disruptions, 10)),
        };
      });
    });
    return data;
  };
  
  // 初始化所有实验组数据
  const initExperimentData = () => {
    experimentGroups.value.forEach((group) => {
      group.data = generateUnifiedData(); // 为每个实验组生成独立数据
    });
  };
  
  // 绘制柱状图的通用函数
  const drawBarChart = (svgRef, data, yDomain, color, width, height) => {
    const svg = d3.select(svgRef)
      .attr('width', width)
      .attr('height', height);
    svg.selectAll('*').remove();
  
    const xScale = d3.scaleBand()
      .domain(data.map((d) => d.category))
      .range([margin.left, width - margin.right])
      .padding(0.2);
  
    const yScale = d3.scaleLinear()
      .domain(yDomain)
      .range([height - margin.bottom, margin.top]);
  
    svg.append('g')
      .attr('transform', `translate(0, ${height - margin.bottom})`)
      .call(d3.axisBottom(xScale))
      .selectAll('text')
      .style('text-anchor', 'middle')
      .style('font-size', '14px')
      .style('font-weight', 'bold');
  
    svg.append('g')
      .attr('transform', `translate(${margin.left}, 0)`)
      .call(d3.axisLeft(yScale).ticks(5))
      .selectAll('text')
      .style('font-size', '14px')
      .style('font-weight', 'bold');
  
    svg.selectAll('.bar')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', 'bar')
      .attr('x', (d) => xScale(d.category))
      .attr('y', (d) => yScale(d.value))
      .attr('width', xScale.bandwidth())
      .attr('height', (d) => height - margin.bottom - yScale(d.value))
      .attr('fill', color);
  };
  
  // 绘制雷达图
  const drawRadarChart = (svgRef, data, width, height) => {
    const svg = d3.select(svgRef)
      .attr('width', width)
      .attr('height', height);
    svg.selectAll('*').remove();
  
    const radius = Math.min(width, height) / 2 - 50;
    const centerX = width / 2;
    const centerY = height / 2;
  
    const labels = ['晴天', '雨天', '高峰', '固定路线', '保守型', '激进型'];
    const angles = d3.range(0, 2 * Math.PI, 2 * Math.PI / labels.length);
  
    const radialScale = d3.scaleLinear()
      .domain([0, 100])
      .range([0, radius]);
  
    // 绘制网格
    const levels = 5;
    for (let level = 0; level <= levels; level++) {
      const levelFactor = radius * (level / levels);
      svg.selectAll(`.grid-${level}`)
        .data(angles)
        .enter()
        .append('line')
        .attr('x1', (d) => centerX + levelFactor * Math.cos(d))
        .attr('y1', (d) => centerY + levelFactor * Math.sin(d))
        .attr('x2', (d, i) => centerX + levelFactor * Math.cos(angles[(i + 1) % angles.length]))
        .attr('y2', (d, i) => centerY + levelFactor * Math.sin(angles[(i + 1) % angles.length]))
        .attr('stroke', '#ccc')
        .attr('stroke-width', 1);
    }
  
    // 绘制轴
    svg.selectAll('.axis')
      .data(labels)
      .enter()
      .append('line')
      .attr('x1', centerX)
      .attr('y1', centerY)
      .attr('x2', (d, i) => centerX + radius * Math.cos(angles[i]))
      .attr('y2', (d, i) => centerY + radius * Math.sin(angles[i]))
      .attr('stroke', '#999')
      .attr('stroke-width', 1);
  
    // 添加标签
    svg.selectAll('.label')
      .data(labels)
      .enter()
      .append('text')
      .attr('x', (d, i) => centerX + (radius + 20) * Math.cos(angles[i]))
      .attr('y', (d, i) => centerY + (radius + 20) * Math.sin(angles[i]))
      .attr('text-anchor', (d, i) => {
        const angle = angles[i];
        if (angle < Math.PI / 2 || angle > 3 * Math.PI / 2) return 'start';
        if (angle > Math.PI / 2 && angle < 3 * Math.PI / 2) return 'end';
        return 'middle';
      })
      .attr('dy', '.35em')
      .style('font-size', '12px')
      .style('font-weight', 'bold')
      .text((d) => d);
  
    // 绘制数据
    const radarData = data.map((value, i) => ({
      x: centerX + radialScale(value) * Math.cos(angles[i]),
      y: centerY + radialScale(value) * Math.sin(angles[i]),
    }));
    radarData.push(radarData[0]); // 闭合路径
  
    svg.append('path')
      .datum(radarData)
      .attr('d', d3.line().x((d) => d.x).y((d) => d.y))
      .attr('fill', 'rgba(33, 150, 243, 0.2)')
      .attr('stroke', '#2196F3')
      .attr('stroke-width', 2);
  };
  
  // 绘制图表
  const renderChart = async () => {
    await nextTick();
  
    if (!floodChart.value || !punctualityChart.value || !disruptionChart.value || !radarChart.value) {
      console.error('One or more SVG elements not found');
      return;
    }
  
    chartTitle.value =
      comparisonMode.value === 'byEnvironment'
        ? `${selectedOption.value}环境下的公交指标对比`
        : `${selectedOption.value}路线在不同环境下的公交指标对比`;
  
    const isByEnv = comparisonMode.value === 'byEnvironment';
    const categories = isByEnv ? strategyOptions.value : environmentOptions.value;
  
    // 获取容器宽度并计算各图表宽度
    const chartContent = document.querySelector('.chart-content');
    const totalWidth = chartContent.clientWidth;
    const radarWidth = totalWidth * 0.3;
    const leftChartWidth = totalWidth * 0.4;
    const rightChartWidth = totalWidth * 0.3;
  
    // 使用当前实验组的数据
    const data = experimentGroups.value.find((g) => g.id === selectedExperiment.value).data;
  
    // 积水影响柱状图（左上）
    const floodData = isByEnv
      ? strategyOptions.value.map((strat) => ({
          category: strat,
          value: data[selectedOption.value][strat].floodImpact,
        }))
      : environmentOptions.value.map((env) => ({
          category: env,
          value: data[env][selectedOption.value].floodImpact,
        }));
    drawBarChart(floodChart.value, floodData, [0, 100], '#FF9800', leftChartWidth, chartHeightLeft);
  
    // 准点率柱状图（左下）
    const punctualityData = isByEnv
      ? strategyOptions.value.map((strat) => ({
          category: strat,
          value: data[selectedOption.value][strat].punctuality,
        }))
      : environmentOptions.value.map((env) => ({
          category: env,
          value: data[env][selectedOption.value].punctuality,
        }));
    drawBarChart(punctualityChart.value, punctualityData, [0, 100], '#2196F3', leftChartWidth, chartHeightLeft);
  
    // 停运次数柱状图（右）
    const disruptionData = isByEnv
      ? strategyOptions.value.map((strat) => ({
          category: strat,
          value: data[selectedOption.value][strat].disruptions,
        }))
      : environmentOptions.value.map((env) => ({
          category: env,
          value: data[env][selectedOption.value].disruptions,
        }));
    drawBarChart(disruptionChart.value, disruptionData, [0, 10], '#F44336', rightChartWidth, chartHeightRight);
  
    // 雷达图数据（保持一致性）
    const radarData = [
      data['晴天'][isByEnv ? '固定路线' : selectedOption.value].punctuality,
      data['雨天'][isByEnv ? '固定路线' : selectedOption.value].punctuality,
      data['高峰'][isByEnv ? '固定路线' : selectedOption.value].punctuality,
      data[isByEnv ? selectedOption.value : '晴天']['固定路线'].punctuality,
      data[isByEnv ? selectedOption.value : '晴天']['保守型'].punctuality,
      data[isByEnv ? selectedOption.value : '晴天']['激进型'].punctuality,
    ];
    drawRadarChart(radarChart.value, radarData, radarWidth, chartHeightRight);
  };
  
  // 处理模式切换
  const onModeChange = (mode) => {
    selectedOption.value = mode === 'byEnvironment' ? environmentOptions.value[0] : strategyOptions.value[0];
    renderChart();
  };
  
  // 刷新图表
  const refreshChart = () => {
    renderChart();
  };
  
  // 初始化图表
  onMounted(async () => {
    initExperimentData(); // 初始化所有实验组数据
    await nextTick();
    renderChart();
  });

  watch(() => props.collapsed, (collapsedNow) => {
  if (!collapsedNow) {
    nextTick(() => {
      // 再等一帧，让 DOM 撑起来
      setTimeout(() => {
        refreshChart()
      }, 400) // 可以根据实际情况调整时间，比如 100ms
    })
  }
})
  </script>
  
  <style scoped>
  .container {
    display: flex;
    width: 100%;
    min-width: 1000px;
    padding: 10px;
  }
  
  .main-card {
    width: 100%;
    height: 100%;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }
  
  .content-wrapper {
    display: flex;
    flex-direction: column;
    height: 100%;
  }
  
  .control-panel {
    width: 100%;
    padding-bottom: 20px;
  }
  
  .chart-container {
    flex: 1;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .chart-wrapper {
    width: 90%;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
  }
  
  .chart-title {
    text-align: center;
    margin: 10px 0;
    font-size: 20px;
    font-weight: bold;
    color: #333;
  }
  
  .chart-content {
    width: 100%;
    height: 90%;
    display: flex;
    flex-direction: row;
    gap: 20px;
    justify-content: center;
    align-items: center;
  }
  
  .radar-chart {
    flex: 3;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
  
  .left-charts {
    flex: 4;
    display: flex;
    flex-direction: column;
    gap: 20px;
    justify-content: center;
    align-items: center;
    height: 100%;
  }
  
  .right-chart {
    flex: 3;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100%;
  }
  
  .chart-section {
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: visible;
  }
  
  .radar-chart .chart-section,
  .right-chart .chart-section {
    height: 100;
  }
  
  .chart-section h4 {
    text-align: center;
    margin: 5px 0;
    font-size: 16px;
    font-weight: bold;
    color: #333;
  }
  
  .chart-section svg {
    width: 100%;
    height: 100%;
    display: block;
  }
  
  @media (max-width: 1200px) {
    .chart-wrapper {
      width: 95%;
    }
  
    .chart-title {
      font-size: 18px;
    }
  
    .chart-section {
      height: 200px;
    }
  
    .radar-chart .chart-section,
    .right-chart .chart-section {
      height: 400px;
    }
  
    .chart-section h4 {
      font-size: 14px;
    }
  }
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