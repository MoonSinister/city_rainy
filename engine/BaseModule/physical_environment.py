"""
物理环境模块，其中包含网格、连续空间
"""

from __future__ import annotations
import itertools
import math
from numbers import Real
from warnings import warn
from pyproj import Proj, transform
""" 用于将经纬度转换为UTM二维坐标系"""


import numpy as np
import numpy.typing as npt
import networkx as nx
import collections
import matplotlib.pyplot as plt

from BaseModule.bus_agent import BusAgent
from BaseModule.agent import Agent
from typing import (
    Tuple,
    Union,
    Any,
    overload,
    Sequence,
    cast,
    Iterator,
    TypeVar,
    Callable,
    Iterable,
    List
)

# 坐标轴
Coordinate = Tuple[int, int]
FloatCoordinate = Union[Tuple[float, float], npt.NDArray[float]]
NetworkCoordinate = int
Position = Union[Coordinate, FloatCoordinate, NetworkCoordinate]

GridContent = Union[Agent, None]
MultiGridContent = List[Agent]

_types_integer = (int, np.integer)

F = TypeVar("F", bound=Callable[..., Any])


def is_integer(x: Real) -> bool:
    # 判断x是CPython整数还是Numpy整数
    return isinstance(x, _types_integer)


def accept_tuple_argument(wrapped_function: F) -> F:
    """允许用户处理(x,y)元组列表"""

    def wrapper(grid_instance, positions) -> Any:
        if isinstance(positions, tuple) and len(positions) == 2:
            return wrapped_function(grid_instance, [positions])
        else:
            return wrapped_function(grid_instance, positions)

    return cast(F, wrapper)


