from BaseModule.agent import Agent
from BaseModule.model import Model
import glob
import os
import numpy as np
import re  # 导入正则表达式模块
from BaseModule.trans_json_to_np import points_to_grid
import json


class BusAgent(Agent):

    def __init__(self, unique_id: int, model: Model) -> None:
        super().__init__(unique_id, model)
        self.name = self.get_route_name(unique_id)  # 从文件名中提取route_name
        self.route = self.load_route(unique_id)  # 加载指定的路线图
        self.current_index = 0  # 用于确认运行方向
        self.pos = None  # 在网格中运行的初始位置
        self.unique_id = unique_id
        self.backward = 0  # 到达终点后返程

    def get_route_name(self, unique_id: int) -> str:
        """
        从文件名中提取 route_name。

        参数：
        - unique_id: 用于选择文件的索引

        返回：
        - route_name: 提取的路线名称
        """
        folder_path = './route_grid'
        # 获取文件夹中的所有.npy文件路径（排除 _pycache 文件夹）
        route_files = sorted(glob.glob(os.path.join(folder_path, '*.npy')))

        # 确保索引有效
        if unique_id < 0 or unique_id >= len(route_files):
            raise IndexError(f"索引 {unique_id} 超出范围 (0-{len(route_files) - 1})")

        # 获取第 unique_id 个文件
        route_file_path = route_files[unique_id]

        # 从文件路径中提取文件名（不包括路径）
        file_name = os.path.basename(route_file_path)

        # 使用正则表达式提取 route_name（即文件名的后半部分）
        match = re.search(r'(\d+)_([\s\S]+).npy', file_name)

        if match:
            # 提取出路由名称部分
            return match.group(2)  # 返回第二组，路由名称
        else:
            raise ValueError(f"文件名 {file_name} 格式不符合预期。")

    def load_route(self, unique_id: int):
        """
        根据 unique_id 从 ./route_grid 文件夹中加载对应的路线图文件。

        参数：
        - unique_id: 用于选择文件的索引

        返回：
        - route: 读取的路线网格数据
        """
        folder_path = './route_grid'
        # 获取文件夹中的所有.npy文件路径（排除 _pycache 文件夹）
        route_files = sorted(glob.glob(os.path.join(folder_path, '*.npy')))

        # 确保索引有效
        if unique_id < 0 or unique_id >= len(route_files):
            raise IndexError(f"索引 {unique_id} 超出范围 (0-{len(route_files) - 1})")

        # 获取第 unique_id 个文件
        route_file_path = route_files[unique_id]

        # 读取 .npy 文件内容
        route = np.load(route_file_path)  # 读取为 NumPy 数组

        return route

    #
    #放到环境里
    # def readsite(self):
    #     with open('site.geojson', 'r', encoding='utf-8') as file:
    #         data = json.load(file)
    #         index = 0
    #         pos = []
    #         while index < len(data['features']):
    #             pos.append(data['features'][index]['geometry']['coordinates'])
    #             index = index + 1
    #         return pos


    # def move_by_route_back(self) -> None:
    #     if self.current_index > 0:
    #         self.current_index -= 1
    #         self.pos = self.route[self.current_index]
    #     else:
    #         print("Reached the end of the route. go front.")
    #         self.backward = 0
    # def move_by_route_front(self) -> None:
    #     """沿路线行驶"""
    #     if self.current_index < len(self.route) - 1 :
    #         self.current_index += 1
    #         self.pos = self.route[self.current_index]
    #         # print(f"Moved to position {self.pos}.")
    #     else:
    #         print("Reached the end of the route. go back.")
    #         self.backward = 1
    #
    #
    # def stop_for_site(self) -> None:
    #     #行驶到站点附近后停靠
    #     site = self.readsite()
    #     proj_in = Proj(init='epsg:4326')  # WGS84
    #     proj_out = Proj(init='epsg:32650')  # UTM Zone 50N
    #     grid_size = 10
    #     latitudes = [point[0] for point in site]
    #     longitudes = [point[1] for point in site]
    #     y_coords,x_coords = transform(proj_in, proj_out, latitudes, longitudes)
    #     agent_y,agent_x = transform(proj_in, proj_out, self.pos[0], self.pos[1])
    #     x_coords = np.array(x_coords)
    #     y_coords = np.array(y_coords)
    #     x_min = min(min(x_coords),agent_x)
    #     y_min = min(min(y_coords),agent_y)
    #     site_x = ((x_coords - x_min) / grid_size).astype(int)
    #     site_y = ((y_coords - y_min) / grid_size).astype(int)
    #     pos_x = ((agent_x - x_min) / grid_size).astype(int)
    #     pos_y = ((agent_y - x_min) / grid_size).astype(int)
    #
    #     grid_x_size = max(max(site_x),pos_x) + 1
    #     grid_y_size = max(max(site_y),pos_y) + 1
    #     site_grid = np.zeros((grid_x_size, grid_y_size),dtype=int)
    #     for x, y in zip(site_x, site_y):
    #         site_grid[x, y] = 1  #
    #     # print(type(site_grid[0, 0]))
    #     #将站点存入网格，并且将agent当前位置转化成网格形式，只需要判定agent指定的格是否为1即可
    #
    #     # np.savetxt('matrix.txt', site_grid, fmt='%d',delimiter=',')
    #     # np.savetxt('matrix.csv', site_grid, delimiter=',')
    #     if site_grid[0][0] == 1:
    #         print('Get to a site,stop for a while')
    #         self.pos = self.route[self.current_index]
    #     else:
    #         self.move_by_route_front()
    #
    #
    #
    #
    # def step(self) -> None:
    #     global backward
    #     if self.backward == 0:
    #          # print(f"Hi, I am a bus agent, ID: {str(self.route_name)}.")
    #         self.move_by_route_front()
    #          # self.stop_for_site()
    #     else:
    #         self.move_by_route_back()

