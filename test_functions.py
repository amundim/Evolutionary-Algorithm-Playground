import numpy as np
import random
import math


def ackley_function(transposed_decimal_pop_input):
    """Ackley Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:

        ackley = 0
        sum_1 = 0
        sum_2 = 0
        for xi in individual:
            sum_1 = sum_1 + xi**2
            sum_2 = sum_2 + math.cos(2*math.pi*xi)
        term_1 = -20*math.exp(-0.2*(math.sqrt(1/len(individual)*sum_1)))
        term_2 = - math.exp((1/len(individual))*sum_2)
        ackley = term_1 + term_2 + 20 + math.exp(1)
        y.append(ackley)
    return y


def bohachevsky_function(transposed_decimal_pop_input):
    """Bohachevsky Test Function"""
    
    y = []
    for individual in transposed_decimal_pop_input:

        bohachevsky = 0
        term_1 = 0
        term_2 = 0

        for idx, xi in enumerate(individual):
            if idx == (len(individual)-1):
                break
            term_1 = (xi**2 + 2*((individual[idx + 1])**2)-0.3*math.cos(3*math.pi*xi))
            term_2 = (-0.4*math.cos(4*math.pi*individual[idx + 1]) + 0.7)
            bohachevsky = bohachevsky + (term_1 + term_2)

        y.append(bohachevsky)
    return y


def de_jong_step_a_function(transposed_decimal_pop_input):
    """De Jong Step - A Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:

        de_jong_step = 0

        for xi in individual:
            de_jong_step = de_jong_step + abs(round(xi))  # (abs) was used to adjust the function for minimization
        y.append(de_jong_step)
    return y


def de_jong_step_b_function(transposed_decimal_pop_input):
    """De Jong Step - B Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:

        de_jong_step_func_4 = 0
        term_1 = 0
        term_2 = random.gauss(0, 1)

        for idx, xi in enumerate(individual):
            term_1 = term_1 + idx*(xi**4)
        de_jong_step_func_4 = term_1 + term_2
        y.append(de_jong_step_func_4)
    return y


def griewangk_function(transposed_decimal_pop_input):
    """Griewangk Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:

        griewangk = 0
        term_1 = 0
        term_2 = 1

        for idx, xi in enumerate(individual):
            term_1 = term_1 + (xi**2)/4000
            term_2 = term_2 * math.cos(xi/(math.sqrt(idx + 1)))
        griewangk = 1 + term_1 - term_2
        y.append(griewangk)
    return y


def rastrigin_function(transposed_decimal_pop_input):
    """Rastrigin Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:
        rastrigin = 0
        term_1 = 10*len(individual)
        term_2 = 0

        for xi in individual:
            term_2 = term_2 + (xi**2)-10*(math.cos(2*xi*(math.pi)))
        rastrigin = term_1 + term_2
        y.append(rastrigin)
    return y


def rosenbrock_function(transposed_decimal_pop_input):
    """Rosenbrock Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:
        rosenbrock = 0
        for idx, xi in enumerate(individual):
            if idx == (len(individual)-1):
                break
            rosenbrock = rosenbrock + (100*(((xi**2)-individual[idx+1])**2)+((1-xi)**2))
        y.append(rosenbrock)
    return y


def schaffer_function(transposed_decimal_pop_input):
    """Schaffer Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:

        shaffer = 0
        parentheses = 0

        for xi in individual:
            parentheses = parentheses + xi**2
        term_1 = parentheses**0.25
        term_2 = (((math.sin(50*(parentheses**0.1)))**2)+1)
        schaffer = (term_1 * term_2)
        y.append(schaffer)
    return y


def schwefel_a_function(transposed_decimal_pop_input):
    """Schwefel - A Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:
        schwefel = 0
        for xi in individual:
            schwefel = schwefel + ((xi + 0.5)**2)
        y.append(schwefel)
    return y


def schwefel_b_function(transposed_decimal_pop_input):
    """Schwefel - B Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:

        schwefel = 0

        for idx, xi in enumerate(individual):
            schwefel = schwefel + (-xi*(math.sin(math.sqrt(abs(xi)))))
#        y.append(schwefel/len(individual)) # The division is not part of the function. However, it might be helpful for some. It enables the same result, independent of the number of inputs.
        y.append(schwefel)
    return y


def schwefels_pro_function(transposed_decimal_pop_input):
    """Schwefel's Pro Test Function"""

    y = []
    schwefels = 0
    for individual in transposed_decimal_pop_input:
        schwefels = 0
        term_2 = 0
        for idx, xi in enumerate(individual):
            j = 0
            term_1 = 0
            while j <= idx:
                term_1 = term_1 + individual[j]
                j = j + 1
            term_2 = term_1**2
            schwefels = schwefels + term_2
        y.append(schwefels)
    return y


def sphere_function(transposed_decimal_pop_input):
    """Sphere Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:
        y.append(sum(np.square(individual)))
    return y


def untitled_function(transposed_decimal_pop_input):
    """Untitled Test Function"""

    y = []
    for individual in transposed_decimal_pop_input:
        untitled = 0
        parentheses = 0
        term_1 = 0
        term_2 = 1

        for xi in individual:
            parentheses = parentheses + xi**2
            term_2 = term_2*(math.cos(20*math.pi*xi))
        term_1 = parentheses/2
        untitled = term_1 - term_2 + 2
        y.append(untitled)
    return y