class _Grid:
    """ 矩形网格的基类

    网格单元按照[x, y]来索引，[0, 0]是网格的左下角，[width-1, length-1]是网格的右上角
    （可以考虑环形网格，在这里暂时不考虑，后续添加可以考虑）
    """

    def __init__(self, width: int, height: int, torus: bool) -> None:
        """
        :param width: 网格的宽度
        :param height: 网格的高度
        :param torus: 是否是环形网格
        """
        self.width = width
        self.height = height
        self.torus = torus
        self.num_cells = width * height

        self._grid: list[list[GridContent]]
        self._grid = [
            [self.default_val() for _ in range(self.height)] for _ in range(self.width)
        ]

        # 空集是否创建的标志
        self._empties_built = False
        # 邻居缓存
        self._neighborhood_cache: dict[Any, list[Coordinate]] = {}
        # 在self.move_to_empty中使用的截止(具体的没太看懂)
        self.cutoff_empties = 7.935 * self.num_cells ** 0.384

    @staticmethod
    def default_val() -> None:
        """在创建时的默认值"""
        return None

    @property
    def empties(self) -> set:
        if self._empties_built:
            self.build_empties()
        return self._empties

    def build_empties(self) -> None:
        self._empties = set(
            filter(
                self.is_cell_empty,
                itertools.product(range(self.width), range(self.height))
            )
        )
        self._empties_built = True

    def is_cell_empty(self, pos: Coordinate) -> bool:
        x, y = pos
        return self._grid[x][y] == self.default_val()

    @overload
    def __getitem__(self, index: int | Sequence[Coordinate]) -> list[GridContent]:
        ...

    @overload
    def __getitem__(
            self, index: tuple[int | slice, int | slice]
    ) -> GridContent | list[GridContent]:
        ...

    def __getitem__(self, index):
        """从网格中获取内容"""
        if isinstance(index, int):
            """一维网格, grid[x]"""
            return self._grid[index]
        elif isinstance(index[0], tuple):
            """二维网格, grid[(x1, y1), (x2, y2), ...]"""
            index = cast(Sequence[Coordinate], index)
            return [self._grid[x][y] for x, y in map(self.torus_adj, index)]
        x, y = index
        x_int, y_int = is_integer(x), is_integer(y)
        if x_int and y_int:
            # grid[x, y]
            index = cast(Coordinate, index)
            x, y = self.torus_adj(index)
            return self._grid[x][y]
        elif x_int:
            # grid[x: ]
            x, _ = self.torus_adj((x, 0))
            y = cast(slice, y)
            return self._grid[x][y]
        elif y_int:
            # grid[:, y]
            _, y = self.torus_adj((0, y))
            x = cast(slice, x)
            return [rows[y] for rows in self._grid[x]]
        else:
            # grid[:, :]
            x, y = cast(cast(slice, x), cast(slice, y))
            return [cell for rows in self._grid[x] for cell in rows[y]]

    """环形网格，暂时用不到"""

    def torus_adj(self, pos: Coordinate) -> Coordinate:
        """转换坐标，处理环面循环"""
        if not self.out_of_bounds(pos):
            return pos
        elif not self.torus:
            raise Exception("Point out of bounds, and space non-toroidal.")
        else:
            return pos[0] % self.width, pos[1] % self.height

    def out_of_bounds(self, pos: Coordinate) -> bool:
        """确定坐标是否脱离网格"""
        x, y = pos
        return x < 0 or x >= self.width or y < 0 or y >= self.height

    def __iter__(self) -> Iterator[GridContent]:
        """将网格的行衔接在一起的迭代器，使其类似于一个列表"""
        return itertools.chain(*self._grid)

    def coord_iter(self) -> Iterator[tuple[GridContent, Coordinate]]:
        """返回位置，以及相应位置内容的迭代器"""
        for row in range(self.width):
            for col in range(self.height):
                yield self._grid[row][col], (row, col)  # Agent, position

    def iter_neighborhood(
            self,
            pos: Coordinate,
            moore: bool,
            include_center: bool = False,
            radius: int = 1
    ) -> Iterator[Coordinate]:
        """
        :param pos: 需要获得邻居的坐标
        :param moore: 如果是True则返回Moore邻居，如果是False则返回冯诺依曼邻居
        :param include_center:如果是True则返回时包括(x,y)单元，如果是False则返回时只包括邻居单元
        :param radius:在单元格中要得到邻居的半径
        :return: 返回给定点邻居的迭代器
        """
        yield from self.get_neighborhood(pos, moore, include_center, radius)

    def get_neighborhood(
            self,
            pos: Coordinate,
            moore: bool,
            include_center: bool = False,
            radius: int = 1
    ) -> list[Coordinate]:
        """
        :param pos: 目标点
        :param moore: True则获得8个邻居，False则获得4个邻居
        :param include_center: 是否包含中心点
        :param radius: 邻居半径
        :return: 返回中心点的邻居节点
        """
        catch_key = (pos, moore, include_center, radius)
        neighborhood = self._neighborhood_cache.get(catch_key, None)

        if neighborhood is not None:
            return neighborhood

        if self.out_of_bounds(pos):
            raise Exception("所给点超出边界范围！")

        neighborhood = []

        x, y = pos
        if self.torus:
            """
            
            这部分没太搞懂，环形区域内寻找邻居
            
            """
            x_max_radius, y_max_radius = self.width // 2, self.height // 2
            x_radius, y_radius = max(radius, x_max_radius), max(radius, y_max_radius)
            # 对于每一个维度，在边缘的情况下半径应该尽可能的大，维度是偶数时需要缩小一个范围的值，以避免在领域重复
            xdim_even, ydim_even = (self.width + 1) % 2, (self.height + 1) % 2
            kx = int(x_radius == x_max_radius and xdim_even)
            ky = int(y_radius == y_max_radius and ydim_even)

            for dx in range(-x_radius, x_radius + 1 - kx):
                for dy in range(-y_radius, y_radius + 1 - ky):
                    if not moore and abs(dx) + abs(dy) > radius:
                        continue

                    nx, ny = (x + dx) % self.width, (y + dy) % self.height
                    neighborhood.append((nx, ny))
        else:
            x_range = range(max(0, x - radius), min(self.width, x + radius + 1))
            y_range = range(max(0, y - radius), min(self.height, y + radius + 1))

            for nx in x_range:
                for ny in y_range:
                    if not moore and abs(nx - x) + abs(ny - y) > radius:
                        continue

                    neighborhood.append((nx, ny))

        if not include_center:
            neighborhood.remove(pos)

        self._neighborhood_cache[catch_key] = neighborhood
        return neighborhood

    def iter_neighbors(
            self,
            pos: Coordinate,
            moore: bool,
            include_center: bool = False,
            radius: int = 1
    ) -> Iterator[Agent]:
        neighborhood = self.get_neighborhood(pos, moore, include_center, radius)
        return self.iter_cell_list_contents(neighborhood)

    def get_neighbors(
            self,
            pos: Coordinate,
            moore: bool,
            include_center: bool = False,
            radius: int = 1
    ) -> list[Agent]:
        return list(self.iter_neighbors(pos, moore, include_center, radius))

    @accept_tuple_argument
    def iter_cell_list_contents(self, cell_list: Iterable[Coordinate]) -> Iterator[Agent]:
        """返回网格中Agent的迭代器，空网格将会被忽略"""
        return (
            self._grid[x][y]
            for x, y in itertools.filterfalse(self.is_cell_empty, cell_list)
        )

    @accept_tuple_argument
    def get_cell_list_contents(self, cell_list: Iterable[Coordinate]) -> list[Agent]:
        return list(self.iter_cell_list_contents(cell_list))

    def place_agent(self, agent: Agent, pos: Coordinate) -> None:
        ...

    def remove_agent(self, agent: Agent) -> None:
        ...

    def move_agent(self, agent: Agent, pos: Coordinate) -> None:
        """把一个Agent从当前位置移动到另一个位置"""
        pos = self.torus_adj(pos)
        self.remove_agent(agent)
        self.place_agent(agent, pos)

    def swap_pos(self, agent_a: Agent, agent_b: Agent) -> None:
        """交换两个Agent的位置"""
        agents_no_pos = []
        if (pos_a := agent_a.pos) is None:
            agents_no_pos.append(agent_a)
        if (pos_b := agent_b.pos) is None:
            agents_no_pos.append(agent_b)
        if agents_no_pos:
            agents_no_pos = [f"<Agent id: {a.unique_id}>" for a in agents_no_pos]
            raise Exception(f"{', '.join(agents_no_pos)} - not on the grid")

        if pos_a == pos_b:
            return

        self.remove_agent(agent_a)
        self.remove_agent(agent_b)
        self.place_agent(agent_a, pos_b)
        self.place_agent(agent_b, pos_a)

    def move_to_empty(self, agent: Agent) -> None:
        """把Agent随机移动到一个空单元"""
        num_empty_cells = len(self.empties)
        if num_empty_cells == 0:
            raise Exception("Error! 没有空单元！")

        if num_empty_cells > self.cutoff_empties:
            while True:
                new_pos = (
                    agent.random.randrange(self.width),
                    agent.random.randrange(self.height)
                )
                if self.is_cell_empty(new_pos):
                    break
        else:
            new_pos = agent.random.choice(sorted(self.empties))

        self.remove_agent(agent)
        self.place_agent(agent, new_pos)

    def exists_empty_cells(self) -> bool:
        """返回是否还有空单元"""
        return len(self.empties) > 0


