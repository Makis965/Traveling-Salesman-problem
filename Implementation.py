import math
import random
import numpy as np
import pandas as pan
import copy
import time

N = 10  # cities number
P = 250 # permutations amount
n = 0.8
pm = 0.2
Tmax = 1000

x_coords = [0, 3, 6, 7, 15, 10, 16, 5, 8, 1.5]
y_coords = [1, 2, 1, 4.5, -1, 2.5, 11, 6, 9, 12]


def Travelsalesman (N,P,n,pm,Tmax, x_coords = [], y_coords = []):

    # Costs summary
    def cost_f(data_frame, tour):
        cost_sum = 0
        for j in range(len(tour)):
            if j < 9:
                cost_sum = cost_sum + data_frame[tour[j]][tour[j + 1]]
            else:
                cost_sum = cost_sum + data_frame[tour[0]][tour[-1]]
        return cost_sum


    if len(x_coords) == 0 or len(y_coords) == 0:
        random.seed(100)
        np.random.seed(100)
        x_coords = np.random.rand(1, 10)
        y_coords = np.random.rand(1, 10)
        coords = np.concatenate((x_coords, y_coords))
    else:
        coords = np.concatenate(([x_coords], [y_coords]))

    # # #create population of P chromosomes => population of possible pi tours.

    cities = list(np.arange(0, N, 1))
    population = []

    for i in range(P):
        tour = random.sample(cities, N)
        population.append(tour)

    # # # define diagonal identity matrix: distances between each individual (chromosomes)

    # define distances matrix

    distance_matrix = np.zeros((N, N))

    for i in range(10):
        for k in range(10):
            distance_matrix[i, k] = math.sqrt((coords[0, i] - coords[0, k]) ** 2 + (coords[1, i] - coords[1, k]) ** 2)

    distance_matrix = pan.DataFrame(distance_matrix)

    # # # define selection operator

    for i in range(Tmax):

        list_of_costs = []

        for P_index in range(P):
            list_of_costs.append(cost_f(distance_matrix, population[P_index]))

        m_f = max(list_of_costs)
        t_i = m_f - list_of_costs
        t_s = sum(m_f - list_of_costs)

        # # # parents selection

        choosed_parents_pi = []
        parents = int(n * P)
        for _ in range(parents):
            r_value = random.uniform(0, t_s)
            ti_sum = 0
            for i in range(len(t_i)):
                ti_sum = ti_sum + t_i[i]
                if ti_sum > r_value:
                    choosed_parents_pi.append(population[i])
                    break

        # # # Crossover operation:

        # define crossover function

        def crossover_f(A1, A2, N):
            O1 = [N + 1] * N
            for i in range(N):
                if i == 0:
                    O1[0] = A1[0]
                    indexA2 = A2.index(A1[0])
                    O1[indexA2] = A1[indexA2]
                else:
                    indexA2 = A2.index(A1[indexA2])
                    if O1[indexA2] > N:
                        O1[indexA2] = A1[indexA2]
                    else:
                        break

            for id in range(N):
                if O1[id] > N:
                    O1[id] = A2[id]

            return O1

        # generate offsprings for each ancestor's pair

        offsprings_generation = []

        for pair in range(0, (len(choosed_parents_pi)), 2):
            A1 = choosed_parents_pi[pair]
            A2 = choosed_parents_pi[pair + 1]
            O1 = crossover_f(A1, A2, 10)
            O2 = crossover_f(A2, A1, 10)
            offsprings_generation.append(O1)
            offsprings_generation.append(O2)

        # # # mutation operator

        mutated_offsprings_generation = []
        for offspr in offsprings_generation:
            mutation_prop = random.random()
            if mutation_prop > pm:
                allel1 = random.randrange(1, N)
                allel2 = random.randrange(1, N)
                offspr_out = offspr
                offspr_out[allel1], offspr_out[allel2] = offspr_out[allel2], offspr_out[allel1]
                mutated_offsprings_generation.append(offspr_out)
            else:
                mutated_offsprings_generation.append(offspr)

        # # # defining new population

        fresh_pool = population + mutated_offsprings_generation
        fresh_cost = []

        for el in range(len(fresh_pool)):
            fresh_cost.append(cost_f(distance_matrix, fresh_pool[el]))

        # # # selecting new N individuals to population

        fresh_population = pan.DataFrame(zip(fresh_pool, fresh_cost))
        fresh_population_sorted = fresh_population.sort_values(by=1).head(P)
        fresh_population_sorted = fresh_population_sorted.iloc[:, 0].to_list()
        fresh_population_sorted = [list(l) for l in fresh_population_sorted]
        population = copy.deepcopy(fresh_population_sorted)

    optim_tour = fresh_population_sorted[0]

    import matplotlib.pyplot as plt


    plt.plot(x_coords, y_coords, "bo")

    for i in range(N):
        for k in range(1,N):
            plt.plot((x_coords[i],x_coords[k]),(y_coords[i],y_coords[k]), "gray", alpha = 0.1)

    new_cords_x = []
    new_cords_y = []
    for id in optim_tour:
        new_cords_x.append(x_coords[id])
        new_cords_y.append(y_coords[id])
    new_cords_x.append(new_cords_x[0])
    new_cords_y.append(new_cords_y[0])
    plt.plot(new_cords_x,new_cords_y)


    plt.show()



    return [optim_tour]


best_tour  = Travelsalesman(N,P,n,pm,Tmax, x_coords, y_coords)



