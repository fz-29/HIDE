__author__ = 'Shubham Dokania'

import numpy as np


def evaluate(point):
    test = Function()
    return test.sphere(point)


class Function:
    def __init__(self):
        pass

    def sphere(self, x):
        z = 0
        for i in xrange(len(x)):
            z += x[i] ** 2
        return z

    def ackley(self, x):
        z1, z2 = 0, 0

        for i in xrange(len(x)):
            z1 += x[i] ** 2
            z2 += np.cos(2.0 * np.pi * x[i])

        return (-20.0 * np.exp(-0.2 * np.sqrt(z1 / len(x)))) - np.exp(z2 / len(x)) + np.e + 20.0

    def rosenbrock(self, x):
        v = 0
        for i in xrange(len(x) - 1):
            v += 100 * (x[i + 1] - x[i] ** 2) ** 2 + (x[i] - 1) ** 2

        return v

    def rastrigin(self, x):
        v = 0

        for i in range(len(x)):
            v += (x[i] ** 2) - (10 * np.cos(2 * np.pi * x[i]))

        return (10 * len(x)) + v

    def stretchedVsine(self, x):
        v = 0
        for ix in xrange(len(x) - 1):
            v += ((x[ix + 1] ** 2 + x[ix] ** 2) ** 0.25) * (
            (np.sin(50 * (x[ix + 1] ** 2 + x[ix] ** 2) ** 0.1)) ** 2 + 1)
        return v

    def thirdDeJong(self, x):
        v = 0
        for i in xrange(len(x)):
            v += abs(x[i])

        return v

    def fourthDeJong(self, x):
        v = 0
        for i in xrange(len(x)):
            v += (i + 1) * (x[i] ** 4)

        return v

    def qing(self, x):
        v = 0
        for i in xrange(len(x)):
            v += (x[i] ** 2 - (i + 1)) ** 2

        return v

    def xinSheXang(self, x):
        z1 = 0.0
        z2 = 0.0
        for i in xrange(len(x)):
            z1 += abs(x[i])
            z2 += np.sin(x[i]**2)

        return z1 * np.exp(-1.0 * z2)

    def schwefel(self, x):
        v = self.multi_sphere(x)

        return v ** (np.sqrt(np.pi))

    def exponential(self, x):
        v = self.multi_sphere(x)

        return 1.0 - np.exp(-0.5 * v)

    def rotated_hef(self, x):
        v = 0
        for i in xrange(len(x)):
            k = 0
            for j in xrange(i):
                k += x[j] ** 2
            v += k

        return v

    def griewank(self, x):
        z1 = self.sphere(x) / 4000
        z2 = 1

        for ix in xrange(len(x)):
            z2 *= np.cos(x[ix] / np.sqrt(ix + 1))

        return 1 + z1 - z2


if __name__ == '__main__':
    print("A collection of several Test functions for optimizations")
