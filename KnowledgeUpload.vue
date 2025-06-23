<template>
  <div style="display: flex; width: 100%; min-width:1200px">
    <el-card style="width: 99%; height: 98%">
      <el-scrollbar max-height="85vh">
        <div style="display: flex; flex-direction: column; width: 100%">
          <!--	导入知识	&& 知识库加载  -->
          <el-card style="width: 100%; height: 400px; margin-top: 1rem">
            <div style="display: flex; width: 100%">
              <!--    导入知识    -->
              <el-card class="click-card" style="width: 20%" shadow="hover">
                <el-scrollbar max-height="320px">
                  <div style="display: flex; flex-direction: column; width: 100%; min-height: 320px;
                      justify-content: center; align-items: center">
                    <el-card class="upload-card" shadow="never" @click="skip('/home/rainCity/knowledgeCreate')">
                      <div style="display: flex; height: 110px; width: 110px; justify-content: center; align-items: center">
                        <el-icon size="30" color="#909399"><Plus/></el-icon>
                      </div>
                    </el-card>
                    <div style="margin-top: 5px">点击创建知识库</div>
                  </div>
                </el-scrollbar>
              </el-card>
              <!--     分割线      -->
              <div style="display: flex; width: 5%; align-items: center; justify-content: center">
                <el-divider direction="vertical" content-position="center" style="height: 360px"/>
                <div class="font-column">知识库加载</div>
              </div>
              <!--    知识库展示    -->
              <div style="width: 75%">
                <el-scrollbar max-height="360px">
                  <div style="display: flex; width: 100%;" v-if="loadedCard.length === 3">
                    <el-card style="display: flex; width: 100%; height: 360px; align-items: center; justify-content: center">
                      <img src="../../assets/images/您还没有知识库哦.png" style="width: 100%" alt="pic"/>
                    </el-card>
                  </div>
                  <div style="display: flex; width: 100%; justify-content: space-between" v-else>
                    <el-card class="click-card" v-for="(item, index) in loadedCard" @click="skip(item.to)"
                             style="width: 30%; margin: 0 1.5%; flex-shrink: 0" shadow="hover">
                      <div class="card-title" :style="{color: item.titleColor}">
                        {{ item.title }}
                      </div>
                      <div
                          style="display: flex; width: 100%; height: 300px; justify-content: center; align-items: center">
                        <img :src="item.url" style="width: 100%; max-height: 90%" :alt="'img' + index"/>
                      </div>
                    </el-card>
                  </div>
                </el-scrollbar>
              </div>
            </div>
          </el-card>
          <!--   知识库展现形式   -->
          <div style="width: 100%; display: flex; min-height: 240px; margin-top: 2rem">
            <el-card style="width: 30%; background-color: rgb(208, 202, 254); border-radius: 20px">
              <div style="display: flex; width: 100%; min-height: 200px">
                <div class="font-column" style="width: 10%; font-size: 20px; color: #000">
                  {{ imgShow[0].title }}
                </div>
                <div style="display: flex; justify-content: center; width: 90%">
                  <img :src="imgShow[0].imgUrl" style="width: 100%; height: 220px" alt="1"/>
                </div>
              </div>
            </el-card>
            <el-card style="width: 30%; margin: 0 5%; background-color: rgb(77, 100, 101); border-radius: 20px">
              <div style="display: flex; width: 100%; min-height: 200px">
                <div class="font-column" style="width: 10%; font-size: 20px; color: #FFF">
                  {{ imgShow[1].title }}
                </div>
                <div style="display: flex; justify-content: center; width: 90%">
                  <img :src="imgShow[1].imgUrl" style="width: 100%; height: 220px" alt="1"/>
                </div>
              </div>
            </el-card>
            <el-card style="width: 30%; background-color: rgb(28, 60, 58); border-radius: 20px">
              <div style="display: flex; width: 100%; min-height: 200px">
                <div class="font-column" style="width: 10%; font-size: 20px; color: #FFF">
                  {{ imgShow[2].title }}
                </div>
                <div style="display: flex; justify-content: center; width: 90%">
                  <img :src="imgShow[2].imgUrl" style="width: 100%; height: 220px" alt="1"/>
                </div>
              </div>
            </el-card>
          </div>
          <div style="display: flex; width: 100%; justify-content: center; margin-top: 1rem;
                      font-size: 22px; font-weight: bold">
            知识库展现形式
          </div>
        </div>
      </el-scrollbar>
    </el-card>
  </div>
</template>

<script>
import {
  ChatLineRound,
  Collection,
  DocumentAdd,
  Expand,
  Notebook,
  OfficeBuilding,
  Plus,
  UploadFilled,
  Van
} from "@element-plus/icons";

export default {
  name: 'PowerGame_KnowledgeUpload',
  components: {UploadFilled, Van, Collection, Notebook, OfficeBuilding, Plus, Expand, DocumentAdd, ChatLineRound},
  data() {
    return {
      loadedCard: [
        {
          title: '主体展示',
          titleColor: 'rgb(121.3, 187.1, 255)',
          url: require('../../assets/images/主体知识.png'),
          to: '/home/powerGame/knowledgeDisplay'
        },
        {
          title: '环境展示',
          titleColor: 'rgb(237.5, 189.9, 118.5)',
          url: require('../../assets/images/3dcity.png'),
          to: '/home/powerGame/knowledgeDisplay'
        },
        {
          title: '规则展示',
          titleColor: 'rgb(250, 181.5, 181.5)',
          url: require('../../assets/images/autonomousAgent.png'),
          to: '/home/powerGame/knowledgeDisplay'
        },
      ],
      imgShow: [
        {title: '主体展示', imgUrl: require('../../assets/images/主体知识.png')},
        {title: '环境展示', imgUrl: require('../../assets/images/3dcity.png')},
        {title: '规则展示', imgUrl: require('../../assets/images/autonomousAgent.png')},
      ]
    }
  },
  methods: {
    skip(to) {
      this.$router.push(to)
    }
  }
}
</script>

<style scoped>
.title-pos {
  display: flex;
  width: 100%;
  align-items: center;
}

.title-font {
  font-size: 20px;
  font-weight: bold;
  font-family: 微软雅黑, serif;
  margin-left: 5px;
}

.content-font {
  font-size: 16px;
  font-weight: lighter;
  line-height: 25px;
  font-family: 微软雅黑, serif;
}

.upload-card{
  width: 150px;
  height: 150px;
  border: 1px dashed #CDD0D6;
  background-color: #FAFCFF;
}
.upload-card:hover{
  width: 150px;
  height: 150px;
  border: 1px dashed #409EFF;
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
  color: #E6A23C
}

.click-title {
  color: #266531;
  cursor: pointer;
}

.click-card {
  display: flex;
  flex-direction: column;
  height: 360px;
}

.click-card:hover {
  cursor: pointer;
}

.tag-card {
  width: 30%;
  background-color: rgb(243.9, 244.2, 244.8);
}

.font-column {
  display: flex;
  writing-mode: vertical-rl;
  letter-spacing: 16px;
  font-size: 18px;
  text-align: center;
  align-items: flex-end;
  justify-content: center;
  font-weight: bold;
}
</style>