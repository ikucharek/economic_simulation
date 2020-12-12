from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule, TextElement
import numpy as np
from model import *
from helper import *
import seaborn as sns
import matplotlib.pyplot as plt


def histogram_data_wealth(typ, model):
    agents = [agent for agent in model.schedule.agents]
    list = []
    for agent in agents:
        if agent.typ == typ:
            list.append(agent.wealth)
    return list


def histogram_data_kh(typ, model):
    agents = [agent for agent in model.schedule.agents]
    list = []
    for agent in agents:
        if agent.typ == typ:
            list.append(agent.know_how)
    return list


# def subplot_save(model):
#     fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(11, 7))
#
#     grid = plt.GridSpec(2, 2, wspace=0.2, hspace=0.5)
#
#     ax1 = plt.subplot(grid[0, 0])
#     plt.hist(histogram_data_wealth('seller', model), bins=15, color='purple')
#     ax2 = plt.subplot(grid[0, 1:])
#     plt.hist(histogram_data_wealth('specialist', model), bins=15, color='skyblue')
#     ax3 = plt.subplot(grid[1, :1])
#     plt.hist(histogram_data_kh('seller', model), bins=15, color='orange')
#     ax4 = plt.subplot(grid[1, 1:])
#     plt.hist(histogram_data_kh('specialist', model), bins=15, color='red')
#
#     ax1.title.set_text('Wealth: sellers')
#     ax2.title.set_text('Weatlh: specialists')
#     ax3.title.set_text('Know-how: sellers')
#     ax4.title.set_text('Know-how: specialists')
#
#     fig.suptitle('\nIteration %i' % model.iter)
#
#     file_name = r'c:\Users\izabe\Desktop\fig_simu_%i' % model.iter
#     plt.savefig(file_name)
#     plt.close()

def starving_agents(model):
    agents = [agent for agent in model.schedule.agents]
    x = 0
    for elem in agents:
        print(elem.typ, elem.starving, elem.goods, elem.pos)
        if elem.typ == "specialist" and elem.starving is True:
            x += 1
    return x

class Starving(TextElement):
    def __init__(self):
        pass

    def render(self, model):
        x = starving_agents(model)
        return "Starving agents: " + str(x)


chart1 = ChartModule([{"Label": "Gini wealth",
                       "Color": "Black"}],
                     data_collector_name="datacollector")

chart2 = ChartModule([{"Label": "Sum exchange-goods",
                       "Color": "Black"}],
                     data_collector_name="datacollector")

chart3 = ChartModule([{"Label": "Sum exchange-know-how",
                       "Color": "Black"}],
                     data_collector_name="datacollector")

chart4 = ChartModule([{"Label": "Summary - know-how increase",
                       "Color": "Pink"}],
                     data_collector_name="datacollector")

chart5 = ChartModule([{"Label": "Avg Price",
                       "Color": "Pink"}],
                     data_collector_name="datacollector")


def make_density(stat, color, x_label, y_label, ax):
    # Draw the histogram and fit a density plot.
    sns.distplot(stat, bins=10, color=color, ax=ax, axlabel=x_label) #ax=ax, bins=10)

def subplot_save(model):
    stat_list = [histogram_data_wealth('seller', model), histogram_data_wealth('specialist', model),
                 histogram_data_kh('seller', model), histogram_data_kh('specialist', model)]
    x_label = ['Wealth: sellers', 'Wealth: specialists', 'Know-how: sellers', 'Know-how: specialists']

    ncols = 2
    nrows = 2
    fig, axes = plt.subplots(ncols=ncols, nrows=nrows, figsize=(ncols * 6, nrows * 5))
    colors = plt.cm.tab10.colors
    for ax, stat, color, label in zip(np.ravel(axes), stat_list, colors, x_label):
        make_density(stat, color, label, 'Number of agents', ax)

    title = '\nIteration %i' % model.iter
    title += '\nStarving %i' % starving_agents(model)
    fig.suptitle(title)


    file_name = r'c:\Users\izabe\Desktop\fig_simu_%i' % model.iter
    plt.savefig(file_name)
    plt.close()
