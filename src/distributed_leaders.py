__author__ = 'Shubham Dokania'

import random
import time
import copy

from helpers.point import Point
from helpers.collection import Collection, Leaders, get_average_z
from helpers import get_best_point

import numpy as np
import matplotlib.pyplot as plt

"""
This algorithm consists of multiple leaders instead of one, which guides all the
points. Here, the multiple leaders are selected based on their fitness among a group
of agents in the population and each leader is then reinitialized after one time step
based on their fitness and distance between points.

Initially we create a leader object which consists the locations of all the leaders
from the given set of points that lie on the population. Then, for each evolutioinary step,
we compute distances (or scores) of points from each leader and decide which leader does the
aggent fall under.
After deciding the leader, we perform the optimization step which moves the point
towards the leader, and we do this for all the agents in the population.
After completion of one evolutionary step, we reinitialize the leaders based on the positions
of the current leaders and agents. Using the scoring function, we create new clusters and the
individual with the best fitness in each cluster is then called the new local leader.
"""


class DL(object):
    def __init__(self, path_length=1.0, step_length=0.1, perturbation=0.5,
        num_iterations=10, dim=2, n_leaders=1, algo_type=1, population_size=20, print_status=False,
        CR=0.4, F=0.48):
        random.seed()
        self.print_status = print_status
        self.dim = dim
        self.CR = CR
        self.F = F
        self.algo_type = algo_type
        self.pathLength = path_length
        self.step = step_length
        self.perturbation = perturbation
        self.numIterations = num_iterations
        self.iteration = 0
        self.n_leaders = n_leaders
        self.population_size = population_size
        self.leaders = Leaders(dim=self.dim, n_leaders=self.n_leaders)
        self.population = self.leaders.generate_population(population_size=self.population_size)

    def generate_perturbation(self):
        p_vector = []
        for nx in range(self.dim):
            rnd = random.random()
            if rnd < self.perturbation:
                p_vector.append(1.0)
            else:
                if self.algo_type == 1:
                    vl = random.uniform(0.650001, 0.770001) * 1.11946659307 / self.dim
                else:
                    vl = 0
                p_vector.append(vl)

        return p_vector

    def get_leader(self):
        top_point = sorted(self.population.points, key=lambda x: x.z)[0]
        return top_point

    def iterate(self):
        self.leaders.update_leaders(self.population)
        # Generate a new population
        l = get_best_point(self.population.points)
        # self.leaders.generate_leaders(pnt)
        # self.population = self.leaders.generate_population(self.population_size)
        
        for ix in range(self.population.num_points):
            x = self.population.points[ix]
            a = self.leaders.get_leader(x)[1]
            [b, c] = random.sample(self.population.points, 2)
            while x == b or x == c:
                [b, c] = random.sample(self.population.points, 2)

            R = random.random() * x.dim
            y = copy.deepcopy(x)

            for iy in xrange(x.dim):
                ri = random.random()

                # if ri < self.CR or iy == R:
                # l = global best, a  = local leader, c = random 
                y.coords[iy] = l.coords[iy] + self.F * (a.coords[iy] - x.coords[iy] - c.coords[iy])

            y.evaluate_point()
            if y.z < x.z:
                self.population.points[ix] = y
        self.iteration += 1

    def simulate(self):
        pnt = get_best_point(self.population.points)
        # print('best value of: ' + str(pnt.z) + ' at ' + str(pnt.coords)
        print('Initial best value of: ' + str(pnt.z))

        save_acc = 0
        sa_i = 0
        while self.iteration < self.numIterations:
            if self.print_status == True and self.iteration%50 == 0:
                pnt = get_best_point(self.population.points)
                print pnt.z, get_average_z(self.population)
                
            self.iterate()
            # if self.print_status == True and self.iteration%50 == 0:
            #     plt.ion()
            #     plt.clf()
                
            #     plt.scatter([p.coords[0] for p in self.population.points], [p.z for p in self.population.points])
            #     #plt.scatter([p.coords[0] for p in self.leaders.leaders], [p.z for p in self.leaders.leaders], c = 'r')

            #     plt.pause(0.05)
                
        pnt = get_best_point(self.population.points)
        # print('best value of: ' + str(pnt.z) + ' at ' + str(pnt.coords)
        print('Final best value of: ' + str(pnt.z))
        print("")
        return pnt.z


if __name__ == '__main__':
    number_of_runs = 10
    val = 0
    print_time = True

    for i in xrange(number_of_runs):
        start = time.clock()
        soma = DL(num_iterations=1000, dim=100, algo_type=0, n_leaders=5, population_size=25, print_status=True)
        val += soma.simulate()
        if print_time:
            print(time.clock() - start)

    print("Final average of all runs: "), (val / number_of_runs)
