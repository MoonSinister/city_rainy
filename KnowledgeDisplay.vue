<template>
  <template v-if = "collapsed">
    <p class="summary-text">👉 点击查看 Direct 详细信息</p>
  </template>
  <template v-else>
	<div style="width: 100%; min-width:1200px; display: flex; flex-direction: row">
		<el-card style="width: 99%; height: 98%; background-color: #1F2932">
      <div style="display: flex; width: 100%">
        <!--    左侧选项卡    -->
        <el-card class="card-class" style="width: 20%" shadow="never">
          <div style="display: flex; flex-direction: column; align-items: center">
            <el-radio-group v-model="showWayRadio">
              <el-radio-button label="0" class="radio-btn left-radio-btn">
                整体查看
              </el-radio-button>
              <el-radio-button label="1" class="radio-btn">
                节点筛选
              </el-radio-button>
            </el-radio-group>
            <el-select v-model="individualSelection" filterable
                       class="select-class input-class"
                       :prefix-icon="Search"
                       style="margin: 1rem 0 8px 0"
                       v-if="showWayRadio === '1'">
              <el-option
                  v-for="(item, index) in individualOption"
                  :key="index" :value="item.value" :label="item.label"/>
            </el-select>
            <el-tabs v-model="baseActiveName" stretch @tab-click="handleClick"
                     style="width: 100%; color: #fff" class="narrow-tab">
              <el-tab-pane label="知识库" name="0">
                <div style="display: flex; flex-direction: column; width: 100%">
                  <el-card class="click-item-card"
                           :class="itemCardSelection === index ? 'click-item-card-selected' : 'click-item-card-unselected'"
                           v-for="(item, index) in itemCard"
                           @click="itemCardClick(index)">
                    <div class="click-item-card-content">
                      <div style="font-weight: bold">{{item.title}}</div>
                      <div style="font-size: 12px; margin-top: 2px">{{item.subtitle}}</div>
                    </div>
                  </el-card>
                </div>
              </el-tab-pane>
              <el-tab-pane label="环境库" name="1">
                <div style="display: flex; flex-direction: column; width: 100%">
                  <el-card class="click-item-card"
                           :class="itemCardSelection === index ? 'click-item-card-selected' : 'click-item-card-unselected'"
                           v-for="(item, index) in itemCard"
                           @click="itemCardClick(index)" v-show="index > 1">
                    <div class="click-item-card-content">
                      <div style="font-weight: bold">{{item.title}}</div>
                      <div style="font-size: 12px; margin-top: 2px">{{item.subtitle}}</div>
                    </div>
                  </el-card>
                </div>
              </el-tab-pane>
              <el-tab-pane label="规则库" name="2">
                <div style="display: flex; flex-direction: column; width: 100%">
                  <el-card class="click-item-card"
                           :class="itemCardSelection === index ? 'click-item-card-selected' : 'click-item-card-unselected'"
                           v-for="(item, index) in itemCard"
                           @click="itemCardClick(index)" v-show="index > 1">
                    <div class="click-item-card-content">
                      <div style="font-weight: bold">{{item.title}}</div>
                      <div style="font-size: 12px; margin-top: 2px">{{item.subtitle}}</div>
                    </div>
                  </el-card>
                </div>
              </el-tab-pane>
            </el-tabs>
            <el-button type="primary" @click="checkIndividualData()"
                       class="query-btn" style="width: 100%; margin-top: 1rem">查看</el-button>
          </div>
        </el-card>
        <!--    知识库     -->
        <div style="display: flex; width: 80%">
          <!--    中间知识库    -->
          <div style="display: flex; flex-direction: column; width: 60%; margin: 0 1%">
            <!--     基本信息     -->
            <el-card class="card-class" style="width: 100%; height: 250px;">
              <div class="card-header" style="margin-top: -20px">
  <!--              <img src="../../assets/images/flags/flag-America.png" style="height: 20px; width: 35px" alt="flag"/>-->
                <span style="margin-left: 5px">{{ individualInfo.name }}</span>
              </div>
              <el-tabs v-model="activeName" type="card" @tab-click="handleClick" class="el-tabs-item-card" style="width: calc(100% + 40px); margin-left: -20px">
                <el-tab-pane label="城市内涝成因" name="城市内涝成因">
                  <div class="card-body">
                    {{ individualInfo.basicInfo }}
                  </div>
                </el-tab-pane>
                <el-tab-pane label="五大影响因素" name="五大影响因素">
                  <div class="card-body">
                    {{ individualInfo.relatedInfo }}
                  </div>
                </el-tab-pane>
              </el-tabs>
            </el-card>
            <!--     知识库     -->
            <el-card class="card-class" style="width: 100%; height: 500px; margin-top: 1rem" shadow="never">
              <div style="display: flex; width: 100%; flex-direction: column; position: relative; margin-top: -20px;">
                <!--   顶部标签&按钮    -->
                <div class="card-header" style="align-items: center; padding: 0; height: 40px">
                  <el-tabs v-model="showWayActiveName" type="card" @tab-click="showWayTabsChange"
                           class="el-tabs-item-card" style="width: 100%; height: 100%">
                    <el-tab-pane label="知识图谱" name="知识图谱"></el-tab-pane>
                    <el-tab-pane label="法律及国家规范" name="法律及国家规范"></el-tab-pane>
                    <el-tab-pane label="应急预案" name="应急预案"></el-tab-pane>
                  </el-tabs>
  <!--                <el-radio-group v-model="modelRadio" @change="radioChange">-->
  <!--                  <el-radio-button label="知识图谱" class="radio-btn left-radio-btn"/>-->
  <!--                  <el-radio-button label="法律及国家规范" class="radio-btn"/>-->
  <!--                  <el-radio-button label="应急预案" class="radio-btn"/>-->
  <!--                </el-radio-group>-->
                </div>
                <!--   主体内容    -->
                <div style="display: flex; width: 100%" v-loading="cardLoading">
                  <!--     知识图谱     -->
                  <div id="knowledgeMapChart" style="width: 100%; height: 430px" v-if="modelRadio === '知识图谱'">
                    
                  </div>
                  <!-- 法律及国家规范（改为 doc1 的 PDF 陈列） -->
