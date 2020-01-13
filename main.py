import numpy as np
from game_config import *
from play_with_ml import *
from genetic_algorithm import *

'''
To-Do List
1. Create all possible permutations for each piece
2. Create function for all possible combinations
3. Create function to create score for each decision
4. Finish up genetic algorithm functions
5. Test
'''

# TRAIN or PLAY
MODE = 'PLAY'
start_over = True

def train():
    sol_per_pop = 50
    num_inputs = 7
    num_outputs = 4
    num_weights = num_inputs * num_outputs

    pop_size = (sol_per_pop, num_weights)
    new_population = np.random.choice(np.arange(-1,1,step=0.01),size=pop_size,replace=True)
    
    if start_over == False:
        parents = np.asarray(last_gen)
        offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))
        offspring_mutation = mutation(offspring_crossover)
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation

    num_generations = 100
    num_parents_mating = 12

    for generation in range(num_generations):
        print('##############        GENERATION ' + str(generation)+ '  ###############' )
        # Measuring the fitness of each chromosome in the population.
        fitness = cal_pop_fitness(new_population)
        print('#######  fittest chromosome in gneneration ' + str(generation) +' is having fitness value:  ', np.max(fitness))
        # Selecting the best parents in the population for mating.
        parents = select_mating_pool(new_population, fitness, num_parents_mating)

        # Generating next generation using crossover.
        offspring_crossover = crossover(parents, offspring_size=(pop_size[0] - parents.shape[0], num_weights))

        # Adding some variations to the offsrping using mutation.
        offspring_mutation = mutation(offspring_crossover)

        # Creating the new population based on the parents and offspring.
        new_population[0:parents.shape[0], :] = parents
        new_population[parents.shape[0]:, :] = offspring_mutation

def play():
    weights = [0] * 28
    run_game(weights, display=True)

if __name__ == "__main__":
    if MODE = 'TRAIN':
        train()
    elif MODE = 'PLAY':
        play()