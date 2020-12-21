import streamlit as st
import numpy as np
import random
import math
import json

import genetic_algorithm
import selection_methods
import crossover_methods
import mutation_methods
import elitism_methods

import particle_swarm

import test_functions

seed = 10

st.title('🦕 Evolutionary Algorithm Playground')

st.markdown('Here you can play with two evolutionary algorithms: Genetic Algorithm and Particle Swarm.')
st.markdown('The **Genetic Algorithm** is based on the evolutionary theory developed by Charles Darwin. Through generations, selection, crossover, mutation and elitism processes are applied to the population in order to find the fittest individual.')
st.markdown('**Particle Swarm** is a computational method which is based on the concept of swarms, such as fish shoals and bird flocks. It iteratively searches for the fittest individual within the cluster.')
st.markdown('Both algorithms are applied to **optimization problems**. An optimization problem is a problem of finding the _best_ solution from all feasible solutions. According to the problem, the best solution can be the arguments which **maximize** or **minimizes** the output of an **objective function**. Examples of maximization quantities are profits, performance, sales, growth, etc. Minimization quantities can be losses, material spending, and many others.')
st.markdown('Most of the time we do not have the answer to an objective function. However, there are some **Test Functions** which we do know its optimal values. They are great to evaluate the performance of optimization algorithms.')
st.markdown("It's important to highlight that the convergence of evolutionary algorithms is not guaranteed. Also, there is no certainty that it will find the optimal value. However, both algorithms are very powerful and they can perform really well for many complex problems with the tuning of a few parameters. Finding near-optimal values is very common.")
st.markdown('Below you can choose from a variety of test functions, define the number of dimensions, and choose the search interval. On the left sidebar, you can choose the evolutionary algorithm and tune all of its parameters.')

st.subheader('Frame the problem')

# Read JSON
with open('test_functions.json') as f:
    data = json.load(f)

test_functions_list = []
for key, value in data.items():
    test_functions_list.append(key)

func_pointer_dict = {
  'Ackley': test_functions.ackley_function,
  'Bohachevsky': test_functions.bohachevsky_function,
  'De Jong Step - A': test_functions.de_jong_step_a_function,
  'De Jong Step - B': test_functions.de_jong_step_b_function,
  'Griewangk': test_functions.griewangk_function,
  'Rastrigin': test_functions.rastrigin_function,
  'Rosenbrock': test_functions.rosenbrock_function,
  'Schaffer': test_functions.schaffer_function,
  'Schwefel - A': test_functions.schwefel_a_function,
  'Schwefel - B': test_functions.schwefel_b_function,
  "Schwefel's Pro 1.2": test_functions.schwefels_pro_function,
  'Sphere': test_functions.sphere_function,
  'Untitled': test_functions.untitled_function,
}

# Problem Statement and Parameters
function_input = st.selectbox('Choose test function', sorted(test_functions_list))

# Latex Equation
st.markdown('The test function is a minimization problem and it is given by:')
st.latex(data[function_input][0]['latex'])

# Optimal values and its arguments
st.markdown('The optimal value is: ' + str(data[function_input][0]['optimal']))

# Retrieve optimization type
optimization_type_input = data[function_input][0]['optimization_type']

# Max number of variables
if data[function_input][0]['max_variables'] > 3:
    max_var = 3
else:
    max_var = 2

n_variables = st.slider('Set number of variables/dimensions', 1, data[function_input][0]['max_variables'], max_var)

if n_variables <= 3:
    st.markdown("The optimal value is given by the following arguments: " + str([data[function_input][0]['arguments']] * n_variables))
else:
    st.markdown("The optimal value is given by the following arguments: [" + str(data[function_input][0]['arguments']) + ", ... , " + str(data[function_input][0]['arguments'])+"]")

# Interval size
interval = st.slider(
    'Choose the bounded constraints of the interval',
    data[function_input][0]['interval_min'],
    data[function_input][0]['interval_max'],
    (data[function_input][0]['interval_min'], data[function_input][0]['interval_max']))

st.markdown('Now that problem is set, please reach out to the sidebar to choose and tune your evolutionary algorithm.')

# Algorithm
algorithm = st.sidebar.selectbox(
     'Choose the evolutionary algorithm you want to play with',
     ['Genetic Algorithm', 'Particle Swarm'])