<div style="display: flex; flex-direction: column; width: 100%" v-if="modelRadio === '法律及国家规范'">
  <el-scrollbar max-height="430px" style="width: 100%;">
    <el-card style="background-color: #2D3F4D;" v-for="(pdf, index) in doc1Pdfs" :key="index" class="pdf-card" @click="openPdfDialog(pdf.path)">
      <div style="display: flex; align-items: center;">
        <el-icon style="font-size: 24px; margin-right: 10px; font-family:Arial, Helvetica, sans-serif;"><Document /></el-icon>
        <span style="color: darkgray;">{{ pdf.name }}</span>
      </div>
    </el-card>
  </el-scrollbar>
</div>
<!-- 应急预案（改为 doc2 的 PDF 陈列） -->
<div style="display: flex; flex-direction: column; width: 100%;" v-if="modelRadio === '应急预案'">
  <el-scrollbar max-height="430px" style="width: 100%;">
    <el-card style="background-color: #2D3F4D;" v-for="(pdf, index) in doc2Pdfs" :key="index" class="pdf-card" @click="openPdfDialog(pdf.path)">
      <div style="display: flex; align-items: center;">
        <el-icon style="font-size: 24px; margin-right: 10px;"><Document /></el-icon>
        <span style="color: darkgray;">{{ pdf.name }}</span>
      </div>
    </el-card>
  </el-scrollbar>
</div>

<!-- PDF 预览弹窗 -->
<el-dialog v-model="pdfDialogVisible" title="PDF 预览" width="80%" :before-close="handleClose">
  <iframe :src="selectedPdfPath" style="width: 100%; height: 500px; border: none;"></iframe>
