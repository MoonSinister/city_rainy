"""
    普通Agent，后续其他特殊类型的Agent都继承这个Agent
"""
from __future__ import annotations
from random import Random
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    # 避免循环引用
    from BaseModule.model import Model
    from BaseModule.physical_environment import Position


class Agent:

    def __init__(self,
                 unique_id: int,
                 model: Model
    ) -> None:
        """
        :param unique_id: 在系统运行时给每一个Agent一个独一无二的id，后续在进行可视化时需要导出
        """
        self.unique_id = unique_id
        self.pos: Position | None = None
        self.model = model

    # Agent行动的一步
    def step(self) -> None:
        print(f"Hi, I am an pre-agent, you can call me {str(self.unique_id)}.")

    def advance(self) -> None:
        """Agent并行运行时会用到，暂时不定义"""
        pass

    @property
    def random(self) -> Random:
        return self.model.random


