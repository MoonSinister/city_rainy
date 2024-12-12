from __future__ import annotations
import random
from typing import Any
from BaseModule.datacollection import DataCollector


# 用来控制模型的一个时间步
class Model:

    """创建一个新的模型对象(object)"""
    def __new__(cls, *args: Any, **kwargs: Any) -> Any:
        obj = object.__new__(cls)
        obj._seed = kwargs.get("seed", None)
        obj.random = random.Random(obj._seed)
        return obj

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Attributes:
            schedule: 表格对象
            running: 用于判断当前的模型是否继续运行
        """
        self.running = True
        self.schedule = None
        self.current_id = 0

    def run_model(self) -> None:
        """模型会一直运行到达到终止条件"""
        while self.running:
            self.step()

    def step(self) -> None:
        """每个时间步模型所作出的改变,此方法可以被重载"""
        print("Model step()")

    def next_id(self) -> int:
        self.current_id = self.current_id + 1
        return self.current_id

    def reset_randomizer(self, seed: int | None = None) -> None:
        """
        重置随机函数发生器
        :param seed: 一个新的种子，如果是None则使用目前的种子
        """
        if seed is None:
            seed = self._seed
        self.random.seed(seed)
        self._seed = seed

    def initialize_data_collector(
        self,
        model_reporters=None,
        agent_reporters=None,
        tables=None,
        exclude_none_values=False,
    ) -> None:
        if not hasattr(self, "schedule") or self.schedule is None:
            raise RuntimeError(
                "在初始化数据收集器之前你必须初始化时间表(self.schedule)!"
            )
        if self.schedule.get_agent_count() == 0:
            raise RuntimeError(
                "在初始化数据收集齐之前必须在时间表中添加一个agent！"
            )
        self.datacollector = DataCollector(
            model_reporters=model_reporters,
            agent_reporters=agent_reporters,
            tables=tables,
            exclude_none_values=exclude_none_values,
        )
        # 在第一次初始化过程中采集数据
        self.datacollector.collect(self)





