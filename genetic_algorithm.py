import numpy as np
import random
import math

import selection_methods
import crossover_methods
import mutation_methods
import elitism_methods
import test_functions

import streamlit as st

# Basic and Auxiliary Functions

# Group of basic functions, responsible for the processes of creating the ranges of variables and converting between binaries and decimals.
# Upon receiving the intervals and their respective bit numbers from the user, two dictionaries are created. These are used for converting between decimal and binary numbers and vice versa. Dictionaries have binary numbers in strings.
# The other functions of this group are also part of the conversion process, but receive arrays in their inputs and make the transformations to strings and vice versa.


def interval_creation(variables_input):  # Array with lower, upper intervals and number of bits

    global inverted_intervals

    variables_input = np.asmatrix(variables_input)
    intervals = []
    inverted_intervals = []

    for variable in variables_input:
        interval_max = float(np.asarray(variable[:, :2]).max())
        interval_min = float(np.asarray(variable[:, :2]).min())
        n_bits = int(variable[:, 2:])

        # Creating bins
        interval_size = interval_max - interval_min + 1
        n_representable_numbers = 2**n_bits
        bins_list = np.linspace(interval_min, interval_max, n_representable_numbers).tolist()

        # Creating a decimal-binary converter list

        binary_list = []
        binary_format = (str('#0'+str(n_bits+2)+'b'))
        i = 0
        while i < n_representable_numbers:
            binary_list.append(format(i, binary_format))
            i = i + 1

        interval = dict(zip(bins_list, binary_list))
        inverted_interval = {v: k for k, v in interval.items()}

        intervals.append(interval)
        inverted_intervals.append(inverted_interval)

    return intervals, inverted_intervals


def dec_bin_converter(values_input, dictionaries_input):
    converted_values = []

    for dictionary, line in enumerate(values_input):
        array = [*dictionaries_input[dictionary]]
        interval_max = max(array)
        interval_min = min(array)

        array = np.asarray(array)

        converted_values_per_variable = []

        for value in line:

            if (valor > interval_max) or (valor < interval_min):
                raise ValueError('Error. Value out of interval.')

            idx = (np.abs(array - value)).argmin()

            converted_values_per_variable.append(dictionaries_input[dictionary].get(array[idx]))

        converted_values.append(converted_values_per_variable)

    return converted_values


def bin_dec_converter(binary_input, dictionaries_input):

    dictionaries_input = inverted_intervals

    conveted_binaries = []

    for idx, line in enumerate(binary_input):

        converted_binaries_per_variable = []

        for binary in line:
            binary_format = str('#0'+str(len([*dictionaries_input[idx]][1]))+'b')
            binary = int(str(binary), 2)
            binary = format(binary, binary_format)

            if (2**(len(binary)-2)) > (len(dictionaries_input[idx])):
                raise ValueError('Error. Value out of interval.')
            else:
                converted_binaries_per_variable.append(dictionaries_input[idx].get(binary))

        conveted_binaries.append(converted_binaries_per_variable)

    return conveted_binaries


def bin_array_converter(binary_strings_input):

    binary_arrays = []

    for line in binary_strings_input:
        binary_arrays_per_variable = []

        for binary_string in line:
            binary_arrays_per_variable.append([int(character) for character in str(binary_string)[2:]])

        binary_arrays.append(binary_arrays_per_variable)

    return binary_arrays


def array_bin_converter(binary_arrays_input):

    binary_values = []

    for line in binary_arrays_input:
        binary_values_per_line = []
        for value in line:
            binary_values_per_line.append(('0b'+''.join(str(bit) for bit in value)))

        binary_values.append(binary_values_per_line)

    return binary_values


def decimal2binary(decimal_arrays_input, intervals_input):
    binary_strings = dec_bin_converter(decimal_arrays_input, intervals_input)
    binary_arrays = bin_array_converter(binary_strings)
    return binary_arrays


def binary2decimal(binary_arrays, inverted_intervals_input):
    binary_strings = array_bin_converter(binary_arrays)
    decimal_values = bin_dec_converter(binary_strings, inverted_intervals_input)
    return decimal_values


# Then, we present auxiliary functions used in the genetic algorithm. These include functions for transposing matrices, etc.
def transposed(matrix_input):
    matrix_array = np.asarray(matrix_input)
    return matrix_array.T


# General function: generates transposed vector of the population and applies selected function
def functions(function_input, decimal_pop_input):
    transposed_decimal_pop = transposed(decimal_pop_input)

    return function_input(transposed_decimal_pop)


def flat_pop(pop_input):

    n_individual = 0
    flat_pop = []

    while n_individual < len(pop_input[0]):
        individual = []
        n_variable = 0
        while n_variable < len(pop_input):
            for bit in (pop_input[n_variable][n_individual]):
                individual.append(bit)
            n_variable = n_variable + 1

        n_individual = n_individual + 1
        flat_pop.append(individual)

    return flat_pop


def unflat_pop(aux_pop_input, n_bits_array):

    unflat_pop = []
    unflat_variable = []

    for individual_idx, individual in enumerate(aux_pop_input):
        cum_count = 0
        for idx, variable in enumerate(n_bits_array):
            unflat_variable = []
            aux_count = 0
            while aux_count < variable:
                unflat_variable.append(aux_pop_input[individual_idx][cum_count])
                aux_count = aux_count + 1
                cum_count = cum_count + 1

            unflat_pop.append(unflat_variable)

    pop_output = []

    for idx, variable in enumerate(n_bits_array):
        storage_per_variable = []
        count = idx
        while count < len(unflat_pop):
            storage_per_variable.append(unflat_pop[count])
            count = count + len(n_bits_array)

        pop_output.append(storage_per_variable)

    return pop_output


