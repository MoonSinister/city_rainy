<template>
  <div class="experiment-design-outer">
    <!-- 新增：最外层一行，可自定义内容（如标题、说明、导航等） -->
    <div class="experiment-design-header" style="width: 100%; min-width: 1200px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between;">
      <div style="font-size: 22px; font-weight: bold; color: #409EFF; letter-spacing: 2px;">城市降水对交通影响实验设计</div>
      <!-- 可在此处添加更多内容，如操作按钮、说明等 -->
      <div style="font-size: 14px; color: #888;">实验流程全览与分步操作</div>
    </div>
    <div style="width: 99%; min-width:1200px; display: flex">
      <div style="width: 99%; min-width: 1200px; display: inline;">
        <!--		实验设计鱼骨图 	-->
        <el-card style="width: 100%;height: 98%; position: relative;" v-show="this.active < 4">
          <el-button type="primary" style="position: absolute; right: 40px; top: 20px; z-index: 1001;" @click="openChatDialog">选择方案</el-button>
          <!-- 聊天对话框 -->
          <el-dialog v-model="chatDialogVisible" width="800px" :close-on-click-modal="false" @close="onChatDialogClose">
            <div>
              <ChatWithAgentD />
              <div style="text-align: right; margin-top: 20px;">
                <el-button type="primary" @click="autoFinishByAgent">由Agent自动完成设计</el-button>
              </div>
            </div>
          </el-dialog>
          <!-- 方案选择内容，仅在聊天对话框关闭后显示 -->
          <el-dialog v-model="presetDialogVisible" title="选择实验预设方案" center width="50%" :close-on-click-modal="false" :show-close="true">
            <div style="display: flex; gap: 1.5rem; justify-content: center;">
              <el-card v-for="(preset, idx) in presetSchemes" :key="idx" style="width: 260px; cursor: pointer; border: 2px solid #409EFF;" @click="selectPresetScheme(idx)">
                <div style="font-weight: bold; font-size: 18px; color: #409EFF; margin-bottom: 10px;">{{ preset.name }}</div>
                <div style="margin-bottom: 8px;"><b>目标：</b>{{ preset.goal.goal_name }}</div>
                <div style="margin-bottom: 8px;"><b>方法：</b>{{ preset.goal.goal_content_name.join(' / ') }}</div>
                <div style="margin-bottom: 8px;"><b>影响因素：</b>{{ preset.influenceNames.join('、') }}</div>
                <div style="margin-bottom: 8px;"><b>响应变量：</b>{{ preset.responseNames.join('、') }}</div>
                <div><b>实验方法：</b>{{ preset.methodNames.join('、') }}</div>
              </el-card>
            </div>
          </el-dialog>
          <div style="display: flex; justify-content: center; width: 100%">
            <el-steps style="width: 50%; max-width: 800px" :active="active" finish-status="success" align-center>
              <el-step title="实验目标设计"/>
              <el-step title="影响因素设计"/>
              <el-step title="响应变量设计"/>
              <el-step title="实验方法选择"/>
            </el-steps>
          </div>
          <!-- 新增一排四个信息块，分别展示目标/方法、影响因素、响应变量、实验方法 -->
          <div style="width: 100%; display: flex; margin-bottom: 18px; gap: 1.5%">
            <!-- 目标/方法详情 -->
            <el-card style="flex: 1; min-width: 180px; background: #fffbe6;">
              <div style="font-size: 14px; color: #666;">
                <div v-if="experimentGoal">
                  <b>目标详情：</b>
                  <div style="margin-top: 4px;">{{ experimentGoal.goal_name || '无' }}</div>
                  <b style="margin-top: 8px; display: block;">方法详情：</b>
                  <div>{{ experimentGoal.goal_content_name ? experimentGoal.goal_content_name.join(' / ') : '无' }}</div>
                </div>
                <div v-else>暂无目标信息</div>
              </div>
            </el-card>
            <!-- 影响因素详情 -->
            <!-- 影响因素综合详情 -->
            <el-card style="flex: 1; min-width: 180px; background: #f0f9eb; cursor: pointer;"
                     @click="enterInfluenceDesign">
              <div style="font-size: 14px; color: #666;">
                <b>影响因素综合详情：</b>
                <div v-if="influenceFactorsDetail && influenceFactorsDetail.length">
                  <div v-for="(item, idx) in influenceFactorsDetail" :key="idx" style="margin-bottom: 6px;">
                    <span style="font-weight: bold;">{{ item.factor_name }}：</span>
                    <span v-if="item.factor_content_name && item.factor_content_name.length">
                      <el-tooltip :content="item.factor_content_name.join(' / ')" placement="top">
                        <span>{{ item.factor_content_name.join(' / ') }}</span>
                      </el-tooltip>
                    </span>
                    <span v-else>未选择</span>
                  </div>
          
                </div>
                <div v-else>暂无影响因素信息</div>
              </div>
            </el-card>
            <!-- 响应变量详情 -->
            <!-- 响应变量综合详情 -->
            <el-card style="flex: 1; min-width: 180px; background: #e8f4fd; cursor: pointer;"
                     @click="enterResponseDesign">
              <div style="font-size: 14px; color: #666;">
                <b>响应变量综合详情：</b>
                <div v-if="responseVarsDetail && responseVarsDetail.length">
                  <div v-for="(item, idx) in responseVarsDetail" :key="idx" style="margin-bottom: 6px;">
                    <span style="font-weight: bold;">{{ item.var_name }}：</span>
                    <span v-if="item.var_content_name && item.var_content_name.length">
                      <el-tooltip :content="item.var_content_name.join(' / ')" placement="top">
                        <span>{{ item.var_content_name.join(' / ') }}</span>
                      </el-tooltip>
                    </span>
                    <span v-else>未选择</span>
                  </div>
                </div>
                <div v-else>暂无响应变量信息</div>
              </div>
            </el-card>
            <!-- 实验方法详情 -->
            <el-card style="flex: 1; min-width: 180px; background: #f3e8fd;">
              <div style="font-size: 14px; color: #666;">
                <b>实验方法详情：</b>
                <div style="margin-top: 4px;">
                  <span v-if="experimentMethods && experimentMethodSelection">
                    <span v-for="(m, idx) in experimentMethods" :key="m">
                      <span v-if="experimentMethodSelection[idx]">
                        {{ m === 'certainExperiment' ? '确定性实验设计' : m === 'randomExperiment' ? '非确定性实验设计' : m }}<br/>
                      </span>
                    </span>
                  </span>
                  <span v-else>无</span>
                </div>
                <div v-if="experimentMethodName" style="margin-top: 8px; color: #409EFF; font-weight: bold;">方案：{{ experimentMethodName }}</div>
              </div>
            </el-card>

          </div>
          <div style="display: flex; height: 0%;margin-top: 1rem;">
            <!-- 实验目标设计（鱼尾） -->
            <div style="display: inline-block; position: relative; width: 12%">
              <el-card style="width: 100%; height: calc(100vh - 270px);">
                <div style="display: inline">
                  <div class="exp-title">实验目标设计</div>
                  <div v-if="experimentGoal" style="margin: 30px 0 20px 0; font-size: 15px; color: #333;">
                  </div>
                  <div style="display: flex; justify-content: center; height: calc(100vh - 270px - 64px - 200px)">
                    <el-tooltip content="实验目标设计" placement="right" effect="light">
                      <img src="../../assets/images/fishTail.png" alt="fish tail"
                           style="margin: auto; cursor: pointer; width: 100%" @click="enterExperimentGoalDesign()"/>
                    </el-tooltip>
                  </div>
                </div>
              </el-card>
              <div class="overlay" v-if="active < 0"></div>
              <div class="overlay-success" v-if="active > 0"></div>
            </div>
            <!-- 影响因素（鱼骨） -->
            <div style="display: inline-block; position: relative; width: 44%; margin-left: 1%">
              <el-card style="width: 100%; height: calc(100vh - 270px);">
                <div style="position: relative; width: 100%; height: 100%;">
                  <fish-bone-chart ref="fishBoneChart"></fish-bone-chart>
                  <!-- 覆盖层，点击跳转，鼠标悬停有提示 -->
                  <div 
                    @click="enterInfluenceDesign" 
                    style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; cursor: pointer; background: rgba(255,255,255,0); z-index: 10;"
                    @mouseenter="showInfluenceTip = true" 
                    @mouseleave="showInfluenceTip = false">
                    <el-tooltip v-if="showInfluenceTip" content="点击进入影响因素设计" placement="top" effect="light">
                      <div style="width:100%;height:100%"></div>
                    </el-tooltip>
                  </div>
                </div>
              </el-card>
              <div class="overlay" v-if="active < 1"></div>
              <div class="overlay-success" v-if="active > 1"></div>
            </div>
            <!-- 响应变量（鱼头） -->
            <div style="display: inline-block; position: relative; width: 20%; margin-left: 1%">
              <el-card style="width: 100%; height: calc(100vh - 270px);">
                <div style="display: inline">
                  <div class="exp-title">响应变量设计</div>
                  <div style="display: flex; justify-content: center; height: calc(100vh - 270px - 64px - 24px)">
                    <el-tooltip content="响应变量设计" placement="right" effect="light">
                      <img src="../../assets/images/fishHead.png" alt="fish head"
                           style="margin: auto; cursor: pointer; width: 90%" @click="enterResponseDesign()"/>
                    </el-tooltip>
                  </div>
                </div>
              </el-card>
              <div class="overlay" v-if="active < 2"></div>
              <div class="overlay-success" v-if="active > 2"></div>
            </div>
            <!-- 实验方法 -->
            <div style="display: inline-block; position: relative; width: 20%; margin-left: 1%">
              <el-card style="width: 100%; height: calc(100vh - 270px);">
                <div style="position: relative; width: 100%; height: 100%;">
                  <div style="display: inline">
                    <div class="exp-title">实验方法选择</div>
                    <div style="width: 100%; margin-top: 1rem">
                      <experiment-content ref="experimentContent"
                                          @certainSelectionChange="certainSelectionChange"
                                          @uncertainSelectionChange="uncertainSelectionChange"
                                          @expMethodName="getExperimentMethodName">
                      </experiment-content>
                    </div>
                  </div>
                  <!-- 覆盖层，点击跳转，鼠标悬停有提示 -->
                  <div 
                    @click="enterMethodDesign" 
                    style="position: absolute; left: 0; top: 0; width: 100%; height: 100%; cursor: pointer; background: rgba(255,255,255,0); z-index: 10;"
                    @mouseenter="showMethodTip = true" 
                    @mouseleave="showMethodTip = false">
                    <el-tooltip v-if="showMethodTip" content="点击进入实验方法选择" placement="top" effect="light">
                      <div style="width:100%;height:100%"></div>
                    </el-tooltip>
                  </div>
                </div>
              </el-card>
              <div class="overlay" v-if="active < 3"></div>
              <div class="overlay-success" v-if="active > 3"></div>
            </div>
          </div>
          <!-- 新增：四个主块之间的箭头导航 -->
          <div style="display: flex; align-items: center; width: 100%; margin: 16px 0 24px 0; justify-content: center;">
            <div style="display: flex; align-items: center; width: 80%; justify-content: space-between;">
              <el-button v-if="active > 0" @click="preStep()" type="primary" circle style="margin: 0 8px;">
                <i class="el-icon-arrow-left" />
              </el-button>
              <div style="flex: 1; height: 2px; background: #e4e7ed; margin: 0 8px;"></div>
              <el-button v-if="active < 3" @click="nextStep()" type="success" circle style="margin: 0 8px;">
                <i class="el-icon-arrow-right" />
              </el-button>
            </div>
          </div>
          <!--		Next Step or Pre Step		-->
          <!-- <div style="display: flex; align-items: center; margin-top: 1rem;">
            <div style="display: flex; justify-content: center; flex-grow: 1">
              <el-button @click="preStep()" :disabled="active===0" type="primary" plain style="margin: 0 10px;">Pre step
              </el-button>
              <el-button @click="nextStep()" type="success" plain v-if="active !== 4" style="margin: 0 10px;">Next step
              </el-button>
              <el-button type="success" @click="submitForm()" v-if="active === 4" style="margin: 0 10px;">Submit
              </el-button>
            </div>
            <!--					<el-button type="primary" @click="preview()" v-if="active === 4" style="margin-left: auto">结构方程模型-->
            <!--					</el-button>-->
          <!-- </div> -->
        </el-card>
        <!--		结构方程模型  	-->
        <el-card style="width: 100%;height: 98%;" v-show="this.active === 4">
          <div style="display: flex; flex-direction: column; width: 100%">
            <div style="display: flex; justify-content: center; width: 100%">
              <el-steps style="width: 50%; max-width: 800px" :active="active" finish-status="success">
                <el-step title="实验目标设计"/>
                <el-step title="影响因素设计"/>
                <el-step title="响应变量设计"/>
                <el-step title="实验方法选择"/>
              </el-steps>
            </div>
            <div style="display: flex; align-items: center; width: 100%; justify-content: center; margin-top: 2rem">
              <span class="exp-title" style="font-size: 22px">结构方程模型</span>
            </div>
            <div style="width: 100%">
              <structural-equation :key="structuralEquationDialogKey" @schemePreview="schemePreview"></structural-equation>
            </div>
            <div style="display: flex; align-items: center; margin-top: 1rem;">
              <div style="display: flex; justify-content: center; flex-grow: 1">
                <el-button @click="preStep()" :disabled="active===0" type="primary" plain style="margin: 0 10px;">Pre step
                </el-button>
                <el-button @click="nextStep()" type="success" plain v-if="active !== 4" style="margin: 0 10px;">Next step
                </el-button>
                <el-button type="success" @click="submitForm()" v-if="active === 4" style="margin: 0 10px;">Submit
                </el-button>
              </div>
            </div>
          </div>
        </el-card>
        <el-dialog v-model="experimentGoalDialogVisible" title="实验目标设计" center width="60%">
          <div style="max-height: 65vh">
            <el-scrollbar style="width: 100%; display: inline" max-height="65vh">
              <el-card style="width: 100%">
                <template #header>
                  <div class="exp-goal-card-head">
                    <span>敏感性分析</span>
                  </div>
                </template>
                <div style="display: flex; width: 100%">
                  <div>变量选择：
                    <el-select v-model="sensitivityVarSelection" placeholder="请选择变量">
                      <el-option
                          v-for="item in sensitivityVarOptions"
                          :key="item.value"
                          :label="item.label"
                          :value="item.value"
                      />
                    </el-select>
                  </div>
                </div>
              </el-card>
              <el-card style="width: 100%; margin-top: 1rem">
                <template #header>
                  <div class="exp-goal-card-head">
                    <span>稳健性分析</span>
                  </div>
                </template>
                <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
                <template #footer>Footer content</template>
              </el-card>
              <el-card style="width: 100%; margin-top: 1rem">
                <template #header>
                  <div class="exp-goal-card-head">
                    <span>离散分析</span>
                  </div>
                </template>
                <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
                <template #footer>Footer content</template>
              </el-card>
              <el-card style="width: 100%; margin-top: 1rem">
                <template #header>
                  <div class="exp-goal-card-head">
                    <span>模型分析</span>
                  </div>
                </template>
                <p v-for="o in 4" :key="o" class="text item">{{ 'List item ' + o }}</p>
                <template #footer>Footer content</template>
              </el-card>
            </el-scrollbar>
          </div>
        </el-dialog>
        <el-dialog v-model="responseDialogVisible" title="响应变量设计" center width="40%">
          <div style="height: 500px">
            <el-checkbox v-model="selectAll" style="display: block"
                         :indeterminate="isIndeterminate" @change="responseSelectAllChange">全选
            </el-checkbox>
            <el-checkbox-group v-model="checkList" @change="responseSelectOptionChange">
              <el-checkbox style="display: block; margin-top: 20px"
                           v-for="(option, index) in checkboxOptions" :key="option.key" :label="option.label">
                {{ option.label }}
                <span class="formula-font">{{ formulaList[index] }}</span>
              </el-checkbox>
            </el-checkbox-group>
          </div>
          <template #footer>
            <div class="dialog-footer" style="display: flex; justify-content: flex-end; margin-right: 2rem">
              <el-button type="success" @click="responseConfirm()">确认</el-button>
              <el-button @click="responseDialogVisible = false">取消</el-button>
            </div>
          </template>
        </el-dialog>
        <el-dialog v-model="formulaDialogVisible" title="公式编辑" center width="80%" top="50px">
          <formula-editor ref="formulaEditor" @msg-from-formulaEdita="receiveMsgFromFormulaEdit"
                          :key="formulaComponentKey" :formula-data="formulaData"></formula-editor>
        </el-dialog>
        <!-- 预览最终生成的实验结果 -->
        <el-dialog v-if="finalShowReview === 1" v-model="expVisible" title="实验设计方法-预览" center width="60%">
          <div>
            <div style="font-family: Arial; font-size: 15px; margin-bottom: 10px">实验目标：目标1</div>
            <div style="font-family: Arial; font-size: 15px; margin-bottom: 10px">实验方法：{{ this.expName }}</div>
            <!--    显示响应变量和影响因素    -->
            <el-table :data="tableData" stripe style="width: 100%">
              <el-table-column prop="first" :label="'agent数量比例：' + formattedClassNames" width="300"/>
              <el-table-column prop="second" label="组织结构" width="180" :formatter="networkTypeFormatter"/>
              <el-table-column prop="third" label="干预策略" :formatter="moneyTypeFormatter"/>
            </el-table>
          </div>
        </el-dialog>
        <el-dialog v-if="finalShowReview === 2" v-model="expVisible" title="实验设计方法-预览" center width="60%">
          <div>
            <div style="font-family: Arial; font-size: 15px; margin-bottom: 10px">实验目标:组织结构实验</div>
            <div style="font-family: Arial; font-size: 15px; margin-bottom: 10px">实验方法：{{ this.expName }}</div>
            <!--    显示响应变量和影响因素    -->
            <el-table :data="tableDataNX" stripe style="width: 100%">
              <el-table-column prop="second" :label="'组织结构：'" width="300"/>
              <el-table-column prop="third" label="概率" width="180" />
              <el-table-column prop="fourth" label="初始边数"/>
              <el-table-column prop="fifth" label="初始邻居" />
              <el-table-column prop="sixth" label="节点度数"/>
            </el-table>
          </div>
        </el-dialog>
        <el-dialog v-model="influenceDialogVisible" title="影响因素设计" @opened="influenceDialogOpen()"
                   @close="influenceDialogClose" center width="60%">
          <div>
            <el-scrollbar ref="scrollbar" max-height="500px">
              <div v-if="influenceShowOrd === 1">
                <el-form v-model="form" ref="form" :rules="rules">
                  <!--			智能主体实验				-->
                  <el-card style="width: 90%; margin-left: 5%">
                    <template #header>
                      <div style="font-size: 18px; font-weight: bold;">
                        <span>智能主体实验</span>
                      </div>
                    </template>
                    <div>
                      <span>智能主体选择： &nbsp;</span>
                      <el-select v-model="agentSelection" placeholder="请根据需求选择需要对比的Agent类型（可多选）"
                                 multiple clearable style="width: 60%">
                        <el-option
                            v-for="item in agentOption"
                            :key="item.value"
                            :value="item.label"
                            :label="item.label"/>
                      </el-select>
                    </div>
                  </el-card>
                </el-form>
              </div>
              <div v-if="influenceShowOrd === 2">
                <el-form v-model="form" ref="form" :rules="rules">
                  <el-card style="width: 90%; margin-left: 5%">
                    <template #header>
                      <div style="font-size: 18px; font-weight: bold;">
                        <span>组织结构实验</span>
                      </div>
                    </template>
                    <el-card >
                      <div>agent协作</div>
                      <hr style="border: none; border-top: 3px solid black;">
                      <el-tabs v-model="activeNamenx" @tab-click="handleClick" class="custom-tabs">
                        <el-tab-pane label="随机网络" name="1"></el-tab-pane>
                        <el-tab-pane label="无标度网络" name="2"></el-tab-pane>
                        <el-tab-pane label="小世界网络" name="3"></el-tab-pane>
                        <el-tab-pane label="规则网络" name="4"></el-tab-pane>
                        <el-tab-pane label="无网络" name="5"></el-tab-pane>
                      </el-tabs>
                      <div v-if="activeNamenx === '1'">
                        <div style="display: flex;  width: 100%">
                          <span style="margin-bottom: 5px; display: block;">概率：</span>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最小值：</span>
                          <el-input-number label="最小值" v-model="nxData.erprobMin" :min="0" :max="1" :step="0.01"/>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最大值：</span>
                          <el-input-number label="最小值" v-model="nxData.erprobMax" :min="0" :max="1" :step="0.01" />&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">步长：</span>
                          <el-input-number label="最小值" v-model="nxData.erprobStep" :min="0" :max="1" :step="0.1" />&nbsp; &nbsp;&nbsp;
                          <el-button type="primary" @click="erprobGet">确认</el-button>
                        </div>

                      </div>
                      <div v-if="activeNamenx === '4'">
                        <div style="display: flex;  width: 100%">
                          <span style="margin-bottom: 5px; display: block;">节点度数：</span>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最小值：</span>
                          <el-input-number label="最小值" v-model="nxData.rgdegreeMin" :min="0" :max="10" :step="1"/>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最大值：</span>
                          <el-input-number label="最小值" v-model="nxData.rgdegreeMax" :min="0" :max="10" :step="1" />&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">步长：</span>
                          <el-input-number label="最小值" v-model="nxData.rgdegreeStep" :min="0" :max="1" :step="1" />&nbsp; &nbsp;&nbsp;
                          <el-button type="primary" @click="rgdegreeGet()">确认</el-button>
                        </div>


                      </div>
                      <div v-if="activeNamenx === '2'">
                        <div style="display: flex;  width: 100%">
                          <span style="margin-bottom: 5px; display: block;">BA_add_deges：</span>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最小值：</span>
                          <el-input-number label="最小值" v-model="nxData.baEdgeMin" :min="0" :max="10" :step="1"/>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最大值：</span>
                          <el-input-number label="最小值" v-model="nxData.baEdgeMax" :min="0" :max="10" :step="1" />&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">步长：</span>
                          <el-input-number label="最小值" v-model="nxData.baEdgeStep" :min="0" :max="1" :step="1" />&nbsp; &nbsp;&nbsp;
                          <el-button type="primary" @click="baEdgeGet()">确认</el-button>
                        </div>

                      </div>
                      <div v-if="activeNamenx === '3'">
                        <div style="display: flex;  width: 100%">
                          <span style="margin-bottom: 5px; display: block;">初始邻居：</span>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最小值：</span>
                          <el-input-number label="最小值" v-model="nxData.wsneighborsMin" :min="0" :max="10" :step="1"/>&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">最大值：</span>
                          <el-input-number label="最小值" v-model="nxData.wsneighborsMax" :min="0" :max="10" :step="1" />&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;
                          <span style="margin-bottom: 5px; display: block;">步长：</span>
                          <el-input-number label="最小值" v-model="nxData.wsneighborsStep" :min="0" :max="1" :step="1" />&nbsp; &nbsp;&nbsp;
                          <el-button type="primary" @click="wsneighborsGet()">确认</el-button>
                        </div>

                      </div>
                      <div v-if="activeNamenx === '5'">
                        <el-button type="primary" style="margin-right: 20px; margin-top: 20px" @click="graphSend()">确认</el-button>
                      </div>
                      <div></div>
                    </el-card>
                  </el-card>
                </el-form>
              </div>
              <div v-if="influenceShowOrd === 3">
                <el-form v-model="form" ref="form" :rules="rules">
                  <el-card style="width: 90%; margin-left: 5%">
                    <template #header>
                      <div style="font-size: 18px; font-weight: bold;">
                        <span>调控策略实验</span>
                      </div>
                    </template>
                    <div>
                      <span>干预调控方式： &nbsp;</span>
                      <el-select v-model="moneyTypeSelection" value-key="value" @change="searchSelect"
                                 placeholder="请根据需求选择干预调控方式（可多选）"
                                 multiple clearable style="width: 50%">
                        <el-option
                            v-for="item in moneyTypeOption"
                            :key="item.value"
                            :value="item.value"
                            :label="item.label"/>
                      </el-select>
                    </div>
                    <div style="display: flex; justify-content: center; padding-top: 20px;">
                      <el-button type="primary"
                                 @click="this.$router.push({path:'/home/smartCity/regulationOpt', query: {type: this.multipleType}})"
                                 style="margin-right: 20px;">详细算法
                      </el-button>
                    </div>
                  </el-card>
                </el-form>
              </div>
            </el-scrollbar>
          </div>
          <template #footer>
            <div class="dialog-footer" style="display: flex; justify-content: flex-end; margin-right: 2rem">
              <el-button type="success" @click="expSend()">确认</el-button>
              <el-button @click="influenceDialogVisible = false">取消</el-button>
            </div>
          </template>
        </el-dialog>
        <el-dialog v-model="presetDialogVisible" title="选择实验预设方案" center width="50%" :close-on-click-modal="false" :show-close="true">
          <div style="display: flex; gap: 1.5rem; justify-content: center;">
            <el-card v-for="(preset, idx) in presetSchemes" :key="idx" style="width: 260px; cursor: pointer; border: 2px solid #409EFF;" @click="selectPresetScheme(idx)">
              <div style="font-weight: bold; font-size: 18px; color: #409EFF; margin-bottom: 10px;">{{ preset.name }}</div>
              <div style="margin-bottom: 8px;"><b>目标：</b>{{ preset.goal.goal_name }}</div>
              <div style="margin-bottom: 8px;"><b>方法：</b>{{ preset.goal.goal_content_name.join(' / ') }}</div>
              <div style="margin-bottom: 8px;"><b>影响因素：</b>{{ preset.influenceNames.join('、') }}</div>
              <div style="margin-bottom: 8px;"><b>响应变量：</b>{{ preset.responseNames.join('、') }}</div>
              <div><b>实验方法：</b>{{ preset.methodNames.join('、') }}</div>
            </el-card>
          </div>
        </el-dialog>
      </div>
    </div>
  </div>
