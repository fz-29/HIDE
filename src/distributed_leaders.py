__author__ = 'Shubham Dokania'

import random
import time
import copy

from helpers.point import Point
from helpers.collection import Collection, Leaders, get_average_z, get_visualization
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
        CR=0.4, F=0.48, visualize=False, stats_freq=10, vec=None, f_id=1):
        random.seed()
        self.f_id = f_id
        self.vec = vec
        self.visualize = visualize
        self.stats_freq = stats_freq
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
        self.leaders = Leaders(dim=self.dim, n_leaders=self.n_leaders, f_id=f_id)
        self.population = self.leaders.generate_population(population_size=self.population_size)
        self.data = []

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
        self.data.append(l.z)
        # self.leaders.generate_leaders(pnt)
        # self.population = self.leaders.generate_population(self.population_size)
        shift = []
        for ix in range(self.population.num_points):
            l = get_best_point(self.population.points)
            x = self.population.points[ix]
            a = self.leaders.get_leader(x)[1]
            a2 = self.leaders.get_leader_2(x)[1]

            [b, c,d] = random.sample(self.population.points, 3)
            while x == b or x == c or x==d:
                [b, c,d] = random.sample(self.population.points, 3)

            R = random.random() * x.dim
            y = copy.deepcopy(x)
            #ri = random.random()

            for iy in xrange(x.dim):
                ri = random.random()


                P = 0.3750

                if ri<P:
                    y.coords[iy] = x.coords[iy] #+ self.F*(b.coords[iy] - c.coords[iy])
                    #y.coords[iy] = x.coords[iy]# + self.F*(b.coords[iy] - c.coords[iy])
                else:
                    if self.iteration>P/3*self.numIterations:
                        #y.coords[iy] = a.coords[iy] + self.F*(a.coords[iy] - x.coords[iy])
                        y.coords[iy] = a.coords[iy] + self.F*(x.coords[iy] - c.coords[iy]) #execution
                    else:
                        #y.coords[iy] = l.coords[iy] + self.F*(l.coords[iy]-a.coords[iy])
                        y.coords[iy] = l.coords[iy] + self.F*(a.coords[iy]-c.coords[iy])   #planning -> optimization of contraction and rela



                # if ri < self.CR or iy == R:
                # l = global best, a  = local leader, c = random 
                # y.coords[iy] = l.coords[iy] - self.F * (x.coords[iy] + c.coords[iy])
                # y.coords[iy] = l.coords[iy]  + self.F * (a.coords[iy] - x.coords[iy] - c.coords[iy])



                # E_g = 0.4*l.coords[iy] + 0.1*a.coords[iy]
                # E_l = 0.1*a.coords[iy] - 0.05*x.coords[iy]

                # y.coords[iy] = E_g + E_l - 0.5*c.coords[iy]
                # P = 0.3750
                # if False:
                #     if ri>P:
                #         y.coords[iy] = a.coords[iy] + self.F*(x.coords[iy]-c.coords[iy])
                #     else:
                #         y.coords[iy] = x.coords[iy] + self.F*(a.coords[iy] - c.coords[iy])
                # # if self.iteration <self.numIterations/5:
                # #     #2 Neighbour
                # #     # pass
                # #     if ri > P:
                # #         y.coords[iy] = 0.99*l.coords[iy] + self.F * (a.coords[iy] - x.coords[iy] - c.coords[iy]) + (self.F) * (a2.coords[iy] +  x.coords[iy] - c.coords[iy])
                # #     else:
                # #         y.coords[iy] = x.coords[iy]
                # else:
                #     #GOVT
                #     # pass
                #     #y.coords[iy] = l.coords[iy] + self.F*(a.coords[iy] - x.coords[iy])
                #     if ri > P:
                #         P1 = 0.02
                #         pr = np.random.random()
                #         pr2 = np.random.random()
                #         if self.iteration>P/3*self.numIterations:
                #             y.coords[iy] = a.coords[iy] + self.F*(x.coords[iy] - c.coords[iy] ) 
                #         else:
                #             y.coords[iy] = l.coords[iy] + self.F*(a.coords[iy]-c.coords[iy])   
                #             ##  y.coords[iy] = d.coords[iy] + self.F*(b.coords[iy]-c.coords[iy])   
                #             #y.coords[iy] = self.vec[0]*l.coords[iy]  + self.vec[1]*a.coords[iy] - self.vec[2]*x.coords[iy] - self.vec[3]*c.coords[iy]
                #     #elif ri>2*P:
                #         #y.coords[iy] = d.coords[iy] + self.F*(b.coords[iy]-c.coords[iy])
                #     else:
                #         y.coords[iy] = d.coords[iy] + self.F*(b.coords[iy] - c.coords[iy])  #+ #self.F*(c.coords[iy])
                # poor
                # y.coords[iy] = 1.0*self.CR*l.coords[iy] + self.F * (a.coords[iy] - x.coords[iy] - c.coords[iy]) - (self.F) * (a2.coords[iy] -  x.coords[iy] - c.coords[iy]);
            y.evaluate_point()
            shift.append((np.asarray(y.coords) - np.asarray(x.coords)).mean())

            if y.z < x.z:
                self.population.points[ix] = y
        self.iteration += 1
        # print np.asarray(shift).mean()

    def simulate(self):
        pnt = get_best_point(self.population.points)
        # print('best value of: ' + str(pnt.z) + ' at ' + str(pnt.coords)
        print('Initial best value of: ' + str(pnt.z))

        save_acc = 0
        sa_i = 0
        while self.iteration < self.numIterations:
            if self.print_status == True and self.iteration%self.stats_freq == 0:
                pnt = get_best_point(self.population.points)
                print self.iteration, pnt.z, get_average_z(self.population)
                
            self.iterate()
            if self.visualize == True and self.iteration%5==0:
                get_visualization(self.population, plot_leaders=True, leaders=self.leaders)
                
        pnt = get_best_point(self.population.points)
        # print('best value of: ' + str(pnt.z) + ' at ' + str(pnt.coords)
        print('Final best value of: ' + str(pnt.z))
        self.data.append(pnt.z)
        # print("")
        # print(pnt.coords)
        return pnt.z, np.asarray(self.data)


if __name__ == '__main__':
    number_of_runs = 10
    val = 0
    print_time = True

    for i in xrange(number_of_runs):
        start = time.clock()
        soma = DL(num_iterations=1000, dim=50, algo_type=0, n_leaders=5, population_size=25, print_status=True, stats_freq=100, visualize=False)#, vec=[0.85, 1.0, 1.0, 1.0])
        val += soma.simulate()[0]
        if print_time:
            print(time.clock() - start)

    print("Final average of all runs: "), (val / number_of_runs)
