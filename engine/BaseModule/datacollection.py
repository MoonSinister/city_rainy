""""
    数据收集为三种字典
    1. 模型级数据：将每个记录值映射到列表
    2. agent级数据：映射每个模型步为一个列表，其中包含agent的id和其对应的值
    3. 表格：分为表格名和列
    最后，DataCollector将会从收集到的数据中创建一个pandas的DataFrame

    默认的DataCollector作出了如下假设：
    1. 模型有一个schedule对象叫做‘schedule’
    2. schedule有一个agent对象列表叫agents
    3. 在收集agent级数据时，agent必须有一个unique_id
"""
import itertools
import types
from operator import attrgetter
import pandas as pd


class DataCollector:

    def __init__(
            self,
            model_reporters=None,
            agent_reporters=None,
            tables=None,
            exclude_none_values=False
    ):
        """
        model_reporters和agent_reporters都是由字典将一个变量名映射为属性名或者一个方法
        例如，如果对于一些agents仅有一个模型级别的reporter，这将为：
            {"agent_count": lambda m: m.schedule.get_agent_count() }
        如果仅有一个agent级别的reporter(e.g. the agent's energy)，这将为：
            {"energy": "energy"}
        或者：
            {"energy": lambda a: a.energy}

        表格变量也是由字典来进行映射，将表名映射为列名列表。如果我们希望允许agent在他们被销毁的时候
        记录自己的年龄，用来记录寿命，具体写为：
            {"Lifespan": ["unique_id", "age"]}

        :param model_reporters: 名称和变量/方法之间映射的字典
        :param agent_reporters: 名称和变量/方法之间映射的字典
        :param tables: 表名和列明列表之间映射的字典
        :param exclude_none_values:布尔值，用于确定在最终结果中是否删除值为None的记录
        """

        self.model_reporters = {}
        self.agent_reporters = {}

        self.model_vars = {}
        self._agent_records = {}
        self.tables = {}
        self.exclude_none_values = exclude_none_values

        if model_reporters is not None:
            for name, reporter in model_reporters.items():
                self._new_model_reporter(name, reporter)

        if agent_reporters is not None:
            for name, reporter in agent_reporters.items():
                self._new_agent_reporter(name, reporter)

        if tables is not None:
            for name, columns in tables.items():
                self._new_table(name, columns)

    def _new_model_reporter(self, name, reporter):
        """
        在记录中添加一个新的模型级别的reporter
        :param name: 记录中模型级变量的名称
        :param reporter: 变量字符串或者函数对象，在给定模型实例后返回变量
        :return:
        """
        self.model_reporters[name] = reporter
        self.model_vars[name] = []

    def _new_agent_reporter(self, name, reporter):
        """
        在记录中添加一个新的agent级别reporter
        :param name: 记录中agent级别的变量
        :param reporter:变量字符串或者函数对象，在给定模型实例后返回变量
        :return:
        """

        if type(reporter) is str:
            attribute_name = reporter

            def reporter(agent):
                return getattr(agent, attribute_name, None)

            reporter.attribute_name = attribute_name

        self.agent_reporters[name] = reporter

    def _new_table(self, table_name, table_columns):
        """
        创建一个对象可以写的表格
        :param table_name: 新表格的名字
        :param table_columns: 添加到表格的列列表
        :return:
        """

        new_table = {column: [] for column in table_columns}
        self.tables[table_name] = new_table

    def _record_agents(self, model):
        """通过将函数与agent映射来记录agent的信息"""
        rep_funcs = self.agent_reporters.values()
        if self.exclude_none_values:
            """去除记录中为空的值"""

            def get_reports(agent):
                _prefix = (agent.model.schedule.steps, agent.unique_id)
                reports = (rep(agent) for rep in rep_funcs)
                reports_without_none = tuple(r for r in reports if r is not None)
                if len(reports_without_none) == 0:
                    return None

                return _prefix + reports_without_none

            agent_records = (get_reports(agent) for agent in model.schedule.agents)
            agent_records_without_none = (r for r in agent_records if r is not None)
            return agent_records_without_none

        if all(hasattr(rep, "attribute_name") for rep in rep_funcs):
            # 此方法用于性能的提升
            prefix = ["model.schedule.steps", "unique_id"]
            attributes = [func.attribute_name for func in rep_funcs]
            get_reports = attrgetter(*prefix + attributes)
        else:

            def get_reports(agent):
                _prefix = (agent.model.schedule.steps, agent.unique_id)
                reports = tuple(rep(agent) for rep in rep_funcs)
                return _prefix + reports

        agent_records = map(get_reports, model.schedule.agents)
        return agent_records

    def collect(self, model):
        # 收集给定模型的所有数据
        if self.model_reporters:
            for var, reporter in self.model_reporters.items():
                # Check if Lambda Type
                if isinstance(reporter, types.LambdaType):
                    self.model_vars[var].append(reporter(model))
                # Check if model attribute
                elif isinstance(reporter, str):
                    self.model_vars[var].append(getattr(model, reporter, None))
                # Check if function with arguments
                elif isinstance(reporter, list):
                    self.model_vars[var].append(reporter[0](*reporter[1]))
                else:
                    self.model_vars[var].append(reporter())

        if self.agent_reporters:
            agent_records = self._record_agents(model)
            self._agent_records[model.schedule.steps] = list(agent_records)

    def add_table_row(self, table_name, row, ignore_missing=False):
        """
        向特定表中添加行字典
        :param table_name: 将要添加行的表
        :param row: 一个字典，格式为{column_name: value...}
        :param ignore_missing: 如果为True，将所有缺失的行填为None
                                如果为False，如果有任意一行的值缺失，则会报错
        """
        if table_name not in self.tables:
            raise Exception("表不存在！")

        for column in self.tables[table_name]:
            if column in row:
                self.tables[table_name][column].append(row[column])
            elif ignore_missing:
                self.tables[table_name][column].append(None)
            else:
                raise Exception("无法插入缺少列的行！")

    def get_model_vars_dataframe(self):
        """
        通过模型变量创建一个pandas的DataFrame
        这个DataFrame对于模型变量只有一列，并且索引值（隐式的）为模型的tick
        """
        # 判断self.model_reporters字典是否为空，若果是则抛出异常
        if not self.model_reporters:
            raise UserWarning(
                "在数据收集部分没有模型数据，返回一个空的数据框架！"
            )

        return pd.DataFrame(self.model_vars)

    def get_agent_vars_dataframe(self):
        """
        通过agent变量创建一个pandas的DataFrame
        这个DataFrame对于模型变量只有一列，有额外的两列分别为tick和agent_id
        """
        # 判断self.agent_reporters字典是否为空，若果是则抛出异常
        if not self.agent_reporters:
            raise UserWarning(
                "在数据收集部分没有agent数据，返回一个空的数据框架！"
            )

        all_records = itertools.chain.from_iterable(self._agent_records.values())
        rep_names = list(self.agent_reporters)

        df = pd.DataFrame.from_records(
            data=all_records,
            columns=["Step", "AgentID", *rep_names],
            index=["Step", "AgentID"]
        )
        return df

    def get_table_dataframe(self, table_name):
        """
        通过一个特定的表格创建一个pandas的DataFrame
        这个DataFrame对于模型变量只有一列，有额外的两列分别为tick和agent_id
        """
        if table_name not in self.tables:
            raise Exception("没有此表！")
        return pd.DataFrame(self.tables[table_name])






