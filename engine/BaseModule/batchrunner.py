"""
控制模型批量运行
"""

import itertools
from functools import partial
from multiprocessing import Pool
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    Union,
)
from tqdm import tqdm
from BaseModule.model import Model


def batch_run(
        model_cls: Type[Model],
        parameters: Mapping[str, Union[Any, Iterable[Any]]],
        number_processes: Optional[int] = 1,
        iterations: int = 1,
        data_collection_period: int = -1,
        max_steps: int = 1000,
        display_progress: bool = True
) -> List[Dict[str, Any]]:
    """
    通过一系列的变量值批量运行模型
    :param model_cls: 批量运行的模型类
    :param parameters: 运行模型需要的模型变量字典
    :param number_processes: 进程数量，默认值为1.设置为None表明使用所有的CPU
    :param iterations: 每个变量结合的迭代次数，默认值为1
    :param data_collection_period: 每多少步之后收集数据，默认值为-1（一个周期结束）
    :param max_steps: 模型运行的最大步，默认值为1000
    :param display_progress: 显式批量运行的进程，默认值为True
    :return:
    """

    runs_list = []
    run_id = 0
    for iteration in range(iterations):
        for kwargs in _make_model_kwargs(parameters):
            runs_list.append((run_id, iteration, kwargs))
            run_id += 1

    process_func = partial(
        _model_run_func,
        model_cls,
        max_steps=max_steps,
        data_collection_period=data_collection_period
    )

    results: List[Dict[str, Any]] = []

    with tqdm(total=len(runs_list), disable=not display_progress) as pbar:
        if number_processes == 1:
            for run in runs_list:
                data = process_func(run)
                results.extend(data)
                pbar.update()
            else:
                with Pool(number_processes) as p:
                    for data in p.imap_unordered(process_func, runs_list):
                        results.extend(data)
                        pbar.update()

    return results


def _make_model_kwargs(
        parameters: Mapping[str, Union[Any, Iterable[Any]]]
) -> List[Dict[str, Any]]:
    """
    从参数字典中创建模型关键参数
    :param parameters: 每个模型变量名的一个或多个值
    :return: 所有关键变量结合的列表
    """
    parameter_list = []
    for param, values in parameters.items():
        if isinstance(values, str):
            # 由于该值仅为一个string，所以我们并不需要使用迭代器进行迭代
            all_values = [(param, values)]
        else:
            try:
                all_values = [(param, value) for value in values]
            except TypeError:
                all_values = [(param, values)]

        parameter_list.append(all_values)

    all_kwargs = itertools.product(*parameter_list)
    kwargs_list = [dict(kwargs) for kwargs in all_kwargs]
    return kwargs_list


def _model_run_func(
        model_cls: Type[Model],
        run: Tuple[int, int, Dict[str, Any]],
        max_steps: int,
        data_collection_period: int,
) -> List[Dict[str, Any]]:
    """
    运行单个模型并且收集模型和agent数据
    :param model_cls: 需要运行的模型类
    :param run:运行id，迭代号，此次运行的关键参数
    :param max_steps:模型的最大运行步数，默认值为1000
    :param data_collection_period:多少步之后开始收集数据
    :return:model_data, agent_data
    """
    run_id, iteration, kwargs = run
    model = model_cls(**kwargs)
    while model.running and model.schedule.steps <= max_steps:
        model.step()

    data = []

    steps = list(range(0, model.schedule.steps, data_collection_period))
    if not steps or steps[-1] != model.schedule.steps - 1:
        steps.append(model.schedule.steps - 1)

    for step in steps:
        model_data, all_agents_data = _collect_data(model, step)
        # 如果这里有agent_reporter, 那么为每个agent创建一个条目
        if all_agents_data:
            stepdata = [
                {
                    "RunId": run_id,
                    "iteration": iteration,
                    "Step": step,
                    **kwargs,
                    **model_data,
                    **agent_data
                }
                for agent_data in all_agents_data
            ]
        # 如果这里仅有模型数据, 那么为每一步创建一个条目
        else:
            stepdata = [
                {
                    "RunId": run_id,
                    "iteration": iteration,
                    "Step": step,
                    **kwargs,
                    **model_data,
                }
            ]
        data.extend(stepdata)
    return data


def _collect_data(
        model: Model,
        step: int
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """通过数据收集模块收集模型中的模型数据和agent数据"""
    dc = model.datacollector
    model_data = {param: values[step] for param, values in dc.model_vars.items()}

    all_agents_data = []
    raw_agent_data = dc._agent_records.get(step, [])
    for data in raw_agent_data:
        agent_dict = {"AgentID": data[1]}
        agent_dict.update(zip(dc.agent_reporters, data[2:]))
        all_agents_data.append(agent_dict)

    return model_data, all_agents_data





