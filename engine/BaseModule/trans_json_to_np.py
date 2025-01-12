import numpy as np


def bresenham(x0, y0, x1, y1, max_x, max_y):
    """
    Bresenham 线算法，用于在网格上绘制一条从 (x0, y0) 到 (x1, y1) 的线。
    返回经过的所有点的列表，确保所有点都在有效的网格范围内。
    """
    points = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        # 确保点在网格范围内
        if 0 <= x0 < max_x and 0 <= y0 < max_y:
            points.append((x0, y0))
        if x0 == x1 and y0 == y1:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy
    return points


def points_to_grid(points):
    """
    将经纬度点放入网格中，并通过插值法将所有的1连接起来。

    :param points: 点列表，格式为 [(lon1, lat1), (lon2, lat2), ...]
    :return: 网格矩阵 (2D numpy array)
    """
    lon_min = 117.17
    lon_max = 117.287
    lat_min = 39.03
    lat_max = 39.117

    lon_step = 0.0001
    lat_step = 0.0001

    # 计算网格的行数和列数
    num_cols = int((lon_max - lon_min) / lon_step) + 1
    num_rows = int((lat_max - lat_min) / lat_step) + 1

    # 初始化网格矩阵
    grid = np.zeros((num_rows, num_cols), dtype=int)

    # 将每个点放入网格中
    for i in range(len(points)):
        lon = points[i][0]
        lat = points[i][1]
        if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:
            # 计算列索引 (经度方向)
            col = int((lon - lon_min) / lon_step)
            # 计算行索引 (纬度方向)
            row = int((lat - lat_min) / lat_step)
            # 标记网格中存在路径
            grid[row, col] = 1

    # 连接相邻的1
    for i in range(1, len(points)):
        lon0 = points[i - 1][0]
        lat0 = points[i - 1][1]
        lon1 = points[i][0]
        lat1 = points[i][1]

        # 计算对应的网格索引
        col0, row0 = int((lon0 - lon_min) / lon_step), int((lat0 - lat_min) / lat_step)
        col1, row1 = int((lon1 - lon_min) / lon_step), int((lat1 - lat_min) / lat_step)

        # 获取连接这两个点的所有网格点，加入最大列数和行数限制
        line_points = bresenham(col0, row0, col1, row1, num_cols, num_rows)

        # 将这些点所在的网格标记为1
        for point in line_points:
            grid[point[1], point[0]] = 1

    return grid
