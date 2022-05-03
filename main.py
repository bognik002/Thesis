from AgentBasedModel.agents import ExchangeAgent, Random, Fundamentalist, Chartist, Universalist
from AgentBasedModel.simulator import Simulator
from AgentBasedModel.visualization import *


exchange = ExchangeAgent(volume=2000)
simulator = Simulator(**{
    'exchange': exchange,
    'traders': [Random(exchange, 2500, 25) for _ in range(20)]
})

simulator.simulate(1000)
info = simulator.info

plot_price(info)
