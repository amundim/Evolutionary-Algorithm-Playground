# Particle Swarm Optimization

import numpy as np
import random
import math

import test_functions

import streamlit as st


# Auxiliary functions
def initiate_population(variables_input, n_individuals_input):
    """Function to initiate the swarm population."""

    pop = []

    i = 0
    while i < n_individuals_input:
        individual = []
        for variable in variables_input:
            low = min(variable)
            high = max(variable)
            individual.append(random.uniform(low, high))
        pop.append(individual)
        i = i + 1
    return np.array(pop)


def treatment(pop_input, variables_input, treatment_method_input):
    """Modular function which receives the treatment method that will be applied for individuals which get out of the function borders."""
    return treatment_method_input(pop_input, variables_input)


def clipper(pop_input, variables_input):
    """Treatment function for individuals which get out of the function borders. This function specifically clips the individual values to the interval limit."""

    new_pop = []

    for individual in pop_input:
        for variable in variables_input:
            individual = np.where(individual < min(variable), min(variable), individual)
            individual = np.where(individual > max(variable), max(variable), individual)
        new_pop.append(individual.tolist())

    return np.array(new_pop)


def euclidean_distance(optimal_arg_input, args_input):
    """Euclidean distance metric computation."""

    dist = []
    for individual in args_input:
        dist.append(np.linalg.norm(np.array(optimal_arg_input) - np.array(individual)))

    return dist


def transposed(matrix_input):
    """Matrix transposer."""
    matrix_array = np.asarray(matrix_input)
    return matrix_array.T


# Main Function
def pso(intervals_input, n_variables_input, n_individuals_input, n_max_gen_input, function_input, optimization_type_input, w_max_input, w_min_input, c1, c2, treatment_method_input, seed):
    """Particle Swarm Optimization"""

    # Initializes variables
    i = 0
    variables_input = []

    while i < n_variables_input:
        variables_input.append([intervals_input[0], intervals_input[1]])
        i = i + 1

    optimal_arg_input = np.zeros((1, len(variables_input)))

    # Initializes population
    pop = initiate_population(variables_input, n_individuals_input)

    # Execution
    n_gen = 0
    fx = function_input(pop)
    x_best = pop

    if optimization_type_input == 'min':
        g_best = pop[np.argmin(fx)]
    else:
        g_best = pop[np.argmax(fx)]

    delta = (w_max_input - w_min_input)/(n_max_gen_input - n_gen)
    w = w_max_input

    r1 = random.uniform(0, 1)
    r2 = random.uniform(0, 1)

    speed_0 = np.random.rand(n_individuals_input, len(variables_input))

    cognitive_speed = c1*r1*(x_best - pop)
    social_speed = c2*r2*(g_best - pop)

    speed_1 = w*speed_0 + cognitive_speed + social_speed

    pop = np.add(pop, speed_1)

    if treatment_method_input is not None:
        pop = treatment(pop, variables_input, treatment_method_input)

    results = []
    euclidean_dist = []
    avg_euclidean_dist = []

    progress_bar = st.progress(n_gen)

    while n_gen < n_max_gen_input:

        fx = function_input(pop)

        if optimization_type_input == 'min':
            if min(fx) < (function_input([g_best])[0]):
                g_best = pop[np.argmin(fx)]

            gate = np.where(np.array(function_input(x_best)) < np.array(function_input(pop)), True, False)

        else:
            if max(fx) > (function_input([g_best])[0]):
                g_best = pop[np.argmax(fx)]

            gate = np.where(np.array(function_input(x_best)) > np.array(function_input(pop)), True, False)

        x_aux = []
        for idx, item in enumerate(gate):
            if item is True:
                x_aux.append(x_best[idx])
            else:
                x_aux.append(pop[idx])
        x_best = x_aux

        r1 = random.uniform(0, 1)
        r2 = random.uniform(0, 1)
        speed_0 = speed_1
        cognitive_speed = c1*r1*(x_best - pop)
        social_speed = c2*r2*(g_best - pop)
        speed_1 = w*speed_0 + cognitive_speed + social_speed
        pop = np.add(pop, speed_1)

        if treatment_method_input is not None:
            pop = treatment(pop, variables_input, treatment_method_input)

        # Results and Plotting
        if n_gen == 0:
            if optimization_type_input == 'max':
                last_rows = max(fx)
            else:
                last_rows = min(fx)

            chart = st.line_chart(np.array(last_rows))

        if optimization_type_input == 'max':
            results.append(max(fx))
            new_rows = np.array([[max(fx)]])

            if n_gen == (n_max_gen_input - 1):
                optimal_found = max(fx)
                arguments = pop[np.argmax(fx)]
                print('O valor máximo obtido foi', max(fx))
                print('Os valores numéricos de entrada que trouxeram esse resultado foram', pop[np.argmax(fx)])

        else:
            results.append(min(fx))
            new_rows = np.array([[min(fx)]])

            if n_gen == (n_max_gen_input - 1):
                optimal_found = min(fx)
                arguments = pop[np.argmin(fx)]
                print('O valor mínimo obtido foi', min(fx))
                print('Os valores numéricos de entrada que trouxeram esse resultado foram', pop[np.argmin(fx)])

        chart.add_rows(new_rows)
        last_rows = new_rows

        progress_bar.progress((n_gen+1)/n_max_gen_input)

        # Metrics
        euclidean_dist.append(np.min(euclidean_distance(optimal_arg_input, pop)))
        avg_euclidean_dist.append(np.mean(euclidean_distance(optimal_arg_input, pop)))

        w = w - delta
        n_gen = n_gen + 1

    return str(optimal_found), str(arguments)
