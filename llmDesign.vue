<template>
  <div style="width: 99%; min-width:1200px; display: flex">
    <div style="width: 99%; min-width: 1200px; display: inline;">
      <el-card style="width: 100%;height: 98%">
        <div style="display: flex; height: 100%; width: 100%; margin-top: 2rem">
          <!--	左侧卡片   -->
          <el-card style="width: 30%; height: 80vh; margin-right: 10px;">
            <template #header>
              <span class="title-font">我的Agent</span>
            </template>
            <div style="display: flex; flex-direction: row; flex-wrap: wrap; justify-content: center;">
              <el-card v-for="(item, index) in classInfo" :key="index" shadow="hover"
                       class="agent-card-pos" @click="cardClick(index)"
                       :style="{width: cardIsExpand[index] ? '100%' : '', background: cardIsExpand[index] ? 'rgb(243.9, 244.2, 244.8)' : '#FFF'}">
                <div style="display: flex; width: 100%; height: 145px; flex-direction: column; align-items: center; justify-content: center;"
                    v-if="!cardIsExpand[index]">
                  <el-image :src="item.imgUrl" style="width: 56%; margin-left:0 auto;" fit="cover"></el-image>
                  <span style="font-size: 16px; font-weight: bold">{{ item.name }}</span>
                  <div>
                    <el-tag type="success" size="small" v-if="item.state === 1">设计完成</el-tag>
                    <el-tag type="info" size="small" v-else>等待设计</el-tag>
                  </div>
                </div>

                <div style="display: flex; width: 100%; flex-direction: column;" v-else>
                  <div style="display: flex; width: 100%; align-items: center; justify-content: space-between;">
                    <el-image :src="item.imgUrl" style="width: 8%" fit="cover"></el-image>
                    <span style="font-size: 16px; font-weight: bold; margin-left: 1rem">{{ item.name }}</span>
                    <el-tag type="success" v-if="item.state === 1">设计完成</el-tag>
                    <el-tag type="info" v-else>等待设计</el-tag>
                  </div>
                  <div style="display: flex; flex-direction: column; align-items: flex-start; line-height: 150%; width: 100%; margin-top: 1rem">
                    <span v-if="item.agentList.length === 0">请添加智能体</span>
                    <span v-for="(agentItem, agentIndex) in item.agentList" v-else>
                      Agent {{ agentIndex + 1}}: {{ agentItem }}
                    </span>
                  </div>
                </div>
              </el-card>
            </div>
          </el-card>
          <!--	右侧卡片  	-->
          <el-card style="width: 69%; height: 80vh; margin-left: 1%">
            <template #header>
              <span class="title-font">
                您正在设计Agent：
                <span style="color: rgb(237.5, 189.9, 118.5)">{{ index2Name[tmpCardIndex] }}</span>
              </span>
            </template>
            <div style="display: flex; justify-content: center; width: 100%; margin: 1rem 0">
              <el-steps style="width: 85%" :active="active" finish-status="success" align-center>
                <el-step title="感知Observation"/>
                <el-step title="判断Orientation"/>
                <el-step title="决策Decision"/>
                <el-step title="行为Action"/>
              </el-steps>
            </div>
            <div style="display: flex; width: 100%; margin-top: 2rem">
              <div id="oodaChart" style="height: 50vh; width: 100%"/>
            </div>
            <div style="display: flex; justify-content: center; width: 100%;">
              <el-button type="primary" @click="preStep()">上一步</el-button>
              <el-button type="success" @click="changeAgentCard()" :disabled="active !== 4">确认修改</el-button>
            </div>
          </el-card>
        </div>
      </el-card>

      <el-dialog v-model="flowChartVisible" title="agent流程图" width="50%" center>
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
          <el-image style="height: 500px;" :src="perceptUrl" :fit="fit"/>
        </div>
      </el-dialog>
      <el-dialog v-model="observationDialogVisible" title="观察" width="40%" center top="20vh">
        <div style="display: flex; justify-content: center; width: 100%;flex-direction: column;">
          <el-form :model="newTemplate[tmpCardIndex]">
            <el-form-item label="感知数据" style="padding-top: 10px;">
              <el-checkbox-group v-model="newTemplate[tmpCardIndex].perceptionSpace">
                <el-checkbox v-for="option in perceptionOptions[tmpCardIndex]" :key="option" :label="option"></el-checkbox>
              </el-checkbox-group>
            </el-form-item>
            <el-form-item label="反馈触发条件" style="padding-top: 10px;">
              <el-radio v-model="newTemplate[tmpCardIndex].gameType" label="complete">数据质量阈值
                <el-tooltip
                    content="数据完整性≥90%、准确性≥85%"
                    placement="top-start"><i
                    class="el-icon-warning"></i></el-tooltip>
              </el-radio>
              <el-radio v-model="newTemplate[tmpCardIndex].gameType" label="uncomplete">异常检测</el-radio>
            </el-form-item>
            <el-form-item v-if="newTemplate[tmpCardIndex].gameType === 'uncomplete'" label="检测方法"
                          style="padding-top: 10px;">
              <el-checkbox-group v-model="newTemplate[tmpCardIndex].gameInfo">
                <el-checkbox label="统计"></el-checkbox>
                <el-checkbox label="机器学习"></el-checkbox>
              </el-checkbox-group>
            </el-form-item>
          </el-form>
        </div>
        <div style="display: flex; justify-content: center; width: 100%; margin-top: 20px;">
          <el-button type="primary" @click="pieDesignFinish(0)">完成设计</el-button>
        </div>
      </el-dialog>
      <el-dialog v-model="orientationDialogVisible" title="判断" width="40%" center top="20vh">
        <el-form :model="newTemplate[tmpCardIndex]">
          <el-form-item label="评估内容" style="padding-top: 10px;">
            <el-select v-model="newTemplate[tmpCardIndex].situationParam" multiple placeholder="请选择LLMAgent评估内容"
                       style="width: 50%;">
                       <el-option v-for="option in situationParamOptions[tmpCardIndex]" :key="option" :label="option" :value="option"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="城市内涝风险程度判断">
            <el-radio v-model="newTemplate[tmpCardIndex].situationOrient" label="LLM">LLM自主判断</el-radio>
            <el-radio v-model="newTemplate[tmpCardIndex].situationOrient" label="formula">公式计算</el-radio>
          </el-form-item>
          <el-form-item v-if="newTemplate[tmpCardIndex].situationOrient === 'formula'" label="计算公式"
                        style="padding-top: 10px;">
            <el-select v-model="newTemplate[tmpCardIndex].situationFormula" placeholder="请选择">
              <el-option
                  v-for="item in situationFormulaOptions"
                  :key="item.value"
                  :label="item.label"
                  :value="item.value">
              </el-option>
            </el-select>

          </el-form-item>


        </el-form>
        <div style="display: flex; justify-content: center; width: 100%; margin-top: 20px;">
          <el-button type="primary" @click="pieDesignFinish(1)">完成设计</el-button>
        </div>
      </el-dialog>
      <el-dialog v-model="decisionDialogVisible" title="决策" width="80%" center top="20vh">
        <div style="display: flex; width: 100%;">
          <!-- 左侧决策智能体展示列 -->
          <div style="width: 40%; border-right: 1px solid #ccc; padding: 10px;">
            <el-card v-for="(agent, index) in newTemplate[tmpCardIndex].agentList" :key="index" shadow="never"
                     style="width: 98%; margin-bottom: 1rem; line-height: 150%;">
              <p><b>知识库:</b> {{ agent.roleName }}</p>
              <p><b>角色与目标:</b> {{ agent.NPCPrompt }}</p>
              <p><b>行为准则:</b> {{ agent.guidelinePrompt }}</p>
            </el-card>
          </div>
          <!-- 右侧设计内部决策智能体列 -->
          <div style="width: 60%; padding: 10px;">
            <div style="display: flex; justify-content: center; width: 100%;flex-direction: column;">
              <el-form :model="newDecisionAgentTemplate" label-position="top" ref="formRef">
                <el-form-item label="接入知识库">
                  <el-select v-model="newDecisionAgentTemplate.roleModeling"
                             placeholder="请选择" @change="agentSelectChange()">
                    <el-option v-for="(item, index) in newTemplate[tmpCardIndex].agentOptions"
                               :key="index" :label="item.label" :value="item.value" />
                  </el-select>
                  <el-input
                      v-if="newDecisionAgentTemplate.roleModeling === 0"
                      v-model="newDecisionAgentTemplate.customRoleName"
                      placeholder="请输入知识库链接" style="margin-top: 10px;"></el-input>
                </el-form-item>
                <el-form-item prop="prompt">
                  <span>角色与目标</span>
                  <el-tooltip content="说明智能体的身份和专业领域并描述其最终希望实现的结果"
                              placement="top-start"><i class="el-icon-warning"></i></el-tooltip>
                  <el-input
                      v-model="newDecisionAgentTemplate.NPCPrompt"
                      type="textarea"
                      placeholder="例如“你是一个城市内涝应急指挥中心的核心智能体，可以针对内涝灾害的实时情况，结合气象学、水文科学、城市规划和应急管理等专业知识，为城市管理者提供全面的灾害应对指导和资源协调方案。你的目标是快速评估内涝影响，制定有效的疏散和救援策略，确保市民生命安全、减少财产损失，并维持城市基本功能的正常运行。”"
                      rows="3"
                      required
                  ></el-input>
                </el-form-item>
                <el-form-item prop="prompt">
                  <span>行为准则</span>
                  <el-tooltip content="描述您希望智能体具备的准则或底线，包括角色内心的想法或者对城市调控的准则底线。"
                              placement="top-start"><i class="el-icon-warning"></i></el-tooltip>
                  <el-input
                      v-model="newDecisionAgentTemplate.guidelinePrompt"
                      type="textarea"
                      placeholder="例如“你正在扮演城市内涝应急指挥中心的核心智能体，你的准则是不惜一切代价保护市民生命安全，并确保灾害响应措施不会导致城市功能的全面瘫痪。”"
                      rows="3"
                      required
                  ></el-input>
                </el-form-item>
              </el-form>
            </div>
            <div style="display: flex; justify-content: center; width: 100%;">
              <el-button type="primary" @click="addAgent(tmpCardIndex)">添加</el-button>
              <el-button type="primary" @click="pieDesignFinish(2)">完成设计</el-button>
            </div>
          </div>
        </div>
      </el-dialog>
      <el-dialog v-model="actionDialogVisible" title="行为" width="40%" center>
        <el-form :model="newTemplate[tmpCardIndex]" label-position="top" ref="formRef">
          <el-form-item label="策略空间" style="padding-top: 10px;">
            <el-checkbox-group v-model="newTemplate[tmpCardIndex].gameStrategy">
              <el-checkbox v-for="strategy in strategyOptions[tmpCardIndex]" :key="strategy" :label="strategy">{{ strategy }}</el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="行为空间">
            <el-select v-model="newTemplate[tmpCardIndex].actionSpace" multiple placeholder="请选择行为空间" style="width: 50%;">
              <el-option v-for="(option, index) in actionOptions[tmpCardIndex]" :key="index" :label="option" :value="index + 1" />
            </el-select>
          </el-form-item>
        </el-form>
        <div style="display: flex; justify-content: center; width: 100%; margin-top: 20px;">
          <el-button type="primary" @click="pieDesignFinish(3)">完成设计</el-button>
        </div>
      </el-dialog>
    </div>
  </div>
