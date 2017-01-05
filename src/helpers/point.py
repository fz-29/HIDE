__author__ = 'Shubham Dokania'

import copy

import numpy as np
import scipy as sp

from test_functions import evaluate


class Point:
    def __init__(self, dim=2, upper_limit=1, lower_limit=0):
        self.dim = dim
        self.coords = [0.0 for dx in range(self.dim)]
        self.z = None
        self.range_upper_limit = upper_limit
        self.range_lower_limit = lower_limit
        self.velocity = [0.0 for dx in range(self.dim)]
        self.p_best = [0.0 for dx in range(self.dim)]
        self.p_z = None
        self.k = 0.99
        self.v_max = self.k * abs(self.range_upper_limit - self.range_lower_limit) / 2.0
        for _dim in range(self.dim):
            self.velocity[_dim] = sp.random.uniform(-1.0 * self.v_max, self.v_max)
        self.evaluate_point()        

    def generate_random_point(self):
        co_od = []
        for _ in xrange(self.dim):
            co_od.append(np.random.uniform(self.range_lower_limit, self.range_upper_limit))

        self.coords = copy.deepcopy(co_od)
        self.p_best = copy.deepcopy(co_od)
        self.evaluate_point()

    def generate_neighbour(self):
        for ix in xrange(self.dim):
            offset = (2 * np.random.random() - 1.0) * 0.5
            self.coords[ix] += offset
            if self.coords[ix] < self.range_lower_limit:
                self.coords[ix] = self.range_lower_limit
            elif self.coords[ix] > self.range_upper_limit:
                self.coords[ix] = self.range_upper_limit

        self.z = evaluate(self.coords)

    def evaluate_point(self):
        self.z = evaluate(self.coords)
        self.p_z = evaluate(self.p_best)

    def clamp_velocity(self):
        for ix in xrange(self.dim):
            if self.velocity[ix] > self.v_max:
                self.velocity[ix] = self.v_max
            if self.velocity[ix] < -1.0 * self.v_max:
                self.velocity[ix] = -1.0 * self.v_max


if __name__ == '__main__':
    print("Point class defined in this script")
