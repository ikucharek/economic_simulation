from statistics import median
from visualizations import *


def calc_best_mate_goods(agent):
    cellmates = agent.model.grid.get_cell_list_contents([agent.pos])
    value_best = 0
    best_mate = None
    for mate in cellmates:
        if mate.typ == 'seller' and mate.goods > 0:
            value = mate.know_how / mate.price
            if value > value_best and mate.price < agent.wealth:
                value_best = value
                best_mate = mate
    return best_mate


def calc_best_mate_know_how(agent):
    cellmates = agent.model.grid.get_cell_list_contents([agent.pos])
    value_best = 0
    best_mate = None
    for mate in cellmates:
        if mate.typ == 'specialist':
            value = mate.know_how / mate.price
            if value > value_best and mate.price < agent.wealth:
                value_best = value
                best_mate = mate
    return best_mate


def compute_exchanges_goods(model):
    agent_all = [agent.exchange_goods for agent in model.schedule.agents]
    G = sum(agent_all) / 2
    return G


def compute_exchanges_know_how(model):
    agent_all = [agent.exchange_know_how for agent in model.schedule.agents]
    KH = sum(agent_all) / 2
    return KH


def compute_gini_wealth(model):
    agents_wealth = [agent.wealth for agent in model.schedule.agents]
    x = sorted(agents_wealth)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)


def compute_gini_know_how(model):
    agent_know_hows = [agent.know_how for agent in model.schedule.agents]
    x = sorted(agent_know_hows)
    N = model.num_agents
    B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
    return (1 + (1 / N) - 2 * B)


def compute_know_how_increase(model):
    agents = [agent.know_how for agent in model.schedule.agents]
    return sum(agents)

def collect_supply_demand(model):
    x = 0
    if model.supply > 0:
        x = model.demand / model.supply
    else:
        x = 0
    model.sd_list.append(x)


def check_supply_demand(model):
    if model.sd is not None:
        return model.sd
    else:
        return 0


def wanna_deliver(agent):
    if agent.goods > 0:
        return False
    else:
        return True


def avg_price(model):
    sum_agents = 0
    price = 0
    for agent in model.schedule.agents:
        if agent.typ == 'seller':
            sum_agents += 1
            price += agent.price
    if sum_agents > 0:
        return format(round(price / sum_agents, 3), '.3f')
    else:
        return 0


def wealth_median(model):
    agents_wealth = [agent.wealth for agent in model.schedule.agents]
    return median(agents_wealth)
