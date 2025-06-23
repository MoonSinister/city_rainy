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
                <el-breadcrumb-item :to="{ path: '/home/rainCity/seconddesign' }">
                  影响因素设计
                </el-breadcrumb-item>
              </el-breadcrumb>
            </template>
          </el-page-header>
        </div>
        <!-- 合并后的整体选择区 -->
        <div style="width: 100%; margin-top: 2rem">
          <el-card class="cardStyle" shadow="hover" style="width: 100%; margin-bottom: 2%">
            <template #header>
              <div class="card-header">
                <span>影响因素整体选择</span>
              </div>
            </template>
            <div class="line-style" style="display: flex; flex-wrap: wrap; gap: 2%; justify-content: center;">
              <div v-for="(factor, idx) in factorOptions" :key="factor.value" style="width: 32%; min-width: 260px; margin-bottom: 1.5rem;">
                <div style="font-weight: bold; font-size: 16px; margin-bottom: 8px;">{{ factor.label }}</div>
                <el-cascader v-model="factorMethods[idx]"
                             :options="factor.children"
                             :props="props"
                             :placeholder="'请选择' + factor.label"
                             @change="onCascaderChange(idx)"
                             style="width: 90%; margin-bottom: 8px;"/>
                <div style="color: #888; font-size: 13px; min-height: 24px;">
                  <span v-if="factorMethodsLabel[idx].length">已选：{{ factorMethodsLabel[idx].join(' / ') }}</span>
                  <span v-else>请在上方选择具体的{{ factor.label }}</span>
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
  name: "PowerGame_InfluenceDesign",
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
      showModel: 0,
      factorOptions: [
        {
          value: 1, label: '环境因素', children: [
            { value: 1, label: '天气' },
            { value: 2, label: '降水' },
            { value: 3, label: '温度' },
            { value: 4, label: '能见度' },
            { value: 5, label: '其他' },
          ]
        },
        {
          value: 2, label: 'Agent自身因素', children: [
            { value: 1, label: '类型' },
            { value: 2, label: '能力' },
            { value: 3, label: '状态' },
            { value: 4, label: '决策规则' },
            { value: 5, label: '其他' },
          ]
        },
        {
          value: 3, label: '交互因素', children: [
            { value: 1, label: '交互方式' },
            { value: 2, label: '信息传递' },
            { value: 3, label: '协作机制' },
            { value: 4, label: '其他' },
          ]
        }
      ],
      factorMethods: [[], [], []], // 三个因素的选择
      factorMethodsLabel: [[], [], []], // 三个因素的label路径
    }
  },
  mounted() {
    let cardHeight = this.$refs.contentCard.$el.offsetHeight;
    this.cardMaxHeight = cardHeight - 64;
    // 恢复本地存储
    const detailStr = localStorage.getItem('influenceFactorsDetail');
    if (detailStr) {
      try {
        const details = JSON.parse(detailStr);
        for (let i = 0; i < 3; i++) {
          if (details[i]) {
            this.factorMethods[i] = details[i].factor_content_index || [];
            this.factorMethodsLabel[i] = details[i].factor_content_name || [];
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
      this.factorMethodsLabel[idx] = getLabelPath(this.factorOptions[idx].children, this.factorMethods[idx]);
    },
    editCompleted() {
      this.loadingAnimation = true;
      // 合并所有选择，结构与主界面展示一致
      let details = [];
      for (let i = 0; i < 3; i++) {
        details.push({
          factor_index: i + 1,
          factor_name: this.factorOptions[i].label,
          factor_content_index: this.factorMethods[i],
          factor_content_name: this.factorMethodsLabel[i],
        });
      }
      localStorage.setItem('influenceFactorsDetail', JSON.stringify(details));
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
  height: 18vh;
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
</style>