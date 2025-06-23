<template>
  <div style="width: 99%; min-width:1200px; display: flex">
    <div style="width: 99%; min-width: 1200px; display: inline;">
      <el-card style="width: 100%; height: 98%; display: flex; flex-direction: column;">
        <div>
          <el-card style="width: 96%; margin-left: 2%; margin-bottom: 1rem; font-size: 16px">
            <p>说明：默认情况下本系统中降雨强度基于<b>气象模型</b>生成。</p>
            <p>积水管理分为三个策略级别：低强度（小雨）、中强度（中雨）、高强度（暴雨）。低强度降雨积水少且对道路的影响小。</p>
            <p>每个区域的积水深度有详细数值（0~100cm），Agent反应速度决定了在降水超过警戒值多久后开始制定与执行计划。</p>
          </el-card>
        </div>
        <div style="display: flex; width: 100%; flex-grow: 1;">
          <!-- 左侧包含选择框和地图 -->
          <div style="width: 45%; margin: 0 2%; display: flex; flex-direction: column; align-items: center;">
            <!-- 选择框 -->
            <div style="width: 600px; margin: 3rem auto 0; text-align: center;">
              <el-form :model="form" ref="form" label-width="120px" :rules="rules" style="max-width: 600px;">
                <el-space fill>
                  <el-alert type="warning" show-icon :closable="false" style="width: 300px; margin-left: 120px">
                    <span v-if="form.runModel === 0"><b>正常模式下</b>降雨仅在运行周期内发生，积水处理完成后停止。</span>
                    <span v-else-if="form.runModel === 1"><b>半无限模式下</b>降雨持续生成，运行指定周期后停止。</span>
                    <span v-else-if="form.runModel === 2"><b>无限运行模式下</b>降雨无限制生成，需手动停止。</span>
                    <span v-else-if="form.runModel === 3"><b>对照实验模式下</b>降雨在周期内生成，包含对照组实验。</span>
                    <span v-else><b>运行模式</b>与降雨持续时间和积水处理时长有关。</span>
                  </el-alert>
                  <el-form-item label="运行模式" prop="runModel" required style="display: flex">
                    <el-select v-model="form.runModel" style="width: 300px" @change="runModelChange()">
                      <el-option
                        v-for="item in runModelOptions"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-space>
                <el-form-item label="降雨模式" prop="rainMode" required>
                  <el-select v-model="form.rainMode" style="width: 300px">
                    <el-option
                      v-for="item in rainModeOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="Agent反应速度" prop="floodDistribute">
                  <el-select v-model="form.floodDistribute" style="width: 300px">
                    <el-option
                      v-for="item in distributeOptions"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="降雨强度" prop="rainIntensity" v-if="form.floodDistribute === 1">
                  <el-input-number v-model="form.rainIntensity" style="width: 300px" :min="1" :max="3"/>
                </el-form-item>
                <el-space fill></el-space>
                <el-form-item label="持续时长" prop="T" v-if="form.runModel !== 2">
                  <el-input-number v-model="form.T" style="width: 300px" :min="10" :max="300"/>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" style="margin-left: 22%" @click="submitForm(form)">提交</el-button>
                </el-form-item>
              </el-form>
            </div>
            <!-- 模拟地点 -->
            <el-card class="bg-card" style="margin-top: 2rem; background-color: rgb(77, 100, 101); width: 100%;">
              <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative">
                <div class="card-title" style="color: #FFF">模拟地点</div>
                <div class="card-content-font card-content-size" style="color: #FFF">
                  <div id="mapContainer"></div>
                </div>
              </div>
            </el-card>
          </div>
          <!-- 右侧模拟环境 -->
          <div style="width: 45%; margin: 0 2%;">
            <el-card class="bg-card" style="background-color: rgb(208, 202, 254); width: 100%; height: 100%;">
              <div style="display: flex; flex-direction: column; height: 100%;">
                <div class="card-title" style="color: rgb(28, 60, 58); padding-top: 10px;">模拟环境</div>
                <div class="card-content-font" style="display: flex; align-items: center; justify-content: center; flex-grow: 1; padding: 20px; text-align: center;">
                  {{bgContent}}
                </div>
              </div>
            </el-card>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import {loadBaiDuMap} from "../../utils/loadBaidumap.js"
import {ElMessageBox, ElMessage} from "element-plus";
import {ref} from "vue";
import request from "../../utils/request.js";

