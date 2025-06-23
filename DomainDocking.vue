<template>
  <div style="width: 99%; min-width:1200px; display: flex;">
    <el-card style="width: 99%; height: 98%">
      <div style="width: 94%; margin: 1rem 3%">
        <el-card class="content-font" style="min-height: calc(45px + 16vh); flex: 0">
          <el-scrollbar style="width: 100%">
            <div style="width: 100%; display: flex">
              <el-tooltip content="请拖拽右侧知识库文件到对应库中">
                <el-card style="width: 120px; height: 16vh; background-color: #F1E0CE" shadow="hover">
                  <el-icon style="color: #EC9A86" size="80"><WarningFilled/></el-icon>
                  <div style="display: flex; justify-content: center; width: 100%">
                    Tips
                  </div>
                </el-card>
              </el-tooltip>
              <el-divider direction="vertical" style="height: 16vh; margin-left: 1rem" border-style="dashed"/>
              <el-tooltip :content="item.name" placement="bottom" effect="light"
                          v-for="(item,index) in knowledgeBaseData">
                <el-card class="draggable-card" shadow="hover"
                         draggable="true" @dragstart="onDragStart($event, item, index)">
                  <div style="display: flex; flex-direction: column;justify-content: center">
                    <el-icon size="80"><Document/></el-icon>
                    <div style="display: flex; justify-content: center; width: 100%; margin-top: 5px">
                      {{item.name.length < 5 ? item.name : item.name.substring(0,4) + '..'}}
                    </div>
                  </div>
                </el-card>
              </el-tooltip>
            </div>
          </el-scrollbar>
        </el-card>
      </div>
      <div style="display: flex; width: 100%; height: 100%; font-size: 20px; margin-top: 2rem">
        <el-card class="card-class" v-for="(item, index) in cardData" @dragover.prevent @drop="onDrop($event, item, index)"
                 :style="{backgroundColor: item.bgColor}">
          <div class="card-title" style="margin-bottom: 1rem">{{item.title}}</div>
          <div class="content-font" style="display: flex; flex-direction: column">
            <div style="width: 100%; display: flex; align-items: center; line-height: 180%"
                 v-for="(param, index1) in item.content">
              <el-popconfirm
                  title="确定将该知识库放回到未分类库中吗？"
                  @confirm="deleteDoc(index, index1)">
                <template #reference>
                  <div class="hover-font">
                    <el-icon><Document/></el-icon> {{param}}
                  </div>
                </template>
              </el-popconfirm>
            </div>
          </div>
        </el-card>
      </div>
    </el-card>
  </div>
</template>

<script>
import {Document, Warning, WarningFilled} from "@element-plus/icons-vue";
import {ElMessage} from "element-plus";

export default {
  name: "PowerGame_DomainDocking",
  components: {WarningFilled, Warning, Document},
  data(){
    return{
      knowledgeBaseData: [
        {name: '降雨数据'},
        {name: '排水报告'},
        {name: '交通流量'},
        {name: '居民疏散'},
        {name: '应急预案'},
        {name: '政策通知'},
        {name: '管制措施'},
        {name: '城市规划'},
      ],
      cardData: [
        {
          title: '主体库', 
          bgColor: '#c6b4d8',
          content: [
            '公交调度 Agent 在内涝期间的线路调整记录',
            '政策发布 Agent 向居民发布的疏散通知样本',
            '交通管制 Agent 对主要路段的管制实施报告'
          ],
        },
        {
          title: '环境库', 
          bgColor: '#f5c0bf',
          content: [
            '城市内涝期间的降雨量和积水深度监测数据',
            '历史内涝事件对城市交通网络影响的分析报告',
            '城市排水系统设计与实际运行效率评估'
          ],
        },
        {
          title: '规则库', 
          bgColor: '#C5DFDF',
          content: [
            '城市内涝应急管理条例及其实施细则',
            '交通管制和疏散行动的法律依据与限制分析',
            '城市规划中关于防洪排涝设施建设的规范'
          ],
        },
      ]
    }
  },
  methods:{
    onDragStart(event, item, index){
      let cardInfo = {fromIndex: index};
      window.sessionStorage.setItem('dragCardInfo', JSON.stringify(cardInfo));
    },
    onDrop(event, item, index){
      let fromIndex = JSON.parse(window.sessionStorage.getItem('dragCardInfo')).fromIndex;
      console.log('fromIndex', fromIndex);
      this.cardData[index].content.push(this.knowledgeBaseData[fromIndex].name);
      this.knowledgeBaseData.splice(fromIndex, 1);
      ElMessage({
        message: '知识库分类成功',
        type: 'success',
      });
    },
    deleteDoc(index0, index1){
      this.knowledgeBaseData.push({name: this.cardData[index0].content[index1]});
      this.cardData[index0].content.splice(index1, 1);
      ElMessage({
        message: '该知识库重新归为未分类状态',
        type: 'info',
      });
    }
  }
}
</script>

<style scoped>
.card-class{
  width: 27.3%;
  height: 55vh;
  margin: 0 3%;
  border-radius: 3%;
  display: flex;
  flex-direction: column;
}
.card-title{
  font-size: 25px;
  font-weight: bold;
  width: 100%;
  display: flex;
  justify-content: center;
  font-family: "Microsoft YaHei", "STHeiti Light", "Segoe UI", sans-serif;
}
.content-font {
  font-size: 16px;
  font-weight: normal;
  line-height: 25px;
  font-family: 微软雅黑, serif;
  display: flex;
}
.hover-font{
  cursor: pointer;
}
.hover-font:hover{
  color: #fff
}
.draggable-card{
  background-color: #F0EAE0;
  width: 120px;
  height: 16vh;
  cursor: pointer;
  margin: 2px 1rem;
}
</style>