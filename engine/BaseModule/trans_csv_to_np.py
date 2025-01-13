import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os


def redistribute_matrix(matrix):
    """
    对矩阵进行操作，每个节点保留一半的值，其余一半分配到周围8个邻居节点。

    参数:
        matrix (2D array): 输入的矩阵

    返回:
        2D array: 处理后的矩阵
    """
    rows, cols = matrix.shape

    # 创建一个新的矩阵来存放操作后的结果
    new_matrix = np.copy(matrix)

    # 邻居位置的相对坐标
    neighbors_offsets = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # 遍历矩阵中的每个元素
    for i in range(rows):
        for j in range(cols):
            # 当前节点的值
            value = matrix[i, j]

            # 保留一半的值
            retained_value = value / 2

            # 更新当前节点的值
            new_matrix[i, j] = retained_value

            # 剩余的一半值
            distribute_value = value / 2

            # 将剩余的值均匀分配给8个邻居
            for di, dj in neighbors_offsets:
                ni, nj = i + di, j + dj

                # 检查邻居是否在矩阵范围内
                if 0 <= ni < rows and 0 <= nj < cols:
                    new_matrix[ni, nj] += distribute_value / 8

    return new_matrix


def plot_scatter_from_matrix(matrix, filename=None):
    """
    根据输入的01矩阵绘制散点图，并将图像保存为文件（可选）。
    散点图的颜色表示矩阵中数字的大小。

    参数:
        matrix (2D array): 输入的矩阵
        filename (str, 可选): 如果提供，将图像保存为指定文件

    返回:
        None
    """
    matrix = np.array(matrix)

    # 获取非零值的行和列
    rows, cols = np.where(matrix != 0)

    # 获取矩阵中的值，用于颜色映射
    values = matrix[rows, cols]

    # 绘制散点图
    plt.figure(figsize=(8, 8))
    scatter = plt.scatter(cols, rows, s=0.1,c=values, cmap='viridis', marker='o')  # 使用颜色映射
    plt.title('Scatter Plot of Binary Matrix')
    plt.xlabel('Columns')
    plt.ylabel('Rows')
    plt.colorbar(scatter)  # 添加颜色条，显示数值到颜色的映射
    plt.grid(True)

    if filename:
        plt.savefig(filename)
    else:
        plt.show()


def save_matrix_to_file(matrix, file_path):
    """
    将矩阵保存为文件（.npy 格式）。

    参数:
        matrix (2D array): 输入的矩阵
        file_path (str): 保存的文件路径

    返回:
        None
    """
    np.save(file_path, matrix)


def scale_matrix_to_integers(matrix, target_max_value=255):
    """
    将矩阵中的数据等比放大到目标最大值，并转换为整数。

    参数:
        matrix (2D array): 输入的矩阵
        target_max_value (int): 目标最大值（默认 255）

    返回:
        2D array: 等比放大的整数矩阵
    """
    # 将输入矩阵转换为 NumPy 数组（如果它还不是）
    matrix = np.array(matrix)

    # 获取矩阵的最大值
    matrix_max = matrix.max()

    # 如果最大值为零，直接返回零矩阵
    if matrix_max == 0:
        return np.zeros_like(matrix, dtype=int)

    # 归一化矩阵到 [0, 1] 区间
    normalized_matrix = matrix / matrix_max

    # 放大到目标最大值
    scaled_matrix = normalized_matrix * target_max_value

    # 转换为整数（可以选择四舍五入或直接转换）
    integer_matrix = np.round(scaled_matrix).astype(int)

    return integer_matrix


# 假设 CSV 数据已经加载到 DataFrame 中
data = pd.read_csv('./route_map/points.csv')

# 过滤出 type 为 4 的记录
type_4_data = data[data['type'] == 4]

# 经纬度范围和步长设置
lon_min = 117.17
lon_max = 117.287
lat_min = 39.03
lat_max = 39.117

lon_step = 0.0001
lat_step = 0.0001

# 计算网格的行数和列数
num_cols = int((lon_max - lon_min) / lon_step) + 1
num_rows = int((lat_max - lat_min) / lat_step) + 1

# 初始化16个矩阵，每个矩阵对应 h01 到 h16
matrices = {f'h{str(i).zfill(2)}': np.zeros((num_rows, num_cols)) for i in range(1, 17)}

# 对 type 为 4 的每个点进行处理
for _, row in type_4_data.iterrows():
    lon = row['longitude']
    lat = row['latitude']

    # 只处理在网格范围内的点
    if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:
        # 计算列索引 (经度方向)
        col = int((lon - lon_min) / lon_step)
        # 计算行索引 (纬度方向)
        row_idx = int((lat - lat_min) / lat_step)

        # 获取该点的 h01 到 h16 数据
        for i in range(1, 17):
            h_value = row[f'h{str(i).zfill(2)}']

            # 如果该 h 值不为 0，则填充到对应的矩阵中
            if h_value != 0:
                matrices[f'h{str(i).zfill(2)}'][row_idx, col] = h_value

# 创建保存路径
output_folder = './raindata'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 打印并保存每个矩阵的散点图和矩阵文件
for i in range(1, 17):
    matrix_name = f'h{str(i).zfill(2)}'

    # 打印矩阵示例
    print(f"Matrix for {matrix_name}:")
    print(matrices[matrix_name])  # 打印部分网格矩阵

    # 先对矩阵进行分配操作
    redistributed_matrix = redistribute_matrix(matrices[matrix_name])

    # 等比放大矩阵到整数
    scaled_matrix = scale_matrix_to_integers(redistributed_matrix, target_max_value=255)

    # 绘制并保存散点图
    plot_scatter_from_matrix(scaled_matrix, filename=os.path.join(output_folder, f'{matrix_name}_scatter.png'))

    # 保存矩阵到文件
    save_matrix_to_file(scaled_matrix, file_path=os.path.join(output_folder, f'{i}.npy'))
