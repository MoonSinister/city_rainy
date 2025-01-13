from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from BaseModule.agent_bus import BusAgent
import matplotlib.pyplot as plt
import numpy as np
from BaseModule.physical_environment import GeoGrid
import json
import warnings
from random import Random

warnings.simplefilter(action='ignore', category=FutureWarning)

# 模型实例
model = Model()


def get_agent():
    agent_list = []
    for i in range(1):#193
        myagent = BusAgent(unique_id=i, model=model)
        print(i)
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
    agent_list = get_agent()

    # 去除所有site为全零矩阵的元素
    agent_list = [agent for agent in agent_list if not np.all(agent.site == 0)]

    print(f"剩余的agent数量: {len(agent_list)}")  # 输出剩余的 agent 数量

    timesch = BaseScheduler(model)

    # 继续执行你的逻辑
    for i in range(len(agent_list)):
        print(agent_list[i].name)
        matrix = np.load('./route_grid/tianjin_expand.npy')
        plot_path(matrix)
        timesch.add(agent_list[i])


if __name__ == "__main__":
    main()
