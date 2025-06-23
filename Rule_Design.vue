<template>
  <div style="width: 100%; min-width:1200px; display: flex; flex-direction: row">
    <el-card style="width: 99%; height: 98%">
      <div style="display: flex; flex-direction: column; width: 100%">
        <div style="display: flex; width: 100%; margin: 1rem auto; font-size: 30px; justify-content: center; align-items: center; color: rgb(28, 60, 58)">
          城市内涝智能体交互设计
        </div>
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center; width: 100%;">
          <div style="display: flex; flex-wrap: nowrap; padding: 1rem 0; width: 100%; justify-content: center">
            <el-card v-for="(item, index) in gamePlayer" :key="index"
              :class="{ 'selected-card': selectedIndex === index }"
              @click="selectCard(index)"
              style="display: flex; width: 10vh; margin:0 2%; border-radius: 100%; flex-shrink: 0; cursor: pointer;">
              <div style="height: calc(10vh - 40px); width: 100%; display: flex; justify-content: center; align-items: center">
                <img :src="item.imgUrl" style="width: 90%; height:100%" :alt="item.name"/>
              </div>
            </el-card>
          </div>
        </div>
        <el-scrollbar max-height="80vh">
          <div style="display: flex; width: 100%; height: 600px; gap: 15px; padding: 10px;">
            <div ref="linkOptionsContainer" style="width: 25%; height: 100%; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #f5f5f5; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); overflow-y: auto; display: flex; flex-direction: column; justify-content: center; align-items: center;">
              <div style="text-align: center; width: 100%; max-width: 200px;">
                <h3 v-if="selectedLink" style="font-size: 20px; color: #333; margin-bottom: 15px; font-weight: bold;">{{ getLinkLabel(selectedLink) }}</h3>
                <div v-if="selectedLink" style="display: flex; flex-direction: column; gap: 10px; align-items: stretch;">
                  <el-button v-for="option in getLinkOptions(selectedLink)" :key="option" @click="toggleLinkText(option)"
                    :type="isSelected(option) ? 'success' : 'primary'" size="small" style="font-size: 16px; width: 100%; margin: 0;">
                    {{ option }}
                  </el-button>
                  <el-button @click="applySelections" type="info" size="small" style="font-size: 16px; width: 100%; margin: 0; margin-top: 10px;">确认选择</el-button>
                </div>
                <p v-else style="font-size: 16px; color: #999; line-height: 1.8;">请点击流程图中的连线以选择内容</p>
              </div>
            </div>
            <div ref="container" style="width: 50%; height: 100%; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #ffffff; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
              <svg ref="flowchart" style="width: 100%; height: 100%;"></svg>
            </div>
            <div ref="detailContainer" style="width: 25%; height: 100%; padding: 20px; border: 1px solid #e0e0e0; border-radius: 8px; background-color: #fafafa; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1); overflow-y: auto; display: flex; flex-direction: column; justify-content: center; align-items: center;">
              <div style="text-align: center;">
                <h3 v-if="selectedNode" style="font-size: 20px; color: #333; margin-bottom: 15px; font-weight: bold;">{{ selectedNode.name }}</h3>
                <p v-if="selectedNode" style="font-size: 16px; color: #666; line-height: 1.8;">{{ selectedNode.description }}</p>
                <p v-else style="font-size: 16px; color: #999; line-height: 1.8;">请点击左侧流程图中的节点以查看详情</p>
              </div>
            </div>
          </div>
        </el-scrollbar>
      </div>
    </el-card>
  </div>
</template>

<script>
import { Plus } from "@element-plus/icons";
import { ref } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import * as d3 from "d3";