</template>

<script>
import {ref, reactive, unref} from 'vue';
import {UploadFilled} from "@element-plus/icons";
import FishBoneChart from "../../components/FishBoneChart.vue";
import ExperimentContent from "../../components/ExperimentContent.vue";
import FormulaEditor from "../../components/FormulaEditor.vue";
import StructuralEquation from "../../components/StructuralEquation.vue";
import request from "../../utils/request";
import {ElMessage} from "element-plus";
import ChatWithAgentD from '@/components/ChatWithAgentD.vue';

export default {
  name: "PowerGame_ExperimentDesign",
  components: {ExperimentContent, UploadFilled, FishBoneChart, FormulaEditor, StructuralEquation, ChatWithAgentD},
  setup() {
    const activeNamenx = ref('0');
    let tableData = [
      {
        first: '(1: 0)',
        second: '随机网络',
        third: '工资',
      },
      {
        first: '(1: 0)',
        second: '随机网络',
        third: '工资',
      },
      {
        first: '(1: 0)',
        second: '随机网络',
        third: '工资',
      }
    ]
    let tableDataNX = [
    ]
    const sensitivityVarSelection = ref('')
    const sensitivityVarOptions = [
      {value: 1, label: '变量1'},
      {value: 2, label: '变量2'},
      {value: 3, label: '变量3'},
    ]
    const intelligentAgentSelection = ref('')
    const intelligentAgentOptions = [
      {value: 1, label: '智能程度'},
      {value: 2, label: '智能体数量'},
      {value: 3, label: '智能体分布'},
      {value: 4, label: '智能程度占比'},
    ]
    const prob = ref(0);
    const WS_init_neighbors = ref(0);
    const BA_add_edges = ref(0);
    const RG_init_degree = ref(0)
    const classNames = ['LLM', '强化学习', '模仿学习', '规则式', 'LLM', '强化学习', '模仿学习', '规则式', 'LLM', '强化学习', '模仿学习', '规则式']
    const socket = new WebSocket('ws://localhost:8080/ws')
    socket.onopen = () => {
      socket.send(JSON.stringify({event: 'class_name'}))
    }
    socket.onmessage = (evt) => {
      let received = JSON.parse(evt.data)
      agentSelection.value = []
      if (received.uri === 'className') {
        classNames.length = 0
        classNames.push(...received.data);
        for (var i = 0; i < received.data.length; ++i) {
          agentOption.push({value: i, label: received.data[i]})
          agentSelection.value.push(received.data[i])
        }
        console.log(agentOption)
      } else if (received.uri === 'exp_ans') {
        console.log('test change exp info')
        tableData.length = 0
        tableData.push(...received.data)
        console.log(tableData)
      }
    }
    const form = reactive({
      moneyType: '0',
      moneyRatio: 0.5
    })
    const visibleNum = ref(0);
    const activeName = ref('0');
    const isIndeterminate = ref(false)
    const props = {
      expandTrigger: 'hover'
    };
    const active = ref(0)
    const selectAll = ref(false)
    const preCheckList = ref([])
    const checkList = ref([])
    const influenceCheckBoxes = ref([])
    const agentNumCheckBox = ref(false)
    const checkboxOptions = [
      {key: 'individualUtility', label: '正面量化评估', index: 0},
      {key: 'systemUtility', label: '负面量化评估', index: 1},
      {key: 'valueEntropy', label: '态势计算', index: 2},
      {key: 'productivity', label: '博弈策略收益', index: 3},
    ]
    const classDefaultValueMin = ref(Array(12).fill(0));
    const classDefaultValueMax = ref(Array(12).fill(10));

    const valueClassMin = ref(Array(12).fill(0));
    const valueClassMax = ref(Array(12).fill(10));
    const influenceCheckboxGroup = ref([])
    const agentNumCheck = ref(false)
    const humanMachineRatioCheck = ref(false)

    const agentCooperationSelection = ref([1, 2])
    const agentSelection = ref('')
    const collaborativeNetOption = [
      {value: 1, label: '随机网络'},
      {value: 2, label: '规则网络'},
      {value: 3, label: '无标度网络'},
      {value: 4, label: '小世界网络'},
      {value: 5, label: '无网络结构'}
    ]
    const agentOption = []
    const moneyTypeSelection = ref([1, 2])
    const moneyTypeOption = [
      {value: 1, label: '工资'},
      {value: 2, label: '派单'},
      {value: 3, label: '重定向'},
    ]
    return {
      props, active, selectAll, checkList, preCheckList,
      checkboxOptions, isIndeterminate, influenceCheckBoxes, agentNumCheckBox,
      influenceCheckboxGroup, agentNumCheck, humanMachineRatioCheck,
      activeName, visibleNum, classNames, classDefaultValueMin, classDefaultValueMax,
      valueClassMin, valueClassMax, form, socket, activeNamenx,
      prob, BA_add_edges, WS_init_neighbors, RG_init_degree,
      agentCooperationSelection, collaborativeNetOption,
      moneyTypeSelection, moneyTypeOption, agentSelection, agentOption, tableData, tableDataNX,
      sensitivityVarSelection, sensitivityVarOptions, intelligentAgentSelection, intelligentAgentOptions,
    }
  },
  data() {
    return {
      imageMap : {
        'agent个体效能': '../../assets/images/fishHead.png',
        '系统效能': '../../assets/images/fishHead.png',
        '价值熵': '../../assets/images/entropy.png',
        '生产力': '../../assets/images/fishHead.png',
      },
      experimentGoal: null,
      finalShowReview :1,
      nxData: { //对应网络结构实验
        erprobMin: 0.0,
        erprobMax: 1.0,
        erprobStep: 0.1,

        baEdgeMin: 0,
        baEdgeMax: 10,
        baEdgeStep: 1,

        wsneighborsMin: 0,
        wsneighborsMax: 10,
        wsneighborsStep: 1,

        rgdegreeMin: 0,
        rgdegreeMax: 10,
        rgdegreeStep: 1,
      },
      erProbNums: [],
      baEdgeNums: [],
      wsneighborsNums: [],
      rgdegreeNums: [],
      nxNums: [],
      expName: '',
      influenceDialogVisible: false,
      influenceShowOrd: 1,
      influenceFactors: ['intelligent_agent', 'control_strategy', 'organization_structure'],
      influenceFactorSelection: [false, false, false,],
      responseVars: ['individual_utility', 'system_utility', 'value_entropy', 'productivity'],
      responseVarSelection: [false, false, false, false],
      experimentMethods: ['certainExperiment', 'randomExperiment'],
      experimentMethodSelection: [false, false],
      experimentMethodName: null,
      experimentMethodNameSelection: [],

      experimentGoalDialogVisible: false,
      responseDialogVisible: false,
      formulaDialogVisible: false,
      expVisible: false,
      checkIndex: 0,
      tailName: '',
      form: {
        agentNum: 100,
        agentNumLower: 10,
        agentNumUpper: 1000,
        agentNumStepLen: 10,

        humanMachineRatio: 2,
        humanMachineRatioLower: 0.1,
        humanMachineRatioUpper: 10,
        humanMachineRatioStepLen: 0.5,
      },
      rules: {},
      multipleType: [],
      formulaComponentKey: 0,
      formulaData: {
        formulaName: '',
        varList: [
          {value: 1, type: 2, label: '效能', enLabel: 'efficacy'},
          {value: 2, type: 2, label: 'Agent数量', enLabel: 'agentNum'},
          {value: 3, type: 2, label: 'Gov数量', enLabel: 'govNum'},
          {value: 4, type: 2, label: 'Agent工作效率', enLabel: 'agentEfficacy'},
          {value: 5, type: 2, label: '订单难度', enLabel: 'orderDiff'},
          {value: 6, type: 2, label: '订单数量', enLabel: 'orderNum'},
          {value: 7, type: 2, label: '订单到达率', enLabel: 'orderArrivalRate'},
          {value: 8, type: 2, label: '个体效能', enLabel: 'individualUtility'},
          {value: 9, type: 2, label: '收益', enLabel: 'reward'},
          {value: 10, type: 2, label: '成本', enLabel: 'cost'},
          {value: 11, type: 2, label: '系统效能', enLabel: 'systemUtility'},
          {value: 12, type: 2, label: '价值熵', enLabel: 'valueEntropy'},
          {value: 13, type: 2, label: '生产力', enLabel: 'productivity'},
          {value: 14, type: 2, label: 'Var7', enLabel: 'var7'},
          {value: 15, type: 2, label: 'Var8', enLabel: 'var8'},
          {value: 16, type: 2, label: 'Var9', enLabel: 'var9'},
          {value: 17, type: 2, label: 'Var10', enLabel: 'var10'},
          {value: 18, type: 2, label: 'Var11', enLabel: 'var11'},
        ],
        symbolList: [
          {value: 1, label: '+'},
          {value: 2, label: '-'},
          {value: 3, label: '*'},
          {value: 4, label: '/'},
          {value: 5, label: '('},
          {value: 6, label: ')'},
          {value: 7, label: '^'},
          {value: 8, label: '='},
          {value: 9, label: 'log'},
          {value: 10, label: 'ln'},
          {value: 11, label: '∑'},
          {value: 12, label: '∏'},
        ],
        numList: [
          {value: 1, label: '1'},
          {value: 2, label: '2'},
          {value: 3, label: '3'},
          {value: 4, label: '4'},
          {value: 5, label: '5'},
          {value: 6, label: '6'},
          {value: 7, label: '7'},
          {value: 8, label: '8'},
          {value: 9, label: '9'},
          {value: 0, label: '0'},
        ],
      },
      formulaList: ['', '', '', ''],
      structuralEquationDialogKey: 0,
      presetDialogVisible: false, // 初始不弹出
      chatDialogVisible: false,
      presetSchemes: [
        {
          name: '方案一：降水对早高峰交通流量影响',
          goal: {
            goal_name: '分析降水对早高峰交通流量的影响',
            goal_content_name: ['历史交通数据分析', '交通流量变化']
          },
          influenceNames: ['降水强度', '时段类型', '道路类型'],
          responseNames: ['交通流量', '平均车速'],
          methodNames: ['描述性分析', '对比实验'],
          influenceSelection: [true, false, true],
          responseSelection: [true, true, false, false],
          methodSelection: [true, false],
          methodName: '描述性分析',
          methodNameSelection: ['历史交通数据分析']
        },
        {
          name: '方案二：降水对事故率的影响',
          goal: {
            goal_name: '评估降水对城市道路事故率的影响',
            goal_content_name: ['事故率分析', '多策略对比']
          },
          influenceNames: ['降水类型', '道路类型'],
          responseNames: ['事故率'],
          methodNames: ['对比实验', '回归分析'],
          influenceSelection: [false, true, true],
          responseSelection: [false, false, true, false],
          methodSelection: [false, true],
          methodName: '对比实验',
          methodNameSelection: ['事故率分析']
        },
        {
          name: '方案三：降水对交通延误的影响',
          goal: {
            goal_name: '探究降水对城市交通延误的影响',
            goal_content_name: ['延误时长分析', '预测建模']
          },
          influenceNames: ['降水量', '时段类型'],
          responseNames: ['延误时长'],
          methodNames: ['预测建模', '回归分析'],
          influenceSelection: [true, true, false],
          responseSelection: [false, false, false, true],
          methodSelection: [false, true],
          methodName: '预测建模',
          methodNameSelection: ['延误时长分析']
        }
      ],
      influenceFactorsDetail: [], // 新增：影响因素综合结果
      responseVarsDetail: [], // 新增：响应变量综合结果
    }
  },
  mounted() {
    this.$refs.fishBoneChart.$watch('influenceVisible', (newValue, oldValue) => {
      if (newValue === true) {
        this.influenceDialogVisible = true
      }
    })
    this.$refs.fishBoneChart.$watch('influenceShowOrd', (newValue, oldValue) => {
      this.influenceShowOrd = newValue
    })
    const goal = localStorage.getItem('experimentGoal');
    if (goal) {
      this.experimentGoal = JSON.parse(goal);
    }
    // 恢复影响因素选择
    const influence = localStorage.getItem('influenceFactorSelection');
    if (influence) {
      this.influenceFactorSelection = JSON.parse(influence);
    }
    // 恢复响应变量选择
    const response = localStorage.getItem('responseVarSelection');
    if (response) {
      this.responseVarSelection = JSON.parse(response);
    }
    // 恢复实验方法选择
    const method = localStorage.getItem('experimentMethodSelection');
    if (method) {
      this.experimentMethodSelection = JSON.parse(method);
    }
    // 恢复实验方法名称
    const methodName = localStorage.getItem('experimentMethodName');
    if (methodName) {
      this.experimentMethodName = methodName;
    }
    // 只在首次进入时弹出预设方案选择
    if (!localStorage.getItem('rainCityPresetSelected')) {
      this.presetDialogVisible = true;
    }
    // 自动读取影响因素综合结果
    const influenceDetail = localStorage.getItem('influenceFactorsDetail');
    if (influenceDetail) {
      try {
        this.influenceFactorsDetail = JSON.parse(influenceDetail);
      } catch (e) {
        this.influenceFactorsDetail = [];
      }
    }
    // 自动读取响应变量综合结果
    const responseDetail = localStorage.getItem('responseVarsDetail');
    if (responseDetail) {
      try {
        this.responseVarsDetail = JSON.parse(responseDetail);
      } catch (e) {
        this.responseVarsDetail = [];
      }
    }
  },
  computed: {
    // 使用计算属性来格式化classNames数组
    formattedClassNames() {
      const uniqueClassNames = Array.from(new Set(this.classNames));
      return `(${uniqueClassNames.join(':')})`;
    },
  },
  methods: {
    getImageUrl(option) {
      const imageMap = {
        'agent个体效能': '../../assets/images/fishHead.png',
        '系统效能': '../../assets/images/fishHead.png',
        '价值熵': '../../assets/images/entropy.png',
        '生产力': '../../assets/images/fishHead.png',
      };
      console.log('info', imageMap[option], option)
      return '../../assets/images/fishTail.png'; // 如果没有找到对应的图片，可以返回一个默认图片
    },
    erprobGet(){

      for (var i = this.nxData.erprobMin; i < this.nxData.erprobMax; i += this.nxData.erprobStep) {
        let roundedNumber = Math.round(i * 100) / 100;
        this.erProbNums.push(roundedNumber)
      }
      console.log(this.erProbNums)
      this.graphSend()
    },
    baEdgeGet(){
      for (var i = this.nxData.baEdgeMin; i < this.nxData.baEdgeMax; i += this.nxData.baEdgeStep) {
        let roundedNumber = Math.round(i * 100) / 100;
        this.baEdgeNums.push(roundedNumber)
      }
      console.log(this.baEdgeNums)
      this.graphSend()
    },
    wsneighborsGet(){
      for (var i = this.nxData.wsneighborsMin; i < this.nxData.wsneighborsMax; i += this.nxData.wsneighborsStep) {
        let roundedNumber = Math.round(i * 100) / 100;
        this.wsneighborsNums.push(roundedNumber)
      }
      console.log(this.wsneighborsNums)
      this.graphSend()
    },
    rgdegreeGet(){
      for (var i = this.nxData.rgdegreeMin; i < this.nxData.rgdegreeMax; i += this.nxData.rgdegreeStep) {
        let roundedNumber = Math.round(i * 100) / 100;
        this.rgdegreeNums.push(roundedNumber)
      }
      console.log(this.rgdegreeNums)
      this.graphSend()
    },
    graphSend(){
      var graph_list = ['ER', 'BA', 'WS', 'RG', 'None']
      var params_list = []
      if (this.activeNamenx == "1") {
        for (let item of this.erProbNums) {
          var nums = ['ER', item, 2, 2, 2]
          this.nxNums.push(nums)
          this.tableDataNX.push({
            first: '(1: 0)',
            second: '随机网络',
            third: item,
            fourth: '',
            fifth: '',
            sixth: ''
          })
        }
        // params_list = [this.valueAgent, this.prob]
      } else if (this.activeNamenx == '2') {
        for (let item of this.baEdgeNums) {
          var nums = ['BA', 0.8, item, 2, 2]
          this.nxNums.push(nums)
          this.tableDataNX.push({
            first: '(1: 0)',
            second: '无标度网络',
            third: '',
            fourth: item,
            fifth: '',
            sixth: ''
          })
        }
        // params_list = [this.valueAgent, this.BA_add_edges]
      } else if (this.activeNamenx == '3') {
        for (let item of this.wsneighborsNums) {
          var nums = ['WS', 0.8, 2, item, 2]
          this.nxNums.push(nums)
          this.tableDataNX.push({
            first: '(1: 0)',
            second: '小世界网络',
            third: '',
            fourth: '',
            fifth: item,
            sixth: ''
          })
        }
        // params_list = [this.valueAgent, this.WS_init_neighbors, this.prob]
      } else if (this.activeNamenx == '4') {
        for (let item of this.wsneighborsNums) {
          var nums = ['RG', 0.8, 2, 2, item]
          this.nxNums.push(nums)
          this.tableDataNX.push({
            first: '(1: 0)',
            second: '规则网络',
            third: '',
            fourth: '',
            fifth: '',
            sixth: item
          })
        }
        // params_list = [this.valueAgent, this.RG_init_degree]
      } else {
        this.nxNums.push(['None', 0, 2, 2, 3])
        this.tableDataNX.push({
          first: '(1: 0)',
          second: '无网络',
          third: '',
          fourth: '',
          fifth: '',
          sixth: ''
        })
        // params_list = [this.valueAgent]
      }
      console.log(this.tableDataNX)
      // this.socket.send(JSON.stringify({event: 'graph_info', nx: graph_list[parseInt(this.activeName) - 1], params: params_list}))
    },
    moneyTypeFormatter(row, column, cellValue) {
      const option = this.moneyTypeOption.find(item => item.value === cellValue);
      return option ? option.label : '';
    },
    networkTypeFormatter(row, column, cellValue) {
      const option = this.collaborativeNetOption.find(item => item.value === cellValue);
      return option ? option.label : '';
    },
    expSend() {
      console.log(this.socket)
      if(this.valuesClass) {
        if(this.influenceShowOrd === 2) {
          this.finalShowReview = 2;
          this.socket.send(JSON.stringify({event: 'exp_nx', nx: this.nxNums}))
        }
        let nums = this.valuesClass.map(unref);
        this.socket.send(JSON.stringify({
          event: 'exp_send',
          agent_num: nums,
          network: [this.activeName, this.prob, this.BA_add_edges, this.WS_init_neighbors, this.RG_init_degree]
        }))
      }
      this.influenceFactorSelection[this.influenceShowOrd - 1] = true;
    },
    responseConfirm() {
      for(let i = 0; i < this.checkboxOptions.length; i++){
        for(let j = 0; j < this.checkList.length; j++) {
          if(this.checkboxOptions[i].label === this.checkList[j]){
            this.responseVarSelection[i] = true;
            break;
          }
        }
      }
      this.responseDialogVisible = false;
    },
    influenceDialogOpen() {
      this.$refs.scrollbar.setScrollTop(0)
    },
    influenceDialogClose() {
      console.log('close')
      this.$refs.fishBoneChart.influenceVisible = false;
    },
    nextStep() {
      if (this.active++ > 3)
        this.active = 4
      this.expTab = this.active + 1 + '';
      this.structuralEquationDialogKey++;

      if(this.active === 2){
        request.post('/setExperimentParam', {
          'influence_factor': {
            'total': this.influenceFactors,
            'name': ['智能主体实验', '调控策略实验', '组织结构实验'],
            'selection': this.influenceFactorSelection,
          }
        }).then(res =>{
          console.log(res)
        })
      }
      else if(this.active === 3){
        request.post('/setExperimentParam', {
          response_var: {
            'total': this.responseVars,
            'name': ['个体效能', '系统效能', '价值熵', '生产力'],
            'selection': this.responseVarSelection,
          }
        }).then(res => {
          console.log(res)
        })
      }
      else if(this.active === 4){
        request.post('/setExperimentParam', {
          experiment_method: {
            'total': this.experimentMethods,
            'name': ['确定性实验设计', '非确定性实验设计'],
            'selection': this.experimentMethodSelection,
            'methods_name': this.experimentMethodName,
            'method_selection': this.experimentMethodNameSelection,
          }
        })
      }
    },
    preStep() {
      if (this.active-- < 1)
        this.active = 0
      this.expTab = this.active + 1 + ''
      this.structuralEquationDialogKey++;
    },
    submitForm() {
      console.log('click submit button')
      let experimentData = this.$refs.experimentContent.paramReturn();
      console.log(experimentData)
    },
    showResponseDialog() {
      this.responseDialogVisible = !this.responseDialogVisible;
    },
    enterExperimentGoalDesign() {
      this.$router.push('/home/rainCity/firstdesign')
    },
    enterInfluenceDesign() {
      this.$router.push('/home/rainCity/secondesign');
    },
    enterResponseDesign() {
      this.$router.push('/home/rainCity/thirdesign');
    },
    enterMethodDesign() {
      this.$router.push('/home/rainCity/firstdesign')
    },
    responseSelectAllChange(val) {
      console.log('response select all change', val)
      console.log('resss', this.checkList);
      this.checkList = [];
      if(val){
        for(let i = 0;i < this.checkboxOptions.length; i++)
          this.checkList.push(this.checkboxOptions[i].label);
      }
      console.log('checkList', this.checkList);
      this.isIndeterminate = false;
    },
    responseSelectOptionChange(value) {
      this.formulaComponentKey++;
      let label=''
      for(let i=0; i<value.length; i++)
        for(let j=0; j<this.preCheckList.length; j++)
          if(value[i]!==this.preCheckList[j].label)
            label=value[i];
      if(this.preCheckList.length === 0) label = value[0]
      for(let i = 0; i < this.checkboxOptions.length; i++)
        if(this.checkboxOptions[i].label === label)
          this.checkIndex = i
      if(value.length > this.preCheckList.length) {
        this.formulaDialogVisible = !this.formulaDialogVisible;
        this.formulaData.formulaName = value[value.length - 1];
      }
      let checkedCount = value.length
      this.selectAll = checkedCount === this.checkboxOptions.length
      this.isIndeterminate = checkedCount > 0 && checkedCount < this.checkboxOptions.length

      this.preCheckList = this.checkList
    },
    preview() {
      this.expVisible = !this.expVisible;
      console.log('test', this.agentSelection)
    },
    findLabelByPath(options, path) {
      let currentOptions = options;
      for (let i = 0; i < path.length; i++) {
        const index = path[i] - 1; // 由于数据结构的`value`从1开始，我们需要减1来得到正确的索引
        currentOptions = i === path.length - 1 ? currentOptions[index] : currentOptions[index].children;
      }
      return currentOptions.label;
    },
    certainSelectionChange(data){
      this.experimentMethodSelection = [true, false]
      this.experimentMethodNameSelection = data
    },
    uncertainSelectionChange(data){
      this.experimentMethods = [false, true]
      this.experimentMethodNameSelection = data
    },
    getExperimentMethodName(data){
      // 过滤掉包含 certainMethods/uncertainMethods 的对象，避免显示为 JSON
      if (data && typeof data === 'object' && (data.certainMethods || data.uncertainMethods)) {
        // 直接清空或给出友好提示
        this.experimentMethodName = '';
        return;
      }
      // 兼容多种数据结构，确保 experimentMethodName 为字符串
      if (Array.isArray(data)) {
        // 如果是 label 数组
        if (data.length && typeof data[0] === 'object' && data[0].label) {
          this.experimentMethodName = data.map(item => item.label).join(' / ');
        } else {
          this.experimentMethodName = data.join(' / ');
        }
      } else if (typeof data === 'object' && data !== null) {
        // 如果是对象，尝试取 label
        if (data.label) {
          this.experimentMethodName = data.label;
        } else if (data.value) {
          this.experimentMethodName = data.value;
        } else {
          this.experimentMethodName = '';
        }
      } else if (typeof data === 'string') {
        this.experimentMethodName = data;
      } else {
        this.experimentMethodName = '';
      }
    },
    callParamReturn() {
      if (this.$refs.experimentContent) {
        const params = this.$refs.experimentContent.paramReturn();
        if (params.random.length !== 0) {
          this.expName = this.findLabelByPath(params.randomData, params.random)
        } else {
          this.expName = this.findLabelByPath(params.certainData, params.certain)
        }
        console.log('check', params.random, params.certain);
      }
    },
    searchSelect(val) {
      this.multipleType = val
    },
    receiveMsgFromFormulaEdit(msg){
      console.log('receive from a', msg);
      this.formulaList[this.checkIndex] = msg;
      this.formulaDialogVisible = !this.formulaDialogVisible
    },
    schemePreview(data){
      this.preview();
    },
    openPresetDialog() {
      this.presetDialogVisible = true;
    },
    openChatDialog() {
      this.chatDialogVisible = true;
      this.presetDialogVisible = false;
    },
    onChatDialogClose() {
      // 对话框关闭后显示方案选择
      this.presetDialogVisible = true;
    },
    selectPresetScheme(idx) {
      const preset = this.presetSchemes[idx];
      this.experimentGoal = JSON.parse(JSON.stringify(preset.goal));
      this.influenceFactorSelection = [...preset.influenceSelection];
      this.responseVarSelection = [...preset.responseSelection];
      this.experimentMethodSelection = [...preset.methodSelection];
      this.experimentMethodName = preset.methodName;
      this.experimentMethodNameSelection = [...preset.methodNameSelection];
      this.presetDialogVisible = false;
      localStorage.setItem('rainCityPresetSelected', '1'); // 标记已选
    },
    autoFinishByAgent() {
      this.chatDialogVisible = false;
      this.presetDialogVisible = true;
    },
  },
  watch: {
    influenceFactorSelection: {
      handler(val) {
        localStorage.setItem('influenceFactorSelection', JSON.stringify(val));
      },
      deep: true
    },
    responseVarSelection: {
      handler(val) {
        localStorage.setItem('responseVarSelection', JSON.stringify(val));
      },
      deep: true
    },
    experimentMethodSelection: {
      handler(val) {
        localStorage.setItem('experimentMethodSelection', JSON.stringify(val));
      },
      deep: true
    },
    experimentMethodName(val) {
      localStorage.setItem('experimentMethodName', val);
    }
  },
}
</script>