</el-dialog>
                </div>
              </div>
            </el-card>
          </div>
          <!--    右侧个体信息    -->
          <el-card class="card-class" style="width: 38%;" shadow="never">
  <div style="display: flex; flex-direction: column; width: 100%">
    <div style="width: 100%; display: flex; flex-direction: column; align-items: center">
      <img :src="individualInfo.imgUrl" style="height: 150px;" alt="Urban Flooding"/>
      <div style="width: 100%; display: flex; flex-direction: column; margin-top: 1rem">
        <div class="card-header">内涝概况</div>
        <div>
          <el-scrollbar  max-height="470px">
            <el-descriptions style="background-color: darkgray;" class="descriptions-class" :column="1" size="normal" border>
              <el-descriptions-item  label="内涝等级">
                Ⅲ级（中型内涝）
              </el-descriptions-item>
              <el-descriptions-item label="发生区域">
                北京市海淀区成府路与王庄路交叉口
              </el-descriptions-item>
              <el-descriptions-item label="触发雨量">
                72mm/h（3小时累计）
              </el-descriptions-item>
              <el-descriptions-item label="排水系统">
                地下管网排水能力：42m³/s
              </el-descriptions-item>
              <el-descriptions-item label="积水特征">
                最大深度：0.65m │ 影响范围：800m×300m
              </el-descriptions-item>
              <el-descriptions-item label="处置策略">
                优先开放下凹式绿地蓄滞 + 移动泵车强排
              </el-descriptions-item>
              <el-descriptions-item label="响应等级">
                市级防汛Ⅱ级响应
              </el-descriptions-item>
              <el-descriptions-item label="处置时间">
                2025-07-20 14:30~19:45
              </el-descriptions-item>
              <el-descriptions-item label="影响范围">
                封控道路3条 │ 转移商户58家 │ 受困车辆32辆
              </el-descriptions-item>
              <el-descriptions-item label="处置效果">
                积水消退速度：25cm/h │ 交通恢复时间：<6小时
              </el-descriptions-item>
              <el-descriptions-item label="专家评价">
                创新应用AI水位预测模型，泵车部署定位误差<3m
              </el-descriptions-item>
              <el-descriptions-item label="空间坐标">
                116.337°E, 39.992°N
              </el-descriptions-item>
              <el-descriptions-item label="气象溯源">
                台风"杜苏芮"外围云系引发极端强对流天气
              </el-descriptions-item>
            </el-descriptions>
            <!-- 处置效能矩阵 -->
            <div style="margin-top: 1rem;">
              <div style="font-weight: bold; margin-bottom: 0.5rem;">处置效能矩阵</div>
              <el-table :data="efficiencyMatrix" border style="width: 100%;">
                <el-table-column prop="indicator" label="指标" />
                <el-table-column prop="standard" label="标准值" />
                <el-table-column prop="actual" label="实际值" />
                <el-table-column prop="achievement" label="达成率" />
              </el-table>
            </div>
          </el-scrollbar>
        </div>
      </div>
    </div>
  </div>
</el-card>
        </div>
        <!--    环境库     -->
        <div style="display: flex; width: 80%" v-if="false"></div>
        <!--    规则库     -->
        <div style="display: flex; width: 80%" v-if="false"></div>
      </div>
		</el-card>
	
  </div>
</template>
</template>

<script>
import request from "../../utils/request";
import * as echarts from "echarts";
import {ref} from "vue";
import { Document } from "@element-plus/icons-vue"; // 导入 Document 图标
import {Paperclip, Search, UploadFilled} from "@element-plus/icons";

