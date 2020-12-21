import numpy as np
import random

def single_point_a_mutation_method(aux_pop_input, mutation_probability_input, seed_input):
    
    # Diferentemente da single_point_mutation, essa abordagem "passeia" por todos os indivíduos
    
    # Para cada bit de cada indivíduo (1)
    # Gera número aleatório entre 0 e 1 (2)
    # Se número aleatório for menor ou igual à probabilidade de mutação (3)
    # Inverte bit (4)
    # Insere indivíduo na população (5)

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
    # Seleciona quantidade de indivíduos igual à probabilidade de mutação (1)
    # Seleciona bit aleatório de variável aleatória (2)
    # Inverte bit (3)
    # Insere indivíduo na população (4)
    
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