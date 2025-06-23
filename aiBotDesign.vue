<template>
	<div style="width: 99%; min-width:1200px; display: flex">
		<div style="width: 99%; min-width: 1200px; display: inline;">
			<el-card style="width: 100%;height: 98%">
				<div style="display: flex; flex-direction: column; height: 100%; width: 100%; font-size: 20px; margin-top: 1rem;">
					<div style="font-family: 黑体;font-weight: bold;font-size: 22px; margin-top: 8px">主体设计</div>
				</div>
				<div>
					<el-divider></el-divider>
				</div>
				<div style="display: flex; height: 100%; width: 100%;margin-top:50px">
					<!--	左侧卡片稍窄   -->
					<el-card style="width: 25%; height: 80vh; margin-right: 10px;">
            <template #header>
              <span class="title-font">我的Agent</span>
            </template>
            <div style="display: flex; flex-direction: column; flex-wrap: wrap; justify-content: center; gap: 10px;">
              <el-card v-for="(item, index) in classInfo" :key="index" shadow="hover"
                       class="agent-card-pos" @click="cardClick(index)"
                       :style="{width: cardIsExpand[index] ? '100%' : '343px', background: cardIsExpand[index] ? 'rgb(243.9, 244.2, 244.8)' : '#FFF'}">
                <div style="display: flex; width: 100%; height: 145px; flex-direction: column; justify-content: space-between"
                    v-if="!cardIsExpand[index]">
                  <el-image :src="item.imgUrl" style="width: 80%; height: 100px;margin-left: 10%;" fit="contain"></el-image>
                  <span style="font-size: 16px; font-weight: bold; text-align: center;">{{ item.name }}</span>
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
					<!--	右侧卡片稍宽  	-->
					<el-card style="width: 75%; min-height: 500px;">
						<ChatWithAgent />
						<template #header>
							您正在设计Agent：
							<strong style="font-size: 20px;">
								{{ currentAgentName }}
							</strong>
						</template>
						<div style="display: flex; justify-content: center; width: 100%">
							<el-steps style="width: 73%; " :active="active" finish-status="success">
								<el-step title="特征集合"/>
								<el-step title="感知模块"/>
								<el-step title="大脑模块"/>
								<el-step title="行为模块"/>
							</el-steps>
						</div>
						<div style="display: flex; justify-content: center; width: 100%">
							<div style="display: flex; height: 100%;margin-top: 1rem; width: 80%;">
								<!--	特征集合设计	-->
								<div style="display: inline-block; position: relative; width: 24%">
									<el-card style="width: 100%; height: calc(60vh - 270px)">
										<div style="display: flex; height: calc(60vh - 270px)">
											<el-tooltip content="特征集合设计" placement="right" effect="light" style="display: flex; justify-content: center; align-items: center">
												<img src="../../assets/images/基本信息.png" alt="fish tail"
												     style="margin: auto; cursor: pointer; width: 80%" @click="statusClick()"/>
											</el-tooltip>
										</div>
									</el-card>
									<div class="overlay" v-if="active < 0"></div>
									<div class="overlay-success" v-if="active > 0"></div>
								</div>
								<!--		感知模块设计 		-->
								<div style="display: inline-block; position: relative; width: 24%; margin-left: 1%">
									<el-card style="width: 100%; height: calc(60vh - 270px)">
										<div style="display: flex; height: calc(60vh - 270px)">
											<el-tooltip content="感知模块设计" placement="right" effect="light">
												<img src="../../assets/images/myviews.png" alt="fish head"
												     style="margin: auto; cursor: pointer; width: 75%" @click="perceptionClick()"/>
											</el-tooltip>
										</div>
									</el-card>
									<div class="overlay" v-if="active < 1"></div>
									<div class="overlay-success" v-if="active > 1"></div>
								</div>
								<!--		大脑模块 		-->
								<div style="display: inline-block; position: relative; width: 24%; margin-left: 1%">
									<el-card style="width: 100%;height: calc(60vh - 270px)">
										<div style="display: flex; height: calc(60vh - 270px)">
											<el-tooltip content="大脑模块设计" placement="right" effect="light">
												<img src="../../assets/images/智慧大脑.png" alt="fish head"
												     style="margin: auto; cursor: pointer; width: 75%" @click="brainClick()"/>
											</el-tooltip>
										</div>
									</el-card>
									<div class="overlay" v-if="active < 2"></div>
									<div class="overlay-success" v-if="active > 2"></div>
								</div>
								<!--		实验方法 		-->
								<div style="display: inline-block; position: relative; width: 24%; margin-left: 1%">
									<el-card style="width: 100%; height: calc(60vh - 270px)">
										<div style="display: flex; height: calc(60vh - 270px)">
											<el-tooltip content="详细设计" placement="right" effect="light">
												<img src="../../assets/images/运动2.png" alt="fish head"
												     style="margin: auto; cursor: pointer; width: 75%" @click="actionClick()"/>
											</el-tooltip>
										</div>
									</el-card>
									<div class="overlay" v-if="active < 3"></div>
									<div class="overlay-success" v-if="active > 3"></div>
								</div>
							</div>
						</div>
						<div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
							<el-button type="primary" @click="goToPreviousStep">上一步</el-button>
							<el-button type="success" @click="changeAgentCard()" :disabled="active !== 4">确认修改</el-button>
						</div>
					</el-card>
				
				</div>
				<div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
					<el-button type="success" @click="sendData">完成设计</el-button>
				</div>
			</el-card>
			
			<div>
				<el-drawer v-model="agentDrawer" ref="drawer" title="Data Analysis" direction="rtl" size="30%">
					<template #title>
						<h4>agent类库信息</h4>
					</template>
					<div style="height: calc(100vh - 100px)">
						<div style="height: calc(100vh - 100px); overflow-x: auto;">
							<el-table :data="classInfo" style="width: 100%;" border stripe>
								<el-table-column prop="name" label="agent名称" width="120"></el-table-column>
								<el-table-column prop="learningType" label="学习方式" width="120"></el-table-column>
								<el-table-column prop="name" label="决策方式" width="120"></el-table-column>
								<el-table-column label="操作" width="120">
									<template #default="scope">
										<el-button type="primary" size="small" @click="removeItem(scope.$index)">
											删除
										</el-button>
									</template>
								</el-table-column>
							
							</el-table>
						</div>
					</div>
				</el-drawer>
			</div>
			<div>
				<el-dialog v-model="flowChartVisible" title="agent流程图" width="50%" center>
					<div style="display: flex; justify-content: center; align-items: center; height: 100%;">
						<el-image style="height: 500px;" :src="perceptUrl" :fit="fit"/>
					</div>
				</el-dialog>
			</div>
			<div>
				<el-dialog v-model="statusVisible" title="特征集合" width="60%" center>
  <div style="display: flex; justify-content: space-around; width: 100%; margin-top: 20px">
    <div style="flex: 1; display: flex; justify-content: center; align-items: center;">
      <el-form label-width="150px">
        <!-- 如果是 BusAgent，显示公交车特定内容 -->
        <template v-if="classInfo[currentAgentIndex].name === 'BusAgent'">
          <!-- 公交车类型 -->
          <el-form-item label="公交车类型">
            <el-checkbox-group v-model="currentBusConfig.types">
              <el-checkbox label="电动公交"></el-checkbox>
              <el-checkbox label="柴油公交"></el-checkbox>
              <el-checkbox label="混合动力公交"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>

          <!-- 最大载客量 -->
          <el-form-item label="最大载客量">
            <el-slider v-model="currentBusConfig.maxCapacity" :min="10" :max="100" show-input></el-slider>
          </el-form-item>

          <!-- 发车频率 -->
          <el-form-item label="发车频率">
            <el-radio-group v-model="currentBusConfig.frequencyType">
              <el-radio label="fixed">固定频率</el-radio>
              <el-radio label="dynamic">动态调整</el-radio>
            </el-radio-group>
            <el-input 
              v-if="currentBusConfig.frequencyType === 'fixed'" 
              v-model="currentBusConfig.frequencyValue" 
              placeholder="输入时长（分钟）" 
              style="width: 200px; margin-left: 20px;"
            ></el-input>
          </el-form-item>

          <!-- 运营时间 -->
          <el-form-item label="运营时间">
            <el-time-picker
              v-model="currentBusConfig.operatingHours"
              is-range
              range-separator="至"
              start-placeholder="开始时间"
              end-placeholder="结束时间"
              format="HH:mm"
            ></el-time-picker>
          </el-form-item>
        </template>

        <!-- CarAgent -->
        <template v-else-if="currentAgentIndex !== -1 && classInfo[currentAgentIndex].name === 'CarAgent'">
          <el-form-item label="车辆类型">
            <el-checkbox-group v-model="currentCarConfig.types">
              <el-checkbox label="轿车"></el-checkbox>
              <el-checkbox label="SUV"></el-checkbox>
              <el-checkbox label="货车"></el-checkbox>
              <el-checkbox label="摩托车"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="燃料类型">
            <el-radio-group v-model="currentCarConfig.fuelType">
              <el-radio label="汽油"></el-radio>
              <el-radio label="柴油"></el-radio>
              <el-radio label="电动"></el-radio>
              <el-radio label="混合动力"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="驾驶风格占比">
            <el-form-item label="保守型">
              <el-slider v-model="currentCarConfig.drivingStyles.conservative" :min="0" :max="100" show-input style="width: 300px;"></el-slider>
            </el-form-item>
            <el-form-item label="激进型">
              <el-slider v-model="currentCarConfig.drivingStyles.aggressive" :min="0" :max="100" show-input></el-slider>
            </el-form-item>
            <el-form-item label="节能型">
              <el-slider v-model="currentCarConfig.drivingStyles.eco" :min="0" :max="100" show-input></el-slider>
            </el-form-item>
            <p v-if="drivingStyleSum !== 100" style="color: red;">总占比必须为100%，当前为 {{ drivingStyleSum }}%</p>
          </el-form-item>
        </template>

        <!-- ResidentAgent -->
        <template v-else-if="currentAgentIndex !== -1 && classInfo[currentAgentIndex].name === 'ResidentAgent'">
          <el-form-item label="居民类型">
            <el-checkbox-group v-model="currentResidentConfig.types">
              <el-checkbox label="上班族"></el-checkbox>
              <el-checkbox label="学生"></el-checkbox>
              <el-checkbox label="退休人员"></el-checkbox>
              <el-checkbox label="游客"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="年龄段占比">
            <el-form-item label="0-18岁">
              <el-slider v-model="currentResidentConfig.ageGroups.youth" :min="0" :max="100" show-input style="width: 300px;"></el-slider>
            </el-form-item>
            <el-form-item label="19-40岁">
              <el-slider v-model="currentResidentConfig.ageGroups.adult" :min="0" :max="100" show-input></el-slider>
            </el-form-item>
            <el-form-item label="41-60岁">
              <el-slider v-model="currentResidentConfig.ageGroups.middle" :min="0" :max="100" show-input></el-slider>
            </el-form-item>
            <el-form-item label="60岁以上">
              <el-slider v-model="currentResidentConfig.ageGroups.senior" :min="0" :max="100" show-input></el-slider>
            </el-form-item>
            <p v-if="ageGroupSum !== 100" style="color: red;">总占比必须为100%，当前为 {{ ageGroupSum }}%</p>
          </el-form-item>
          <el-form-item label="活动地点">
            <el-checkbox-group v-model="currentResidentConfig.activityLocations">
              <el-checkbox label="家"></el-checkbox>
              <el-checkbox label="工作场所"></el-checkbox>
              <el-checkbox label="学校"></el-checkbox>
              <el-checkbox label="购物中心"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
        </template>

        <!-- 其他情况（默认通用表单） -->
        <template v-else>
          <el-form-item label="固定特征：" style="margin-bottom: 30px">
            <el-checkbox v-model="form.nature" label="nature">编号ID</el-checkbox>
          </el-form-item>
          <el-form-item label="可变特征属性：" style="margin-bottom: 30px">
            <el-checkbox v-model="form.nature" label="nature">位置</el-checkbox>
            <el-checkbox v-model="form.nature" label="nature">速度</el-checkbox>
          </el-form-item>
          <el-form-item label="自定义属性名称">
            <el-input v-model="newAttribute.name" placeholder="输入自定义属性名称"></el-input>
          </el-form-item>
          <el-form-item label="自定义属性值">
            <el-input v-model="newAttribute.value" placeholder="输入属性值"></el-input>
          </el-form-item>
          <el-button type="primary" @click="addAttribute">添加属性</el-button>
          <el-table :data="customAttributes" style="width: 100%; margin-top: 20px;">
            <el-table-column prop="name" label="自定义属性名称"></el-table-column>
            <el-table-column prop="value" label="自定义属性值"></el-table-column>
            <el-table-column label="操作">
              <template v-slot="scope">
                <el-button @click="removeAttribute(scope.$index)" type="danger" size="small">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </template>
      </el-form>
    </div>
  </div>
  <div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
    <el-button type="primary" @click="statusFinish()">完成设计</el-button>
  </div>
