import numpy as np
import matplotlib.pyplot as plt

# 示例矩阵
matrix = np.load("./route_grid/tianjin.npy")

# 找出非零元素的索引
rows, cols = np.nonzero(matrix)  # rows 是行索引，cols 是列索引

# 获取非零元素的值（可选，用于颜色或大小）
values = matrix[rows, cols]

# 绘制散点图
plt.figure(figsize=(6, 6))
plt.scatter(cols, rows, c=values, cmap='viridis', s=0.1, edgecolor='k')  # cols 是 x，rows 是 y

# 设置图形属性
plt.gca().invert_yaxis()  # 反转 y 轴，使矩阵视觉上符合行列布局
plt.colorbar(label='Value')  # 可视化值
plt.title('Scatter Plot of Matrix')
plt.xlabel('Column Index')
plt.ylabel('Row Index')
plt.grid(True)

plt.show()
