"""
    主要用于对Agent的激活，含有不同的时间模块
"""
from __future__ import annotations
from collections import defaultdict
from BaseModule.agent import Agent
from BaseModule.model import Model
from typing import Union

"""
    在BaseSchedule中time是int类型
    在StagedActivation中time是float类型
"""
timeT = Union[int, float]


class BaseScheduler:
    """
    最基本的时间表，每个Agent按照添加的顺序被激活
    """

    def __init__(self, model: Model) -> None:
        self.model = model
        self.steps = 0
        self.time: timeT = 0
        self._agents: dict[int, Agent] = {}

    def add(self, agent: Agent) -> None:
        """
        :param agent: 在时间表中添加的Agent，前提是Agent具有step()函数
        """
        if agent.unique_id in self._agents:
            raise Exception(
                f"Agent with unique id {agent.unique_id!r} already added to schedule"
            )

        self._agents[agent.unique_id] = agent

    def remove(self, agent: Agent) -> None:
        """
        移除表中所有该agent的实例
        :param agent: 被移除的agent对象
        """
        del self._agents[agent.unique_id]

    def step(self) -> None:
        """执行所有Agent的step方法，一次执行一个"""
        self.do_each("step")
        self.steps += 1
        self.time += 1

    def get_agent_count(self) -> int:
        """返回目前列表里Agent的数量"""
        return len(self._agents)

    @property
    def agents(self) -> list[Agent]:
        return list(self._agents.values())

    def get_agent_keys(self, shuffle: bool = False) -> list[int]:
        agent_keys = list(self._agents.keys())
        if shuffle:
            self.model.random.shuffle(agent_keys)
        return agent_keys

    def do_each(self, method, agent_keys=None, shuffle=False):
        if agent_keys is None:
            agent_keys = self.get_agent_keys()
        if shuffle:
            self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            if agent_key in self._agents:
                """触发相应的方法"""
                getattr(self._agents[agent_key], method)()


class RandomActivation(BaseScheduler):
    """按照Random的方式激活Agent，需要每一个Agent都有一个step()方法"""
    def step(self) -> None:
        self.do_each("step", shuffle=True)
        self.steps += 1
        self.time += 1


class SimultaneousActivation(BaseScheduler):
    """
        所有Agent同时激活，也就是并行运行
        要求Agent同时具有step()和advance()方法
    """
    def step(self) -> None:
        """step所有的Agent，然后再advance"""
        self.do_each("step")
        self.do_each("advance")
        self.steps += 1
        self.time += 1


class StagedActivation(BaseScheduler):
    def __init__(
            self,
            model: Model,
            stage_list: list[str] | None = None,
            shuffle: bool = False,
            shuffle_between_stages: bool = False
    ) -> None:
        """
        :param model: 初始化父类需要的参数
        :param stage_list: 不同等级的Agent运行列表
        :param shuffle: 如果为Ture则打乱Agent激活的顺序
        """
        super().__init__(model)
        self.stage_list = stage_list if stage_list else ["step"]
        self.shuffle = shuffle
        self.shuffle_between_stages = shuffle_between_stages
        self.stage_time = 1/len(self.stage_list)

    def step(self) -> None:
        """运行所有等级的所有Agent"""
        agent_keys = self.get_agent_keys(shuffle=self.shuffle)
        for stage in self.stage_list:
            if stage.startswith("model."):
                getattr(self.model, stage[6:])()
            else:
                self.do_each(stage, agent_keys=agent_keys)
            agent_keys = self.get_agent_keys(self.shuffle_between_stages)
            self.time += self.stage_time

        self.steps += 1


class RandomActivationByType(BaseScheduler):
    """
    在每一步激活不同类型的Agent，并且将Agent的激活顺序按照Random来打乱
    """
    def __init__(self, model: Model) -> None:
        super().__init__(model)
        self.agents_by_type = defaultdict(dict)

    def add(self, agent: Agent) -> None:
        super().add(agent)
        agent_class: type[Agent] = type(agent)
        self.agents_by_type[agent_class][agent.unique_id] = agent

    def remove(self, agent: Agent) -> None:
        del self._agents[agent.unique_id]
        agent_class: type[Agent] = type(agent)
        del self.agents_by_type[agent_class][agent.unique_id]

    def step(self, shuffle_types: bool = True, shuffle_agents: bool = True) -> None:
        type_keys: list[type[Agent]] = list(self.agents_by_type.keys())
        if shuffle_types:
            self.model.random.shuffle(type_keys)
        for agent_class in type_keys:
            self.step_type(agent_class, shuffle_agents=shuffle_agents)
        self.steps += 1
        self.time += 1

    def step_type(self, type_class: type[Agent], shuffle_agents: bool = True) -> None:
        agent_keys: list[int] = list(self.agents_by_type[type_class].keys())
        if shuffle_agents:
            self.model.random.shuffle(agent_keys)
        for agent_key in agent_keys:
            self.agents_by_type[type_class][agent_key].step()

    def get_type_count(self, type_class: type[Agent]) -> int:
        """返回给定type队列下Agent的数目"""
        return len(self.agents_by_type[type_class])