class SingleGrid(_Grid):
    """
    长方形的网格，并且每个网格单元中只允许有一个Agent
    网格单元按照[x, y]来索引，[0, 0]是网格的左下角，[width-1, length-1]是网格的右上角
    """

    def place_agent(self, agent: Agent, pos: Coordinate) -> None:
        """在网格单元中放置一个Agent，并且位置是可变的"""
        if self.is_cell_empty(pos):
            x, y = pos
            self._grid[x][y] = agent
            if self._empties_built:
                self._empties.discard(pos)
            agent.pos = pos
        else:
            raise Exception("该单元格非空！")

    def remove_agent(self, agent: Agent) -> None:
        """把Agent从单元格中移出并将该单元格设置为空"""
        if (pos := agent.pos) is None:
            return
        x, y = pos
        # self._grid[x][y] = self.default_val()
        self._grid[x][y] = None
        if self._empties_built:
            self._empties.add(pos)
        agent.pos = None


class MultiGrid(_Grid):
    """
    长方形的网格，并且每个网格单元中允许有多个Agent
    网格单元按照[x, y]来索引，[0, 0]是网格的左下角，[width-1, length-1]是网格的右上角
    """
    grid: list[list[MultiGridContent]]

    @staticmethod
    def default_val() -> MultiGridContent:
        """新的单元格的默认值"""
        return []

    def place_agent(self, agent: Agent, pos: Coordinate) -> None:
        x, y = pos
        if agent.pos is None or agent not in self._grid[x][y]:
            self._grid[x][y].append(agent)
            agent.pos = pos
            if self._empties_built:
                self._empties.discard(pos)

    def remove_agent(self, agent: Agent) -> None:
        """把Agent从单元格中移出"""
        pos = agent.pos
        x, y = pos
        self._grid[x][y].remove(agent)
        if self._empties_built and self.is_cell_empty(pos):
            self._empties.add(pos)
        agent.pos = None

    @accept_tuple_argument
    def iter_cell_list_contents(self, cell_list: Iterable[Coordinate]) -> Iterator[Agent]:
        return itertools.chain.from_iterable(
            self._grid[x][y]
            for x, y in itertools.filterfalse(self.is_cell_empty, cell_list)
        )


