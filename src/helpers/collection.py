__author__ = 'Shubham Dokania'

import copy
import numpy as np
from matplotlib import pyplot as plt

from point import Point


def get_average_z(population):
    pts = population.points
    avg = 0.0
    for ix in pts:
        avg += ix.z
    avg = float(avg)/len(pts)
    return avg

def get_visualization(population, plot_leaders=False, leaders=None):
    pts = population.points
    plt.ion()
    plt.clf()
    R = 20
    plt.xlim(-R, R)
    plt.ylim(-R, R)

    for p in pts:
        plt.scatter(p.coords[0], p.coords[1])
    
    if plot_leaders == True and leaders is not None:
        for pt in leaders.leaders:
            plt.scatter(pt.coords[0], pt.coords[1], c='r')
    plt.pause(0.05)


class Collection:
    def __init__(self, dim=2, num_points=50, upper_limit=10, lower_limit=-10, init_generate=True, f_id=1):
        self.points = []
        self.f_id = f_id
        self.num_points = num_points
        self.init_generate = init_generate
        self.dim = dim
        # If initial generation parameter is true, then generate collection
        if self.init_generate == True:
            for ix in xrange(num_points):
                new_point = Point(dim=dim, upper_limit=upper_limit,
                                  lower_limit=lower_limit, f_id=self.f_id)
                new_point.generate_random_point()
                self.points.append(copy.deepcopy(new_point))

    def generate_neighbour_collection(self):
        neighbour = copy.deepcopy(self)

        for ix in xrange(self.num_points):
            neighbour.points[ix].generate_neighbour()

        return neighbour


class Leaders:
    """
    The Leaders class just contains the co-ordinates for all the distributed leaders of the
    clusters and the location of the global leader (which is usually the best scoring
    individual or the individual with the best fitness score.). Aditionally, we can also store
    the information about the best performing leader throughout the evolutionary process
    in the best leader variable.
    """
    def __init__(self, dim=2, n_leaders=1, population=None, scoring_function=None, f_id=1):
        self.n_leaders = n_leaders
        self.f_id = f_id
        self.dim = dim
        if scoring_function == None:
            self.scoring_function = None    # Pass a default scoring function
        else:
            self.scoring_function = scoring_function
        self.leaders = []
        self.parent_leader = Point(dim=self.dim)
        self.parent_leader.generate_random_point()
        self.generate_leaders(self.parent_leader)

    def generate_leaders(self, center):
        self.leaders = []
        self.leaders.append(copy.deepcopy(center))
        mu = np.asarray(center.coords)
        #cov = (center.z / self.dim) * np.eye(self.dim)
        cov = 45.0 * np.eye(self.dim)

        data_pts = np.random.multivariate_normal(mu, cov, self.n_leaders-1)
        for ix in range(data_pts.shape[0]):
            lead_pt = Point(dim=self.dim, f_id=self.f_id)
            lead_pt.coords = list(data_pts[ix])
            lead_pt.evaluate_point()
            self.leaders.append(copy.deepcopy(lead_pt))

    def get_leader(self, pt):
        """
        This function accepts a point and computes the distance between
        the point and all the leaders and returns the leader which has the minimum distance
        from the point.
        """
        dist = []
        val = []
        for px in range(self.n_leaders):
            dist.append(self.calc_distance(pt, self.leaders[px]))
            val.append(self.leaders[px].z)
        dist = np.asarray(dist)
        best = dist.argmin()

        return best, self.leaders[best]

    def get_leader_2(self, pt):
        """
        This function accepts a point and computes the distance between
        the point and all the leaders and returns the leader which has the minimum distance
        from the point.
        """
        dist = []
        for px in range(self.n_leaders):
            dist.append(self.calc_distance(pt, self.leaders[px]))
        dist = np.asarray(dist)
        best_i = dist.argmin()
        np.delete(dist, best_i)
        best_i = dist.argmin()
        return best_i, self.leaders[best_i]

    def calc_distance(self, p1, p2):
        """
        Calculate the distance between two point objects
        using the distance metric defined in this function.
        Currently using the eucledian distance (Subject to change).
        """
        coords_01 = np.asarray(p1.coords)
        coords_02 = np.asarray(p2.coords)
        
        # return np.sqrt(abs(((coords_01**2 - coords_02**2))**1).sum())
        # return np.sqrt(abs((coords_01**2 - coords_02**2))).sum()
        return np.sqrt(abs(((coords_01 - coords_02))**2).sum())

    def update_leaders(self, population):
        """
        Takes a population of points and computes new leader co-ordinates
        based on the scoring function. This method saves all the new updates
        to the leaders in it's own object and doesn't return any value or
        object.
        """
        # clusters = [[] for ix in range(self.n_leaders)]
        # scores = [[] for ix in range(self.n_leaders)]
        for point in population.points:
            allocation = self.get_leader(point)
            lead = allocation[1]
            if point.z <= lead.z:
                # Update leader
                self.leaders[allocation[0]] = copy.deepcopy(point)
            else:
                pass

    def generate_population(self, population_size=10):
        cluster = []
        total_fitness = 0.0

        for lead in self.leaders:
            total_fitness += lead.z

        for lx in range(self.n_leaders):
            lead = self.leaders[lx]
            mean_lx = np.asarray(lead.coords)
            # print lead.z, self.dim
            cov_lx = np.eye(self.dim) * 10.0 #   / float(self.dim))
            num_pts = int((1.0 - (lead.z / total_fitness)) * population_size)
            dist = np.random.multivariate_normal(mean_lx, cov_lx, num_pts)
            for px in range(dist.shape[0]):
                pt = dist[px]
                new_pt = Point(dim=self.dim, f_id=self.f_id)
                new_pt.coords = list(pt)
                new_pt.evaluate_point()
                cluster.append(new_pt)

        # Create a new collection from these new points
        coll = Collection(dim=self.dim, num_points=len(cluster), init_generate=False)
        coll.points = cluster

        # Return the generated population
        return coll


if __name__ == '__main__':
    print("Collection classes defined in this script")