</template>

<script>
import {reactive, ref} from 'vue'
import {ElMessage} from "element-plus";
import ChatWithAgent from '../../components/ChatWithAgent.vue';
import * as echarts from "echarts";

export default {
  components: {
    ChatWithAgent
  },
  name: "PowerGame_llmDesign",
  setup() {
    const envType = ref("0")
    const active = ref(0)
    const form = reactive({
      social: true,
      nature: true,
      otherAgent: false,
      map: true,
      weather: false,
      sameAgent: false,
      differentAgent: false,
      sysAgent: false,
      rider: false,
      platform: false,
      brainType: 0,
      evoType: 0,
      user: false,
      market: false,
      buy: false,
      work: false,
      walk: false,
      learningType: '0',
      workStatus: 10,
      sex: 1,
      order: true,
      talk: false,
      rest: true,
      dayRatio: 0.5,
      talkRatio: 3,
      name: 'llmAgent',
      decType: '0'
    });
    const newDecisionAgentTemplate = ref ({
      NPCPrompt: '',
      guidelinePrompt: '',
      roleModeling: '',
      customRoleName: ''
    })
    return {
      form, active, envType, newDecisionAgentTemplate
    }
  },
  data() {
    return {
      // 新增策略空间选项
      strategyOptions: {
        1: ["优先级排序策略", "分散响应策略", "预防性储备策略", "动态调整策略"], // PolicyAgent
        2: ["需求导向策略", "绕行优化策略", "应急增援策略", "协同调度策略"], // 公交调度Agent
        3: ["多渠道传播策略", "分级预警策略", "行为引导策略", "反馈调整策略"], // 政策发布Agent
        4: ["分区管制策略", "动态疏导策略", "优先通行策略", "渐进式恢复策略"] // 交通管制Agent
      },

      // 新增行为空间选项
      actionOptions: {
        1: ["发布疏散令", "启动救援", "协调企业支持"], // PolicyAgent
        2: ["执行路线调整", "通知乘客", "增加班次"], // 公交调度Agent
        3: ["发布公告", "召开新闻会", "更新信息"], // 政策发布Agent
        4: ["实施封路", "调整信号", "通知驾驶员"] // 交通管制Agent
      },
      situationParamOptions: {
        1: ["积水深度", "受灾范围", "市民安全风险"], // PolicyAgent
        2: ["公交延误时间", "乘客满意度", "道路通行能力"], // 公交调度 Agent
        3: ["政策覆盖率", "公众接受度", "媒体反应"], // 政策发布 Agent
        4: ["交通拥堵程度", "事故率", "可通行路段比例"] // 交通管制 Agent
      },
      perceptionOptions: {
        1: ["降雨量", "水位", "道路状况", "电力供应状态", "市民求助信息"], // PolicyAgent
        2: ["公交车位置", "道路积水情况", "乘客需求"], // 公交调度Agent
        3: ["内涝态势", "现有政策", "公众反馈"], // 政策发布Agent
        4: ["交通流量", "积水路段", "事故报告"] // 交通管制Agent
      },
      rules: {
        name: [{required: true, message: 'Agent名称是必填项', trigger: 'blur'}],
        prompt: [{required: true, message: '角色定义是必填项', trigger: 'blur'}]
      },
      situationFormulaOptions: [
        {value: 'Option1', label: '公式1'},
        {value: 'Option3', label: '公式2'},
        {value: 'Option4', label: '公式3'},
        {value: 'Option2', label: '自定义公式'},
      ],
      newTemplate: [
        {},
        {
          name: '',
          model: '',
          NPCPrompt: "",
          memoryMechanism: 'relevance',
          gameStrategy: [],
          perceptionSpace: [],
          gameType: '',
          gameInfo: [],
          situationOrient: '',
          situationFormula: '',
          situationParam: [],
          guidelinePrompt: '',
          actionSpace: [],
          agentList: [],
          agentOptions: [
            {label: "城市内涝知识库", value: 1},
            {label: "外接知识库", value: 0},
          ]
        },
        {
          name: '',
          model: '',
          NPCPrompt: "",
          memoryMechanism: 'relevance',
          gameStrategy: [],
          perceptionSpace: [],
          gameType: '',
          gameInfo: [],
          situationOrient: '',
          situationFormula: '',
          situationParam: [],
          guidelinePrompt: '',
          actionSpace: [],
          agentList: [],
          agentOptions: [
            {label: "城市内涝知识库", value: 2},
            {label: "外接知识库", value: 0},
          ]
        },
        {
          name: '',
          model: '',
          NPCPrompt: "",
          memoryMechanism: 'relevance',
          gameStrategy: [],
          perceptionSpace: [],
          gameType: '',
          gameInfo: [],
          situationOrient: '',
          situationFormula: '',
          situationParam: [],
          guidelinePrompt: '',
          actionSpace: [],
          agentList: [],
          agentOptions: [
            {label: "城市内涝知识库", value: 3},
            {label: "外接知识库", value: 0},
          ]
        },
        {
          name: '',
          model: '',
          NPCPrompt: "",
          memoryMechanism: 'relevance',
          gameStrategy: [],
          perceptionSpace: [],
          gameType: '',
          gameInfo: [],
          situationOrient: '',
          situationFormula: '',
          situationParam: [],
          guidelinePrompt: '',
          actionSpace: [],
          agentList: [],
          agentOptions: [
            {label: "城市内涝知识库", value: 4},
            {label: "外接知识库", value: 0},
          ]
        }
      ],
      orientationDialogVisible: false,
      actionDialogVisible: false,
      observationDialogVisible: false,
      flowChartVisible: false,
      decisionDialogVisible: false,
      changeVisible: false,
      nameVisible: false,
      imageUrl: '/static/icons/aibot.png',
      perceptUrl: '/static/flowcharts/perception.jpeg',
      percptionOneUrl: '/static/flowcharts/random.png',
      percptionTwoUrl: '/static/flowcharts/ifelse.png',
      percptionThreeUrl: '/static/flowcharts/learning.png',
      brainUrl: '/static/icons/brain.png',
      perceptionUrl: '/static/icons/perception.png',
      actionUrl: '/static/icons/move.png',
      learnUrl: '/static/icons/read.png',
      imagesStore: [
        require('@/assets/images/flags/flag-Russia.png'),
        require('@/assets/images/flags/flag-Cuba.png'),
        '/static/icons/bot1.png',
        '/static/icons/bot2.png',
        '/static/icons/bot3.png',
        '/static/icons/bot4.png',
      ],
      classInfo: [
        {
          imgUrl: require('@/assets/images/people/policyagent.png'),
          name: 'PolicyAgent',
          index: 1,
          state: 0,
          agentList: [],
        }, {
          imgUrl: require('@/assets/images/people/busdispatching.png'),
          name: '公交调度Agent',
          index: 2,
          state: 0,
          agentList: [],
        }, {
          imgUrl: require('@/assets/images/people/informationrelease.png'),
          name: '政策发布Agent',
          index: 3,
          state: 0,
          agentList: [],
        }, {
          imgUrl: require('@/assets/images/people/trafficcontrol.png'),
          name: '交通管制Agent',
          index: 4,
          state: 0,
          agentList: [],
        },
      ],
      index2Name: ['Null', 'PolicyAgent', '公交调度Agent', '政策发布Agent', '交通管制Agent'],
      tmpCardIndex: 0,
      cardIsExpand: [false, false, false, false],
      newAgentImage: '/static/icons/bot1.png',

      oodaChart: null,
      oodaOption: {},
      oodaData: [
        {value: 100, name: 'Observation', itemStyle: {color: 'rgb(177.3, 179.4, 183.6)'}},
        {value: 100, name: 'Orientation', itemStyle: {color: 'rgb(221.7, 222.6, 224.4)'}},
        {value: 100, name: 'Decision', itemStyle: {color: 'rgb(221.7, 222.6, 224.4)'}},
        {value: 100, name: 'Action', itemStyle: {color: 'rgb(221.7, 222.6, 224.4)'}}
      ],
      pieDefaultColor: 'rgb(221.7, 222.6, 224.4)',
      pieProcessingColor: 'rgb(177.3, 179.4, 183.6)',
      pieColor: ['rgb(250, 181.5, 181.5)', 'rgb(179, 224.5, 156.5)', 'rgb(237.5, 189.9, 118.5)', 'rgb(121.3, 187.1, 255)'],
    };
  },
  mounted() {
    this.loadOodaChart();
  },
  methods: {
    addAgent(tmpCardIndex) {
      if(this.newDecisionAgentTemplate.roleModeling === 0)
        this.newDecisionAgentTemplate.roleName = this.newDecisionAgentTemplate.customRoleName;
      // 将新的智能体添加到列表中
      this.newTemplate[tmpCardIndex].agentList.push({...this.newDecisionAgentTemplate});
      // 清空输入框
      this.newDecisionAgentTemplate.NPCPrompt = '';
      this.newDecisionAgentTemplate.guidelinePrompt = '';
    },
    agentSelectChange() {
      let newValue = this.newDecisionAgentTemplate.roleModeling;
      if (newValue === 1) {
        this.newDecisionAgentTemplate.roleName = '城市内涝知识库';
        this.newDecisionAgentTemplate.NPCPrompt = '你是一个城市内涝应急指挥中心的核心智能体，可以针对内涝灾害的实时情况，结合气象学、水文科学、城市规划和应急管理等专业知识，为城市管理者提供全面的灾害应对指导和资源协调方案。你的目标是快速评估内涝影响，制定有效的疏散和救援策略，确保市民生命安全、减少财产损失，并维持城市基本功能的正常运行。';
        this.newDecisionAgentTemplate.guidelinePrompt = '你正在扮演城市内涝应急指挥中心的核心智能体，你的准则是不惜一切代价保护市民生命安全，并确保灾害响应措施不会导致城市功能的全面瘫痪。';
      } else if (newValue === 2) {
        this.newDecisionAgentTemplate.roleName = '城市内涝知识库';
        this.newDecisionAgentTemplate.NPCPrompt = '你是一个城市内涝场景中的公交调度智能体，可以针对内涝灾害的实时交通状况，结合交通流量分析、道路通行能力和乘客需求预测等专业知识，为公交系统提供高效的调度方案和应急调整建议。你的目标是优化公交线路和班次安排，确保市民在灾害中的出行安全与便利，同时维持公交服务的稳定运行。';
        this.newDecisionAgentTemplate.guidelinePrompt = '你正在扮演城市内涝场景中的公交调度智能体，你的准则是确保市民在灾害中的出行安全，并避免公交服务因内涝而全面中断。';
      } else if (newValue === 3) {
        this.newDecisionAgentTemplate.roleName = '城市内涝知识库';
        this.newDecisionAgentTemplate.NPCPrompt = '你是一个城市内涝场景中的政策发布智能体，可以针对内涝灾害的实时进展，结合灾害管理、信息传播和公众心理等专业知识，为市民和相关部门提供准确的政策信息和应急指导。你的目标是提高公众对内涝的知情度和应对能力，引导市民采取正确的防护措施，并通过及时透明的信息发布维护社会稳定。';
        this.newDecisionAgentTemplate.guidelinePrompt = '你正在扮演城市内涝场景中的政策发布智能体，你的准则是确保信息发布的准确性和透明性，并避免因信息误导或延迟导致公众恐慌和社会混乱。';
      } else if (newValue === 4) {
        this.newDecisionAgentTemplate.roleName = '城市内涝知识库';
        this.newDecisionAgentTemplate.NPCPrompt = '你是一个城市内涝场景中的交通管制智能体，可以针对内涝灾害的实时路况，结合交通流量分析、道路通行能力和应急疏散需求等专业知识，为城市交通系统提供科学的管制方案和通行指导。你的目标是减少交通拥堵和事故发生，确保救援通道畅通，并为市民和应急车辆提供安全的出行条件。';
        this.newDecisionAgentTemplate.guidelinePrompt = '你正在扮演城市内涝场景中的交通管制智能体，你的准则是确保交通系统在灾害中保持基本畅通，并避免因管制不当导致救援通道阻塞或交通全面瘫痪。';
      } else {
        this.newDecisionAgentTemplate.NPCPrompt = '';
        this.newDecisionAgentTemplate.guidelinePrompt = '';
      }
    },
    handlePieClick(param) {
      console.log('pieClick', param)
      if (this.tmpCardIndex === 0) {
        ElMessage({
          message: '请先点击左侧Agent图片，选择您要设计的智能体',
          type: 'error'
        })
        return;
      }
      if (this.active === param.dataIndex) {
        if (this.active === 0) this.observationDialogVisible = true;
        else if (this.active === 1) this.orientationDialogVisible = true;
        else if (this.active === 2) this.decisionDialogVisible = true;
        else if (this.active === 3) this.actionDialogVisible = true;
      } else {
        ElMessage({
          message: '请点击深灰色扇区，按照步骤设计Agent',
          type: 'error'
        })
      }
    },
    loadOodaChart() {
      this.$nextTick(() => {
        this.oodaChart = echarts.init(document.getElementById('oodaChart'));
        this.oodaChart.on('click', this.handlePieClick);
        this.oodaChart.resize();
        this.oodaOption = {
          tooltip: {
            show: false,
            trigger: 'item'
          },
          legend: {
            top: '5%',
            left: 'center'
          },
          series: [{
            name: 'Access From',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            padAngle: 5,
            itemStyle: {
              borderRadius: 10
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 40,
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: this.oodaData
          }]
        };
        this.oodaChart.setOption(this.oodaOption);
      })
    },
    changeAgentCard() {
      this.classInfo[0].state = 1;
      this.classInfo[0].agentList = [];
      let newAgentList = this.newTemplate[this.tmpCardIndex].agentList;
      for(let i = 0; i < newAgentList.length; i++)
        this.classInfo[0].agentList.push(newAgentList[i].roleName);
      this.active = 0;
      this.newDecisionAgentTemplate.roleModeling = '';
      for (let i = 0; i < this.oodaData.length; i++)
        this.oodaData[i].itemStyle.color = this.pieDefaultColor;
      this.oodaData[0].itemStyle.color = this.pieProcessingColor;
      this.oodaOption.series.data = this.oodaData;
      this.oodaChart.setOption(this.oodaOption);
    },
    cardClick(index) {
      if (this.cardIsExpand[index] === true) {
        this.tmpCardIndex = 0;
        this.cardIsExpand[index] = false;
      } else {
        this.classInfo.unshift(this.classInfo[index]);
        this.classInfo.splice(index + 1, 1);
        this.cardIsExpand = [true, false, false, false];
        this.tmpCardIndex = this.classInfo[0].index;
      }
    },
    pieDesignFinish(value) {
      //观察模块设计完成
      if (value === 0) {
        this.observationDialogVisible = false
      }
      // 判断模块设计完成
      else if (value === 1) {
        this.orientationDialogVisible = false;
      }
      // 决策模块设计完成
      else if (value === 2) {
        this.decisionDialogVisible = false;
      }
      // 行为模块设计完成
      else if (value === 3) {
        this.actionDialogVisible = false;
      }
      this.oodaData[this.active].itemStyle.color = this.pieColor[this.active];
      if (this.active < 3) this.oodaData[this.active + 1].itemStyle.color = this.pieProcessingColor;
      this.oodaOption.series.data = this.oodaData;
      this.oodaChart.setOption(this.oodaOption);
      this.nextStep();
    },
    nextStep() {
      if (this.active++ > 3)
        this.active = 4
    },
    preStep() {
      if (this.active < 4)
        this.oodaData[this.active].itemStyle.color = this.pieDefaultColor;
      if (this.active-- < 1) this.active = 0;
      this.oodaData[this.active].itemStyle.color = this.pieProcessingColor;
      this.oodaOption.series.data = this.oodaData;
      this.oodaChart.setOption(this.oodaOption);
    },
  },
};
</script>

<style scoped>
.agent-card-pos {
  margin: 1rem 2.5%;
  width: 45%;
  height: 180px;
  text-align: center;
  transition: ease-in-out 0.5s;
  cursor: pointer;
}

.title-font {
  font-family: "Microsoft YaHei", serif;
  font-size: 16px;
  font-weight: bold;
}
</style>