</el-dialog>
			</div>
			<div>
				<el-dialog v-model="perceptionVisible" title="感知模块" width="60%" center>
					<div style="display: flex; justify-content: space-around; width: 100%; margin-top: 20px">
						<div style="flex: 1; display: flex; justify-content: center; align-items: center;">
							
							<el-form label-width="150px">
								
								<el-form-item label="感知环境类型：" style="margin-bottom: 30px">
									<el-select
									v-model="envType"
									placeholder="Select"
									size="small"
									style="width: 240px"
									>
										<el-option
										v-for="item in optionsEnv"
										:key="item.value"
										:label="item.label"
										:value="item.value"
										/>
									</el-select>
								</el-form-item>
								<el-form-item v-if="envType=='0'" label="基础设定：" style="margin-bottom: 30px">
									<el-form-item label="感知半径" style="margin-bottom: 30px">
										<el-slider v-model="valueR" :step="0.1" :min="0" :max="1"/>
									</el-form-item>
									<el-form-item label="感知角度" style="margin-bottom: 30px">
										<el-slider v-model="valueL" :step="0.1" :min="0" :max="1"/>
									</el-form-item>
								</el-form-item>
								<el-form-item v-if="envType=='1'" label="基础设定：" style="margin-bottom: 30px">
									<el-form-item label="感知方向：" style="margin-bottom: 30px">
										<el-checkbox v-model="form.nature" label="nature">前</el-checkbox>
										<el-checkbox v-model="form.social" label="social">后</el-checkbox>
										<el-checkbox v-model="form.social" label="social">左</el-checkbox>
										<el-checkbox v-model="form.social" label="social">右</el-checkbox>
									</el-form-item>
									<el-form-item label="感知长度：" style="margin-bottom: 30px">
										<el-slider v-model="valueL" :step="1" :min="0" :max="10"/>
									</el-form-item>
								</el-form-item>
								<el-form-item v-if="envType=='2'" label="基础设定：" style="margin-bottom: 30px">
									<el-form-item label="感知方向：" style="margin-bottom: 30px">
										<el-checkbox v-model="form.nature" label="nature">前</el-checkbox>
										<el-checkbox v-model="form.social" label="social">后</el-checkbox>
										<el-checkbox v-model="form.social" label="social">左</el-checkbox>
										<el-checkbox v-model="form.social" label="social">右</el-checkbox>
										<el-checkbox v-model="form.social" label="social">上</el-checkbox>
										<el-checkbox v-model="form.social" label="social">下</el-checkbox>
									</el-form-item>
									<el-form-item label="感知长度：" style="margin-bottom: 30px">
										<el-slider v-model="valueL" :step="1" :min="0" :max="10"/>
									</el-form-item>
								</el-form-item>
								<el-form-item label="感知地图信息：" style="margin-bottom: 30px">
									<el-checkbox v-model="form.nature" label="nature">道路信息</el-checkbox>
									<el-checkbox v-model="form.social" label="social">障碍物信息</el-checkbox>
									<el-checkbox v-model="form.social" label="social">建筑信息</el-checkbox>
									<el-checkbox v-model="form.social" label="social">设施信息</el-checkbox>
								</el-form-item>
								<el-form-item label="agent交互信息：" style="margin-bottom: 30px">
									<el-checkbox v-model="form.sameAgent" label="sameAgent">周边agent数量</el-checkbox>
									<el-checkbox v-model="form.differentAgent" label="differentAgent">周边Agent类型</el-checkbox>
									<el-checkbox v-model="form.differentAgent" label="differentAgent">可交互agent</el-checkbox>
								</el-form-item>
								<el-form-item label="agent感知行为：" style="margin-bottom: 30px">
									<el-checkbox v-model="form.sameAgent" label="sameAgent">周边可交互agent的行为</el-checkbox>
									<el-checkbox v-model="form.differentAgent" label="differentAgent">周边可交互agent的状态</el-checkbox>
									<el-checkbox v-model="form.differentAgent" label="differentAgent">周边可交互agent的属性</el-checkbox>
								</el-form-item>
							</el-form>
						</div>
					</div>
					<div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
						<el-button type="primary" @click="perceptionFinish()">完成设计</el-button>
					</div>
				</el-dialog>
			</div>
			<div>
				<el-dialog v-model="brainVisible" title="决策模块" width="60%" center>
  				<el-tabs v-model="brainTab" type="border-card" style="width: 99%;height: 98%" @tab-click="brainTabClick">
    			    <el-tab-pane label="决策方式" name="1">
  						<div style="display: flex; justify-content: center; width: 100%; margin-top: 20px">
    				  		<div>
      							<el-form label-width="150px">
        				  			<el-form-item label="决策偏好：" style="margin-bottom: 30px">
                            			<el-select
            				  			  v-model="brainType"
            				  			  multiple
            				    		  placeholder="Select"
            				  			  size="small"
            				  			  style="width: 240px"
          								>
            			      				<el-option
              								  v-for="item in brainList"
                 				    		  :key="item.value"
               								  :label="item.label"
              								  :value="item.value"
             				  				/>
            				 			</el-select>
          				  			</el-form-item>
         				  			<el-form-item label="决策方式：" style="margin-bottom: 30px">
           				    			<el-radio-group v-model="form.decType">
            				  				<el-radio :label="'0'">规则决策</el-radio>
            				  				<el-radio :label="'1'">基于效用的决策</el-radio>
             				  				<el-radio :label="'2'">基于概率的决策</el-radio>
          								</el-radio-group>
        				  			</el-form-item>
        				  			<el-form-item v-if="form.decType === '0'" label="" style="margin-bottom: 30px">
          								<p><b>规则决策：</b>为agent预设一系列规则，当满足特定条件时，执行对应的行为</p>
          								<p><b>示例：</b>公交agent在检测到前方路段拥堵时，根据规则选择换道或等待</p>
        				  			</el-form-item>
        				  			<el-form-item v-if="form.decType === '1'" label="" style="margin-bottom: 30px">
          								<p><b>基于效用的决策：</b>让agent根据行为的预期效用来选择最优行为</p>
          								<p><b>示例：</b>公交agent在选择路线时，综合考虑各因素，计算每条路线的效用值，选择效用最高的路线</p>
        				  			</el-form-item>
        				  			<el-form-item v-if="form.decType === '2'" label="" style="margin-bottom: 30px">
          								<p><b>基于概率的决策：</b>让agent根据行为成功的概率来选择行为</p>
          								<p><b>示例：</b>居民agent在选择避难场所时，根据各个避难场所的安全概率等因素，随机选择一个避难场所</p>
        				  			</el-form-item>
      							</el-form>
   	 				  		</div>
  						</div>
				  	</el-tab-pane>
					<el-tab-pane label="学习演化" name="2">
  						<div style="display: flex; justify-content: center; width: 100%; margin-top: 20px">
    						<el-form label-width="150px">
      							<el-form-item label="学习演化：" style="margin-bottom: 30px">
        							<el-radio-group v-model="form.learningType">
          								<el-radio :label="'0'">强化学习</el-radio>
          								<el-radio :label="'1'">模仿学习</el-radio>
          								<el-radio :label="'2'">遗传算法</el-radio>
        							</el-radio-group>
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '0'" label="" style="margin-bottom: 30px">
        							<p><b>强化学习：</b>agent通过与环境的交互不断学习和优化自己的行为策略</p>
        							<p><b>示例：</b>公交agent在运行过程中，根据反馈信息，不断调整发车频率和路线，提高运输效率</p>
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '1'" label="" style="margin-bottom: 30px">
        							<p><b>模仿学习：</b>agent通过观察和模仿其他优秀agent或人类专家的行为来学习</p>
        							<p><b>示例：</b>居民agent在面对内涝时，观察邻居的避难行为，学习他们的避难策略</p>
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '2'" label="" style="margin-bottom: 30px">
        							<p><b>遗传算法：</b>通过选择、交叉、变异等操作，不断优化agent的决策策略</p>
        							<p><b>示例：</b>公交agent在规划发车策略时，根据乘客流量等信息，不断优化发车频率和路线</p>
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '1'" label="模仿概率" style="margin-bottom: 30px">
        							<el-slider v-model="value1" :step="0.1" :min="0" :max="1" />
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '1'" label="模仿对象：" style="margin-bottom: 30px">
        							<el-checkbox v-model="form.nature" label="nature">感知范围内agent</el-checkbox>
        							<el-checkbox v-model="form.social" label="social">可交互agent</el-checkbox>
        							<el-checkbox v-model="form.social" label="social">相同属性agent</el-checkbox>
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '1'" label="模仿内容：" style="margin-bottom: 30px">
        							<el-form-item v-if="form.learningType === '1'" label="状态：" style="margin-bottom: 30px">
          								<el-checkbox v-model="form.nature" label="nature">当前状态</el-checkbox>
          								<el-checkbox v-model="form.social" label="social">最高频率状态</el-checkbox>
        							</el-form-item>
        							<el-form-item v-if="form.learningType === '1'" label="行为：" style="margin-bottom: 30px">
          								<el-checkbox v-model="form.nature" label="nature">当前行为</el-checkbox>
          								<el-checkbox v-model="form.social" label="social">最高频率行为</el-checkbox>
        							</el-form-item>
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '0'" label="算法选择" style="margin-bottom: 30px">
        							<el-select
          							  v-model="value"
          							  placeholder="方法选择"
          							  size="large"
          							  style="width: 240px"
        							>
          								<el-option
            							  v-for="item in optionsRL"
            							  :key="item.value"
            							  :label="item.label"
            							  :value="item.value"
          								/>
        							</el-select>
      							</el-form-item>
      							<el-form-item v-if="form.learningType === '0'" label="强化内容：" style="margin-bottom: 30px">
        							<el-form-item v-if="form.learningType === '0'" label="状态属性：" style="margin-bottom: 30px">
          								<el-checkbox v-model="form.nature" label="nature">当前状态</el-checkbox>
          								<el-checkbox v-model="form.social" label="social">最高频率状态</el-checkbox>
        							</el-form-item>
        							<el-form-item v-if="form.learningType === '0'" label="行为规律：" style="margin-bottom: 30px">
          								<el-checkbox v-model="form.nature" label="nature">当前行为</el-checkbox>
         								<el-checkbox v-model="form.social" label="social">最高频率行为</el-checkbox>
        							</el-form-item>
      							</el-form-item>
    						</el-form>
  						</div>
					</el-tab-pane>
					</el-tabs>
					
					<div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
						<el-button type="primary" @click="brainFinish()">完成设计</el-button>
					</div>
				</el-dialog>
			</div>
			<div>
				<el-dialog v-model="learnVisible" title="学习演化" width="60%" center>
					<div style="display: flex; justify-content: center; width: 100%; margin-top: 20px">
						<el-form label-width="150px">
							<el-form-item label="学习方式：" style="margin-bottom: 30px">
								<el-radio-group v-model="form.learningType">
									<el-radio :label="'0'">大模型</el-radio>
									<el-radio :label="'2'">模仿学习</el-radio>
									<el-radio :label="'3'">强化学习</el-radio>
								</el-radio-group>
							</el-form-item>
							<el-form-item v-if='form.learningType === "0"' label="模型" style="margin-bottom: 30px">
								<el-select
								v-model="form.sex"
								placeholder="选择性别"
								size="large"
								style="width: 240px"
								>
									<el-option
									v-for="item in optionsGPT"
									:key="item.value"
									:label="item.label"
									:value="item.value"
									/>
								</el-select>
							</el-form-item>
							<el-form-item v-if='form.learningType === "0"' label="temperature" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="100"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "0"' label="max tokens" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="1" :min="100" :max="10000"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "0"' label="top_p" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="1"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "0"' label="frequency_penalty" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="1"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "0"' label="presence_penalty" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="1"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "0"' label="提示词设计" style="margin-bottom: 30px">
								<el-button type="primary" round>模板下载</el-button>
								<el-button type="success" round>确认-提交</el-button>
							</el-form-item>
							<el-form-item v-if='form.learningType === "2"' label="模仿概率" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="1"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "3"' label="算法选择" style="margin-bottom: 30px">
								<el-select
								v-model="value"
								placeholder="方法选择"
								size="large"
								style="width: 240px"
								>
									<el-option
									v-for="item in optionsRL"
									:key="item.value"
									:label="item.label"
									:value="item.value"
									/>
								</el-select>
							</el-form-item>
							<el-form-item v-if='form.learningType === "3"' label="学习率" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="1"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "3"' label="折扣因子" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="1"/>
							</el-form-item>
							<el-form-item v-if='form.learningType === "3"' label="探索率" style="margin-bottom: 30px">
								<el-slider v-model="value1" :step="0.1" :min="0" :max="1"/>
							</el-form-item>
						</el-form>
					</div>
					<div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
						<el-button type="primary" @click="learnFinish()">完成设计</el-button>
					</div>
				</el-dialog>
			</div>
			<div>
				<el-dialog v-model="actionVisible" title="行动模块" width="60%" center>
  <div style="display: flex; justify-content: center; width: 100%; margin-top: 20px">
    <el-form label-width="150px">
      <el-form-item label="基础行为：" style="margin-bottom: 30px">
        <el-checkbox v-model="form.order" label="order">移动</el-checkbox>
        <el-checkbox v-model="form.talk" label="talk">更换方向</el-checkbox>
        <el-checkbox v-model="form.rest" label="rest">加速</el-checkbox>
      </el-form-item>
      <el-form-item label="交互动作：" style="margin-bottom: 30px">
        <el-checkbox v-model="form.talk" label="talk">协作（在规则设计详细设计）</el-checkbox>
      </el-form-item>

      <!-- BusAgent 速度选择 -->
      <el-form-item v-if="currentAgentIndex !== -1 && classInfo[currentAgentIndex].name === 'BusAgent'" label="速度选择：" style="margin-bottom: 30px">
        <el-slider v-model="currentBusSpeed" :min="0" :max="50" show-input></el-slider>
      </el-form-item>

      <!-- CarAgent 速度选择 -->
      <el-form-item v-if="currentAgentIndex !== -1 && classInfo[currentAgentIndex].name === 'CarAgent'" label="速度选择：" style="margin-bottom: 30px">
        <el-slider v-model="currentCarSpeed" :min="0" :max="120" show-input></el-slider>
      </el-form-item>
	  <!-- ResidentAgent 交通方式及工具条件 -->
      <template v-if="currentAgentIndex !== -1 && classInfo[currentAgentIndex].name === 'ResidentAgent'">
        <el-form-item label="交通方式优先级" style="margin-bottom: 30px">
          <el-table :data="currentResidentConfig.transportOptions" row-key="mode" style="width: 100%;">
            <el-table-column label="启用">
              <template #default="scope">
                <el-checkbox v-model="scope.row.enabled"></el-checkbox>
              </template>
            </el-table-column>
            <el-table-column prop="mode" label="方式"></el-table-column>
            <el-table-column label="优先级">
              <template #default="scope">
                <el-input-number v-model="scope.row.priority" :min="1" :max="5" :disabled="!scope.row.enabled"></el-input-number>
              </template>
            </el-table-column>
          </el-table>
        </el-form-item>
        <el-form-item label="工具使用条件" style="margin-bottom: 30px">
          <el-form-item label="步行距离">
            <el-input v-model="currentResidentConfig.conditions.walkDistance" placeholder="小于（公里）" type="number" style="width: 150px;"></el-input>
          </el-form-item>
          <el-form-item label="公共交通距离">
            <el-input v-model="currentResidentConfig.conditions.publicTransportDistance" placeholder="大于（公里）" type="number" style="width: 150px;"></el-input>
          </el-form-item>
        </el-form-item>
      </template>

      <el-form-item label="动作执行条件：" style="margin-bottom: 30px">
        <el-form-item label="移动：" style="margin-bottom: 30px">
          <el-checkbox v-model="form.rest" label="talk">其他agent影响</el-checkbox>
          <el-checkbox v-model="form.rest" label="talk">policyAgent引导</el-checkbox>
        </el-form-item>
        <el-form-item label="变速：" style="margin-bottom: 30px">
          <el-checkbox v-model="form.talk" label="talk">积水深度影响</el-checkbox>
          <el-checkbox v-model="form.rest" label="talk">其他agent影响</el-checkbox>
		  <el-checkbox v-model="form.rest" label="talk">policyAgent引导</el-checkbox>
        </el-form-item>
        <el-form-item label="变向：" style="margin-bottom: 30px">
          <el-checkbox v-model="form.talk" label="talk">障碍物/积水感知</el-checkbox>
          <el-checkbox v-model="form.rest" label="talk">policyAgent引导</el-checkbox>
        </el-form-item>
        <el-form-item label="交互：" style="margin-bottom: 30px">
          <el-checkbox v-model="form.talk" label="talk">组织网络周期变化</el-checkbox>
          <el-checkbox v-model="form.rest" label="talk">状态变化</el-checkbox>
          <el-checkbox v-model="form.rest" label="talk">感知agent</el-checkbox>
        </el-form-item>
      </el-form-item>
    </el-form>
  </div>
  <div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
    <el-button type="primary" @click="actionFinish()">完成设计</el-button>
  </div>
