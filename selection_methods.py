import numpy as np
import random

def roulette_selection_method(fx_input, optimization_type_input, n_individuals_input, seed_input):

    random.seed(seed_input)
    
    roulette_sum = sum(fx_input)
    roulette_sum = np.array(roulette_sum)
    roulette_mean = np.mean(fx_input)
    roulette_max = np.max(fx_input)
    
    if optimization_type_input == 'max': # Se max
        fi_over_roulette_sum = fx_input/roulette_sum
        prob_if_max = fi_over_roulette_sum
        roulette_cum_probability = np.cumsum(prob_if_max)  
    else: # Se min
        prob_if_min = ((roulette_sum/fx_input)/(sum(roulette_sum/fx_input)))
        roulette_cum_probability = np.cumsum(prob_if_min)  

    parents_idxs = []

    # Performa os trials:
    n_roulette_spin = 0
    while n_roulette_spin < n_individuals_input:
        idx = (np.abs(roulette_cum_probability - random.uniform(0, 1))).argmin()
        parents_idxs.append(idx)
        n_roulette_spin = n_roulette_spin + 1

    return parents_idxs


def log_roulette_selection_method(fx_input, optimization_type_input, n_individuals_input, seed_input):

    random.seed(seed_input)
    
    roulette_sum = sum(np.log(fx_input))
    roulette_sum = np.array(roulette_sum)
    roulette_mean = np.mean(np.log(fx_input))
    roulette_max = np.max(np.log(fx_input))
    
    if optimization_type_input == 'max': # Se max
        fi_over_roulette_sum = np.log(fx_input)/roulette_sum
        prob_if_max = fi_over_roulette_sum
        roulette_cum_probability = np.cumsum(prob_if_max)  
    else: # Se min
        prob_if_min = ((roulette_sum/np.log(fx_input))/(sum(roulette_sum/np.log(fx_input))))
        roulette_cum_probability = np.cumsum(prob_if_min)  

    parents_idxs = []

    # Performa os trials:
    n_roulette_spin = 0
    while n_roulette_spin < n_individuals_input:
        idx = (np.abs(roulette_cum_probability - random.uniform(0, 1))).argmin()
        parents_idxs.append(idx)
        n_roulette_spin = n_roulette_spin + 1

    return parents_idxs

def tournament_selection_method(fx_input, optimization_type_input, n_individuals_input, seed_input):
    # Gera dois arrays com números aleatórios   
    # Compara qual indivíduo tem a melhor performance conforme tipo de otimização

    random.seed(seed_input)
    
    parents =  np.random.randint(len(fx_input), size=(2, len(fx_input)))
    idx_a = parents[0, :]
    idx_b = parents[1, :]
    fx_a = np.array(fx_input)[idx_a.astype(int)]
    fx_b = np.array(fx_input)[idx_b.astype(int)]

    # se max:
    if optimization_type_input == 'max':
        selected = np.array(fx_a) > np.array(fx_b)
    # se min:
    else:
        selected = np.array(fx_a) < np.array(fx_b)

    parents_idxs = []
    for idx, item in enumerate(selected):
        if item == True:
            parents_idxs.append(idx_a[idx])
        else:
            parents_idxs.append(idx_b[idx])
            
    return parents_idxs