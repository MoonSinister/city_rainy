<template>
  <div style="width: 99%; min-width:1200px; display: flex">
    <div style="width: 99%; min-width: 1200px; display: inline; position: relative">
      <el-card ref="contentCard" style="width: 100%;height: 98%"
               v-loading="loadingAnimation" element-loading-text="正在返回实验设计界面，请稍后...">
        <!-- 头部返回组件 -->
        <div style="width: 100%; display: flex">
          <el-page-header @back="goBack()">
            <template #content>
              <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/home/rainCity/firstdesign' }">
                  实验目标设计
                </el-breadcrumb-item>
              </el-breadcrumb>
            </template>
          </el-page-header>
        </div>
        <!-- 内容Card -->
        <div style="display: inline; width: 100%">
          <el-scrollbar :max-height="cardMaxHeight">
            <div style="display: flex; width: 100%; margin-top: 2rem" v-if="showModel === 0">
              <div style="width: 48%; margin: 0 2% 0 1%; display: flex; flex-direction: column; justify-content: center; min-height: 600px;">
                <el-card shadow="hover" style="padding: 0; border-radius: 16px; box-shadow: 0 4px 24px 0 rgba(0,0,0,0.08);">
                  <div style="font-size: 22px; font-weight: bold; text-align: center; margin: 24px 0 12px 0; letter-spacing: 2px; color: #3a3a3a;">
                    实验目标设计助手
                  </div>
                  <div style="display: flex; justify-content: center; align-items: center; min-height: 480px;">
                    <!-- 直接嵌入ChatWithAgent组件，替换原有对话输入区 -->
                    <ChatWithAgent />
                  </div>
                </el-card>
              </div>
              <div style="width: 49%; display: flex; flex-direction: column; justify-content: space-between;">
                <el-card class="cardStyle" shadow="hover">
                  <template #header>
                    <div class="card-header">
                      <span>无干扰状态下的降水对交通影响</span>
                      <el-button type="primary" size="default" @click="selectBtnClick(1)">选定</el-button>
                    </div>
                  </template>
                  <div class="line-style">
                    <span>分析在无任何干预措施下，降水事件对城市交通运行状况（如拥堵、延误、事故率等）的直接影响。</span>
                  </div>
                </el-card>
                <el-card class="cardStyle" shadow="hover">
                  <template #header>
                    <div class="card-header">
                      <span>简单策略下的降水对交通影响</span>
                      <el-button type="primary" size="default" @click="selectBtnClick(2)">选定</el-button>
                    </div>
                  </template>
                  <div class="line-style">
                    <span>评估如交通管制、临时疏导等基础应对策略下，降水对交通运行的改善效果及其局限性。</span>
                  </div>
                </el-card>
                <el-card class="cardStyle" shadow="hover">
                  <template #header>
                    <div class="card-header">
                      <span>大模型Agent参与决策下的降水对交通影响</span>
                      <el-button type="primary" size="default" @click="selectBtnClick(3)">选定</el-button>
                    </div>
                  </template>
                  <div class="line-style">
                    <span>探讨引入AI大模型Agent进行智能调度与决策时，降水对交通系统的影响及其优化空间。</span>
                  </div>
                </el-card>
                <el-card class="cardStyle" shadow="hover" style="margin-bottom: 0">
                  <template #header>
                    <div class="card-header">
                      <span>多种策略对比下的降水对交通影响</span>
                      <el-button type="primary" size="default" @click="selectBtnClick(4)">选定</el-button>
                    </div>
                  </template>
                  <div class="line-style">
                    <span>对比不同干预策略（如无干预、简单策略、智能决策等）下，降水对城市交通运行的综合影响与反馈。</span>
                  </div>
                </el-card>
              </div>
            </div>
            <!-- 其余部分保持不变 -->
            <div style="display: flex; margin-top: 2rem; margin-left: 0.5%" v-if="showModel === 1">

              
            </div>
            <div style="display: flex; margin-top: 2rem" v-if="showModel === 1">
              <el-button type="info" style="margin-bottom: 16px; margin-right: 16px;" @click="showModel = 0">重选</el-button>
              <el-card class="card-style-1" shadow="hover" v-if="selectedCard === 1">
                <template #header>
                  <div class="card-header">
                    <span>无干扰状态下的降水对交通影响</span>
                    <div>
                      <el-button type="success" @click="selectBtnClick(1)" plain disabled>已选定</el-button>
                      <el-button type="success" @click="editCompleted()">编辑完成</el-button>
                    </div>
                  </div>
                </template>
                <div class="line-style" style="display: flex">
                  <div style="width: 50%">
                    <p style="line-height: 30px">
                      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                      研究在没有任何交通干预措施时，降水对城市道路通行能力、交通流量、事故发生率等方面的直接影响。
                    </p>
                    <el-cascader v-model="descriptiveMethod"
                                 :options="descriptiveResearch" :props="props"
                                 placeholder="请选择分析方法"
                                 @change="testChange()"
                                 style="width: 60%; margin-top: 1rem"/>
                  </div>
                  <div>
                    <el-divider direction="vertical" style="height: 100%"/>
                  </div>
                  <div style="width: 50%">
                    <div style="margin-left: 1rem" v-if="descriptiveMethod.length === 0">
                      <p class="explain-text-title">详细介绍</p>
                      <div class="unselected-right-card">
                        请在左侧选择具体的方法
                      </div>
                    </div>
                    <div style="margin-left: 1rem" v-if="descriptiveMethod.length === 1 && descriptiveMethod[0] === 1">
                      <p class="explain-text-title">历史交通数据分析</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过对历史降水期间的交通运行数据进行统计分析，揭示降水对交通流量、速度、事故等的影响规律。</p>
                      <el-checkbox-group v-model="descriptiveSubMethod1" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="交通流量变化">交通流量变化</el-checkbox>
                        <el-checkbox label="平均车速">平均车速</el-checkbox>
                        <el-checkbox label="事故率">事故率</el-checkbox>
                        <el-checkbox label="延误时长">延误时长</el-checkbox>
                      </el-checkbox-group>
                      <!-- 交通流量变化级联选择器 -->
                      <el-cascader v-if="descriptiveSubMethod1.includes('交通流量变化')"
                                   v-model="trafficFlowCascader"
                                   :options="trafficFlowCascaderOptions"
                                   :props="{ multiple: false }"
                                   placeholder="请选择流量分析维度"
                                   style="width: 70%; margin-top: 1rem; font-size: 18px;" />
                      <!-- 平均车速级联选择器 -->
                      <el-cascader v-if="descriptiveSubMethod1.includes('平均车速')"
                                   v-model="avgSpeedCascader"
                                   :options="avgSpeedCascaderOptions"
                                   :props="{ multiple: false }"
                                   placeholder="请选择车速分析维度"
                                   style="width: 70%; margin-top: 1rem; font-size: 18px;" />
                    </div>
                    <div style="margin-left: 1rem" v-if="descriptiveMethod.length === 1 && descriptiveMethod[0] === 2">
                      <p class="explain-text-title">现场观测法</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过实地观测降水期间的交通状况，记录道路积水、拥堵点、事故多发区等信息。</p>
                      <el-checkbox-group v-model="descriptiveSubMethod2" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="积水点分布">积水点分布</el-checkbox>
                        <el-checkbox label="拥堵路段">拥堵路段</el-checkbox>
                        <el-checkbox label="事故多发区">事故多发区</el-checkbox>
                      </el-checkbox-group>
                    </div>
                    <div style="margin-left: 1rem" v-if="descriptiveMethod.length === 1 && descriptiveMethod[0] === 3">
                      <p class="explain-text-title">问卷调查法</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;通过对市民、司机等群体进行问卷调查，收集降水期间出行体验与交通问题反馈。</p>
                      <el-checkbox-group v-model="descriptiveSubMethod3" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="出行满意度">出行满意度</el-checkbox>
                        <el-checkbox label="主要困难">主要困难</el-checkbox>
                        <el-checkbox label="建议与意见">建议与意见</el-checkbox>
                      </el-checkbox-group>
                    </div>
                    <div style="margin-left: 1rem" v-if="descriptiveMethod.length === 1 && descriptiveMethod[0] === 4">
                      <p class="explain-text-title">交通仿真建模</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;利用仿真软件模拟降水情景下的交通运行，分析不同降水强度对交通系统的影响。</p>
                      <el-checkbox-group v-model="descriptiveSubMethod4" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="仿真降水强度">仿真降水强度</el-checkbox>
                        <el-checkbox label="仿真路网规模">仿真路网规模</el-checkbox>
                        <el-checkbox label="仿真时段">仿真时段</el-checkbox>
                      </el-checkbox-group>
                    </div>
                  </div>
                </div>
              </el-card>
              <el-card class="card-style-1" shadow="hover" v-if="selectedCard === 2">
                <template #header>
                  <div class="card-header">
                    <span>简单策略下的降水对交通影响</span>
                    <div>
                      <el-button type="success" @click="selectBtnClick(2)" plain disabled>已选定</el-button>
                      <el-button type="success" @click="editCompleted()">编辑完成</el-button>
                    </div>
                  </div>
                </template>
                <div class="line-style" style="display: flex">
                  <div style="width: 50%">
                    <p style="line-height: 30px">
                      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                      评估如交通管制、临时疏导、限速等基础应对措施下，降水对交通运行的影响变化及其效果。
                    </p>
                    <el-cascader v-model="explainMethod"
                                 :options="explainResearch" :props="props"
                                 placeholder="请选择干预分析方法"
                                 @change="testChange()"
                                 style="width: 60%; margin-top: 1rem"/>
                  </div>
                  <div>
                    <el-divider direction="vertical" style="height: 100%"/>
                  </div>
                  <div style="width: 50%">
                    <div style="margin-left: 1rem" v-if="explainMethod.length === 0">
                      <p class="explain-text-title">详细介绍</p>
                      <div class="unselected-right-card">
                        请在左侧选择具体的方法
                      </div>
                    </div>
                    <div style="margin-left: 1rem" v-if="explainMethod.length === 2 && explainMethod[0] === 1 && explainMethod[1] === 1">
                      <p class="explain-text-title">局部交通管制效果分析</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;针对重点路段实施临时交通管制，分析其对缓解降水期间交通拥堵的实际效果。</p>
                      <el-checkbox-group v-model="explainSubMethod1" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="管制路段选择">管制路段选择</el-checkbox>
                        <el-checkbox label="管制时段">管制时段</el-checkbox>
                        <el-checkbox label="交通流恢复速度">交通流恢复速度</el-checkbox>
                      </el-checkbox-group>
                    </div>
                    <div style="margin-left: 1rem" v-if="explainMethod.length === 1 && explainMethod[0] === 3">
                      <p class="explain-text-title">敏感性分析</p>
                      <p>1. <b>识别关键影响因素</b>：如降水强度、交通流量、管制措施等对交通运行的影响程度。<br/></p>
                      <p>2. <b>风险评估</b>：评估不同应对策略下交通系统的脆弱性和风险点。<br/></p>
                      <p>3. <b>优化建议</b>：为后续策略优化提供数据支持。<br/></p>
                      <el-checkbox-group v-model="explainSubMethod2" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="关键变量分析">关键变量分析</el-checkbox>
                        <el-checkbox label="敏感性排序">敏感性排序</el-checkbox>
                        <el-checkbox label="风险点定位">风险点定位</el-checkbox>
                      </el-checkbox-group>
                    </div>
                  </div>
                </div>
              </el-card>
              <el-card class="card-style-1" shadow="hover" v-if="selectedCard === 3">
                <template #header>
                  <div class="card-header">
                    <span>大模型Agent参与决策下的降水对交通影响</span>
                    <div>
                      <el-button type="success" @click="selectBtnClick(3)" plain disabled>已选定</el-button>
                      <el-button type="success" @click="editCompleted()">编辑完成</el-button>
                    </div>
                  </div>
                </template>
                <div class="line-style" style="display: flex">
                  <div style="width: 50%">
                    <p style="line-height: 30px">
                      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                      探索AI大模型Agent参与下，如何通过智能调度、预测与实时决策，提升降水期间城市交通的运行效率与安全性。
                    </p>
                    <el-cascader v-model="predictiveMethod"
                                 :options="predictiveResearch" :props="props"
                                 placeholder="请选择智能决策分析方法"
                                 @change="testChange()"
                                 style="width: 60%; margin-top: 1rem"/>
                  </div>
                  <div>
                    <el-divider direction="vertical" style="height: 100%"/>
                  </div>
                  <div style="width: 50%">
                    <div style="margin-left: 1rem" v-if="predictiveMethod.length === 0">
                      <p class="explain-text-title">详细介绍</p>
                      <div class="unselected-right-card">
                        请在左侧选择具体的方法
                      </div>
                    </div>
                    <div style="margin-left: 1rem" v-if="predictiveMethod.length === 1 && predictiveMethod[0] === 1">
                      <p class="explain-text-title">黑盒AI调度分析</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;利用AI大模型进行交通流预测与调度优化，分析其在降水情景下的实际表现与优势。</p>
                      <el-checkbox-group v-model="predictiveSubMethod1" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="预测准确率">预测准确率</el-checkbox>
                        <el-checkbox label="调度响应速度">调度响应速度</el-checkbox>
                        <el-checkbox label="系统鲁棒性">系统鲁棒性</el-checkbox>
                      </el-checkbox-group>
                    </div>
                    <div style="margin-left: 1rem" v-if="predictiveMethod.length === 1 && predictiveMethod[0] === 2">
                      <p class="explain-text-title">白盒决策机制剖析</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;解析AI决策过程，理解其在降水期间对交通调度的具体优化逻辑与可解释性。</p>
                      <el-checkbox-group v-model="predictiveSubMethod2" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="决策规则透明度">决策规则透明度</el-checkbox>
                        <el-checkbox label="可解释性分析">可解释性分析</el-checkbox>
                        <el-checkbox label="优化建议">优化建议</el-checkbox>
                      </el-checkbox-group>
                    </div>
                  </div>
                </div>
              </el-card>
              <el-card class="card-style-1" shadow="hover" v-if="selectedCard === 4">
                <template #header>
                  <div class="card-header">
                    <span>多种策略对比下的降水对交通影响</span>
                    <div>
                      <el-button type="success" plain disabled>已选定</el-button>
                      <el-button type="success" @click="editCompleted()">编辑完成</el-button>
                    </div>
                  </div>
                </template>
                <div class="line-style" style="display: flex">
                  <div style="width: 50%">
                    <p style="line-height: 30px">
                      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
                      综合对比无干预、简单策略、AI智能决策等多种应对措施下，降水对城市交通运行的影响差异与反馈。
                    </p>
                    <el-cascader v-model="parallelMethod"
                                 :options="parallelOptimization" :props="props"
                                 placeholder="请选择对比分析方法"
                                 @change="testChange()"
                                 style="width: 60%; margin-top: 1rem"/>
                  </div>
                  <div>
                    <el-divider direction="vertical" style="height: 100%"/>
                  </div>
                  <div style="width: 50%">
                    <div style="margin-left: 1rem" v-if="parallelMethod.length === 0">
                      <p class="explain-text-title">详细介绍</p>
                      <div class="unselected-right-card">
                        请在左侧选择具体的方法
                      </div>
                    </div>
                    <div style="margin-left: 1rem" v-if="parallelMethod.length === 1 && parallelMethod[0] === 1">
                      <p class="explain-text-title">策略优化对比</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;对比不同干预策略在降水期间对交通运行效率、拥堵缓解、事故减少等方面的优化效果。</p>
                      <el-checkbox-group v-model="parallelSubMethod1" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="效率提升幅度">效率提升幅度</el-checkbox>
                        <el-checkbox label="事故率变化">事故率变化</el-checkbox>
                        <el-checkbox label="拥堵缓解效果">拥堵缓解效果</el-checkbox>
                      </el-checkbox-group>
                    </div>
                    <div style="margin-left: 1rem" v-if="parallelMethod.length === 1 && parallelMethod[0] === 2">
                      <p class="explain-text-title">模型优化对比</p>
                      <p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;分析不同决策模型在降水情景下的适应性与优化能力，为城市交通管理提供决策参考。</p>
                      <el-checkbox-group v-model="parallelSubMethod2" style="margin-top: 10px; font-size: 20px;">
                        <el-checkbox label="模型适应性">模型适应性</el-checkbox>
                        <el-checkbox label="优化空间">优化空间</el-checkbox>
                        <el-checkbox label="实际应用反馈">实际应用反馈</el-checkbox>
                      </el-checkbox-group>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>
          </el-scrollbar>
        </div>
      </el-card>
      <el-card style="width: 400px; height: 80px; position: absolute; top: 24vh; left: calc(25% - 200px);"
               shadow="never" v-if="analysisPercentageShow">
        <div style="display: flex; width: 100%; height: 40px; align-items: center;">
          <span style="font-size: 16px">正在解析：</span>
          <el-progress :percentage="analysisPercentage" :stroke-width="15" striped
                       :color="customColors" style="width: 260px" />
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import request from "../../utils/request";
import {ElMessage, ElNotification} from "element-plus";
import {Plus} from "@element-plus/icons-vue";
import * as echarts from "echarts";
import ChatWithAgent from '../../components/ChatWithAgentD.vue';

