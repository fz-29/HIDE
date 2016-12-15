import numpy as np
import scipy as sp

INF = 1000000


class TestFunction:
    def __init__(self):
        pass

    def ackley(self, x):
        v = 0
        z = 0
        for i in range(len(x)):
            v += x[i] ** 2
            z += np.cos(2 * np.pi * x[i])

        return (-20 * np.exp(-0.2 * np.sqrt(v / len(x)))) - np.exp(z / len(x)) + np.e + 20.0

    def multi_sphere(self, x):
        v = 0
        for i in range(len(x)):
            v += (x[i] ** 2)
        return v

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
        v = 0
        for i in xrange(len(x)):
            v += np.random.random() * (x[i] ** i)

        return v

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
        z1 = self.multi_sphere(x) / 4000
        z2 = 1

        for ix in xrange(len(x)):
            z2 *= np.cos(x[ix] / np.sqrt(ix + 1))

        return 1 + z1 - z2


if __name__ == '__main__':
    x = []
    for _ in xrange(20):
        x.append(sp.random.uniform(1, 10))
    tf = TestFunction()
