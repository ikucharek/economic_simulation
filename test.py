from mesa import Agent
from helper import *
from model import *


class MyAgent(Agent):
    def __init__(self, unique_id, model, wealth, know_how, price, goods, pos, typ):
        super().__init__(unique_id, model)
        self.typ = typ
        self.goods = goods
        self.wealth = wealth
        self.know_how = know_how
        self.price = price
        self.pos = pos
        self.starving = False
        self.exchange_goods = 0
        self.exchange_know_how = 0

    def move(self):
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, moore=True, include_center=True)]
        new_position = self.random.choice(neighbors)
        if self.pos == new_position:
            pass
        else:
            self.model.grid.move_agent(self, new_position)
            self.pos = new_position

    def get_know_how_sel(self):
        mate = calc_best_mate_know_how(self)
        if mate is not None:
            mate.wealth += mate.price
            self.wealth -= mate.price
            self.exchange_know_how += 1
            mate.exchange_know_how += 1
            self.know_how += 1
            mate.know_how += 0.05

    def get_know_how_spec(self):
        mates = self.model.grid.get_cell_list_contents([self.pos])
        for agent in mates:
            if agent.typ == self.typ and agent.pos == self.pos:
                self.know_how += 0.05
                self.exchange_know_how += 1
                agent.know_how += 0.05
                agent.exchange_know_how += 1

    def buy(self, reserve):
        if self.goods < reserve and self.wealth > 0:
            self.model.demand += 1
            mate = calc_best_mate_goods(self)
            if mate is not None:
                mate.wealth += mate.price
                self.wealth -= mate.price
                self.exchange_goods += 1
                mate.exchange_goods += 1
                self.goods += 1
                mate.goods -= 1
                mate.know_how += 0.05

    def eat(self):
        self.goods -= self.model.substract

    def delivery(self):
        #dostawa moze nastapic lub nie co nie zalezy od sprzedawcy
        if wanna_deliver(self) is True and self.model.random.choice([True, False]) is True:
            self.goods += 1
        self.model.supply += self.goods

    def change_price_sd(self):
        collect_supply_demand(self.model)
        if check_supply_demand(self.model) > 1:
            self.price += 0.05
        elif check_supply_demand(self.model) < 1:
            if self.price > 0.3: #cena minimalna
                self.price -= 0.05

    def raise_price(self, value):
        self.price += value

    def check_stock_and_sale(self, value):
        self.wealth < 3
        if self.price > value and self.price > 0.3: #cena minimalna
            self.price -= value


    def standard_step(self, reserve, sale):
        self.move()
        if self.typ == 'specialist':
            self.get_know_how_spec()  # podziel sie know how z innymi agentami tego samego typu jesli sa w poblizu
            self.buy(reserve)
            if self.goods >= self.model.substract:
                self.eat()  # zjedz jesli masz wystarczajaca ilosc
                self.starving = False
            else:
                self.starving = True

        elif self.typ == 'seller':
            self.change_price_sd()  # sprawdzenie popytu,podazy i reg cen
            self.check_stock_and_sale(sale)
            if self.wealth > 4:  # jesli srodki na to pozwalaja to sprzedawca moze "ulepszyc" K-H
                self.get_know_how_sel()
            self.delivery()  # dostawa

    def step_scenario_1(self):
        if 40 <= self.model.iter <= 80:
            pass
        else:
            self.standard_step(1, 0.03)

    def step_scenario_2(self):
        if 40 <= self.model.iter <= 80:
            pass
        elif self.model.iter == 15:
            self.standard_step(1, 0.03)
            if self.typ == 'seller':
                self.raise_price(0.5) #podwyzka cen o X jednostki
        else:
            self.standard_step(1, 0.03)


    def step_scenario_3(self):
        if 40 <= self.model.iter <= 80:
            pass
        elif 20 <= self.model.iter < 40:
            self.standard_step(7, 0.03)#agenci robia wieksze zapasy
        else:
            self.standard_step(1, 0.03)


    def step(self):
        if self.model.scenario_1 is True:
            self.step_scenario_1()
        elif self.model.scenario_2 is True:
            self.step_scenario_2()
        elif self.model.scenario_3 is True:
            self.step_scenario_3()
        else:
            self.standard_step(1, 0.03)