"""

六边形网格后续有时间再补充

"""


class _HexGrid:
    """Hexagonal Grid which handles hexagonal neighbors.

    Functions according to odd-q rules.
    See http://www.redblobgames.com/grids/hexagons/#coordinates for more.

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether to treat the grid as a torus.

    Methods:
        get_neighbors: Returns the objects surrounding a given cell.
        get_neighborhood: Returns the cells surrounding a given cell.
        iter_neighbors: Iterates over position neighbors.
        iter_neighborhood: Returns an iterator over cell coordinates that are
            in the neighborhood of a certain point.
    """

    def torus_adj_2d(self, pos: Coordinate) -> Coordinate:
        return pos[0] % self.width, pos[1] % self.height

    def get_neighborhood(
        self, pos: Coordinate, include_center: bool = False, radius: int = 1
    ) -> list[Coordinate]:
        """Return a list of coordinates that are in the
        neighborhood of a certain point. To calculate the neighborhood
        for a HexGrid the parity of the x coordinate of the point is
        important, the neighborhood can be sketched as:

            Always: (0,-), (0,+)
            When x is even: (-,+), (-,0), (+,+), (+,0)
            When x is odd:  (-,0), (-,-), (+,0), (+,-)

        Args:
            pos: Coordinate tuple for the neighborhood to get.
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of coordinate tuples representing the neighborhood. For
            example with radius 1, it will return list with number of elements
            equals at most 9 (8) if Moore, 5 (4) if Von Neumann (if not
            including the center).
        """
        cache_key = (pos, include_center, radius)
        neighborhood = self._neighborhood_cache.get(cache_key, None)

        if neighborhood is not None:
            return neighborhood

        queue = collections.deque()
        queue.append(pos)
        coordinates = set()

        while radius > 0:
            level_size = len(queue)
            radius -= 1

            for _i in range(level_size):
                x, y = queue.pop()

                if x % 2 == 0:
                    adjacent = [
                        (x, y - 1),
                        (x, y + 1),
                        (x - 1, y + 1),
                        (x - 1, y),
                        (x + 1, y + 1),
                        (x + 1, y),
                    ]
                else:
                    adjacent = [
                        (x, y - 1),
                        (x, y + 1),
                        (x - 1, y),
                        (x - 1, y - 1),
                        (x + 1, y),
                        (x + 1, y - 1),
                    ]

                if self.torus:
                    adjacent = [
                        coord
                        for coord in map(self.torus_adj_2d, adjacent)
                        if coord not in coordinates
                    ]
                else:
                    adjacent = [
                        coord
                        for coord in adjacent
                        if not self.out_of_bounds(coord) and coord not in coordinates
                    ]

                coordinates.update(adjacent)

                if radius > 0:
                    queue.extendleft(adjacent)

        if include_center:
            coordinates.add(pos)
        else:
            coordinates.discard(pos)

        neighborhood = sorted(coordinates)
        self._neighborhood_cache[cache_key] = neighborhood

        return neighborhood

    def iter_neighborhood(
        self, pos: Coordinate, include_center: bool = False, radius: int = 1
    ) -> Iterator[Coordinate]:
        """Return an iterator over cell coordinates that are in the
        neighborhood of a certain point.

        Args:
            pos: Coordinate tuple for the neighborhood to get.
            include_center: If True, return the (x, y) cell as well.
                            Otherwise, return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            An iterator of coordinate tuples representing the neighborhood.
        """
        yield from self.get_neighborhood(pos, include_center, radius)

    def iter_neighbors(
        self, pos: Coordinate, include_center: bool = False, radius: int = 1
    ) -> Iterator[Agent]:
        """Return an iterator over neighbors to a certain point.

        Args:
            pos: Coordinates for the neighborhood to get.
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            An iterator of non-None objects in the given neighborhood
        """
        neighborhood = self.get_neighborhood(pos, include_center, radius)
        return self.iter_cell_list_contents(neighborhood)

    def get_neighbors(
        self, pos: Coordinate, include_center: bool = False, radius: int = 1
    ) -> list[Agent]:
        """Return a list of neighbors to a certain point.

        Args:
            pos: Coordinate tuple for the neighborhood to get.
            include_center: If True, return the (x, y) cell as well.
                            Otherwise,
                            return surrounding cells only.
            radius: radius, in cells, of neighborhood to get.

        Returns:
            A list of non-None objects in the given neighborhood
        """
        return list(self.iter_neighbors(pos, include_center, radius))