</el-dialog>
			</div>
			<div>
				<el-dialog v-model="changeVisible" title="详细信息" width="60%" center>
					<div style="width: 100%; height: 100%;">
						<el-form label-width="150px">
							<el-form-item label="agent行动：" style="margin-bottom: 30px">
								<div v-for="(item, index) in names" :key="item.value" style="margin-bottom: 10px">
									<el-button type="primary" size="small" @click="removeItem(index)">
										移除：{{ item.label }}
									</el-button>
								</div>
							</el-form-item>
						</el-form>
						<div style="display: flex; justify-content: center; width: 100%; margin-top: 40px;">
							<el-button type="primary" @click="closeCard()">确认</el-button>
						</div>
					</div>
				</el-dialog>
			</div>
		</div>
	</div>
</template>

<script>
import {reactive, ref} from 'vue'
import {ElMessage, ElMessageBox} from "element-plus";
import ChatWithAgent from '../../components/ChatWithAgent.vue';
export default {
	components: {
		ChatWithAgent
	},
	name: "SmartCity_aiBotDesign",
	setup() {
		const currentAgentIndex = ref(-1);
		const currentAgentName = ref('None'); // 初始值
		const structNames = ref([]);
		const structLinks = ref([]);
		const xNum = ref(0);
		const yNum = ref([1]);
		const socket = new WebSocket('ws://localhost:8080/ws')
		const optionsWork = [
			{label: '懒惰', value: 1},
			{label: '普通', value: 5},
			{label: '勤劳', value: 10}
		]
		const optionsSex = [
			{label: '男', value: 1},
			{label: '女', value: 0}
		]
		const newAttribute = ref({
			name: '',
			value: ''
		});
		const removeAttribute = (index) => {
			customAttributes.splice(index, 1);
		};
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
			name: 'None',
			decType: '0'
		});
		
		// 新增 BusAgent 的配置数据
		const currentBusConfig = reactive({
    types: [], // 公交车类型（多选）
    maxCapacity: 50, // 最大载客量，默认值 50
    frequencyType: 'fixed', // 发车频率类型，默认固定频率
    frequencyValue: '10', // 固定频率值，默认 10 分钟
    operatingHours: ['08:00', '22:00'], // 运营时间，默认 08:00-22:00
  });
  const currentBusSpeed = ref(30); // 新增：默认速度 30
  const currentCarSpeed = ref(60); // 新增：CarAgent 的速度，默认 60
