import numpy as np
import random

def single_point_crossover_method(aux_pop_idxs_input, pop_input, crossover_probability_input, seed_input):
    
    random.seed(seed_input)

    parents =  np.random.randint(len(aux_pop_idxs_input), size=(2, int(len(aux_pop_idxs_input)/2)))

    idx_a = parents[0, :]
    idx_b = parents[1, :]

    # pop_matrix = flat_pop(pop_input)
    pop_matrix = pop_input

    individual_len = len(pop_matrix[0])

    aux_pop = []
    crossover = 0
        
    while crossover < (len(idx_a)):

        # Definições do cruzamento
        crossover_point = int(random.uniform(1, individual_len)) # Sorteio de ponto de corte. Na nossa implementação, cada cruzamento tem um ponto de corte diferente
        crossover_probability = random.uniform(0,1) # Se maior ou igual que a crossover_probability_input, define se haverá ou não cruzamento
        
        # Define pais
        parent_a = pop_matrix[idx_a[crossover]]
        parent_b = pop_matrix[idx_b[crossover]]

        # new_individual = [] # COMENTÁRIO A POSTERIORI

        # POSSIBILIDADE A: Se houver cruzamento
        if crossover_probability_input >= crossover_probability:   

            # Executa o cruzamento
            offspring_a = parent_a[:crossover_point] + parent_b[crossover_point:]
            offspring_b = parent_b[:crossover_point] + parent_a[crossover_point:]

            aux_pop.append(offspring_a)
            aux_pop.append(offspring_b)

        # POSSIBILIDADE B: Se não houver cruzamento passa os pais adiante
        else:

            aux_pop.append(parent_a)
            aux_pop.append(parent_b)

        crossover = crossover +  1 
    return aux_pop