class HexSingleGrid(_HexGrid, SingleGrid):
    """Hexagonal SingleGrid: a SingleGrid where neighbors are computed
    according to a hexagonal tiling of the grid.

    Functions according to odd-q rules.
    See http://www.redblobgames.com/grids/hexagons/#coordinates for more.

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether to treat the grid as a torus.
    """


class HexMultiGrid(_HexGrid, MultiGrid):
    """Hexagonal MultiGrid: a MultiGrid where neighbors are computed
    according to a hexagonal tiling of the grid.

    Functions according to odd-q rules.
    See http://www.redblobgames.com/grids/hexagons/#coordinates for more.

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether to treat the grid as a torus.
    """


class HexGrid(HexSingleGrid):
    """Hexagonal Grid: a Grid where neighbors are computed
    according to a hexagonal tiling of the grid.

    Functions according to odd-q rules.
    See http://www.redblobgames.com/grids/hexagons/#coordinates for more.

    Properties:
        width, height: The grid's width and height.
        torus: Boolean which determines whether to treat the grid as a torus.
    """

    def __init__(self, width: int, height: int, torus: bool) -> None:
        super().__init__(width, height, torus)
        warn(
            (
                "HexGrid is being deprecated; use instead HexSingleGrid or HexMultiGrid "
                "depending on your use case."
            ),
            DeprecationWarning,
            stacklevel=2,
        )


