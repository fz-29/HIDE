__author__ = ''

import copy
import random
import time
import numpy as np

from helpers.collection import Collection, get_average_z, get_visualization
from helpers import get_best_point, get_best_point_PSODE


class PSO_DE(object):
    def __init__(self, dim=2, num_iterations=10, phi_p=2.00, phi_g=2.00, w=0.7, CR=0.48, F=0.5, population_size=40, print_status=False, visualize=False, f_id=1):
        random.seed()
        self.f_id = f_id
        self.visualize = visualize
        self.print_status = print_status
        self.population_size = population_size
        self.dim = dim       
        self.num_iterations = num_iterations
        self.iteration = 0
        #DE PARAMS
        self.CR = CR
        self.F = F
        self.data = []                
        #PSO PARAMS
        self.phi_p = phi_p
        self.phi_g = phi_g
        self.w = w
        #POPULATIONS
        self.population1 = Collection(dim=dim, num_points=(self.population_size)/2, f_id=self.f_id) #DE
        self.population2 = Collection(dim=dim, num_points=(self.population_size)/2, f_id=self.f_id) #PSO

    def iterate(self):
        ## DE

        
        l = get_best_point_PSODE(self.population1.points, self.population2.points)
        self.data.append(l.z)
        for ix in xrange(self.population1.num_points):
            x = self.population1.points[ix]
            [a, b, c] = random.sample(self.population1.points, 3)
            
            while x == a or x == b or x == c:
                [a, b, c] = random.sample(self.population1.points, 3)
            R = random.random() * x.dim
            y = copy.deepcopy(x)
            
            for iy in xrange(self.dim):
                ri = random.random()
                if ri < self.CR or iy == R:
                    y.coords[iy] = l.coords[iy] + self.F * (b.coords[iy] - c.coords[iy])

            y.evaluate_point()
            #shift.append((np.asarray(y.coords) - np.asarray(x.coords)).mean())
            if y.z < x.z:
                self.population1.points[ix] = y

        g_best = copy.deepcopy(get_best_point_PSODE(self.population1.points, self.population2.points))        
        
        ## PSO
        
        for i in xrange(self.population2.num_points):            
            current_point = self.population2.points[i]
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
        
        self.iteration += 1
        


    def simulate(self):
        pnt = get_best_point_PSODE(self.population1.points, self.population2.points)
        
        print("Initial best value: " + str(pnt.z))

        while self.iteration < self.num_iterations:
            if self.print_status == True and self.iteration%10 == 0:
                pnt = get_best_point_PSODE(self.population1.points, self.population2.points)
                print self.iteration, pnt.z, (get_average_z(self.population1)+get_average_z(self.population2))/2
            self.iterate()
        pnt = get_best_point_PSODE(self.population1.points, self.population2.points)
        self.data.append(pnt.z)
        print("Final best value: " + str(pnt.z))
        # print pnt.coords
        return pnt.z, np.asarray(self.data)


if __name__ == '__main__':
    number_of_runs = 1
    val = 0
    print_time = True

    for i in xrange(number_of_runs):
        start = time.clock()
        de = PSO_DE(dim=10, population_size=100, num_iterations=200, phi_p=2.00, phi_g=2.00, w=0.7, CR=0.48, F=0.5, print_status=True, visualize=False, f_id=21)
        val += de.simulate()[0]
        if print_time:
            print("")
            print(time.clock() - start)
    print("Final average of all runs: "), (val / number_of_runs)