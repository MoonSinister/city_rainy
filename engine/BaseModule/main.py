# 假设 BaseModule.model 和 BaseModule.physical_environment 是可用的模块
from BaseModule.model import Model
from BaseModule.time import BaseScheduler
from BaseModule.physical_environment import Position
from bus_agent import BusAgent
from random import Random




def main():
    model = Model()
    timesch=BaseScheduler(model)
    bounds = ((34.0, 35.0), (118.0, 119.0))
    agent1 = BusAgent(unique_id=1, model=model, bounds=bounds)
    agent1.pos = (34.5, 118.5)
    agent2 = BusAgent(unique_id=2, model=model, bounds=bounds)
    agent2.pos = (34.5, 118.5)
    timesch.add(agent1)
    timesch.add(agent2)

    for i in range(5):
        i=i+1
        timesch.step()


    print(1)
    # 初始化位置设置为范围内的一个点


    # 输出初始化状态
    print(f"Initial position: {agent1.pos}")
    print(f"Initial position: {agent2.pos}")




if __name__ == "__main__":
    main()