class ContinuousSpace:
    """
    在连续空间中，每个Agent可以有任意的位置
    Agent的位置存储在(x,y)元组中
    """

    def __init__(
            self,
            x_max: float,
            y_max: float,
            torus: bool,
            x_min: float = 0,
            y_min: float = 0
    ) -> None:
        """
        创建一个新的连续空间
        :param x_max: x坐标的最大值
        :param y_max: y坐标的最大值
        :param torus: 是否是环形
        :param x_min: x坐标的最小值（默认值为0）
        :param y_min: y坐标的最小值（默认值为0）
        """
        self.x_min = x_min
        self.x_max = x_max
        self.width = x_max - x_min
        self.y_min = y_min
        self.y_max = y_max
        self.height = y_max - y_min
        self.center = np.array(((x_max + x_min) / 2, (y_max + y_min) / 2))
        self.size = np.array((self.width, self.height))
        self.torus = torus

        self._agent_points: npt.NDArray[FloatCoordinate] | None = None
        self._index_to_agent: dict[int, Agent] = {}
        self._agent_to_index: dict[Agent, int | None] = {}

    def _build_agent_cache(self):
        """将Agent的位置存入缓存中，加速运算"""
        self._index_to_agent = {}
        for idx, agent in enumerate(self._agent_to_index):
            self._agent_to_index[agent] = idx
            self._index_to_agent[idx] = agent

        self._agent_points = np.array([agent.pos for agent in self._agent_to_index])

    def _invalidate_agent_cache(self):
        """清除空间中Agent和位置信息的缓存"""
        self._agent_points = None
        self._index_to_agent = {}

    def place_agent(self, agent: Agent, pos: FloatCoordinate) -> None:
        """在环境中添加一个新的Agent"""
        self._invalidate_agent_cache()
        self._agent_to_index[agent] = None
        pos = self.torus_agj(pos)
        agent.pos = pos

    def move_agent(self, agent: Agent, pos: FloatCoordinate) -> None:
        """把Agent从当前位置移动到新的位置"""
        pos = self.torus_agj(pos)
        agent.pos = pos

        if self._agent_points is not None:
            """同时需要修改缓存中的内容"""
            idx = self._agent_to_index[agent]
            self._agent_points[idx] = pos

    def remove_agent(self, agent: Agent) -> None:
        """把Agent从当前位置移开"""
        if agent not in self._agent_to_index:
            raise Exception("环境中并没有此Agent！")
        del self._agent_to_index[agent]
        self._invalidate_agent_cache()
        agent.pos = None

    def get_neighbors(
            self, pos: FloatCoordinate, radius: float, include_center: bool = True
    ) -> list[Agent]:
        """
        获得在给定原点和半径内的所有Agent
        :param pos: 原点
        :param radius: 半径
        :param include_center: 是否包含圆心 如果是True则在返回邻居时包括此圆心agent，False则不包括
        :return: 邻居Agent列表
        """
        if self._agent_points is None:
            self._build_agent_cache()

        deltas = np.abs(self._agent_points - np.array(pos))
        if self.torus:
            deltas = np.minimum(deltas, self.size - deltas)
        dists = deltas[:, 0] ** 2 + deltas[:, 1] ** 2

        (idxs,) = np.where(dists < radius ** 2)
        neighbors = [
            self._index_to_agent[x] for x in idxs if include_center or dists[x] > 0
        ]
        return neighbors

    def get_heading(
            self, pos_1=FloatCoordinate, pos_2=FloatCoordinate
    ) -> FloatCoordinate:
        """获得两点之间的向量"""
        one = np.array(pos_1)
        two = np.array(pos_2)
        heading = two - one
        if self.torus:
            """这部分暂时没搞懂，环形区域"""
            inverse_heading = heading - np.sign(heading) * self.size

            def get_min_abs(x, y):
                return x if abs(x) > abs(y) else y

            heading = tuple(
                get_min_abs(heading[i], inverse_heading[i]) for i in range(2)
            )

        if isinstance(pos_1, np.ndarray):
            heading = np.ndarray(heading)
        else:
            heading = tuple(heading)
        return heading

    def get_distance(
            self, pos_1: FloatCoordinate, pos_2: FloatCoordinate
    ) -> float:
        """计算连续中间中两点之间的距离"""
        x1, y1 = pos_1
        x2, y2 = pos_2
        dx = abs(x1 - x2)
        dy = abs(y1 - y2)

        if self.torus:
            dx = min(dx, self.width - dx)
            dy = min(dy, self.height - dy)
        return math.sqrt(dx * dx + dy * dy)

    def torus_agj(self, pos: FloatCoordinate) -> FloatCoordinate:
        """
        解决环形问题
        如果坐标超出边界且空间为环形，则返回空间内对应点
        如果空间不是环形，且坐标超出边界，则返回异常
        """
        if not self.out_of_bounds(pos):
            return pos
        elif not self.torus:
            raise Exception("坐标点超出边界范围！")
        else:
            x = self.x_min + ((pos[0] - self.x_min) % self.width)
            y = self.y_min + ((pos[1] - self.y_min) % self.height)
            if isinstance(pos, tuple):
                return (x, y)
            else:
                return np.array((x, y))

    def out_of_bounds(self, pos: FloatCoordinate) -> bool:
        """判断坐标点是否超出边界"""
        x, y = pos
        return x < self.x_min or x > self.x_max or y < self.y_min or y > self.y_max


