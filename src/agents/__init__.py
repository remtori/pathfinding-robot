from controller import controller

from .greedy import greedy
from .a_star import a_star
from .uniform_cost_search import uniform_cost_search

controller.addAlgorithm('Greedy', greedy)
controller.addAlgorithm('A Star', a_star)
controller.addAlgorithm('Uniform Cost Search', uniform_cost_search)