export default {
  name: "UrbanFlooding_EnvironmentDesign",
  setup() {
    const runModelOptions = [
      { value: 0, label: "正常模式" },
      { value: 1, label: "调试模式" },
      { value: 2, label: "反馈模式" },
    ];
    const rainModeOptions = [
      { value: 0, label: "实际数据" },
      { value: 1, label: "均匀降雨" },
    ];
    const distributeOptions = [
      { value: 2, label: "普通状态" },
      { value: 0, label: "快速反应" },
      { value: 1, label: "紧急响应" },
    ];
    return {
      runModelOptions,
      rainModeOptions,
      distributeOptions,
    }
  },
  data(){
    return{
      map: null,
      mapdata: {
        center: {lat: 39., lng: 117.13},
        zoom: 1,
        show: true,
        dragging: true
      },
      bgContent: '模拟环境由一个动态的城市模型驱动，包括道路、公交、天气等核心要素。降雨开始后，环境会根据降雨强度模拟不同区域的积水情况，影响道路通行能力，并导致部分交通流量受阻。交通管制、公交调度和信息发布等执行Agent会在政策Agent的指令下采取行动，例如封闭道路、设置应急通道、优化公交线路，或向市民发布预警信息。这些调整会实时改变环境状态，并影响群众的出行选择。为了评估政策Agent的决策是否合理，系统会持续监测多个关键指标，包括公交线路的拥堵情况、公交准点率等。如果政策Agent的决策能够有效减少拥堵，提高公交通行率则说明它的策略是有效的；相反，如果环境反馈显示某些区域因决策不当出现更严重的拥堵、公共交通瘫痪则说明策略需要调整。每轮决策后，环境会根据新的状态给出反馈，政策Agent再基于反馈调整策略，形成动态优化机制',
      form: {
        runModel: 0,
        rainIntensity: 2,
        rainMode: 0,
        rainRate: 20,
        floodDistribute: 1,
        T: 60,
      },
      rules: {
        rainIntensity: [{ required: true, message: "请选择降雨强度", trigger: "blur" }],
        floodDistribute: [{ required: true, message: "请选择积水分布", trigger: "blur" }],
        rainRate: [
          { required: true, message: "请输入降雨率", trigger: "blur" },
          {
            validator: function (rule, value, callback) {
              if (value !== "") {
                let reg = /^(0\.[5-9]|[1-9]\d?(\.\d+)?|100(\.0+)?)$/;
                if (!reg.test(value)) callback(new Error("请输入0.5~100之间的数值"));
                else callback();
              }
            },
            trigger: "blur",
          },
        ],
        T: [{ required: true, message: "请输入周期时长", trigger: "blur" }],
      },
    }
  },
  mounted(){
    this.initMap();
  },
  methods:{
    initMap(){
      loadBaiDuMap().then((BMapGL) => {
        let map = new BMapGL.Map("mapContainer", {enableMapClick: false});
        this.map = map
        this.map.addControl(
          new BMapGL.ScaleControl({
            anchor: BMAP_ANCHOR_BOTTOM_LEFT,
            offset: new BMapGL.Size(20, -10),
          })
        );
        this.map.setMinZoom(10)
        this.map.setMaxZoom(10)
        this.map.addControl(
          new BMapGL.ZoomControl({
            anchor: BMAP_ANCHOR_BOTTOM_RIGHT,
            offset: new BMapGL.Size(10, 10),
          })
        )
        this.map.disableDoubleClickZoom()
        const point = new BMapGL.Point(this.mapdata.center.lng, this.mapdata.center.lat)
        map.centerAndZoom(point, 12)
        map.enableScrollWheelZoom(true)
      }).catch((err) => {
        console.log(err)
      })
    },
    cardContentChange(label){
      ElMessageBox({
        title: '内容修改',
        showInput: true,
        inputType: 'textarea',
        inputValue: this.bgContent,
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
      }).then(({value}) =>{
        this.bgContent = value
      })
    },
    submitForm(form) {
      this.$refs.form.validate((valid) => {
        if (valid) {
          request
            .post("/envDesign", {
              rain_intensity: form.rainIntensity,
              rain_mode: Number(form.rainMode),
              rain_rate: Number(form.rainRate),
              flood_distribute: form.floodDistribute,
              run_model: form.runModel,
              T: Number(form.T),
            })
            .then((res) => {
              console.log(res);
              ElMessage({
                message: res.data,
                type: res.type,
              });
            });
        } else {
          ElMessage({
            message: "请确保填写的信息正确",
            type: "error",
          });
        }
      });
    },
    runModelChange() {
      console.log(this.form.runModel);
      if (this.form.runModel === 2) this.form.T = 9999;
      else if (this.form.runModel === 3) {
        this.form.T = 60;
        this.form.rainIntensity = 2;
        this.form.floodDistribute = 0;
      } else this.form.T = 60;
    },
  }
}
</script>

<style scoped>
.bg-card {
  width: 100%;
  border-radius: 20px;
}

.card-title {
  display: flex;
  width: 100%;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-family: 微软雅黑, serif;
  font-weight: bold;
  margin-bottom: 8px;
  color: #000;
}

.card-content-size {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 22vh;
  padding: 5px;
}

.card-content-font {
  font-size: 16px;
  font-family: 'Microsoft YaHei', serif;
  line-height: 1.7;
  font-weight: lighter;
}

#mapContainer {
  width: 100%;
  height: 300px;
  border-radius: 10px;
}

.el-card {
  border: 1px solid #e6f7ff;
}

.el-button--primary {
  background-color: #1890ff;
  border-color: #1890ff;
}

/* 确保选择框居中 */
.el-form {
  width: 100%;
  text-align: left; /* 表单内部保持左对齐 */
}

/* 可选：调整选择框宽度 */
.el-select, .el-input-number {
  width: 100%; /* 让选择框和输入框占满容器宽度 */
}
</style>