import numpy as np
import glob
import os
import re
from BaseModule.agent import Agent
from BaseModule.model import Model
from BaseModule.trans_json_to_np import points_to_grid
import json


class BusAgent(Agent):

    def __init__(self, unique_id: int, model: Model) -> None:
        unique_id = unique_id+1
        self.unique_id = unique_id
        self.name = self.get_route_name(unique_id)  # 从文件名中提取route_name
        self.route = self.load_route(unique_id)  # 加载指定的路线图
        self.site = self.get_pass_site(self.route)
        # self.current_index = 0  # 用于确认运行方向
        # self.backward = 0  # 到达终点后返程
    def get_route_name(self, unique_id: int) -> str:
        """
        根据unique_id从文件名中提取route_name。
        文件名格式：unique_id_路由名称.npy
        例如：1_ABC.npy 会提取出ABC作为名称。
        """
        # 设定路径为 ./route_grid 文件夹
        folder_path = './route_grid'
        pattern = os.path.join(folder_path, f"{unique_id}_*.npy")  # 匹配文件名格式，例如 "1_*.npy"
        files = glob.glob(pattern)  # 查找匹配的文件
        if not files:
            raise FileNotFoundError(f"没有找到与unique_id {unique_id} 匹配的文件。")

        # 假设文件名格式为 "unique_id_name.npy"，提取出name部分
        filename = os.path.basename(files[0])  # 取得文件的名字
        match = re.match(rf"^{unique_id}_(.*).npy$", filename)
        if match:
            return match.group(1)  # 返回提取的名称部分
        else:
            raise ValueError(f"文件名格式不正确：{filename}")

    def load_route(self, unique_id: int) -> np.ndarray:
        """
        根据unique_id加载对应的.npy文件，返回对应的矩阵数据。
        """
        # 设定路径为 ./route_grid 文件夹
        folder_path = './route_grid'
        pattern = os.path.join(folder_path, f"{unique_id}_*.npy")  # 匹配文件名格式
        files = glob.glob(pattern)  # 查找匹配的文件
        if not files:
            raise FileNotFoundError(f"没有找到与unique_id {unique_id} 匹配的文件。")

        # 假设只取第一个匹配的文件
        file_path = files[0]
        route_matrix = np.load(file_path)  # 加载.npy文件为矩阵
        return route_matrix

    def get_pass_site(self,route: np.ndarray) -> np.ndarray:

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
