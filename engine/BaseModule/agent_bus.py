import numpy as np
import glob
import os
import re
from BaseModule.agent import Agent
from BaseModule.model import Model


class BusAgent(Agent):

    def __init__(self, unique_id: int, route_id: int, model: Model) -> None:
        self.unique_id = unique_id
        route_id = route_id + 1
        self.route_id = route_id
        self.name = self.get_route_name(route_id)  # 从文件名中提取route_name
        self.route = self.init_route(route_id)  # 初始化路线
        self.site = self.get_pass_site(self.route)  # 当前路线经过的站点
        self.pos = []
        self.visited = set()  # 用于记录物体已访问的坐标
        rows, cols = np.where(self.site != 0)
        if rows.size > 0:
            self.pos = (int(rows[0]), int(cols[0]))  # agent初始位置，从某个车站开始移动

    def get_route_name(self, route_id: int) -> str:
        """
        根据route_id从文件名中提取route_name。
        文件名格式：route_id_路由名称.npy
        例如：1_ABC.npy 会提取出ABC作为名称。
        """
        # 设定路径为 ./route_grid 文件夹
        folder_path = './route_grid'
        pattern = os.path.join(folder_path, f"{route_id}_*.npy")  # 匹配文件名格式，例如 "1_*.npy"
        files = glob.glob(pattern)  # 查找匹配的文件
        if not files:
            raise FileNotFoundError(f"没有找到与route_id {route_id} 匹配的文件。")

        # 假设文件名格式为 "route_id_name.npy"，提取出name部分
        filename = os.path.basename(files[0])  # 取得文件的名字
        match = re.match(rf"^{route_id}_(.*).npy$", filename)
        if match:
            return match.group(1)  # 返回提取的名称部分
        else:
            raise ValueError(f"文件名格式不正确：{filename}")

    def init_route(self, route_id: int) -> np.ndarray:
        """
        根据route_id加载对应的.npy文件，返回对应的矩阵数据。
        """
        # 设定路径为 ./route_grid 文件夹
        folder_path = './route_grid'
        pattern = os.path.join(folder_path, f"{route_id}_*.npy")  # 匹配文件名格式
        files = glob.glob(pattern)  # 查找匹配的文件
        if not files:
            raise FileNotFoundError(f"没有找到与route_id {route_id} 匹配的文件。")

        # 假设只取第一个匹配的文件
        file_path = files[0]
        route_matrix = np.load(file_path)  # 加载.npy文件为矩阵
        return route_matrix

    def get_pass_site(self, route: np.ndarray) -> np.ndarray:
        site_path = './route_grid/site.npy'
        if not os.path.exists(site_path):
            raise FileNotFoundError(f"没有找到文件：{site_path}")

        # 加载site.npy矩阵
        site_matrix = np.load(site_path)

        # 检查site和route是否形状相同
        if site_matrix.shape != route.shape:
            raise ValueError("site矩阵和route矩阵的形状不一致！")

        # 找到site和route中都为1的位置
        pass_site_mask = (site_matrix == 1) & (route == 1)

        # 生成一个新的矩阵，只有符合条件的点为1，其他点为0
        result_matrix = np.zeros_like(route)
        result_matrix[pass_site_mask] = 1  # 设置符合条件的位置为1

        return result_matrix

    def step(self) -> None:
        """
        物体向可行的方向移动一步。

        如果物体可以移动，则更新位置。如果没有可以移动的方向，返回 None 表示终止。
        """
        print(f"当前物体位置: {self.pos}")
        row, col = self.pos

        # 尝试八个方向
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_row, new_col = row + dx, col + dy

            # 检查新位置是否在矩阵内且为路径 (即值为 1)，并且未访问过
            if (0 <= new_row < self.route.shape[0] and  # 行索引有效
                    0 <= new_col < self.route.shape[1] and  # 列索引有效
                    self.route[new_row, new_col] != 0 and  # 是路径
                    (new_row, new_col) not in self.visited):  # 未访问过该位置

                # 更新物体的位置
                self.visited.add(self.pos)
                self.pos = (new_row, new_col)
                # 更新已访问的位置
                # print(f"物体移动到新位置: {self.pos}")
                return  # 成功移动，退出方法

        # 如果没有合法的移动方向，清空 visited 并输出 no route
        # print("no route")
        self.visited = set()  # 清空 visited 集合以便物体可以返回
