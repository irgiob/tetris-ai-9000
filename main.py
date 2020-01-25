import numpy as np
from game_config import *
from play_with_ml import *
from genetic_algorithm import *

# Notes
# start at level 25 for training and level 15 for playing
# python3 -u  main.py | tee Output.txt

MODE = 'TRAIN' # TRAIN or PLAY
start_over = False # Set to False if continuing from existing data

def train():
    # initial variables
    sol_per_pop = 25
    num_weights = 4
    start_gen = 0

    pop_size = (sol_per_pop, num_weights)
    new_population = np.random.choice(np.arange(-1,1,step=0.01),size=pop_size,replace=True)
    
    # if continue training from previous session
    if start_over == False:
        parents = np.asarray(last_gen)
        offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
        offspring_mutation = mutation(offspring_crossover)
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation
        start_gen = 0

    num_generations = 50
    num_parents_mating = 6

    # use genetic algorithm for every generation
    for generation in range(start_gen,num_generations):
        print('##############        GENERATION ' + str(generation)+ '  ###############' )
        # Measuring the fitness of each chromosome in the population.
        fitness = cal_pop_fitness(new_population)
        print('#######  fittest chromosome in generation ' + str(generation) +' is having fitness value:  ', np.max(fitness))
        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(new_population, fitness, num_parents_mating)

        # Generating next generation using crossover.
        offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))

        # Adding some variations to the offspring using mutation.
        offspring_mutation = mutation(offspring_crossover)

        # Creating the new population based on the parents and offspring.
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation

def play():
    # weights from previous training
    weights = [-2.556,-0.665,2.194,-0.326]
    run_game(weights, display=True)

if __name__ == "__main__":
    if MODE == 'TRAIN':
        train()
    elif MODE == 'PLAY':
        play()