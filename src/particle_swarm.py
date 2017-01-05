__author__ = 'Shubham Dokania'

import random
import time
import copy

from helpers.point import Point
from helpers.collection import Collection, Leaders, get_average_z, get_visualization
from helpers import get_best_point

import numpy as np
import matplotlib.pyplot as plt


class PSO:
    def __init__(self, dim=2, num_iterations=20, phi_p=2.05, phi_g=2.05, w=0.7, population_size=10, print_status=False, visualize=False):
        random.seed()
        self.print_status = print_status
        self.visualize = visualize
        self.dim = dim
        self.phi_p = phi_p
        self.phi_g = phi_g
        self.w = w
        self.population_size = population_size
        self.population = Collection(dim=dim, num_points=self.population_size)
        self.num_iterations = num_iterations
        self.iteration = 0

    def iterate(self):
        g_best = copy.deepcopy(get_best_point(self.population.points))
        # print g_best.z
        # print max(g_best.velocity)

        for i in xrange(self.population_size):
            current_point = self.population.points[i]

            for _dim in range(self.dim):
                rp = np.random.uniform(0, 1)
                rg = np.random.uniform(0, 1)

                current_point.velocity[_dim] = self.w * (current_point.velocity[_dim]) + self.phi_p * rp * (
                    current_point.p_best[_dim] - current_point.coords[_dim]) + self.phi_g * rg * (
                    g_best.coords[_dim] - current_point.coords[_dim])

                current_point.clamp_velocity()

                current_point.coords[_dim] += current_point.velocity[_dim]

            current_point.evaluate_point()
            if current_point.z < current_point.p_z:
                current_point.p_best = copy.deepcopy(current_point.coords)
                current_point.evaluate_point()
                # if current_point.p_z < g_best.z:
                #     g_best = copy.deepcopy(current_point)
        self.iteration += 1

    def simulate(self):
        pnt = get_best_point(self.population.points)
        print("Initial best value: " + str(pnt.z))
        while self.iteration < self.num_iterations:
            if self.print_status == True and self.iteration%50 == 0:
                pnt = get_best_point(self.population.points)
                print pnt.z, get_average_z(self.population)
            self.iterate()
            if self.visualize == True and self.iteration%2==0:
                get_visualization(self.population)

        pnt = get_best_point(self.population.points)
        print("Final best value: " + str(pnt.z))
        return pnt.z


if __name__ == '__main__':
    import time

    n = 1
    val = 0
    best = []
    for ix in xrange(n):
        start = time.clock()
        # pso = PSO(dim=10, numIterations=500, phi_p=-0.6485, phi_g=1.6475, w=-0.6031)
        pso = PSO(dim=10, num_iterations=1000, phi_p=-0.6485, phi_g=1.6475, w=-0.6031, print_status=True, visualize=False, population_size=30)
        val = pso.simulate()
        best.append(val)
        print (time.clock() - start)

    best_sort = sorted(best)
    # print "Best Value: ", best_sort[0], best_sort[1], best_sort[2]