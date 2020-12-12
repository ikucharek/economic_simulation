from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from model import *
from mesa.visualization.UserParam import UserSettableParameter
from visualizations import *
from visualizations import Starving


def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true"}
    if agent is None:
        return
    if agent.typ == 'specialist' and agent.starving is False:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.4
    elif agent.typ == 'seller' and agent.goods > 0:
        portrayal["Color"] = "purple"
        portrayal["Layer"] = 0
        portrayal["r"] = 0.6
    elif agent.typ == 'specialist' and agent.starving is True:
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 2
        portrayal["r"] = 0.3
    elif agent.typ == 'seller' and agent.goods <= 0:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 3
        portrayal["r"] = 0.1
    return portrayal


starving_element = Starving()

set_a = UserSettableParameter('checkbox', 'Scenario 1: lockdown agents from 40 to 80 iteration', value=False)

set_b = UserSettableParameter('checkbox', 'Scenario 2: sellers prepared for lockdown from 40 to 80 iteration', value=False)

set_c = UserSettableParameter('checkbox', 'Scenario 3: agents prepared for lockdown from 40 to 80 iteration', value=False)

set_seller = UserSettableParameter('number', 'Agent type seller', value=40)

set_spec = UserSettableParameter('number', 'Agent type specialist', value=40)

set_sub = UserSettableParameter("slider", "Consumed good per iteration", 0.05, 0.00, 0.5, 0.10)

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

server = ModularServer(MoneyModel,
                       [grid, starving_element, chart5, chart2, chart4, chart1],
                       "Economic Simulation",
                       {"t": set_spec, "s": set_seller, "width": 10, "height": 10,
                        "substract": set_sub,
                        "scenario_1": set_a,
                        "scenario_2": set_b,
                        "scenario_3": set_c})

server.port = 8521