class NetworkGrid:
    """网络单元，每个节点可以有0个或多个agent"""
    def __init__(self, g: Any) -> None:
        """
        创建一个新的网络
        :param g: 一个NetworkX网络实例
        """
        self.G = g
        for node_id in self.G.nodes:
            g.nodes[node_id]["agent"] = self.default_val()

    @staticmethod
    def default_val() -> list:
        """新节点的默认值"""
        return []

    def get_neighborhood(
            self, node_id: int, include_center: bool = False, radius: int = 1
    ) -> list[int]:
        """在给定的半径范围内获取所有的邻接节点"""
        if radius == 1:
            neighborhood = list(self.G.neighbors(node_id))
            if include_center:
                neighborhood.append(node_id)
        else:
            neighbors_with_distance = nx.single_source_shortest_path_length(
                self.G, node_id, radius
            )
            if not include_center:
                del neighbors_with_distance[node_id]
            neighborhood = sorted(neighbors_with_distance.keys())

        return neighborhood

    def get_neighbors(self, node_id: int, include_center: bool = False) -> list[Agent]:
        """获得节点上的agent"""
        neighborhood = self.get_neighborhood(node_id, include_center)
        return self.get_cell_list_contents(neighborhood)

    def place_agent(self, agent: Agent, node_id: int) -> None:
        """把agent放置到一个节点上"""
        self.G.nodes[node_id]["agent"].append(agent)
        agent.pos = node_id

    def move_agent(self, agent: Agent, node_id: int) -> None:
        """把agent从当前节点移动到另外一个新的节点"""
        self.remove_agent(agent)
        self.place_agent(agent, node_id)

    def remove_agent(self, agent: Agent) -> None:
        """把agent从当前位置移开，并且把agent的位置置为空值"""
        node_id = agent.pos
        self.G.nodes[node_id]["agent"].remove(agent)
        agent.pos = None

    def is_cell_empty(self, node_id: int) -> bool:
        """返回一个bool类型的值，表示单元中的内容是否为空"""
        return self.G.nodes[node_id]["agent"] == self.default_val()

    def get_cell_list_contents(self, cell_list: list[int]) -> list[Agent]:
        """返回节点列表中包含的agents列表，空节点将会被排除"""
        return list(self.iter_cell_list_contents(cell_list))

    def get_all_cell_contents(self) -> list[Agent]:
        """获得网络上所有的agent"""
        return self.get_cell_list_contents(self.G)

    def iter_cell_list_contents(self, cell_list: list[int]) -> Iterator[Agent]:
        """返回节点列表中节点的Agents的迭代器，空节点将会被排除"""
        return itertools.chain.from_iterable(
            self.G.nodes[node_id]["agent"]
            for node_id in itertools.filterfalse(self.is_cell_empty, cell_list)
        )


