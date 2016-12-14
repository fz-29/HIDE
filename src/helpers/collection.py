__author__ = 'Shubham Dokania'

import copy
import numpy as np

from point import Point


class Collection:
    def __init__(self, dim=2, num_points=10, upper_limit=10, lower_limit=-10):
        self.points = []
        self.num_points = num_points
        for ix in xrange(num_points):
            new_point = Point(dim=dim, upper_limit=upper_limit,
                              lower_limit=lower_limit)
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
    def __init__(self, dim=2, n_leaders=1, population=None, scoring_function=None):
        self.n_leaders = n_leaders
        self.dim = dim
        if scoring_function == None:
            self.scoring_function = None    # Pass a default scoring function
        else:
            self.scoring_function = scoring_function
        self.leaders = []
        for ix in range(self.n_leaders):
            pt = Point(dim=self.dim)
            pt.generate_random_point()
            self.leaders.append(copy.deepcopy(pt))
        self.population = population

    def get_leader(self, pt):
        """
        This function accepts a point and computes the distance between
        the point and all the leaders and returns the leader which has the minimum distance
        from the point.
        """
        dist = []
        for px in range(self.n_leaders):
            dist.append(self.calc_distance(pt, self.leaders[px]))
        dist = np.asarray(dist)
        best = dist.argmin()
        return best, self.leaders[best]

    def calc_distance(self, p1, p2):
        """
        Calculate the distance between two point objects
        using the distance metric defined in this function.
        Currently using the eucledian distance (Subject to change).
        """
        coords_01 = np.asarray(p1.coords)
        coords_02 = np.asarray(p2.coords)
        
        return np.sqrt(((coords_01 - coords_02)**2).sum())

    def update_leaders(self, population):
        """
        Takes a population of points and computes new leader co-ordinates
        based on the scoring function. This method saves all the new updates
        to the leaders in it's own object and doesn't return any value or
        object.
        """
        clusters = [[] for ix in range(self.n_leaders)]
        scores = [[] for ix in range(self.n_leaders)]
        for point in population.points:
            allocation = self.get_leader(point)
            clusters[allocation[0]].append(point)
            scores[allocation[0]].append(point.z)

        for sc in range(self.n_leaders):
            leader_score = np.asarray(scores[sc])
            self.leaders[sc] = clusters[sc][leader_score.argmin()]


if __name__ == '__main__':
    print("Collection classes defined in this script")
