import numpy as np
from genetic_algorithm import *

# To output to file and terminal
# python3 -u  main.py | tee Output.txt

MODE = 'PLAY' # TRAIN or PLAY
start_over = False # Set to False if continuing from existing data

# Last Generation Data
last_gen = [
    [0.01,-3.422,2.015,-0.965],
    [-0.505,-3.221,1.05,-0.251],
    [-2.178,-2.636,0.524,-0.965],
    [-2.309,-1.654,0.524,-0.514],
    [-1.917,-2.636,0.524,-0.965],
    [-2.309,-3.221,1.05,-0.251]
]

# best weights from previous training
weights_1 = [-2.72,-2.731,0.259,-1.769]
weights_2 = [-1.91,-1.704,2.342,-0.498]

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
    weights = weights_2 # choose weight to use
    terminal_view = False # display scanned data in terminal
    run_game(weights, play_mode=True, display=terminal_view)

if __name__ == "__main__":
    if MODE == 'TRAIN':
        # start from play again screen
        train()
    elif MODE == 'PLAY':
        # start from pause screen
        play()