# Population Initiation
def initiate_population(n_individuals_input, n_bits_array_input, seed_input):

    random.seed(seed_input)
    pop = []
    n_var = len(n_bits_array_input)

    for line in range(0, n_individuals_input):
        individual = []
        for column in range(0, sum(n_bits_array_input)):
            rndm = random.uniform(0, 1)
            individual.append(round(rndm))
        pop.append(individual)

    # Divide the population as follows:
    # pop_per_variable = [[individuals_variable_1], [individuals_variable_2], [individuals_variable_3], [individuals_variable_n]]

    start_bit = 0
    ending_bit = 0
    pop_per_variable = []

    for idx, n_bits in enumerate(n_bits_array_input):  # Separation of the population by variables
        ending_bit = start_bit + n_bits
        pop_per_variable.append((np.asarray(pop)[:, start_bit:ending_bit]).tolist())
        start_bit = start_bit + n_bits

    return pop_per_variable


def selection(selection_method_input, fx_input, optimization_type_input, n_individuals_input, seed_input):
    return selection_method_input(fx_input, optimization_type_input, n_individuals_input, seed_input)


def crossover(crossover_method_input, aux_pop_idxs_input, pop_input, crossover_probability_input, seed_input):
    return crossover_method_input(aux_pop_idxs_input, flat_pop(pop_input), crossover_probability_input, seed_input)


def mutation(mutation_method_input, aux_pop_input, mutation_probability_input, seed_input):
    return mutation_method_input(aux_pop_input, mutation_probability_input, seed_input)


def genetic_algorithm(interval, n_variables, bits_number, n_individuals, n_max_gen, selection_method_input, crossover_method_input, crossover_probability_input, mutation_method_input, mutation_probability_input, elitism_method_input, elitism_probability_input, function_input, optimization_type_input, seed):

    variables = []
    i = 0
    while i < n_variables:
        variables.append([min(interval), max(interval), bits_number])
        i = i + 1

    n_gen = 0

    intervals, inverted_intervals = interval_creation(variables)

    n_bits_array = np.asarray(variables)[:, 2].astype(int)

    results = []

    # Evolution
    pop = initiate_population(n_individuals, n_bits_array, seed)
    decimal_pop = binary2decimal(pop, inverted_intervals)
    aux_fx = functions(function_input, decimal_pop)

    progress_bar = st.progress(n_gen)

    while n_gen < n_max_gen:

        # (1) Backup of previous result (best individuals) for elitism
        # Capture of indexes and results with better performance

        n_elitism_individuals_input = int(elitism_probability_input*n_individuals)

        if optimization_type_input == 'max':
            fx_elite = sorted(aux_fx)[-int(n_elitism_individuals_input):]
            elite_idxs = np.argsort(aux_fx)[-int(n_elitism_individuals_input):]

        else:
            fx_elite = sorted(aux_fx)[:int(n_elitism_individuals_input)]
            elite_idxs = np.argsort(aux_fx)[:int(n_elitism_individuals_input)]

        # Capture the elements of the population with better performance
        pop_matrix_backup = flat_pop(pop)
        elite_pop_matrix_backup = []

        for elite_idx in elite_idxs:
            elite_pop_matrix_backup.append(pop_matrix_backup[elite_idx])

        # (2) Selection
        aux_pop_idxs = selection(selection_method_input, aux_fx, optimization_type_input, n_individuals, seed)

        # (3) Crossover
        aux_pop = crossover(crossover_method_input, aux_pop_idxs, pop, crossover_probability_input, seed)

        # (4) Mutation
        aux_pop = mutation(mutation_method_input, aux_pop, mutation_probability_input, seed)

        # (5) Partial evaluation, pre-elitism
        pop = unflat_pop(aux_pop, n_bits_array)
        decimal_pop = binary2decimal(pop, inverted_intervals)
        aux_fx = functions(function_input, decimal_pop)

        # (6) Elitism
        final_pop_matrix = elitism_method_input(fx_elite, elite_pop_matrix_backup, aux_fx, aux_pop, optimization_type_input, n_elitism_individuals_input)

        # (5) Final evaluation, post-elitism
        pop = unflat_pop(final_pop_matrix, n_bits_array)
        decimal_pop = binary2decimal(pop, inverted_intervals)
        aux_fx = functions(function_input, decimal_pop)

        # Results and Plotting
        if n_gen == 0:
            if optimization_type_input == 'max':
                last_rows = max(aux_fx)
            else:
                last_rows = min(aux_fx)

            chart = st.line_chart(np.array(last_rows))

        if optimization_type_input == 'max':
            results.append(max(aux_fx))
            new_rows = np.array([[max(aux_fx)]])

            if n_gen == (n_max_gen - 1):
                optimal_found = max(aux_fx)
                arguments = transposed(decimal_pop)[np.argmax(aux_fx)]

        else:
            results.append(min(aux_fx))
            new_rows = np.array([[min(aux_fx)]])

            if n_gen == (n_max_gen - 1):
                optimal_found = min(aux_fx)
                arguments = transposed(decimal_pop)[np.argmin(aux_fx)]

        chart.add_rows(new_rows)
        last_rows = new_rows

        progress_bar.progress((n_gen+1)/n_max_gen)
        n_gen = n_gen + 1

    return str(optimal_found), str(arguments)
