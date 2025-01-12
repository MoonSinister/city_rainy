from BaseModule.trans_json_to_np import points_to_grid
import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csr_matrix
import json
import warnings
import os

warnings.simplefilter(action='ignore', category=FutureWarning)

index = 1
def plot_path(matrix):
    matrix_np = np.array(matrix)

    # 找到值为 1 的坐标
    coordinates = np.column_stack(np.where(matrix_np == 1))

    # 创建一个绘图
    plt.figure(figsize=(6, 6))

    plt.plot(coordinates[:, 1], coordinates[:, 0], color='red', linewidth=2, marker='o', markersize=3, zorder=5)
    # 显示值为1的点，并调整点的大小
    plt.scatter(coordinates[:, 1], coordinates[:, 0], color='blue', s=1, zorder=5)  # s=100 控制点的大小

    plt.gca().invert_yaxis()  # 反转 y 轴，使得 (0, 0) 是左上角
    plt.title('Displaying 1s as large points')
    plt.show()


def readsite():
    with open('./tianjinsite.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
    site = []
    for i in range(len(data['features'])):
        site.append(data['features'][i]["geometry"]['coordinates'])

    """ 公交线路经纬度 """
    return site

def save_realroad(realroad):
    """保存生成的realroad为.npy文件"""
    # 确保目录存在
    output_dir = './route_grid/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 保存为 .npy 格式
    file_path_npy = os.path.join(output_dir, f"site.npy")
    np.save(file_path_npy, realroad)

def main():

        site = readsite()

        #现在route里还有顺序信息，直接用插值填满！！！！！！！！！！
        route_grid = points_to_grid(site)
        # plot_path(route_grid)
        # sparse_matrix = csr_matrix(route_grid)
        # 保存 realroad 到 .npy 文件
        save_realroad(route_grid)
        plot_path(route_grid)

if __name__ == "__main__":
    main()
