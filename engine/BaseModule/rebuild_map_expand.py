import numpy as np
import os


def bitwise_or_multiple_files(input_dir, output_file):
    # 获取目录中所有.npy文件
    files = [f for f in os.listdir(input_dir) if f.endswith('.npy')]

    if len(files) < 2:
        raise ValueError("There must be at least two .npy files to perform bitwise OR")

    # 初始化第一个矩阵
    result_matrix = np.load(os.path.join(input_dir, files[0]))

    # 逐个文件进行按位或操作
    for file in files[1:]:
        matrix = np.load(os.path.join(input_dir, file))

        # 确保矩阵形状一致
        if result_matrix.shape != matrix.shape:
            raise ValueError(f"Shape mismatch: {result_matrix.shape} vs {matrix.shape}")

        # 执行按位或操作
        result_matrix = np.bitwise_or(result_matrix, matrix)

    # 将结果保存到输出文件
    np.save(output_file, result_matrix)

    return result_matrix


# 示例调用
input_dir = './route_grid'  # 输入目录路径
output_file = './route_grid/tianjin_expand.npy'  # 输出结果文件

result = bitwise_or_multiple_files(input_dir, output_file)
print(result)