if algorithm == 'Genetic Algorithm':

    selection_pointer_dict = {
        'Roulette': selection_methods.roulette_selection_method,
        'Log Roulette': selection_methods.log_roulette_selection_method,
        'Tournament': selection_methods.tournament_selection_method,
    }

    crossover_pointer_dict = {
        'Single Point': crossover_methods.single_point_crossover_method,
    }

    mutation_pointer_dict = {
        'Single Point A': mutation_methods.single_point_a_mutation_method,
        'Single Point B': mutation_methods.single_point_b_mutation_method,
    }

    elitism_pointer_dict = {
        'Elitism': elitism_methods.elitism,
    }

    selection_method_input = st.sidebar.selectbox('Selection Method', ['Roulette', 'Log Roulette', 'Tournament'])
    selection_method_input = selection_pointer_dict[selection_method_input]

    crossover_method_input = st.sidebar.selectbox('Crossover Method', ['Single Point'])
    crossover_method_input = crossover_pointer_dict[crossover_method_input]

    crossover_probability_input = st.sidebar.slider('Crossover Probability', 0.0, 1.0, 0.1)

    mutation_method_input = st.sidebar.selectbox('Mutation Method', ['Single Point A', 'Single Point B'])
    mutation_method_input = mutation_pointer_dict[mutation_method_input]

    mutation_probability_input = st.sidebar.slider('Mutation Probability', 0.0, 1.0, 0.1)

    elitism_method_input = st.sidebar.selectbox('Elitism Method', ['Elitism'])
    elitism_method_input = elitism_pointer_dict[elitism_method_input]

    elitism_probability_input = st.sidebar.slider('Elitism Probability', 0.0, 1.0, 0.1)

    # Number of bits
    bits_number = st.sidebar.number_input('Choose how many bits will be used to represent each number', 1, 12, 4)

    n_individuals = st.sidebar.number_input('Set population size', 10, 1000, 100)

    n_max_gen = st.sidebar.number_input('Set number of generations', 10, 1000, 100)

elif algorithm == 'Particle Swarm':

    w_min_input = st.sidebar.slider('Initial Weight', 0.1, 1.0, 0.9)
    w_max_input = st.sidebar.slider('Final Weight', 0.1, 1.0, 0.2)

    c1 = st.sidebar.slider('Self Trust Parameter', 0.1, 10.0, 2.0)
    c2 = st.sidebar.slider('Neighbor Trust Parameter', 0.1, 10.0, 2.0)

    n_individuals = st.sidebar.number_input('Set swarm size', 10, 1000, 100)
    n_max_gen = st.sidebar.number_input('Set number of generations', 10, 1000, 100)

if st.sidebar.button('Run'):

    st.subheader('Optimization Results')

    if algorithm == 'Genetic Algorithm':
        optimization_result, arguments_result = genetic_algorithm.genetic_algorithm(interval, n_variables, bits_number, n_individuals, n_max_gen, selection_method_input, crossover_method_input, crossover_probability_input, mutation_method_input, mutation_probability_input, elitism_method_input, elitism_probability_input, func_pointer_dict[function_input], optimization_type_input, seed)

    elif algorithm == 'Particle Swarm':
        optimization_result, arguments_result = particle_swarm.pso(interval, n_variables, n_individuals, n_max_gen, func_pointer_dict[function_input], optimization_type_input, w_min_input, w_max_input, c1, c2, particle_swarm.clipper, seed)

    if optimization_type_input == 'min':
        st.markdown('The minimal value found by the algorithm was ' + optimization_result + '.')
    else:
        st.markdown('The maximum value found by the algorithm was ' + optimization_result + '.')
    st.markdown('The expected value was ' + str(data[function_input][0]['optimal']) + '.')
    st.markdown('The arguments which brought this result are ' + arguments_result + '.')
    st.markdown('The expected arguments were ' + str([data[function_input][0]['arguments']] * n_variables) + '.')

st.info("""
            Feel free to reach out if you want to learn more about evolutionary algorithms, colaborate with the project or hire me for any Data Science, Machine Learning and Optimization demand you might have.
            Developed by: [Alexandre Mundim](https://www.linkedin.com/in/alexandremundim/) | Source: [GitHub](https://github.com/amundim/Evolutionary-Algorithm-Playground)
        """)