class GeoGrid:

    def __init__(self) -> None:
        """
        将路网读入网格（路网数据为坐标对列表）
        """
        # 初始化四个列表，分别用于存储路径和代理的坐标
        self.path_x = []
        self.path_y = []
        self.agent_x = []
        self.agent_y = []

        self.agentindex = []
        # 用于每个id储存其坐标对，例如id=i的agent，当前所处坐标为[self.agent_x[agentindex[1]],self.agent_y[agentindex[i]]]
        # 后期如果需要删除agent，不能直接删除agentindex中的元素

    def add_path(self,latlon_list) -> None:
        """
        将经纬度数组转换为二维网格模型。
        :param latlon_pairs: 经纬度对的列表
        :param grid_size: 网格单元的大小（以米为单位）
        :return: (x_indices, y_indices) 表示的二维网格坐标
        """
        proj_in = Proj(init='epsg:4326')  # WGS84
        proj_out = Proj(init='epsg:32650')  # UTM Zone 50N
        grid_size = 100
        latitudes = [point[0] for point in latlon_list]
        longitudes = [point[1] for point in latlon_list]

        # 转换经纬度为平面坐标
        x_coords, y_coords = transform(proj_in, proj_out, latitudes,longitudes)


        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        # 计算网格索引
        self.path_x = (x_coords / grid_size).astype(int)
        self.path_y = (y_coords / grid_size).astype(int)

    def get_path(self):
        """获取所有路径坐标"""
        return self.path_x,self.path_y

    def add_agent(self, agent: BusAgent, node_id: int) -> None:
        """
        将agent放置在初始位置,注意node_id表示第几个放入图的agent，从1开始
        """
        proj_in = Proj(init='epsg:4326')  # WGS84
        proj_out = Proj(init='epsg:32650')  # UTM Zone 50N
        grid_size = 100
        latitudes = agent.pos[0]
        longitudes = agent.pos[1]

        # 转换经纬度为平面坐标
        x_coords, y_coords = transform(proj_in, proj_out, latitudes,longitudes)


        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        # 计算网格索引
        self.agent_x.append((x_coords / grid_size).astype(int))
        self.agent_y.append((y_coords / grid_size).astype(int))

        self.agentindex.append(node_id-1)

    def move_agent(self, agent: BusAgent, latlon_list,node_id: int) -> None:
        proj_in = Proj(init='epsg:4326')  # WGS84
        proj_out = Proj(init='epsg:32650')  # UTM Zone 50N
        grid_size = 100
        latitudes = latlon_list[0]
        longitudes = latlon_list[1]

        # 转换经纬度为平面坐标
        x_coords, y_coords = transform(proj_in, proj_out, latitudes,longitudes)


        x_coords = np.array(x_coords)
        y_coords = np.array(y_coords)
        # 计算网格索引
        self.agent_x[node_id] = (x_coords / grid_size).astype(int)
        self.agent_x[node_id] = (y_coords / grid_size).astype(int)
        # 更改agent坐标



    def get_agent(self,node_id: int):
        """获取node_id的agent坐标"""
        return self.agent_x[node_id],self.agent_y[node_id]
    def visualize_grid(x_coords, y_coords):
        plt.figure(figsize=(6, 10))
        plt.scatter(x_coords, y_coords, s=0.1,c='blue', marker='o', label='Data Points')
        plt.title('Scatter plot of geographical points')
        plt.xlabel('X Coordinates (meters)')
        plt.ylabel('Y Coordinates (meters)')
        plt.grid()
        plt.legend()
        plt.show()




