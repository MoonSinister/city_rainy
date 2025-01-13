from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from BaseModule.agent_bus import BusAgent
import matplotlib.pyplot as plt
import numpy as np
from BaseModule.physical_environment import GeoGrid
import json
import warnings
import os
from random import Random

warnings.simplefilter(action='ignore', category=FutureWarning)

# 模型实例
model = Model()


def get_agent():
    agent_list = []
    for i in range(1):#193
        for j in range(1):#3每个线路安排三辆车
            myagent = BusAgent(unique_id=i*3+j,route_id=i, model=model)
            agent_list.append(myagent)
    return agent_list


def plot_path(matrix):
    matrix_np = np.array(matrix)

    # 找到值为 1 的坐标
    coordinates = np.column_stack(np.where(matrix_np == 1))

    # 创建一个绘图
    plt.figure(figsize=(6, 6))

    plt.plot(coordinates[:, 1], coordinates[:, 0], color='red', linewidth=2, marker='o', markersize=3, zorder=5)
    # 显示值为1的点，并调整点的大小
    plt.scatter(coordinates[:, 1], coordinates[:, 0], color='blue', s=1, zorder=5)  # s=100 控制点的大小

    # plt.gca().invert_yaxis()  # 反转 y 轴，使得 (0, 0) 是左上角
    plt.title('Displaying 1s as large points')
    plt.show()

def main():
    map_path = './route_grid/tianjin_expand.npy'
    map_matrix = np.load(map_path)
    env = GeoGrid(map_matrix)
    #初始化环境，初始状态不添加降水情况
    agent_list = get_agent()
    #每种不同路线的busagent
    agent_list = [agent for agent in agent_list if not np.all(agent.site == 0)]
    # 去除所有site为全零矩阵的元素（不好看）
    print(f"剩余的agent数量: {len(agent_list)}")  # 输出剩余的 agent 数量
    timesch = BaseScheduler(model)
    for j in range(len(agent_list)):
        # print(agent_list[j].name)
        # plot_path(agent_list[j].route)
        timesch.add(agent_list[j])
    #将所有agent添加到时间表统一管理

    #每个时间更新env
    for i in range(1):#16
        rain_path = os.path.join('./raindata', f'{i+1}.npy')
        rain_matrix = np.load(rain_path)
        env.map_update(rain_matrix)
        for j in range(2000):#5分钟走一下
            timesch.step()



if __name__ == "__main__":
    main()
