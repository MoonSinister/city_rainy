import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Proj, transform
from scipy.sparse import lil_matrix

# 读取CSV文件
df = pd.read_csv('route_map/points.csv')

# 筛选type为4的数据
df_type4 = df[df['type'] == 4]

# 投影转换
proj_in = Proj(init='epsg:4326')  # WGS84
proj_out = Proj(init='epsg:32650')  # UTM Zone 50N

# 转换经纬度为平面坐标
latitudes = df_type4['latitude'].tolist()
longitudes = df_type4['longitude'].tolist()

y_coords,x_coords= transform(proj_in, proj_out, longitudes, latitudes)

x_coords = np.array(x_coords)
y_coords = np.array(y_coords)

x_min = min(x_coords)
y_min = min(y_coords)

# 计算网格索引
grid_size = 100  # 假设网格大小为1米
path_x = ((x_coords - x_min) / grid_size).astype(int)
path_y = ((y_coords - y_min) / grid_size).astype(int)

grid_x_size = max(path_x) + 1
grid_y_size = max(path_y) + 1
# 确定积水深度的全局最大值


# 为每个时间点生成积水矩阵，并可视化
for hour in range(1, 17):


    column_name = f'{hour:02d}h'

    # 提取每个点的积水深度
    depths = df_type4[column_name].tolist()

    #将积水深度放入矩阵
    grid = np.zeros((grid_x_size, grid_y_size))
    i=0
    for x, y in zip(path_x, path_y):
        grid[x, y] = grid[x,y] + depths[i]  # 储存为稀疏矩阵
        i = i+1
    values = []
    for x, y in zip(path_x, path_y):
        values.append(grid[x,y])
    max_depth = np.max(grid)
    # 绘制散点图
    plt.figure(figsize=(25, 25))
    plt.title(f'Time: {column_name}')
    scatter = plt.scatter(path_x, path_y, c=values, cmap='turbo', s=50, edgecolor='k', vmin=0, vmax=max_depth)
    plt.colorbar(scatter, label='Flooding Depth (m)')
    plt.xlabel('X Index')
    plt.ylabel('Y Index')
    plt.grid(True)
    plt.savefig(f'flooding_depth_scatter_{column_name}.png')
    plt.close()

print("生成完毕")