// 新增：CarAgent 配置
const currentCarConfig = reactive({
    types: [],
    fuelType: '汽油', // 默认值
    drivingStyles: {
      conservative: 33, // 保守型
      aggressive: 33,  // 激进型
      eco: 34,         // 节能型
    },
  });

  // 新增：ResidentAgent 配置
  const currentResidentConfig = reactive({
    types: [],
    ageGroups: {
      youth: 25,   // 0-18岁
      adult: 35,   // 19-40岁
      middle: 25,  // 41-60岁
      senior: 15,  // 60岁以上
    },
    activityLocations: [],
	transportOptions: [ // 新增：交通方式及优先级
      { mode: '步行', enabled: true, priority: 1 },
      { mode: '自行车', enabled: false, priority: 2 },
      { mode: '公共交通', enabled: true, priority: 3 },
      { mode: '私家车', enabled: false, priority: 4 },
    ],
    conditions: { // 新增：工具使用条件
      walkDistance: '1', // 默认步行距离小于 1 公里
      publicTransportDistance: '5', // 默认公共交通距离大于 5 公里
    },
  });
		const classInfo = ref([
  {
    imgUrl: '/static/icons/bus.png',
    name: 'BusAgent',
    state: 0, // 0 表示等待设计，1 表示设计完成
    designStep: 0, // 新增字段，表示设计进度
    agentList: [],
	brainType: [], // 新增字段，用于存储 BusAgent 的决策偏好
    social: true,
    nature: true,
    otherAgent: false,
    map: true,
    weather: false,
    sameAgent: false,
    differentAgent: false,
    sysAgent: false,
    learningType: '0',
    workStatus: 10,
	speed:[], // 新增：初始速度 30
    sex: 1,
    order: true,
    talk: false,
    rest: true,
    dayRatio: 0.5,
    talkRatio: 3
  },
  {
    imgUrl: '/static/icons/car.png',
    name: 'CarAgent',
    state: 0,
    designStep: 0,
    agentList: [],
	brainType: [],
	carConfig: { ...currentCarConfig }, // 初始化 CarAgent 配置
	speed: [],
    social: true,
    nature: true,
    otherAgent: false,
    map: true,
    weather: false,
    sameAgent: false,
    differentAgent: false,
    sysAgent: false,
    learningType: '0',
    workStatus: 10,
    sex: 1,
    order: true,
    talk: false,
    rest: true,
    dayRatio: 0.5,
    talkRatio: 3
  },
  {
    imgUrl: '/static/icons/resident.png',
    name: 'ResidentAgent',
    state: 0,
    designStep: 0,
    agentList: [],
	brainType: [],
	residentConfig: { ...currentResidentConfig }, // 初始化 ResidentAgent 配置
    social: true,
    nature: true,
    otherAgent: false,
    map: true,
    weather: false,
    sameAgent: false,
    differentAgent: false,
    sysAgent: false,
    learningType: '0',
    workStatus: 10,
    sex: 1,
    order: true,
    talk: false,
    rest: true,
    dayRatio: 0.5,
    talkRatio: 3
  }
])
const cardIsExpand = ref([false, false, false])
		const names = ref([
			{
				label: 'defaultAgent',
				value: 0
			}
		])
		const addToClassInfo = () => {
			classInfo.value.push({...form});
		};
		return {
    form, active, classInfo, addToClassInfo, names, optionsSex, optionsWork, socket,
    structNames, structLinks, xNum, yNum, removeAttribute, newAttribute, envType, 
    cardIsExpand, currentAgentName, currentAgentIndex, currentBusConfig, currentBusSpeed, currentCarConfig, currentResidentConfig, currentCarSpeed
  };
	},
	data() {
		return {
			evoList: [
				{value: '0', label: '轮盘赌选择',},
				{value: '1', label: '精英选择',},
				{value: '2', label: '截断选择',},
				{value: '3', label: '锦标赛选择',},
			],
			brainType: [],
			// 通用 Agent 的决策偏好选项
			defaultBrainList: [
      { value: '0', label: '交互协作' },
      { value: '1', label: '收益状态变化' },
      { value: '2', label: '体力状态变化' },
      { value: '3', label: '移动距离' },
    ],
    // BusAgent 的决策偏好选项
    busBrainList: [
      { value: '0', label: '安全运营' },
      { value: '1', label: '维持基本服务' },
      { value: '2', label: '疏散辅助' },
      { value: '3', label: '资源优化' },
    ],
	// 新增：CarAgent 的决策偏好
    carBrainList: [
      { value: '0', label: '乘员安全' },
      { value: '1', label: '遵守指挥' },
      { value: '2', label: '道路资源公平性' },
      { value: '3', label: '个人行程达成' },
    ],
    // 新增：ResidentAgent 的决策偏好
    residentBrainList: [
      { value: '0', label: '生存安全' },
      { value: '1', label: '家庭团聚' },
      { value: '2', label: '财产保护' },
      { value: '3', label: '出行效率' },
    ],
    // 当前使用的 brainList，默认为通用选项
    brainList: [],
			optionsEnv: [
				{value: '0', label: 'GIS地图',},
				{value: '1', label: '2D栅格',},
				{value: '2', label: '3D栅格',},
			],
			customAttributes: [],
			valueR: 0,
			valueL: 0,
			
			brainTab: '1',
			agentDrawer: false,
			optionsGPT: [
				{value: 'Option1', label: 'chatGPT'},
				{value: 'Option3', label: 'llama3'},
				{value: 'Option4', label: 'kimi'},
				{value: 'Option2', label: '星火'},
			],
			optionsRL: [
				{value: 'Option1', label: 'Q-lerning方法',},
				{value: 'Option2', label: 'SARSA方法',},
				{value: 'Option3', label: 'Deep Q-Network (DQN)',},
				{value: 'Option4', label: 'Policy Gradient',},
				{value: 'Option5', label: 'Actor-Critic',},
				{value: 'Option6', label: 'Monte Carlo Methods',},
				{value: 'Option7', label: 'Temporal Difference (TD) Learning',},
				{value: 'Option8', label: 'Advantage Actor-Critic (A2C)',},
				{value: 'Option9', label: 'Proximal Policy Optimization (PPO)',},
				{value: 'Option10', label: 'Trust Region Policy Optimization (TRPO)',},
				{value: 'Option11', label: 'Deep Deterministic Policy Gradient (DDPG)',},
				{value: 'Option12', label: 'Multi-Agent Reinforcement Learning',},
				{value: 'Option13', label: 'Hierarchical Reinforcement Learning',}
			],
			valueScope: [],
			valueEnvOne: [],
			optionsEnvOne: [
				{value: '0', label: '地理信息'},
				{value: '1', label: '社会环境感知'}
			],
			valueEnvTwo: [],
			optionsEnvTwo: [
				{value: '0', label: '自然环境感知'},
				{value: '1', label: '社会环境感知'}
			],
			optionsScope: [
				{value: '0', label: '自然环境感知',},
				{value: '1', label: '社会环境感知',}
			],
			stepMsg: ['特征集合', '感知模块', '决策模块', '行动模块'],
			perceptionVisible: false,
			statusVisible: false,
			flowChartVisible: false,
			brainVisible: false,
			actionVisible: false,
			learnVisible: false,
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
			images: [
				'/static/icons/aibot.png',
			],
			imagesStore: [
				'/static/icons/bot1.png',
				'/static/icons/bot2.png',
				'/static/icons/bot3.png',
				'/static/icons/bot4.png',
			],
			newAgentImage: '/static/icons/bot1.png'
		};
	},
	computed: {
  drivingStyleSum() {
    const styles = this.currentCarConfig.drivingStyles;
    return styles.conservative + styles.aggressive + styles.eco;
  },
  ageGroupSum() {
    const ages = this.currentResidentConfig.ageGroups;
    return ages.youth + ages.adult + ages.middle + ages.senior;
  },
},
	methods: {
		goToPreviousStep() {
  if (this.currentAgentIndex === -1) {
    ElMessage({
      type: 'warning',
      message: '请先选择一个 Agent',
    });
    return;
  }
  const currentAgent = this.classInfo[this.currentAgentIndex];
  const maxStep = currentAgent.designStep;
  const newStep = this.active - 1;

  if (newStep >= 0 && newStep < maxStep) {
    this.active = newStep;
    ElMessage({
      type: 'success',
      message: `已返回到 ${this.stepMsg[newStep]}，请点击模块卡片进行编辑`,
    });
  } else {
    ElMessage({
      type: 'info',
      message: '已经是第一个设计模块',
    });
  }
},
openDesignDialog(step) {
  // 先关闭所有对话框
  this.statusVisible = false;
  this.perceptionVisible = false;
  this.brainVisible = false;
  this.actionVisible = false;

  // 根据步骤打开对应对话框
  switch (step) {
    case 0:
      this.statusVisible = true; // 特征集合
      break;
    case 1:
      this.perceptionVisible = true; // 感知模块
      break;
    case 2:
      this.brainVisible = true; // 大脑模块
      break;
    case 3:
      this.actionVisible = true; // 行为模块
      break;
    default:
      break;
  }
},
changeAgentCard() {
  if (this.currentAgentIndex === -1) {
    ElMessage({
      type: 'warning',
      message: '请先选择一个 Agent',
    });
    return;
  }

  this.classInfo[this.currentAgentIndex].state = 1; // 更新选中的 Agent 状态
  this.classInfo[this.currentAgentIndex].agentList = [];
  let newAgentList = this.newTemplate[this.tmpCardIndex].agentList; // 这部分代码可能有问题，见下方说明
  for(let i = 0; i < newAgentList.length; i++)
  this.classInfo[this.currentAgentIndex].agentList.push(newAgentList[i].roleName);
  this.active = 0;
  this.newDecisionAgentTemplate.roleModeling = ''; // 未定义，可能需要移除或修复
  for (let i = 0; i < this.oodaData.length; i++)
  this.oodaData[i].itemStyle.color = this.pieDefaultColor;
  this.oodaData[0].itemStyle.color = this.pieProcessingColor;
  this.oodaOption.series.data = this.oodaData;
  this.oodaChart.setOption(this.oodaOption);
},
cardClick(index) {
  if (this.cardIsExpand[index]) {
    this.cardIsExpand[index] = false;
    this.currentAgentName = 'newAgent';
    this.currentAgentIndex = -1;
    this.brainList = this.defaultBrainList;
    this.brainType = [];
  } else {
    this.cardIsExpand = this.cardIsExpand.map(() => false);
    this.cardIsExpand[index] = true;
    this.currentAgentName = this.classInfo[index].name;
    this.currentAgentIndex = index;
    this.active = this.classInfo[index].designStep;

    if (this.classInfo[index].name === 'BusAgent') {
      this.brainList = this.busBrainList;
      this.brainType = this.classInfo[index].brainType || [];
      Object.assign(this.currentBusConfig, this.classInfo[index].busConfig);
      this.currentBusSpeed = this.classInfo[index].speed;
    } else if (this.classInfo[index].name === 'CarAgent') {
      this.brainList = this.carBrainList;
      this.brainType = this.classInfo[index].brainType || [];
      Object.assign(this.currentCarConfig, this.classInfo[index].carConfig);
      this.currentCarSpeed = this.classInfo[index].speed;
    } else if (this.classInfo[index].name === 'ResidentAgent') {
      this.brainList = this.residentBrainList;
      this.brainType = this.classInfo[index].brainType || [];
      Object.assign(this.currentResidentConfig, this.classInfo[index].residentConfig); // 加载 ResidentAgent 配置
    } else {
      this.brainList = this.defaultBrainList;
      this.brainType = this.classInfo[index].brainType || [];
    }
  }
},
		removeAttribute(index) {
			this.customAttributes.splice(index, 1);
		},
		addAttribute() {
			if (this.newAttribute.name && this.newAttribute.value) {
				this.customAttributes.push({
					name: this.newAttribute.name,
					value: this.newAttribute.value
				});
				this.newAttribute.value = '';
				this.newAttribute.name = '';
			} else {
				alert(newAttribute.value.name)
				alert(newAttribute.value.value)
				alert('请填写完整的自定义属性名称和值');
			}
		},
		handleTabClick(tab, event) {
			console.log(tab, event);
		},
		showDrower() {
			this.agentDrawer = !this.agentDrawer;
		},
		sendData() {
			this.socket.send(JSON.stringify({event: 'class_info', data: this.classInfo}))
		},
		removeItem(index) {
			this.classInfo.splice(index, 1);
		},
		statusClick() {
  if (this.active >= 0) {
    this.statusVisible = true; // 打开特征集合模块对话框
  } else {
    ElMessage({
      type: 'error',
      message: '请先完成前置模块',
    });
  }
},

perceptionClick() {
  if (this.active >= 1) {
    this.perceptionVisible = true; // 打开感知模块对话框
  } else {
    ElMessage({
      type: 'error',
      message: '请先完成特征集合设计',
    });
  }
},

brainClick() {
  if (this.active >= 2) {
    this.brainVisible = true; // 打开大脑模块对话框
  } else {
    ElMessage({
      type: 'error',
      message: '请先完成感知模块设计',
    });
  }
},

actionClick() {
  if (this.active >= 3) {
    this.actionVisible = true; // 打开行动模块对话框
  } else {
    ElMessage({
      type: 'error',
      message: '请先完成大脑模块设计',
    });
  }
},
		learnClick() {
			if (this.active > 3) {
				let msg1 = ''
				if (this.active > 2)
					msg1 = '所有步骤已全部完成，'
				ElMessageBox.confirm(
				msg1 + '确定返回 <b>' + this.stepMsg[1] + '</b> 重新设计吗？',
				'Warning',
				{
					dangerouslyUseHTMLString: true,
					confirmButtonText: '确认',
					cancelButtonText: '取消',
					type: 'warning',
				}
				).then(() => {
					this.active = 1
					this.learnVisible = true;
				})
			} else if (this.active < 3) {
				ElMessage({
					type: 'error',
					message: '请先设计<b>' + this.stepMsg[this.active] + '</b>',
					dangerouslyUseHTMLString: true,
				})
			} else {
				this.learnVisible = true;
			}
			console.log('action click')
		},
		changeClick() {
			this.changeVisible = true
			console.log('change click')
		},
		buttonClick() {
			this.nameVisible = true;
			console.log('Button was clicked!')
		},
		addBot() {
			this.flowChartVisible = true;
			this.structNames = ['决策接单', '路径规划', '派送完成', '评估状态', '随机游走', '选择商区'];
			this.structLinks = [
				{source: '决策接单', target: '路径规划'},
				{source: '路径规划', target: '派送完成'},
				{source: '派送完成', target: '评估状态'},
				{source: '评估状态', target: '随机游走'},
				{source: '随机游走', target: '选择商区'}
			];
			this.xNum = 1;
			this.yNum = [6];
			if (this.active < 3) {
				ElMessage({
					type: 'error',
					message: '请先完成所有模块的设计'
				})
				return;
			}
			console.log('add bot')
			this.images.push(this.newAgentImage)
			this.newAgentImage = this.imagesStore[Math.floor(Math.random() * this.imagesStore.length)]
			this.active = 0
			// this.names.push(this.form.name)
			this.addToClassInfo()
			console.log(this.classInfo)
			this.names.push({
				label: this.form.name,
				value: this.names.length,
			})
			this.cardIsExpand.push(false);
			console.log(this.names)
			if (this.form.decType === '0') {
				this.perceptUrl = this.percptionOneUrl;
			} else if (this.form.decType === '1') {
				this.perceptUrl = this.percptionTwoUrl;
			} else {
				this.perceptUrl = this.percptionThreeUrl;
			}
		},
		changeClass() {
			this.changeVisible = true
		},
		statusFinish() {
  if (this.currentAgentIndex === -1) {
    ElMessage({
      type: 'warning',
      message: '请先选择一个 Agent',
    });
    return;
  }
  const currentAgent = this.classInfo[this.currentAgentIndex];
  currentAgent.designStep = Math.max(currentAgent.designStep, 1);
  this.active = 1;

  if (currentAgent.name === 'BusAgent') {
    currentAgent.busConfig = { ...this.currentBusConfig };
  } else if (currentAgent.name === 'CarAgent') {
    if (this.drivingStyleSum !== 100) {
      ElMessage({
        type: 'error',
        message: '驾驶风格总占比必须为100%',
      });
      return;
    }
    currentAgent.carConfig = { ...this.currentCarConfig };
  } else if (currentAgent.name === 'ResidentAgent') {
    if (this.ageGroupSum !== 100) {
      ElMessage({
        type: 'error',
        message: '年龄段总占比必须为100%',
      });
      return;
    }
    currentAgent.residentConfig = { ...this.currentResidentConfig };
  }

  this.statusVisible = false;
},

perceptionFinish() {
  if (this.currentAgentIndex === -1) {
    ElMessage({
      type: 'warning',
      message: '请先选择一个 Agent',
    });
    return;
  }
  this.classInfo[this.currentAgentIndex].designStep = Math.max(this.classInfo[this.currentAgentIndex].designStep, 2);
  this.active = 2;
  this.perceptionVisible = false;
},

brainFinish() {
  if (this.currentAgentIndex === -1) {
    ElMessage({
      type: 'warning',
      message: '请先选择一个 Agent',
    });
    return;
  }
  const currentAgent = this.classInfo[this.currentAgentIndex];
  currentAgent.designStep = Math.max(currentAgent.designStep, 3);
  currentAgent.brainType = [...this.brainType]; // 保存选择的决策偏好
  this.active = 3;
  this.brainVisible = false;
},
		learnFinish() {
			if (this.active === 3)
				this.active++;
			this.learnVisible = !this.learnVisible;
		},
		actionFinish() {
  if (this.currentAgentIndex === -1) {
    ElMessage({
      type: 'warning',
      message: '请先选择一个 Agent',
    });
    return;
  }
  const currentAgent = this.classInfo[this.currentAgentIndex];
  currentAgent.designStep = 4;
  this.active = 4;

  if (currentAgent.name === 'BusAgent') {
    currentAgent.speed = this.currentBusSpeed;
  } else if (currentAgent.name === 'CarAgent') {
    currentAgent.speed = this.currentCarSpeed;
  } else if (currentAgent.name === 'ResidentAgent') {
    currentAgent.residentConfig = { ...this.currentResidentConfig }; // 保存 ResidentAgent 配置
  }

  this.actionVisible = false;
},
		nextStep() {
			if (this.active++ > 2)
				this.active = 3
		},
		closeCard() {
			this.changeVisible = !this.changeVisible;
		},
		preStep() {
			if (this.active-- < 1)
				this.active = 0
		},
	}
};
</script>

<style scoped>
.bg {
	background: url('../../assets/images/agents.png') no-repeat center center / contain !important;
	min-height: 60vh;
	width: 100%;
	min-width: 500px;
	display: flex;
	position: relative;
}

.image-button {
	position: absolute;
	background-color: rgba(0, 0, 0, 0); /* 半透明黑色背景 */
	color: white; /* 白色文字 */
	border: none;
	cursor: pointer;
	width: 150px; /* 设置宽度 */
	height: 60px; /* 设置高度 */
	display: flex;
	align-items: center;
	justify-content: center;
	text-align: center;
	border-radius: 5px; /* 圆角边框 */
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
</style>

