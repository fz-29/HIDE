__author__ = 'Shubham Dokania'

import copy
import random
import time
import numpy as np

from helpers.collection import Collection, get_average_z, get_visualization
from helpers import get_best_point


class JADE(object):
    def __init__(self, num_iterations=10, dim=2, population_size=10, print_status=False, visualize=False, f_id=1, p=0.2, c=0.1):
        random.seed()
        self.visualize = visualize
        self.print_status = print_status
        self.num_iterations = num_iterations
        self.iteration = 0
        self.population_size = population_size
        self.f_id = f_id
        self.population = Collection(dim=dim, num_points=self.population_size, f_id=f_id)
        self.data = []
        self.mu_cr = 0.5
        self.mu_f = 0.5
        self.A = []
        self.c = c
        self.p = p

    def iterate(self):
        s_f = []
        s_cr = []

        l = get_best_point(self.population.points)
        self.data.append(l.z)
        for ix in xrange(self.population.num_points):
            CR = self.generate_CR()
            F = self.generate_F()
            
            x = self.population.points[ix]

            xp_best = random.choice(sorted(self.population.points, key=lambda x:x.z)[:int(self.population_size * self.p)])

            x_r1 = random.choice(self.population.points)
            while x_r1.coords == x.coords:
                x_r1 = random.choice(self.population.points)

            x_r2 = random.choice(self.population.points + self.A)
            while x_r2.coords == x.coords:
                x_r2 = random.choice(self.population.points + self.A)

            
            v = copy.deepcopy(x)

            for jx in xrange(x.dim):
                j_rand = np.random.randint(x.dim)

                if np.random.random() < CR or j_rand == jx:
                    v.coords[jx] = x.coords[jx] + F*(xp_best.coords[jx] - x.coords[jx]) + F*(x_r1.coords[jx] - x_r2.coords[jx])

            v.evaluate_point()
            if v.z < x.z:
                self.population.points[ix] = v
                self.A.append(x)
                s_f.append(F)
                s_cr.append(CR)
        self.iteration += 1
        while len(self.A) > self.population_size:
            self.A.pop(np.random.randint(len(self.A)))

        self.mu_cr = (1.0 - self.c)*self.mu_cr + self.c*self.mean_A(s_cr)
        self.mu_f = (1.0 - self.c)*self.mu_f + self.c*self.mean_L(s_f)
        # print np.asarray(shift).mean()


    def simulate(self):
        pnt = get_best_point(self.population.points)
        print("Initial best value: " + str(pnt.z))
        while self.iteration < self.num_iterations:
            if self.print_status == True and self.iteration%100 == 0:
                pnt = get_best_point(self.population.points)
                print self.iteration, pnt.z, get_average_z(self.population)
            self.iterate()
            if self.visualize == True and self.iteration%1==0:
                get_visualization(self.population)

        pnt = get_best_point(self.population.points)
        print("Final best value: " + str(pnt.z))
        self.data.append(pnt.z)
        # print pnt.coords
        return pnt.z, np.asarray(self.data)

    def generate_CR(self):
        return np.random.normal(self.mu_cr, 0.1)

    def generate_F(self):
        return np.random.normal(self.mu_f, 0.1)

    def mean_A(self, z):
        z = np.asarray(z)

        return z.mean()

    def mean_L(self, z):
        z = np.asarray(z)

        return (z**2).sum()/(float(z.sum()) + 1e-08)


if __name__ == '__main__':
    number_of_runs = 10
    val = 0
    print_time = True

    for i in xrange(number_of_runs):
        start = time.clock()
        de = JADE(num_iterations=1000, dim=10, population_size=50, print_status=True, visualize=False, f_id=10)
        val += de.simulate()[0]
        if print_time:
            print("")
            print(time.clock() - start)

    print("Final average of all runs: "), (val / number_of_runs)

