import numpy as np

def elitism(elite_fx_input, elite_pop_matrix_input, aux_fx_input, aux_pop_input, optimization_type_input, n_elitism_individuals_input):
    
    fx_concat = elite_fx_input + aux_fx_input
    aux_elite_idxs = np.argsort(fx_concat)
    
    pop_concat = elite_pop_matrix_input + aux_pop_input
    
    if optimization_type_input == 'max':
        final_elite_idxs = aux_elite_idxs[-int(len(pop_concat)-n_elitism_individuals_input):]

    else:
        final_elite_idxs = aux_elite_idxs[:int(len(pop_concat)-n_elitism_individuals_input)]
    
    final_pop_matrix = []
    
    for final_elite_idx in final_elite_idxs:
        final_pop_matrix.append(pop_concat[final_elite_idx])
    
    return final_pop_matrix