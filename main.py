from model import *
from simulation import *

population = []
N = 1000
population  = model(N)
cap1 = plot_capital_to_class(population,1000)

#create function that calculates capital per social class
run_simulation(population,100)
