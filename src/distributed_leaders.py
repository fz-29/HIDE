__author__ = 'Shubham Dokania'

import random
import time

from helpers.point import Point
from helpers.collection import Collection, Leaders
from helpers import get_best_point

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
    def __init__(self, path_length=2.0, step_length=0.1, perturbation=0.4,
        num_iterations=10, dim=2, n_leaders=1, algo_type=1):
        random.seed()
        self.dim = dim
        self.algo_type = algo_type
        self.pathLength = path_length
        self.step = step_length
        self.perturbation = perturbation
        self.numIterations = num_iterations
        self.iteration = 0
        self.n_leaders = n_leaders
        self.population = Collection(dim=dim)
        self.leaders = Leaders(dim=self.dim, n_leaders=self.n_leaders, population=self.population)

    def generate_perturbation(self):
        p_vector = []
        for nx in range(self.dim):
            rnd = random.random()
            if rnd < self.perturbation:
                p_vector.append(1)
            else:
                if self.algo_type == 1:
                    vl = random.uniform(0.65, 0.77) * 1.11946659307 / self.dim
                else:
                    vl = 0
                p_vector.append(vl)

        return p_vector

    def get_leader(self):
        top_point = sorted(self.population.points, key=lambda x: x.z)[0]
        return top_point

    def iterate(self):
        self.leaders.update_leaders(self.population)

        for ix in range(len(self.population.points)):
            curr_point = self.population.points[ix]
            leader = self.leaders.get_leader(curr_point)[1]
            path_value = 0
            p_vec = self.generate_perturbation()
            new_points = []
            while path_value <= self.pathLength:
                new_point = Point(dim=self.dim)
                for dx in range(new_point.dim):
                    new_point.coords[dx] = curr_point.coords[dx] + (leader.coords[dx] - curr_point.coords[
                        dx]) * path_value * p_vec[dx]
                new_point.evaluate_point()
                new_points.append(new_point)
                path_value += self.step
            self.population.points[ix] = get_best_point(new_points)
        self.iteration += 1

    def simulate(self):
        pnt = get_best_point(self.population.points)
        # print('best value of: ' + str(pnt.z) + ' at ' + str(pnt.coords)
        print('Initial best value of: ' + str(pnt.z))
        while self.iteration < self.numIterations:
            self.iterate()
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
        soma = DL(num_iterations=1000, dim=50, algo_type=0)
        val += soma.simulate()
        if print_time:
            print(time.clock() - start)

    print("Final average of all runs: "), (val / number_of_runs)