<style scoped>
.experiment-design-outer {
  width: 100vw;
  min-width: 1200px;
  background: #f7f9fa;
  min-height: 100vh;
  padding: 0;
}
.experiment-design-header {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(64,158,255,0.08);
  padding: 18px 32px 12px 32px;
  margin-bottom: 18px;
}
.exp-title {
  display: flex;
  justify-content: center;
  font-size: 18px;
  color: #333;
  font-style: normal;
  font-weight: bolder;
  font-family: 'sans-serif';
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.el-cascader {
  width: 30%;
  min-width: 200px;
}

.input-with-select .el-input-group__prepend {
  background-color: gray;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(177, 179, 184, 0.5); /* 半透明背景 */
  z-index: 999; /* 确保遮罩层位于el-card上方 */
}

.overlay-success {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(209, 237, 196, 0.5); /* 半透明背景 */
  z-index: 999; /* 确保遮罩层位于el-card上方 */
}

.slider-container {
  display: flex; /* 将内容水平排列 */
  align-items: center; /* 垂直居中对齐 */
  margin-bottom: 5px; /* 调整元素之间的间距 */
}

.exp-goal-card-head {
  font-size: 18px;
  font-family: ui-serif;
  font-weight: bold;
}

:deep(.default-card.el-card) {
  background-color: #f4f4f5;
  margin-top: 1rem;
  width: 90%;
  margin-left: 5%
}

:deep(.miniInputNumber.el-input-number) {
  width: 150px;
}
.formula-font{
  color: black;
  font-family: 'KaTeX_Main', serif;
  font-size: 20px;
  line-height: 1.2;
  font-style: italic;
}
</style>