export default {
  name: "PowerGame_ExperimentGoalDesign",
  components: { Plus, ChatWithAgent },
  setup() {
    const cardMaxHeight = ref(100)
    const props = {
      expandTrigger: 'hover'
    }
    const loadingAnimation = ref(false)
    const analysisPercentage = ref(0)
    const customColors = [
      { color: '#f56c6c', percentage: 20 },
      { color: '#e6a23c', percentage: 40 },
      { color: '#5cb87a', percentage: 60 },
      { color: '#1989fa', percentage: 80 },
      { color: '#6f7ad3', percentage: 100 },
    ]
    return {
      cardMaxHeight, props, loadingAnimation, analysisPercentage,
      customColors
    }
  },
  data() {
    return {
      Title: '实验目标设计',
      selectedCard: 0,
      showModel: 0,
      demandText: '',
      selectedCardName: ['', '无干扰状态下的降水对交通影响', '简单策略下的降水对交通影响', '大模型Agent参与决策下的降水对交通影响', '多种策略对比下的降水对交通影响'],
      descriptiveMethod: [],
      descriptiveResearch: [
        {value: 1, label: '历史交通数据分析',},
        {value: 2, label: '现场观测法',},
        {value: 3, label: '问卷调查法',},
        {value: 4, label: '交通仿真建模',},
      ],
      descriptiveMethod: [],
      descriptiveResearch: [
        {value: 1, label: '历史交通数据分析',},
        {value: 2, label: '现场观测法',},
        {value: 3, label: '问卷调查法',},
        {value: 4, label: '交通仿真建模',},
      ],
      descriptiveSubMethod1: [],
      descriptiveSubResearch1: [
        { value: 1, label: '交通流量变化' },
        { value: 2, label: '平均车速' },
        { value: 3, label: '事故率' },
        { value: 4, label: '延误时长' },
      ],
      descriptiveSubMethod2: [],
      descriptiveSubResearch2: [
        { value: 1, label: '积水点分布' },
        { value: 2, label: '拥堵路段' },
        { value: 3, label: '事故多发区' },
      ],
      descriptiveSubMethod3: [],
      descriptiveSubResearch3: [
        { value: 1, label: '出行满意度' },
        { value: 2, label: '主要困难' },
        { value: 3, label: '建议与意见' },
      ],
      descriptiveSubMethod4: [],
      descriptiveSubResearch4: [
        { value: 1, label: '仿真降水强度' },
        { value: 2, label: '仿真路网规模' },
        { value: 3, label: '仿真时段' },
      ],
      explainMethod: [],
      explainResearch: [
        {
          value: 1, label: '交通管制效果分析',
          children: [
            {
              value: 1, label: '局部交通管制效果分析',
            },
            {
              value: 2, label: '全局交通管制效果分析',
            },
          ]
        },
        {value: 2, label: '离散分析',},
        {value: 3, label: '敏感性分析'},
        {value: 4, label: '稳健性分析'},
        {value: 5, label: '模型分析'},
      ],
      explainSubMethod1: [],
      explainSubResearch1: [
        { value: 1, label: '管制路段选择' },
        { value: 2, label: '管制时段' },
        { value: 3, label: '交通流恢复速度' },
      ],
      explainSubMethod2: [],
      explainSubResearch2: [
        { value: 1, label: '关键变量分析' },
        { value: 2, label: '敏感性排序' },
        { value: 3, label: '风险点定位' },
      ],
      predictiveMethod: [],
      predictiveResearch: [
        {value: 1, label: '黑盒AI调度分析',},
        {value: 2, label: '白盒决策机制剖析',},
      ],
      predictiveSubMethod1: [],
      predictiveSubResearch1: [
        { value: 1, label: '预测准确率' },
        { value: 2, label: '调度响应速度' },
        { value: 3, label: '系统鲁棒性' },
      ],
      predictiveSubMethod2: [],
      predictiveSubResearch2: [
        { value: 1, label: '决策规则透明度' },
        { value: 2, label: '可解释性分析' },
        { value: 3, label: '优化建议' },
      ],
      parallelMethod: [],
      parallelOptimization: [
        {value: 1, label: '策略优化对比',},
        {value: 2, label: '模型优化对比',},
      ],
      parallelSubMethod1: [],
      parallelSubResearch1: [
        { value: 1, label: '效率提升幅度' },
        { value: 2, label: '事故率变化' },
        { value: 3, label: '拥堵缓解效果' },
      ],
      parallelSubMethod2: [],
      parallelSubResearch2: [
        { value: 1, label: '模型适应性' },
        { value: 2, label: '优化空间' },
        { value: 3, label: '实际应用反馈' },
      ],
      goalContent: [],
      goalContentName: [],
      analysisPercentageShow: false,
      demandChart: null,
      demandOption: {},
      demandData: [
        {id: '0', symbol: 'image://https://cdn.luogu.com.cn/upload/image_hosting/y4b178hg.png',
          symbolSize: 60, name: '需求加工厂', label: '需求加工厂'}
      ],
      demandLink: [],
      documentData: [
        '关于美国肯尼迪政府内部讨论古巴导弹危机应对策略的会议纪要', '苏联赫鲁晓夫与古巴卡斯特罗之间的通信记录', '土耳其领导人杰马勒・古尔塞尔关于本国在北约中角色及对古巴导弹危机立场的讲话记录',
        '冷战时期美苏核军备竞赛的历史背景报告', '美国对古巴长期经济封锁和军事威胁的相关文件汇编', '20 世纪 60 年代国际格局与地缘政治形势分析报告',
        '《联合国宪章》相关条款解读及在古巴导弹危机中的适用性分析', '《部分禁止核试验条约》与古巴导弹危机的关系研究', '国际法中关于领海、领土主权及军事行动限制的相关规定在古巴导弹危机中的案例分析'
      ],
      trafficFlowCascade: [],
      trafficFlowCascadeOptions: [
        {
          value: '高峰时段',
          label: '高峰时段',
          children: [
            { value: '主干道', label: '主干道' },
            { value: '次干道', label: '次干道' },
            { value: '支路', label: '支路' }
          ]
        },
        {
          value: '平峰时段',
          label: '平峰时段',
          children: [
            { value: '主干道', label: '主干道' },
            { value: '次干道', label: '次干道' },
            { value: '支路', label: '支路' }
          ]
        }
      ],
      cascadeProps: { expandTrigger: 'hover' },
      // 交通流量变化级联选择器
      trafficFlowCascader: [],
      trafficFlowCascaderOptions: [
        {
          value: '时段类型',
          label: '时段类型',
          children: [
            { value: '早高峰', label: '早高峰' },
            { value: '晚高峰', label: '晚高峰' },
            { value: '平峰', label: '平峰' }
          ]
        },
        {
          value: '道路类型',
          label: '道路类型',
          children: [
            { value: '主干道', label: '主干道' },
            { value: '次干道', label: '次干道' },
            { value: '支路', label: '支路' }
          ]
        }
      ],
      // 平均车速级联选择器
      avgSpeedCascader: [],
      avgSpeedCascaderOptions: [
        {
          value: '时段类型',
          label: '时段类型',
          children: [
            { value: '早高峰', label: '早高峰' },
            { value: '晚高峰', label: '晚高峰' },
            { value: '平峰', label: '平峰' }
          ]
        },
        {
          value: '道路类型',
          label: '道路类型',
          children: [
            { value: '主干道', label: '主干道' },
            { value: '次干道', label: '次干道' },
            { value: '支路', label: '支路' }
          ]
        }
      ],
    }
  },
  created() {

  },
  mounted() {
    console.log(this.$refs.contentCard)
    let cardHeight = this.$refs.contentCard.$el.offsetHeight;
    console.log('height', cardHeight);
    this.cardMaxHeight = cardHeight - 64;
    console.log(this.cardMaxHeight)
    this.loadDemandChart();
  },
  methods: {
    goBack() {
      this.$router.push('/home/rainCity/expDesign');
    },
    selectBtnClick(value) {
      console.log('click ', value);
      this.showModel = 1;
      this.selectedCard = value;
      this.explainMethod = [];
      this.parallelMethod = [];
      this.predictiveMethod = [];
      this.descriptiveMethod = [];
    },
    testChange() {
      let arr = []
      if (this.selectedCard === 1) {
        this.goalContent = this.descriptiveMethod;
        arr = this.descriptiveResearch;
      } else if (this.selectedCard === 2) {
        this.goalContent = this.explainMethod;
        arr = this.explainResearch;
      } else if (this.selectedCard === 3) {
        this.goalContent = this.predictiveMethod;
        arr = this.predictiveResearch;
      } else if (this.selectedCard === 4) {
        this.goalContent = this.parallelMethod;
        arr = this.parallelOptimization;
      }
      // 递归查找完整 label 路径
      const getLabelPath = (options, path) => {
        let labels = [];
        let currentOptions = options;
        for (let i = 0; i < path.length; i++) {
          const val = path[i];
          const found = currentOptions.find(opt => opt.value === val);
          if (found) {
            labels.push(found.label);
            currentOptions = found.children || [];
          } else {
            break;
          }
        }
        return labels;
      };
      this.goalContentName = getLabelPath(arr, this.goalContent);
    },
    editCompleted() {
      this.loadingAnimation = true;
      localStorage.setItem('experimentGoal', JSON.stringify({
        goal_index: this.selectedCard,
        goal_name: this.selectedCardName[this.selectedCard],
        goal_content_index: this.goalContent,
        goal_content_name: this.goalContentName,
      }));
      // 临时注释掉接口请求，直接跳转
      this.loadingAnimation = false;
      this.$router.push('/home/rainCity/expDesign');
      // request.post('/setExperimentParam', {
      //   'experiment_goal': {
      //     'goal_index': this.selectedCard,
      //     'goal_name': this.selectedCardName[this.selectedCard],
      //     'goal_content_index': this.goalContent,
      //     'goal_content_name': this.goalContentName,
      //   },
      // }).then(res => {
      //   this.loadingAnimation = false;
      //   this.$router.push('/home/rainCity/expDesign')
      // }).catch(err => {
      //   this.loadingAnimation = false;
      //   // 可选：提示错误
      // });
    },

    demandAnalysis(){
      this.analysisPercentage = 0;
      this.analysisPercentageShow = true;
      let timeLeft = 10
      let timer = setInterval(() => {
        --timeLeft;
        if(timeLeft < 0) {
          clearInterval(timer);
          this.analysisPercentageShow = false;
          ElMessage({
            type: 'success',
            message: '需求解析完成'
          })
        }
        this.analysisPercentage += 10;
      }, 1000)
      //
    },
    demandChartNodeClick(param){
      console.log(param)
      if(param.data.id === '0') return ;
      this.documentData.push(param.data.label);
      this.demandLink.splice(this.demandLink.length-1, 1);
      this.demandData.splice(parseInt(param.data.id), 1)
      for (let i = 1; i < this.demandData.length; i++) {
        this.demandData[i].id = '' + i
        this.demandData[i].name = 'Doc' + i
      }
      this.demandOption.series[0].data = this.demandData;
      this.demandOption.series[0].links = this.demandLink;
      this.demandChart.setOption(this.demandOption);
      ElMessage({
        type: 'warning',
        message: '删除成功'
      })
    },
    loadDemandChart(){
      this.$nextTick(() => {
        this.demandChart = echarts.init(document.getElementById('demandChart'));
        this.demandChart.resize();
        this.demandChart.on('click', this.demandChartNodeClick);
        this.demandOption = {
          title: {
            show: true,
            text: '点击右侧文件添加需求解析涉及的知识图谱',
            left: 'center',
          },
          tooltip: {
            formatter: function (params) {
              return params.data.label;
            }
          },
          series: [{
            type: 'graph',
            layout: 'force',
            force: {
              repulsion: 150,
              edgeLength: 100
            },
            draggable: true,
            symbolSize: 40,
            roam: true,
            label: {
              show: true,
              fontSize: 10
            },
            edgeSymbol: ['circle', 'arrow'],
            edgeSymbolSize: [4, 4],
            edgeLabel: {
              show: false,
              fontSize: 12
            },
            data: this.demandData,
            links: this.demandLink,
            itemStyle:{
              color: 'rgb(242.5, 208.5, 157.5)'
            },
            lineStyle: {
              opacity: 0.9,
              width: 2,
              curveness: 0,
            },
          }],
          animationDurationUpdate: 1500,
        }
        this.demandChart.setOption(this.demandOption);
      })
    },
    docAdd(index){
      this.demandData.push({
        id: '' + this.demandData.length,
        name: 'Doc' + this.demandData.length,
        label: this.documentData[index]
      })
      this.demandLink.push({
        source: '0',
        target: '' + (this.demandData.length - 1)
      })
      this.demandOption.series[0].data = this.demandData;
      this.demandOption.series[0].links = this.demandLink;
      this.demandChart.setOption(this.demandOption);
      this.documentData.splice(index,1);
      ElMessage({
        type: 'success',
        message: '添加成功'
      })
    }
  },
}
</script>

<style scoped>
.cardStyle {
  width: 98%;
  margin: 0 2% 1rem 0;
  height: 18vh;
}

.card-style-1 {
  width: 96%;
  margin: 0 2%;
}

.card-style-3 {
  width: 30%;
  margin: 0 1.5%;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.explain-text-title {
  font-size: 20px;
  font-weight: bolder;
  margin-bottom: 10px;
}

.unselected-right-card {
  height: 220px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  color: #909399;
}

.line-style {
  font-size: 16px;
  line-height: 25px;
}

:deep(.el-breadcrumb__inner) {
  font-size: 16px;
  line-height: 24px;
}

.docStyle{
  display: flex;
  width: 100%;
  align-items: center;
  padding: 5px 0;
  font-size: 14px;
  color: #000000;
  cursor: pointer;
}
.docStyle:hover{
  color: #409EFF;
}
</style>