export default {
  name: "PowerGame_Exp_Strategy",
  components: { Plus },
  setup() {
    const strategySelect = ref(['', '', '', '']);
    const strategyOptions = [
      [{ label: '城市积水数据', value: 1 }, { label: '道路数据', value: 2 }],
      [{ label: '交通管制agent', value: 1 }, { label: '公交调度agent', value: 2 }, { label: '信息发布agent', value: 3 }],
      [{ label: '普通时间段', value: 1 }, { label: '早高峰', value: 2 }, { label: '晚高峰', value: 3 }],
      [{ label: '策略整体应用', value: 1 }, { label: '策略分部应用', value: 2 }],
    ];
    const flowchart = ref(null);
    const container = ref(null);
    const detailContainer = ref(null);
    const linkOptionsContainer = ref(null);

    return { strategySelect, strategyOptions, flowchart, container, detailContainer, linkOptionsContainer };
  },
  data() {
    return {
      selectedIndex: 0,
      selectedNode: null,
      selectedLink: null,
      linksWithText: {}, // 存储连线对应的文字（多选后为数组）
      tempSelectedOptions: [], // 临时存储多选选项
      linkSpecificOptions: { // 每条连线的独立选项
        '1-2': ['发布预警', '不发布预警'],
        '1-3': ['授权交通管制', '无权交通管制'],
        '1-4': ['授权跳站', '无权跳站', '优先通行'],
        '4-5': ['线路调整', '跳站运行', '备用车辆'],
        '2-6': ['公众通知', '出行建议', '灾害预警'],
        '2-5': ['临时通知', '路线变更', '实时反馈'],
        '3-6': ['路况反馈', '疏散指引', '交通调整'],
      },
      gamePlayer: [
        { id: '1', name: '应急响应中心', imgUrl: require('../../assets/images/rainicon/指挥中心.png'), description: '分析城市内涝状况，分区域制定策略。调度信息发布系统、道路管理系统、公交管理系统协同工作。通过预测分析，调整应对方案' },
        { id: '2', name: '信息发布系统', imgUrl: require('../../assets/images/rainicon/告警-紧急.png'), description: '向群众发布道路封闭、公交调整、灾害预警信息。影响群众出行决策，减少交通拥堵' },
        { id: '3', name: '道路管理系统', imgUrl: require('../../assets/images/rainicon/转交警.png'), description: '监测道路淹水情况，根据指挥中心（政策agent）的指挥，决定封闭、开放或调整交通流量。设定临时红绿灯策略，优化疏散路线。与公交管理系统协作，确保公交优先通行' },
        { id: '4', name: '公交管理系统', imgUrl: require('../../assets/images/rainicon/管理系统.png'), description: '监测公交线路受灾情况，调整公交路线允许跳站、调用备用车辆。与道路管理系统协作，绕开封闭道路。' },
        { id: '5', name: '公交车', imgUrl: require('../../assets/images/rainicon/公交管理.png'), description: '根据公交管理系统的指令行驶。反馈道路状况（如积水、交通状况）。影响群众的出行选择' },
        { id: '6', name: '群众', imgUrl: require('../../assets/images/rainicon/群众.png'), description: '依据信息发布系统提供的信息，调整出行决策。体现在系统上为某时刻的道路阻塞情况' }
      ],
      strategyName: ['内涝相关数据', '政策agent倾向', '时段选择', '指令的作用范围'],
      strategies: [
        { name: '内涝相关数据', description: '多层面的数据分析' },
        { name: '政策agent倾向', description: '调动哪种执行agent' },
        { name: '时段选择', description: '普通时间段和高峰时间' },
        { name: '指令的作用范围', description: '执行整体的指令或分成几部分执行' }
      ]
    };
  },
  mounted() {
    this.drawFlowchart();
  },
  methods: {
    selectCard(index) {
      this.selectedIndex = index;
    },
    addStrategy(index) {
      ElMessageBox({
        title: this.strategies[index].name + '添加',
        showInput: true,
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
      }).then(({ value }) => {
        if (value !== null && value !== '') {
          this.strategyOptions[index].push({ label: value, value: this.strategyOptions[index].length + 1 });
          ElMessage({
            type: 'success',
            message: '添加成功',
          });
        }
      });
    },
    getLinkLabel(link) {
      const sourceNode = this.gamePlayer.find(n => n.id === link.source) || { name: '未知' };
      const targetNode = this.gamePlayer.find(n => n.id === link.target) || { name: '未知' };
      return `${sourceNode.name} -> ${targetNode.name}`;
    },
    getLinkOptions(link) {
      return this.linkSpecificOptions[`${link.source}-${link.target}`] || [];
    },
    isSelected(option) {
      return this.tempSelectedOptions.includes(option);
    },
    toggleLinkText(option) {
      const index = this.tempSelectedOptions.indexOf(option);
      if (index === -1) {
        this.tempSelectedOptions.push(option); // 选中
      } else {
        this.tempSelectedOptions.splice(index, 1); // 取消选中
      }
    },
    applySelections() {
      if (this.selectedLink) {
        this.linksWithText[`${this.selectedLink.source}-${this.selectedLink.target}`] = [...this.tempSelectedOptions]; // 保存多选结果
        this.tempSelectedOptions = []; // 清空临时选择
        this.drawFlowchart(); // 重新绘制
        this.selectedLink = null; // 清空选中连线
      }
    },
    drawFlowchart() {
      const svg = d3.select(this.$refs.flowchart);
      const container = this.$refs.container;
      const width = Math.max(container.getBoundingClientRect().width, 600); // 最小宽度 600px
      const height = 600; // 固定高度
      svg.attr("width", width).attr("height", height);

      const nodeWidth = 150;
      const nodeHeight = 50;
      const verticalSpacing = height / 4; // 调整为 4 层布局
      const horizontalSpacing = width / 4; // 水平间距

      // 清空之前的绘制内容
      svg.selectAll("*").remove();

      // 定义节点数据
      const nodes = [
        { id: '1', name: '应急响应中心', imgUrl: this.gamePlayer[0].imgUrl, x: width / 2 - nodeWidth / 2, y: verticalSpacing / 2, description: this.gamePlayer[0].description },
        { id: '2', name: '信息发布系统', imgUrl: this.gamePlayer[1].imgUrl, x: width / 2 - horizontalSpacing - nodeWidth / 2, y: verticalSpacing * 1.5, description: this.gamePlayer[1].description },
        { id: '3', name: '道路管理系统', imgUrl: this.gamePlayer[2].imgUrl, x: width / 2 - nodeWidth / 2, y: verticalSpacing * 1.5, description: this.gamePlayer[2].description },
        { id: '4', name: '公交管理系统', imgUrl: this.gamePlayer[3].imgUrl, x: width / 2 + horizontalSpacing - nodeWidth / 2, y: verticalSpacing * 1.5, description: this.gamePlayer[3].description },
        { id: '5', name: '公交车', imgUrl: this.gamePlayer[4].imgUrl, x: width / 2 + horizontalSpacing - nodeWidth / 2, y: verticalSpacing * 2.5, description: this.gamePlayer[4].description },
        { id: '6', name: '群众', imgUrl: this.gamePlayer[5].imgUrl, x: width / 2 - horizontalSpacing - nodeWidth / 2, y: verticalSpacing * 2.5, description: this.gamePlayer[5].description },
      ];

      // 定义边数据
      const links = [
        { source: '1', target: '2' }, // 应急响应中心 -> 信息发布系统
        { source: '1', target: '3' }, // 应急响应中心 -> 道路管理系统
        { source: '1', target: '4' }, // 应急响应中心 -> 公交管理系统
        { source: '4', target: '5' }, // 公交管理系统 -> 公交车
        { source: '2', target: '6' }, // 信息发布系统 -> 群众
        { source: '2', target: '5' }, // 信息发布系统 -> 公交车
        { source: '3', target: '6' }, // 道路管理系统 -> 群众
      ];

      // 绘制节点（先绘制节点）
      const node = svg.append("g")
        .selectAll("g")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .attr("transform", d => `translate(${d.x},${d.y})`)
        .on("click", (event, d) => {
          this.selectedNode = d; // 点击时更新选中节点
          this.selectedLink = null; // 清空选中连线
          this.tempSelectedOptions = []; // 清空临时选择
          event.stopPropagation(); // 阻止事件冒泡
        })
        .on("mouseover", function () {
          d3.select(this).select("rect")
            .attr("stroke", "#ff6600")
            .attr("stroke-width", 4)
            .attr("fill", "#fff8e1");
          d3.select(this).transition().duration(300)
            .attr("transform", d => `translate(${d.x},${d.y}) scale(1.1)`);
        })
        .on("mouseout", function (event, d) {
          d3.select(this).select("rect")
            .attr("stroke", "#666")
            .attr("stroke-width", 2)
            .attr("fill", "#fff");
          d3.select(this).transition().duration(300)
            .attr("transform", d => `translate(${d.x},${d.y}) scale(1)`);
        });

      node.append("rect")
        .attr("width", nodeWidth)
        .attr("height", nodeHeight)
        .attr("rx", 8)
        .attr("fill", "#fff")
        .attr("stroke", "#666")
        .attr("stroke-width", 2);

      node.append("image")
        .attr("xlink:href", d => d.imgUrl)
        .attr("x", 10)
        .attr("y", 10)
        .attr("width", 30)
        .attr("height", 30);

      node.append("text")
        .attr("x", 45)
        .attr("y", nodeHeight / 2 + 5)
        .attr("text-anchor", "start")
        .attr("font-family", "Microsoft YaHei, serif")
        .attr("font-size", "14px")
        .attr("font-weight", "bold")
        .attr("fill", "#333")
        .style("text-shadow", "1px 1px 2px rgba(0, 0, 0, 0.1)")
        .text(d => d.name);

      // 绘制边（后绘制连线）
      const link = svg.append("g")
        .selectAll("g")
        .data(links)
        .enter()
        .append("g")
        .attr("class", "link");

      // 绘制可见连线
      link.append("path")
        .attr("d", d => {
          const source = nodes.find(n => n.id === d.source);
          const target = nodes.find(n => n.id === d.target);
          const sx = source.x + nodeWidth / 2;
          const sy = source.y + nodeHeight;
          const tx = target.x + nodeWidth / 2;
          const ty = target.y;
          return `M${sx},${sy} L${tx},${ty}`;
        })
        .attr("stroke", "#666")
        .attr("stroke-width", 2)
        .attr("fill", "none")
        .attr("marker-end", "url(#arrow)");

      // 添加透明点击区域
      link.append("path")
        .attr("d", d => {
          const source = nodes.find(n => n.id === d.source);
          const target = nodes.find(n => n.id === d.target);
          const sx = source.x + nodeWidth / 2;
          const sy = source.y + nodeHeight;
          const tx = target.x + nodeWidth / 2;
          const ty = target.y;
          return `M${sx},${sy} L${tx},${ty}`;
        })
        .attr("stroke", "transparent")
        .attr("stroke-width", 10)
        .attr("fill", "none")
        .on("click", (event, d) => {
          this.selectedLink = d; // 选中连线
          this.selectedNode = null; // 清空选中节点
          this.tempSelectedOptions = this.linksWithText[`${d.source}-${d.target}`] || []; // 加载已有选择
          event.stopPropagation(); // 阻止事件冒泡
          console.log("Link clicked:", d);
        });

      // 添加连线文字（先绘制文字）
      const textElements = link.append("text")
        .attr("x", d => {
          const source = nodes.find(n => n.id === d.source);
          const target = nodes.find(n => n.id === d.target);
          return (source.x + target.x + nodeWidth) / 2;
        })
        .attr("y", d => {
          const source = nodes.find(n => n.id === d.source);
          const target = nodes.find(n => n.id === d.target);
          return (source.y + nodeHeight + target.y) / 2;
        })
        .attr("text-anchor", "middle")
        .attr("font-family", "Microsoft YaHei, serif")
        .attr("font-size", "14px")
        .attr("font-weight", "bold")
        .attr("fill", "#ff6600")
        .style("text-shadow", "1px 1px 2px rgba(0, 0, 0, 0.2)")
        .text(d => {
          const text = this.linksWithText[`${d.source}-${d.target}`] || [];
          return text.join(", ");
        });

      // 添加连线文字背景（根据文字实际宽度调整）
      link.append("rect")
        .attr("x", d => {
          const textElement = textElements.filter(dd => dd === d).node();
          const bbox = textElement ? textElement.getBBox() : { width: 0, x: 0 };
          return bbox.x - 10; // 左右各留 10px 边距
        })
        .attr("y", d => {
          const textElement = textElements.filter(dd => dd === d).node();
          const bbox = textElement ? textElement.getBBox() : { height: 0, y: 0 };
          return bbox.y - 5; // 上下各留 5px 边距
        })
        .attr("width", d => {
          const textElement = textElements.filter(dd => dd === d).node();
          const bbox = textElement ? textElement.getBBox() : { width: 0 };
          return bbox.width + 20; // 宽度加上左右边距
        })
        .attr("height", d => {
          const textElement = textElements.filter(dd => dd === d).node();
          const bbox = textElement ? textElement.getBBox() : { height: 0 };
          return bbox.height + 10; // 高度加上上下边距
        })
        .attr("rx", 4)
        .attr("fill", "#fff8e1")
        .attr("stroke", "#ff6600")
        .attr("stroke-width", 1)
        .attr("opacity", d => (this.linksWithText[`${d.source}-${d.target}`] && this.linksWithText[`${d.source}-${d.target}`].length > 0) ? 1 : 0)
        .lower(); // 确保矩形在文字下方

      // 定义箭头标记
      svg.append("defs").append("marker")
        .attr("id", "arrow")
        .attr("viewBox", "0 -5 10 10")
        .attr("refX", 8)
        .attr("refY", 0)
        .attr("markerWidth", 6)
        .attr("markerHeight", 6)
        .attr("orient", "auto")
        .append("path")
        .attr("d", "M0,-5L10,0L0,5")
        .attr("fill", "#666");
    }
  }
};
</script>

<style scoped>
.card-style {
  width: 40%;
  margin: 1rem 1.5rem;
  height: 300px;
  background-color: #E9ECEC;
}
.card-title {
  display: flex;
  width: 100%;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  font-family: "Microsoft YaHei", serif;
  margin: 1rem 0;
}
.card-content {
  display: flex;
  margin-left: 10%;
  width: 80%;
  height: 150px;
  justify-content: center;
  align-items: center;
  font-size: 16px;
  font-family: 'Microsoft YaHei', serif;
  line-height: 1.7;
  font-weight: lighter;
}
.selected-card {
  background-color: rgb(148.6, 212.3, 117.1) !important;
}
</style>