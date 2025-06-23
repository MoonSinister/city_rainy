<template>
  <div style="width: 99%; min-width:1200px; display: flex">
    <div style="width: 99%; min-width: 1200px; display: inline; position: relative">
      <el-card ref="contentCard" style="width: 100%; height: auto; min-height: 400px;"
               v-loading="loadingAnimation" element-loading-text="正在返回实验设计界面，请稍后...">
        <!-- 头部返回组件 -->
        <div style="width: 100%; display: flex">
          <el-page-header @back="goBack()">
            <template #content>
              <el-breadcrumb separator="/">
                <el-breadcrumb-item :to="{ path: '/home/rainCity/thirddesign' }">
                  响应变量设计
                </el-breadcrumb-item>
              </el-breadcrumb>
            </template>
          </el-page-header>
        </div>
        <!-- 响应变量整体选择区 -->
        <div style="width: 100%; margin-top: 2rem">
          <el-card class="cardStyle" shadow="hover" style="width: 100%; margin-bottom: 2%">
            <template #header>
              <div class="card-header">
                <span>响应变量整体选择</span>
              </div>
            </template>
            <div class="line-style" style="display: flex; flex-wrap: wrap; gap: 2%; justify-content: center;">
              <div v-for="(variable, idx) in responseVarOptions" :key="variable.value" style="width: 32%; min-width: 260px; margin-bottom: 1.5rem;">
                <div style="font-weight: bold; font-size: 16px; margin-bottom: 8px;">{{ variable.label }}</div>
                <el-cascader v-model="responseVarMethods[idx]"
                             :options="variable.children"
                             :props="props"
                             :placeholder="'请选择' + variable.label"
                             @change="onCascaderChange(idx)"
                             style="width: 90%; margin-bottom: 8px;"/>
                <div style="color: #888; font-size: 13px; min-height: 24px;">
                  <span v-if="responseVarMethodsLabel[idx].length">已选：{{ responseVarMethodsLabel[idx].join(' / ') }}</span>
                  <span v-else>请在上方选择具体的{{ variable.label }}</span>
                </div>
              </div>
            </div>
            <div style="width: 100%; display: flex; justify-content: flex-end;">
              <el-button type="success" @click="editCompleted">编辑完成</el-button>
            </div>
          </el-card>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script>
import {ref} from "vue";
import {ElMessage} from "element-plus";

export default {
  name: "PowerGame_ResponseVarDesign",
  setup() {
    const cardMaxHeight = ref(100)
    const props = {
      expandTrigger: 'hover'
    }
    const loadingAnimation = ref(false)
    return {
      cardMaxHeight, props, loadingAnimation
    }
  },
  data() {
    return {
      responseVarOptions: [
        {
          value: 1, label: '个体效能', children: [
            { value: 1, label: '出行时间' },
            { value: 2, label: '出行成本' },
            { value: 3, label: '满意度' },
            { value: 4, label: '其他' },
          ]
        },
        {
          value: 2, label: '系统效能', children: [
            { value: 1, label: '整体通行效率' },
            { value: 2, label: '拥堵指数' },
            { value: 3, label: '事故率' },
            { value: 4, label: '其他' },
          ]
        },
        {
          value: 3, label: '价值熵', children: [
            { value: 1, label: '公平性' },
            { value: 2, label: '多样性' },
            { value: 3, label: '不确定性' },
            { value: 4, label: '其他' },
          ]
        }
      ],
      responseVarMethods: [[], [], []], // 三个响应变量的选择
      responseVarMethodsLabel: [[], [], []], // 三个响应变量的label路径
    }
  },
  mounted() {
    let cardHeight = this.$refs.contentCard?.$el.offsetHeight || 600;
    this.cardMaxHeight = cardHeight - 64;
    // 恢复本地存储
    const detailStr = localStorage.getItem('responseVarsDetail');
    if (detailStr) {
      try {
        const details = JSON.parse(detailStr);
        for (let i = 0; i < 3; i++) {
          if (details[i]) {
            this.responseVarMethods[i] = details[i].var_content_index || [];
            this.responseVarMethodsLabel[i] = details[i].var_content_name || [];
          }
        }
      } catch (e) {}
    }
  },
  methods: {
    goBack() {
      this.$router.push('/home/rainCity/expDesign');
    },
    onCascaderChange(idx) {
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
      this.responseVarMethodsLabel[idx] = getLabelPath(this.responseVarOptions[idx].children, this.responseVarMethods[idx]);
    },
    editCompleted() {
      this.loadingAnimation = true;
      // 合并所有选择，结构与主界面展示一致
      let details = [];
      for (let i = 0; i < 3; i++) {
        details.push({
          var_index: i + 1,
          var_name: this.responseVarOptions[i].label,
          var_content_index: this.responseVarMethods[i],
          var_content_name: this.responseVarMethodsLabel[i],
        });
      }
      localStorage.setItem('responseVarsDetail', JSON.stringify(details));
      this.loadingAnimation = false;
      this.$router.push('/home/rainCity/expDesign');
    },
  },
}
</script>

<style scoped>
.cardStyle {
  width: 98%;
  margin: 0 2% 1rem 0;
  /* height: 18vh; */
  min-height: 120px;
}

.card-header {
  font-size: 18px;
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.line-style {
  font-size: 16px;
  line-height: 25px;
}
</style>
