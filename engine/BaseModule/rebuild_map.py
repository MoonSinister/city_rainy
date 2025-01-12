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


def readroute():
    with open('./tianjin.geojson', 'r', encoding='utf-8') as file:
        data = json.load(file)
    route_num = len(data['features'])
    route= []
    for i in range(route_num):
        routetype = data['features'][i]["geometry"]['type']
        # if data['features'][i]['properties']['name'] == None:
        #     print('skip')
        #     continue
        if routetype == 'LineString':
            route.append(data['features'][i]["geometry"]['coordinates'])
        elif routetype == 'MultiLineString':
            for j in range(len(data['features'][i]["geometry"]['coordinates'])):
                route.append(data['features'][i]["geometry"]['coordinates'][j])
    """ 公交线路经纬度 """
    return route


def save_realroad(realroad):
    """保存生成的realroad为.npy文件"""
    # 确保目录存在
    output_dir = './route_grid/'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    global index
    # 保存为 .npy 格式
    file_path_npy = os.path.join(output_dir, f"tianjin.npy")
    np.save(file_path_npy, realroad)
    index=index+1

def main():
    # 假设有一个函数 readroute() 返回所有路线数据
    route = readroute()  # route 是一个包含所有路线的列表
    combined_matrix = None  # 初始化为空

    for i in range(len(route)):
        map_grid = points_to_grid(route[i])  # 每次生成的矩阵
        if combined_matrix is None:
            combined_matrix = map_grid  # 初始化第一个矩阵
        else:
            combined_matrix += map_grid  # 矩阵逐步累加
        print('step: ',i)
    plot_path(combined_matrix)
        # plot_path(map_grid)
        # print(route[i])
    #现在route里还有顺序信息，直接用插值填满！！！！！！！！！！
    # route_grid = points_to_grid(route)
    # plot_path(route_grid)
    # sparse_matrix = csr_matrix(combined_matrix)
    # # 保存 realroad 到 .npy 文件
    save_realroad(combined_matrix)
    # # plot_path(realroad)
    # print(i)

if __name__ == "__main__":
    main()
