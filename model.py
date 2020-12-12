from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector
import csv
import numpy as np
from mesa.batchrunner import BatchRunner
from helper import *
from test import *


def clear_csv():
    filename = r'c:\Users\izabe\Desktop\wealth.csv'
    f = open(filename, "w+")
    f.close()


class MoneyModel(Model):

    def __init__(self, t, s, width, height, substract, scenario_1, scenario_2, scenario_3):
        self.num_specialists = t
        self.num_sellers = s
        self.sd_list = []
        self.sd = None
        self.num_agents = t + s
        self.grid = MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)
        self.running = True
        self.iter = 0
        self.substract = substract
        self.scenario_1 = scenario_1
        self.scenario_2 = scenario_2
        self.scenario_3 = scenario_3
        self.demand = 0
        self.supply = 0
        types = []

        clear_csv()

        for i in range(t):
            types.append('specialist')
        for j in range(s):
            types.append('seller')

        # Create agents specialist and sellers
        for k in range(t + s):
            wealth = self.random.uniform(6, 8)
            know_how = self.random.random()  # od 0 do 1
            price = self.random.random()  # od 0 do 1
            goods = self.random.randrange(1, 3)
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            a = MyAgent(k, self, wealth, know_how, price, goods, (x, y), types[k])
            self.schedule.add(a)
            self.grid.place_agent(a, (x, y))

        self.datacollector = DataCollector(
            model_reporters={"Gini wealth": compute_gini_wealth,
                             "Gini know-how": compute_gini_know_how,
                             "Avg Price": avg_price,
                             "Sum exchange-goods": compute_exchanges_goods,
                             "Sum exchange-know-how": compute_exchanges_know_how,
                             "Summary - know-how increase": compute_know_how_increase,
                             "Wealth median": wealth_median},

            agent_reporters={"Id": "unique_id", "Typ": "typ", "Wealth": "wealth", "Know-How": "know_how",
                             "Price": "price", "Goods": "goods"})

    def upload_csv(self):
        with open(r'c:\Users\izabe\Desktop\wealth.csv', 'a', newline='') as csvfile:
            fieldnames = ['Iter', 'Wealth median']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow({'Iter': self.iter, 'Wealth median': round(wealth_median(self), 4)})
            csvfile.close()

    def histogram(self):
        # histogram co 50 iteracji
        if (self.iter - 1) % 50 == 0:
            subplot_save(self)

    def save_supply_demand(self):
        if len(self.sd_list) > 0:
            x = self.sd_list[-1]
        else:
            x = 0
        self.sd = x
        self.sd_list = []

    def step(self):
        self.iter += 1
        self.demand = 0
        self.supply = 0
        self.upload_csv()
        self.histogram()
        self.save_supply_demand()
        self.datacollector.collect(self)
        self.schedule.step()