export default {
	name: "PowerGame_knowledgeDisplay",
  components: { Document }, // 注册 Document 图标
  computed: {
    Search() {
      return Search
    }
  },
  components: {Paperclip, UploadFilled},
	setup() {
  const cardLoading = ref(true)
  const modelRadio = ref("知识图谱")
  const pdfDialogVisible = ref(false); // 弹窗可见性
    const selectedPdfPath = ref(""); // 选中的 PDF 路径

    // PDF 文件列表（假设这些是目录下的文件）
    const doc1Pdfs = ref([
      { name: "中华人民共和国防汛条例.pdf", path: "/doc1/中华人民共和国防汛条例.pdf" },
      { name: "中华人民共和国防洪法.pdf", path: "/doc1/中华人民共和国防洪法.pdf" },
      { name: "城市规划编制办法.pdf", path: "/doc1/城市规划编制办法.pdf" },
      { name: "城市黄线管理办法.pdf", path: "/doc1/城市黄线管理办法.pdf" },
      { name: "城市蓝线管理办法.pdf", path: "/doc1/城市蓝线管理办法.pdf" },
      { name: "国务院办公厅关于加强城市.pdf", path: "/doc1/国务院办公厅关于加强城市.pdf" },
      { name: "水利部重大水旱灾害事件调度指挥机制.pdf", path: "/doc1/水利部重大水旱灾害事件调度指挥机制.pdf" },
    ]);
    const doc2Pdfs = ref([
      { name: "天津市防洪调度应急指挥平台建设实践_李匡.pdf", path: "/doc2/天津市防洪调度应急指挥平台建设实践_李匡.pdf" },
      { name: "突发洪涝灾害应急管理框架研...市内涝与山洪的典型案例分析_薛军.pdf", path: "/doc2/突发洪涝灾害应急管理框架研...市内涝与山洪的典型案例分析_薛军.pdf" },
      { name: "京津冀极端降水时空分布特征及其对城市排水压力的影响_崔丹阳.pdf", path: "/doc2/京津冀极端降水时空分布特征及其对城市排水压力的影响_崔丹阳.pdf" },
      { name: "农林部部长沙风在抗击河南驻马店“75·8”水灾中_李金明.pdf", path: "/doc2/农林部部长沙风在抗击河南驻马店“75·8”水灾中_李金明.pdf" },
      { name: "平急两用内涝防治设施规划探索_刘江涛.pdf", path: "/doc2/平急两用内涝防治设施规划探索_刘江涛.pdf" },
      { name: "让城市告别“看海”现象.pdf", path: "/doc2/让城市告别“看海”现象.pdf" },
      { name: "韧性城市视角下城市内涝防治...州“5·22”特大暴雨为例_尹来盛.pdf", path: "/doc2/韧性城市视角下城市内涝防治...州“5·22”特大暴雨为例_尹来盛.pdf" },
      { name: "石家庄市城市水系智慧管控平台构建与应用_韦艳红.pdf", path: "/doc2/石家庄市城市水系智慧管控平台构建与应用_韦艳红.pdf" },
    ]);
  const sliderValue = ref([1959, 1962])
  const marks = ({
    1959: '1959',
    1960: '1960',
    1961: '1961',
    1970: '1970',
  })
  const showWayRadio = ref('1')
  const individualSelection = ref()
  const baseActiveName = ref('0')
  const activeName = ref('城市内涝成因')
  const showWayActiveName = ref('知识图谱')
  const efficiencyMatrix = ref([
    { indicator: '响应时间', standard: '30min', actual: '22min', achievement: '135%' },
    { indicator: '排水效率', standard: '20cm/h', actual: '25cm/h', achievement: '125%' },
    { indicator: '人员疏散', standard: '4小时', actual: '3.2小时', achievement: '120%' },
  ])
  return {
    cardLoading, modelRadio, sliderValue, marks, showWayRadio,
    individualSelection, baseActiveName, activeName, showWayActiveName,
    efficiencyMatrix, doc1Pdfs, doc2Pdfs, pdfDialogVisible, selectedPdfPath,
  }
},
	data(){
		return{
			knowledgeMapChart: null,
			knowledgeMapOption: null,
			knowledgeMapData: [],
			knowledgeMapLinks: [],
      originalData: [
        [
          {head: "1959年古巴革命胜利", tail: "费德尔·卡斯特罗", content: "领导革命", timestamp: "1959-01-01"},
          {head: "费德尔·卡斯特罗", tail: "古巴共和国", content: "建立社会主义政权", timestamp: "1959-01-01"}
        ],
        [
          {head: "美国", tail: "古巴共和国", content: "断交并实施经济制裁", timestamp: "1961-01-03"},
          {head: "美国", tail: "古巴共和国", content: "猪湾入侵失败", timestamp: "1961-04-17"}
        ],
        [
          {head: "赫鲁晓夫", tail: "费德尔·卡斯特罗", content: "秘密协议部署导弹", timestamp: "1962-07"},
          {head: "苏联", tail: "古巴", content: "运送中程导弹和军事人员", timestamp: "1962-07-01"},
          {head: "美国中央情报局", tail: "苏联在古巴的导弹基地", content: "通过U-2侦察机发现", timestamp: "1962-10-14"},
          {head: "约翰·F·肯尼迪", tail: "美国", content: "宣布对古巴实施海上隔离", timestamp: "1962-10-22"},
          {head: "美洲国家组织", tail: "美国", content: "支持对古巴的隔离行动", timestamp: "1962-10-23"},
          {head: "赫鲁晓夫", tail: "约翰·F·肯尼迪", content: "提出撤除导弹的条件", timestamp: "1962-10-26"},
          {head: "苏联", tail: "古巴", content: "宣布撤除导弹", timestamp: "1962-10-28"},
          {head: "美国", tail: "土耳其", content: "同意撤除朱庇特导弹", timestamp: "1962-10-28"},
          {head: "苏联", tail: "古巴", content: "导弹撤离完成", timestamp: "1962-11-20"},
          {head: "美国", tail: "古巴", content: "结束对古巴的海上封锁", timestamp: "1962-11-20"}
        ]
      ],
      data: [
        [
          {timestamp: '1900/4/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1900/4/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1900/4/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
        ],
        [
          {timestamp: '1917/4/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1917/5/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1917/6/30', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
        ],
        [
          {timestamp: '1935/2/01', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1935/6/21', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1935/12/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
        ],
        [
          {timestamp: '1935/2/01', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1935/6/21', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1935/12/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
        ],
        [
          {timestamp: '1935/2/01', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1935/6/21', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
          {timestamp: '1935/12/12', head: 'aaaa', tail: 'bbbb', content: 'ccccc'},
        ],
      ],

      imgUrl: [
        require('../../assets/images/flags/flag-America.png'),
        require('../../assets/images/flags/flag-Russia.png'),
        require('../../assets/images/flags/flag-Cuba.png'),
      ],
      sequenceChart: null,
      sequenceOption: {},
      sequenceData: [],
      dataImportDialog: false,
      individualOption: [
        {label: '肯尼迪', value: 0},
        {label: '约翰·C·阿奎里诺', value: 1},
        {label: '赫鲁晓夫', value: 2},
        {label: '骑手张三', value: 3},
      ],

      itemCardSelection: 0,
      itemCard: [
        {title: '古巴导弹危机', subtitle: '知识库'},
        {title: '智慧城市', subtitle: '知识库'},
        {title: '俄乌战争', subtitle: '知识库'},
        {title: '美朝H博弈', subtitle: '知识库'},
        {title: '城市内涝', subtitle: '知识库'},
      ],

      individualInfo: {
        name: '内涝',
        basicInfo: '城市内涝的主要成因包括以下几点：1. 短时强降雨：当降雨强度超过城市排水系统承载能力（通常指1小时降雨量>50mm），地表径流快速积聚形成积水；2. 地形制约：低洼地区（如河道周边、地下通道）易形成雨水汇集，地面坡度<0.3%的区域排水效率下降40%以上；3. 排水能力不足：老旧管网设计标准低（通常仅能应对1-3年一遇降雨），管径偏小、淤塞率>30%时会大幅降低过流能力；4. 地表渗透减少：混凝土覆盖率>70%的区域，雨水渗透率下降90%，径流系数从0.3增至0.9，汇流速度加快2-3倍。',
        relatedInfo: '城市内涝的五大影响因素包括：1. 降雨特征：强度、时长和时空分布对内涝影响权重达90%；2. 地形地貌：高程（如低洼区）、坡度和水系分布，影响权重约75%；3. 排水系统：管网密度、泵站能力和管径匹配度，影响权重85%；4. 城市规划：绿地率（<30%为高风险）、透水铺装和蓄滞空间，影响权重65%；5. 应急管理：预警响应速度和排涝设备调度效率，影响权重55%。',
        imgUrl: require('../../assets/images/内涝.jpg') // 替换为实际内涝图片路径
      },

      agentIconImg: [
          require('../../assets/images/cubaAgentIcons/古巴导弹危机.jpg'),
          require('../../assets/images/cubaAgentIcons/美国.jpg'),
          require('../../assets/images/cubaAgentIcons/苏联.jpg'),
          require('../../assets/images/cubaAgentIcons/古巴.jpg'),
          require('../../assets/images/cubaAgentIcons/约翰・肯尼迪.jpg'),
          require('../../assets/images/cubaAgentIcons/尼基塔・赫鲁晓夫.jpg'),
          require('../../assets/images/cubaAgentIcons/菲德尔·亚历杭德罗·卡斯特罗·鲁斯.jpg'),
          require('../../assets/images/cubaAgentIcons/冷战.jpg'),
          require('../../assets/images/cubaAgentIcons/猪湾事件.jpg'),
          require('../../assets/images/cubaAgentIcons/美苏核军备竞赛.jpg'),
          require('../../assets/images/cubaAgentIcons/苏联导弹部署战略.jpg'),
          require('../../assets/images/cubaAgentIcons/联合国.jpg'),
          require('../../assets/images/cubaAgentIcons/导弹发现.jpg'),
          require('../../assets/images/cubaAgentIcons/美军封锁.jpg'),
          require('../../assets/images/cubaAgentIcons/苏联撤导弹.jpg'),
          require('../../assets/images/cubaAgentIcons/协议达成.jpg'),
      ]
		}
	},
	mounted(){
		this.initKnowledgeMap();
    this.sliderChange([1959, 1962])
	},
	methods:{
    openPdfDialog(pdfPath) {
      this.selectedPdfPath = pdfPath;
      this.pdfDialogVisible = true;
    },
    handleClose(done) {
      this.selectedPdfPath = "";
      done();
    },
    radioChange(){
      if(this.modelRadio === '知识图谱')
        this.initKnowledgeMap();
      else if(this.modelRadio === '法律及国家规范'){
        this.cardLoading = false;
      }
      else if(this.modelRadio === '应急预案'){
        this.initSequenceChart();
        this.cardLoading = false;
      }
    },
    showWayTabsChange(tab){
      this.modelRadio = tab.paneName;
      if(this.modelRadio === '知识图谱')
        this.initKnowledgeMap();
      else if(this.modelRadio === '法律及国家规范'){
        this.cardLoading = false;
      }
      else if(this.modelRadio === '应急预案'){
        this.initSequenceChart();
        this.cardLoading = false;
      }
    },
    itemCardClick(value){
      this.itemCardSelection = value
      console.log('click card, value：', value)
      request.post('/getKnowledgeNodeName', {
        baseName: value
      }).then((res) => {
        console.log('card click', res)
        this.individualOption = []
        for(let i = 0; i < res.data.length; i++)
          this.individualOption.push({label: res.data[i], value: i})
      })
    },
		async initKnowledgeMap(){
			this.cardLoading = true;
			await request.get('/getKnowledge').then(res => {
				this.cardLoading = false;
				console.log('ressss', res)
				this.knowledgeMapData = res.data.data
				this.knowledgeMapLinks = res.data.link
			})
			this.initChart()
		},
		initChart(){
			this.$nextTick(() => {
				this.knowledgeMapChart = echarts.init(document.getElementById('knowledgeMapChart'));
        this.knowledgeMapChart.resize();
				this.knowledgeMapOption = {
					tooltip: {},
					series: [{
						type: 'graph',
						layout: 'force',
						force: {
							repulsion: 150,
							edgeLength: 100
						},
						draggable: true,
						symbolSize: 30,
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
						data: this.knowledgeMapData,
						links: this.knowledgeMapLinks,
						lineStyle: {
							opacity: 0.9,
							width: 2,
							curveness: 0,
						},
					}],
					animationDurationUpdate: 1500,
					// animationEasingUpdate: 'quinticInOut',
				}
				this.knowledgeMapChart.setOption(this.knowledgeMapOption);
			})
		},
    sliderChange(value){
      console.log('slider', value);
      this.data = []
      for(let i = 0; i < this.originalData.length; i++){
        let year = this.originalData[i][0].timestamp.slice(0, 4)
        if(value[0] <= year && year <= value[1])
          this.data.push(this.originalData[i])
      }
      this.$nextTick(() =>{
        this.$refs.rowBarRef.update();
      })
    },
    getSequenceData(){
      let eventNum = 10;
      let rightPos = 1500;
      let heightPos = 800;
      let midPos = 0;
      let singleHeight = heightPos / (eventNum + 1)
      this.sequenceData = [
        {name: 'A1', x: 0, y: 0, symbol: 'image://' + this.imgUrl[0], symbolSize: [45, 30], label: {show: false}},
        {name: 'A2', x: 0, y: heightPos, symbol: 'none'},
        {name: 'S1', x: rightPos / 2, y: midPos, symbol: 'image://' + this.imgUrl[1], symbolSize: [45, 30], label: {show: false}},
        {name: 'S2', x: rightPos / 2, y: midPos + heightPos, symbol: 'none'},
        {name: 'G1', x: rightPos, y: 0, symbol: 'image://' + this.imgUrl[2], symbolSize: [45, 30], label: {show: false}},
        {name: 'G2', x: rightPos, y: heightPos, symbol: 'none'},
        // 古巴革命胜利
        {
          name: '1959-01-01', x: rightPos, y: singleHeight,
          info: '古巴革命胜利，建立古巴共和国',
          label: {
            show: true,
            position: 'left',
          }
        },
        // 美国与古巴断交并实施经济制裁
        {
          name: '1961-01-03', x: 0, y: singleHeight * 2,
          label: {
            show: true,
            position: 'left',
          }
        },
        {
          name: '1961-01-03-1', x: rightPos, y: singleHeight * 2,
          label: {
            show: false,
            position: 'left',
          }
        },
        // 猪湾入侵 失败
        {
          name: '1961-04-17', x: 0, y: singleHeight * 3,
          label: {
            show: true,
            position: 'left',
          }
        },
        {
          name: '1961-04-17-1', x: rightPos, y: singleHeight * 3,
          label: {
            show: false,
            position: 'left',
          }
        },
        // 苏联在古巴部署导弹
        {
          name: '1962-07-17', x: rightPos / 2, y: midPos + singleHeight * 4,
          info: '赫鲁晓夫',
          label: {
            show: true,
            position: 'left',
          }
        },
        {
          name: '1962-07-17-1', x: rightPos, y: singleHeight * 4,
          info: '费德尔·卡斯特罗',
          label: {
            show: false,
            position: 'left',
          }
        },
        // 美国发现导弹
        {
          name: '1962-10-14', x: 0, y: singleHeight * 5,
          info: '中央情报局发现导弹基地',
          label: {
            show: true,
            position: 'left',
          }
        },
        // 美国对古巴实施海上隔离
        {
          name: '1962-10-22', x: 0, y: singleHeight * 6,
          info: '约翰·F·肯尼迪',
          label: {
            show: true,
            position: 'left',
          }
        },
        {
          name: '1962-10-22-1', x: rightPos, y: singleHeight * 6,
          label: {
            show: false,
            position: 'left',
          }
        },
        // 苏联提出撤除导弹的条件
        {
          name: '1962-10-26', x: rightPos / 2, y: midPos + singleHeight * 7,
          info: '赫鲁晓夫',
          label: {
            show: true,
            position: 'left',
          }
        },
        {
          name: '1962-10-26-1', x: 0, y: singleHeight * 7,
          info: '约翰·F·肯尼迪',
          label: {
            show: false,
            position: 'left',
          }
        },
        // 苏联 → 古巴 宣布撤除导弹
        {
          name: '1962-10-28', x: rightPos / 2, y: midPos + singleHeight * 8,
          info: '苏联',
          label: {
            show: true,
            position: 'left',
          }
        },
        {
          name: '1962-10-28-1', x: rightPos, y: singleHeight * 8,
          info: '古巴',
          label: {
            show: false,
            position: 'left',
          }
        },
        // 导弹撤离完成
        {
          name: '1962-11-19', x: rightPos, y: singleHeight * 9,
          info: '导弹撤离完成',
          label: {
            show: true,
            position: 'left',
          }
        },
        // 美国结束对古巴的海上封锁
        {
          name: '1962-11-20', x: 0, y: singleHeight * 10,
          info: '美国',
          label: {
            show: true,
            position: 'left',
          }
        },
        {
          name: '1962-11-20-1', x: rightPos, y: singleHeight * 10,
          info: '古巴',
          label: {
            show: false,
            position: 'left',
          }
        },
      ]
      this.sequenceLink = [
        {source: 'A1', target: 'A2', symbol: ['none', 'none'], lineStyle: {width: 5} },
        {source: 'S1', target: 'S2', symbol: ['none', 'none'], lineStyle: {width: 5} },
        {source: 'G1', target: 'G2', symbol: ['none', 'none'], lineStyle: {width: 5} },
        {
          source: '1961-01-03', target: '1961-01-03-1',
          symbol: ['none', 'arrow'],
          lineStyle: {
            type: 'solid'
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '断交并实施经济制裁',
          }
        },
        {
          source: '1961-04-17', target: '1961-04-17-1',
          symbol: ['none', 'arrow'],
          lineStyle: {
            type: 'solid'
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '猪湾入侵失败',
          }
        },
        {
          source: '1962-07-17', target: '1962-07-17-1',
          symbol: ['none', 'arrow'],
          lineStyle: {
            type: 'dotted'
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '秘密协议部署导弹',
          }
        },
        {
          source: '1962-10-22', target: '1962-10-22-1',
          symbol: ['none', 'arrow'],
          lineStyle: {
            type: 'solid'
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '宣布对古巴实施海上隔离',
          }
        },
        {
          source: '1962-10-26', target: '1962-10-26-1',
          symbol: ['none', 'arrow'],
          lineStyle: {
            type: 'dotted'
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '提出撤除导弹条件',
          }
        },
        {
          source: '1962-10-28', target: '1962-10-28-1',
          symbol: ['none', 'arrow'],
          lineStyle: {
            type: 'dotted'
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '宣布撤除导弹',
          }
        },
        {
          source: '1962-11-20', target: '1962-11-20-1',
          symbol: ['none', 'arrow'],
          lineStyle: {
            type: 'solid'
          },
          label: {
            show: true,
            fontSize: 14,
            formatter: '结束对古巴的海上封锁',
          }
        },
      ]
    },
    initSequenceChart(){
      this.$nextTick(() => {
        this.getSequenceData();
        this.sequenceChart = echarts.init(document.getElementById('sequenceChart'));
        this.sequenceChart.resize();
        this.sequenceOption = {
          tooltip: {},
          animationDurationUpdate: 1500,
          animationEasingUpdate: 'quinticInOut',
          series: [
            {
              type: 'graph',
              layout: 'none',
              tooltip: {//提示框
                show: true,
                trigger: 'item',
                triggerOn: 'mousemove',
                enterable: true,
                formatter: this.formatterHover,
              },
              symbolSize: 10,
              roam: true,
              label: {show: false},
              edgeSymbol: ['circle', 'arrow'],
              edgeSymbolSize: [4, 10],
              edgeLabel: {fontSize: 20},
              data: this.sequenceData,
              links: this.sequenceLink,
              lineStyle: {
                opacity: 0.9,
                width: 2,
                curveness: 0
              }
            }
          ]
        }
        this.sequenceChart.setOption(this.sequenceOption);
      })
    },
    dataImport(){
      this.dataImportDialog = !this.dataImportDialog;
    },
    async checkIndividualData(){
      this.cardLoading = true;
      await request.post('/getCubaKnowledge', {
        type: this.showWayRadio,
        baseName: this.itemCardSelection,
        nodeName: this.individualOption[this.individualSelection].label,
      }).then(res => {
        console.log(res)
        this.cardLoading = false;
        this.individualInfo = {
          name: res.data.name,
          basicInfo: res.data.background,
          relatedInfo: '',
          imgUrl: this.agentIconImg[parseInt(res.data.id) - 1]
        }
        this.descriptionItemLabel = res.data.attributes;
        this.knowledgeMapData = res.base_data
        this.knowledgeMapLinks = res.links

        this.knowledgeMapOption.series[0].symbolSize = 50;
        this.knowledgeMapOption.series[0].label.fontSize = 14;
        this.knowledgeMapOption.series[0].force = {
          repulsion: 150,
          edgeLength: 150
        };
        this.knowledgeMapOption.series[0].data = this.knowledgeMapData;
        this.knowledgeMapOption.series[0].links = this.knowledgeMapLinks;
        this.knowledgeMapChart.setOption(this.knowledgeMapOption);
      })
    }
	}
}
</script>

<style scoped>
.pdf-card {
  margin: 10px;
  cursor: pointer;
  transition: all 0.3s;
}

.pdf-card:hover {
  background-color: #f5f5f5;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.el-dialog__body {
  padding: 0;
}
.card-class{
  background-color: #25313D;
  width: 50%;
  border: 0;
}
.click-item-card{
  width: 100%;
  margin: 5px 0;
  border: 0;
  cursor: pointer;
}
.click-item-card-unselected{
  background-color: #2D3F4D;
}
.click-item-card-selected{
  background-color: #577a95;
}
.click-item-card-content{
  color: #fff;
  font-size: 14px;
  display: flex;
  flex-direction: column;
  font-family: "Microsoft YaHei", serif;
}
.card-header{
  width: calc(100% + 40px);
  margin-left: -20px;
  height: 50px;
  display: flex;
  align-items: center;
  color: #FFF;
  font-size: 16px;
  font-weight: bold;
  padding: 10px;
  background-color: #2d3f4d;
}
.card-body{
  font-family: "Microsoft YaHei", serif;
  font-size: 16px;
  font-weight: bold;
  padding: 0 20px;
  color: #FFF;
}
.cell-item{
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100px;
}
:deep(.descriptions-class .el-descriptions__body){
  background-color: transparent;
  color: #FFF;
  width: 100%;
  --el-descriptions-table-border: 0;
}
:deep(.label-class){
  background: rgba(0, 0, 0, 0) !important;
}
:deep(.content-class){
  background: transparent;
}
.radio-btn{
  --el-radio-button-checked-background-color: #577a95;
  --el-radio-button-checked-border-color: #577a95;
  --el-radio-button-checked-font-color: #fff;
}
:deep(.select-class.el-select){
  --el-select-border-color-hover: #598cb5 !important;
  --el-select-input-focus-border-color: #559ad1 !important;
}
:deep(.input-class .el-input){
  --el-input-background-color: transparent;
  --el-input-border-color: #375575;
  --el-input-font-color: #fff;
  --el-input-border: 1px solid #577a95;
}
:deep(.el-radio-button__inner){
  padding: 10px 20px;
  color: #fff;
  background-color: #25313D;
  border: 1px solid #375575;
}
:deep(.left-radio-btn .el-radio-button__inner){
  border-left: 1px solid #375575;
}
:deep(.el-tabs__active-bar){
  background-color: #577a95;
}

:deep(.el-tabs__item){
  color: #b8b3b3;
}
:deep(.el-tabs__item.is-active){
  color: #FFF;
}
:deep(.el-tabs-item-card .el-tabs__item.is-active){
  color: #FFF;
  background-color: #577a95;
  border-bottom: 2px solid #0056b6;
}
:deep(.el-tabs-item-card .el-tabs__item){
  border-left: 0;
}
:deep(.query-btn.el-button){
  --el-button-background-color: #18395c;
  --el-button-border-color: #092d57;
  --el-button-hover-color: #0b498e;
  --el-button-active-background-color: #226bba;
}
:deep(.el-tabs--card>.el-tabs__header .el-tabs__nav){
  border: 0;
}
:deep(.narrow-tab .el-tabs__item){
  padding: 0 10px;
}
</style>