import numpy as np
import random


def single_point_a_mutation_method(aux_pop_input, mutation_probability_input, seed_input):
    """
    This approach runs through every individual.
    It evaluates every bit of the individual and inverts it if a random generated number is larger the mutation probability (previously set by the user). This approach allows multiple mutations per individual;

    For each bit of every individual (1)
    Generates a random number between 0 and 1 (2)
    If the random number is lower or equal to the mutation probability (3)
    Inverts bit (4)
    Add the individual to the population (5)
    """
    random.seed(seed_input)

    # (1)
    i = 0
    while i < len(aux_pop_input):
        b = 0
        while b < len(aux_pop_input[i]):
            # (2) e (3)
            if random.uniform(0, 1) <= mutation_probability_input:
                # (4) e (5)
                aux_pop_input[i][b] = int(not(aux_pop_input[i][b]))

            b = b + 1
        i = i + 1

    return aux_pop_input


def single_point_b_mutation_method(aux_pop_input, mutation_probability_input, seed_input):
    """
    In this approach, the number of individuals is the size of the population multiplied by the mutation probability.
    The individuals are selected (1)
    A random generated bit position is selected (2)
    Inverts bit (3)
    Add the individual to the population (4)
    """

    random.seed(seed_input)

    # (1)
    n_mutations = 0
    individual_len = len(aux_pop_input[0])

    while n_mutations < round(mutation_probability_input*len(aux_pop_input)):

        # (2)
        random_individual_idx = int(random.uniform(0, len(aux_pop_input)))

        # Seleção do bit aleatório
        random_bit_position = int(random.uniform(0, individual_len))

        random_bit_value = aux_pop_input[random_individual_idx][random_bit_position]

        # (3)
        if random_bit_value == 0:
            new_bit = 1
        else:
            new_bit = 0

        # (4)
        aux_pop_input[random_individual_idx][random_bit_position] = new_bit

        n_mutations = n_mutations + 1

    return aux_pop_input
