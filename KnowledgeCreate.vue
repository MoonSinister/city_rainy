<template>
  <div style="width: 99%; min-width:1200px; display: flex;">
    <el-card style="width: 99%; height: 98%">
      <div style="display: flex; flex-direction: column; width: 100%; height: 100%; font-size: 20px; margin-top: 1rem">
        <!--   头部导航     -->
        <div style="display: flex; width: 100%; align-items: center">
          <el-page-header @back="onBack()">
            <template #content>
              <el-breadcrumb separator="/" style="margin-top: 5px">
                <el-breadcrumb-item :to="{ path: '/' }">知识库</el-breadcrumb-item>
                <el-breadcrumb-item>配置</el-breadcrumb-item>
              </el-breadcrumb>
            </template>
          </el-page-header>
        </div>

        <el-card style="width: 100%; height: 150px; margin-top: 1rem" v-if="false">

        </el-card>

        <div style="display: flex; width: 100%">
          <!--     左侧头像+选项卡     -->
          <div style="width: 18%; display: flex; flex-direction: column; align-items: center">
            <el-card style="border-radius: 50%; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; margin-top: 5rem; --el-card-padding: 10px">
              <img src="../../assets/images/autonomousAgentImg.png" style="width: 100%; height: 100%" alt="pic"/>
            </el-card>
            <span style="font-size: 16px; margin-top: 1rem; font-weight: bold">Test</span>

            <el-divider style="width: 90%; margin-right: 5%" border-style="dashed"></el-divider>

            <div style="display: flex; flex-direction: column; width: 90%; margin: 0 5%">
              <el-card :class="index === selectedCard ? 'item-card-selected' : 'item-card'" v-for="(item, index) in itemCard"
                       shadow="never" @click="itemCardClick(index)">
                <div style="display: flex; align-items: center">
                  <el-icon size="20" style="margin-right: 5px; margin-top: 1px">
                    <component :is="item.icon"></component>
                  </el-icon>
                  {{item.name}}
                </div>
              </el-card>
            </div>
          </div>
          <!--     右侧主体     -->
          <div style="width: 82%">
            <el-scrollbar max-height="81vh">
              <div style="display: flex; width: 100%; flex-direction: column; margin-top: 3rem" v-if="selectedCard === 0">
                <div>数据集</div>
                <div style="font-size: 14px; margin-top: 5px; display: flex; align-items: center">
                  <el-icon size="14" style="margin-right: 5px"><Shop/> </el-icon>
                  解析成功后才可以回答哦
                </div>
                <el-divider></el-divider>
                <div style="display: flex; width: 100%; flex-direction: column">
                  <div style="display: flex; align-items: center; justify-content: space-between; width: 100%">
                    <el-select v-model="batchSelection" placeholder="批量" :disabled="batchSelectionDisabled" style="width: 100px">
                      <el-option v-for="item in batchOptions"
                                 :label="item.label" :key="item.value" :value="item.value" />
                    </el-select>
                    <div style="display: flex">
                      <el-input v-model="docNameSearch" placeholder="请输入文件名称">
                        <template #prepend>
                          <el-icon><Search/></el-icon>
                        </template>
                      </el-input>
                      <el-button type="primary" style="margin-left: 1rem">+ 新增文件</el-button>
                    </div>
                  </div>
                  <el-table :data="filteredData"
                            @selection-change="handleSelectionChange"
                            style="width: 100%">
                    <el-table-column type="selection" />
                    <el-table-column prop="name" label="名称" min-width="200" align="center" style="color: #67C23A"/>
                    <el-table-column prop="blockNum" label="分块数" min-width="120" align="center"/>
                    <el-table-column prop="date" label="上传日期" min-width="200" align="center"/>
                    <el-table-column prop="analysisMethod" label="解析方法" min-width="200" align="center"/>
                    <el-table-column prop="isRun" label="启用" min-width="120" align="center">
                      <template #default="scope">
                        <el-switch v-model="scope.row.isRun" />
                      </template>
                    </el-table-column>
                    <el-table-column prop="analysisState" label="解析状态" min-width="120" align="center">
                      <template #default="scope">
                        <el-tag :type="scope.row.analysisState === 1 ? 'success' : 'primary'"
                            disable-transitions>
                          {{ scope.row.analysisState === 1 ? '成功' : '未解析' }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="action" label="动作" min-width="280" align="center">
                      <template #default="scope">
                        <div style="display: flex; width: 100%; justify-content: center">
                          <el-button plain size="mini" style="padding: 0 6px">
                            <el-icon><setting/></el-icon>
                          </el-button>
                          <el-tooltip effect="dark" content="重命名" placement="top">
                            <el-button plain size="mini" style="padding: 0 6px">
                              <el-icon><edit/></el-icon>
                            </el-button>
                          </el-tooltip>
                          <el-tooltip effect="dark" content="删除" placement="top">
                            <el-button plain size="mini" style="padding: 0 6px">
                              <el-icon><delete/></el-icon>
                            </el-button>
                          </el-tooltip>
                          <el-tooltip effect="dark" content="下载" placement="top">
                            <el-button plain size="mini" style="padding: 0 6px">
                              <el-icon><download/></el-icon>
                            </el-button>
                          </el-tooltip>
                        </div>
                      </template>
                    </el-table-column>
                  </el-table>
                </div>
              </div>
              <div style="display: flex; width: 100%; margin-top: 1rem; justify-content: space-between"
                   v-if="selectedCard === 1">
                <el-scrollbar max-height="78vh" style="width: 25%">
                  <div style="display: flex; flex-direction: column; margin-top: 1rem; font-size: 14px; width: 95%">
                    <span style="font-weight: bold; font-size: 16px">检索测试</span>
                    <span style="margin-top: 5px; font-size: 14px">最后一步！成功后就放心交给RagFlow（MACE版）吧。</span>
                    <el-divider></el-divider>

                    <span style="margin: 0.5rem 0">相似度阈值</span>
                    <el-slider v-model="retrievalTest.similarityThreshold" :min="0" :max="1" :step="0.01" style="width: 92%; margin: 0 4%" />
                    <span style="margin: 0.5rem 0">关键字相似度权重</span>
                    <el-slider v-model="retrievalTest.keywordSimilarityWeight" :min="0" :max="1" :step="0.01" style="width: 92%; margin: 0 4%" />
                    <span style="margin: 0.5rem 0">Rerank模型</span>
                    <el-select v-model="retrievalTest.rerankModel" clearable style="width: 100%">
                      <el-option-group
                          v-for="group in rerankOptions"
                          :key="group.label"
                          :label="group.label">
                        <el-option
                            v-for="item in group.options"
                            :key="item.value"
                            :label="item.label"
                            :value="item.value"/>
                      </el-option-group>
                    </el-select>
                    <span style="margin: 1rem 0">使用知识图谱</span>
                    <el-switch v-model="retrievalTest.isUseKnowledgeMap" />
                    <span style="margin: 1rem 0">测试文本</span>
                    <el-input v-model="retrievalTest.testText" type="textarea" :rows="8"/>
                    <el-button style="margin: 1rem auto; width: 20%" type="primary">测试</el-button>
                    <div style="height: 100px" />
                  </div>
                </el-scrollbar>
                <div style="display: flex; width: 72%; margin-top: 1rem">
                  <el-card style="width: 100%; height: 50px; --el-card-padding: 12px 20px" shadow="never">
                    <span style="font-size: 14px">0/0  选定的文件</span>
                  </el-card>
                </div>
              </div>
              <div style="display: flex; width: 100%; margin-top: 1rem" v-if="selectedCard === 2">
                <!--      中间表单      -->
                <div style="width: 38%; display: flex; flex-direction: column">
                  <el-form :model="knowledgeBaseForm" label-width="auto" label-position="top"
                           style="max-width: 600px">
                    <el-form-item label="知识库名称" required>
                      <el-input v-model="knowledgeBaseForm.name" style="width: 90%"/>
                    </el-form-item>
                    <el-form-item label="知识库图片">
                      <el-upload
                          action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15"
                          multiple list-type="picture-card" :auto-upload="false"
                          style="display: flex; width: 100%; justify-content: center; flex-grow: 1">
                        <el-icon size="100" style="margin-top: 3.5rem"><Plus /></el-icon>
                      </el-upload>
                    </el-form-item>
                    <el-form-item label="描述">
                      <el-input v-model="knowledgeBaseForm.description" style="width: 90%"></el-input>
                    </el-form-item>
                    <el-form-item label="文档语言" required>
                      <el-select v-model="knowledgeBaseForm.language" style="width: 90%">
                        <el-option v-for="item in languageOptions"
                                   :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="权限" required>
                      <el-radio-group v-model="knowledgeBaseForm.authority">
                        <el-radio label="0">只有我</el-radio>
                        <el-radio label="1">团队</el-radio>
                      </el-radio-group>
                    </el-form-item>
                    <el-form-item label="嵌入模型" required>
                      <el-select v-model="knowledgeBaseForm.model" style="width: 90%">
                        <el-option-group
                            v-for="group in modelOptions"
                            :key="group.label"
                            :label="group.label">
                          <el-option
                              v-for="item in group.options"
                              :key="item.value"
                              :label="item.label"
                              :value="item.value"/>
                        </el-option-group>
                      </el-select>
                    </el-form-item>
                    <el-form-item label="解析方法" required>
                      <el-select v-model="knowledgeBaseForm.analyticMethod" style="width: 90%">
                        <el-option v-for="item in analyticMethodOptions"
                                   :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="页面排名">
                      <el-slider v-model="knowledgeBaseForm.pageRank" :max="100" style="width: 88%; margin-left: 2%" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label="自动关键词">
                      <el-slider v-model="knowledgeBaseForm.autoKeyWord" :max="30" style="width: 88%; margin-left: 2%" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label="自动问题">
                      <el-slider v-model="knowledgeBaseForm.autoQuestion" :max="10" style="width: 88%; margin-left: 2%" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label="块Token数">
                      <el-slider  v-model="knowledgeBaseForm.tokenNum" :min="128" :max="2048" style="width: 88%; margin-left: 2%" show-input></el-slider>
                    </el-form-item>
                    <el-form-item label="分段标识符" required>
                      <el-input v-model="knowledgeBaseForm.segmentIdentifier" style="width: 90%"/>
                    </el-form-item>
                    <el-form-item label="布局识别和OCR">
                      <el-select v-model="knowledgeBaseForm.layoutAndOCR" style="width: 90%">
                        <el-option v-for="item in layoutAndOCROptions"
                                   :key="item.value" :label="item.label" :value="item.value" />
                      </el-select>
                    </el-form-item>
                    <el-form-item label="表格转HTML">
                      <el-switch v-model="knowledgeBaseForm.isTableToHtml" />
                    </el-form-item>
                    <el-form-item label="使用召回增强RAPTOR策略">
                      <el-switch v-model="knowledgeBaseForm.isRAPTOR" />
                    </el-form-item>
                    <el-form-item label="提示词" v-if="knowledgeBaseForm.isRAPTOR === true" required>
                      <el-input type="textarea" v-model="knowledgeBaseForm.RAPTORPrompt" :rows="5"></el-input>
                    </el-form-item>
                    <el-card style="width: 90%; display: flex; flex-direction: column; background-color: #FAFCFF; --el-card-padding: 5px">
                      <el-form-item label="提取知识图谱">
                        <el-switch v-model="knowledgeBaseForm.isGetKnowledgeMap" />
                      </el-form-item>
                      <div v-if="knowledgeBaseForm.isGetKnowledgeMap === true">
                        <el-form-item label="实体类型" required>
                          <el-tag v-for="tag in knowledgeBaseForm.knowledgeMapCategory" style="margin-right: 5px"
                              :key="tag" closable @close="knowledgeMapCategoryClose(tag)">
                            {{ tag }}
                          </el-tag>
                          <el-input v-if="inputVisible" style="width: 90%"
                              ref="InputRef" v-model="inputValue" size="small"
                              @keyup.enter="handleInputConfirm" @blur="handleInputConfirm"/>
                          <el-button v-else class="button-new-tag" size="small" @click="knowledgeMapCategoryShowInput()">
                            + New
                          </el-button>
                        </el-form-item>
                        <el-form-item label="方法">
                          <el-select v-model="knowledgeBaseForm.knowledgeMapMethod" style="width: 90%">
                            <el-option v-for="item in knowledgeMapMethodOptions"
                                       :key="item.value" :label="item.label" :value="item.value" />
                          </el-select>
                        </el-form-item>
                        <el-form-item label="实体归一化" >
                          <el-switch v-model="knowledgeBaseForm.knowledgeMapNormalize" />
                        </el-form-item>
                        <el-form-item label="社区报告生成" >
                          <el-switch v-model="knowledgeBaseForm.knowledgeMapReport" />
                        </el-form-item>
                      </div>
                    </el-card>
                  </el-form>
                  <div style="width: 100%; display: flex; justify-content: center; margin-top: 2rem">
                    <el-button>取消</el-button>
                    <el-button type="primary" @click="onSubmit">保存</el-button>
                  </div>
                </div>
                <div style="width: 2%; display: flex">
                  <el-divider direction="vertical" style="height: 100%"/>
                </div>
                <!--     右侧解释性文字     -->
                <div class="display-content"
                     v-if="knowledgeBaseForm.analyticMethod === 0">
                  <b style="font-size: 18px">"General" 分块方法说明</b>
                  <p>支持的文件格式为<b>DOCX、EXCEL、PPT、IMAGE、PDF、TXT、MD、JSON、EML、HTML。</b></p>
                  <p>此方法将简单的方法应用于块文件：</p>
                  <p>- 系统将使用视觉检测模型将连续文本分割成多个片段。</p>
                  <p>- 接下来，这些连续的片段被合并成Token数不超过“Token数”的块。</p>
                  <p style="font-size: 18px; margin-top: 1rem"><b>"General" 示例</b></p>
                  <p>提出以下屏幕截图以促进理解。</p>
                  <div style="display: flex; width: 100%">
                    <img src="../../assets/images/knowledge-general-1.svg" style="width: 49%; margin-right: 2%" alt="pic"/>
                    <img src="../../assets/images/knowledge-general-2.svg" style="width: 49%" alt="pic"/>
                  </div>
                  <b style="font-size: 18px; margin-top: 1rem">"General" 对话示例</b>
                  <el-divider></el-divider>
                </div>
                <div class="display-content"
                     v-else-if="knowledgeBaseForm.analyticMethod === 1">
                  <b style="font-size: 18px">"Q&A" 分块方法说明</b>
                  <p>此块方法支持 <b>excel</b> 和 <b>csv/txt</b> 文件格式。</p>
                  <p>- 如果文件是 <b>excel</b> 格式，则应由两个列组成 没有标题：一个提出问题，另一个用于答案， 答案列之前的问题列。多张纸是 只要列正确结构，就可以接受。</p>
                  <p>- 如果文件是 <b>csv/txt</b> 格式 以 UTF-8 编码且用 TAB 作分开问题和答案的定界符。</p>
                  <p>未能遵循上述规则的文本行将被忽略，并且 每个问答对将被认为是一个独特的部分。</p>
                  <p style="font-size: 18px; margin-top: 1rem"><b>"Q&A" 示例</b></p>
                  <p>提出以下屏幕截图以促进理解。</p>
                  <div style="display: flex; width: 100%">
                    <img src="../../assets/images/knowledge-q&a-1.svg" style="width: 49%; margin-right: 2%" alt="pic"/>
                    <img src="../../assets/images/knowledge-q&a-2.svg" style="width: 49%" alt="pic"/>
                  </div>
                  <b style="font-size: 18px; margin-top: 1rem">Q&A 对话示例</b>
                  <el-divider></el-divider>
                </div>
                <div class="display-content"
                     v-else>
                  <b style="font-size: 18px">"Resume" 分块方法说明</b>
                  <p>支持的文件格式为<b>DOCX、PDF、TXT。</b></p>
                  <p>简历有多种格式，就像一个人的个性一样，但我们经常必须将它们组织成结构化数据，以便于搜索。</p>
                  <p>我们不是将简历分块，而是将简历解析为结构化数据。 作为HR，你可以扔掉所有的简历， 您只需与'RAGFlow'交谈即可列出所有符合资格的候选人。</p>
                  <p style="font-size: 18px; margin-top: 1rem"><b>"Resume" 示例</b></p>
                  <p>提出以下屏幕截图以促进理解。</p>
                  <div style="display: flex; width: 100%">
                    <img src="../../assets/images/knowledge-resume-1.svg" style="width: 49%; margin-right: 2%" alt="pic"/>
                    <img src="../../assets/images/knowledge-resume-2.svg" style="width: 49%" alt="pic"/>
                  </div>
                  <b style="font-size: 18px; margin-top: 1rem">Resume 对话示例</b>
                  <el-divider></el-divider>
                </div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import {Plus, House, Setting, Aim, Coin, Shop, Search, Download, Delete, Edit} from "@element-plus/icons";
import {computed, nextTick, ref} from "vue";

export default {
  name: "PowerGame_KnowledgeCreate",
  components: {Edit, Delete, Download, Search, Shop, Plus, House, Setting, Aim, Coin},
  setup(){},
  data(){
    return{
      knowledgeBaseForm: {
        name: '',
        img: '',
        description: '',
        language: 0,
        authority: '0',
        model: 0,
        analyticMethod: 0,
        pageRank: 0,
        autoKeyWord: 0,
        autoQuestion: 0,
        tokenNum: 0,
        segmentIdentifier: '\\n!?;。；！？',
        layoutAndOCR: 0,
        isTableToHtml: false,
        isRAPTOR: false,
        RAPTORPrompt: '请总结以下段落。 小心数字，不要编造。 段落如下：\n' +
            '      {cluster_content}\n' +
            '以上就是你需要总结的内容。',
        isGetKnowledgeMap: false,
        knowledgeMapCategory: ['organization', 'person', 'geo', 'event', 'category'],
        knowledgeMapMethod: 0,
        knowledgeMapNormalize: false,
        knowledgeMapReport: false,
      },
      languageOptions: [
        {label: '简体中文', value: 0},
        {label: '英文', value: 1},
      ],
      modelOptions: [
        {
          label: 'BAAI',
          options: [
            {value: 0, label: 'BAAI/bge-large-zh-v1.5'},
          ],
        },
        {
          label: 'FastEmbed',
          options: [
            {value: 1, label: 'BAAI/bge-base-en-v1.5'},
            {value: 2, label: 'BAAI/bge-large-en-v1.5'},
            {value: 3, label: 'BAAI/bge-small-en-v1.5'},
            {value: 4, label: 'BAAI/bge-small-zh-v1.5'},
            {value: 5, label: 'jinnaai/jina-embeddings-v2-base-en'},
            {value: 6, label: 'jinnaai/jina-embeddings-v2-small-en'},
            {value: 7, label: 'nomic-ai/nomic-embed-text-v1.5'},
            {value: 7, label: 'sentence-transformers/all-MiniLM-L6-v2'},
          ],
        },
        {
          label: 'youdao',
          options: [
            {value: 5, label: 'maidalun1020/bce-embedding-base_v1'},
          ],
        },

      ],
      analyticMethodOptions: [
        {label: 'General', value: 0},
        {label: 'Q&A', value: 1},
        {label: 'Resume', value: 2},
        {label: 'Manual', value: 3},
        {label: 'Table', value: 4},
        {label: 'Paper', value: 5},
        {label: 'Book', value: 6},
        {label: 'Laws', value: 7},
        {label: 'Presentation', value: 8},
        {label: 'One', value: 9},
        {label: 'Tag', value: 10},
      ],
      layoutAndOCROptions: [
        {label: 'DeepDoc', value: 0},
        {label: 'Plain Text', value: 1},
      ],
      knowledgeMapMethodOptions: [
        {label: 'Light', value: 0},
        {label: 'General', value: 1},
      ],
      inputVisible: false,
      inputValue: '',
      selectedCard: 0,
      itemCard: [
        {icon: Coin, name: '数据集'},
        {icon: Aim, name: '检索测试'},
        {icon: Setting, name: '配置'},
      ],
      datasetData: [
        {name: '你好', blockNum: '1', date: '2025-03-04', analysisMethod: 'Picture', isRun: true, analysisState: 0, action: 1},
        {name: '你好？', blockNum: '3', date: '2025-03-05', analysisMethod: 'Picture', isRun: false, analysisState: 1, action: 2},
        {name: '我不好', blockNum: '3', date: '2025-03-05', analysisMethod: 'Picture', isRun: false, analysisState: 1, action: 2},
        {name: '哦天呐', blockNum: '3', date: '2025-03-05', analysisMethod: 'Picture', isRun: false, analysisState: 1, action: 2},
      ],
      filterTableData: this.datasetData,
      docNameSearch: '',
      batchSelection: '',
      batchSelectionDisabled: true,
      batchOptions: [
        {value: 0, label: '启用'},
        {value: 1, label: '禁用'},
        {value: 2, label: '解析'},
        {value: 3, label: '取消'},
        {value: 4, label: '删除'},
      ],
      retrievalTest: {
        similarityThreshold: 0.2,
        keywordSimilarityWeight: 0.7,
        rerankModel: '',
        isUseKnowledgeMap: false,
        testText: '',
      },
      rerankOptions: [
        {
          label: 'BAAI',
          options: [
            {value: 0, label: 'BAAI/bge-rerank-v2-m3'},
          ],
        },
        {
          label: 'youdao',
          options: [
            {value: 1, label: 'maidalun1020/bge-rerank-base_v1'},
          ],
        },
      ]
    }
  },
  computed:{
    filteredData() {
      if(this.docNameSearch === '')
        return this.datasetData;
      else
        return this.datasetData.filter((data) =>
            !this.docNameSearch || data.name.toLowerCase().includes(this.docNameSearch.toLowerCase())
        )
    }
  },
  methods: {
    onBack(){
      this.$router.push('/home/powerGame/knowledgeUpload')
    },
    knowledgeMapCategoryClose(tag){
      this.knowledgeBaseForm.knowledgeMapCategory.splice(this.knowledgeBaseForm.knowledgeMapCategory.indexOf(tag), 1)
    },
    knowledgeMapCategoryShowInput(){
      this.inputVisible = true;
      nextTick(() => {
        this.$refs.InputRef.focus();
      })
    },
    handleInputConfirm(){
      if (this.inputValue) {
        this.knowledgeBaseForm.knowledgeMapCategory.push(this.inputValue)
      }
      this.inputVisible = false;
      this.inputValue = ''
    },
    itemCardClick(index){
      this.selectedCard = index;
    },
    handleSelectionChange(){
      this.batchSelectionDisabled = !this.batchSelectionDisabled;
    }
  }
}
</script>

<style scoped>
.display-content{
  width: 60%;
  display: flex;
  flex-direction: column;
  line-height: 180%;
  font-size: 16px
}
.item-card{
  width: 95%;
  height: 45px;
  display: flex;
  align-items: center;
  --el-card-padding: 0 20px;
  border: 0;
  margin: 1px 0;
  font-size: 16px;
  font-weight: bold;
  color: #000;
  border-radius: 8px;
  cursor: pointer;
  transition: ease-in-out 0.2s;
}
.item-card:hover{
  background-color: rgb(199.5, 201, 204);
}
.item-card-selected{
  background-color: rgb(216.8, 235.6, 255);
  color: #409EFF;
  width: 95%;
  height: 45px;
  display: flex;
  align-items: center;
  --el-card-padding: 0 20px;
  border: 0;
  margin: 1px 0;
  font-size: 16px;
  font-weight: bold;
  border-radius: 8px;
  cursor: pointer;
  transition: ease-in-out 0.2s;
}
</style>