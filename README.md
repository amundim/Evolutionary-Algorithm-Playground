# Evolutionary-Algorithm-Playground
This web app allows the experimentation with two evolutionary approaches for optimization: Genetic Algorithm (GA) and Particle Swarm Optimization (PSO).


The Genetic Algorithm performs the following procedure:

  The search interval (set by the user) is converted to a binary representation (the number of representation bits is also set by the user).
  A new population is randomly built. Beyond the number of representation bits, it also considers the number of individuals and the dimension of the problem (both set by the user).
  The population is evaluated by the test function and the selection, crossover, mutation and elitism procedures are executed. This is iteratively repeated, until the number of generations is reached.
  
  In the Evolutionary Algorithm Playground, the following methods are implemented:\
  
   Selection:\
      - Roulette;\
      - Log Roulette: in this approach, the roulette probabilities are processed by a log function. It reduces the difference between individual's scores, enabling higher  diversity to the population.\
      - Tournament;\
     
   Crossover:\
      - Single Point;\
      
   Mutation:\
      - Single Point A: this approach runs through every individual. It evaluates every bit of the individual and inverts it if a random generated number is larger the mutation probability (previously set by the user). This approach allows multiple mutations per individual;\
      - Single Point B: in this approach, a number of individuals is selected. The number of individuals is the size of the population multiplied by the mutation probability (previously set by the user). Later, a random generated bit position is inverted;\
    
   Elistism:\
      - A number of individuals (given by the size of the population multiplied by the elitism probability) will remain to the next generation. This are the most near-optimal individuals. The same number of individuals will be dicarded. This are the less optimal individuals.\
     
     
The Particle Swarm Algorithm performs the following procedure:

  A population is build within the search interval (set by the user). Differently from the Genetic Algorithm, the population is countinuos. It also considers the number of individuals and the dimension of the problem (both set by the user).
  The individuals of the swarm-like population will be individually evaluated through the test function. After the evaluation, they will move according to the cognitive and social speeds. The speed is also influenced by a inertia weight (set by the user), which normally decreases through the evolutionary process. The cognitive speed is influenced by the Self Trust Parameter and the social speed is influenced by the Social Trust Parameter.
  This is iteratively repeated, until the number of generations is reached.
