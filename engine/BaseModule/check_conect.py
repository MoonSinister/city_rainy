#用于检测route连通性
import numpy as np
from collections import deque

# 定义8个方向，分别为上下左右四个方向和四个对角线方向
directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]


def in_bounds(x, y, n):
    """ 检查坐标 (x, y) 是否在矩阵内 """
    return 0 <= x < n and 0 <= y < n


def bfs(matrix, visited, x, y, n):
    """ 使用 BFS 查找连通分量 """
    queue = deque([(x, y)])
    visited[x][y] = True
    component = [(x, y)]

    while queue:
        cx, cy = queue.popleft()
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if in_bounds(nx, ny, n) and not visited[nx][ny] and matrix[nx][ny] == 1:
                visited[nx][ny] = True
                queue.append((nx, ny))
                component.append((nx, ny))

    return component


def check_connectivity(matrix):
    """ 检查矩阵是否连通 """
    n = matrix.shape[0]
    visited = np.zeros((n, n), dtype=bool)
    components = []

    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 1 and not visited[i, j]:
                component = bfs(matrix, visited, i, j, n)
                components.append(component)

    return components


def make_connected(matrix):
    """ 如果矩阵不连通，找到最小改变的方式使其连通 """
    components = check_connectivity(matrix)

    if len(components) == 1:
        return "correct"  # 已经连通

    # 找到最小的改变，通过将 0 变为 1 使其连接
    n = matrix.shape[0]
    min_changes = []

    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 0:
                # 临时将 (i, j) 置为 1，检查它连接的区域
                matrix[i, j] = 1
                new_components = check_connectivity(matrix)
                if len(new_components) < len(components):
                    min_changes.append((i, j))
                # 恢复原状
                matrix[i, j] = 0

    if min_changes:
        return min_changes
    else:
        return "No valid changes found"


# 读取指定路径的文件
file_path = './route_grid/1_826路(合肥道--大寺新家园公交站).npy'

try:
    matrix = np.load(file_path)
    result = make_connected(matrix)
    print(result)
except Exception as e:
    print(f"Error loading the file: {e}")
