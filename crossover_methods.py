import numpy as np
import random


def single_point_crossover_method(aux_pop_idxs_input, pop_input, crossover_probability_input, seed_input):
    """Single point crossover.
    In this implementation, every crossover will be performed in a different bit.
    """

    random.seed(seed_input)

    parents = np.random.randint(len(aux_pop_idxs_input), size=(2, int(len(aux_pop_idxs_input)/2)))

    idx_a = parents[0, :]
    idx_b = parents[1, :]

    # pop_matrix = flat_pop(pop_input)
    pop_matrix = pop_input

    individual_len = len(pop_matrix[0])

    aux_pop = []
    crossover = 0

    while crossover < (len(idx_a)):

        crossover_point = int(random.uniform(1, individual_len))
        crossover_probability = random.uniform(0, 1)

        parent_a = pop_matrix[idx_a[crossover]]
        parent_b = pop_matrix[idx_b[crossover]]

        # new_individual = []

        if crossover_probability_input >= crossover_probability:

            # Executes crossover
            offspring_a = parent_a[:crossover_point] + parent_b[crossover_point:]
            offspring_b = parent_b[:crossover_point] + parent_a[crossover_point:]

            aux_pop.append(offspring_a)
            aux_pop.append(offspring_b)

        else:  # In case of no crossover, parents are kept in the population.

            aux_pop.append(parent_a)
            aux_pop.append(parent_b)

        crossover = crossover + 1
    return aux_pop
