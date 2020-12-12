from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
import matplotlib.pyplot as plt
from mesa.datacollection import DataCollector
import multilevel_mesa as mlm
from mesa.batchrunner import BatchRunner
from Helper_functions import *


class SellerAgent(Agent):
    def __init__(self, unique_id, model, wealth, know_how, price, goods, pos):
        super().__init__(unique_id, model)
        self.type = "seller"
        self.goods = goods
        self.wealth = wealth
        self.know_how = know_how
        self.price = price
        self.pos = pos
        self.exchange_goods = 0
        self.exchange_know_how = 0
        self.bought_goods = 0

    def __str__(self):
        return "Seller"

    def no_agent(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return len(this_cell) == 0

    def move(self):
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, moore=False)
                     if self.no_agent(i)]
        # mozliwosc pozostania na swoim miejscu
        neighbors.append(self.pos)
        new_position = self.random.choice(neighbors)
        if self.pos == new_position:
            pass
        else:
            self.model.grid.move_agent(self, new_position)
            self.pos == new_position


    def get_know_how(self):
        mate = calc_best_mate_know_how(self)
        flag_move_ok = 0
        if mate is not None:
            mate.wealth += mate.price
            self.wealth -= mate.price
            self.exchange_know_how += 1
            mate.exchange_know_how += 1
            self.know_how += 0.1
            flag_move_ok = 1
        return flag_move_ok

    def buy_goods(self):
        self.wealth -= self.price * 0.8
        self.goods += 1
        self.bought_goods += 1

    def substract_goods(self):
        self.goods -= 1

    def step(self):

        self.move()
        if self.goods < 2 and self.wealth > 0:
            self.buy_goods()
        elif self.wealth > 0:
            self.get_know_how()
        if self.goods > 0:
            self.substract_goods()



class SpecialistAgent(Agent):
    def __init__(self, unique_id, model, wealth, know_how, price, goods, pos):
        super().__init__(unique_id, model)
        self.type = "specialist"
        self.goods = goods
        self.wealth = wealth
        self.know_how = know_how
        self.price = price
        self.pos = pos
        self.exchange_goods = 0
        self.exchange_know_how = 0

    def __str__(self):
        return "Specialist"


    def no_agent(self, pos):
        this_cell = self.model.grid.get_cell_list_contents([pos])
        return len(this_cell) == 0


    def move(self):
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, \
                                                                 moore=False) \
                     if self.no_agent(i)]

        #mozliwosc pozostania na swoim miejscu
        neighbors.append(self.pos)

        new_position = self.random.choice(neighbors)
        if self.pos == new_position:
            pass
        else:
            self.model.grid.move_agent(self, new_position)
            self.pos = new_position


    def get_know_how(self):
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        flag_move_ok = 0
        for agent in this_cell:
            if agent.type == self.type:
                self.know_how += 0.1
                agent.know_how += 0.1
                self.exchange_know_how += 1
                agent.exchange_know_how += 1
                flag_move_ok = 1
        return flag_move_ok

    def buy_goods(self):
        mate = calc_best_mate_goods(self)
        flag_move_ok = 0
        if mate is not None:
            mate.wealth += mate.price
            self.wealth -= mate.price
            self.exchange_goods += 1
            mate.exchange_goods += 1
            self.goods += 1
            flag_move_ok = 1
        return flag_move_ok

    def substract_goods(self):
        self.goods -= 1

    def step(self):

        self.move()

        if self.goods < 2 and self.wealth > 0:
            self.buy_goods()

        self.get_know_how()

        if self.goods > 0:
            self.substract_goods()


class MoneyModel(Model):

    def __init__(self, T, S, width, height):
        self.num_agents = T + S
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.ml = mlm.MultiLevel_Mesa(self, group_to_net = True)

        # Create agents specialist
        for j in range(T):
            wealth = self.random.randrange(7, 15)
            know_how = self.random.randrange(1, 10)
            price = self.random.randrange(1, 3)
            goods = self.random.randrange(1, 3)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            b = SpecialistAgent(j, self, wealth, know_how, price, goods, (x, y))
            self.schedule.add(b)
            # Add the agent to a random grid cell
            self.ml.add(b)
            self.grid.place_agent(b, (x, y))


        # Create agents seller
        for i in range(S):
            wealth = self.random.randrange(4, 10)
            know_how = self.random.randrange(1, 10)
            price = self.random.randrange(1, 3)
            goods = self.random.randrange(1, 3)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            c = SellerAgent(i, self, wealth, know_how, price, goods, (x, y))
            self.schedule.add(c)
            # Add the agent to a random grid cell
            self.ml.add(c)
            self.grid.place_agent(c, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Gini wealth": compute_gini_wealth, "Gini know-how": compute_gini_know_how,
                         "Sum exchange-goods": compute_exchanges_goods,
                         "Sum exchange-know-how": compute_exchanges_know_how},
            agent_reporters={"Type": "type", "Wealth": "wealth", "Know-How": "know_how", "Price": "price",
                         "Goods": "goods"})


    def step(self):
        self.datacollector.collect(self)
        self.ml.net_group(link_type="trades", link_value=10)
        self.ml.step()



